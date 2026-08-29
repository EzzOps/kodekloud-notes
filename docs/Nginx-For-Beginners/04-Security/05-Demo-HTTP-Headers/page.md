# HTTP (redirects to HTTPS)
curl http://example.com

# HTTPS without trusting the CA: fails with certificate verification error
curl https://example.com
# Example error:
# curl: (60) SSL certificate problem: unable to get local issuer certificate
```

To bypass certificate verification for testing only, use `-k` (equivalent to `--insecure`):

<Callout icon="lightbulb">
  Using `-k` disables certificate verification. Only use it for testing; do not use it in production scripts.
</Callout>

```bash theme={null}
# Send a HEAD request and ignore cert verification
curl -k --head https://example.com

# Sample response headers (truncated)
# HTTP/1.1 200 OK
# Server: nginx/1.18.0 (Ubuntu)
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# ...
```

If you request the protected `/admin` without credentials, Nginx returns `401 Unauthorized`:

```bash theme={null}
curl -k --head https://example.com/admin
# HTTP/1.1 401 Unauthorized
# WWW-Authenticate: Basic realm="Restricted Access"
```

***

## Manually block a single IP with `deny`

To block a specific IP (for example `node02` with IP `192.231.128.3`), add a `deny` directive in the `location /` block. Example:

```nginx theme={null}
location / {
    deny 192.231.128.3/32; # node02
    try_files $uri $uri/ =404;
}
```

After editing the Nginx site file, test and reload Nginx:

```bash theme={null}
nginx -t
nginx -s reload
```

Expected outcome:

* node01 (allowed) → receives `200 OK`.
* node02 (denied) → receives `403 Forbidden`.

***

## Allow only one IP to access `/admin` and deny all others

To permit a single management IP (e.g., `node01` at `192.231.128.12`) to access `/admin` and deny everyone else, use `allow` followed by `deny all` inside the `/admin` location:

```nginx theme={null}
location /admin {
    allow 192.231.128.12/32; # node01
    deny all;
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
}
```

Notes:

* Each `allow` and `deny` directive requires a trailing semicolon.
* If the allowed client supplies an invalid username/password, Nginx will still return `401 Unauthorized` because `auth_basic` runs after the allow/deny check.

***

## Allow a whole subnet (CIDR) instead of many single IPs

Instead of maintaining many `/32` entries, permit an entire subnet. For example, to allow the `192.231.128.0/24` network (which contains `node01` and `node02`), use:

```nginx theme={null}
location / {
    allow 192.231.128.0/24; # node01 and node02
    deny all;
    try_files $uri $uri/ =404;
}

location /admin {
    allow 192.231.128.0/24; # node01 and node02
    deny all;
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
}
```

CIDR quick reference:

| CIDR  | What it means                                                                                            |
| ----- | -------------------------------------------------------------------------------------------------------- |
| `/32` | Only the exact IP specified is allowed (single host).                                                    |
| `/24` | The first three octets are fixed; the last octet ranges 0–255 (e.g., `192.231.128.0`–`192.231.128.255`). |

Remember: include the trailing semicolon: `allow 192.231.128.0/24;`

***

## Why not maintain long deny lists? Use fail2ban to automate bans

Manually maintaining long `deny` lists in Nginx becomes cumbersome and error-prone. [fail2ban](https://www.fail2ban.org/) monitors logs (including Nginx error logs), detects repeated failures (such as failed HTTP Basic auth attempts), and adds temporary firewall rules (bans) for misbehaving IPs.

Install and configure fail2ban (Debian/Ubuntu example):

```bash theme={null}
sudo apt update -y
sudo apt install -y fail2ban
```

Create a local config so package updates don't overwrite your settings:

```bash theme={null}
cd /etc/fail2ban
sudo cp jail.conf jail.local
```

Enable and configure the `nginx-http-auth` jail by adding or editing a snippet in `/etc/fail2ban/jail.local`:

```ini theme={null}
[nginx-http-auth]
enabled    = true
port       = http,https
filter     = nginx-http-auth
logpath    = %(nginx_error_log)s
maxretry   = 1
bantime    = 600
```

fail2ban option meanings:

| Option     | Description                                                          |
| ---------- | -------------------------------------------------------------------- |
| `enabled`  | Enable this jail when `true`.                                        |
| `port`     | Ports to apply the ban to (`http`, `https`).                         |
| `filter`   | The filter name (matches patterns in logs).                          |
| `logpath`  | Path to the Nginx error log where failed auth attempts are recorded. |
| `maxretry` | Number of failures before banning (`1` = ban after one failure).     |
| `bantime`  | Duration of the ban in seconds (`600` = 10 minutes).                 |

<Callout icon="warning">
  Setting `maxretry = 1` will ban after a single failed authentication attempt. For production, increase `maxretry` to reduce false positives and tune `bantime` to suit your environment.
</Callout>

Start/restart fail2ban and check the status:

```bash theme={null}
# Start or restart using systemd
sudo systemctl restart fail2ban
sudo systemctl enable --now fail2ban

# Or reload filters/config without restarting service
sudo fail2ban-client reload

# Show global status
sudo fail2ban-client status

# Show status for the nginx-http-auth jail
sudo fail2ban-client status nginx-http-auth
```

Sample output for the `nginx-http-auth` jail:

```text theme={null}
Status for the jail: nginx-http-auth
|- Filter
|  |- Currently failed: 0
|  |- Total failed:  2
|  `- File list:     /var/log/nginx/error.log
`- Actions
   |- Currently banned: 1
   |- Total banned:     2
   `- Banned IP list:   174.0.252.84
```

To unban an IP:

```bash theme={null}
# Unban an IP from a specific jail
sudo fail2ban-client set nginx-http-auth unbanip 174.0.252.84
```

***

When a client accesses `/admin` from a browser and submits incorrect credentials, the browser's sign-in prompt appears. Repeated failed attempts will be detected by fail2ban and the IP will be banned according to your jail settings.

<Frame>
  <img alt="A browser screenshot showing a sign-in dialog for &#x22;https://example.com&#x22; with the username &#x22;admin&#x22; filled in and a masked password field, plus &#x22;Cancel&#x22; and &#x22;Sign In&#x22; buttons. The rest of the page is mostly blank." />
</Frame>

After a failed attempt (or the number specified by `maxretry`), fail2ban will add the client's IP to the banned list and access to `/admin` (and possibly other HTTP(S) ports) will be blocked until the ban expires or is removed.

***

## Option: Let fail2ban handle blocking instead of large `deny` lists

If you want Nginx config to remain simple and prefer dynamic blocking, do not add `allow` / `deny` rules on the site root. Instead, rely on fail2ban jails to block offenders. Example server config without `allow`/`deny`:

```nginx theme={null}
server {
    listen 443 ssl;

    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.com.pem;
    ssl_certificate_key /etc/ssl/certs/example.com-key.pem;

    root /var/www/html;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
    add_header X-Frame-Options "SAMEORIGIN";
    add_header Content-Security-Policy "default-src 'self'";
    add_header Referrer-Policy origin;

    index index.html index.htm index.nginx-debian.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /admin {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    }
}
```

This approach keeps Nginx configuration manageable and lets fail2ban dynamically add IP-level blocks in the firewall when repeated failures are detected.

***

## Summary & best practices

* Use Nginx `allow`/`deny` for small, static lists of trusted or blocked IPs.
* Use CIDR ranges (`/24`, `/16`, etc.) to cover networks instead of many `/32` entries.
* For automated handling of attackers (e.g., repeated failed HTTP Basic auth attempts), use [fail2ban](https://www.fail2ban.org/) to monitor Nginx logs and apply temporary bans.
* Tune fail2ban `maxretry` and `bantime` to balance security and the risk of false positives in your environment.

Further reading:

* [Nginx documentation — ngx\_http\_access\_module](https://nginx.org/en/docs/http/ngx_http_access_module.html)
* [fail2ban documentation](https://www.fail2ban.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/a317f900-cb06-48ac-822a-12a9f64d432f" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/66fef843-b5b8-4c77-a01b-ce3999f9643c" />
</CardGroup>


# Demo HTTP Headers

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Demo-HTTP-Headers/page

Configuring NGINX to add security HTTP headers, terminate TLS, load balance to Apache backends, forward proxy headers, and update Apache logs to record original client information.

In this lesson we configure an NGINX server to return a set of security HTTP headers, then extend that configuration to act as a TLS-terminating load balancer that forwards requests to two Apache backend servers. We also pass useful proxy headers so the Apache backends can log the original client information for debugging and auditing.

Flow overview:

* Inspect current response headers from the site.
* Add security headers to the TLS (`listen 443 ssl`) server block.
* Configure an `upstream` block and proxy traffic to two Apache backends.
* Add `proxy_set_header` directives so the backend sees the original client IP and scheme.
* Update Apache logging to include forwarded headers or use `mod_remoteip`.

<Frame>
  <img alt="A simple diagram showing a desktop computer on the left communicating with a website/browser window on the right via dashed arrows to represent requests and responses. Icons of a magnifying glass over code and a small HTTP request/status box indicate inspection and response details." />
</Frame>

We will then configure NGINX as a load balancer to distribute traffic to two backend Apache servers and include proxy headers so the Apache logs record useful client information (instead of all requests appearing to come from the load balancer).

<Frame>
  <img alt="A simple architecture diagram showing a user/browser sending requests to an NGINX load balancer which distributes traffic to two backend web servers. The two web servers are running Apache HTTP Server and are labeled 1 and 2." />
</Frame>

***

## 1) Initial checks — inspect current headers

I added an internal DNS entry for `example.com` pointing to loopback. For example, your `/etc/hosts` may include:

```bash theme={null}
root@nginx ~ ➜ cat /etc/hosts
127.0.0.1        localhost
::1              localhost ip6-localhost ip6-loopback
fe00::0          ip6-localnet
ff00::0          ip6-mcastprefix
ff02::1          ip6-allnodes
ff02::2          ip6-allrouters
192.231.70.6     nginx
127.0.0.1        example.com
```

Check headers with curl:

```bash theme={null}
root@nginx ~ ➜ curl --head https://example.com
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Wed, 12 Feb 2025 19:24:14 GMT
Content-Type: text/html
Content-Length: 8710
Last-Modified: Wed, 12 Feb 2025 18:42:19 GMT
Connection: keep-alive
ETag: "67aceb8b-2206"
Accept-Ranges: bytes
```

In the browser: open DevTools → Network → select a resource to view response headers. At this point the server returns standard headers such as `Server` and `Date`, but no custom security headers yet.

***

## 2) Add security headers in NGINX (TLS server block)

Edit your site config (e.g., `/etc/nginx/sites-available/example-https`) and add the security headers inside the `server { listen 443 ssl; ... }` block.

Example configuration:

```nginx theme={null}
