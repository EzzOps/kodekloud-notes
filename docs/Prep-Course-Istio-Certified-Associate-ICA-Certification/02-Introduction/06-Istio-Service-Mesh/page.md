# Create a test pod
kubectl run test --image=nginx
# Check pod readiness
kubectl get pods
# Check services
kubectl get svc

# Test application connectivity from the test pod
kubectl exec -ti test -- curl http://helloworld:5000/hello
# Sample responses showing traffic reaching different versions
# Hello version: v2, instance: helloworld-v2-654d97458-7vp24
# Hello version: v1, instance: helloworld-v1-7459d7b54b-lqt16
```

These outputs illustrate how traffic may route to different service versions (v1/v2) when traffic splitting is configured.

Security and zero-trust

* Enforce mTLS for secure service-to-service communication.
* Use AuthenticationPolicies (or PeerAuthentication in newer versions) and AuthorizationPolicies to implement role-based access control and fine-grained permissions.

<Frame>
  <img alt="The image illustrates the Zero-Trust Security Model with components like devices, identities, data, applications, infrastructure, and network, accompanied by the motto: &#x22;Never trust, always verify! Even inside your own network.&#x22; It also features a small inset of a person wearing a &#x22;KodeKloud&#x22; t-shirt." />
</Frame>

Advanced scenarios

* Register external workloads with `WorkloadEntry`.
* Troubleshoot common issues and apply best practices for multi-cluster and hybrid deployments.
* Learn performance considerations and tips for production readiness.

Throughout the course, I’ll share exam strategies, common pitfalls, and proven approaches to studying for the ICA.

Community & continuous learning
Join the KodeKloud community to ask questions, share insights, and collaborate with peers — a great way to reinforce learning and get unstuck during labs.

<Frame>
  <img alt="The image shows a screenshot of a KodeKloud platform interface displaying community and category sections alongside a map with user avatars. There's also an inset of a person speaking at the bottom right." />
</Frame>

Ready to master Istio and accelerate your cloud-native career? Start the course and practice with the labs and mock exams to confidently earn your Istio Certified Associate certification.

Links and references

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
* [Linux Foundation - ICA Exam Information](https://training.linuxfoundation.org/certification/)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/0d441034-8968-4e53-94ec-8d930da493de)


# Istio Service Mesh

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Introduction/Istio-Service-Mesh/page

Introduction to Istio service mesh explaining data and control planes, istiod, Envoy sidecars, traffic management, security with mTLS, observability, and operational considerations for microservices

Now that we know what a sidecar is, let's define Istio and how it helps run microservice-based applications.

Istio is an open-source service mesh that helps organizations run distributed, microservice-based applications anywhere.

<Frame>
  <img alt="The image displays the Istio logo and describes it as an open-source service mesh for running microservices apps across any environment." />
</Frame>

What does that mean in practice?

There are many container runtimes—Docker, containerd, rkt, Podman, CRI-O, LXC, Mirantis, and others. Managing these runtimes across many services and environments can be complex and time-consuming.

<Frame>
  <img alt="The image shows logos of different container runtimes, including Docker, containerd, Rocket, Podman, and cri-o, along with a caption stating, &#x22;Managing containers can be difficult and time-consuming.&#x22;" />
</Frame>

Kubernetes solves much of the container orchestration problem by managing lifecycle operations (create, restart, destroy) across runtimes. In a similar way, Istio is to the Envoy proxy what Kubernetes is to containers: an orchestrator that manages deployed Envoy sidecars.

<Frame>
  <img alt="The image shows logos of Istio and Envoy, with a note stating that an orchestrator facilitates the management of Envoy Proxies." />
</Frame>

Architecture overview

An Istio service mesh consists of two primary layers: the data plane and the control plane. Understanding the responsibilities of each is key to designing and operating an Istio mesh.

Data plane

* The data plane handles actual traffic between microservices.
* It deploys sidecar proxies (typically Envoy) next to each workload.
* Responsibilities include routing, load balancing, TLS encryption using mTLS, telemetry collection, and service-level authentication.

<Frame>
  <img alt="The image illustrates a data plane setup where &#x22;Service A&#x22; and &#x22;Service B&#x22; communicate over mesh traffic using Envoy proxies." />
</Frame>

Control plane

* The control plane manages and configures the data plane.
* It distributes policies and certificates, performs service discovery, and enforces authentication and authorization.
* It dynamically converts high-level routing and policy definitions into Envoy-specific configuration and pushes those configs to sidecars.

<Frame>
  <img alt="The image is a diagram showing how Istio's control plane manages and configures the data plane through network policies, certificate authority, authentication, and authorization." />
</Frame>

istiod: the core control-plane component

The primary control-plane component in modern Istio is istiod. When Istio is installed into a Kubernetes cluster, istiod runs as a pod (or a set of pods) and provides several critical services:

* Service discovery and config distribution: translates mesh-level routing and policy into Envoy-specific configuration and pushes changes to sidecars at runtime.
* Certificate Authority: issues and rotates certificates used for mTLS so workloads can securely authenticate one another.
* Authentication and authorization enforcement: supports service-to-service and end-user identity, enabling fine-grained access control.

<Frame>
  <img alt="The image is a diagram showing the architecture of an Istio service mesh within a Kubernetes environment, illustrating the control plane and the distribution of Envoy proxies across multiple nodes." />
</Frame>

Istiod functions as a certificate authority and supports workload identity and credential management. This allows you to enforce strict access controls so services accept traffic only from authorized callers.

<Frame>
  <img alt="The image illustrates a Kubernetes architecture with Istio for security, showcasing three nodes with different namespaces and services interconnected through Envoy proxies. It highlights the control plane, certificate authority, and secure communication between services." />
</Frame>

At-a-glance comparison

| Layer         | Primary responsibilities                                                  | Examples                                |
| ------------- | ------------------------------------------------------------------------- | --------------------------------------- |
| Data plane    | Handles traffic, sidecar proxies, routing, mTLS, telemetry                | Envoy sidecars adjacent to pods         |
| Control plane | Service discovery, policy and config distribution, certificate management | `istiod` running as pods in the cluster |

Why use Istio?

* Traffic management: Define advanced routing rules such as traffic splitting, canary releases, mirroring, and weighted routing—far beyond a simple load balancer.
* Security: Automatically encrypt traffic between workloads using mTLS and manage certificates, removing the need for custom TLS implementations.
* Authentication and authorization: Enforce access control policies so services only accept traffic from authorized sources.

<Frame>
  <img alt="The image outlines three benefits of using Istio: Traffic Management, Security, and Policies. Each benefit is briefly described, emphasizing customizable routing, automatic encryption, and access control." />
</Frame>

Other key benefits

* Observability: Centralized telemetry (logs, metrics, traces) simplifies aggregation and analysis with tools such as Jaeger, Prometheus, or Datadog APM.
* Resilience and reliability: Built-in patterns like circuit breaking, retries, timeouts, and fault injection help reduce cascading failures and improve availability.
* Reduced operational overhead: Shifts networking, security, and observability concerns out of application code and into the mesh so developers can focus on business logic. The sidecar approach is transparent to applications—workloads generally do not need modification to take advantage of the mesh.

<Frame>
  <img alt="The image presents three reasons to use Istio: Observability, Resilience and Reliability, and Reduced Operation Overhead, each highlighted with a brief description." />
</Frame>

> **lightbulb** Istio's sidecar model is transparent to application code: you typically inject Envoy proxies beside your workloads (automatically or manually) and let Istio manage networking, security, and telemetry without modifying your application binaries.

> **warning** While Istio reduces application complexity, it introduces operational components (control plane, certificate lifecycle, sidecar management) that must be monitored and maintained. Plan for observability and backup strategies for the control plane.

Feature summary

| Feature                       | Benefit                                                |
| ----------------------------- | ------------------------------------------------------ |
| Traffic shaping & routing     | Canary releases, A/B testing, fault injection          |
| mTLS and certificate rotation | Secure, authenticated service-to-service communication |
| Centralized telemetry         | Easier troubleshooting and performance monitoring      |
| Policy enforcement            | Fine-grained access control and rate limiting          |

Further reading and references

* [Istio Documentation](https://istio.io/)
* [Envoy Proxy](https://www.envoyproxy.io/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

That wraps up this introductory section. In the next lesson we'll summarize and start configuring a simple Istio-enabled workload.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/a7a3147b-376c-4759-8100-becb5d9e2eab)
