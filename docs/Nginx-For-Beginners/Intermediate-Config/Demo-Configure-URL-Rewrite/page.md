# or: systemctl reload nginx
```

## 5. Verify the redirect and HTTPS behavior

Test the HTTP → HTTPS redirect locally with curl.

Check only headers (should show `301` and `Location` header):

```bash theme={null}
root@ubuntu-host:~# curl -I http://localhost
HTTP/1.1 301 Moved Permanently
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 01 Jan 20XX 00:00:00 GMT
Content-Type: text/html
Content-Length: 178
Connection: keep-alive
Location: https://localhost/
```

A plain curl will show the HTML 301 page:

```bash theme={null}
root@ubuntu-host:~# curl http://localhost
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx/1.18.0 (Ubuntu)</center>
</body>
</html>
```

With port 443 allowed and NGINX serving your TLS server block, visiting `https://<your-host>` in a browser should load the site over HTTPS (no 502).

If a user visits `http://diner.com/some/path`, the `return 301 https://$host$request_uri;` will redirect them to `https://diner.com/some/path`, preserving the full path and query string.

<Callout icon="warning">
  Make sure the TLS certificate and key are valid for the `server_name` you use. An invalid certificate will produce browser warnings even if the redirect is correct.
</Callout>

## Quick checklist

| Step            | Purpose                                        | Example command / file                                                              |
| --------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------- |
| Verify firewall | See which ports are open                       | `ufw status`                                                                        |
| Allow HTTPS     | Permit inbound TLS traffic                     | `ufw allow 443/tcp`                                                                 |
| Configure NGINX | Add HTTP → HTTPS redirect and TLS server block | `/etc/nginx/sites-available/diner-https` (see above)                                |
| Enable site     | Activate site config                           | `ln -s /etc/nginx/sites-available/diner-https /etc/nginx/sites-enabled/diner-https` |
| Test & reload   | Validate and apply changes                     | `nginx -t && nginx -s reload`                                                       |
| Verify          | Confirm redirect and TLS are working           | `curl -I http://localhost` and visit `https://<your-host>`                          |

## Recap

* Use a simple server block on port 80 to issue a `301` redirect to HTTPS.
* Serve the site on port 443 with TLS configured.
* Ensure the firewall allows port 443 before relying on HTTPS.
* Validate the NGINX config and reload before testing to avoid downtime.

Further reading:

* NGINX docs: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Let's Encrypt: [https://letsencrypt.org/](https://letsencrypt.org/)
* curl: [https://curl.se/](https://curl.se/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/c78ff9cb-c15d-4f85-92fc-abee5ed98b20/lesson/4335a4b8-d404-4150-9001-09851f436e4a" />
</CardGroup>


# Demo Configure URL Rewrite

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Demo-Configure-URL-Rewrite/page

Guide showing how to configure an Nginx rewrite to permanently redirect /images requests to /pics, preserving links and issuing HTTP 301 responses

This guide demonstrates how to use the Nginx `rewrite` directive to map one URL path to another. In this example, the site serves images from `/var/www/html/images`, but the site owner wants to use `/pics` going forward. To preserve existing `/images/*` links (so bookmarks and external links keep working), we’ll add a rewrite that transparently redirects `/images/...` requests to `/pics/...`.

Why this matters:

* Keeps old links working while you change the public path.
* Issues an HTTP 301 (permanent) redirect so clients and search engines update bookmarks and indexes.
* Easy to implement without moving clients to the new path manually.

Example URLs:

```text theme={null}
http://example.com/images/pic10.jpg
http://example.com/pics/pic10.jpg
