# Install: sudo apt install apache2-utils
htpasswd -c /etc/nginx/.htpasswd alice
# You will be prompted to enter a password
```

Nginx config snippet:

```nginx theme={null}
location /admin {
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://backend_admin;
}
```

Notes on authentication

* This is simple HTTP Basic Auth suitable for small, controlled areas or staging environments.
* For production, consider federated solutions (OAuth, OpenID Connect) or single sign-on (SSO) options for user management and stronger security.

Allow / deny directives (IP-based access control)
Use `allow` and `deny` in Nginx to restrict access by IP or network:

```nginx theme={null}
location /internal {
    allow 10.0.0.0/8;
    allow 192.168.1.0/24;
    deny all;
    proxy_pass http://internal_service;
}
```

* `allow` and `deny` are evaluated in order; when a client matches `allow`, access is granted. If no allow matches, the `deny all` will block the request.

Automated blocking with Fail2Ban
Fail2Ban can monitor logs (e.g., Nginx access/error logs) and automatically add firewall rules to block IPs that show malicious behavior (repeated login failures, scan attempts, etc.). Configuring and running Fail2Ban requires elevated privileges and persistent access to system logs.

<Callout icon="warning">
  Fail2Ban requires access to system logs and the ability to modify firewall rules. In restricted environments we will show configuration examples, but a full live demo may not be possible.
</Callout>

When to use Fail2Ban

* Protects SSH, login endpoints, and services exposed to the public internet.
* Works well as a complementary defense; it is not a substitute for secure application logic or proper authentication.

Recommended resources and next steps

* Generate and test local certs with `mkcert` and configure Nginx to serve HTTPS.
* Add security headers incrementally and verify site behavior in different browsers.
* Protect sensitive locations with `auth_basic` for quick access control.
* Use `allow`/`deny` for IP-based restrictions in trusted network segments.
* Consider deploying Fail2Ban on production servers with full log and firewall access.

Links and references

* [mkcert — local CA for development](https://github.com/FiloSottile/mkcert)
* [Let's Encrypt](https://letsencrypt.org/)
* [Certbot](https://certbot.eff.org/)
* [Fail2Ban](https://www.fail2ban.org/)
* [OAuth](https://oauth.net/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/f7f66739-dcb8-4386-976f-30308b76016c" />
</CardGroup>


# Summary

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Summary/page

Concise security and operational guide for serving web traffic, covering HTTPS, certificates, reverse proxy headers, authentication, access control, security headers, and automation best practices.

This lesson recaps the critical concepts from the module, emphasizing practical security and operational best practices for serving web traffic. Use this concise reference to remember the most important points about HTTPS, certificates, reverse proxy behavior, headers, authentication, and access control.

## HTTPS and redirects

* Always serve sites over HTTPS whenever possible. Modern browsers may block or warn users about insecure HTTP pages and many web platform features require HTTPS.
* Redirect plain `http://` traffic to `https://` at the proxy or web server level so users always receive the encrypted site.
* Use HSTS (HTTP Strict Transport Security) to tell browsers to always connect over HTTPS after the first secure visit.

Example NGINX redirect (place in the `server` block listening on port 80):

```nginx theme={null}
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}
```

<Callout icon="lightbulb">
  Always enforce HTTPS and configure an HSTS policy (for example: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`) only after you are confident all subdomains support HTTPS.
</Callout>

## SSL vs TLS and certificate sources

* TLS is the modern protocol that replaced the deprecated SSL family. People still say “SSL” colloquially, but TLS is the current, secure standard.
* For local development, use `mkcert` to create locally trusted certificates. It installs a local CA into your machine so your browser trusts development certs.
* For public-facing sites, obtain certificates from a trusted CA such as Let’s Encrypt (free) or commercial CAs like DigiCert and Comodo.

Table — certificate sources and typical uses:

| Source                            | Use case                         | Notes                                           |
| --------------------------------- | -------------------------------- | ----------------------------------------------- |
| `mkcert`                          | Local development                | Installs a local CA so browsers trust dev certs |
| `Let's Encrypt`                   | Public-facing, automated renewal | Free, widely used; supports ACME automation     |
| Commercial CAs (DigiCert, Comodo) | Enterprise / extended validation | Paid, may offer warranty and enterprise support |

## HTTP headers and reverse-proxy behavior

Understanding which headers a reverse proxy sets or forwards is critical. Misconfigured headers can cause incorrect application behavior or security gaps.

* Common proxy-forwarded headers:
  * `X-Forwarded-For` — original client IP
  * `X-Forwarded-Proto` — original protocol (`http` or `https`)
  * `Host` — requested host header
* Make sure your backend application trusts and correctly parses these headers (or use a trusted proxy with header rewriting features).

Table — important security and caching headers:

| Header                               | Purpose                             | Example / Notes                                                           |
| ------------------------------------ | ----------------------------------- | ------------------------------------------------------------------------- |
| `Strict-Transport-Security`          | Enforces HTTPS in browsers          | `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy`            | Mitigates XSS and content injection | Define allowed sources for scripts, styles, images                        |
| `X-Frame-Options`                    | Prevents clickjacking               | `DENY` or `SAMEORIGIN`                                                    |
| `Referrer-Policy`                    | Controls referral information       | `no-referrer-when-downgrade`, `strict-origin-when-cross-origin`           |
| `X-Content-Type-Options`             | Prevents MIME sniffing              | `nosniff`                                                                 |
| `Cache-Control` / `Expires` / `ETag` | Cache behavior and validation       | Tune for static assets vs. dynamic content                                |

## Authentication: `auth_basic` and robust alternatives

* NGINX `auth_basic` (HTTP Basic Auth) is simple to set up and useful for internal, staging, or temporary protection.
* For public-facing apps, prefer stronger, auditable authentication methods such as OAuth2, OpenID Connect, or SSO providers integrated with your app or identity provider.

<Callout icon="warning">
  Do not use HTTP Basic Auth for production user-facing authentication. It lacks modern features like session management, multifactor authentication, and robust auditing.
</Callout>

## Access control: `allow`/`deny` vs scalable protections

* NGINX `allow`/`deny` directives are convenient for small, static IP-based access lists (for example, allowing a management subnet).
* These rules do not scale well when you have many IPs or frequently changing lists.
* For larger deployments, use centralized, scalable solutions:
  * Network firewalls and ACLs
  * Web Application Firewalls (WAF)
  * Automated blocklists or dynamic tools like Fail2Ban to detect abuse and update firewall rules

Tip: Fail2Ban can monitor logs and dynamically block abusive IPs, reducing manual maintenance for straightforward abuse patterns.

## Operational recommendations

Combine layered controls for a secure, maintainable production environment:

* Enforce TLS and implement strong HSTS policies once ready.
* Set comprehensive security headers (`CSP`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`).
* Ensure the reverse proxy forwards the correct `X-Forwarded-*` headers and your backend validates them.
* Use automated tooling:
  * Let’s Encrypt (ACME) for certificate issuance and automated renewal
  * Fail2Ban, WAF, or cloud security services for blocking abuse
  * Infrastructure-as-code (Terraform, CloudFormation) for reproducible network and firewall rules

## Quick checklist

* [ ] Serve all production sites over HTTPS
* [ ] Redirect HTTP to HTTPS at the proxy/web server
* [ ] Use trusted certificates and automate renewals
* [ ] Configure HSTS after verifying all subdomains support HTTPS
* [ ] Harden with security headers and validate them in staging
* [ ] Prefer OAuth/OpenID Connect for public authentication
* [ ] Use scalable access controls for large or dynamic environments
* [ ] Automate detection and blocking of abusive traffic (Fail2Ban/WAF)

## Links and references

* [mkcert — GitHub](https://github.com/FiloSottile/mkcert)
* [Let's Encrypt](https://letsencrypt.org)
* [Fail2Ban](https://www.fail2ban.org)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/8905470e-b1ea-48ec-b0cd-711687ce7159/lesson/490c345b-92a0-427b-bfb2-93f1c8c5bf18" />
</CardGroup>
