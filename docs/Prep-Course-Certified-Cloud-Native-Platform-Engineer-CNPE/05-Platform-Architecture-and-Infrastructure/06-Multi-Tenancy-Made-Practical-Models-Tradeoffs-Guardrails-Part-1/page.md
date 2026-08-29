# controller pod
NAME                                           READY   STATUS    RESTARTS   AGE
ingress-nginx-controller-c47b845b-bpvxz       1/1     Running   0          10m

# controller service
NAME                         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
ingress-nginx-controller     NodePort       172.20.253.85   <none>        80:30080/TCP,443:30443/TCP
```

* In cloud environments the controller's Service is often type `LoadBalancer` with an external IP.
* In labs it may be `NodePort`, which exposes controller ports on the node(s).

All external traffic for this demo will enter via the Ingress controller service.

## 5) Create a second service — `api`

Create an `api` Deployment using HashiCorp's `http-echo` image to return a simple message. Use the `--command` flag to pass container arguments:

```bash theme={null}
kubectl create deployment api --image=hashicorp/http-echo --replicas=2 --command -- /http-echo -text="hello from kodekloud"
kubectl expose deployment api --port=5678 --target-port=5678 --name=api-svc
kubectl get svc api-svc
```

Example service:

```text theme={null}
NAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
api-svc   ClusterIP   172.20.211.200  <none>        5678/TCP
```

Verify API pods:

```bash theme={null}
kubectl get pods -l app=api
```

You can test the API service from within the cluster or with `kubectl port-forward` to confirm it returns the message.

## 6) Create an Ingress resource to route to both services

Create an Ingress manifest (for example `ingress.yaml`) that routes `/api` to `api-svc:5678` and `/` to `web-svc:80`. Example:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: platform-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-svc
                port:
                  number: 5678
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-svc
                port:
                  number: 80
```

Apply the Ingress:

```bash theme={null}
kubectl apply -f ingress.yaml
kubectl describe ingress platform-ingress
```

You should see the Ingress scheduled for sync by the nginx controller, and the two rules listed in the description.

## 7) Test routing via the ingress controller NodePort

Use the controller NodePort (for example `30080`) to test both routes:

* Root `/` should route to `web-svc` (NGINX welcome page).
* `/api` should route to `api-svc` and return the echo message.

Example commands:

```bash theme={null}
curl localhost:30080/
curl localhost:30080/api
```

Expected responses:

* `curl localhost:30080/` returns the NGINX welcome HTML.
* `curl localhost:30080/api` returns:

```text theme={null}
hello from kodekloud
```

This demonstrates a single external entry point (the Ingress controller) routing to different internal services based on request path, without changing the application pods themselves.

## 8) The three-layer relationship

Understand the three-layer architecture and responsibilities:

* Ingress: external routing, host/path matching, TLS termination (external entry point).
* Service: stable internal discovery and load balancing (virtual IP / DNS for a set of pods).
* Pod: the actual workload (ephemeral compute).

When debugging connectivity, walk the chain from outside in:

* Can't reach the app externally? Check the Ingress resource and the Ingress controller.
* Ingress appears fine but routing is wrong? Re-check the Ingress rules and annotations.
* Service has no endpoints? Verify pod labels/selectors and pod readiness.
* Pod-level issues? Inspect pod logs and readiness/liveness probes.

Comparison: Service types

| Service Type | Use Case                                       | Notes / Example                                           |
| ------------ | ---------------------------------------------- | --------------------------------------------------------- |
| ClusterIP    | Internal cluster access                        | `kubectl expose deploy web --port=80 --name=web-svc`      |
| NodePort     | External access for labs or single-node setups | Exposes port in `30000–32767` range; `80:30309/TCP`       |
| LoadBalancer | Cloud environments for external IPs            | Provisioned by cloud provider; recommended for production |

Troubleshooting checklist

| Symptom                  | Quick checks                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------------- |
| No external access       | Verify Ingress controller pods and service; confirm controller NodePort/LoadBalancer is accessible |
| Wrong backend served     | `kubectl describe ingress <name>` → verify rule paths and backend service names/ports              |
| Service has no endpoints | `kubectl describe svc <service>` → check `Endpoints`; ensure pods match Service selectors          |
| Pod errors               | `kubectl logs <pod>` and `kubectl describe pod <pod>`; check readiness/liveness probes             |

> **warning** Ingress resources require a running Ingress controller. Creating an Ingress without a controller will not provide routing traffic. In cloud environments you may get a LoadBalancer service automatically for the controller; in labs you often use NodePort.

## Links and references

* Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* Ingress and Ingress Controllers: [https://kubernetes.io/docs/concepts/services-networking/ingress/](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* nginx-ingress Controller: [https://kubernetes.github.io/ingress-nginx/](https://kubernetes.github.io/ingress-nginx/)
* Traefik Ingress Controller: [https://traefik.io/](https://traefik.io/)
* HashiCorp http-echo: [https://github.com/hashicorp/http-echo](https://github.com/hashicorp/http-echo)

This walkthrough shows how Services and Ingress work together to provide stable discovery and flexible external routing, enabling reliable communication even as pods come and go.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/1ed2dc1a-4ce9-4793-b1f3-a2c15035cfd8)


# Multi Tenancy Made Practical Models Tradeoffs Guardrails Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-Architecture-and-Infrastructure/Multi-Tenancy-Made-Practical-Models-Tradeoffs-Guardrails-Part-1/page

Guidance on multi-tenancy tradeoffs and practical guardrails for Kubernetes clusters including models, isolation mechanisms, and minimum controls like RBAC ResourceQuota and NetworkPolicies

Assuming a platform blueprint and appropriately sized resources, a critical question follows: what happens when multiple teams share the same infrastructure?

In this lesson you will learn how to compare multi-tenancy models, choose an appropriate model based on trust boundaries, implement namespace-level isolation using a guardrail stack, and understand what Kubernetes does and does not provide by default.

<Frame>
  <img alt="The image lists learning objectives related to multi-tenancy models, trust boundaries, namespace-level isolation, and Kubernetes behavior, organized in a colorful, vertical numbered format." />
</Frame>

## Why namespaces alone are not enough

Consider an example where four teams share one cluster and each team has its own namespace. It’s a common assumption that namespaces act as security boundaries—this is incorrect. By default, namespaces do not enforce security or resource boundaries between teams. Without guardrails, shared clusters are vulnerable to several common failure modes.

### Four common failure modes in a shared cluster

Failure mode 1 — secrets exposure:
If a developer runs the following command without RBAC restrictions, they may list secrets across namespaces:

```bash theme={null}
kubectl get secrets --all-namespaces
```

This can expose database credentials, API keys, and TLS private keys for every team. Without properly configured RBAC, there is no secret isolation between namespaces.

> **warning** Secrets and credential leakage is one of the highest-risk outcomes in shared clusters. Ensure RBAC and least-privilege access are configured before allowing broad `kubectl` access.

Failure mode 2 — resource exhaustion:
If no ResourceQuota is configured, a single team can scale a workload to hundreds of replicas and consume cluster CPU and memory. Other teams’ pods may remain in Pending due to lack of capacity.

<Frame>
  <img alt="The image lists four failure modes: Secrets Exposure, Resource Exhaustion, Accidental Deletion, and Network Segmentation, with highlighted implications of Resource Exhaustion due to lack of ResourceQuota configuration." />
</Frame>

Impact: cluster instability, unfair resource usage, and operational disruption.

Failure mode 3 — accidental deletion:
A developer intends to delete a deployment in Team A's namespace but runs the kubectl command against the wrong namespace. For example:

```bash theme={null}
