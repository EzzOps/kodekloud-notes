# On node01 (backend)
sudo tail -f /var/log/apache2/access.log
```

Example (shortened) Apache output showing images and CSS being served:

```text theme={null}
192.231.221.4 - - [17/Feb/2025:01:20:34 +0000] "GET /images/pic04.jpg HTTP/1.1" 200 6499 "https://.../ " "Mozilla/5.0 ..."
192.231.221.4 - - [17/Feb/2025:01:20:34 +0000] "GET /assets/css/main.css HTTP/1.1" 200 8551 "https://.../" "Mozilla/5.0 ..."
```

Also watch NGINX access logs on the proxy to see requests arriving there:

```bash theme={null}
# On the NGINX node
sudo tail -f /var/log/nginx/access.log
```

Open Developer Tools → Network in your browser and verify there are no proxy/Cache-Control headers from NGINX yet. Note that browser caching (Cache-Control, Expires) is different from NGINX proxy caching.

<Callout icon="lightbulb">
  Browser caching (Cache-Control, Expires) is client-side. NGINX proxy caching sits between clients and the origin and lets many clients get responses without hitting the origin for each request.
</Callout>

## 2 — Make the demo results more visible

To make cache hits obvious, increase the size of a few static files on the backends so that repeating origin requests are large and easy to spot:

```bash theme={null}
cd /var/www/html/images
# Increase each jpg to ~20 MiB (demo only)
for file in *.jpg; do sudo fallocate -l 20M "$file"; done
ls -l
```

You should now see large file sizes (\~20,971,520 bytes). This exaggeration helps demonstrate the savings achieved when NGINX serves cached responses.

## 3 — Configure NGINX disk cache (global settings)

Add a global cache path and defaults in the main NGINX config (commonly `/etc/nginx/nginx.conf`) — this must be outside any `http`, `server`, or `location` blocks:

```nginx theme={null}
##
# Caching (global)
##

proxy_cache_path /var/lib/nginx/cache levels=1:2 keys_zone=app_cache:10m;
proxy_cache_key "$scheme$request_method$host$request_uri";
proxy_cache_valid 200 302 10m;
proxy_cache_valid 404 1m;
```

Key points:

* `levels=1:2` splits the cache into subdirectories for filesystem performance.
* `keys_zone=app_cache:10m` reserves memory to store cache keys (adjust as traffic grows).
* `proxy_cache_key` composes the cache lookup key — include scheme, method, host, and URI to avoid collisions.

Create and secure the cache directory and set ownership to the NGINX worker user (commonly `www-data`):

```bash theme={null}
sudo mkdir -p /var/lib/nginx/cache
sudo chown -R www-data:www-data /var/lib/nginx/cache
```

<Callout icon="warning">
  Monitor disk usage and cache size. A misconfigured cache or too large TTLs can quickly consume disk space. Plan eviction policies and sizing for production.
</Callout>

## 4 — Enable proxy cache in the site/server config

Edit your site config (for example `/etc/nginx/sites-available/example-https`) and enable `proxy_cache` for the proxied location(s). Optionally add `Cache-Control` to responses for browser caching.

Example server block (showing the relevant parts):

```nginx theme={null}
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.com.pem;
    ssl_certificate_key /etc/ssl/certs/example.com-key.pem;

    root /var/www/html;

    add_header Strict-Transport-Security "max-age=31560000; includeSubDomains; preload";
    add_header X-Frame-Options "SAMEORIGIN";
    add_header Content-Security-Policy "default-src 'self'";
    add_header Referrer-Policy origin;
    add_header Cache-Control "public, max-age=3600";

    index index.html index.htm index.nginx-debian.html;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Let the origin see how NGINX handled the request (useful for origin logs):
        proxy_set_header X-Proxy-Cache $upstream_cache_status;

        # Enable proxy cache for this location
        proxy_cache app_cache;

        # Forward to the upstream backend block named "example"
        proxy_pass https://example;
    }

    location /admin {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    }
}
```

Be sure an `upstream` block exists and matches your backends and ports:

```nginx theme={null}
upstream example {
    server node01:443;
    server node02:443;
}
```

If proxying to HTTPS backends, enable SNI so NGINX sends the correct server name to the upstream:

```nginx theme={null}
proxy_ssl_server_name on;
```

Also ensure NGINX trusts the backend certificate chain (or use IPs, or disable verification in non-production testing).

Use modern TLS settings for client \<-> proxy and proxy \<-> backend connections:

```nginx theme={null}
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
```

Test and reload NGINX after making changes:

```bash theme={null}
sudo nginx -t
sudo systemctl reload nginx
```

## 5 — Add a log field on Apache to show upstream cache status

To make verification straightforward, have Apache log the `X-Proxy-Cache` header sent by NGINX. Add or update a `LogFormat` in `/etc/apache2/apache2.conf` or in your vhost:

```apache theme={null}
LogFormat "%v:%p \"%{X-Forwarded-For}i\" \"%{X-Forwarded-Proto}i\" \"%{X-Proxy-Cache}i\" %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
```

Then test and restart Apache:

```bash theme={null}
sudo apachectl -t
sudo systemctl restart apache2
```

When NGINX forwards a request you will see `"MISS"` in the Apache logs for the first fetch; subsequent requests served from the cache will not reach Apache (they will not generate HIT entries in origin logs).

## 6 — Verify caching behavior

Follow these checks to confirm caching is working:

1. Confirm the cache directory is initially empty or minimal:

```bash theme={null}
ls -l /var/lib/nginx/cache
```

2. Trigger traffic (open the site or use curl). Initially NGINX will fetch items and create cache files. Example curl to show headers:

```bash theme={null}
curl -I -k https://example.com/images/pic01.jpg
# or use -H "Host: example.com" with direct proxy IPs
```

Look for `X-Proxy-Cache: MISS` on the first request when you included `proxy_set_header X-Proxy-Cache $upstream_cache_status;`.

3. Inspect the NGINX cache directory — it should contain subdirectories and cached object files:

```bash theme={null}
ls -l /var/lib/nginx/cache
# Example result will show directories like 1/ and 2/
```

4. Tail the NGINX access log to observe cached responses being served. Cached responses may show status `200` (full) or `206` (partial) depending on client ranged requests:

```bash theme={null}
sudo tail -f /var/log/nginx/access.log
```

Example NGINX access log entries showing cached responses:

```text theme={null}
192.231.221.4 - - [17/Feb/2025:01:38:22 +0000] "GET /images/pic12.jpg HTTP/1.1" 206 2097136 "-" "Cloud-CDN-Google (GFE/2.0)"
192.231.221.4 - - [17/Feb/2025:01:38:22 +0000] "GET /images/pic05.jpg HTTP/1.1" 206 2097136 "-" "Cloud-CDN-Google (GFE/2.0)"
```

5. Re-open the site or use a new browser session/Incognito. The Apache backend logs should show fewer repeated requests for large assets; NGINX will be serving them from cache. When Apache does see requests, the `X-Proxy-Cache` field will typically show `"MISS"` for the first fetch and not appear for subsequent HITs (because the origin is not contacted).

If you included `proxy_set_header X-Proxy-Cache $upstream_cache_status;` and Apache's `LogFormat` captures it (`%{X-Proxy-Cache}i`), you'll see whether requests were `MISS`, `HIT`, `EXPIRED`, or `REVALIDATED`.

## DevTools verification

Open Browser Developer Tools → Network and inspect response headers and sizes. You should see large resource sizes (we made them large for the demo), but after the cache warms, repeated loads should not cause new origin hits. NGINX will serve cached responses, reducing backend load.

<Frame>
  <img alt="A browser screenshot showing the &#x22;This is Phantom&#x22; HTML5 UP template with three colored feature tiles near the top. The developer tools Network panel is open at the bottom, listing many GET requests and showing headers for a selected image." />
</Frame>

## Quick reference: cache settings

| Setting                          | Purpose                                          | Example                                                                     |
| -------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------- |
| `proxy_cache_path`               | Defines cache storage path, levels, and key zone | `proxy_cache_path /var/lib/nginx/cache levels=1:2 keys_zone=app_cache:10m;` |
| `proxy_cache_key`                | Key used to identify cacheable responses         | `proxy_cache_key "$scheme$request_method$host$request_uri";`                |
| `proxy_cache_valid`              | TTLs for responses by status code                | `proxy_cache_valid 200 302 10m; proxy_cache_valid 404 1m;`                  |
| `proxy_cache` (in location)      | Enables cache for a proxied location             | `proxy_cache app_cache;`                                                    |
| `proxy_set_header X-Proxy-Cache` | Send cache status to origin for logging          | `proxy_set_header X-Proxy-Cache $upstream_cache_status;`                    |

## Summary & next steps

* Without proxy caching, each client request hits Apache and the origin bears the full response cost.
* We configured a disk cache with `proxy_cache_path`, set a cache key, and declared TTLs with `proxy_cache_valid`.
* We enabled `proxy_cache` in the proxied location and forwarded `$upstream_cache_status` to the origin for visibility.
* After the cache warms (first requests = MISS), subsequent requests are served by NGINX (HIT) and origins are spared repeated heavy responses.

Because the demo used inflated image sizes to make results obvious, a recommended next step is to enable on-the-fly compression (gzip/brotli) and set appropriate cache-control headers for production workloads.

## Links and references

* NGINX proxy\_cache documentation: [https://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html#proxy\_cache](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)
* NGINX caching guide: [https://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
* Apache logging docs: [https://httpd.apache.org/docs/current/logs.html](https://httpd.apache.org/docs/current/logs.html)
* Browser DevTools Network panel: [https://developer.chrome.com/docs/devtools/network/](https://developer.chrome.com/docs/devtools/network/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/42757c8a-6e6c-48c7-b89e-a4ada8791ad9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/1559660d-8686-4508-8474-33f2e7fbfdd4" />
</CardGroup>


# Demo Compression

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Performance/Demo-Compression/page

Demonstrating enabling and verifying gzip compression in Nginx, measuring performance improvements, configuring gzip directives, and validating compressed responses in browser and server logs

In this lesson you'll learn how to enable and verify HTTP compression (gzip) in Nginx. We'll first measure performance without compression, then enable `gzip` in the Nginx configuration and confirm responses are compressed and transferred much faster. Note that compressing already-compressed image formats (JPEG, PNG, GIF) usually yields little to no benefit — this demo intentionally inflates JPEG sizes so the difference is easy to observe in browser developer tools.

We begin by testing the site with no compression and hitting backend Apache servers. Most text-based assets (HTML, CSS, JS) are already efficient, but artificially large `image/jpeg` files will exhibit long transfer times when not compressed.

<Frame>
  <img alt="A simple network diagram showing a browser requesting a CSS resource through an NGINX reverse proxy labeled &#x22;No Compression&#x22; to backend Apache web servers. Arrows indicate NGINX forwards the request to two Apache web servers." />
</Frame>

To highlight the effect, we inflate JPEG sizes on the Apache servers, observe the slow transfers in the browser, then enable gzip in Nginx and confirm dramatic improvements.

<Frame>
  <img alt="A simple architecture diagram showing a browser requesting assets (CSS, JS, HTML, JPG, XML) routed through an NGINX reverse proxy with compression. The proxy forwards the requests to multiple Apache web servers." />
</Frame>

## Preparing the environment

* Confirm your Nginx reverse proxy forwards requests to Apache upstreams. Example `upstream` and HTTP-to-HTTPS redirect:

```nginx theme={null}
