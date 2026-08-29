# (returns the page HTML; output shortened for clarity)
<!doctype html>
<html>
  <head>...</head>
  <body>
    <h1>Welcome</h1>
    <p>Served by node01</p>
  </body>
</html>
```

Check service status examples:

```bash theme={null}
# On a web backend:
root@node01 ~ ➜  systemctl status apache2

# On the load balancer (to verify nginx presence or absence):
root@nginx ~ ➜  systemctl status nginx
# If nginx is not installed you will see: "Unit nginx.service could not be found."
```

## Restrict direct access to backends (UFW)

Best practice: only allow the load balancer to reach backend HTTP ports. First, discover the load balancer IP (example from `ip a` on `nginx`):

```bash theme={null}
root@nginx ~ ➜  ip a
...
    inet 192.230.202.10/24 brd 192.230.202.255 scope global eth0
...
```

On each backend (`node01`, `node02`) allow HTTP access only from the load balancer IP:

```bash theme={null}
# On node01 and node02:
root@node01 ~ ➜ ufw allow from 192.230.202.10 proto tcp to any port 80
# Example response:
# Rule added
```

Confirm UFW rules:

```bash theme={null}
root@node01 ~ ➜ ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       192.230.202.10
```

Useful references:

* UFW documentation: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)
* Nginx docs (load balancing): [https://nginx.org/en/docs/http/load\_balancing.html](https://nginx.org/en/docs/http/load_balancing.html)

## Configure Nginx as a reverse proxy with upstreams

On the load balancer, edit the Nginx site config (example: `/etc/nginx/sites-available/apache-app`). Confirm the file exists:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ ll
total 12
-rw-r--r-- 1 root root 443 Feb 10 20:53 apache-app
```

Start with an `upstream` block (the pool of backends) and a `server` block that proxies requests to it. Example default (round-robin) configuration:

```nginx theme={null}
# Upstream configuration
upstream apache_example {
    server 192.230.202.12:80;
    server 192.230.202.3:80;
}

# Default server configuration
server {
    listen 80;

    root /var/www/html;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    server_name apache.example.com;

    location / {
        proxy_pass http://apache_example;
    }
}
```

Notes:

* The example uses IP addresses for the backends (`192.230.202.12` for `node01` and `192.230.202.3` for `node02`). You may use DNS names instead.
* The `upstream` block above uses Nginx’s default round-robin algorithm.

Test configuration, enable the site and reload Nginx:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# Enable site (create symlink if needed)
root@nginx /etc/nginx/sites-available ➜ ln -s /etc/nginx/sites-available/apache-app /etc/nginx/sites-enabled/

# Reload nginx
root@nginx /etc/nginx/sites-available ➜ nginx -s reload
```

Test from the load balancer:

```bash theme={null}
root@nginx ~ ➜ curl http://localhost
# Returns the proxied HTML page. Refreshing the page shows alternating "Served by node01" / "Served by node02" indicating round-robin behavior.
```

## Load balancing methods — quick reference

|            Algorithm | Description                                            | When to use                                                                                       |
| -------------------: | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
|          round-robin | Default. Cycles requests evenly across servers.        | Simple, stateless backends with similar capacity.                                                 |
| weighted round-robin | Assign weights to servers (`weight=`) to bias traffic. | Backends have different capacity or you want preferential routing.                                |
|            `ip_hash` | Maps client IP to a backend (simple sticky sessions).  | Simple session persistence without a shared session store; not ideal when many clients share IPs. |

## Weighted round-robin

To bias traffic toward one backend, add `weight=` to the server entries in the `upstream` block:

```nginx theme={null}
upstream apache_example {
    server 192.230.202.12:80 weight=10;
    server 192.230.202.3:80  weight=1;
}

server {
    listen 80;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name apache.example.com;

    location / {
        proxy_pass http://apache_example;
    }
}
```

* With the above weights, roughly 10 requests will go to `node01` for every 1 request to `node02`.
* Reload Nginx after changes:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ nginx -s reload
```

Observe behavior in a browser or with repeated `curl` — the higher-weight backend should serve the majority of requests.

## ip\_hash (sticky sessions)

Enable basic session stickiness by adding `ip_hash` to the `upstream` block. This maps the client IP to a backend and keeps subsequent requests from that IP directed to the same server:

```nginx theme={null}
upstream apache_example {
    ip_hash;
    server 192.230.202.12:80;
    server 192.230.202.3:80;
}

server {
    listen 80;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name apache.example.com;

    location / {
        proxy_pass http://apache_example;
    }
}
```

* Reload Nginx:

```bash theme={null}
root@nginx /etc/nginx/sites-available ➜ nginx -s reload
```

* After enabling `ip_hash`, the same client IP should consistently be mapped to the same backend. Refreshing from the same client should repeatedly show the same backend serving the request.

> **lightbulb** ip\_hash provides simple sticky sessions by client IP. It is not suitable if clients are behind NAT/proxies that cause many clients to share an IP, and it does not account for backend health checks or capacity — consider more advanced session persistence strategies or a shared session store for production-grade stickiness.

## Quick reference — common files & commands

| Item                    | Purpose                             | Example                                                                 |
| ----------------------- | ----------------------------------- | ----------------------------------------------------------------------- |
| Nginx site file         | Configure upstreams and proxy rules | `/etc/nginx/sites-available/apache-app`                                 |
| Test config             | Syntax check before reload          | `nginx -t`                                                              |
| Enable site             | Activate site config                | `ln -s /etc/nginx/sites-available/apache-app /etc/nginx/sites-enabled/` |
| Reload Nginx            | Apply config changes                | `nginx -s reload`                                                       |
| Restrict backend access | Limit HTTP access to load balancer  | `ufw allow from 192.230.202.10 proto tcp to any port 80`                |

## Wrap-up

* Nginx upstreams default to round-robin load balancing.
* Use `weight=` to bias traffic (weighted round-robin).
* Use `ip_hash` to pin client IPs to backends for simple session persistence.
* Always validate changes with `nginx -t` and gracefully reload Nginx.
* Restrict backend access (for example with UFW) so only the load balancer can reach backend HTTP ports.

Further reading:

* Nginx load balancing docs: [https://nginx.org/en/docs/http/load\_balancing.html](https://nginx.org/en/docs/http/load_balancing.html)
* UFW documentation: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)
* Apache HTTP Server: [https://httpd.apache.org/](https://httpd.apache.org/)

That completes this demo.

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/a2b8d77e-6682-4fa2-bedf-a8dde19a29ef)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/da8e5437-fc04-466c-9446-8f856d5bb9ec)


# Demo Reverse Proxy

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Demo-Reverse-Proxy/page

Configuring Nginx as a reverse proxy to load balance and forward HTTP requests on port 80 to multiple Flask backends running on port 5000, with firewall and testing steps.

Welcome back. In this lesson you'll learn how to configure Nginx as a reverse proxy that forwards incoming HTTP requests (port 80) to two backend Flask applications listening on port 5000. This setup is useful when you want to expose a single public endpoint while running multiple backend apps, and you can host both Nginx and the Flask apps on the same machine to save resources.

> **lightbulb** A reverse proxy accepts client requests on port 80 (or 443) and forwards them to one or more backend servers (here, Flask apps on port 5000). A load balancer is conceptually similar, but the reverse proxy often runs on the same host as the entry Nginx instance.

<Frame>
  <img alt="A diagram showing a reverse proxy setup: users connect through a network cloud to an NGINX reverse proxy, which forwards requests to backend Flask web servers running on port 5000." />
</Frame>

Why this matters (quick summary)

* Centralized entry point for multiple backends.
* Ability to scale or take down individual backends without exposing internal hosts.
* Offload SSL, caching, or compression to Nginx while keeping app logic in Flask.

Quick reference: hosts and ports

| Host      | Role              | Service             | Port   |
| --------- | ----------------- | ------------------- | ------ |
| `node01`  | Backend Flask app | Flask app           | `5000` |
| `node02`  | Backend Flask app | Flask app           | `5000` |
| `nginx`   | Reverse proxy     | Nginx (public)      | `80`   |
| any admin | SSH access        | Open for management | `22`   |

Prerequisites and links

* Nginx installed on the reverse proxy host — see [Nginx documentation](https://nginx.org/en/docs/).
* Flask app running on each backend host — see [Flask quickstart](https://flask.palletsprojects.com/en/latest/quickstart/).
* UFW (or your host firewall) configured to restrict backend access — see [UFW documentation](https://help.ubuntu.com/community/UFW).

Step-by-step walkthrough

1. Inspect backend node (node01)

Verify there is no HTTP server on port 80, and that the Flask app is listening on port 5000.

Check port 80 on node01:

```bash theme={null}
root@node01 ~ ✦ ➜ curl localhost
curl: (7) Failed to connect to localhost port 80 after 0 ms: Connection refused
```

Check the Flask app on port 5000:

```bash theme={null}
root@node01 ~ ✦ ➜ curl localhost:5000
<h1>Hello, Human!</h1>[Not Authenticated]
```

2. Confirm node02

Confirm node02 returns the same Flask response on port 5000 (omitted here for brevity). Both backends should serve the same application content so Nginx can load-balance between them.

3. Firewall: allow only the Nginx server to reach backends on port 5000

Only the reverse proxy host should be able to reach the backend Flask apps on port 5000. Keep SSH (port 22) open for management but lock down access to port 5000 to the reverse proxy IP (example IP used below: `192.230.206.12`).

Check current UFW status:

```bash theme={null}
root@node01 ~ ✦ ➜ ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
```

Allow traffic from the reverse proxy IP to port 5000:

```bash theme={null}
root@node01 ~ ✦ ➜ ufw allow from 192.230.206.12 proto tcp to any port 5000
Rule added
```

Verify the new rule:

```bash theme={null}
root@node01 ~ ✦ ➜ ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
5000/tcp                   ALLOW       192.230.206.12
22/tcp (v6)                ALLOW       Anywhere (v6)
```

> **warning** When changing firewall rules, be careful not to lock yourself out. Confirm SSH access remains allowed before applying strict rules. Always test connectivity from the reverse proxy after adding rules.

4. On the Nginx reverse proxy host

Confirm Nginx is serving the default welcome page on port 80:

```bash theme={null}
root@nginx ~ ➜ curl localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</html>
```

Remove the default site and create a new site configuration. On the Nginx host, go to `/etc/nginx/sites-available/` and create a file named `helloworld`. Be consistent when creating the symlink in `/etc/nginx/sites-enabled/` later.

Create the Nginx site configuration `/etc/nginx/sites-available/helloworld`. This file defines an `upstream` pointing to the two backend Flask servers on port 5000 and proxies all requests to that upstream:

```nginx theme={null}
