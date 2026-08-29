# Basic Authentication

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/Basic-Authentication/page

Guide to setting up HTTP Basic Authentication with NGINX including creating htpasswd credentials, configuring auth_basic for protected locations, and security best practices

NGINX can enforce HTTP Basic Authentication to protect an entire site or specific paths. This guide explains when to use NGINX basic auth, how to create the credentials file, and how to configure NGINX to require authentication for a `location` (for example, `/admin`).

<Frame>
  <img alt="A slide titled &#x22;Password Protected&#x22; featuring a stylized web browser window and a shield icon with a padlock, indicating secure or password-protected access. The illustration includes a small desk scene with a potted plant and two caption boxes referencing authorization libraries and Nginx." />
</Frame>

Why use NGINX basic auth?

* Fast to set up for internal, staging, or admin-only pages.
* Works at the webserver layer — no application code changes required.
* Uses standard browser username/password prompt (no UI customization).

Use cases

| Resource                   | Typical use                                    | Notes                                   |
| -------------------------- | ---------------------------------------------- | --------------------------------------- |
| Admin panel                | Protect `https://example.com/admin`            | Quick protection for internal admin UIs |
| Staging or preview sites   | Restrict access to pre-production environments | Simple gating for testers or QA         |
| Premium content (internal) | Limit access to specific resources             | Consider UX for public-facing content   |

> **lightbulb** NGINX basic auth uses the browser's built-in username/password prompt. It's appropriate for internal or staging protection, but for public-facing authentication consider framework-based auth, OAuth, or SSO for a better user experience.

Example: password-protecting a subpath
You may want `https://www.kodekloud.com` publicly available while protecting `https://www.kodekloud.com/admin` with a username and password. When configured, visiting `/admin` will trigger the browser's basic auth prompt.

<Frame>
  <img alt="An illustration of a person sitting at a desk working on a laptop. To the right is a login form and URL (&#x22;https://www.kodekloud.com/admin&#x22;) under the heading &#x22;Not Protected.&#x22;" />
</Frame>

Creating the credentials file
NGINX reads credentials from a file such as `/etc/nginx/conf.d/.htpasswd`. Two common ways to build this file:

1. Recommended: using `htpasswd` from apache2-utils (Debian/Ubuntu) or httpd-tools (RHEL/CentOS/Fedora)

* Install the utility (Debian/Ubuntu example):

```bash theme={null}
sudo apt update
sudo apt install -y apache2-utils
```

* Create the password file and add the first user (`-c` creates the file; omit `-c` to add more users without overwriting):

```bash theme={null}
sudo htpasswd -c /etc/nginx/conf.d/.htpasswd admin
