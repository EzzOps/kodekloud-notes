# You will be prompted to enter and confirm the password.
```

* Add a second user (do NOT use `-c` here):

```bash theme={null}
sudo htpasswd /etc/nginx/conf.d/.htpasswd jsmith
```

2. Using OpenSSL (no extra package required)
   If you prefer not to install apache2-utils, you can append APR1/MD5-style password hashes with `openssl`. Because writing to `/etc/nginx/conf.d/.htpasswd` often requires root privileges, use `sudo sh -c` for each append.

* Add `admin`:

```bash theme={null}
sudo sh -c "echo -n 'admin:' >> /etc/nginx/conf.d/.htpasswd"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/conf.d/.htpasswd"
# You will be prompted to set and verify the password for openssl.
```

* Add `jsmith` similarly:

```bash theme={null}
sudo sh -c "echo -n 'jsmith:' >> /etc/nginx/conf.d/.htpasswd"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/conf.d/.htpasswd"
```

Notes on storage and hashing

* The file stores hashed passwords (APR1/MD5-style in these examples) — plaintext passwords are not recoverable from the file.
* Store credentials securely using a secrets manager (e.g., 1Password, HashiCorp Vault) when possible.

Viewing and verifying the file
To inspect the htpasswd file and confirm entries:

```bash theme={null}
cat /etc/nginx/conf.d/.htpasswd
```

Example output:

```text theme={null}
admin:$apr1$egX1fPMK$EXwGqVFsOSBFsQNJMc2iB0
jsmith:$apr1$L5aCfsuK$XPsXg11JMTQpd0ihTVyus.
```

Configure NGINX to require authentication
Add `auth_basic` and `auth_basic_user_file` within the `server` or `location` block for the path you want to protect (here `/admin`). Use a quoted string for the `auth_basic` prompt and include trailing semicolons.

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html;

    location /admin {
        auth_basic "Restricted Content";
        auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    }
}
```

Test and reload NGINX

* Test the configuration:

```bash theme={null}
sudo nginx -t
```

* If the test passes, reload NGINX:

```bash theme={null}
sudo systemctl reload nginx
# or: sudo nginx -s reload
```

Behavior
When you visit `http://example.com/admin` (or `https://example.com/admin` if TLS is configured), the browser will display a login dialog using the `auth_basic` string (e.g., "Restricted Content"). Enter a username and password from the `.htpasswd` file to proceed.

Important security reminder

<Callout icon="warning">
  Always use HTTPS when using HTTP Basic Authentication. Basic auth sends credentials Base64-encoded with each request; over plain HTTP they can be intercepted. Configure TLS in NGINX and use certificate best practices for any protected endpoints on untrusted networks.
</Callout>

Best practices and final notes

* Basic auth is great for quick protection of internal or staging sites, admin panels, and simple gating scenarios.
* Because the browser prompt cannot be styled, consider application-level authentication or OAuth/SSO for public-facing user experiences.
* Rotate credentials periodically and manage them with a secure secrets store for production-sensitive use.
* Prefer `htpasswd` for convenience; use `openssl` only when adding a minimal dependency is preferred.

Links and references

* NGINX official docs: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Apache htpasswd utility / apache2-utils: [https://httpd.apache.org/docs/current/programs/htpasswd.html](https://httpd.apache.org/docs/current/programs/htpasswd.html)
* OpenSSL passwd: [https://www.openssl.org/docs/man1.1.1/man1/openssl-passwd.html](https://www.openssl.org/docs/man1.1.1/man1/openssl-passwd.html)
* Secrets management: HashiCorp Vault — [https://www.vaultproject.io/](https://www.vaultproject.io/); 1Password — [https://1password.com/](https://1password.com/)

Try this workflow in a test environment first to validate configuration and behavior before applying to production.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/3082fc69-784b-4bf2-b7d0-b19c7fb94952" />
</CardGroup>


# Blocking Traffic

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Blocking-Traffic/page

Explains blocking unwanted traffic using NGINX allow/deny and Fail2Ban for automated IP bans and rate limiting to protect web applications.

Attackers can steal data, spread malware (spyware or ransomware), or even take a site offline. While many bots are benign (search engine crawlers), others scrape content, post spam, or generate fake reviews. Blocking unwanted traffic early reduces risk and preserves resources.

<Frame>
  <img alt="An infographic titled &#x22;Hackers&#x22; showing a hooded attacker at computer screens with a skull emblem. Above are icons and labels for &#x22;Steal data,&#x22; &#x22;Spread spyware and ransomware,&#x22; and &#x22;Take down the whole site.&#x22;" />
</Frame>

A common defensive stack combines authentication, service-level controls, and automated blocking. One service-level control is blocking IPs and ranges at the NGINX layer to prevent known bad actors or unexpected network ranges from reaching your application.

<Frame>
  <img alt="A diagram titled &#x22;Blocking Traffic&#x22; showing three sources—IPs, Bots, and Network Traffic—being routed toward a website and stopped by a red prohibited symbol. Colorful icons represent each traffic source and a stylized webpage on the right shows the blocked content." />
</Frame>

## NGINX access control: allow / deny

NGINX uses the http\_access module to control access via `allow` and `deny` directives (see the official docs: [https://nginx.org/en/docs/http/ngx\_http\_access\_module.html](https://nginx.org/en/docs/http/ngx_http_access_module.html)). Place these directives inside `http`, `server`, or `location` blocks to permit or block traffic by IPv4/IPv6 address or CIDR block.

Example — allow two specific IPv4 addresses and deny all other traffic:

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html;

    allow 192.168.1.100/32;
    allow 174.168.100.252/32;
    deny all;
}
```

To block a range, use CIDR prefixes. Example — deny a `/24` range and allow a specific `/24` inside a location:

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html;

    deny 203.0.113.0/24;

    location /admin {
        allow 174.0.252.0/24;
        deny all;
        try_files $uri $uri/ =404;
    }
}
```

Use CIDR to express address scope efficiently:

* `/32` — single IPv4 address
* `/24` — block of 256 addresses (e.g., `203.0.113.0` through `203.0.113.255`)

<Callout icon="lightbulb">
  CIDR quick reminder: `/32` = one IPv4 address; `/24` = 256 addresses. Use CIDR notation to manage large address sets instead of listing many single addresses.
</Callout>

However, adding many `allow`/`deny` rules directly to NGINX configuration files does not scale well. Attackers rotate IPs, and long lists make configuration brittle and hard to maintain.

<Frame>
  <img alt="A slide titled &#x22;Not Scalable&#x22; showing two columns labeled &#x22;Allow&#x22; (with a green check) and &#x22;Deny&#x22; (with a red X) listing several IP addresses under each. The allow column contains five IPs and the deny column contains two IPs." />
</Frame>

## Automated blocking with Fail2Ban

For many deployments, using an automated agent to monitor logs and apply short-term bans is more effective than static lists. Fail2Ban ([https://www.fail2ban.org](https://www.fail2ban.org)) watches log files for suspicious patterns and updates host firewall rules (iptables, nftables, or firewalld) to block offending IPs temporarily.

<Frame>
  <img alt="The image shows the Fail2Ban logo: a small cartoon house with a red &#x22;stop&#x22; sign featuring a raised hand, above the text &#x22;FAIL2BAN.&#x22; A caption below explains it enhances server security by blocking malicious IPs, especially against brute‑force attacks." />
</Frame>

Fail2Ban is especially effective against brute-force attempts and repeated abuse because it:

* Parses logs for configurable regex patterns (filters).
* Applies bans when thresholds are exceeded (jails).
* Unbans automatically after a configured `bantime`.

Example runtime output (tailing the Fail2Ban log):

```bash theme={null}
ubuntu@linux:~$ sudo tail -f /var/log/fail2ban.log
2024-08-10 19:26:27,469 fail2ban.jail    [7786]: INFO    Creating new jail 'ssh'
2024-08-10 19:26:27,469 fail2ban.jail    [7786]: INFO    Jail 'ssh' uses pyinotify {}
2024-08-10 19:26:27,472 fail2ban.jail    [7786]: INFO    Initiated 'pyinotify' backend
2024-08-10 19:26:27,473 fail2ban.filter  [7786]: INFO    maxLines: 1
2024-08-10 19:26:27,473 fail2ban.filter  [7786]: INFO    maxRetry: 2
2024-08-10 19:26:27,473 fail2ban.filter  [7786]: INFO    findtime: 300
2024-08-10 19:26:27,473 fail2ban.filter  [7786]: INFO    banTime: 86400
2024-08-10 19:26:27,473 fail2ban.filter  [7786]: INFO    encoding: UTF-8
2024-08-10 19:26:27,475 fail2ban.jail    [7786]: INFO    Jail 'sshd' started
2024-08-10 19:26:46,275 fail2ban.filter  [7786]: INFO    [sshd] Found 192.168.8.131 - 2024-08-10 19:26:46
2024-08-10 19:27:40,771 fail2ban.actions [7786]: NOTICE  [sshd] Ban 192.168.8.131
```

### Installing Fail2Ban

Common installation commands:

| Distribution family    | Install command                                            |
| ---------------------- | ---------------------------------------------------------- |
| Debian / Ubuntu        | `sudo apt install fail2ban`                                |
| RHEL / CentOS / Fedora | `sudo yum install fail2ban` or `sudo dnf install fail2ban` |

After installation, create a local override and configure jails:

```bash theme={null}
cd /etc/fail2ban
sudo cp jail.conf jail.local
sudo vim jail.local
```

### Example Fail2Ban jails for NGINX

Add jails to `jail.local` to enable NGINX-related monitoring:

```ini theme={null}
[nginx-http-auth]
enabled  = true
port     = http,https
filter   = nginx-http-auth
logpath  = /var/log/nginx/access.log
maxretry = 3
bantime  = 600
findtime = 600
```

Block known bad bots with a longer ban:

```ini theme={null}
[nginx-badbots]
enabled  = true
port     = http,https
filter   = nginx-badbots
logpath  = /var/log/nginx/access.log
maxretry = 1
bantime  = 48h
```

Rate-limit excessive requests:

```ini theme={null}
[nginx-limit-req]
enabled  = true
port     = http,https
filter   = nginx-limit-req
logpath  = /var/log/nginx/access.log
maxretry = 10
bantime  = 24h
findtime = 60m
```

Fail2Ban filters are stored in `/etc/fail2ban/filter.d`. Many filters are included by default.

```bash theme={null}
cd /etc/fail2ban/filter.d
ls -la
```

Example filter file listing (illustrative):

```text theme={null}
-rw-r--r-- 1 root root  474 Nov  9  2022 nginx-bad-request.conf
-rw-r--r-- 1 root root  740 Nov  9  2022 nginx-botsearch.conf
-rw-r--r-- 1 root root 1048 Nov  9  2022 nginx-http-auth.conf
-rw-r--r-- 1 root root 1513 Nov  9  2022 nginx-limit-req.conf
```

Sample snippet from `nginx-http-auth.conf` (truncated):

```ini theme={null}
[Definition]
mode = normal
