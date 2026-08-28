# NAME             TYPE        CLUSTER-IP       PORT(S)     AGE
# devsecops-svc    ClusterIP   10.101.121.127   8080/TCP    4d3h
# node-service     ClusterIP   10.101.46.231    5000/TCP    4d5h
```

Internally it responds as expected:

```bash theme={null}
while true; do
  curl -s 10.101.121.127:8080/increment/99
  sleep 1
done
```

### Create Gateway + VirtualService for `prod`

Create both resources in a single manifest (`istio-gateway-vs.yaml`):

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: devsecops-gateway
  namespace: prod
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      name: http
      number: 80
      protocol: HTTP
    hosts:
    - "*"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: devsecops-numeric
  namespace: prod
spec:
  gateways:
  - devsecops-gateway
  hosts:
  - "*"
  http:
  - match:
    - uri:
        prefix: /increment
    - uri:
        exact: /
    route:
    - destination:
        host: devsecops-svc
        port:
          number: 8080
```

Apply and verify:

```bash theme={null}
kubectl apply -f istio-gateway-vs.yaml
kubectl get gateway,virtualservice -n prod
```

## Access via Istio Ingress Gateway

Istio’s `istio-ingressgateway` Service is typically a LoadBalancer or NodePort. In this environment it’s exposed on NodePort **32564**:

```bash theme={null}
kubectl -n istio-system get svc istio-ingressgateway
# NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# istio-ingressgateway   NodePort   10.96.123.45    <none>        80:32564/TCP     2h
```

Test external access:

```bash theme={null}
curl localhost:32564/
curl localhost:32564/increment/11
# 12
```

Both `/` and `/increment` are reachable through the Gateway.

## Restricting Paths with VirtualService

To disable the root path (`/`) externally, remove or comment out the exact-match rule:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: devsecops-numeric
  namespace: prod
spec:
  gateways:
  - devsecops-gateway
  hosts:
  - "*"
  http:
  - match:
    - uri:
        prefix: /increment
    # - uri:
    #     exact: /
    route:
    - destination:
        host: devsecops-svc
        port:
          number: 8080
```

Apply and test again:

```bash theme={null}
kubectl apply -f istio-gateway-vs.yaml
curl localhost:32564/                # no response
curl localhost:32564/increment/11    # returns 12
```

## Viewing Configuration in Kiali

Kiali provides a UI for inspecting Istio resources.

<Frame>
  ![The image shows a Kiali dashboard displaying Istio configuration for a namespace "prod," listing a Gateway and a VirtualService with their configurations.](https://kodekloud.com/kk-media/image/upload/v1752873746/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-Ingress-Gateway-and-Virtual-Service/kiali-dashboard-istio-configuration-prod.jpg)
</Frame>

You can also view your service mesh topology:

<Frame>
  ![The image shows a Kiali dashboard displaying a service mesh graph with nodes representing services and their interactions within a Kubernetes environment. The graph includes services like "devsecops-svc" and "node-service" with connections indicating data flow.](https://kodekloud.com/kk-media/image/upload/v1752873748/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-Ingress-Gateway-and-Virtual-Service/kiali-dashboard-service-mesh-graph.jpg)
</Frame>

And inspect metrics & traffic:

<Frame>
  ![The image shows a Kiali dashboard displaying a service mesh graph with nodes representing services and their interactions, including "devsecops-svc" and "node-service." The graph is set to show response time and other metrics within a specified namespace.](https://kodekloud.com/kk-media/image/upload/v1752873749/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-Ingress-Gateway-and-Virtual-Service/kiali-dashboard-service-mesh-graph-2.jpg)
</Frame>

## Summary

| Resource       | Purpose                                | Example Snippet                            |
| -------------- | -------------------------------------- | ------------------------------------------ |
| Gateway        | Configure edge load balancer listeners | `selector: istio: ingressgateway`          |
| VirtualService | Define routing rules for HTTP/TCP      | `hosts: ["*"]`, `match: prefix /increment` |
| Kiali          | Visualize and troubleshoot mesh        | UI for Gateways, VirtualServices, metrics  |

## Links and References

* [Istio Gateway API][istio-gateway]
* [Istio VirtualService API][istio-virtualservice]
* [Kiali Documentation](https://www.kiali.io/documentation/)

[istio-gateway]: https://istio.io[AWS_SECRET_ACCESS_KEY]/gateway/

[istio-virtualservice]: https://istio.io[AWS_SECRET_ACCESS_KEY]/virtual-service/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/5989174f-a567-4767-af9c-4d614153c883" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/ee9e210b-61c4-4b60-9049-7bc4d0012108" />
</CardGroup>


# Demo Istio Injecting SideCar Container

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Istio-Injecting-SideCar-Container/page

This guide explains how to automatically inject an Envoy sidecar into a Kubernetes pod for traffic management and telemetry using Istio.

## Introduction

Istio sidecar injection embeds an Envoy proxy alongside your application container to enable advanced traffic management, mutual TLS, and telemetry within Kubernetes. In this guide, you’ll learn how to:

* Inject an Envoy sidecar into a pod automatically
* Deploy a Node.js microservice in a dedicated namespace
* Verify the injected sidecar and inspect traffic flows

Sidecar proxy is also known as a sidecar container, proxy sidecar, or Envoy sidecar—these terms are used interchangeably.

## Sidecar Injection Methods

Istio offers two approaches to inject the Envoy proxy into your workloads:

| Method              | Description                                                                         | Commands                                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Automatic Injection | Labels a namespace so that any new pod includes the sidecar via a mutating webhook. | `bash<br>kubectl label namespace <name> istio-injection=enabled<br>kubectl apply -f movies.yaml` |
| Manual Injection    | Injects proxy settings directly into your YAML before applying with `istioctl`.     | `bash<br>kubectl apply -f <(istioctl kube-inject -f movies.yaml)`                                |

<Callout icon="lightbulb">
  We’ll use **Automatic Injection** for this demo, since it requires no modifications to your application manifests.
</Callout>

## Istio Demo Architecture

<Frame>
  ![The image is a diagram of an Istio demo architecture on the Azure platform, showing the interaction between Kubernetes, microservices, Envoy, Apigee, and monitoring tools. It illustrates HTTP calls, API management, and traffic management within the system.](https://kodekloud.com/kk-media/image/upload/v1752873750/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-Injecting-SideCar-Container/istio-demo-architecture-azure-diagram.jpg)
</Frame>

| Component                   | Role                                                                  |
| --------------------------- | --------------------------------------------------------------------- |
| Azure VM Kubernetes Cluster | Hosts Istio control plane (Pilot, Citadel, Galley) and workloads      |
| Istio Sidecar (Envoy)       | Intercepts pod traffic for routing, mTLS, and telemetry               |
| Telemetry & Visualization   | Grafana, Prometheus, Kiali, Jaeger capture metrics and traces         |
| API Management (Optional)   | Apigee integration for API security, developer portals, and analytics |

## Prerequisites

* A Kubernetes cluster with Istio installed
* `kubectl` and `istioctl` CLI tools available
* Docker image `siddharth67/node-service:v1` pushed to a registry

## 1. Create and Label the `prod` Namespace

First, set a shorthand for `kubectl`:

```bash theme={null}
alias k=kubectl
```

List your namespaces:

```bash theme={null}
k get ns
```

Create `prod` and confirm:

```bash theme={null}
k create namespace prod
k get ns
```

## 2. Deploy the Node.js Service

Deploy the Node.js microservice with a single container initially:

```bash theme={null}
k -n prod create deployment node-app \
  --image=siddharth67/node-service:v1
```

Expose it as a ClusterIP service on port 5000:

```bash theme={null}
k -n prod expose deployment node-app \
  --name=node-service \
  --port=5000 \
  --target-port=5000 \
  --type=ClusterIP
```

Verify the resources:

```bash theme={null}
k get all -n prod
```

## 3. Enable Automatic Sidecar Injection

Inspect existing namespace labels:

```bash theme={null}
kubectl get ns --show-labels
```

Label `prod` for Istio:

```bash theme={null}
kubectl label namespace prod istio-injection=enabled
kubectl get ns --show-labels
```

<Callout icon="lightbulb">
  The `istio-system` namespace is generally labeled `istio-injection=disabled` to prevent sidecar injection into control plane components.
</Callout>

## 4. Restart the Deployment

Trigger pod recreation so the Envoy sidecar is injected:

```bash theme={null}
kubectl -n prod rollout restart deployment node-app
kubectl -n prod rollout status deployment/node-app
```

Confirm new pods show `2/2` READY:

```bash theme={null}
kubectl get pods -n prod
```

## 5. Verify the Sidecar Injection

Inspect one of the pods in detail:

```bash theme={null}
kubectl -n prod describe pod <pod-name>
```

Under **Containers:** you should see:

* `node-service` (your application)
* `istio-proxy` (Envoy sidecar, e.g., `docker.io/istio/proxyv2:1.9.0`)

List pods again:

```bash theme={null}
kubectl -n prod get pods
NAME                            READY   STATUS    RESTARTS   AGE
node-app-597c464649-lgs82       2/2     Running   0          100s
```

## Next Steps

You can extend this workflow by deploying additional services—such as a Spring Boot app via Jenkins Pipeline—or by customizing traffic routing with Istio VirtualServices and DestinationRules.

## Links and References

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
* [Grafana](https://grafana.com/) & [Prometheus](https://prometheus.io/) & [Kiali](https://kiali.io/) & [Jaeger](https://www.jaegertracing.io/)
* [Apigee on Google Cloud](https://cloud.google.com/apigee)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/c955f7a9-f289-4e8b-89b4-f6d7964ec75b" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/8ebe9001-3358-4027-b9c9-5b359cdfcdb9" />
</CardGroup>
