# Summary

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Introduction/Summary/page

Concise overview of Nginx, its event-driven architecture, open-source and commercial editions, and common uses like reverse proxying, load balancing, TLS termination, and caching

This lesson reviewed the fundamentals of how web servers work and why Nginx is widely used in modern web architectures.

* When you browse a website, your browser sends HTTP(S) requests to a web server. The server generates or proxies the requested content and returns it to the browser.
* Nginx was designed as a high-performance alternative to legacy servers (for example, Apache or IIS). Its design goals—efficiency, high concurrency, and low memory usage—help explain its broad adoption.
* Two main editions exist:
  * The open-source Nginx is freely available and widely used.
  * Nginx Plus is the commercial edition that adds enterprise features, advanced monitoring, and commercial support.
* Nginx remains a market leader because of its event-driven, asynchronous architecture, which provides high concurrency with a low memory footprint. It’s commonly deployed as:
  * a static file server,
  * a reverse proxy,
  * a load balancer,
  * a TLS (SSL) terminator.

## Nginx editions at a glance

| Edition           | Best for                                             | Key differences                                                                              |
| ----------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Open-source Nginx | Developers, small teams, general-purpose deployments | Lightweight, flexible, free to use                                                           |
| Nginx Plus        | Enterprises, mission-critical deployments            | Adds active health checks, advanced load balancing controls, metrics, and commercial support |

## How Nginx works (high level)

* Nginx uses an event-driven, non-blocking architecture rather than one-thread-per-connection. This allows a small number of worker processes to handle many simultaneous connections efficiently.
* For dynamic content, Nginx usually proxies requests to application servers (e.g., Node.js, Python WSGI, PHP-FPM). For static files, it serves content directly from disk.
* As a reverse proxy and load balancer, Nginx can:
  * distribute traffic across backend servers,
  * terminate TLS so backends can run unencrypted,
  * cache responses and reduce load on origin servers.

## Common Nginx use cases

* Static file hosting (images, CSS, JavaScript)
* Reverse proxy in front of application servers
* SSL/TLS termination and certificate management
* Layer 7 load balancing with health checks and session persistence
* Caching and request rate limiting

<Frame>
  <img alt="A presentation summary slide with a turquoise sidebar and four colorful numbered points. It lists takeaways about web servers and Nginx — its popularity, open-source and commercial variants, installation flexibility, and performance/use cases." />
</Frame>

> **lightbulb** Tip: If you’re evaluating Nginx for production use, start with the open-source edition for learning and development, then consider Nginx Plus if you need enterprise-grade features and support. For authoritative documentation, see the official Nginx resources linked below.

That wraps up this lesson. Next, we'll begin installing and configuring Nginx.

## Links and references

* Official Nginx site: [https://nginx.org/](https://nginx.org/)
* Nginx documentation and commercial product info: [https://www.nginx.com/](https://www.nginx.com/)
* HTTP basics: [https://developer.mozilla.org/en-US/docs/Web/HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/9e6f72d7-933d-42dd-a948-ae48d66aecb6/lesson/b0a86095-d6d4-402f-a256-26a6d7abdda2)
