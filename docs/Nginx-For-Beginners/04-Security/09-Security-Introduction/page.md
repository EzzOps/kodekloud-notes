# Obtain a certificate using the standalone plugin for devops.org and www.devops.org
sudo certbot certonly --standalone --preferred-challenges http -d devops.org -d www.devops.org
```

Note: package names, installation commands, and recommended Certbot plugins (e.g., `certbot-nginx`) vary by distribution. Check the Certbot documentation for platform-specific instructions: [https://certbot.eff.org](https://certbot.eff.org)

Local development / testing: mkcert

* mkcert makes short-lived, locally trusted certificates for development and testing by installing a local CA in your machine’s trust store.
* These certificates are only appropriate for local testing and should never be used for public production sites.

> **lightbulb** mkcert installs a local CA in your OS/browser trust store so the generated certs are trusted on your development machine. It is very convenient for local HTTPS but is not a replacement for CA‑signed certificates like those from Let’s Encrypt in production.

Example mkcert workflow (local testing)

* Install mkcert (platform-specific) and run `mkcert --install` once to register the local CA.
* Generate certificates for one or more hostnames. Note: X.509 wildcards only match a single subdomain level (e.g., `*.example.com` matches `a.example.com` but not `a.b.example.com`).

```bash theme={null}
sudo apt install mkcert
cd /etc/ssl/private
mkcert --install
mkcert '*.example.com'
```

Sample mkcert output (representative):

```text theme={null}
Created a new certificate valid for the following names 📜
 - "*.example.com"

Reminder: X.509 wildcards only go one level deep, so this won't match a.b.example.com ℹ️

The certificate is at "./_wildcard.example.com.pem" and the key at "./_wildcard.example.com-key.pem"
```

Place the generated certificate and key into secure locations (for example, certificate into `/etc/ssl/certs/` and private key into `/etc/ssl/private/`) and reference those paths from your web server configuration.

> **warning** Do not use mkcert-generated certificates in production. For public-facing services, always use CA-signed certificates (e.g., from Let’s Encrypt or a commercial CA).

Using the certificate in an Nginx server block

* After obtaining the certificate and private key, reference them in your Nginx configuration and listen on port 443 for TLS traffic.
* Example Nginx server block — adjust `server_name` and file paths to match your environment:

```nginx theme={null}
server {
    listen 443 ssl;
    server_name honda.cars.com;

    ssl_certificate /etc/ssl/certs/honda.cars.com.pem;
    ssl_certificate_key /etc/ssl/private/honda.cars.com-key.pem;

    root /var/www/honda.cars.com/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

After configuring Nginx, test and reload:

```bash theme={null}
sudo nginx -t
sudo systemctl reload nginx
```

Quick reference table — certificate options

| Certificate Type                  | Use Case                       | Notes                                            |
| --------------------------------- | ------------------------------ | ------------------------------------------------ |
| Let’s Encrypt                     | Production, automated          | Free, widely trusted; use Certbot for automation |
| Commercial CA (DigiCert, Sectigo) | Enterprise/extended validation | Paid options, extended features and support      |
| mkcert                            | Local development              | Installs local CA; never use in production       |

Summary

* HTTPS/TLS protects confidentiality and integrity of web traffic; it’s essential for any site handling sensitive data.
* TLS certificates are issued and validated by Certificate Authorities. Let’s Encrypt provides free, trusted certificates and Certbot is a commonly used client for obtaining and renewing them.
* Use mkcert only for local development and testing; do not use mkcert certs in production.
* After obtaining certificates, configure your web server (example shown with Nginx) to serve HTTPS on port 443, and verify with `nginx -t` and browser or SSL tools.

<Frame>
  <img alt="A presentation slide showing the Let's Encrypt logo with the heading &#x22;Several reputable Certificate Authorities include:&#x22; and a note that it &#x22;Offers free TLS certificates.&#x22;" />
</Frame>

Links and references

* Certbot: [https://certbot.eff.org](https://certbot.eff.org)
* Let’s Encrypt: [https://letsencrypt.org](https://letsencrypt.org)
* mkcert GitHub: [https://github.com/FiloSottile/mkcert](https://github.com/FiloSottile/mkcert)
* Nginx documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)

Now that you understand the concepts and commands, practice obtaining a certificate (e.g., with Certbot) and configuring Nginx to serve HTTPS for your site.

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/a4af90be-9d47-4d0b-a285-bec7a50ef02a)


# Security Introduction

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Security-Introduction/page

Practical guide to securing local web development using HTTPS, TLS, Nginx headers, authentication, and access controls.

In this lesson we'll cover essential web security concepts and practical Nginx configurations you can apply in hands-on exercises. The goal is to give you a pragmatic toolkit for securing local development and preparing you for production deployment patterns.

Summary of what you'll learn

* Why HTTPS matters and why plain HTTP is insecure
* How TLS (formerly SSL) protects data in transit
* Key HTTP security headers and how to add them in Nginx
* How to protect site areas with Nginx basic authentication
* How to allow/block traffic with `allow`/`deny` and an introduction to Fail2Ban

Why HTTPS matters

* HTTPS encrypts traffic between client and server, preventing eavesdropping and tampering.
* Modern browsers mark plain HTTP sites as insecure and will limit functionality (e.g., geolocation, service workers).
* TLS also enables server identity via certificates, which helps prevent man-in-the-middle attacks.

For demos and local hands-on exercises in this material we use `mkcert` to generate locally trusted TLS certificates: [mkcert](https://github.com/FiloSottile/mkcert). In production you would normally use a public CA such as [Let's Encrypt](https://letsencrypt.org/) with an automation tool like [Certbot](https://certbot.eff.org/). That approach requires control of a public domain and DNS — something most learners don't have for local exercises.

> **lightbulb** For local development and hands-on exercises, `mkcert` provides a convenient way to create certificates trusted by your machine. For production deployments, use a public CA like [Let's Encrypt](https://letsencrypt.org/) with [Certbot](https://certbot.eff.org/).

Quick mkcert usage (local)

* Install `mkcert` following the project README.
* Create a local CA and generate a certificate for `localhost`:

```bash theme={null}
mkcert -install
mkcert localhost 127.0.0.1 ::1
```

* The generated `localhost+2.pem` and `localhost+2-key.pem` (filenames may vary) can be referenced in your Nginx `ssl_certificate` and `ssl_certificate_key` directives for local testing.

<Frame>
  <img alt="A presentation slide titled &#x22;Objectives&#x22; with a teal gradient sidebar and three numbered items about web security: why HTTPS matters, how SSL/TLS secures data, and HTTP headers and their uses. Each objective has a colorful numbered tag (01–03) along the right edge of the sidebar." />
</Frame>

TLS fundamentals (brief)

* TLS provides:
  * Confidentiality: traffic is encrypted.
  * Integrity: tampering is detected.
  * Authentication: server identity via certificates (optionally client certs).
* Browsers verify the certificate chain, validity period, and hostname match.

HTTP security headers — what matters most
We won't cover every available header, but these are the most effective and commonly used headers to improve security posture. Add them at the `server` or `location` level in Nginx as appropriate.

| Header                             | Purpose                                             | Example Nginx directive                                                                               |
| ---------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `Strict-Transport-Security` (HSTS) | Instructs browsers to only use HTTPS for a domain   | `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;`         |
| `X-Frame-Options`                  | Prevents clickjacking by disallowing framing        | `add_header X-Frame-Options "DENY" always;`                                                           |
| `X-Content-Type-Options`           | Stops MIME sniffing                                 | `add_header X-Content-Type-Options "nosniff" always;`                                                 |
| `Referrer-Policy`                  | Controls information in the `Referer` header        | `add_header Referrer-Policy "no-referrer-when-downgrade" always;`                                     |
| `Content-Security-Policy` (CSP)    | Restricts sources for scripts, styles, images, etc. | `add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline';" always;` |
| `Permissions-Policy`               | Limits browser features (formerly Feature-Policy)   | `add_header Permissions-Policy "geolocation=(), microphone=()" always;`                               |
| `Expect-CT`                        | Certificate Transparency enforcement (optional)     | `add_header Expect-CT "max-age=86400, enforce" always;`                                               |

Nginx example: adding headers
Place these inside your `server` block (or specific `location`) to apply them. Use `always` so headers are sent even on error responses.

```nginx theme={null}
server {
    listen 443 ssl;
    server_name example.local;

    ssl_certificate     /etc/ssl/certs/localhost+2.pem;
    ssl_certificate_key /etc/ssl/private/localhost+2-key.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline';" always;
    add_header Permissions-Policy "geolocation=(), microphone=()" always;

    location / {
        proxy_pass http://backend;
    }
}
```

Important CSP note

* Content-Security-Policy is powerful but can break site functionality if it is too restrictive. Start with a permissive policy and tighten gradually while testing.

Nginx basic authentication (protecting paths)
Use `htpasswd` from Apache's `httpd-tools` or `apache2-utils` to create password files, then protect Nginx locations with `auth_basic`.

Create an htpasswd file:

```bash theme={null}
