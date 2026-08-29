# you should see something like:
# lrwxrwxrwx 1 root root 37 Feb  5 14:07 helloworld -> /etc/nginx/sites-available/helloworld
```

## 6. Test NGINX configuration and reload

Always test NGINX configuration syntax before reloading:

```bash theme={null}
nginx -t
```

Common error example:

```text theme={null}
nginx: [emerg] a duplicate default server for 0.0.0.0:80 in /etc/nginx/sites-enabled/helloworld:3
nginx: configuration file /etc/nginx/nginx.conf test failed
```

This indicates two server blocks are configured as the `default_server`. Fix the conflicting `listen` lines (remove `default_server` from one) or disable the default site, then re-run the test:

```bash theme={null}
nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Reload NGINX to apply the new configuration:

```bash theme={null}
nginx -s reload
```

(Alternatively: `systemctl reload nginx`.)

## 7. Test locally using the Host header

If you switched to root, return to your regular user for testing:

```bash theme={null}
exit
```

A plain `curl localhost` will still return the default "Welcome to nginx!" page because the request lacks a `Host` header matching `helloworld.com`:

```bash theme={null}
curl localhost
# returns the default "Welcome to nginx!" HTML
```

To test the `helloworld.com` site without DNS, send the `Host` header explicitly:

```bash theme={null}
curl --header "Host: helloworld.com" localhost
```

You should get the Hello World page:

```html theme={null}
<h1> Hello World! </h1>
```

If you pass a `Host` header that doesn't match any `server_name` in your enabled configs (for example `Host: someunknown`), NGINX will serve the first available server block (often the default). Proper `server_name` configuration and testing are important.

## Quick reference: useful paths and commands

| Item                  | Purpose                        | Example                                                                 |
| --------------------- | ------------------------------ | ----------------------------------------------------------------------- |
| NGINX config dir      | Main configuration files       | `/etc/nginx`                                                            |
| Available sites       | Site definitions (not enabled) | `/etc/nginx/sites-available/`                                           |
| Enabled sites         | Active site symlinks           | `/etc/nginx/sites-enabled/`                                             |
| Create site file      | Copy default stub              | `cp default helloworld`                                                 |
| Enable site           | Create symlink to enable       | `ln -s /etc/nginx/sites-available/helloworld /etc/nginx/sites-enabled/` |
| Test config           | Syntax check before reload     | `nginx -t`                                                              |
| Reload NGINX          | Apply configuration changes    | `nginx -s reload` or `systemctl reload nginx`                           |
| Test with Host header | Verify virtual host selection  | `curl --header "Host: helloworld.com" localhost`                        |

## Troubleshooting tips

* Duplicate default server error: remove `default_server` from one `listen` directive or disable the default site.
* 403 Forbidden: check filesystem permissions and ownership for `/var/www/helloworld` and the index file.
* Still seeing default page: ensure your `Host` header matches `server_name` or update `/etc/hosts`/DNS accordingly.

## 8. Next steps

* If you want this site reachable from other machines, open port 80 in your firewall. On Ubuntu, use `ufw`:

```bash theme={null}
sudo ufw allow http
```

* Use DNS or update `/etc/hosts` for a friendly hostname (e.g., `helloworld.com`) in your testing environment.
* For production, configure TLS (HTTPS) using a certificate from Let's Encrypt or another CA, and consider a reverse proxy or load balancer if needed.

Resources and further reading:

* NGINX official docs: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Ubuntu `ufw` guide: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)
* curl manual: [https://curl.se/docs/manpage.html](https://curl.se/docs/manpage.html)

That’s it — you now have a minimal NGINX-hosted site and know how to test virtual hosts locally using the `Host` header.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/205db332-da0d-4f3d-8273-225f9566c386" />
</CardGroup>


# Demo Nginx Install Config

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Demo-Nginx-Install-Config/page

Guide to installing, verifying, and inspecting Nginx on Ubuntu, covering apt commands, service management, configuration files, testing with curl, and log locations.

This lesson shows how to install, verify, and inspect Nginx on an Ubuntu-based system. Commands are shown for apt-based distributions; on CentOS/RHEL use `yum` or `dnf` instead. Paths like `/etc/nginx` and `/var/log/nginx` are common, but verify them for your specific OS.

<Callout icon="lightbulb">
  If you're on CentOS or Red Hat use `yum` or `dnf` instead of `apt`. The configuration directories (`/etc/nginx`, `/var/log/nginx`) are common across many Linux distributions but may vary—especially with custom packages or older releases.
</Callout>

## Quick command reference

| Task                 | Command                       | Description                                                  |
| -------------------- | ----------------------------- | ------------------------------------------------------------ |
| Update package index | `sudo apt update`             | Refresh package metadata before install/upgrade.             |
| Install Nginx        | `sudo apt install nginx`      | Install the nginx package (add `-y` to auto-accept prompts). |
| Check service status | `sudo systemctl status nginx` | View Nginx systemd status and process info.                  |
| Start service        | `sudo systemctl start nginx`  | Start Nginx immediately.                                     |
| Test configuration   | `sudo nginx -t`               | Validate Nginx configuration files.                          |
| Reload after changes | `sudo systemctl reload nginx` | Reload config without dropping connections.                  |
| Test HTTP response   | `curl http://localhost`       | Confirm Nginx serves HTTP requests locally.                  |
| View Nginx logs      | `ls -l /var/log/nginx`        | List Nginx log files.                                        |

Useful references:

* Nginx documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Ubuntu packages/apt: [https://help.ubuntu.com/community/AptGet/Howto](https://help.ubuntu.com/community/AptGet/Howto)

## 1. Update package lists

Refresh the package index to ensure you install the latest available Nginx package and dependencies:

```bash theme={null}
sudo apt update
```

Tip: `apt update` only refreshes the package index. If you want to upgrade installed packages non-interactively, run `sudo apt -y upgrade`.

Example output when updating package lists:

```bash theme={null}
bob@alpine-host ~ ➜ sudo apt update
Get:1 http://security.ubuntu.com/ubuntu focal-security InRelease [128 kB]
Get:2 http://security.ubuntu.com/ubuntu focal-security/main amd64 Packages [4,219 kB]
Get:3 http://archive.ubuntu.com/ubuntu focal InRelease [265 kB]
Get:4 http://security.ubuntu.com/ubuntu focal-security/restricted amd64 Packages [4,329 kB]
Get:5 http://security.ubuntu.com/ubuntu focal-security/universe amd64 Packages [1,298 kB]
Get:6 http://security.ubuntu.com/ubuntu focal-security/multiverse amd64 Packages [30.9 kB]
Get:7 http://archive.ubuntu.com/ubuntu focal-updates InRelease [128 kB]
Get:8 http://archive.ubuntu.com/ubuntu focal-backports InRelease [128 kB]
Get:9 http://archive.ubuntu.com/ubuntu focal/restricted amd64 Packages [33.4 kB]
Get:10 http://archive.ubuntu.com/ubuntu focal/universe amd64 Packages [11.3 MB]
Get:11 http://archive.ubuntu.com/ubuntu focal/main amd64 Packages [1,275 kB]
Get:12 http://archive.ubuntu.com/ubuntu focal/multiverse amd64 Packages [177 kB]
Get:13 http://archive.ubuntu.com/ubuntu focal-updates/restricted amd64 Packages [4,517 kB]
Get:14 http://archive.ubuntu.com/ubuntu focal-updates/multiverse amd64 Packages [34.6 kB]
Get:15 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages [4,695 kB]
Get:16 http://archive.ubuntu.com/ubuntu focal-updates/universe amd64 Packages [1,589 kB]
Get:17 http://archive.ubuntu.com/ubuntu focal-backports/universe amd64 Packages [28.6 kB]
Get:18 http://archive.ubuntu.com/ubuntu focal-backports/main amd64 Packages [55.2 kB]
Fetched 34.3 MB in 3s (10.7 MB/s)
Reading package lists... Done
Building dependency tree
Reading state information... Done
47 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

## 2. Install Nginx

Install Nginx using apt. Running interactively will prompt for confirmation; include `-y` to skip prompts:

```bash theme={null}
sudo apt install nginx
```

Typical install output (shows dependencies and disk usage before confirmation):

```bash theme={null}
bob@alpine-host ~ ➜ sudo apt install nginx
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  libnginx-mod-http-image-filter libnginx-mod-http-xslt-filter libnginx-mod-mail libnginx-mod-stream nginx-common nginx-core
Suggested packages:
  fcgiwrap nginx-doc ssl-cert
The following NEW packages will be installed:
  libnginx-mod-http-image-filter libnginx-mod-http-xslt-filter libnginx-mod-mail libnginx-mod-stream nginx nginx-common nginx-core
0 upgraded, 7 newly installed, 0 to remove and 47 not upgraded.
Need to get 604 kB of archives.
After this operation, 2,141 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
```

It is normal to see several modules and helper packages installed along with `nginx`.

## 3. Verify and start the Nginx service

Check the service status through systemd to see whether Nginx is running, enabled, or stopped:

```bash theme={null}
sudo systemctl status nginx
```

If Nginx was just installed but not started, you might see:

```bash theme={null}
bob@alpine-host ~ › sudo systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
    Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
    Active: inactive (dead)
    Docs: man:nginx(8)
```

Start Nginx:

```bash theme={null}
sudo systemctl start nginx
```

Then confirm it is active (running):

```bash theme={null}
sudo systemctl status nginx
```

Example of an active status:

```bash theme={null}
bob@alpine-host ~ ➜ sudo systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2025-02-05 11:59:11 EST; 5s ago
   Docs: man:nginx(8)
  Process: 6598 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
  Process: 6599 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
 Main PID: 6600 (nginx)
    Tasks: 17 (limit: 154503)
    Memory: 14.4M
    CGroup: /system.slice/nginx.service
    ├─6600 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
    ├─6601 nginx: worker process
    ├─6602 nginx: worker process
    ├─6603 nginx: worker process
    └─... (worker processes continue)
```

The key line is `Active: active (running)` — this confirms Nginx is serving.

## 4. Test with curl

Confirm Nginx responds on the local host by requesting the default page:

```bash theme={null}
curl http://localhost
```

You should see the default "Welcome to nginx!" HTML page when Nginx is serving content correctly.

## 5. Inspect the Nginx configuration directory

Nginx’s configuration is usually kept under `/etc/nginx`. List and inspect the directory to understand its structure:

```bash theme={null}
cd /etc/nginx
ll
```

Example output showing typical files and directories:

```bash theme={null}
bob@alpine-host /etc/nginx🔒 ➜ ll
total 76
drwxr-xr-x 8 root root 4096 Feb 5 11:58 ./
drwxr-xr-x 1 root root 4096 Feb 5 11:58 ../
drwxr-xr-x 2 root root 4096 Sep 10 09:52 conf.d/
-rw-r--r-- 1 root root 1077 Mar 20 2024 fastcgi.conf
-rw-r--r-- 1 root root 1007 Mar 20 2024 fastcgi_params
-rw-r--r-- 1 root root 2837 Mar 20 2024 koi-utf
-rw-r--r-- 1 root root 2223 Mar 20 2024 koi-win
-rw-r--r-- 1 root root 3957 Mar 20 2024 mime.types
drwxr-xr-x 2 root root 4096 Sep 10 09:52 modules-available/
drwxr-xr-x 2 root root 4096 Feb 5 11:58 modules-enabled/
-rw-r--r-- 1 root root 1490 Mar 20 2024 nginx.conf
-rw-r--r-- 1 root root 180 Mar 20 2024 proxy_params
-rw-r--r-- 1 root root 636 Mar 20 2024 scgi_params
drwxr-xr-x 2 root root 4096 Feb 5 11:58 sites-available/
drwxr-xr-x 2 root root 4096 Feb 5 11:58 sites-enabled/
drwxr-xr-x 2 root root 4096 Feb 5 11:58 snippets/
-rw-r--r-- 1 root root 664 Mar 20 2024 uwsgi_params
-rw-r--r-- 1 root root 3071 Mar 20 2024 win-utf
```

The primary global configuration file is `nginx.conf`. It sets global directives (worker processes, logging, gzip, etc.) and includes other configuration files via `include` statements.

Relevant excerpts from a typical `/etc/nginx/nginx.conf`:

```nginx theme={null}
