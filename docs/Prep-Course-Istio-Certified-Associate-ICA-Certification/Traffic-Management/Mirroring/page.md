# Mirroring

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Mirroring/page

Istio traffic mirroring explained, comparing canary and blue green releases, showing Kubernetes examples to mirror production requests to a v2 service for safe real traffic testing.

Before we talk about mirroring, we need to cover release strategies.

A canary release is the process of introducing a new version of your application gradually. The typical pattern is to route the majority of traffic to the stable v1 deployment while a small percentage of users are routed to the new v2 version.

<Frame>
  <img alt="The image illustrates the concept of a Canary Release, showing a Kubernetes setup where 90% of users are directed to Deployment V1 and 10% to Deployment V2 via an ingress gateway." />
</Frame>

The percentage can be tuned higher or lower, but the gradual rollout and limited exposure are what define canary releases.

Blue-green release, by contrast, is an immediate switch of traffic from v1 to v2 — a hard cutover. Users are on v1 one moment and on v2 the next.

<Frame>
  <img alt="The image illustrates a Blue/Green release deployment strategy using Kubernetes, showing an ingress gateway directing traffic to different service deployments within a namespace." />
</Frame>

Both approaches have trade-offs.

* Rollout: Canary is gradual; blue-green is all-or-nothing.
* Risk/downtime: Canary minimizes risk to a subset of users; blue-green can be rolled back quickly but is riskier during the switch.
* Exposure: Canary limits exposure (so it can be hard to know how the full stack will behave under full load), while blue-green immediately exposes the whole user base to the new version.

<Frame>
  <img alt="The image is a table comparing the pros and cons of Canary Release and Blue/Green Release strategies, focusing on rollout, downtime, and exposure aspects." />
</Frame>

In summary: canary releases are ideal for gradual testing with low risk, while blue-green offers a fast switch and easier rollback. But what if you want the best of both worlds?

Istio provides that with [traffic mirroring](https://istio.io/latest/docs/tasks/traffic-management/mirroring/).

Istio traffic mirroring sends a copy of live production traffic to another service (for example, a test or staging version) while still returning responses from the production service. This lets you exercise v2 with real requests without impacting end users.

In this lesson/article, to set up mirroring you need two versions of the application (v1 and v2) and a shared Service that selects both versions. Example Kubernetes resources:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v2-deployment
  namespace: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: v2
  template:
    metadata:
      labels:
        app: frontend
        version: v2
    spec:
      containers:
      - name: app
        image: app:2.1
---
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
    app: frontend
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v1-deployment
  namespace: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: v1
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      containers:
      - name: app
        image: app:1.1
```

Both deployments share the same `app-svc` Service via the `app: frontend` selector, while each deployment is distinguished by its `version` label.

Istio does not provide a standalone "mirror" resource; mirroring is configured in the [VirtualService](https://istio.io/latest/docs/reference/config/networking/virtual-service/) (with subsets defined in a [DestinationRule](https://istio.io/latest/docs/reference/config/networking/destination-rule/)). Here is an example VirtualService and DestinationRule that send all production traffic to subset `v1` while mirroring it to subset `v2`:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: app-vs
  namespace: frontend
spec:
  hosts:
  - app-svc
  http:
  - route:
    - destination:
        host: app-svc
        port:
          number: 80
        subset: v1
      weight: 100
    mirror:
      host: app-svc
      port:
        number: 80
      subset: v2
    mirrorPercent: 100
```

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: app-ds
  namespace: frontend
spec:
  host: app-svc
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

Explanation:

* The `route` block sends 100% of client requests to subset `v1`.
* The `mirror` block instructs [Envoy](https://www.envoyproxy.io/docs/envoy/latest/) to send a copy of the request to subset `v2`.
* `mirrorPercent` controls what fraction of requests are mirrored (100 means mirror every request; you can set a lower percentage to sample).

Why use mirroring?

* Test new versions with real production traffic without affecting users.
* Detect bugs and performance issues early, under real-world conditions.
* Gain insights for debugging, benchmarking, and capacity planning.
* Safely validate behavior before switching traffic fully.

<Frame>
  <img alt="The image presents reasons to use mirroring in software deployment, highlighting benefits such as testing in production, early issue identification, no user impact, safe transitions, and gaining performance insights." />
</Frame>

Important notes:

<Callout icon="lightbulb">
  Mirrored requests are sent as copies by the sidecar proxy (Envoy). The proxy does not wait for the mirrored response — the client only receives the response from the primary (non-mirrored) route. Because mirrored traffic can still trigger side effects on the mirrored service, avoid mirroring requests that cause irreversible actions (e.g., charging payments) unless the mirrored service is prepared to handle such effects safely.
</Callout>

Istio mirroring has a compact set of options (destination, subset, port, and mirrorPercent). For complete details and the latest API versions, see the [Istio VirtualService documentation](https://istio.io/latest/docs/reference/config/networking/virtual-service/). Setting up mirroring is straightforward and provides a low-risk way to validate new service versions with live traffic before a full rollout.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/40d8a24b-c16f-4781-9c26-20d4b1d5baf3" />
</CardGroup>
