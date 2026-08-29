# Sidecar

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Introduction/Sidecar/page

Explains the sidecar pattern, how Envoy proxies support service meshes like Istio by offloading traffic management, security, observability, and how Istio automates sidecar deployment and configuration

To understand Istio, start with the concept of a sidecar.

Think back to learning how to ride a bike. At first you try to balance on your own and might fall. A sidecar is like an extra rider who helps keep balance, watches for traffic, navigates, and communicates with others so you can focus on driving. In software, a sidecar offloads auxiliary responsibilities from your main application so the application can focus on its core logic.

In short: a sidecar handles supporting tasks, organizes communication, improves safety, and provides observability so the main application can stay focused on business functionality.

<Frame>
  <img alt="The image is a list titled &#x22;Role of a Sidecar,&#x22; detailing its functions like handling tasks, organizing essentials, enhancing safety, and communication." />
</Frame>

Proxies used as sidecars are central to service-mesh traffic management. The most widely adopted proxy in modern service meshes is Envoy Proxy, which Istio uses (Istio provides its own distribution and configuration of Envoy). Other meshes and projects also adopt Envoy—examples include HashiCorp Consul and Kuma; AWS App Mesh can also use Envoy.

There are alternative proxies and proxy-based meshes as well:

| Proxy          | Typical meshes / use cases                                           | Docs                                                   |
| -------------- | -------------------------------------------------------------------- | ------------------------------------------------------ |
| Envoy          | Istio, Consul, Kuma, AWS App Mesh                                    | [https://www.envoyproxy.io](https://www.envoyproxy.io) |
| Linkerd2 proxy | Linkerd (linkerd.io) — lightweight service mesh                      | [https://linkerd.io](https://linkerd.io)               |
| Traefik Proxy  | Traefik Mesh — user-friendly routing and ingress features            | [https://traefik.io](https://traefik.io)               |
| HAProxy        | Used in custom or some Consul setups where HAProxy fits requirements | [https://www.haproxy.org](https://www.haproxy.org)     |

<Frame>
  <img alt="The image displays logos of four software options: Envoy, Traefik Proxy, Linkerd, and HAProxy." />
</Frame>

Envoy Proxy is an open-source, high-performance service proxy originally created at Lyft and now part of the Cloud Native Computing Foundation (CNCF). It functions like modern software load balancers (for example, NGINX) but is purpose-built for distributed, microservice architectures and the needs of service meshes.

A quick terminology note: "proxy" vs "sidecar"

* A proxy is the software that handles traffic (e.g., Envoy).
* A sidecar is the deployment pattern where that proxy runs alongside your application in the same Pod (or host).
  When people mention "sidecar injection," they refer to adding a proxy container (such as Envoy) to a workload so it intercepts and manages the application’s traffic.

<Callout icon="lightbulb">
  Sidecar injection means adding a proxy container (for example, Envoy) to a workload so the proxy runs alongside the application and intercepts inbound/outbound traffic.
</Callout>

How does an Envoy sidecar work?

Think of Envoy as a traffic controller or assistant for your application. In a system with many services that communicate, Envoy helps ensure messages reach the right destination efficiently and securely. In Kubernetes, the Envoy sidecar runs as a separate container inside the same Pod as your application container. It typically intercepts inbound and outbound communication (often via network-level redirection) and acts as a middleman that can enforce policies, secure traffic, route requests, and gather telemetry.

<Frame>
  <img alt="The image is a diagram of a Kubernetes service mesh setup, illustrating three nodes (Node 01, Node 02, Node 03) each with an application and service, along with Envoy proxies communicating within the mesh." />
</Frame>

Core responsibilities of an Envoy sidecar

| Responsibility     | What it does                                                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Routing            | Determines paths and forwards requests to the appropriate service instances; supports advanced routing (header-based, path-based) |
| Load balancing     | Distributes traffic across healthy replicas using algorithms such as round-robin, least-request, ring-hash                        |
| Security           | Enables encryption between services (e.g., mTLS), and enforces authentication and authorization policies                          |
| Observability      | Collects metrics, logs, and traces (latency, request counts, error rates) for monitoring and debugging                            |
| Traffic management | Implements rate limiting, retries, timeouts, circuit breaking, traffic splitting (canary, A/B), and mirroring                     |

These capabilities simplify interservice communication, improve security posture, and provide actionable telemetry for operations teams.

<Frame>
  <img alt="The image outlines three benefits of using Envoy Proxy: simplified communication, enhanced security, and improved performance. Each benefit is accompanied by a brief description and an icon." />
</Frame>

Reliability and advanced traffic control

Envoy improves reliability by routing traffic away from unhealthy instances, applying retry and timeout policies, and enabling traffic-shaping features like rate limiting and traffic mirroring. These mechanisms help with safer rollouts, fault isolation, and graceful degradation during failures.

<Frame>
  <img alt="The image explains why to use Envoy Proxy, highlighting its reliability in redirecting traffic when services fail, and its advanced features like rate limiting and traffic mirroring." />
</Frame>

Installing Envoy

You can install Envoy on many platforms (Linux distributions, macOS) or deploy it inside Kubernetes (for example via Helm). Managing Envoy instances manually for every workload in a large cluster is complex; service meshes like Istio provide control-plane components that automate sidecar injection, configuration, and lifecycle management.

Example installation commands:

```bash theme={null}
