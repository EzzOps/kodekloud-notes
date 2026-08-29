# Check current status (likely inactive in a fresh lab)
bob@alpine-host ~ ➜  sudo ufw status
Status: inactive

# Allow SSH first to avoid being locked out (recommended)
bob@alpine-host ~ ➜  sudo ufw allow OpenSSH
Rule added
Rule added (v6)

# Enable UFW (turns on the firewall and enables it at startup)
bob@alpine-host ~ ➜  sudo ufw enable
Firewall is active and enabled on system startup

# Allow HTTP (port 80) and HTTPS (port 443)
bob@alpine-host ~ ➜  sudo ufw allow 80/tcp
Rule added
Rule added (v6)

bob@alpine-host ~ ➜  sudo ufw allow 443/tcp
Rule added
Rule added (v6)

# (Optional) Allow the Flask app port if you need direct external access (not recommended)
bob@alpine-host ~ ➜  sudo ufw allow 5000/tcp
Rule added
Rule added (v6)

# View current active rules
bob@alpine-host ~ ➜  sudo ufw status
Status: active

To                         Action      From
--                         ------      -----
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
5000/tcp                   ALLOW       Anywhere
22/tcp                     ALLOW       Anywhere
80/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)
5000/tcp (v6)              ALLOW       Anywhere (v6)
22/tcp (v6)                ALLOW       Anywhere (v6)
```

## Port summary and recommended exposure

| Service                 | Port   | Typical use / recommendation                                                                              |
| ----------------------- | ------ | --------------------------------------------------------------------------------------------------------- |
| NGINX (HTTP)            | `80`   | Publicly expose for HTTP traffic; use only if you intentionally serve unencrypted content.                |
| NGINX (HTTPS)           | `443`  | Publicly expose for secure web traffic. Use a TLS certificate for production.                             |
| Flask app (development) | `5000` | Development port. Avoid exposing directly to the Internet. Instead, route via NGINX on `80`/`443`.        |
| SSH                     | `22`   | Required for remote administration. Always allow before enabling the firewall. (`sudo ufw allow OpenSSH`) |

## Best practices and notes

* UFW adds both IPv4 and IPv6 rules. You will typically see `Rule added (v6)` in the command output. If your environment supports IPv6 (mobile networks frequently do), those rules are relevant.
* Always permit SSH (`22/tcp` or `OpenSSH`) before enabling UFW to prevent locking yourself out.
* For public-facing services, prefer exposing only `80` and `443`. Avoid opening non-standard ports (like `5000`) to reduce your attack surface and avoid confusion for end users who normally do not append ports to URLs.
* To expose internal apps on standard web ports, use NGINX as a reverse proxy (or a load balancer) to accept traffic on `80`/`443` and forward requests internally to your application on `5000`. Reverse proxying and load balancing deserve their own dedicated guides.

Resources:

* UFW documentation: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)
* NGINX documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)

Summary: enable UFW, allow only the ports you need (and always allow SSH before enabling), and use NGINX as a reverse proxy to present backend applications on standard web ports (`80`/`443`) instead of opening many arbitrary ports.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/794628cb-4836-49d0-828f-6248c05f4b83" />
</CardGroup>


# Demo First Website with Nginx

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Demo-First-Website-with-Nginx/page

Guide to creating and serving a minimal Hello World website with NGINX, including configuration, document root, enabling site, testing with Host header, and troubleshooting.

This lesson walks through creating a minimal "Hello World" website served by NGINX on a single host. Follow these steps in order:

* Verify NGINX is running.
* Create a simple server block in `sites-available`.
* Create the document root and `index.html`.
* Enable the site and test it locally using the `Host` header.

## 1. Verify NGINX is running

Check the service status and start it if necessary:

```bash theme={null}
sudo systemctl status nginx
sudo systemctl start nginx
```

Confirm the default page is served:

```bash theme={null}
curl localhost
```

Example returned HTML (truncated):

```html theme={null}
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</html>
```

This verifies that NGINX is installed and serving the default page.

## 2. Become root and inspect NGINX configuration directories

To avoid prefixing `sudo` for each command, switch to root for the remainder of the setup (optional but convenient):

```bash theme={null}
sudo su
cd /etc/nginx
ll
```

You should see `sites-available/` and `sites-enabled/` among the configuration files. Then change into `sites-available`:

```bash theme={null}
cd /etc/nginx/sites-available
ll
```

Typically you'll see a `default` file here.

## 3. Create a new site configuration

Copy the default site config to a new file named `helloworld`:

```bash theme={null}
cp default helloworld
```

Edit `helloworld` and simplify it to the essentials: `listen`, `root`, `index`, and `server_name`. Remove commented examples to keep the file focused.

Example minimal `helloworld` server block:

```nginx theme={null}
server {
    listen 80;

    root /var/www/helloworld;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    server_name helloworld.com;

    location / {
        # First attempt to serve request as file, then as directory,
        # then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }
}
```

Notes:

* Do not use `listen 80 default_server;` in more than one server block — this causes a duplicate default server error.
* Set `server_name` to the hostname you intend to serve (we'll test this with a Host header).

<Callout icon="lightbulb">
  Set `server_name` to the hostname you intend to serve (for example, `helloworld.com`). NGINX uses the `Host` header to select the matching server block; if no match is found, NGINX serves the first matching server block (often the default).
</Callout>

## 4. Create the document root and index page

Create the document root that matches the `root` directive and add a basic `index.html`:

```bash theme={null}
mkdir -p /var/www/helloworld
cd /var/www/helloworld
```

Create the index file:

```html theme={null}
<!-- /var/www/helloworld/index.html -->
<h1> Hello World! </h1>
```

Ensure the file is named `index.html` because the server block uses `index index.html` in its `index` list.

## 5. Enable the site (sites-available → sites-enabled)

Enable the site by creating a symbolic link from `sites-available` to `sites-enabled`:

```bash theme={null}
ln -s /etc/nginx/sites-available/helloworld /etc/nginx/sites-enabled/
```

Verify the symlink exists:

```bash theme={null}
ll /etc/nginx/sites-enabled/
