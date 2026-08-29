# Example regex patterns; <HOST> is replaced by Fail2Ban with the matched IP
mdre-auth = ^\s*\[error\] \d+#\d+: \*\d+ user "(?:[^"]+|.*?)"?:? (?:password mismatch|was not found in "[^"]*"), client: <HOST>, server: \S*, request: "\S+ \S+ HTTP/\d+\.\d+", host: "\S+"(?:, referrer: "\S+")?\s*$
mdre-fallback = ^\s*\[crit\] \d+#\d+: \*\d+ SSL_do_handshake\(\) failed \(SSL: error:\S+(?: \S+){1,3} too (?:long|short)\)[^,]*, client: <HOST>
```

These filters use regular expressions to match authentication failures or other suspicious log lines. When the configured thresholds (e.g., `maxretry` within `findtime`) are exceeded, Fail2Ban triggers the ban action.

### Managing Fail2Ban and banned IPs

Check jail status and currently banned IPs:

```bash theme={null}
sudo fail2ban-client status nginx-http-auth
```

Example output:

```text theme={null}
Status for the jail: nginx-http-auth
|- Filter
|  |- Currently failed: 0
|  `- File list: /var/log/nginx/access.log
`- Actions
   |- Currently banned: 1
   `- Banned IP list: 192.0.2.45
```

To unban an IP:

```bash theme={null}
sudo fail2ban-client set nginx-http-auth unbanip 192.0.2.45
```

Because Fail2Ban operates on host logs and firewall rules, it typically requires no change to application configurations to be effective.

<Callout icon="warning">
  Fail2Ban depends on host log files and the host firewall. It may not work as expected in ephemeral container environments or Kubernetes clusters where logs are aggregated or networking is managed by the platform. For containers, consider ingress rate limiting, a Web Application Firewall (WAF), or platform-native network policies.
</Callout>

## Quick reference

| Topic            | Notes / Commands                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| NGINX allow/deny | Use `allow` and `deny` in `http`, `server`, or `location` blocks. See `ngx_http_access_module`.                             |
| CIDR examples    | Use `/32` for a single IPv4 address, `/24` for a 256-address block.                                                         |
| Install Fail2Ban | Debian/Ubuntu: `sudo apt install fail2ban` — RHEL/CentOS/Fedora: `sudo yum install fail2ban` or `sudo dnf install fail2ban` |
| Check jails      | `sudo fail2ban-client status <jailname>`                                                                                    |
| Unban IP         | `sudo fail2ban-client set <jailname> unbanip <IP>`                                                                          |

In this lesson you learned:

* How to use NGINX `allow`/`deny` with CIDR notation to block IPs or ranges.
* Why long static lists in NGINX are hard to maintain and scale poorly.
* How Fail2Ban dynamically blocks abusive IPs by monitoring logs and updating firewall rules.
* Basic Fail2Ban configuration patterns and how to inspect/unban IPs.

If you're testing locally on Ubuntu:

1. Install Fail2Ban (`sudo apt install fail2ban`).
2. Copy `jail.conf` to `jail.local` and enable the NGINX jails you need.
3. Tail `/var/log/fail2ban.log` and `/var/log/nginx/access.log` to verify detection and bans.

Useful references:

* NGINX access module: [https://nginx.org/en/docs/http/ngx\_http\_access\_module.html](https://nginx.org/en/docs/http/ngx_http_access_module.html)
* Fail2Ban project: [https://www.fail2ban.org](https://www.fail2ban.org)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/328c0054-1639-4d6d-aeda-f1255e8ebaa0" />
</CardGroup>


# Demo Authentication

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Demo-Authentication/page

Shows how to add Basic Auth to an NGINX site to protect an /admin path using auth_basic and an .htpasswd file, with setup, testing, and alternatives

In this lesson we implement basic authentication on an NGINX server to protect a single endpoint. The public site will remain open, while an `/admin` path will require a username and password.

Example site:

```text theme={null}
https://www.example.com
```

Open a terminal on the NGINX host and confirm the site is reachable. The generic public page looks like this:

<Frame>
  <img alt="A screenshot of a clean webpage template called &#x22;Phantom&#x22; with a large headline announcing it's a free, fully responsive HTML5 UP template. Below the header is a grid of colorful square tiles labeled with words like &#x22;Magna&#x22;, &#x22;Lorem&#x22;, and &#x22;Feugiat&#x22;." />
</Frame>

At this point, visiting `https://www.example.com/admin` shows the same public page because authentication isn't enabled yet. We'll update the NGINX configuration to require Basic Auth only for the `/admin` location.

## Update the NGINX server configuration

Edit your site configuration (for example `/etc/nginx/sites-available/example-https`) and add a `location /admin` block with `auth_basic` and `auth_basic_user_file`. This example server block shows a minimal HTTPS configuration with the `/admin` protection:

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com www.example.com;

    ssl_certificate /etc/ssl/certs/example.com.pem;
    ssl_certificate_key /etc/ssl/certs/example.com-key.pem;

    root /var/www/html;

    add_header Strict-Transport-Security "max-age=31560000; includeSubDomains; preload";
    add_header X-Frame-Options "SAMEORIGIN";
    add_header Content-Security-Policy "default-src 'self'";
    add_header Referrer-Policy origin;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }

    location /admin {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    }
}
```

Quick reference: what the key directives do

| Directive                                 |                                                    Purpose | Example                                             |
| ----------------------------------------- | ---------------------------------------------------------: | --------------------------------------------------- |
| `auth_basic`                              |  Sets the authentication realm shown in the browser prompt | `auth_basic "Restricted Access";`                   |
| `auth_basic_user_file`                    | Path to the htpasswd-style file with encrypted credentials | `auth_basic_user_file /etc/nginx/conf.d/.htpasswd;` |
| `try_files`                               |             Fallback behavior to serve files or return 404 | `try_files $uri $uri/ =404;`                        |
| `ssl_certificate` / `ssl_certificate_key` |                           TLS certificate and key location | `/etc/ssl/certs/example.com.pem`                    |

Notes:

* `auth_basic` is the realm string that appears in the browser prompt (here: `"Restricted Access"`).
* `auth_basic_user_file` should point to a readable file containing `username:encrypted-password` entries.

## Create the `.htpasswd` file and add a user

Create the `.htpasswd` file and add a user (we'll add `admin` in this example). The commands below create or overwrite the file and append an APR1 (Apache MD5) encrypted password produced by `openssl passwd`:

```bash theme={null}
