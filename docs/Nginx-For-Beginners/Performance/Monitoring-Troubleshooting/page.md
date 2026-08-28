# make a typo (missing semicolon) and save
root@nginx:~# nginx -t
nginx: [emerg] directive "deny" is not terminated by ";" in /etc/nginx/sites-enabled/example-https:9
nginx: configuration file /etc/nginx/nginx.conf test failed
```

Common causes of `nginx -t` failures:

* Syntax errors (missing `;` or mismatched braces).
* Directives placed in the wrong context (see next section).
* Missing files referenced by the config (certificates, include files).

## Context errors: directives must be in the right block

Some directives are only valid in specific contexts (`main`, `http`, `server`, `location`). Putting an `http { ... }` block inside a `server` block will fail.

Example error when a directive is not allowed in this context

```bash theme={null}
root@nginx:~# nginx -t
nginx: [emerg] "http" directive is not allowed here in /etc/nginx/sites-enabled/example-https:33
nginx: configuration file /etc/nginx/nginx.conf test failed
```

Correct usage: `http` is a top-level context in `/etc/nginx/nginx.conf`; `server` and `location` are nested inside it.

Common bad snippet that triggers errors (do not put `http` inside `server`):

```nginx theme={null}
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;

    http {
        access_log /var/log/nginx/access.log;  # WRONG: http block is not allowed here
    }
}
```

## Apply changes gracefully: reload vs restart

Prefer reloading the configuration so worker processes are replaced without dropping connections.

* Reload (graceful): `nginx -s reload` or `sudo systemctl reload nginx`
* Restart (full stop/start): `sudo systemctl restart nginx`

<Callout icon="warning">
  Avoid `restart` unless necessary. `restart` interrupts active connections briefly; `reload` applies configuration changes without downtime when `nginx -t` reports OK.
</Callout>

<Callout icon="lightbulb">
  Always run `nginx -t` and then `nginx -s reload` (or `systemctl reload nginx`) if the test is successful. Use `restart` only for recovering failed workers or replacing the master process.
</Callout>

## Main configuration and logging

The global configuration file `/etc/nginx/nginx.conf` contains the `http` block and global logging settings. When hosting multiple sites, configure per-site logs to simplify debugging.

Example of key sections in `/etc/nginx/nginx.conf`:

```nginx theme={null}
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
}

http {
    ##
    # Basic Settings
    ##
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ##
    # SSL Settings
    ##
    ssl_protocols TLSv1.2 TLSv1.3; # prefer modern TLS
    ssl_prefer_server_ciphers on;

    ##
    # Logging Settings
    ##
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    ##
    # Gzip Settings
    ##
    gzip on;

    ##
    # Virtual Host Configs
    ##
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

Note: It’s safer to leave defaults (like `worker_processes`) unless you understand the performance implications.

### Per-site logging (recommended)

Configure each virtual host to write to its own log directory. Create the directory before reloading NGINX — NGINX will create files but not parent directories.

Example server block for a site with per-site logs:

```nginx theme={null}
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

    access_log /var/log/nginx/example.com/access.log;
    error_log  /var/log/nginx/example.com/error.log;

    add_header Strict-Transport-Security "max-age=31560000; includeSubDomains; preload";
    add_header X-Frame-Options "SAMEORIGIN";
    add_header Content-Security-Policy "default-src 'self'";
    add_header Referrer-Policy origin;

    index index.html index.htm index.nginx-debian.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Create log directory and set ownership

```bash theme={null}
# create the directory (if not present)
sudo mkdir -p /var/log/nginx/example.com
# verify configuration syntax
sudo nginx -t
# set sensible ownership and permissions
sudo chown -R www-data:adm /var/log/nginx/example.com
# reload nginx to apply changes
sudo nginx -s reload
# inspect logs
ls -l /var/log/nginx/example.com
tail -f /var/log/nginx/example.com/access.log
```

## Verify reachability with curl

Use `curl` from the server to check whether NGINX serves requests. This distinguishes between NGINX, DNS, and firewall issues.

Examples:

```bash theme={null}
# quick check to see server response (full body)
curl localhost

# get only headers to check status code quickly
curl --head https://example.com
# or
curl -I https://example.com
```

If NGINX is stopped, `curl` will fail — indicating the service is the problem:

```bash theme={null}
sudo systemctl stop nginx
curl --head https://example.com
# curl will hang/fail because there's no webserver responding
```

## Hosts file for local resolution

For testing or when the server needs to resolve its own hostname, add entries to `/etc/hosts`.

Example:

```text theme={null}
127.0.0.1 localhost example.com www.example.com
# On some distributions (e.g., Debian) you may also see a separate line like:
# IPv6 entries
::1 ip6-localhost ip6-loopback
```

## Firewalls and cloud provider security

Confirm both the server firewall (UFW, firewalld) and any cloud security groups (AWS Security Groups, GCP firewall rules, etc.) allow required ports (80 and 443).

Example `ufw status` output:

```text theme={null}
Status: active

To                         Action      From
--                         -------     ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)
```

Why port 80 still matters

* Even if your site redirects HTTP to HTTPS, leaving port 80 closed prevents users visiting `http://example.com` from being redirected. Best practice: keep both 80 and 443 reachable and redirect HTTP to HTTPS.

## TLS & protocol considerations

Tune TLS settings carefully. Removing older TLS versions improves security but may block very old clients.

Example TLS line to restrict to modern versions:

```nginx theme={null}
ssl_protocols TLSv1.2 TLSv1.3;
```

## Common errors and quick fixes

|                                          Symptom | Likely cause                                                     | Quick fix                                                          |
| -----------------------------------------------: | ---------------------------------------------------------------- | ------------------------------------------------------------------ |
|          `nginx -t` shows syntax error about `;` | Missing semicolon or brace                                       | Fix the syntax and run `nginx -t` again                            |
|      `nginx -t` shows directive not allowed here | Directive placed in wrong context (e.g., `http` inside `server`) | Move directive to appropriate context in `nginx.conf`              |
| Site unreachable from internet but works locally | Cloud security group or external firewall blocks ports           | Open ports 80/443 in cloud firewall and server firewall            |
|                        Logs not created for site | Directory missing or wrong ownership                             | `mkdir -p /var/log/nginx/example.com && chown -R www-data:adm ...` |
|                       Connections drop on deploy | Using `restart` instead of `reload`                              | Use `nginx -s reload` after `nginx -t`                             |

## Final troubleshooting checklist

* Run: `nginx -t` to validate syntax.
* If `nginx -t` is OK: reload with `nginx -s reload` (or `systemctl reload nginx`).
* Check logs in `/var/log/nginx/` and per-site log directories.
* Use `curl` locally (`curl -I`) to verify a working response.
* Verify firewall and cloud security groups allow required ports.
* If changing log paths, ensure directories exist and ownership is correct.
* Confirm TLS settings are compatible with your clients.

## Links and references

* NGINX official docs: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Systemd service control: [https://www.freedesktop.org/software/systemd/man/systemctl.html](https://www.freedesktop.org/software/systemd/man/systemctl.html)
* UFW documentation: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)
* curl manual: [https://curl.se/docs/manpage.html](https://curl.se/docs/manpage.html)

Thanks for reading — I appreciate it.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/53475fbe-d12f-48d7-9602-d4a93debd874" />
</CardGroup>


# Monitoring Troubleshooting

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Performance/Monitoring-Troubleshooting/page

Guide for monitoring and troubleshooting NGINX covering access and error logs, stub_status metrics, monitoring integrations, runtime checks, configuration validation, reloads, and production best practices

This guide explains practical ways to monitor and troubleshoot NGINX. It covers access and error logs, the built-in `stub_status` endpoint, integration options with monitoring platforms, and common runtime checks and commands to validate changes safely.

## Logging

NGINX produces two primary log streams:

* Access logs — record every incoming HTTP request (useful for traffic analysis, response codes, request sizes, user agents, and referers).
* Error logs — record server-side errors and configuration/runtime issues.

You can customize the access log format with the `log_format` directive inside the `http` block. See the NGINX log module docs for full details: [https://nginx.org/en/docs/http/ngx\_http\_log\_module.html](https://nginx.org/en/docs/http/ngx_http_log_module.html)

Example custom log format:

```nginx theme={null}
http {
    log_format custom '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
}
```

Choose the variables that match your analysis and monitoring requirements (for example, add `$host` to capture the requested host header).

Common log variables

<Frame>
  <img alt="A presentation slide titled &#x22;Log Format Options&#x22; that lists common web-server log variables (e.g., remote_addr, remote_user, time_local, request, $status) with short descriptions. The content is shown inside a rounded light-gray box with a KodeKloud copyright." />
</Frame>

| Variable                | Meaning                                        |
| ----------------------- | ---------------------------------------------- |
| `$remote_addr`          | Client IP address.                             |
| `$remote_user`          | Authenticated user (empty if not used).        |
| `$time_local`           | Local timestamp.                               |
| `$request`              | Full request line (method, URI, HTTP version). |
| `$status`               | Response status code (200, 301, 404, etc.).    |
| `$body_bytes_sent`      | Bytes sent in the response body.               |
| `$http_referer`         | Referral URL (if present).                     |
| `$http_user_agent`      | Browser or client user-agent string.           |
| `$http_x_forwarded_for` | Proxy forwarded IPs (when behind a proxy).     |

Enable access logs inside a `server` block (default log files are usually under `/var/log/nginx`):

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html;

    access_log /var/log/nginx/access.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Tail access logs to watch incoming requests in real time:

```bash theme={null}
cd /var/log/nginx/
tail -f access.log
```

Example access log entry (trimmed):

```text theme={null}
192.168.1.1 - - [26/Jan/2025:14:23:35 +0000] "GET /images/logo.png HTTP/1.1" 200 512 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
```

Troubleshooting with access logs:

* Ask a remote user to make a request while you `tail -f` the access log. If there’s no entry, the request didn’t reach NGINX (DNS, client, proxy, or firewall issue).
* Ensure `access_log` is set in the appropriate `http`, `server`, or `location` block. Custom logs won’t be enabled unless explicitly configured.

## Error logs

Error logs capture server-side and runtime issues. They should be quiet during normal operation; frequent errors indicate misconfiguration or application problems. Configure location and verbosity with `error_log`:

```nginx theme={null}
error_log /var/log/nginx/error.log warn;
```

Check `error_log` for stack traces, file-not-found errors, permission problems, or upstream failures.

## NGINX metrics: stub\_status

NGINX provides a lightweight status endpoint through the `stub_status` module (see [https://nginx.org/en/docs/http/ngx\_http\_stub\_status\_module.html](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)). It exposes runtime counters for connections and requests.

Example server block to enable a local-only `/nginx_status` endpoint:

```nginx theme={null}
server {
    listen 81;
    server_name example.com;

    location /nginx_status {
        stub_status;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
}
```

Notes:

* `access_log off;` prevents scrape requests from cluttering logs.
* Restricting access (localhost or your monitoring hosts) and using a nonstandard port reduce exposure.

Query locally:

```bash theme={null}
curl localhost:81/nginx_status
```

Sample output:

```text theme={null}
Active connections: 309
server accepts handled requests
16630948 16630948 31070465
Reading: 11 Writing: 218 Waiting: 38
```

Field meanings:

* Active connections — current client connections.
* accepts — total accepted connections.
* handled — accepted and handled connections.
* requests — total number of client requests.
* Reading/Writing/Waiting — connections reading the request, writing the response, and keep-alive idle connections.

## Monitoring platforms and approaches

There are many solutions for metrics and log aggregation. Common choices include Prometheus + Grafana, Datadog, Dynatrace, and New Relic.

<Frame>
  <img alt="A presentation slide titled &#x22;Monitoring Tools&#x22; displaying the logos and names of Prometheus, Grafana, Datadog, Dynatrace, and New Relic. The logos are arranged inside a rounded rectangle on the slide." />
</Frame>

| Tool                                                                   | Type                             | Typical use                                                                  |
| ---------------------------------------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------- |
| [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/) | Open-source metrics + dashboards | Scrape `stub_status` via an exporter, create dashboards and alerts.          |
| [Datadog](https://www.datadoghq.com/)                                  | SaaS monitoring                  | Agent collects system and NGINX metrics, ingest logs, dashboards and alerts. |
| [Dynatrace](https://www.dynatrace.com/)                                | SaaS APM                         | Full-stack tracing and infrastructure monitoring.                            |
| [New Relic](https://newrelic.com/)                                     | SaaS APM                         | Application and infrastructure monitoring with log ingestion.                |

Common approach:

* Install an agent on the host (Datadog Agent, Prometheus node\_exporter).
* Collect system metrics (CPU, memory, disk, network) and NGINX metrics (via `stub_status` or an NGINX exporter).
* Centralize logs and metrics, then build dashboards and alerts (error rate, response codes, connection saturation).

## Datadog example

Datadog can ingest both logs and metrics and scrape `stub_status` for basic NGINX metrics. A typical system dashboard includes CPU, memory, load, disk, network, and NGINX charts.

<Frame>
  <img alt="Screenshot of a DataDog system metrics dashboard. It shows multiple monitoring charts—CPU and memory (including a treemap), load averages, disk latency, network traffic and disk usage—for an nginx host." />
</Frame>

Note: NGINX Plus (commercial) exposes additional metrics such as detailed status codes, upstream health, and cache statistics. Open-source NGINX combined with exporters and monitoring tools still provides strong observability for most environments.

## Example log excerpts

Error and request lines can reveal missing files, bad routes, or failing backends:

```text theme={null}
2018/05/16 22:02:02 [error] 1244#1244: *203 open() "/var/www/html/order/2480" failed (2: No such file or directory), client: 127.0.0.1, server: _, request: "GET /order/2480 HTTP/1.1"
2018/05/16 22:02:02 [error] 1244#1244: *202 open() "/var/www/html/send/notice" failed (2: No such file or directory), client: 127.0.0.1, server: _, request: "GET /send/notice HTTP/1.1"
GET /order/2480 HTTP/1.1
GET /send/notice HTTP/1.1
GET /pass/beanserver/refund/2480 HTTP/1.1
GET /pass/beanserver/payment/ HTTP/1.1
GET /pass/beanserver/payment/7794 HTTP/1.1
GET /pass/beanserver/order/8048 HTTP/1.1
GET /pass/beanserver/order/4943 HTTP/1.1
2018/05/16 22:02:01 [error] 1244#1244: *186 open() "/var/www/html/bad" failed (2: No such file or directory), client: 127.0.0.1, server: _, request: "GET /bad HTTP/1.1"
GET /pass/welcome HTTP/1.1
```

## Configuration testing and reloading

Always test configuration changes before applying them to avoid service disruption.

Test configuration syntax:

```bash theme={null}
nginx -t
```

Successful test example:

```text theme={null}
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Sample failure output for misplaced directives or typos:

```text theme={null}
nginx: [emerg] unknown directive "worker_connections" in /etc/nginx/nginx.conf:7
nginx: configuration file /etc/nginx/nginx.conf test failed
2025/01/29 23:46:03 [emerg] 71439#71439: "server" directive is not allowed here in /etc/nginx/sites-enabled/default:39
```

Reload without dropping connections after a successful test:

```bash theme={null}
nginx -s reload
```

Check service status with `systemctl`:

```bash theme={null}
systemctl status nginx
```

Example active service output (trimmed):

```text theme={null}
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2025-01-28 00:18:10 UTC; 1 day 23h ago
     Docs: man:nginx(8)
  Main PID: 2164 (nginx)
    Tasks: 2 (limit: 1130)
   Memory: 24.7M
      CPU: 16.367s
```

If inactive, start and inspect recent logs:

```bash theme={null}
systemctl start nginx
journalctl -u nginx --since "10 minutes ago"
```

<Callout icon="warning">
  Do not run two services bound to the same port (for example, Apache and NGINX both listening on port 80). Port conflicts will prevent the web server from starting.
</Callout>

## Quick runtime checks

If `systemctl` reports NGINX as active but users still have problems, test the local HTTP response:

```bash theme={null}
curl --head localhost
```

Example response:

```text theme={null}
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Thu, 30 Jan 2025 00:10:05 GMT
Content-Type: text/html
Content-Length: 612
Connection: keep-alive
ETag: "67982241-264"
Accept-Ranges: bytes
```

A `200` status shows NGINX is responding locally; next check the application, firewall, DNS, or network path.

## Firewalls and connectivity

Ensure cloud-provider security groups and host firewalls allow ports 80 and 443.

UFW (Ubuntu) example:

```bash theme={null}
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

firewalld (RHEL/CentOS) example:

```bash theme={null}
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

## Production monitoring best practices

* Rotate logs to avoid disk exhaustion (logrotate or your platform’s logging agent).
* Centralize metrics and logs (Prometheus, Datadog, ELK/Opensearch) and set alerts for high error rates, CPU spikes, or connection limits.
* Limit exposure of sensitive endpoints (for example, restrict `/nginx_status` to localhost or specific monitoring hosts).
* Consider NGINX Plus for advanced metrics and commercial support if you need upstream health, cache analytics, and built-in dashboarding.

## Final recommendations

<Callout icon="lightbulb">
  Always validate configuration changes with `nginx -t` before reloading, restrict sensitive endpoints (e.g., `/nginx_status`) to trusted hosts, and centralize logs and metrics to simplify troubleshooting and alerting.
</Callout>

This concludes the monitoring and troubleshooting guide for NGINX. For further reading, see:

* NGINX documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Datadog: [https://www.datadoghq.com/](https://www.datadoghq.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/4a5db5c4-df5f-4291-84f0-013d1c4ce235/lesson/b7d13e4f-c250-4bf4-a964-c072516a654a" />
</CardGroup>
