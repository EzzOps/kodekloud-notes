# Create or overwrite .htpasswd with the username and trailing colon
sudo sh -c "echo -n 'admin:' > /etc/nginx/conf.d/.htpasswd"

# Append an APR1 (Apache MD5) encrypted password (you will be prompted for the password)
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/conf.d/.htpasswd"
```

When prompted enter the desired password (demo uses `password123`). The `.htpasswd` file will contain a single line similar to:

```text theme={null}
admin:$apr1$MASb7ZA.$b8LOCauVuqug5nH2AIk72/
```

Verify the file content:

```bash theme={null}
sudo cat /etc/nginx/conf.d/.htpasswd
# Example output:
# admin:$apr1$MASb7ZA.$b8LOCauVuqug5nH2AIk72/
```

> **warning** Ensure the `.htpasswd` file is readable by the NGINX worker process (adjust ownership or permissions as needed). For example:

  ```bash theme={null}
  sudo chown root:nginx /etc/nginx/conf.d/.htpasswd
  sudo chmod 640 /etc/nginx/conf.d/.htpasswd
  ```

  Avoid world-writable/readable permissions on sensitive files.

## Test and reload NGINX

Validate the configuration and reload NGINX so changes take effect:

```bash theme={null}
sudo nginx -t
sudo nginx -s reload
# Or, on systems using systemd:
# sudo systemctl reload nginx
```

Now visit the protected endpoint. Refresh `https://www.example.com/admin` — the browser should prompt for credentials:

<Frame>
  <img alt="A browser screenshot showing a sign-in dialog box with username and password fields and &#x22;Cancel&#x22; and &#x22;Sign In&#x22; buttons near the top center. The address bar displays a kodekloud.dev URL." />
</Frame>

Enter the username (`admin`) and the password you created (e.g., `password123`). After successful authentication you gain access to `/admin`. The public `/` endpoint remains accessible without credentials.

## Protecting the entire site

If you prefer to require authentication for the entire site, move the `auth_basic` and `auth_basic_user_file` directives into the `location /` block or the server block (scope depends on your needs). Example replacing the earlier `location /`:

```nginx theme={null}
location / {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
    try_files $uri $uri/ =404;
}
```

After editing, run `nginx -t` and reload NGINX. Note: browsers may cache credentials; use a private/incognito window or clear credentials if you do not see the login prompt immediately.

> **lightbulb** Basic authentication with `.htpasswd` is simple and useful for internal or small-scale protection, but it does not scale well for large production deployments. Credentials are sent with every request and managing many users via `.htpasswd` becomes cumbersome. For production consider more robust solutions like [OAuth](https://oauth.net/), [OpenID Connect](https://openid.net/connect/), or integrating with an identity provider or SSO.

## Alternatives and integrations

If you use NGINX Plus (commercial) or additional modules, you can integrate NGINX with external identity providers. Examples include the NGINX JavaScript module (njs), OpenID Connect integrations, or vendor-specific modules.

Example: install and enable the njs module (package names vary by distribution):

```bash theme={null}
# Example installation commands (package names differ between distros)
sudo apt install nginx-plus-module-njs
# OR
sudo yum install nginx-plus-module-njs

# And then load the module in nginx.conf
load_module modules/ngx_http_js_module.so;
```

Use the appropriate module and configuration for your chosen identity provider or auth flow.

## Summary

This lesson showed how to:

* Protect a single NGINX location (`/admin`) using Basic Auth with `auth_basic` and a `.htpasswd` file.
* Create APR1-encrypted credentials using `openssl passwd -apr1`.
* Extend protection to the entire site.
* Consider alternatives for production deployments (OAuth, OpenID Connect, NGINX modules).

Links and references

* NGINX auth\_basic documentation: [https://nginx.org/en/docs/http/ngx\_http\_auth\_basic\_module.html](https://nginx.org/en/docs/http/ngx_http_auth_basic_module.html)
* `openssl passwd` manual: [https://www.openssl.org/docs/man1.1.1/man1/openssl-passwd.html](https://www.openssl.org/docs/man1.1.1/man1/openssl-passwd.html)
* NGINX documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* NGINX Plus: [https://www.nginx.com/products/nginx-plus/](https://www.nginx.com/products/nginx-plus/)

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/3264362e-1f24-419d-9a96-d225e7708fd1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/3898f285-8614-4509-86f8-16bc73f921ea)


# Demo Blocking Traffic

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Demo-Blocking-Traffic/page

Configuring Nginx to allow or deny IPs and using fail2ban to automatically ban repeated failed HTTP Basic auth attempts

In this lesson you'll learn how to block and allow traffic for an example site (`example.com`) using Nginx `allow` / `deny` directives, and how to use [fail2ban](https://www.fail2ban.org/) to automatically ban IPs that repeatedly fail authentication. The site exposes a protected `/admin` endpoint that uses HTTP Basic authentication; you can restrict access by IP in Nginx and automatically ban attackers with fail2ban.

Key goals:

* Use Nginx `allow` and `deny` to permit or block specific IP addresses or CIDR ranges.
* Use [fail2ban](https://www.fail2ban.org/) to automatically block IPs that repeatedly submit bad credentials, avoiding large, manually maintained deny lists.

***

## Base Nginx configuration (HTTP -> HTTPS, TLS, headers, protected /admin)

Start with this base Nginx site configuration for `example.com`. It redirects HTTP to HTTPS, configures TLS, sets security headers, serves files from a document root, and protects `/admin` with HTTP Basic auth:

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

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
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

This configuration is the baseline used for the rest of the examples below.

***

## Verify DNS/name resolution and test connectivity

On your client nodes (for example `node01` and `node02`) ensure `example.com` resolves to your Nginx server by editing `/etc/hosts`:

```text theme={null}
127.0.0.1        localhost
::1              localhost ip6-localhost ip6-loopback
192.231.128.3    node02
192.231.128.10   example.com
```

Check connectivity with curl. Because the TLS certificate was issued with a local CA (e.g., [mkcert](https://mkcert.dev)), curl will not trust it by default.

Example checks:

```bash theme={null}
