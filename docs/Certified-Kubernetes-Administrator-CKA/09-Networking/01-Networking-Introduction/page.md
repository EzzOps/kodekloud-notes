# ingress-wear-watch.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - host: wear.my-online-store.com
    http:
      paths:
      - backend:
          serviceName: wear-service
          servicePort: 80
  - host: watch.my-online-store.com
    http:
      paths:
      - backend:
          serviceName: watch-service
          servicePort: 80
```

This configuration supports HTTP-based rules such as host and path matching. However, it does not natively support other routing protocols like TCP, UDP, or advanced features such as traffic splitting, header manipulation, authentication, or rate limiting. To implement these capabilities, controller-specific annotations are used. For example, the following configuration adds NGINX-specific SSL redirection via annotations:

```yaml theme={null}
# ingress-with-annotations.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  rules:
  - host: wear.my-online-store.com
    http:
      paths:
      - path: /foo
        backend:
          serviceName: wear-service
          servicePort: 80
  - host: watch.my-online-store.com
    http:
      paths:
      - backend:
          serviceName: watch-service
          servicePort: 80
```

> **lightbulb** Because each controller implements its own set of annotations, these configurations are tightly coupled to specific controllers and cannot be validated by Kubernetes itself.

Similarly, advanced scenarios like configuring Cross-Origin Resource Sharing (CORS) require different annotations depending on the controller. For example, a CORS configuration for NGINX might look like this:

```yaml theme={null}
# Ingress-cors.yaml (for NGINX)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cors-ingress
  annotations:
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, PUT, POST"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://allowed-origin.com"
    nginx.ingress.kubernetes.io/cors-allow-credentials: "true"
```

And for a traffic controller like Traefik, a similar configuration would be:

```yaml theme={null}
# Ingress-traefik.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: traefik-ingress
  annotations:
    # CORS Configuration
    traefik.ingress.kubernetes.io/headers.customresponseheaders: |
      Access-Control-Allow-Origin: '*'
      Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
      Access-Control-Allow-Headers: Content-Type,Authorization
      Access-Control-Allow-Credentials: true
      Access-Control-Max-Age: 3600
```

These examples clearly demonstrate that the same use case leads to different configurations based solely on the chosen controller.

## Introducing the Gateway API

The Gateway API was created as an official Kubernetes project to overcome the limitations of Ingress. It supports both layer 4 (transport) and layer 7 (application) routing, representing the next generation of load balancing and service mesh APIs. By decoupling responsibilities, the Gateway API introduces three distinct objects:

1. **Gateway Class:** Configured by infrastructure providers to define the underlying network infrastructure (e.g., NGINX, Traefik, or other load balancers).
2. **Gateway:** Managed by cluster operators; these are instances built from a Gateway Class.
3. **HTTPRoute (and other route types):** Managed by application developers; these routes support various protocols such as HTTP, TCP, and gRPC.

Unlike Ingress, the Gateway API offers a unified and declarative configuration that is independent of controller-specific annotations.

### Gateway API Configuration Example

The following example illustrates how to define a Gateway Class, a Gateway, and an HTTPRoute using the Gateway API:

```yaml theme={null}
# gateway-class.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: example-class
spec:
  controllerName: example.com/gateway-controller
```

```yaml theme={null}
# gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: example-gateway
spec:
  gatewayClassName: example-class
  listeners:
    - name: http
      protocol: HTTP
      port: 80
```

```yaml theme={null}
# http-route.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: example-httproute
spec:
  parentRefs:
    - name: example-gateway
  hostnames:
    - "www.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /login
      backendRefs:
        - name: example-svc
          port: 8080
```

In this configuration, the HTTPRoute routes requests with a path prefix of "/login" arriving at "[www.example.com](http://www.example.com)" to the backend service "example-svc" on port 8080.

## TLS Configuration with Gateway API

Traditional Ingress configurations handle TLS by using the `spec.tls` section, often accompanied by additional annotations to enforce HTTPS redirection. Consider the following Ingress example for a secure application:

```yaml theme={null}
# ingress-secure-app.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-app
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - secure.example.com
      secretName: tls-secret
```

In contrast, the Gateway API allows for a more structured TLS configuration as part of the listener definition:

```yaml theme={null}
# gateway-secure.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: secure-gateway
spec:
  gatewayClassName: example-gc
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: tls-secret
  allowedRoutes:
    kinds:
      - kind: HTTPRoute
```

Here, the HTTPS listener on port 443 is explicitly configured with TLS termination, referencing the necessary TLS secret. The `allowedRoutes` field ensures that only HTTPRoute objects can attach to the listener.

## Traffic Splitting and Canary Deployments

Ingress relies on annotations for complex use cases like canary deployments. For example, you might use NGINX annotations to route 20% of the traffic to a new application version:

```yaml theme={null}
# canary-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: canary-ingress
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "20"
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-v2
            port:
              number: 80
```

The Gateway API simplifies this process by natively defining traffic splitting within an HTTPRoute:

```yaml theme={null}
# app-gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: split-traffic
spec:
  parentRefs:
    - name: app-gateway
  rules:
    - backendRefs:
        - name: app-v1
          port: 80
          weight: 80
        - name: app-v2
          port: 80
          weight: 20
```

In this example, "app-v1" receives 80% of the traffic while "app-v2" handles the remaining 20%. This declarative and controller-agnostic approach greatly simplifies advanced traffic management scenarios.

## Centralized Advanced Configuration

For features like Cross-Origin Resource Sharing (CORS), the Gateway API centralizes configurations without relying on controller-specific annotations. Consider the following Gateway API-based CORS configuration:

```yaml theme={null}
# http-route-cors.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: cors-route
spec:
  parentRefs:
    - name: my-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      filters:
        - type: ResponseHeaderModifier
          responseHeaderModifier:
            add:
              - name: Access-Control-Allow-Origin
                value: "*"
              - name: Access-Control-Allow-Methods
                value: "GET, POST, PUT, DELETE, OPTIONS"
              - name: Access-Control-Allow-Headers
                value: "Content-Type,Authorization"
              - name: Access-Control-Allow-Credentials
                value: "true"
              - name: Access-Control-Max-Age
                value: "3600"
  backendRefs:
    - name: api-service
```

This self-contained configuration is consistent and works seamlessly across different Gateway API controllers.

## Gateway API Controller Support

A range of major controllers now support, or are actively implementing, the Gateway API. This industry support includes platforms such as Amazon EKS, Azure Application Gateway for Containers, Contour, Envoy, Google Kubernetes Engine, HAProxy, Istio, Kong, Kuma, NGINX, and many others. Such broad adoption underlines the growing momentum and reliability of the Gateway API.

![The image is a table describing different Gateway API objects, their OSI layers, routing discriminators, TLS support, and purposes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869853/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Introduction-to-Gateway-API-2025-Updates/gateway-api-objects-table.jpg)

![The image lists various gateway controller implementations along with their status, such as GA (General Availability), beta, alpha, tech preview, and work in progress.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869854/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Introduction-to-Gateway-API-2025-Updates/gateway-controllers-status-list.jpg)

## Conclusion

The Gateway API overcomes the limitations of Ingress by providing a more declarative, structured, and multi-protocol solution for traffic management. By segregating responsibilities among GatewayClass, Gateway, and HTTPRoute, it simplifies multi-tenant management and advanced routing scenarios such as TLS termination, traffic splitting, and CORS configuration.

> **lightbulb** For a deeper understanding of these concepts, try practicing with hands-on labs to experiment with different Gateway API configurations.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/44bc9a9f-319c-40ee-babd-0f7b53a70de7/lesson/9b8ec47d-505f-4107-a5bf-1d629f5da5b4)


# Networking Introduction

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Networking/Networking-Introduction/page

Overview of Kubernetes networking fundamentals including pod IP addressing, CNI plugins, services, Cluster DNS, load balancing, ingress, and troubleshooting.

Hello, and welcome to this section on Kubernetes networking. My name is Mumshad Mannambeth. This lesson covers the core networking concepts you need to design, operate, and troubleshoot Kubernetes clusters.

A solid understanding of a few foundational networking topics will help you get the most from this section. Before diving into cluster-specific details, make sure you are comfortable with:

* Configuring network interfaces and IP addresses
* Gateways and routing basics
* Name resolution and DNS fundamentals
* DNS configuration on Linux systems
* CoreDNS basics
* Network namespaces and how container runtimes (for example Docker) use them

> **lightbulb** These short prerequisite lectures are optional but recommended. If you already know these basics, skip what you don't need — but review network namespaces and Docker networking if you haven't, since they directly affect how pods and containers are isolated and connected.

<Frame>
  <img alt="A presentation slide titled &#x22;Networking&#x22; showing a vertical list of seven prerequisite topics (Switching and Routing, CoreDNS, Tools, DNS, CNI, Networking in Docker, and Networking Configuration on Cluster Nodes). A presenter stands to the right, gesturing while speaking." />
</Frame>

Why these prerequisites matter

* Network namespaces define per-process network stacks used by container runtimes; understanding them makes pod isolation and container networking much clearer.
* Gateways, routes, and interface configuration are essential when diagnosing connectivity problems between nodes, pods, and external services.
* DNS and CoreDNS are central to Kubernetes service discovery — misconfiguration here is a common source of application failures.

Learning sequence (what we’ll cover)
To provide a clear learning path, this lesson follows an ordered sequence that builds from cluster-level requirements to higher-level routing and ingress patterns:

1. Cluster networking needs — what Kubernetes expects from the network
2. Pod networking concepts — IP addressing, isolation, and reachability for pods
3. CNI in Kubernetes — how Container Network Interface plugins provide pod networking
4. Service networking — ClusterIP, NodePort, and stable endpoints for applications
5. Cluster DNS — how Kubernetes implements DNS (CoreDNS) for service discovery
6. Network load balancers — external access patterns and load balancing options
7. Ingress and Gateway API — HTTP routing and the newer Gateway API for advanced ingress

<Frame>
  <img alt="A presentation slide titled &#x22;Networking&#x22; shows a vertical timeline of topics (POD Networking Concepts; CNI in Kubernetes; Service Networking; Cluster DNS; Network Load Balancer; Ingress; Gateway API). On the right, a presenter in a dark sweater with red stripes gestures while speaking against a white background." />
</Frame>

What you’ll gain from this lesson

* A mental model of how Kubernetes connects pods, services, and external clients.
* Practical knowledge of CNI plugins and how they affect pod IP allocation and routing.
* Familiarity with Service types (ClusterIP, NodePort, LoadBalancer), when to use each, and common troubleshooting steps.
* Understanding of Cluster DNS (CoreDNS) patterns for service discovery and name resolution.
* An overview of ingress patterns, load balancers, and the Gateway API for modern HTTP routing.

Quick reference — concepts and resources

| Concept               | Purpose                                                  | Where to start                           |
| --------------------- | -------------------------------------------------------- | ---------------------------------------- |
| Pod networking        | IP addressing and connectivity between containers        | Pod CIDR, network namespaces             |
| CNI                   | Plugin model for providing pod network connectivity      | CNI plugins (Calico, Flannel, Cilium)    |
| Service types         | Stable access to pods: ClusterIP, NodePort, LoadBalancer | `kubectl get svc` and Service spec       |
| Cluster DNS           | Service discovery via CoreDNS                            | CoreDNS ConfigMap and `kube-dns`         |
| Ingress / Gateway API | HTTP routing and advanced ingress features               | Ingress controllers; Gateway API docs    |
| Network namespaces    | Process-level networking isolation                       | `ip netns`, container runtime networking |

Further reading and references

* Kubernetes Networking Concepts: [https://kubernetes.io/docs/concepts/cluster-administration/networking/](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* CoreDNS: [https://coredns.io/](https://coredns.io/)
* CNI (Container Network Interface): [https://github.com/containernetworking/cni](https://github.com/containernetworking/cni)
* Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* Ingress and Gateway API: [https://kubernetes.io/docs/concepts/services-networking/ingress/](https://kubernetes.io/docs/concepts/services-networking/ingress/) and [https://gateway-api.sigs.k8s.io/](https://gateway-api.sigs.k8s.io/)

By the end of this lesson you should be able to reason about IP addressing and routing inside a cluster, choose appropriate CNI and Service types for common application topologies, and troubleshoot common DNS and ingress-related networking issues.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/44bc9a9f-319c-40ee-babd-0f7b53a70de7/lesson/a9551c0c-5853-4e55-844a-df2d193100a2)
