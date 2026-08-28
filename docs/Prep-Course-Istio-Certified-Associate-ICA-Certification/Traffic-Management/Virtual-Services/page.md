# Virtual Services

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Virtual-Services/page

Explains Istio VirtualService usage for L7 traffic routing, rewrites, splitting, mirroring, fault injection, and retries in Kubernetes with Envoy sidecars.

VirtualServices are one of the most important resources in Istio's traffic management model. They give you L7 control over how traffic is routed to your Kubernetes services — something a plain Kubernetes Service cannot do.

Analogy: think of a university's course assignment system. Each course (Literature, Mathematics, Geography, etc.) has a designated teacher and a schedule, and students are assigned to the right classes automatically. A VirtualService plays the role of that assignment system: traffic (students) arrives and the VirtualService directs it to the correct backend service (course) based on rules you define.

<Frame>
  <img alt="The image displays an illustration representing a university curriculum with subjects like Literature, Mathematics, Physics, Economics, and Geography, each accompanied by relevant icons." />
</Frame>

When students need to know where and when to attend classes, the schedule provides that mapping. Similarly, a VirtualService maps incoming requests to destinations using URI, headers, weights, and other match criteria.

<Frame>
  <img alt="The image shows a weekly course schedule with classes such as &#x22;Intro to Psychology,&#x22; &#x22;Ancient Civilizations,&#x22; &#x22;Art History,&#x22; and &#x22;Political Science 101&#x22; distributed across different days and times." />
</Frame>

Below is a minimal Kubernetes deployment and Service for an example application named `app` in the `frontend` namespace. This is the workload the VirtualService will route to.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: frontend
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: app:1.1
```

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: app-svc
  namespace: frontend
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: app
```

Note: the selector uses `app: app`. In production you should choose clear, consistent labels for maintainability.

A simple VirtualService for this workload might look like this. It is created in the same namespace (`frontend`) and targets the Kubernetes Service `app-svc`. The `http` block contains match rules and routes to your destination service.

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: app-vs
  namespace: frontend
spec:
  hosts:
    - app-svc
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: app-svc.frontend.svc.cluster.local
          port:
            number: 80
```

You do not always need a `match` entry; it is shown here to illustrate what you can include. At the bottom of the rule, `route` forwards traffic to the Kubernetes Service destination.

You can add multiple matches and even rewrite the URI. For example, requests to `/login` can be rewritten to `/` before being forwarded to the backend:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: app-vs
  namespace: frontend
spec:
  hosts:
  - app-svc
  http:
  - match:
    - uri:
        prefix: /login
    rewrite:
      uri: /
    route:
    - destination:
        host: app-svc.frontend.svc.cluster.local
        port:
          number: 80
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: app-svc.frontend.svc.cluster.local
        port:
          number: 80
```

This pattern is useful when the external path differs from how the application expects the route internally.

Why use a VirtualService? What can it do that a Kubernetes Service cannot?

* Fine-grained L7 routing based on headers, URIs, query parameters, and more.
* Traffic splitting for canary releases and A/B testing (weighted routing).
* Mirroring (shadowing) traffic for testing.
* Fault injection for resilience testing.
* Retries, timeouts, and advanced retry policies.
* URL rewrites and redirects.
* Advanced load balancing (round-robin, least connections, weighted routing).

<Frame>
  <img alt="The image explains reasons to use a virtual service, highlighting features like fine-grained routing, directing traffic for gradual rollouts, and implementing various testing and deployment strategies." />
</Frame>

You can simulate faults or inject delays to validate resilience, configure retries and timeouts to improve reliability, and use weighted routing to gradually shift traffic to new versions.

<Frame>
  <img alt="The image explains why to use a virtual service, highlighting the benefits of simulating faults to test service resilience and configuring retries and timeouts to improve reliability." />
</Frame>

Table: Common VirtualService capabilities and typical uses

|         Capability | Use case                           | Example / notes                           |
| -----------------: | ---------------------------------- | ----------------------------------------- |
|         L7 routing | Route by path, headers, or query   | `uri` prefix or `headers` match           |
|  Traffic splitting | Canary releases, A/B testing       | Weighted `route` destinations             |
|          Mirroring | Shadow traffic to test new service | `mirror` field in `http` route            |
|    Fault injection | Resilience testing                 | `fault` injection with `abort` or `delay` |
| Retries & timeouts | Improve reliability                | `retries` and `timeout` in `http` rule    |
|        URL rewrite | Map external to internal paths     | `rewrite` to change request `uri`         |

Important: VirtualServices only take effect when traffic passes through the Envoy sidecar proxy. If the target namespace does not have Istio sidecar injection enabled or a sidecar proxy is not injected into the pod, the VirtualService routing will not be applied.

<Callout icon="warning">
  If a namespace is not Istio-enabled (no sidecar proxy), a VirtualService will not have any effect. Ensure sidecar injection is enabled or that the workload includes the Envoy sidecar. See Istio sidecar injection docs: [https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/](https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/)
</Callout>

Most advanced Istio traffic-management features require a VirtualService. If you want mirroring, rewrites, fault injection, or any L7 policies, you will do it via VirtualService configuration. Become familiar with the Istio VirtualService reference so you can quickly craft the right rules:

* Istio VirtualService reference: [https://istio.io/latest/docs/reference/config/networking/virtual-service/](https://istio.io/latest/docs/reference/config/networking/virtual-service/)

<Callout icon="lightbulb">
  Traffic management and VirtualServices are heavily tested topics on the Istio certification. Spend time practicing match conditions, routing rules, rewrites, retries, and fault injection scenarios. Many exam tasks involve creating or troubleshooting VirtualServices.
</Callout>

Now that you understand the concepts and examples, try creating a VirtualService in a lab environment and observe how rules are applied when Envoy sidecars are present. This hands-on practice will solidify your understanding of routing behavior, rewrites, and canary strategies.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/0b22c7ab-b9bd-4abe-a20e-a7ba9d6f4441" />
</CardGroup>
