# Start two app containers (both use the same image)
docker run -d --name app1 photoapp:v1
docker run -d --name app2 photoapp:v1
# Example output: b7e2d1...
```

Send requests to the load balancer on port 8080:

```bash theme={null}
# Send requests to the load balancer
curl localhost:8080
curl localhost:8080
# Example response: Hello from app2
```

Simulate failover by stopping one backend while requests are ongoing:

```bash theme={null}
# Stop one backend container
docker stop app1

# Requests should continue and be routed to the remaining container
curl localhost:8080
# Example response: Hello from app2
```

## Commands reference

| Task                     |                                 Command | Notes / Example output                                                   |
| ------------------------ | --------------------------------------: | ------------------------------------------------------------------------ |
| Run first app container  | `docker run -d --name app1 photoapp:v1` | Starts `app1` in detached mode; sample container ID `a1f3c9...`          |
| Run second app container | `docker run -d --name app2 photoapp:v1` | Starts `app2`; sample container ID `b7e2d1...`                           |
| Query load balancer      |                   `curl localhost:8080` | Response shows which backend served the request, e.g., `Hello from app1` |
| Stop a backend           |                      `docker stop app1` | Takes `app1` offline; NGINX should then route requests to `app2`         |

> **warning** Make sure container names (e.g., `app1`, `app2`) match the backend upstream configuration in your NGINX proxy, and that the load balancer is listening on `localhost:8080`. If NGINX isn’t configured correctly, requests will not be forwarded to your containers.

## Troubleshooting tips

* If `curl localhost:8080` returns a connection refused error, validate that NGINX is running and listening on port 8080:
  * `ss -ltnp | grep 8080` or `docker ps` (if NGINX is containerized).
* If responses always come from the same backend, inspect the NGINX upstream configuration to confirm the load-balancing method.
* Use `docker logs <container>` to see app-specific output if you don’t get the expected `Hello from ...` responses.

## Links and references

* [Introduction to NGINX](https://learn.kodekloud.com/user/courses/introduction-to-nginx)
* Docker documentation: [https://docs.docker.com/](https://docs.docker.com/)
* NGINX upstream module reference: [https://nginx.org/en/docs/http/ngx\_http\_upstream\_module.html](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)

This exercise shows how NGINX maintains availability by routing traffic to the remaining healthy backend when one container is taken down.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/cf5f79dd-4231-449a-ac1a-357d65d1c399)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/8f843c54-252a-4195-a75a-acbbdc090246)


# Vertical vs Horizontal Scaling

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Vertical-vs-Horizontal-Scaling/page

Comparison of vertical and horizontal scaling strategies for web apps, explaining trade-offs, operational considerations, and when to scale up versus scale out for capacity and reliability.

Your photo app is growing: CPU is at \~80% and feeds are loading slower. To gain capacity there are two fundamental approaches — make a single server more powerful (vertical scaling) or run many servers in parallel (horizontal scaling). Each approach has trade-offs in cost, complexity, and reliability.

## Vertical scaling (scale up)

Vertical scaling means increasing a single machine’s resources: more CPU, more RAM, faster disk. You keep the same application code and simply provision a larger instance.

<Frame>
  <img alt="The image illustrates the concept of vertical scaling, showing how to make a server bigger by adding more CPU, RAM, and a faster disk, with a smartphone interface on the left and server icons on the right." />
</Frame>

Pros

* Simple to implement — no app changes required.
* Low operational overhead for small-scale apps.
* Quick to get more capacity by resizing instances.

Example: an unchanged server startup call remains valid.

```javascript theme={null}
app.listen(80);
```

Drawbacks

* Hard upper limit: you can only buy the biggest machine available.
* Diminishing returns: higher tiers often cost disproportionately more for modest gains.
* Single point of failure: one large server failing takes your whole app down.

<Frame>
  <img alt="The image illustrates a scenario where a single large server failure causes an entire app to go down, depicted by a broken server icon and a mobile app interface showing errors. The text emphasizes &#x22;One big server is still one server&#x22; and &#x22;The whole app is down.&#x22;" />
</Frame>

When to use vertical scaling

* Early stages or prototypes.
* Predictable workloads that fit within the capacity of a single machine.
* When minimizing operational complexity is a priority.

## Horizontal scaling (scale out)

Horizontal scaling runs multiple instances of your app across many smaller servers. Add more machines as traffic grows.

<Frame>
  <img alt="The image illustrates horizontal scaling using multiple small servers, showing that if one server fails, the others continue to function. It has a diagram with an app interface pointing to a grid of servers, with one marked as failed." />
</Frame>

Advantages

* Virtually unlimited capacity by adding instances.
* Higher availability: no single point of failure.
* Cost efficiency at scale when using commodity instances or containers.

Operational considerations

* You need a load balancer to distribute requests across the fleet.
* Shared state must be externalized (database, object storage, or shared cache) so any instance can serve any request.
* More complexity: service discovery, orchestration (e.g., Kubernetes), monitoring, and autoscaling policies.

When to use horizontal scaling

* High and/or unpredictable traffic.
* Requirements for high availability and fault tolerance.
* Architectures built around microservices, containers, or distributed systems.

## At-a-glance comparison

| Aspect            | Vertical scaling (Scale Up)             | Horizontal scaling (Scale Out)                         |
| ----------------- | --------------------------------------- | ------------------------------------------------------ |
| Complexity        | Low                                     | Higher (load balancing, orchestration)                 |
| Cost pattern      | Often nonlinear, expensive at top tiers | More predictable; benefits from commodity instances    |
| Failure domain    | Single point of failure                 | Resilient to individual instance failures              |
| Capacity ceiling  | Limited by largest machine              | Practically unlimited by adding nodes                  |
| Example use cases | Small apps, prototyping, simple stacks  | Large-scale services, high availability, microservices |

## Practical rule of thumb

> **lightbulb** Start with vertical scaling for simplicity and lower initial cost. Move to horizontal scaling when you hit vertical limits, need higher availability, or when traffic grows beyond what a single machine can handle.

For further reading on building resilient, scalable systems, see:

* [Kubernetes: Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Load balancing patterns](https://en.wikipedia.org/wiki/Load_balancing_\(computing\))
* [Object storage for shared assets (S3-like)](https://aws.amazon.com/s3/)

Start simple, monitor key metrics (CPU, memory, latency, error rates), and evolve your architecture to match your traffic, availability, and cost requirements.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/1f08cb2d-dcd4-4e72-bfdc-2b3504bdb124)
