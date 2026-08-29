# Verify installation, enable at boot
sudo systemctl enable --now nginx
```

CentOS / RHEL / Fedora

```bash theme={null}
# On CentOS 7/8 or RHEL; use dnf on newer distributions:
sudo yum install -y nginx
# or
sudo dnf install -y nginx

# Start and enable at boot
sudo systemctl enable --now nginx
```

macOS (Homebrew)

```bash theme={null}
brew update
brew install nginx
# Start Nginx (Homebrew service)
brew services start nginx
```

Windows

* Recommended: use WSL and follow the Ubuntu instructions inside the WSL environment.
* Alternatively, use Chocolatey:

```powershell theme={null}
choco install nginx
```

***

## Manage the Nginx service

You will commonly use systemctl on modern Linux systems. Here are the essential commands:

| Action                          | systemd (`systemctl`)          |
| ------------------------------- | ------------------------------ |
| Check status                    | `sudo systemctl status nginx`  |
| Start                           | `sudo systemctl start nginx`   |
| Stop                            | `sudo systemctl stop nginx`    |
| Restart                         | `sudo systemctl restart nginx` |
| Reload configuration (graceful) | `sudo systemctl reload nginx`  |
| Enable at boot                  | `sudo systemctl enable nginx`  |

Older SysV init / compatibility:

```bash theme={null}
sudo service nginx start
sudo service nginx stop
sudo service nginx reload
```

<Callout icon="warning">
  Reloading (`reload`) applies configuration changes without terminating worker processes; use `restart` when you need a full restart. Always test config before reloading: `sudo nginx -t`.
</Callout>

***

## Understanding nginx.conf: structure and inheritance

Nginx configuration is hierarchical. The main contexts you should know:

* Main/global context (top-level): process-wide directives (user, worker\_processes, error\_log).
* `events` context: connection handling directives (e.g., `worker_connections`).
* `http` context: HTTP server configuration, MIME types, logging, upstreams, and general `server` directives.
* `server` blocks: Virtual hosts — listen addresses, `server_name`, SSL, access logging.
* `location` blocks (inside server): How requests are routed and handled for specific URIs.

Minimal example (illustrative):

```nginx theme={null}
user www-data;
worker_processes auto;
error_log /var/log/nginx/error.log warn;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile      on;
    keepalive_timeout 65;

    server {
        listen 80;
        server_name example.com www.example.com;

        root /var/www/example;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

Always validate changes before reloading:

```bash theme={null}
sudo nginx -t
sudo systemctl reload nginx
```

***

## Host a static website with Nginx

Typical steps to serve a simple static site:

1. Create the document root and a test page:

```bash theme={null}
sudo mkdir -p /var/www/example
echo "<h1>Hello from Nginx</h1>" | sudo tee /var/www/example/index.html
sudo chown -R www-data:www-data /var/www/example
```

2. Create a server block (virtual host). On Debian/Ubuntu, use `sites-available` and `sites-enabled`:

```nginx theme={null}
# /etc/nginx/sites-available/example
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

3. Enable the site and reload:

```bash theme={null}
sudo ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

If you use a different path or platform, adapt the file locations accordingly.

***

## Networking basics & firewall (UFW)

Nginx commonly uses these ports:

| Service | Port | Description                 |
| ------: | ---: | --------------------------- |
|    HTTP |   80 | Unencrypted web traffic     |
|   HTTPS |  443 | Encrypted web traffic (TLS) |

Allow HTTP/HTTPS through UFW on Ubuntu:

```bash theme={null}
# Allow pre-defined Nginx profiles
sudo ufw allow 'Nginx Full'   # allows ports 80 and 443
# Or allow only HTTP:
sudo ufw allow 80/tcp
# Enable/Status:
sudo ufw enable
sudo ufw status
```

You can also permit only HTTP or HTTPS as needed (`'Nginx HTTP'` or `'Nginx Full'`).

***

## Links and references

* Nginx documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* apt (Debian package manager): [https://wiki.debian.org/Apt](https://wiki.debian.org/Apt)
* yum (package manager overview): [https://en.wikipedia.org/wiki/YUM\_(package\_manager)](https://en.wikipedia.org/wiki/YUM_\(package_manager\))
* Homebrew (macOS package manager): [https://brew.sh](https://brew.sh)
* UFW (Uncomplicated Firewall): [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)

Use these resources for deeper configuration examples, SSL/TLS setup, reverse proxy patterns, and performance tuning.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/196d68ff-0e61-4b1b-a24b-3ef74ccf275c" />
</CardGroup>


# Install Config

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Install-Config/page

Guide to package managers and installing NGINX with common commands for apt, yum/dnf, Homebrew and Chocolatey.

Before we move on to installing NGINX, it's important to understand package managers. A package manager is an automation tool that handles installing, upgrading, configuring, and removing software on your system. It downloads packages, resolves and installs dependencies, and integrates software with your OS configuration. Using a package manager makes software installation predictable, repeatable, and secure compared to manual installs — which is why we use them to install NGINX.

<Frame>
  <img alt="A slide titled &#x22;Package Manager&#x22; showing three colorful boxes labeled &#x22;Downloading software,&#x22; &#x22;Sorting out dependencies,&#x22; and &#x22;Managing everything in the system,&#x22; each with an icon. An orange tools icon sits above the boxes inside a dashed rounded rectangle." />
</Frame>

How it works

* The package manager contacts one or more repositories (maintained by the OS vendor, third parties, or the open-source community) to fetch packages and metadata.
* When you request an install, the manager checks dependency metadata and installs any required packages automatically.
* It may run configuration or post-install scripts to integrate the software with system services.
* From fetching packages to resolving dependencies and running configuration tasks, the package manager automates the full software lifecycle.

Popular package managers (summary)

| Package Manager | Common OS / Distros  | Package Format | Example install command                                |
| --------------- | -------------------- | -------------- | ------------------------------------------------------ |
| APT             | Debian, Ubuntu       | `.deb`         | `sudo apt install nginx`                               |
| YUM / DNF       | RHEL, CentOS, Fedora | `.rpm`         | `sudo yum install nginx` (or `sudo dnf install nginx`) |
| Homebrew        | macOS, Linux (brew)  | Formulae       | `brew install nginx`                                   |
| Chocolatey      | Windows              | NuGet packages | `choco install nginx -y`                               |

First up: apt (Advanced Package Tool)

* Used on Debian-based systems (including Ubuntu).
* Works with `.deb` packages and maintains a package index for fast lookups.
* Common commands:
  * Update package index: `sudo apt update`
  * Install a package: `sudo apt install package_name`
  * Remove a package: `sudo apt remove package_name`
  * Upgrade installed packages: `sudo apt upgrade`
  * Search packages: `sudo apt-cache search package_name`

<Frame>
  <img alt="A presentation slide titled &#x22;Popular Package Managers&#x22; featuring &#x22;The Advanced Package Tool (APT)&#x22;. It notes APT is used for Debian-based systems (like Ubuntu) and works with .deb packages." />
</Frame>

Next: YUM (Yellowdog Updater, Modified) and DNF

* Common on Red Hat–based distributions (RHEL, CentOS, older Fedora). Newer Fedora and RHEL/CentOS versions use DNF (`dnf`) which is largely compatible with YUM commands.
* Works with RPM packages and resolves dependencies automatically.
* Common commands:
  * Update packages and metadata: `sudo yum update` (or `sudo dnf update`)
  * Install a package: `sudo yum install package_name` (or `sudo dnf install package_name`)
  * Remove a package: `sudo yum remove package_name`
  * Search for a package: `sudo yum search package_name`

<Frame>
  <img alt="A presentation slide titled &#x22;Popular Package Managers&#x22; showing a highlighted badge for &#x22;Yellowdog Updater Modified (YUM)&#x22;. A bullet notes it is used for Red Hat–based systems (like CentOS and Fedora)." />
</Frame>

Next: Homebrew (macOS and Linux)

* Popular on macOS and also available on Linux as `brew`.
* Installs into a user-writable prefix (for example `/usr/local` on Intel macs or `/opt/homebrew` on Apple Silicon), so most installs do not require `sudo`.
* Common commands:
  * Update Homebrew: `brew update`
  * Install a package: `brew install nginx`
  * Uninstall a package: `brew uninstall package_name`
  * Search packages: `brew search package_name`

<Frame>
  <img alt="A presentation slide titled &#x22;Popular Package Managers&#x22; highlighting Homebrew. It notes Homebrew is used for macOS and installs software into the home directory without requiring sudo privileges." />
</Frame>

On Windows: Chocolatey

* Command-line package manager for Windows that wraps installers and handles dependency scripts.
* Common commands:
  * Install a package: `choco install package_name`
  * Uninstall a package: `choco uninstall package_name`

<Callout icon="lightbulb">
  Note: `sudo apt update` refreshes the package index and does not accept `-y`. To automatically accept prompts on Debian/Ubuntu, use `-y` with `apt install` or `apt upgrade` (for example, `sudo apt install -y nginx`). Similarly, use the auto-confirm flags for other package managers when performing non-interactive installs (e.g., `-y` for `yum`, `dnf`, and `choco`).
</Callout>

Consolidated command examples

* Replace `package_name` with the package you want (for our purpose: `nginx`).

```bash theme={null}
