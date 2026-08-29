# Debian/Ubuntu
sudo apt update
sudo apt install nginx

# RHEL/CentOS (dnf or yum)
sudo dnf install nginx
sudo systemctl enable --now nginx
```

You’ll also learn how to manage virtual servers (`server` blocks), set up redirects and rewrites, and configure upstream server pools for load balancing.

We’ll cover HTTPS and best practices for TLS termination — including using automated certificate issuers like Let's Encrypt — and how to configure essential HTTP headers (HSTS, Content-Security-Policy, X-Frame-Options) to harden your deployment.

<Frame>
  <img alt="A presentation slide titled &#x22;Importance of HTTPS&#x22; showing a computer and a browser window linked by a padlock icon to illustrate secure HTTP. A small circular video inset of the presenter appears in the bottom-right." />
</Frame>

Security callouts:

<Callout icon="warning">
  Always run updates and follow the principle of least privilege. Use valid TLS certificates and enable strong cipher suites. When exposing services to the public internet, make sure your firewall is configured and only necessary ports (e.g. 80, 443) are open.
</Callout>

Optimization and observability are key parts of production operations. You will implement rate limiting, HTTP caching, gzip/brotli compression, and basic monitoring to reduce latency and improve throughput. We’ll also cover how to read and make sense of NGINX access and error logs to diagnose issues.

<Frame>
  <img alt="A screenshot of an Nginx dashboard displaying graphs, request logs, and connection metrics. A small circular video feed of a person appears in the bottom-right corner." />
</Frame>

Course structure

| Module                         | Focus                  | What you'll learn                                     |
| ------------------------------ | ---------------------- | ----------------------------------------------------- |
| Installation & Basics          | Get started            | Install NGINX, directory layout, managing the service |
| Virtual Hosts & Routing        | Hosting multiple sites | `server` blocks, `location` matching, redirects       |
| Reverse Proxy & Load Balancing | Scale applications     | Upstreams, health checks, sticky sessions             |
| TLS & Security                 | Secure delivery        | HTTPS, certificates, security headers, rate limiting  |
| Performance & Caching          | Improve latency        | gzip/brotli, proxy\_cache, caching headers            |
| Monitoring & Troubleshooting   | Maintain reliability   | Logs, status module, metrics, debugging tips          |

<Callout icon="lightbulb">
  Tip: Follow along with the labs. Practicing each module on a local VM or cloud instance will help you retain the configuration patterns and troubleshooting steps covered in the videos.
</Callout>

Additional resources and references

* NGINX official documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* NGINX Beginner Guide: [https://nginx.org/en/docs/beginners\_guide.html](https://nginx.org/en/docs/beginners_guide.html)
* Let’s Encrypt for TLS certificates: [https://letsencrypt.org/](https://letsencrypt.org/)
* KodeKloud community and course labs: [https://kodekloud.com/](https://kodekloud.com/)

Community
At KodeKloud, community learning matters. Join the discussion forums to ask questions, share configurations, and compare troubleshooting approaches with peers worldwide.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/9e6f72d7-933d-42dd-a948-ae48d66aecb6/lesson/b982ee43-0a38-4e27-b570-2e22b1d6ae55" />
</CardGroup>


# Introduction to Nginx

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Introduction/Introduction-to-Nginx/page

Introduction to Nginx web server, its event driven architecture, uses as reverse proxy and load balancer, static content serving, editions, performance strengths and widespread adoption

## What is Nginx?

Nginx is a high-performance web server and reverse proxy first released in the early 2000s. Built around an event-driven, asynchronous architecture, it was designed to address the limitations of older process-per-connection servers and to scale efficiently on modern workloads. Nginx runs on Linux, macOS, and Windows (note: Windows builds exist but Unix-like systems—especially Linux—are the most common production platforms).

<Frame>
  <img alt="A presentation slide titled &#x22;Nginx – Introduction&#x22; with the line &#x22;It was designed to overcome the limitations of older web servers.&#x22; The slide also shows performance-related icons, including a growth chart and a thumbs-up badge." />
</Frame>

Nginx was created to compete with long-established servers like Apache and IIS that used process- or thread-per-connection models. Its non‑blocking, event-driven workers allow a single process to manage thousands of simultaneous connections with lower memory use and latency — making Nginx ideal for high-concurrency scenarios.

<Frame>
  <img alt="A slide titled &#x22;Nginx – Introduction&#x22; showing a central server icon connected by dotted arrows to five user avatar icons. It visually represents users routing or load-balancing traffic to a single server." />
</Frame>

## Key strengths and common uses

* Serving static content (HTML, CSS, images, audio, video) with minimal resource consumption and low latency.
* Acting as a reverse proxy and edge server to terminate TLS, perform caching, and shield backend services.
* Load balancing and traffic routing across multiple application servers.
* Supporting extensibility via modules and integrations (e.g., OpenResty for Lua scripting).

Serving static content is one of Nginx’s most polished capabilities. It’s optimized to deliver assets quickly and efficiently, which is why many sites use Nginx as the front-facing server in front of application servers or CDNs.

<Frame>
  <img alt="A presentation slide titled &#x22;Serving Static Content With Nginx&#x22; showing HTML5, CSS3 and Node.js icons inside a rounded pink panel with labeled boxes for &#x22;Frontend Software&#x22; and &#x22;Videos.&#x22; The subtitle reads &#x22;Effortless handling of various file types.&#x22;" />
</Frame>

Under the hood, Nginx’s worker model is non-blocking and asynchronous. This design enables a single worker to handle many connections concurrently, which often yields better throughput and lower latency compared to traditional architectures that spawn one thread or process per connection.

Nginx is available in both the free open source community edition and a commercially supported edition that includes additional features and professional support.

<Frame>
  <img alt="A presentation slide titled &#x22;Commercial Variant&#x22; with a turquoise box labeled &#x22;Open-Source Community Version,&#x22; a purple box labeled &#x22;Commercial Paid Version,&#x22; and a smaller pink bar labeled &#x22;Paid Support.&#x22; Copyright KodeKloud is shown at the bottom left." />
</Frame>

|                 Edition | Best for                                            | Notable features                                                                         |
| ----------------------: | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
|     Open-source (nginx) | Developers, hobby projects, many production sites   | Core web server, reverse proxy, load balancing, caching, modular architecture            |
| Commercial (Nginx Plus) | Enterprises needing support and additional features | Active support, advanced monitoring, session persistence, commercial modules and tooling |

<Callout icon="lightbulb">
  If you want the open source distribution, use [nginx.org](https://nginx.org). For the commercial Nginx Plus and related products, use [nginx.com](https://nginx.com). The sites are related but serve different editions and documentation.
</Callout>

## Adoption and market presence

Nginx has broad adoption across the web due to its performance, flexibility (reverse proxying, load balancing, caching, TLS termination), and rich ecosystem. Surveys and market analyses frequently show Nginx as one of the most used web servers globally — including significant share among top-ranked websites and in overall domain counts.

<Frame>
  <img alt="A slide titled &#x22;NGINX Metrics&#x22; showing a Netcraft market-share line chart and a table reporting web server usage, with nginx listed as the most popular server (~21% in June 2024). The left column contains short bullet points comparing nginx to OpenResty and Cloudflare." />
</Frame>

Because of these attributes, Nginx is trusted by thousands of organizations — including many recognizable technology and media companies.

<Frame>
  <img alt="A slide titled &#x22;Testimonials&#x22; showing a grid of well-known company logos. Examples include Adobe, Atlassian, Cisco, Disney+, Instagram, Airbnb, LinkedIn, Cloudflare, GitHub, Salesforce, Netflix, IBM, Microsoft, Facebook, X and Zendesk." />
</Frame>

In the lessons that follow, we’ll explore Nginx’s architecture, configuration basics, and common deployment patterns (reverse proxy, load balancing, caching, TLS termination), showing how its design enables high performance and scalability for modern web applications.

## Links and references

* Nginx official (open source): [https://nginx.org](https://nginx.org)
* Nginx commercial (Nginx Plus): [https://nginx.com](https://nginx.com)
* Nginx documentation and configuration examples: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/9e6f72d7-933d-42dd-a948-ae48d66aecb6/lesson/7c5a412f-6586-46e5-acb2-b1ea364b4de8" />
</CardGroup>
