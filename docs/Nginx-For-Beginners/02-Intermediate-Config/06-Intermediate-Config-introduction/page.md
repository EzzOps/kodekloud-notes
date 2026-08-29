# Upstream configuration
upstream hello_world {
    server 192.230.206.3:5000;
    server 192.230.206.6:5000;
}

# Default server configuration
server {
    listen 80;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name helloworld.com;

    location / {
        proxy_pass http://hello_world;
    }
}
```

Notes:

* The `upstream` block lists the backend Flask app IPs and port `5000`.
* `proxy_pass` points to the upstream name `http://hello_world`; Nginx will load-balance requests to the listed servers.

5. Enable the site and reload Nginx

Create a symlink to enable the site:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ ln -s /etc/nginx/sites-available/helloworld /etc/nginx/sites-enabled/helloworld
```

Always test the Nginx configuration before reloading:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

root@nginx /etc/nginx/sites-available ➜ nginx -s reload
```

6. Test reverse proxy behavior using the Host header

When testing directly on the reverse proxy host, include the `Host` header so Nginx matches `server_name helloworld.com`.

Example requests:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ curl --header "Host: helloworld.com" localhost
<h1>Hello, Human!</h1>[Not Authenticated]

root@nginx /etc/nginx/sites-available ➜ curl --header "Host: helloworld.com" localhost/foo
<h1>Foo page</h1><a href="/do-something?next=/foo">Do something and redirect</a>

root@nginx /etc/nginx/sites-available ➜ curl --header "Host: helloworld.com" localhost/bar
<h1>Bar page</h1><a href="/do-something?next=/bar">Do something and redirect</a>
```

All client requests are sent to Nginx on port 80; Nginx forwards them to the Flask backends on port 5000.

7. Simulate a backend failure

To simulate one backend being unavailable, comment out its `server` line in the `upstream` block and reload Nginx. The remaining backend will continue to serve traffic.

Example: comment out the second backend:

```nginx theme={null}
# Upstream configuration
upstream hello_world {
    server 192.230.206.3:5000;
    # server 192.230.206.6:5000;
}
```

Reload Nginx and test again:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ nginx -s reload
root@nginx /etc/nginx/sites-available ➜ curl --header "Host: helloworld.com" localhost
<h1>Hello, Human!</h1>[Not Authenticated]
```

The reverse proxy continues to function, routing requests to the available backend.

Best practices and next steps

* Consider adding `proxy_set_header` directives (e.g., `Host`, `X-Real-IP`, `X-Forwarded-For`) in the `location` block for proper client IP and host propagation. See Nginx proxy docs: [NGINX proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).
* For production, enable SSL/TLS on the Nginx host and redirect HTTP to HTTPS.
* Monitor backend health and use `max_fails`/`fail_timeout` or an upstream health-checking solution if you need automatic failover beyond simple server removal.

References

* [Nginx documentation — HTTP proxying](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
* [Flask documentation — Quickstart](https://flask.palletsprojects.com/en/latest/quickstart/)
* [UFW — Uncomplicated Firewall guide](https://help.ubuntu.com/community/UFW)

That's it for this demo on configuring a simple Nginx reverse proxy to forward requests to Flask applications running on port 5000.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/85497d1b-b7c7-46d0-a176-56ec8041abff" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/236908f4-ff1d-4bd9-8ff8-ffa770855e35" />
</CardGroup>


# Intermediate Config introduction

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Intermediate-Config-introduction/page

Practical NGINX guide covering hosting multiple sites, redirects, rewrites, upstream load balancing, reverse proxying, and caching for production.

Welcome back — I hope you had a good break.

In this lesson we explore several practical NGINX features you’ll use regularly in production. We won't cover every option, but we will focus on the most common and useful capabilities:

* Host multiple websites on a single server using `server_name`.
* Perform redirects with `return` (for simple canonicalization like HTTP → HTTPS).
* Rewrite URLs with `rewrite` using regular expressions and capture groups.
* Define `upstream` pools and apply load balancing (round-robin, weighted, least connections, IP hashing).
* Use NGINX as a reverse proxy to forward requests to backend services on other ports.
* Enable caching to improve performance and reduce backend load.

<Frame>
  <img alt="A slide titled &#x22;Objectives&#x22; with a teal gradient panel on the left. On the right are three numbered goals: hosting multiple sites on one web server, learning to redirect websites, and rewriting friendly URLs." />
</Frame>

## Quick overview

Below is a short table summarizing the topics and their typical use cases:

| Feature                        | Use case                                      | Example snippet                                                 |
| ------------------------------ | --------------------------------------------- | --------------------------------------------------------------- |
| Multiple sites (`server_name`) | Host several domains on one server            | See "Hosting multiple sites" section                            |
| Redirects (`return`)           | Simple 301/302 redirections, canonicalization | `return 301 https://$host$request_uri;`                         |
| Rewrites (`rewrite`)           | URL transformations using regex               | `rewrite ^/old/(.*)$ /new/$1 permanent;`                        |
| Upstream pools                 | Group backend servers for proxying            | `upstream backend { server 10.0.0.1:8080; }`                    |
| Load balancing                 | Distribute requests (round-robin, weighted)   | `upstream backend { server a weight=3; server b; }`             |
| Reverse proxy                  | Forward requests (preserve headers)           | `proxy_pass http://backend;`                                    |
| Caching                        | Cache backend responses for performance       | `proxy_cache_path /tmp/cache levels=1:2 keys_zone=mycache:10m;` |

## Hosting multiple sites on one server (server\_name)

NGINX matches requests to a particular server block by listening port and `server_name`. Use separate `server {}` blocks for each domain or subdomain.

Example: two sites on the same IP, one for `example.com` and one for `api.example.com`:

```nginx theme={null}
