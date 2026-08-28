# Demo Caching

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Performance/Demo-Caching/page

Guide demonstrating how to configure and verify NGINX disk proxy caching in front of Apache backends to reduce origin load with logging and verification steps.

In this lesson we configure disk caching in an NGINX reverse proxy that fronts two Apache backend web servers. First we'll observe the behavior with no proxy cache (every request hits the backends), then enable NGINX caching so the reverse proxy can serve repeated static assets and reduce load on Apache.

<Frame>
  <img alt="A diagram showing several users connecting through a network cloud to an NGINX reverse proxy (labeled No-Cache), which forwards requests to backend web servers running Apache and serving HTML/CSS/JS assets. Arrows indicate the traffic flow from clients → proxy → servers." />
</Frame>

At first, every asset request (HTML, CSS, JS, images, fonts, etc.) is proxied to the Apache backends and served by them. After enabling NGINX proxy caching, repeated requests for cacheable assets are served directly by NGINX from disk, saving backend CPU, memory, and network bandwidth.

<Frame>
  <img alt="A simple architecture diagram showing users connecting through a network cloud to a reverse-proxy/cache running NGINX. The NGINX proxy forwards requests to backend web servers (Apache)." />
</Frame>

Below is a concise, step-by-step walkthrough of what to change and how to verify caching.

## 1 — Inspect backend activity (no cache)

Tail the Apache access logs on a backend while you load the site from a client. This confirms that the origin receives every request before we enable proxy caching.

```bash theme={null}
