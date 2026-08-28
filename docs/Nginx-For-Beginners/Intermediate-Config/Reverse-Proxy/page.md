# Reverse Proxy

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Reverse-Proxy/page

Overview of NGINX reverse proxy functionality including TLS termination, load distribution, caching, header manipulation, and configuration examples for proxying backend application servers.

Welcome back.

In this lesson we take a closer look at reverse proxies: what they are, common use cases, and how NGINX implements reverse-proxying, TLS termination, load distribution, and caching.

## What is a reverse proxy?

A reverse proxy is a network component that sits between clients (browsers, API consumers, mobile apps) and one or more backend application servers. It accepts client requests, forwards them to one or more servers in an upstream pool, and returns the backend responses to the clients. A reverse proxy hides backend topology, centralizes cross-cutting concerns (TLS, caching, headers), and can improve security and performance.

<Frame>
  <img alt="A diagram titled &#x22;Reverse Proxy vs Load Balancer&#x22; showing clients sending requests to a Load Balancer, which then distributes traffic across multiple backend servers labeled Server 1–4." />
</Frame>

Although reverse proxies and load balancers can look and act similarly, their primary intents differ:

| Role          | Primary purpose                                                                                            | Typical features                                                               |
| ------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Reverse proxy | Act as an intermediary between clients and backend applications; hide backend details and centralize logic | TLS termination, header manipulation, request routing, caching, authentication |
| Load balancer | Distribute incoming traffic across multiple backend servers for availability and scale                     | Round-robin, least-connections, session affinity, health checks                |

NGINX can serve either role (or both) using the same configuration building blocks — for example, `upstream` blocks and `proxy_pass` — but configuration details and intent (session affinity, health checks, caching) determine whether you are acting primarily as a reverse proxy or a load balancer.

## Typical backend application frameworks

Applications running behind a reverse proxy are usually built with frameworks that bind to local ports and are not directly exposed to the public internet. Examples include:

<Frame>
  <img alt="A presentation slide titled &#x22;Frameworks&#x22; with the definition &#x22;A software framework is a reusable set of code and tools for application development.&#x22; It also shows logos for React, Flask, Ruby on Rails, and Laravel." />
</Frame>

Common frameworks and typical development/demo ports:

| Framework                    | Typical bind port / runtime |
| ---------------------------- | --------------------------- |
| React (dev server)           | `3000`                      |
| Flask (development)          | `5000`                      |
| Ruby on Rails (puma/webrick) | `3000` (or configured port) |
| Laravel (php artisan serve)  | `8000`                      |

Think of frameworks as foundations that provide common functionality so you don't have to build everything from scratch. When deployed, these applications often bind to `localhost` or a private interface and are reachable only via the host and port they listen on. Placing a reverse proxy in front of them exposes a single public endpoint while keeping application processes private.

<Frame>
  <img alt="A slide titled &#x22;Localhost&#x22; showing two browser windows: the left displays the React default page with the React logo and &#x22;Edit src/App.js...&#x22; (localhost:3000), and the right shows a &#x22;Welcome to Flask&#x22; webpage (localhost:5000)." />
</Frame>

## TLS / SSL termination and end-to-end encryption

A common role for a reverse proxy is TLS termination: the reverse proxy accepts HTTPS connections from clients, decrypts the traffic, and forwards requests to backends over HTTP. Offloading TLS to the proxy simplifies certificate management, centralizes TLS configuration, and reduces CPU work on application servers.

If you need full end-to-end encryption, you can terminate TLS at the proxy and still connect to backends via HTTPS (or you can terminate at the proxy only for public endpoints and use a secure internal network). The important configuration changes are to use `443` on the upstream servers and `proxy_pass https://...` when forwarding.

<Callout icon="warning">
  If you terminate TLS at the proxy, ensure you manage certificates securely and verify backend trust if internal encryption is required for compliance. You can also configure the proxy to validate backend certificates when using `proxy_ssl_verify` and related directives.
</Callout>

### Example: basic upstream and HTTP proxying

This minimal NGINX configuration defines an `upstream` group and forwards requests to it over HTTP:

```nginx theme={null}
http {
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
}
```

From this example you can't tell whether the intent is reverse-proxying or load balancing — the roles overlap and are determined by additional settings (session affinity, health checks, caching, etc.).

### Example: terminating TLS at the proxy (with optional HTTPS to backends)

If you terminate TLS at NGINX, you configure the server block with `listen 443 ssl` and certificate paths. Optionally, proxy to backends over HTTPS for end-to-end encryption:

```nginx theme={null}
http {
    upstream backend {
        server 10.10.0.101:443;
        server 10.10.0.102:443;
        server 10.10.0.103:443;
    }

    server {
        listen 443 ssl;
        server_name example.com www.example.com;

        ssl_certificate      /etc/nginx/ssl/server.crt;
        ssl_certificate_key  /etc/nginx/ssl/server.key;
        ssl_protocols        TLSv1.2 TLSv1.3;

        location / {
            # Proxy to backends using HTTPS for end-to-end encryption
            proxy_pass https://backend/;
        }
    }
}
```

If you require full end-to-end TLS, ensure the `upstream` ports are `443` and use `proxy_pass https://backend/;` so connections from proxy to backend are encrypted.

## Caching at the proxy

Caching is a powerful reverse-proxy capability. Without caching, the proxy forwards every request to the backend — including static assets and repeated content — increasing backend load and latency. NGINX can cache backend responses and serve repeated requests directly from the proxy cache.

A basic caching configuration:

```nginx theme={null}
http {
    proxy_cache_path /var/lib/nginx/cache levels=1:2 zone=app_cache:8m;
    proxy_cache_key "$scheme$request_method$host$request_uri$is_args$args";
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;

    server {
        listen 80;
        server_name example.com www.example.com;

        location / {
            proxy_cache app_cache;
            proxy_cache_bypass $http_cache_control;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://backend/;
        }
    }
}
```

We will cover caching strategies, cache-control semantics, and performance tuning in more detail later in the course.

## Quick reference: features you can centralize with an NGINX reverse proxy

* TLS termination and certificate management
* Load distribution and session affinity
* Health checks and failover logic
* Response caching for static and semi-static content
* Header manipulation (X-Forwarded-For, Host, custom headers)
* Authentication / authorization gating
* Rate limiting and basic WAF rules

<Callout icon="lightbulb">
  Using an NGINX reverse proxy centralizes TLS, caching, header manipulation, and load distribution — simplifying backend deployments while improving performance, observability, and security.
</Callout>

## Links and further reading

* NGINX official docs: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* NGINX reverse proxy guide: [https://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
* TLS best practices (Mozilla): [https://ssl-config.mozilla.org/](https://ssl-config.mozilla.org/)
* Let's Encrypt (free certificates): [https://letsencrypt.org/](https://letsencrypt.org/)

That brings us to the end of this lesson. Next, we'll move to a demo where you can see these reverse-proxy features implemented hands-on.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/beb4a7aa-77e5-4e9b-9d41-4a3f7029a73a" />
</CardGroup>
