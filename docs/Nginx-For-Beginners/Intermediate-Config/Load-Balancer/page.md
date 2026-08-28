# site 1
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;
}

# site 2 (API)
server {
    listen 80;
    server_name api.example.com;
    root /var/www/api.example.com/html;
    index index.html;
}
```

Notes:

* The order of `server_name` matching: exact names, longest wildcard starting with `*`, longest wildcard ending with `*`, then regex.
* Use `listen 443 ssl;` and certificate directives in the HTTPS server block.

<Callout icon="lightbulb">
  When you add a new domain, create a dedicated `server` block and test the config using `nginx -t` before reloading with `systemctl reload nginx` (or `nginx -s reload`).
</Callout>

## Redirects using `return`

For straightforward redirects (for example redirecting all HTTP traffic to HTTPS or canonicalizing `www`), prefer `return` because it’s simpler and faster than `rewrite`.

HTTP → HTTPS redirect example:

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}
```

Redirect `www` to non-`www`:

```nginx theme={null}
server {
    listen 80;
    server_name www.example.com;
    return 301 $scheme://example.com$request_uri;
}
```

Use `301` for permanent redirects and `302` for temporary ones.

<Callout icon="warning">
  Avoid using `rewrite` when a simple `return` covers your use case—`return` is easier to read and slightly more efficient.
</Callout>

## Rewriting URLs with `rewrite` and regex

`rewrite` allows transforming requested URIs using PCRE regular expressions and capture groups. Use it when you need complex mapping (e.g., legacy URL structures -> friendly URLs).

Example: redirect old article paths to a new structure:

```nginx theme={null}
location /old/ {
    rewrite ^/old/([0-9]{4})/([0-9]{2})/(.*)$ /articles/$1/$2/$3 permanent;
}
```

Explanation:

* `^/old/([0-9]{4})/([0-9]{2})/(.*)$` captures year, month, and slug.
* `$1`, `$2`, `$3` reference the captured groups.
* `permanent` issues a 301 redirect.

Tips:

* Test your regex with tools like regex101 to avoid accidental matches.
* Order matters: exact `location` blocks are evaluated before regex `location` blocks. Place regex `location` blocks carefully.

## Upstream pools and load balancing

Use `upstream` blocks to define backend server groups. Reference the group from `proxy_pass` or other proxy directives.

Basic upstream with round-robin (default):

```nginx theme={null}
upstream backend {
    server 10.0.0.10:8080;
    server 10.0.0.11:8080;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Weighted servers:

```nginx theme={null}
upstream backend {
    server 10.0.0.10:8080 weight=3;
    server 10.0.0.11:8080 weight=1;
}
```

Common load balancing methods:

| Algorithm             | Use case                                                                      |
| --------------------- | ----------------------------------------------------------------------------- |
| Round-robin (default) | Simple equal distribution across backends                                     |
| `weight`              | Give more traffic to stronger servers                                         |
| `least_conn`          | Prefer servers with fewer active connections (better for long-lived requests) |
| `ip_hash`             | Sticky sessions by client IP (useful when you don’t have a session store)     |

## Reverse proxy essentials

When proxying, ensure headers and client IPs are passed correctly. The typical minimal proxy configuration includes:

```nginx theme={null}
location / {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
}
```

Notes:

* `proxy_http_version 1.1` and clearing `Connection` header help with keepalive behavior to upstreams.
* If your backend runs on a different port, include it in the upstream server definition (e.g., `server 127.0.0.1:3000;`).

## Caching responses with `proxy_cache`

Caching reduces backend load and improves response times. A simple caching setup:

```nginx theme={null}
# define cache storage
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=mycache:10m max_size=1g inactive=60m use_temp_path=off;

# server block
server {
    listen 80;
    server_name cache.example.com;

    location / {
        proxy_pass http://backend;
        proxy_cache mycache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        add_header X-Proxy-Cache $upstream_cache_status;
    }
}
```

Key points:

* `keys_zone` reserves memory for cache keys (e.g., `10m`).
* `proxy_cache_valid` sets caching durations by status code.
* `X-Proxy-Cache` header helps verify whether a response was served from cache (`HIT`) or passed to the backend (`MISS`).

<Callout icon="lightbulb">
  Design cache keys carefully (including query strings or authentication headers when needed) and have a strategy for cache invalidation. For advanced cache purging, consider modules like `ngx_cache_purge` or manage via short TTLs and revalidation.
</Callout>

## Final notes and best practices

* Always test configuration changes with `nginx -t` and monitor error logs at `/var/log/nginx/error.log`.
* Keep redirect and rewrite rules simple and clearly documented to avoid surprise behavior.
* Use health checks and proper monitoring for upstream backends to detect failures quickly.
* Use HTTPS and HSTS in production; consider automating certificate management with Let’s Encrypt (Certbot) or similar tools.

## Links and references

* [NGINX Documentation — Module ngx\_http\_core\_module](https://nginx.org/en/docs/http/ngx_http_core_module.html)
* [NGINX Docs — Reverse Proxy](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
* [NGINX Guide — Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)

This lesson prepares you to host multiple sites, redirect and rewrite URLs, load-balance proxied backends, and cache responses effectively using NGINX.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/4ab9e29b-b87b-47ca-b1dc-0a13b41351ed" />
</CardGroup>


# Load Balancer

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Load-Balancer/page

Explains NGINX load balancing concepts, supported algorithms, health checks, configuration examples, and testing methods to improve performance and fault tolerance.

A load balancer is software that distributes incoming network traffic across multiple backend servers to improve performance, availability, and fault tolerance. Without a load balancer, a website relies on a single server, which can quickly become a bottleneck for CPU, memory, disk, or network I/O as traffic grows. More importantly, a single server creates a single point of failure.

One key advantage of a load balancer is avoiding requests being forwarded to unhealthy backends. NGINX Open Source uses passive health checks by default: when a backend repeatedly fails to respond or returns errors, NGINX marks it unavailable and stops sending it new requests. Active health checks — where the load balancer proactively probes backends — are provided by NGINX Plus.

<Callout icon="lightbulb">
  NGINX Open Source performs passive health checks by default (it detects failures from error responses/timeouts). Active health checks that periodically probe backends are available in NGINX Plus.
</Callout>

<Frame>
  <img alt="A diagram titled &#x22;Load Balancing With Nginx&#x22; showing clients connecting through a network cloud to an NGINX load balancer that distributes traffic to multiple web servers. Health checks are illustrated, with one server marked as unhealthy." />
</Frame>

You can tune timeouts and failure-handling options in NGINX, but the default passive behavior ensures that unhealthy servers stop receiving traffic. If one or more web servers go down, the site remains available while you repair or replace the affected nodes.

## Load-balancing algorithms supported by NGINX

NGINX supports several algorithms. Choosing the right one depends on your application workload, server capacity, and session state requirements.

* Round Robin (default)
* Weighted Round Robin
* IP hash (sticky sessions)
* Least connections (`least_conn`)
* Least time (`least_time`, available in NGINX Plus)

### Round Robin

Round Robin distributes requests in a circular fashion: request 1 → server A, request 2 → server B, request 3 → server C, then back to A. It is the default algorithm and works well when backend servers have similar capacity and identical content.

<Frame>
  <img alt="A diagram titled &#x22;Algorithms: Round Robin&#x22; showing an NGINX load balancer using a round-robin icon to distribute requests to three web servers labeled 1, 2, and 3." />
</Frame>

Define a pool of backend servers in an `upstream` block (typically inside `http { ... }` or an included file) and reference that name with `proxy_pass` to forward requests:

```nginx theme={null}
upstream backend {
    server 10.10.0.101:80;
    server 10.10.0.102:80;
    server 10.10.0.103:80;
}

server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://backend/;
    }
}
```

The `backend` name is arbitrary — it is only a handle for the pool. An `upstream` can include many servers, but 3–10 servers is often more maintainable.

### Weighted Round Robin

Weighted Round Robin allows assigning a `weight` to each server to control the relative share of requests. If server A has `weight=4`, B `weight=2`, and C `weight=1`, A receives four times as many requests as C.

<Frame>
  <img alt="A diagram titled &#x22;Algorithms: Weighted Round Robin&#x22; showing an NGINX load balancer using a weighted round-robin algorithm to distribute traffic to three web servers. The servers are labeled with weights 4, 2, and 1 to indicate relative traffic share." />
</Frame>

Use weights when backends have different hardware capacity or when some servers handle more load:

```nginx theme={null}
upstream backend {
    server 10.10.0.101:80 weight=4;
    server 10.10.0.102:80 weight=2;
    server 10.10.0.103:80 weight=1;
}

server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://backend/;
    }
}
```

### Sticky sessions (`ip_hash`)

Some apps store session state locally (for example, shopping carts). To ensure a client is routed to the same backend across requests, enable `ip_hash`, which hashes the client IP to select a backend and provides sticky sessions.

<Frame>
  <img alt="Diagram titled &#x22;Algorithms: IP Hash&#x22; showing an NGINX load balancer using an IP-hash algorithm to route incoming requests to one of three web servers." />
</Frame>

```nginx theme={null}
upstream backend {
    ip_hash;
    server 10.10.0.101:80;
    server 10.10.0.102:80;
    server 10.10.0.103:80;
}

server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://backend/;
    }
}
```

Note: `ip_hash` ties clients to backends by IP, which may be problematic behind NATs or shared proxies. For more flexible session affinity, consider application-level session stores (Redis, database) or cookies.

### Least connections

The `least_conn` algorithm sends a new request to the backend with the fewest active connections. It's effective when request durations vary, because it avoids overloading servers currently handling long-running connections.

<Frame>
  <img alt="A diagram showing the &#x22;Least Connection&#x22; load-balancing algorithm: an NGINX load balancer directs traffic to the web server with the fewest active connections (servers shown with counts 2, 5, and 4)." />
</Frame>

```nginx theme={null}
upstream backend {
    least_conn;
    server 10.10.0.101:80;
    server 10.10.0.102:80;
    server 10.10.0.103:80;
}

server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://backend/;
    }
}
```

### Least time (NGINX Plus)

The `least_time` algorithm selects the backend with the lowest recent response time. Options like `last_byte` or `header` control whether NGINX measures time until the last response byte or until the first byte, respectively. This method is available in NGINX Plus.

<Callout icon="warning">
  The `least_time` balancing method (and active health checks) are available in NGINX Plus — the commercial edition.
</Callout>

```nginx theme={null}
upstream backend {
    least_time last_byte;
    server 10.10.0.101:80;
    server 10.10.0.102:80;
    server 10.10.0.103:80;
}

server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://backend/;
    }
}
```

## Quick comparison: which algorithm to choose

| Algorithm                       | Best for                                       | NGINX Edition |
| ------------------------------- | ---------------------------------------------- | ------------- |
| `round_robin`                   | Default; similar servers and identical content | Open Source   |
| `weight` (weighted round robin) | Mixed-capacity servers                         | Open Source   |
| `ip_hash`                       | Session affinity based on client IP            | Open Source   |
| `least_conn`                    | Requests with variable durations               | Open Source   |
| `least_time`                    | Minimize latency by response time (advanced)   | NGINX Plus    |

## Testing and next steps

To validate any load-balancing configuration, run controlled load tests and monitor backend metrics (CPU, memory, connection counts, response times). Popular tools:

* `ab` (ApacheBench) — simple HTTP load testing
* `wrk` — multi-threaded HTTP benchmarking for higher concurrency
* `siege`, `hey` — other lightweight tools

Example `wrk` command to generate load:

```bash theme={null}
wrk -t4 -c100 -d30s http://example.com/
```

References:

* NGINX documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* NGINX Plus features: [https://www.nginx.com/products/nginx/](https://www.nginx.com/products/nginx/)
* `wrk` — [https://github.com/wg/wrk](https://github.com/wg/wrk)

Now we'll implement a few of these algorithms in practice to see how they behave under load.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/4356e2fa-9121-4fb3-9d11-8b96f964df6c" />
</CardGroup>
