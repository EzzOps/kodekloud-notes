# Summary

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Summary/page

NGINX installation and configuration guide covering package installation, service control, nginx.conf structure, serving static files and reverse proxy setup, default page customization, and firewall best practices.

Thanks for following along — that wraps up this lesson. Below is a focused recap of the key NGINX topics we covered, organized for quick reference and practical use.

* Why use package managers instead of compiling NGINX from source
  * Prefer your distribution’s package manager (apt, yum/dnf, pacman) for routine installs and upgrades. Compiling from source is only recommended when you need custom modules or non-standard builds (for example, third-party NGINX modules not available as packages).
  * Keywords: NGINX installation, package manager, compile NGINX from source.

* Installing NGINX across distributions
  * Examples used Ubuntu, but the same concepts apply on other Linux distributions. For Ubuntu/Debian:
    ```bash theme={null}
    sudo apt update
    sudo apt install nginx
    ```
  * For RHEL/CentOS/Fedora, use `yum`/`dnf`; for Arch, use `pacman`.
  * Keywords: install NGINX Ubuntu, install NGINX Debian, install NGINX CentOS.

* Platform guidance
  * While you can test NGINX on Windows or macOS for learning, Linux is the recommended platform for production NGINX servers.

<Callout icon="warning">
  Avoid running production NGINX on Windows or macOS—Linux is the standard and most supported platform for production NGINX deployments.
</Callout>

* Controlling the NGINX process
  * Use your service manager for lifecycle operations:
    ```bash theme={null}
    sudo systemctl start nginx
    sudo systemctl stop nginx
    sudo systemctl restart nginx
    sudo systemctl reload nginx
    ```
  * Send signals directly to the master process:
    ```bash theme={null}
    sudo nginx -s reload   # reload configuration gracefully
    sudo nginx -s quit     # graceful shutdown
    sudo nginx -s stop     # immediate stop
    sudo nginx -s reopen   # reopen log files
    ```
  * Keywords: systemctl nginx, nginx -s reload, graceful reload NGINX.

* NGINX configuration structure
  * The primary config file is `nginx.conf`. Its main parts are the global directives, the `events` block, the `http` block, and inside `http` multiple `server` blocks for virtual hosting.
  * You can host multiple sites on one NGINX instance using separate `server` blocks. Always set `server_name` for each site; if no `server_name` matches, NGINX uses the default server for that listen address (the first matching server block, or the one marked `default_server`).

<Callout icon="lightbulb">
  Tip: Use `default_server` on the `listen` directive to explicitly choose the server block that should handle unmatched requests.
</Callout>

* Quick reference: `nginx.conf` blocks

| Block      | Purpose                          | Common directives / examples                |
| ---------- | -------------------------------- | ------------------------------------------- |
| Global     | Settings applied before blocks   | `user`, `worker_processes`, `error_log`     |
| `events`   | Worker connection settings       | `worker_connections`                        |
| `http`     | HTTP server-wide settings        | `include`, `log_format`, `sendfile`, `gzip` |
| `server`   | Virtual host configuration       | `listen`, `server_name`, `root`, `location` |
| `location` | Request handling inside a server | `proxy_pass`, `try_files`, `alias`          |

* Serving static files and reverse proxy usage
  * NGINX excels at serving static assets (HTML, CSS, JS, images) and is often used as a reverse proxy in front of application servers (Node, Python, Ruby, etc.).
  * Example minimal server block for a static site:
    ```nginx theme={null}
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
  * Keywords: NGINX static files, NGINX reverse proxy, NGINX server block example.

* Customizing the default page and adding a simple “Hello World”
  * Replace the default root document (commonly `/var/www/html/index.html`) with your own static HTML to change the default NGINX page. A basic file like `index.html` with “Hello World” is enough for testing.

* Firewalls and port management
  * Always run a host firewall (e.g., `ufw`, `firewalld`) and a cloud provider security policy. Only open the ports and IPs you intend to expose.
  * Common public ports:
    * 80 — HTTP
    * 443 — HTTPS
  * For private testing, restrict access to specific IP addresses.
  * Cloud provider firewall references:
    * [GCP Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)
    * [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
    * [Azure Network Security](https://learn.microsoft.com/azure/virtual-network/security-overview)

<Frame>
  <img alt="A presentation summary slide with a turquoise left panel and the title &#x22;Summary.&#x22;Three numbered points list Nginx topics: serving static sites and hosting multiple sites with server blocks, customizing Nginx's default page, and the importance of firewall and ports management." />
</Frame>

Thanks again for participating in this module. You’ve earned a break—grab a cup of coffee.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/48af9384-cad6-4cbf-a8c4-10299f8f241e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/4a9d775f-003d-4a42-8cc3-661b8dbde1eb" />
</CardGroup>
