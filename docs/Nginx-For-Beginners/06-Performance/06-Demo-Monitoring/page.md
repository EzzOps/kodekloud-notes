# Upstream configuration
upstream example {
    server node01:443;
    server node02:443;
}

# Default HTTP -> HTTPS redirect
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

* Example HTTPS server block on the reverse proxy (shortened for clarity):

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

    index index.html index.htm index.nginx-debian.html;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass https://example;
        proxy_ssl_server_name on;
    }

    location /admin {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    }
}
```

> **lightbulb** Best practice: configure `proxy_set_header` lines so your backend sees the original Host and client IPs, and include `proxy_ssl_server_name on;` when proxying to HTTPS backends.

## Inflating images for the demo

On the Apache webserver(s) we intentionally inflate the JPEG files to simulate very large images. Run these commands in the images directory:

```bash theme={null}
cd /var/www/html/images
ll
for file in *.jpg; do fallocate -l 20M "$file"; done
```

Example listing prior to inflation:

```text theme={null}
total 136
drwxr-xr-x 2 root root 4096 Feb 17 20:31 ./
drwxr-xr-x 5 root root 4096 Feb 17 20:31 ../
-rw-r--r-- 1 root root 1259 Feb 17 20:31 logo.svg
-rw-r--r-- 1 root root 6311 Feb 17 20:31 pic01.jpg
...
-rw-r--r-- 1 root root 17129 Feb 17 20:31 pic13.jpg
...
```

After `fallocate -l 20M`, each `.jpg` reports a much larger size. This produces invalid image contents in many cases — acceptable here because we only demonstrate transfer size and compression behavior, not image fidelity.

> **warning** Using `fallocate` as shown will change file contents and can corrupt images. Do this only in test/demo environments where file integrity doesn't matter.

## Monitoring access logs

Tail the Apache access log while exercising the site so you can observe incoming GET requests and response sizes:

```bash theme={null}
tail -f /var/log/apache2/access.log
```

Example access log entry:

```text theme={null}
example.com:443 127.0.0.1 - - [17/Feb/2025:20:32:46 +0000] "GET / HTTP/1.1" 200 11242 "-" "curl/7.81.0"
```

## Testing in the browser (no compression)

* Open an Incognito/private window, open Developer Tools → Network tab, and load the site.
* Without compression you'll see large transferred sizes for the inflated JPEGs and long transfer times (multiple seconds per file).

Example response headers for an uncompressed image (notice `Content-Length` \~ 20 MB and no `Content-Encoding`):

```text theme={null}
Response Headers
Content-Length: 20971520
Content-Type: image/jpeg
Date: Mon, 17 Feb 2025 20:56:45 GMT
Etag: "1400000-62e5cbe7aae75"
Last-Modified: Mon, 17 Feb 2025 20:55:27 GMT
...
```

<Frame>
  <img alt="A browser screenshot showing a webpage header that reads &#x22;This is Phantom, a free, fully responsive site.&#x22; The developer tools Network panel is open below, listing many GET requests, file names, types and transfer sizes." />
</Frame>

Firefox displays both the resource size and the transferred bytes. When uncompressed, they match and transfer times are long for each large image.

## Enabling gzip in Nginx

Edit the main Nginx configuration (typically `/etc/nginx/nginx.conf`) and add gzip settings inside the `http` block. The key directives to enable and control gzip:

* `gzip on;` — enables gzip compression.
* `gzip_vary on;` — adds `Vary: Accept-Encoding` to responses (important for caches).
* `gzip_proxied any;` — allow compression when requests come via a proxy.
* `gzip_comp_level 6;` — compression level (1–9).
* `gzip_http_version 1.1;` — ensures proper handling for HTTP/1.1 clients.
* `gzip_types` — list of MIME types to compress (text-based types are priority).

Here is a concise gzip snippet to include under the `http` block:

```nginx theme={null}
##
# Gzip Settings
##

gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_buffers 16 8k;
gzip_http_version 1.1;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/jpeg image/jpg font/otf font/eot font/ttf font/woff;
```

### What these gzip directives do

| Directive                | Purpose                                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| `gzip on;`               | Enable gzip compression globally in the `http` context.                                             |
| `gzip_vary on;`          | Adds `Vary: Accept-Encoding` header so caches treat compressed/uncompressed responses separately.   |
| `gzip_proxied any;`      | Enables compression for responses served through proxies (useful for reverse-proxy setups).         |
| `gzip_comp_level 6;`     | Balances compression ratio and CPU cost (range: `1`–`9`).                                           |
| `gzip_buffers 16 8k;`    | Controls memory buffers for compression output.                                                     |
| `gzip_http_version 1.1;` | Ensures gzip is used only for HTTP/1.1+ clients where appropriate.                                  |
| `gzip_types ...`         | MIME types to compress; include text, JSON, JS, CSS, XML. Note: most images are already compressed. |

Notes:

* Keep `gzip_types` focused on compressible, text-based content (HTML/CSS/JS/JSON/XML).
* Adding `image/jpeg` to `gzip_types` generally has little benefit because JPEGs are already compressed; in this demo we included it to illustrate the effect on inflated files.

## Validate and reload Nginx

Always test the config before restarting:

```bash theme={null}
nginx -t
sudo systemctl restart nginx
```

If `nginx -t` reports errors, fix them before reloading.

## Verifying compression in the browser

Reload the page in an incognito/private window and watch the Network tab. Compressed responses will include `Content-Encoding: gzip` and `Vary: Accept-Encoding` headers. The browser shows a smaller "Transferred" size than the resource "Size" when compression is applied.

Example compressed response headers:

```text theme={null}
Response Headers
Content-Encoding: gzip
Content-Type: image/jpeg
Date: Mon, 17 Feb 2025 21:03:05 GMT
Etag: W/"1400000-62e5cbe7acdb5"
Last-Modified: Mon, 17 Feb 2025 20:55:27 GMT
Vary: Accept-Encoding
```

You will also see compressed JavaScript/CSS responses with smaller transferred sizes:

```text theme={null}
GET /assets/js/skel.min.js
Status 200
Transferred 3.76 kB (9.09 kB size)
Response Headers:
content-encoding: gzip
content-type: text/javascript
```

<Frame>
  <img alt="A browser window showing the &#x22;Phantom&#x22; website template with a large headline and placeholder text. The browser's developer tools (Network tab) are open at the bottom, listing many GET requests and resource details." />
</Frame>

## Consolidated configuration examples

Below is a compact snapshot of common server-wide settings you can place in `nginx.conf` or your site-specific configuration. Adjust values for your environment.

```nginx theme={null}
events {
    worker_connections 768;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip settings (as shown earlier)
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/javascript text_xml application/xml application/xml+rss text/javascript image/jpeg image/jpg font/otf font/eot font/ttf font/woff;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=1000r/m;
    limit_req_status 429;

    # Proxy cache
    proxy_cache_path /var/lib/nginx/cache levels=1:2 keys_zone=app_cache:10m;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

And a compact server block recap with headers and proxy settings:

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

    index index.html index.htm index.nginx-debian.html;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass https://example;
    }

    location /admin {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    }
}
```

## HTTP headers reference

For comprehensive information about HTTP headers and their semantics, see:

* [MDN Web Docs — HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
* [NGINX gzip module documentation](https://nginx.org/en/docs/http/ngx_http_gzip_module.html)

<Frame>
  <img alt="A screenshot of the MDN Web Docs page titled &#x22;HTTP headers,&#x22; showing explanatory text and section links about different types of HTTP headers. The page layout includes a left navigation column, main article content in the center, and a right-hand table of contents." />
</Frame>

## Conclusion

* Enabling `gzip` in Nginx with a sensible `gzip_types` list and `gzip_vary on;` dramatically improves transfer times for compressible content (HTML, CSS, JavaScript, JSON, XML).
* Most modern image formats (JPEG, PNG, WEBP) are already compressed; gains from gzipping them are usually minimal. This demo inflated JPEGs to make the compression effect visible.
* Always validate configuration changes with `nginx -t` before reloading, and verify behavior using multiple clients (Chrome, Firefox, `curl`) and your browser developer tools.

Additional resources:

* NGINX gzip module: [https://nginx.org/en/docs/http/ngx\_http\_gzip\_module.html](https://nginx.org/en/docs/http/ngx_http_gzip_module.html)
* MDN — HTTP headers: [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/ab86ef5a-e11e-439b-9dbe-6aa962facf7b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/a5e800f9-add5-4f9d-9970-e3d9dfed2b9e)


# Demo Monitoring

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Performance/Demo-Monitoring/page

Guide to installing the Datadog Agent on Ubuntu EC2 and enabling NGINX stub status integration to collect system and NGINX metrics, view dashboards and create alerts

In this lesson you'll install the Datadog Agent on an Ubuntu EC2 instance and enable Datadog's NGINX integration so the agent can collect system metrics (CPU, memory, disk I/O, network) and NGINX `stub_status` metrics (active connections, requests, reading/writing/waiting). You will need a Datadog account and an API key to follow along.

> **lightbulb** Sign up for a [Datadog trial account](https://www.datadoghq.com/) if you don't have one. During onboarding, copy the one-line agent install command and your API key — you'll use them on your EC2 host.

## Prerequisites

* Ubuntu/Debian EC2 instance with sudo access.
* NGINX installed and running on the instance.
* Datadog account and API key.
* Basic familiarity with editing NGINX configuration files and reloading the service.

## 1. Install the Datadog Agent

From the Datadog web UI choose the correct OS (Ubuntu/Debian) and copy the one-line install command. Replace `<YOUR_API_KEY>` with your Datadog API key and set `DD_SITE` to the appropriate Datadog site (for example, `datadoghq.eu` for the EU region). Example command:

```bash theme={null}
DD_API_KEY="<YOUR_API_KEY>" DD_SITE="datadoghq.eu" bash -c "$(curl -L https://install.datadoghq.com/scripts/install_script_agent7.sh)"
```

Run that command on your EC2 instance. The installer will:

* Add the Datadog apt repository and import signing keys.
* Install the `datadog-agent` package.
* Start the Datadog Agent service.

Example excerpt from a successful install:

```bash theme={null}
gpg: key E6266D4AC0962C7D: "Datadog, Inc. APT key (2023-04-20) (APT key) <package+aptkey@datadoghq.com>" not changed
Get:2 https://apt.datadoghq.com stable Release [26.0 kB]
Get:5 https://apt.datadoghq.com stable/7 amd64 Packages [92.1 kB]
Fetched 252 MB in 3s (95.5 MB/s)
Selecting previously unselected package datadog-agent.
Preparing to unpack .../datadog-agent_1%3a7.62.3-1_amd64.deb ...
Unpacking datadog-agent (1:7.62.3-1) ...
Setting up datadog-agent (1:7.62.3-1) ...
datadog-agent start/running, process 1234
```

The install can take a few minutes. After completion, Datadog will begin reporting the host to the Datadog web app. Visit Datadog → Dashboards → Hosts to see your host and system metrics.

<Frame>
  <img alt="A Datadog dashboard screenshot titled &#x22;System - Disk I/O&#x22; displaying multiple time-series charts (I/O wait, disk latency, disk read/write rates, read/write requests, and disk CPU utilization) with small spikes around 12:15. The Datadog left sidebar and top navigation bar are also visible." />
</Frame>

You should begin to see system metrics (CPU, memory, disk I/O, network, etc.) appear in Datadog.

<Frame>
  <img alt="A screenshot of a Datadog monitoring dashboard showing system metrics panels (system load, CPU usage, I/O wait, system memory, and network traffic) with small line graphs. The left side has a navigation sidebar and the top bar contains time-range controls and action buttons like Share and Clone." />
</Frame>

## 2. Enable the NGINX integration (stub\_status)

Datadog needs a locally reachable NGINX `stub_status` endpoint to collect NGINX metrics. The safest approach is to expose this endpoint only to `localhost`, so the agent (running on the same host) can scrape it while external access remains blocked.

Go to Datadog → Integrations → Integrations and search for "NGINX". Datadog may autodetect NGINX on your host.

<Frame>
  <img alt="A screenshot of the Datadog Integrations page showing autodetected integrations (Nginx and SSH) at the top and a grid of available integration tiles (e.g., .NET, 1Password, Active Directory, Ably) below. The Datadog sidebar navigation and search/filter bar are also visible." />
</Frame>

Follow these steps to enable and configure the integration:

1. Verify your NGINX has the `stub_status` module:

```bash theme={null}
nginx -V 2>&1 | grep -o http_stub_status_module || true
```

If the output includes `http_stub_status_module`, the module is present.

2. Configure NGINX to expose `stub_status` on `localhost`. A common pattern is to listen on `127.0.0.1:81` and restrict access to the loopback interface. Add a server block (for example in `/etc/nginx/sites-available/example-https` or another site file):

```nginx theme={null}
server {
    listen 127.0.0.1:81;
    server_name localhost;

    access_log off;
    allow 127.0.0.1;
    deny all;

    location /nginx_status {
        # Open source NGINX stub status
        stub_status;

        # For older open source NGINX (<1.7.5) the syntax may be:
        # stub_status on;

        # NGINX Plus users may use:
        # status;

        # ensure version info is available
        server_tokens on;
    }
}
```

This configuration:

* Listens on `127.0.0.1:81` so only the local host can connect.
* Turns off access logging for the endpoint to prevent log growth from frequent scraping.
* Allows only `127.0.0.1` and denies all other addresses.

3. Test and reload NGINX:

```bash theme={null}
sudo nginx -t
sudo nginx -s reload
```

4. Verify the endpoint from the host itself (run on the server):

```bash theme={null}
curl http://127.0.0.1:81/nginx_status
```

Example expected output:

```text theme={null}
Active connections: 1
server accepts handled requests
9 9 13
Reading: 0 Writing: 1 Waiting: 0
```

Notes:

* If you fetch the endpoint from a remote machine you should either receive a `403 Forbidden` (if bound to 0.0.0.0 but access denied) or a connection error like `connection refused` (if bound to loopback only). Both outcomes are normal depending on your binding configuration.
* In Datadog’s NGINX integration settings, use `localhost` and the port you configured (for example, `81`) if it requests a host/port.

If you prefer to place the `stub_status` location inside an existing HTTPS server block, ensure you include `allow 127.0.0.1; deny all;` and `access_log off;` inside that `location /nginx_status` so only the local agent can access it:

```nginx theme={null}
location /nginx_status {
    stub_status;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

After reloading NGINX, Datadog's agent should be able to scrape the `stub_status` endpoint and start reporting NGINX metrics.

## 3. Datadog dashboards and host view

Once the integration is configured and the agent collects `stub_status`, Datadog will populate or create NGINX dashboards. Navigate to Dashboards → All Dashboards to find NGINX-related dashboards.

<Frame>
  <img alt="A screenshot of the Datadog web app displaying an &#x22;All Dashboards&#x22; list with various dashboard names and a purple banner that reads &#x22;Organize Dashboards with Lists.&#x22; The left sidebar shows navigation items like Dashboards, Monitors, and Integrations." />
</Frame>

Open the "NGINX - Overview" dashboard (it may take a few minutes for metrics to appear). Adjust the time range (for example, last 15 minutes) to see recent activity.

<Frame>
  <img alt="A screenshot of the Datadog web app showing an &#x22;NGINX - Overview&#x22; dashboard. It displays a large green NGINX banner, activity summary panels on the right, and sections for alerts and anomaly detection below." />
</Frame>

If you still see “no data”, verify the agent and integration settings. You can view the specific host under Datadog’s Hosts or via the Integrations host list to check system metrics and the host map.

<Frame>
  <img alt="A screenshot of the Datadog web UI showing a Host Map for a single &#x22;nginx&#x22; host, displayed as a green hexagon. The host details list components like &#x22;agent&#x22; and &#x22;ntp&#x22; and show system/metrics panels on the page." />
</Frame>

From the host and dashboard views you can:

* Bookmark dashboards you use often.
* Create monitors/alerts for CPU, memory, disk I/O, or NGINX-specific metrics (active connections, request rates).
* Run load tests (for example `ab`, `wrk`) to generate traffic and observe behavior.

## Quick reference — useful commands & checks

| Task                                  | Command / Action                        |                                    |   |        |
| ------------------------------------- | --------------------------------------- | ---------------------------------- | - | ------ |
| Check Datadog Agent status            | `sudo systemctl status datadog-agent`   |                                    |   |        |
| Test NGINX config                     | `sudo nginx -t`                         |                                    |   |        |
| Reload NGINX                          | `sudo nginx -s reload`                  |                                    |   |        |
| Verify `stub_status` locally          | `curl http://127.0.0.1:81/nginx_status` |                                    |   |        |
| Confirm NGINX has stub\_status module | \`nginx -V 2>&1                         | grep -o http\_stub\_status\_module |   | true\` |

## Troubleshooting checklist

* Ensure the Datadog Agent is running: `sudo systemctl status datadog-agent`.
* Confirm the `nginx_status` endpoint is reachable from the host: `curl http://127.0.0.1:81/nginx_status`.
* If Datadog reports no NGINX metrics:
  * Verify the NGINX integration is enabled in Datadog and the host/port configured in the integration matches your setup (e.g., `localhost:81`).
  * Check the agent logs for errors: `sudo journalctl -u datadog-agent -f` (or review `/var/log/datadog/`).
* Keep the `stub_status` endpoint bound to `localhost` or explicitly deny external access to avoid exposing internal server state.

That completes the Datadog Agent install and NGINX integration setup. In future lessons we'll cover advanced performance troubleshooting for NGINX and configuring Datadog monitors/alerts.

## Links and references

* [Datadog Agent installation documentation](https://docs.datadoghq.com/agent/)
* [Datadog NGINX integration docs](https://docs.datadoghq.com/integrations/nginx/)
* [NGINX stub\_status module documentation](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/c2a5f613-208c-4bab-b4b7-201c76dc566a)
