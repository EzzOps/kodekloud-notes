# Two Containers Behind a Load Balancer

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Two-Containers-Behind-a-Load-Balancer/page

Demonstrates running two backend containers behind an NGINX load balancer to observe request distribution and failover when one container stops.

This lab demonstrates running a small app in two backend containers behind an NGINX load balancer. You will:

* Start two app containers from the same image.
* Send multiple requests to the load balancer at `localhost:8080` and observe how requests are distributed.
* Stop one backend container while requests are being served and observe failover to the remaining container.

<Callout icon="lightbulb">
  This lab assumes an NGINX-based load balancer is already configured to proxy requests from `localhost:8080` to the two backend app containers. For a refresher, see [Introduction to NGINX](https://learn.kodekloud.com/user/courses/introduction-to-nginx).
</Callout>

## What you'll observe

* Requests to `localhost:8080` are proxied by NGINX to one of the two app containers.
* NGINX performs simple load distribution between the backends (round-robin or similar, depending on config).
* If one backend stops, NGINX continues to forward requests to the remaining healthy container, keeping the service available.

## Quick step-by-step

1. Launch two app containers (they both use the same image).
2. Confirm each container is running.
3. Send multiple `curl` requests to the load balancer and observe responses from each backend.
4. Stop one backend and continue sending requests to observe failover.

## Commands and examples

Start both containers:

```bash theme={null}
