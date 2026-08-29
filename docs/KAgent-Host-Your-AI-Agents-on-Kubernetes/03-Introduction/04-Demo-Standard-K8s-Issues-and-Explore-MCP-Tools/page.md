# Demo Standard K8s Issues and Explore MCP Tools

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Introduction/Demo-Standard-K8s-Issues-and-Explore-MCP-Tools/page

Hands-on lab demonstrating troubleshooting of Kubernetes service selector and HPA quota issues, comparing manual kubectl diagnostics with AI-assisted KAgent remediation.

Hello everyone — welcome to the first lab. In this hands-on lesson we will reproduce two common Kubernetes cluster issues, troubleshoot them manually, and then repeat the same analysis using KAgent (an AI-assisted Kubernetes agent). The goal is to show how correlating diagnostics (kubectl, events, metrics, quotas) leads to the root cause, and how AI can speed up discovery and remediation.

Task summary

|                                              Problem |    Namespace   | Symptom                                                                          |
| ---------------------------------------------------: | :------------: | :------------------------------------------------------------------------------- |
|              `order-api` Service not routing traffic |    `default`   | Service exists but has no endpoints; curl to NodePort fails                      |
| `inventory-service` HPA not scaling to `minReplicas` | `backend-apps` | HPA shows `minReplicas=3` but only 1 pod runs; events show pod creation failures |

<Callout icon="lightbulb">
  Follow a reproducible troubleshooting pattern: observe symptoms, gather cluster state ([AWS_SECRET_ACCESS_KEY]), link evidence to possible causes, and apply the smallest safe remediation. Use `kubectl` + events + metrics to avoid misdirection.
</Callout>

***

## Task 1 — Order API: Service exists but traffic not routed

Reproduce symptom:

1. From the host try the NodePort:

```bash theme={null}
curl http://localhost:30081
```

(Initially this will fail because the Service has no endpoints.)

2. Gather basic cluster state in the `default` namespace:

```bash theme={null}
kubectl get svc -n default
kubectl get pods -n default --show-labels
kubectl get endpoints -n default
```

You should see the `order-api` Service present but with empty endpoints. Inspect the Service manifest to check selectors:

```yaml theme={null}
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"order-api","namespace":"default"},"spec":{"ports":[{"nodePort":30081,"port":80,"targetPort":80}],"selector":{"app":"order-api","version":"v1"},"type":"NodePort"}}
  creationTimestamp: "2025-12-16T10:29:13Z"
  name: order-api
  namespace: default
spec:
  clusterIP: 10.43.187.240
  ports:
  - nodePort: 30081
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: order-api
    version: v1
  type: NodePort
```

Diagnosis:

* Running pods show label `app=order-api` but `version=v2` (pod template uses `v2`).
* The Service selector is `version=v1`. This selector mismatch means the Service selects no pods → no endpoints → traffic not routed.

Fix options:

* Edit the Service selector to match pods, or update the Deployment labels to match the Service.
* To change the Service selector to `v2` (example using `kubectl patch`):

```bash theme={null}
kubectl patch svc order-api -n default --type='json' -p='[{"op":"replace","path":"/spec/selector/version","value":"v2"}]'
```

* Alternatively, edit the Service interactively:

```bash theme={null}
kubectl edit svc order-api -n default
