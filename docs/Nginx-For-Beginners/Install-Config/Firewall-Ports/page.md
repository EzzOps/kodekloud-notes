# Basic Settings
##

sendfile on;
tcp_nopush on;
tcp_nodelay on;
keepalive_timeout 65;
types_hash_max_size 2048;
# server_names_hash_bucket_size 64;
include /etc/nginx/mime.types;
default_type application/octet-stream;

##
# SSL Settings
##

ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
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

# gzip_vary on;
# gzip_proxied any;
# gzip_comp_level 6;
# gzip_buffers 16 8k;
# gzip_http_version 1.1;
# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript
;

##
# Virtual Host Configs
##

include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
}
```

Notes:

* `include /etc/nginx/conf.d/*.conf` and `include /etc/nginx/sites-enabled/*` pull in additional server blocks and per-site configs.
* Best practice: keep site definitions in `sites-available/` and enable them by symlinking into `sites-enabled/`. Keep `nginx.conf` focused on global settings.

<Callout icon="warning">
  Always validate configuration changes before reloading the service. Run `sudo nginx -t` to test syntax and correctness. Failing to test can cause Nginx to reject a reload and potentially interrupt service.
</Callout>

Before applying changes:

```bash theme={null}
sudo nginx -t
```

If the test is successful, reload Nginx to apply configuration changes without restarting the process:

```bash theme={null}
sudo systemctl reload nginx
```

## 6. Logs

Nginx writes its logs to `/var/log/nginx` by default. List the directory to find the access and error logs:

```bash theme={null}
cd /var/log/nginx/
ll
```

Example output after a fresh install:

```bash theme={null}
bob@alpine-host /var/log/nginx🔒 ➜ ll
total 16
drwxr-xr-x 2 root     adm    4096 Feb  5 11:58 ./
drwxr-xr-x 1 root     root   4096 Feb  5 11:58 ../
-rw-r----- 1 www-data adm     86 Feb  5 12:00 access.log
-rw-r----- 1 www-data adm      0 Feb  5 11:58 error.log
```

* `access.log` records requests served by Nginx.
* `error.log` records runtime errors and warnings.
  You can configure per-site log locations inside server blocks to separate logs per virtual host.

## Next steps

In a follow-up lesson you'll learn to:

* Create and enable site configurations (virtual hosts) using `sites-available` and `sites-enabled`.
* Configure custom access/error logs per site.
* Add SSL/TLS (Let’s Encrypt) and multi-site server blocks for secure hosting.

For further reading:

* Nginx Beginner’s Guide: [https://nginx.org/en/docs/beginners\_guide.html](https://nginx.org/en/docs/beginners_guide.html)
* Ubuntu Nginx package on Launchpad/Debian packaging notes (for distro-specific differences).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/8a76fda2-9055-43c0-af1e-f08df0c8cb1a" />
</CardGroup>


# Firewall Ports

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Firewall-Ports/page

Guide to firewall ports, how firewalls control network traffic, common web and SSH ports, and managing rules with UFW, Firewalld and inspection tools like ss or netstat.

A firewall is a software or hardware security guard that sits between your system and the internet. It inspects and controls network traffic flowing in and out of a host or network to block unwanted access and reduce attack surface.

<Frame>
  <img alt="An infographic showing a computer behind a dashed boundary protected by a brick-and-shield firewall icon between it and a wireless router. A caption reads, &#x22;It acts like a barrier between the system and the internet.&#x22;" />
</Frame>

Think of a firewall like a home security system: it watches doors and windows and only lets approved people in. Firewalls can be implemented as host-level software (common on personal and server OSes) or as dedicated hardware appliances in data centers.

Linux distributions expose firewall management tools as friendly front-ends to the kernel packet-filtering system (historically `iptables`, increasingly `nftables`). For example:

* Debian / Ubuntu: UFW (Uncomplicated Firewall)
* Red Hat / Fedora / CentOS: Firewalld

Both tools configure the kernel packet filters; the kernel enforcement is what actually permits or blocks packets.

<Frame>
  <img alt="A slide titled &#x22;Firewall&#x22; showing Red Hat and Fedora logos side by side, with bullet notes mentioning installing via YUM and that iptables comes pre-installed in Linux distros." />
</Frame>

Windows and macOS include built-in firewalls as well. Windows Firewall is typically enabled by default; macOS firewall must usually be enabled manually. Whatever platform you use, enable the firewall and only allow the traffic you need.

Ports — what are they?

A port is a network communication endpoint used by services on a computer. If a computer is a house, ports are the doors and windows. Close the ones you don’t need and only open the ones required by your services. For web traffic these are:

<Frame>
  <img alt="A diagram titled &#x22;Common Ports&#x22; showing client computers routed through a Web Application Firewall (a brick wall with flames) to origin servers. Two clients are allowed (green checkmarks) while a malicious client is blocked (red X) by the WAF." />
</Frame>

| Service        | Port(s) | Notes                                                           |
| -------------- | ------- | --------------------------------------------------------------- |
| HTTP           | `80`    | Unencrypted web traffic                                         |
| HTTPS          | `443`   | Encrypted web traffic (TLS)                                     |
| SSH            | `22`    | Secure shell for remote administration — always treat carefully |
| Other services | varies  | Expose only when necessary; prefer whitelisting IPs             |

You don’t need to memorize every port number, but know `80`, `443`, and `22`. For servers exposed to the public internet, generally only open the web ports (80/443) and any management port (like SSH) restricted to trusted IPs. If you must open additional ports, prefer IP whitelisting or VPN access over broad exposure.

<Callout icon="warning">
  Avoid opening ports to “anywhere” unless absolutely necessary. Exposing management ports to the internet increases risk—use IP allowlists, SSH keys, or a VPN.
</Callout>

Managing UFW (Debian / Ubuntu)

Before enabling UFW on a remote machine, allow SSH so you don't lock yourself out.

<Callout icon="lightbulb">
  Always allow SSH first. Example: `sudo ufw allow 22/tcp` before running `sudo ufw enable` on a remote server.
</Callout>

Common UFW commands:

```bash theme={null}
