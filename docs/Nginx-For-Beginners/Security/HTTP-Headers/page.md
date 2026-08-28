# on the NGINX host
sudo ufw allow 443/tcp
sudo ufw status
```

Example status output:

```shell theme={null}
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)
```

Create an NGINX site configuration that redirects HTTP to HTTPS and serves TLS on port 443. Save this file as `/etc/nginx/sites-available/example-https`:

```nginx theme={null}
# /etc/nginx/sites-available/example-https
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.com.pem;
    ssl_certificate_key /etc/ssl/certs/example.com-key.pem;

    root /var/www/html;
    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }
}
```

Enable the site and test the NGINX configuration:

```shell theme={null}
sudo ln -s /etc/nginx/sites-available/example-https /etc/nginx/sites-enabled/example-https
sudo nginx -t
```

At this point `nginx -t` will fail if the certificate files referenced above do not exist. For testing you can generate a cert and key with mkcert.

Generate test certificates using mkcert:

```shell theme={null}
# generate cert and key in the current directory
mkcert example.com

# move them into /etc/ssl/certs and set permissions
sudo mkdir -p /etc/ssl/certs
sudo mv example.com.pem /etc/ssl/certs/example.com.pem
sudo mv example.com-key.pem /etc/ssl/certs/example.com-key.pem
sudo chmod 644 /etc/ssl/certs/example.com.pem
sudo chmod 600 /etc/ssl/certs/example.com-key.pem
```

Note: `mkcert` creates `example.com.pem` (certificate) and `example.com-key.pem` (private key) by default in the current directory. `mkcert` also supports `-cert-file` and `-key-file` flags to write directly to target locations.

After placing the certificate and key, test and reload NGINX:

```shell theme={null}
sudo nginx -t
sudo nginx -s reload
```

Verify the site responds over HTTPS:

```shell theme={null}
curl -I https://example.com --insecure
```

Use `--insecure` only for local testing where the mkcert CA may not be trusted by the client. Do not use `--insecure` in production.

2. Reverse proxy: NGINX front-end (HTTPS) → Apache backends (HTTPS)

Assume you have two Apache backends already configured to serve HTTPS on port 443. Configure NGINX so it proxy\_passes requests to those backends using HTTPS, keeping the connection encrypted end-to-end.

Create an upstream block listing backend IPs (port 443) and configure the server block to proxy to that upstream. Example combined configuration at `/etc/nginx/sites-available/example-https`:

```nginx theme={null}
# Upstream configuration (backends terminate TLS on 443)
upstream example {
    server 192.230.210.3:443;
    server 192.230.210.6:443;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.com.pem;
    ssl_certificate_key /etc/ssl/certs/example.com-key.pem;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    location / {
        proxy_pass https://example;

        # Forward typical headers to the backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Allow proxying to HTTPS backends using SNI
        proxy_ssl_server_name on;
        proxy_ssl_name $host;
    }
}
```

Key details and options

* Because the upstream servers are HTTPS endpoints, NGINX will initiate TLS when contacting them. `proxy_ssl_server_name on;` ensures the Server Name Indication (SNI) extension is sent so backends can present the correct certificate.
* In production you should enable upstream certificate validation. Depending on your environment you may need to provide a CA bundle or configure `proxy_ssl_trusted_certificate` and `proxy_ssl_verify` options (see NGINX docs).
* For internal environments using self-signed certificates you can disable verification during testing, but this is a security risk in production.

<Callout icon="warning">
  Do NOT disable TLS verification (`proxy_ssl_verify off`) in production. If using self-signed certs for internal services, add the CA to the NGINX host trust store instead of skipping verification.
</Callout>

Apache backend example

Each Apache backend should redirect HTTP to HTTPS and serve the site on port 443 with the certificate and key. Example Apache virtual host (save as `/etc/apache2/sites-available/example.conf`):

```apache theme={null}
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName example.com

    # Redirect all HTTP requests to HTTPS, preserving host and URI
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</VirtualHost>

<VirtualHost *:443>
    SSLEngine on
    ServerName example.com
    DocumentRoot /var/www/html

    SSLCertificateFile /etc/ssl/certs/example.com.pem
    SSLCertificateKeyFile /etc/ssl/certs/example.com-key.pem

    CustomLog ${APACHE_LOG_DIR}/access.log combined
    ErrorLog ${APACHE_LOG_DIR}/error.log
</VirtualHost>
```

Firewall and testing

* Make sure each backend allows incoming `443/tcp`:

```shell theme={null}
# on each backend
sudo ufw allow 443/tcp
sudo ufw status
```

* Place the corresponding certificates on each backend (they can use the same certificate if the domain and CA match).
* Restart/reload services after configuration changes:

```shell theme={null}
# On the NGINX host
sudo nginx -t
sudo nginx -s reload

# On each Apache backend
sudo systemctl reload apache2
```

Quick functional test

* To validate load balancing and which backend handled a request, add a unique identifier to each backend's `index.html` (for example "NODE01" on `192.230.210.3` and "NODE02" on `192.230.210.6`) and issue multiple requests. Responses should alternate according to upstream load balancing.

Example snippet to add to `/var/www/html/index.html` on a backend:

```html theme={null}
<!-- add somewhere in the page -->
<p>Served from NODE01</p>
```

Wrap-up and best practices

* We configured NGINX to redirect HTTP → HTTPS and serve TLS using locally generated certs for testing.
* We extended NGINX to act as an HTTPS reverse proxy, forwarding requests to HTTPS backends with SNI support.
* For production use:
  * Obtain certificates from a trusted CA (e.g., Let's Encrypt).
  * Ensure proper certificate verification between proxy and backends (add CA bundles or enable `proxy_ssl_verify`).
  * Avoid disabling TLS verification on the proxy.
  * Consider monitoring, access and error logging, and automated certificate renewal.

Links and references

* mkcert — [https://mkcert.dev](https://mkcert.dev)
* Let's Encrypt — [https://letsencrypt.org](https://letsencrypt.org)
* NGINX proxying to HTTPS backends — [https://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
* Apache mod\_ssl / VirtualHost examples — [https://httpd.apache.org/docs/2.4/ssl/ssl\_howto.html](https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html)
* UFW (Uncomplicated Firewall) — [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/af1b832f-e266-40ac-b2f3-86945bc5805b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/64f0226a-545c-4456-b704-e4ee931b410f" />
</CardGroup>


# HTTP Headers

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/HTTP-Headers/page

Guide explaining HTTP headers, categories, examples, security, caching, CORS, proxy usage, and NGINX configuration to set and forward headers

HTTP headers are the metadata "envelope" that travels with every request and response on the web. They are simple key-value pairs (format: `Key: value`) that tell clients, servers, and intermediaries how to handle the payload and connection. Think of headers like the address, postage, and delivery instructions on a physical envelope — they don't contain the letter (body) but they tell everyone how to process it.

This guide explains the most common HTTP header categories, shows realistic examples, and demonstrates how to configure headers in NGINX. It maintains the original examples while improving readability and structure for quick reference.

<Frame>
  <img alt="A presentation slide titled &#x22;Types of HTTP Headers&#x22; showing two categories: a &#x22;General Headers&#x22; box and a &#x22;Request/Response Headers&#x22; box. The request/response box lists header types such as Security, Authentication, Caching, CORS, Proxy, and Custom Headers." />
</Frame>

## Quick overview: header categories

| Category               | Purpose                                                           | Examples                                                      |
| ---------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------- |
| General headers        | Metadata used in both requests and responses                      | `Date`, `Connection`                                          |
| Request headers        | Sent by the client to describe the request or client capabilities | `Accept`, `User-Agent`, `Cookie`, `Accept-Language`           |
| Response headers       | Sent by the server to describe the response                       | `Content-Type`, `Cache-Control`, `Set-Cookie`                 |
| Security headers       | Help mitigate XSS, clickjacking, MIME sniffing, etc.              | `Content-Security-Policy`, `X-Frame-Options`                  |
| Authentication headers | Carry credentials or tokens                                       | `Authorization: Basic ...`, `Authorization: Bearer ...`       |
| Caching headers        | Control caching behavior across browsers and CDNs                 | `Cache-Control`, `Etag`, `Expires`, `Vary`                    |
| CORS headers           | Control cross-origin resource access for browsers                 | `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods` |
| Proxy headers          | Preserve original client info when traffic flows through proxies  | `X-Forwarded-For`, `X-Forwarded-Proto`                        |
| Custom headers         | Application-specific metadata                                     | `X-Custom-Build`, `X-Feature-Flag`                            |

## Request example (HTTP/1.1)

A typical browser request contains many request headers that describe the client, acceptable media types, language, caching preferences, and more.

```http theme={null}
GET / HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/103.0
Accept: text/html
Accept-Language: en-US
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
```

Key points:

* `Host` identifies the target host (required for virtual hosting).
* `User-Agent` identifies the client software and platform.
* `Accept` and `Accept-Language` guide content negotiation.

### HTTP/2 pseudo-headers + modern request example

Some transports (HTTP/2) include pseudo-headers (beginning with `:`) together with standard headers:

```http theme={null}
:authority: kodekloud.com
:method: GET
:path: /
:scheme: https
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Cache-Control: max-age=0
Cookie: session=abc123; preferences=lang=en
Referer: https://www.google.com/
Sec-CH-UA: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
Sec-CH-UA-Mobile: ?0
Sec-CH-UA-Platform: "macOS"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
```

* `Sec-CH-*` headers are part of Client Hints for improved server-side decisions.
* `Cookie` transmits session or user state to the server.

## Response example (common response headers)

Servers include response headers that describe the payload, caching, compression, and server metadata:

```http theme={null}
Age: 387887
Cf-Cache-Status: DYNAMIC
Content-Encoding: br
Content-Security-Policy: frame-ancestors 'self' https://*.webflow.com http://*.webflow.com
Content-Type: text/html; charset=utf-8
Date: Fri, 17 Jan 2025 18:44:46 GMT
Server: cloudflare
Vary: Accept-Encoding
X-Cache: HIT
X-Cache-Hits: 57
X-Served-By: cache-yyz4562-YYZ
```

Notable headers:

* `Content-Type` — MIME type and charset.
* `Content-Encoding` — compression used (gzip, br).
* `Vary` — instructs caches that different request headers produce different responses.

## Security headers — purpose and examples

Security headers defend against common web threats such as XSS, clickjacking, and protocol downgrade. Example of a secure application's headers (trimmed for clarity):

```http theme={null}
cache-control: no-cache, no-store, max-age=0, must-revalidate
content-encoding: gzip
content-security-policy: script-src 'nonce-6tC1Rsh6ZnR2cX-hVemx5A' 'strict-dynamic' https: http: 'unsafe-inline'; object-src 'none'; base-uri 'self'
content-type: text/html; charset=utf-8
cross-origin-resource-policy: same-site
date: Sat, 18 Jan 2025 17:03:06 GMT
expires: Mon, 01 Jan 1990 00:00:00 GMT
permissions-policy: geolocation=(), microphone=()
pragma: no-cache
server: ESF
strict-transport-security: max-age=10886400; includeSubDomains
vary: Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-xss-protection: 0
```

Important security headers:

* `Content-Security-Policy` (CSP) — restricts sources for scripts, styles, frames, etc., and can use nonces or hashes for fine-grained control.
* `X-Content-Type-Options: nosniff` — prevents MIME sniffing, forcing the browser to obey `Content-Type`.
* `X-Frame-Options: SAMEORIGIN` — blocks framing by other origins (mitigates clickjacking).
* `Strict-Transport-Security` (HSTS) — enforces HTTPS for future requests.

<Callout icon="lightbulb">
  Security headers like `Cache-Control`, `Pragma`, and `Expires` are often combined with CSP and HSTS to prevent sensitive pages from being cached and to harden the application against client-side attacks.
</Callout>

## Authentication headers

Authentication credentials are commonly passed in headers. Examples:

```http theme={null}
Authorization: Basic YWRtaW46c2VjcmV0
```

* `Authorization: Basic <base64>` — legacy Basic Auth, where the base64 decodes to `username:password`. Only use over TLS and avoid in modern systems.
* `Authorization: Bearer <token>` — common for token-based authentication (OAuth2, JWT). Always protect tokens and avoid logging them.

<Callout icon="warning">
  Do not log full `Authorization` header values or other sensitive headers (tokens, passwords) in production logs. Mask or truncate these fields to prevent leakage.
</Callout>

## Caching headers and how caching works

Caching headers tell browsers and intermediaries how long to store responses and when to revalidate.

Key caching headers:

* `Cache-Control` — modern and flexible; supports `max-age`, `no-cache`, `no-store`, `must-revalidate`.
* `Expires` — older, date-based expiry.
* `Etag` — entity tag for versioning; used with `If-None-Match` to validate resources.
* `Vary` — lists request headers that affect the cache (e.g., `Accept-Encoding`).

Example response with cache-related fields:

```http theme={null}
Accept-Ranges: bytes
Cache-Control: max-age=0, must-revalidate
Content-Encoding: gzip
Content-Length: 44549
Content-Type: text/html; charset=UTF-8
Date: Sat, 18 Jan 2025 18:31:33 GMT
Etag: W/"[AWS_SECRET_ACCESS_KEY]"
Set-Cookie: edition-view=espn-en-us; Path=/; Expires=Sat, 25 Jan 2025 18:31:33 GMT
Vary: Accept-Encoding
Via: 1.1 varnish (Varnish/6.0), 1.1 cloudfront
X-Cache: Miss from cloudfront
```

* `Etag` enables conditional GETs: client sends `If-None-Match` and server may return `304 Not Modified`.
* CDNs and reverse proxies (Varnish, CloudFront) often add `X-Cache` or `Via` headers for debugging cache behavior.

When deploying behind a proxy/CDN, configure caching at the edge to reduce origin traffic and improve latency.

## CORS (Cross-Origin Resource Sharing)

CORS is a browser security feature that restricts cross-origin HTTP requests. Servers explicitly allow cross-origin access using CORS response headers.

<Frame>
  <img alt="An infographic titled &#x22;CORS Header&#x22; showing a web browser, a globe/network and servers connected by dashed arrows labeled &#x22;Retrieves data&#x22; and &#x22;Includes CORS headers.&#x22; It notes that CORS controls resource requests from different domains and restricts external website access to protect data." />
</Frame>

Example of an OPTIONS preflight response:

```http theme={null}
HTTP/1.1 204 No Content
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Origin: https://petexchangehk-frontend.vercel.app
Connection: keep-alive
Content-Length: 0
Date: Mon, 19 Sep 2022 13:23:51 GMT
Server: Cowboy
Vary: Origin, Access-Control-Request-Headers
```

Key CORS headers:

* `Access-Control-Allow-Origin` — allowed origin(s) or `*`.
* `Access-Control-Allow-Methods` — allowed HTTP methods for the cross-origin request.
* `Access-Control-Allow-Headers` — allowed request headers the client may send.
* `Access-Control-Allow-Credentials` — whether cookies/credentials are allowed.

CORS must be coordinated between client and server domains; incorrect CORS settings can break legitimate cross-domain interactions or, conversely, open up security exposure.

## Proxy headers

When requests traverse proxies or load balancers, they commonly add headers to preserve original client information. Handle these carefully and only trust them from known, internal proxies.

Common proxy headers:

* `X-Forwarded-For` — original client IP and proxy chain.
* `X-Forwarded-Host` — original `Host` header.
* `X-Forwarded-Proto` — original scheme (`http` or `https`).
* `X-Forwarded-Server` — proxy hostname.
* `X-Real-IP` — client IP (used when a single proxy exists).

Example (environment-style display):

```text theme={null}
HOST                   'web:8001'
UPGRADE_INSECURE_REQUESTS '1'
USER_AGENT             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
X_FORWARDED_FOR        '192.168.122.4'
X_FORWARDED_HOST       'web.domain.com'
X_FORWARDED_PROTO      'https'
X_FORWARDED_SERVER     '172.19.0.5'
```

Best practices:

* Only trust these headers when they are set by your own proxies/load balancers.
* Use strict access controls and validation to avoid spoofed client IPs.

## Custom headers

You can define custom headers for application-specific metadata. Historically, they used an `X-` prefix but modern practice prefers descriptive, namespaced headers without the `X-` prefix.

Example:

```http theme={null}
GET /api HTTP/1.1
Host: example.com
User-Agent: curl/8.1.2
Accept: */*
X-Custom-Header1: Value1
```

Use cases: feature toggles, build/version identifiers, routing hints. Never put sensitive data in custom headers unless it is encrypted and protected.

## NGINX built-in variables (common ones)

NGINX exposes many dynamic variables that you can use in configuration files. These are prefixed with `$`.

| Variable              | Description                                            | Example value              |
| --------------------- | ------------------------------------------------------ | -------------------------- |
| `$remote_addr`        | Client IP address                                      | `174.0.252.84`             |
| `$remote_port`        | Client source port                                     | `52344`                    |
| `$server_addr`        | IP of the server handling the request                  | `10.0.0.5`                 |
| `$request`            | Full request line                                      | `GET /index.html HTTP/1.1` |
| `$uri`                | Current URI without arguments                          | `/index.html`              |
| `$request_uri`        | Full request URI including query string                | `/index.html?user=Anthony` |
| `$request_method`     | HTTP method                                            | `GET`                      |
| `$args`               | Query string                                           | `id=1234&name=example`     |
| `$http_<header_name>` | Any HTTP header (lowercase, dashes become underscores) | `$http_user_agent`         |
| `$http_referer`       | Referer header                                         | `https://google.com`       |
| `$status`             | Response status code                                   | `200`                      |
| `$upstream_addr`      | Upstream server that handled the request               | `10.0.0.10:8080`           |
| `$scheme`             | Protocol scheme                                        | `http` or `https`          |
| `$host`               | Original `Host` header                                 | `www.kodekloud.com`        |
| `$ssl_protocol`       | TLS protocol used                                      | `TLSv1.3`                  |
| `$ssl_cipher`         | TLS cipher suite                                       | `TLS_AES_256_GCM_SHA384`   |
| `$http_cookie`        | Cookie header                                          | `session=abc123`           |

To construct a full URL in NGINX:

```nginx theme={null}
$scheme://$host$request_uri
```

This results in `https://www.example.com/path?query`.

## Example NGINX configuration: set response headers + forward request headers

This concise NGINX example demonstrates how to add security and cache headers to responses and how to forward original request details to an upstream backend.

```nginx theme={null}
server {
    listen 443 ssl;
    server_name example.com;

    location / {
        # Response headers sent back to the client
        add_header X-Content-Type-Options "nosniff" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
        add_header Cache-Control "public, max-age=86400" always;

        # Proxy to upstream backend and pass original request info
        proxy_pass http://backend_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Notes:

* `add_header` sets headers on NGINX responses. Use `always` to ensure headers are added even on error responses.
* `proxy_set_header` controls headers sent to upstream servers — useful for preserving client IP, host, and scheme.

## Summary

* HTTP headers are essential metadata used by clients, servers, and intermediaries to coordinate content negotiation, caching, authentication, security, and routing.
* Security and CORS headers are critical for protecting web applications; misconfiguration can lead to vulnerabilities or broken integrations.
* When using proxies and CDNs, pay attention to proxy headers and cache-related headers.
* In NGINX, use `add_header` to set response headers and `proxy_set_header` to preserve client/request info for upstreams.

## Links and references

* [MDN Web Docs — HTTP headers](https://developer.mozilla.org/en-US/docs/Glossary/HTTP_header)
* [RFC 7231 — HTTP/1.1 Semantics and Content](https://datatracker.ietf.org/doc/html/rfc7231)
* [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
* [NGINX Documentation — Variables](https://nginx.org/en/docs/varindex.html)
* [MDN — CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

In follow-up lessons you can inspect headers with browser devtools, curl (`curl -I` / `curl -v`), or network proxies, and practice configuring NGINX to add, modify, and strip headers for different environments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/889d65af-d23e-4813-98fb-afae795ba3e9" />
</CardGroup>
