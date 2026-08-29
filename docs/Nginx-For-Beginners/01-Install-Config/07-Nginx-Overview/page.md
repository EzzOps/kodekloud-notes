# Debian / Ubuntu (APT)
sudo apt update
sudo apt install -y nginx
sudo apt remove -y package_name
sudo apt upgrade -y
sudo apt-cache search package_name

# Red Hat / CentOS / Fedora (YUM/DNF)
# On newer Fedora/RHEL systems, prefer dnf (e.g., sudo dnf install ...)
sudo yum update -y
sudo yum install -y nginx
sudo yum remove -y package_name
sudo yum search package_name

# macOS / Linux (Homebrew)
brew update
brew install nginx
brew uninstall package_name
brew search package_name

# Windows (Chocolatey)
choco install nginx -y
choco uninstall package_name -y
```

Summary

* Always prefer your platform's package manager to install NGINX (or other software). Package managers handle dependency resolution, updates, and clean removal in a consistent way.
* Next: a demo that shows step-by-step installation and basic configuration of NGINX using the package manager appropriate for your OS.

Links and references

* [NGINX: Official Download and Installation Guides](https://nginx.org/en/docs/install.html)
* [APT Guide (Debian/Ubuntu)](https://wiki.debian.org/Teams/Apt)
* [DNF Documentation (Fedora)](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
* [Homebrew Documentation](https://brew.sh/)
* [Chocolatey Documentation](https://chocolatey.org/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/1b1f4be9-32f7-441a-ae68-f5dd0e0a9c6f)


# Nginx Overview

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Nginx-Overview/page

Concise guide to NGINX configuration structure, key directives, server blocks, common files and commands for managing and troubleshooting NGINX.

This guide gives a concise, practical overview of NGINX configuration and the structure of the primary configuration file, `nginx.conf`. It explains the typical file layout, key configuration blocks, example snippets, and common commands you’ll use when managing NGINX. This is ideal for beginners and engineers who need a quick reference while editing configs.

> **lightbulb** On most Linux distributions `nginx.conf` lives at `/etc/nginx/nginx.conf`. You can confirm this with `nginx -V` which prints the configured paths.

You’ll typically see this high-level structure in `nginx.conf`:

* Global settings — server-wide options (user, worker counts, pid file, etc.)
* `events` block — connection and event model settings
* `http` block — HTTP-level configuration and includes for server blocks
* `server` blocks — virtual hosts that define how NGINX responds to requests

Global settings apply to the whole NGINX instance: user privileges, number of worker processes, PID file, and other server-wide behaviors. Features like compression and caching are usually configured inside the `http` block rather than the global scope.

<Frame>
  <img alt="A slide titled &#x22;Structure of nginx.conf&#x22; showing a &#x22;Global Settings&#x22; box that &#x22;set up configurations that affect the entire Nginx server.&#x22; Below are icons and labels for examples like user privileges, number of worker processes, and rate limiting settings." />
</Frame>

## events block

The `events` block controls how worker processes handle connections and the event model (select/epoll/kqueue). A minimal `events` block:

```nginx theme={null}
events {
    worker_connections 1024;
    use epoll;
}
```

Key points:

* `worker_connections` sets the max simultaneous connections each worker can handle.
* Total theoretical concurrent connections ≈ `worker_processes * worker_connections`.
* Real limits depend on OS file descriptor limits (ulimit), socket limits, and other factors — treat the formula as an approximation.
* `use` is optional; NGINX auto-selects the best mechanism if you omit it (`epoll` on Linux, `kqueue` on BSD/macOS).

## http block

The `http` block holds HTTP-specific settings: logging, compression, MIME types, keepalives, and includes for `server` blocks or other fragments. A practical example:

```nginx theme={null}
http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    gzip on;
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" "$http_user_agent"';
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Server blocks (virtual hosts) and additional configuration:
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

Notes:

* Use `include` to keep `nginx.conf` concise and load site-specific files from `conf.d` or `sites-enabled`.
* Configure gzip, caching, proxy, and upstreams in this section or in included files.

## server block (virtual host)

`server` blocks (virtual hosts) define how NGINX responds for specific domains, IPs, or ports. You can host multiple sites on one instance by adding multiple `server` blocks.

<Frame>
  <img alt="A slide titled &#x22;Creating and Editing Server Blocks (Virtual Hosts)&#x22; showing four colorful browser/window icons labeled &#x22;WWW&#x22; tied by lines into a single stack of servers below, illustrating multiple virtual hosts served from one server." />
</Frame>

NGINX chooses the matching `server` block using `listen` and `server_name` (or the IP) from the incoming request.

<Frame>
  <img alt="A presentation slide titled &#x22;Creating and Editing Server Blocks (Virtual Hosts)&#x22;. It shows a user icon sending a &#x22;Request&#x22; arrow to the NGINX logo, with labels like &#x22;server_name&#x22; and &#x22;IP address&#x22; beneath." />
</Frame>

Example `server` block:

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Directive summary:

| Directive       | Purpose                                                                |
| --------------- | ---------------------------------------------------------------------- |
| `listen`        | Port/address to monitor (e.g., `80` for HTTP, `443 ssl` for HTTPS).    |
| `server_name`   | Domain or hostnames this block should respond to.                      |
| `root`          | Filesystem path that serves site content.                              |
| `index`         | Default file(s) served for directory requests.                         |
| `location`      | Path-based matching blocks for request handling; `/` is the site root. |
| `try_files ...` | Try files or directories in order; fallback (e.g., `=404`) on miss.    |

Default webroots vary by distribution:

* Debian/Ubuntu: `/var/www/<site>/html`
* CentOS/Red Hat: `/usr/share/nginx/html`

## NGINX modules

NGINX functionality is provided by modules (core HTTP module, SSL, proxy, rewrite, gzip, etc.). Which directives you can use depends on the modules compiled into your NGINX binary. Use `nginx -V` to see compile-time modules and options.

<Frame>
  <img alt="A presentation slide titled &#x22;Nginx Modules&#x22; showing a screenshot of the ngx_http_core_module documentation with a long list of Nginx directive names and the NGINX logo. The slide also credits KodeKloud in the corner." />
</Frame>

## Common NGINX directories and files

Typical locations and purpose:

| Path                         | Purpose / Notes                                                                   |
| ---------------------------- | --------------------------------------------------------------------------------- |
| `/etc/nginx/nginx.conf`      | Main configuration file.                                                          |
| `/etc/nginx/sites-available` | Site config files (not active by default).                                        |
| `/etc/nginx/sites-enabled`   | Symlinks to `sites-available` to enable sites.                                    |
| `/etc/nginx/conf.d`          | Additional config snippets (often auto-generated or small fragments).             |
| `mime.types`                 | Maps extensions to MIME types.                                                    |
| `nginx.pid`                  | Master process PID file.                                                          |
| `/var/log/nginx/`            | Access and error logs.                                                            |
| Webroots                     | Typically under `/var/www/` (Debian/Ubuntu) or `/usr/share/nginx/` (CentOS/RHEL). |

Using symbolic links in `sites-enabled` is a common pattern to enable/disable sites (similar in intent to Apache’s approach, but usually managed manually or with helper scripts).

## Useful NGINX commands

Use the following commands when managing or troubleshooting NGINX:

| Command             | Purpose                                                                         |
| ------------------- | ------------------------------------------------------------------------------- |
| `nginx -h`          | Show NGINX command-line options.                                                |
| `nginx -v`          | Show NGINX version (brief).                                                     |
| `nginx -V`          | Show version plus configure/build options.                                      |
| `nginx -t`          | Test configuration for syntax errors and validity.                              |
| `nginx -T`          | Dump processed configuration to stdout and test it.                             |
| `nginx -s <signal>` | Send a signal to the master process (e.g., `stop`, `quit`, `reload`, `reopen`). |

Always validate configuration before reloading:

> **lightbulb** Run `nginx -t` (or `sudo nginx -t`) after edits to verify syntax and detect errors before reloading or restarting NGINX.

Example syntax check output:

```bash theme={null}
sudo nginx -t

nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Reload vs restart:

* `nginx -s reload` or `sudo systemctl reload nginx` — reloads config without dropping existing connections (preferred when possible).
* `sudo systemctl restart nginx` — fully restarts the service and interrupts active connections.

## Quick links and further reading

* NGINX official documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* NGINX Admin Guide: [https://nginx.org/en/docs/admin\_guide.html](https://nginx.org/en/docs/admin_guide.html)

That wraps up this concise overview of NGINX configuration structure and common operations.

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/7b0d11fb-1a0d-4765-a49d-8b9ec4d97b11)
