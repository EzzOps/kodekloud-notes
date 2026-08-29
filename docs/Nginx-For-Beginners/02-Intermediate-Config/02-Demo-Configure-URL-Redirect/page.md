# remove the default symlink (or file) from sites-enabled and reload
root@ubuntu-host:/etc/nginx/sites-enabled# rm default
root@ubuntu-host:/etc/nginx/sites-enabled# nginx -s reload
root@ubuntu-host:/etc/nginx/sites-enabled# curl localhost
curl: (7) Failed to connect to localhost port 80: Connection refused
```

Explanation: after removing the default server block that listened on port 80, Nginx no longer has a listener for that address/port. Connections to `localhost:80` are refused until you enable a site that listens on port 80.

<Callout icon="warning">
  Removing the default site will stop responses on port 80 until at least one valid site is enabled. Ensure you add and enable your site configurations before relying on the server in production.
</Callout>

## Create site configurations

1. Copy the default configuration to use as a template for `example1`, then edit it:

```bash theme={null}
root@ubuntu-host:/etc/nginx/sites-available# cp default example1
root@ubuntu-host:/etc/nginx/sites-available# vim example1
```

A minimal, cleaned `server` block for `example1`:

```nginx theme={null}
server {
    listen 80;
    root /var/www/example1;
    index index.html index.htm;
    server_name www.example1.com;

    location / {
        # try_files will check each option in order and return 404 if none match
        try_files $uri $uri/ =404;
    }
}
```

Notes:

* `try_files` attempts to serve a file or directory; if nothing matches, it returns a 404.
* Use a dedicated `root` directory per site to avoid accidentally serving `/var/www/html` content.

2. Create `example2` by copying `example1` and updating `root` and `server_name`:

```bash theme={null}
root@ubuntu-host:/etc/nginx/sites-available# cp example1 example2
# Edit example2 and change:
# root /var/www/example2;
# server_name www.example2.com;
```

## Prepare site content

Create site directories and simple `index.html` pages:

```bash theme={null}
root@ubuntu-host:~# mkdir -p /var/www/example1 /var/www/example2

root@ubuntu-host:~# cat > /var/www/example1/index.html <<'HTML'
<h1>Example 1!!!</h1>
HTML

root@ubuntu-host:~# cat > /var/www/example2/index.html <<'HTML'
<h1>Example 2!!!</h1>
HTML
```

## Enable the sites, validate, and reload

Create symlinks in `sites-enabled`, validate the configuration, and reload Nginx:

```bash theme={null}
root@ubuntu-host:/etc/nginx/sites-available# ln -s /etc/nginx/sites-available/example1 /etc/nginx/sites-enabled/example1
root@ubuntu-host:/etc/nginx/sites-available# ln -s /etc/nginx/sites-available/example2 /etc/nginx/sites-enabled/example2

# Validate and reload
root@ubuntu-host:/etc/nginx/sites-available# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

root@ubuntu-host:/etc/nginx/sites-available# nginx -s reload
```

## Test using curl with a Host header

Simulate requests for different domains by setting the `Host` header with `curl`:

```bash theme={null}
root@ubuntu-host:/etc/nginx/sites-available# curl --header "Host: www.example1.com" localhost
<h1>Example 1!!!</h1>

root@ubuntu-host:/etc/nginx/sites-available# curl --header "Host: www.example2.com" localhost
<h1>Example 2!!!</h1>

# If the Host header doesn't match any server_name, Nginx serves the first matching server block
root@ubuntu-host:/etc/nginx/sites-available# curl --header "Host: anything.com" localhost
<h1>Example 1!!!</h1>
```

Quick mapping reference:

| Request Host header | Served content                                        |
| ------------------- | ----------------------------------------------------- |
| `www.example1.com`  | `Example 1` page                                      |
| `www.example2.com`  | `Example 2` page                                      |
| any other host      | First enabled server block (`example1` in this setup) |

Behavior detail:

* When no `server_name` matches the `Host` header, Nginx falls back to the default server for that address/port. With multiple enabled files, the fallback is typically the first server block encountered (often determined by alphabetical order of files in `/etc/nginx/sites-enabled`).

## Alternative: multiple server blocks in one file

You can place multiple `server { ... }` blocks in a single configuration file. Example:

```nginx theme={null}
server {
    listen 80;
    root /var/www/example1;
    index index.html index.htm;
    server_name www.example1.com;
    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    root /var/www/example2;
    index index.html index.htm;
    server_name www.example2.com;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

Operational considerations:

* If both sites are in the same file and that file is deleted or misconfigured, both sites will be affected.
* Best practice: keep one site per file in `/etc/nginx/sites-available` and enable sites with symlinks in `/etc/nginx/sites-enabled` to limit the blast radius and simplify rollbacks.

## Final reminders

* Always run `nginx -t` after editing configuration files to validate syntax.
* After a successful test, reload Nginx with `nginx -s reload` to apply changes.
* Creating/editing files under `/etc/nginx/sites-available` alone does not activate a site — remember to create corresponding symlinks in `/etc/nginx/sites-enabled`.

<Callout icon="lightbulb">
  Keep each site's configuration separate (one file per site) and use symlinks in `/etc/nginx/sites-enabled` for better isolation and safer rollbacks.
</Callout>

That's it for this lesson.

## Links and references

* [Nginx documentation — Server names](https://nginx.org/en/docs/http/server_names.html)
* [Nginx documentation — try\_files directive](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/db98f13e-91c5-43d1-9400-fd40daf84b42" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/c74f891f-6063-47cc-8144-ada26fef3e78" />
</CardGroup>


# Demo Configure URL Redirect

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Demo-Configure-URL-Redirect/page

Guide to configure NGINX to redirect HTTP traffic to HTTPS, enable TLS and firewall rules, enable site, reload NGINX, and verify redirects.

In this lesson you'll configure NGINX to redirect all plain HTTP traffic to HTTPS using the `return` directive. This forces clients connecting on port 80 to be redirected to port 443 so all requests are encrypted.

We have a simple "Diner" app served from port 80 on the host. The steps covered here:

* Check firewall rules.
* Allow inbound HTTPS (port 443).
* Create a single NGINX config containing two server blocks:
  * one to redirect HTTP → HTTPS (301),
  * one to serve the site over HTTPS with TLS certificates.
* Enable the site, validate and reload NGINX.
* Verify the redirect using curl and a browser.

<Frame>
  <img alt="An illustration of a desktop computer and a web page with a padlock icon between them and the caption &#x22;It's the secure version of HTTP.&#x22; It represents an encrypted HTTPS connection protecting data between a browser and a website." />
</Frame>

## 1. Confirm current firewall status

Check which ports are allowed so you can open port 443 before enabling HTTPS:

```bash theme={null}
root@ubuntu-host:~# ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
```

Port 443 is not listed, so HTTPS requests will fail until it is allowed.

Enable HTTPS (TCP 443):

```bash theme={null}
root@ubuntu-host:~# ufw allow 443/tcp
Rule added
Rule added (v6)
```

## 2. Understand what happens if port 443 is open but NGINX isn't serving HTTPS

If port 443 is allowed but NGINX has no TLS server block for the site, the browser may show a connection error or an upstream proxy might return a 502 Bad Gateway. Example browser output:

<Frame>
  <img alt="A browser window showing a &#x22;502 Bad Gateway&#x22; error page. The page is mostly blank and displays &#x22;nginx/1.27.2&#x22; under the error message." />
</Frame>

## 3. Create the combined NGINX configuration

We keep the configuration DRY by putting two server blocks in the same file:

* A lightweight port 80 server block that issues a permanent `301` redirect to the same host and URI on `https://`.
* A port 443 server block that enables TLS and serves the app files.

Create or edit `/etc/nginx/sites-available/diner-https` with the following:

```nginx theme={null}
#
server {
    listen 80;

    server_name diner.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;

    server_name diner.com;

    ssl_certificate /etc/ssl/certs/diner.com.pem;
    ssl_certificate_key /etc/ssl/certs/diner.com-key.pem;

    root /var/www/diner;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }
}
```

Notes about this configuration:

* The `return 301 https://$host$request_uri;` preserves the hostname, path and query string so `http://diner.com/some/path?x=1` becomes `https://diner.com/some/path?x=1`.
* The second server block enables `ssl`, and points to the certificate and key files used for TLS.
* The example certificate/key paths are present for this exercise. In production obtain valid certificates (for example via Let's Encrypt) and reference them here.

<Callout icon="lightbulb">
  Using a `301 Moved Permanently` response will cause clients and search engines to cache the redirect. Use `302 Found` during testing if you expect to change behavior later, then switch to `301` once everything is final.
</Callout>

## 4. Enable the site and reload NGINX

Create the symlink in `sites-enabled`:

```bash theme={null}
root@ubuntu-host:~# ln -s /etc/nginx/sites-available/diner-https /etc/nginx/sites-enabled/diner-https
```

Validate the NGINX configuration and reload:

```bash theme={null}
root@ubuntu-host:~# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

root@ubuntu-host:~# nginx -s reload
