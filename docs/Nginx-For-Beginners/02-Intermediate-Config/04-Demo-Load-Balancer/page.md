# desired rewrite:
rewrite ^/images/(.*)$ /pics/$1 permanent;
```

Open your browser to the site (port 80) and request `/images/pic10.jpg` to confirm the image is currently reachable. The demo site uses the Phantom template and contains a set of small picture files:

<Frame>
  <img alt="A screenshot of a clean webpage for the &#x22;Phantom&#x22; responsive site template, showing a large headline and brief paragraph beneath the logo. Below that is a grid of colorful square tiles labeled with words like &#x22;MAGNA,&#x22; &#x22;LOREM,&#x22; and &#x22;FEUGIAT.&#x22;" />
</Frame>

## 1. Prepare the filesystem

Make a copy of the existing `images` directory to `pics` so both directories exist on disk:

```bash theme={null}
# change to the web root
cd /var/www/html

# verify images directory exists
ls -l images/

# copy images/ to pics/
cp -R images/ pics/

# verify pics/ was created
ls -l
```

Example listing of `images/` (the files that will be served):

```text theme={null}
total 136
-rw-r--r-- 1 root root 1259 Feb 18 16:14 logo.svg
-rw-r--r-- 1 root root 6311 Feb 18 16:14 pic01.jpg
-rw-r--r-- 1 root root 6084 Feb 18 16:14 pic02.jpg
...
-rw-r--r-- 1 root root 6489 Feb 18 16:14 pic10.jpg
-rw-r--r-- 1 root root 6338 Feb 18 16:14 pic11.jpg
...
```

## 2. Add the rewrite rule to your Nginx site config

Edit your Nginx server block (for example `/etc/nginx/sites-available/example`) and add the `rewrite` directive inside the `location /` block, before `try_files`. The `^` anchors the match to the start of the path, `(.*)` captures the rest of the requested path, and `/pics/$1` inserts that captured portion into the new path. The `permanent` flag issues an HTTP 301.

```nginx theme={null}
# /etc/nginx/sites-available/example
server {
    listen 80;

    server_name example.com;

    root /var/www/html;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    location / {
        # Rewrite any /images/<path> to /pics/<path> permanently
        rewrite ^/images/(.*)$ /pics/$1 permanent;

        # First attempt to serve request as file, then as directory,
        # then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }
}
```

Notes on the regex:

* `^/images/(.*)$` — matches any URI starting with `/images/` and captures everything after the slash.
* `$1` — is the first capture group, representing whatever `(.*)` matched.
* Use more specific patterns if you need to limit matches (e.g., only `.jpg` or `.png`).

## 3. Test and reload Nginx

Always validate configuration before reloading:

```bash theme={null}
# test the config
sudo nginx -t

# if the test is successful, reload nginx
sudo nginx -s reload
```

A successful test returns:

```text theme={null}
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

## 4. Verify the redirect in a browser

Open a fresh browser window (or incognito) and request the old URL:

```text theme={null}
http://example.com/images/pic10.jpg
```

You should receive an HTTP 301 redirect to:

```text theme={null}
http://example.com/pics/pic10.jpg
```

and the image will load from the new `/pics/` location.

> **warning** Permanent redirects (HTTP 301) are cached aggressively by browsers and search engines. Use an incognito window or clear the cache when testing. If you need a temporary redirect while testing, use the `redirect` flag instead of `permanent`.

> **lightbulb** Test rewrite rules on a staging environment before applying them in production. Regular expressions in `rewrite` directives are powerful but easy to misconfigure.

## Quick reference — rewrite flags

| Flag        | Effect                                                  | When to use                                                                                     |
| ----------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `permanent` | Returns HTTP 301                                        | Use when the resource has permanently moved and you want clients/search engines to update links |
| `redirect`  | Returns HTTP 302                                        | Use for temporary moves or when testing before making permanent                                 |
| `last`      | Re-evaluates location with changed URI                  | Use if you want Nginx to search for a new matching location after rewrite                       |
| `break`     | Stops processing rewrite directives in current location | Use to stop rewrite processing without re-evaluating locations                                  |

For more details on `rewrite` and directives, see the official Nginx docs: [nginx rewrite module](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html).

That covers a basic permanent rewrite from `/images` to `/pics`. Adjust the regex and flags (`last`, `break`, `redirect`, `permanent`) to suit your specific routing and caching requirements.

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/329f508c-8da5-4a0a-ad7a-f9504ab5e4f7)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/7716ca0d-be85-45f9-a67a-11e298853b2b)


# Demo Load Balancer

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Demo-Load-Balancer/page

Configuring Nginx as a reverse proxy load balancer demonstrating round-robin, weighted round-robin and ip_hash sticky sessions with Apache backends

Welcome back. In this lesson we configure an Nginx reverse proxy to act as a load balancer and demonstrate three common balancing methods: round-robin (default), weighted round-robin, and `ip_hash` (simple sticky sessions). The demo uses two Apache backend servers to show how Nginx can proxy to other web servers (Apache, LiteSpeed, etc.).

<Frame>
  <img alt="A diagram titled &#x22;Algorithms: Round Robin&#x22; showing an NGINX load balancer sending traffic via a round-robin router to two Apache web servers labeled 1 and 2. The illustration visualizes evenly distributing requests across the web servers." />
</Frame>

Round-robin cycles requests evenly across the available backends (request 1 → backend A, request 2 → backend B, request 3 → backend A, and so on).

For weighted round-robin you assign weights to each backend so one receives proportionally more requests than the other.

<Frame>
  <img alt="A diagram showing an NGINX load balancer using a weighted round-robin algorithm to distribute traffic to two Apache web servers, with weights 10 and 1." />
</Frame>

The `ip_hash` method pins clients to a backend based on a hash of the client IP — useful for simple session stickiness (for example, shopping carts) when no shared session store is available.

<Frame>
  <img alt="A diagram showing an NGINX load balancer using IP-hash routing to distribute client requests across three web servers. Arrows indicate how the IP-hash maps clients to specific backend servers." />
</Frame>

## Environment overview

* One node serves as the Nginx load balancer (`nginx`).
* Two nodes run Apache and serve a simple HTML page (`node01` and `node02`).

Validate a backend’s site (example on `node01`):

```bash theme={null}
root@node01 ~ ➜  curl http://localhost
