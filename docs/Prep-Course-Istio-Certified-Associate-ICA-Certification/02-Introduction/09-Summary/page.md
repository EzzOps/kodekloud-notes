# Debian/Ubuntu (ensure the keyrings directory exists)
sudo mkdir -p /etc/apt/keyrings
wget -O - https://apt.envoyproxy.io/signing.key | sudo gpg --dearmor -o /etc/apt/keyrings/envoy-keyring.gpg
echo "deb [arch=amd64,arm64,signed-by=/etc/apt/keyrings/envoy-keyring.gpg] https://apt.envoyproxy.io `lsb_release -cs` stable" | sudo tee /etc/apt/sources.list.d/envoy.list
sudo apt-get update
sudo apt-get install -y envoy
envoy --version
```

```bash theme={null}
# macOS (Homebrew)
brew update
brew install envoy
envoy --version
```

Why use a service mesh like Istio?

Managing each proxy instance across many services—keeping configurations consistent, rotating certificates, applying global policies, and collecting telemetry—creates operational overhead. Istio provides a control plane that automates sidecar injection, distributes configuration, manages certificates (for mTLS), and offers higher-level traffic-management APIs so you don't manage every Envoy manually.

Later sections will build on this sidecar foundation to explain how Istio leverages Envoy for traffic management, security, and observability across microservices.

Links and references

* Envoy Proxy: [https://www.envoyproxy.io](https://www.envoyproxy.io)
* Istio: [https://istio.io](https://istio.io)
* Linkerd: [https://linkerd.io](https://linkerd.io)
* Traefik: [https://traefik.io](https://traefik.io)
* HashiCorp Consul: [https://www.consul.io](https://www.consul.io)
* Kuma: [https://kuma.io](https://kuma.io)
* AWS App Mesh: [https://aws.amazon.com/app-mesh](https://aws.amazon.com/app-mesh)
* CNCF: [https://www.cncf.io](https://www.cncf.io)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/dc89929f-2873-4397-8cc5-9fab62003c1f)


# Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Introduction/Summary/page

Overview of the ICA exam and Istio service mesh, covering sidecars, Envoy, Ambient mode, prerequisites, and proxy orchestration for secure Kubernetes workload communication

All right — this is a concise recap of what we covered in this introduction section.

* ICA exam: intermediate level, 2 hours long, 16 hands-on questions, passing score 68%. The exam no longer includes multiple-choice questions; it focuses entirely on hands-on tasks, and is generally easier than the previous version of the ICA.
* Prerequisites: familiarity with Kubernetes is essential. I don't recommend proceeding with this course or attempting the ICA unless you're comfortable using Kubernetes.
* Service mesh purpose: facilitates communication between workloads and provides security and reliability features that Kubernetes does not provide out of the box.

Sidecars, or proxies, are containers that

<Frame>
  <img alt="The image is a summary slide outlining three points: ICA is a 2-hour exam with a 68% passing score, Kubernetes knowledge is essential before certification, and Service Mesh ensures secure communication between workloads." />
</Frame>

run alongside application containers and proxy all traffic in and out. By delegating responsibilities such as authentication, encryption, observability (logging/metrics/tracing), and traffic routing to sidecars, teams avoid embedding these features into application code. This reduces operational overhead and lets developers focus on business logic while the service mesh handles cross-cutting concerns.

We also examined Istio’s Ambient mode, which is a sidecar-less deployment option. Istio uses Envoy as its data plane proxy; Envoy is a widely adopted proxy used by many service meshes (for example, Consul and Kuma also use Envoy). Istio has a large ecosystem and is one of the most popular service meshes in the Kubernetes landscape.

<Frame>
  <img alt="The image is a summary slide describing Istio, highlighting its features like the sidecarless mode called Ambient, its use of Envoy Proxy, its popularity as a service mesh for Kubernetes, and its proxy management capabilities similar to Kubernetes' container management." />
</Frame>

Conceptually, Istio functions as an orchestrator for proxies—similar to how Kubernetes orchestrates containers—managing proxy deployment, configuration, and lifecycle across the cluster.

That concludes the summary of this section.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/4b733cb1-68f8-421d-8584-bbbce581c88c)
