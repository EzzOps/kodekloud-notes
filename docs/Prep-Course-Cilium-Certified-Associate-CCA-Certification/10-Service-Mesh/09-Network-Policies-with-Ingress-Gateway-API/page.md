# values.yaml (excerpt)
# -- Configure L2 announcements (example section)
l2announcements:
  enabled: true

# -- Enable transparent network encryption.
enableXTSocketFallback: true
encryption:
  enabled: true
  # Encryption method: ipsec or wireguard
  type: ipsec

# -- Enable Non-Default-Deny policies
enableNonDefaultDenyPolicies: true

# Configuration for types of authentication for Cilium (beta)
authentication:
  # Enable authentication processing and garbage collection. When disabled,
  # policy enforcement will still block requests that require authentication
  # but authentication requests will not be processed.
  enabled: true
  queueSize: 1024

# Spire integration (for mTLS)
spire:
  enabled: true
```

> **warning** Spire must be reachable from Cilium agents for SPIFFE identity issuance and verification to succeed. Ensure network access, node selectors, tolerations, and resource constraints in your Helm values match your environment.

> **lightbulb** If you run a hardened cluster, adjust node selectors and tolerations for the Spire server and agents in the Helm values. Confirm the Cilium Helm chart version supports the spire integration for your Cilium release.

Install / upgrade Cilium with the updated values
Apply the updated Helm values to Cilium:

```bash theme={null}
helm upgrade cilium cilium/cilium -f values.yaml -n kube-system
```

Restart the operator and agent pods so the changed configuration takes effect:

```bash theme={null}
kubectl -n kube-system rollout restart deployment cilium-operator
kubectl -n kube-system rollout restart daemonset cilium
```

Enable debug logging for authentication troubleshooting
Enable Cilium debug logging to surface authentication events:

```bash theme={null}
# Using the Cilium CLI (if available)
cilium config set debug true
```

This updates the Cilium config, which will cause agent pods to restart and pick up debug logging.

Verify Spire and Cilium resources are running
Confirm that Spire and Cilium components are present and running:

```bash theme={null}
kubectl get pods -A
```

Representative output (trimmed):

```text theme={null}
NAMESPACE     NAME                                   READY   STATUS    AGE
cilium-spire  spire-agent-xxxxx                      1/1     Running   16m
cilium-spire  spire-server-0                         2/2     Running   16m
kube-system   cilium-xxxxx                           1/1     Running   16m
kube-system   cilium-envoy-xxxxx                    1/1     Running   16m
kube-system   cilium-operator-xxxxx                 1/1     Running   16m
```

Check services:

```bash theme={null}
kubectl get svc -A
```

Representative output:

```text theme={null}
NAMESPACE     NAME          TYPE        CLUSTER-IP      PORT(S)
cilium-spire  spire-server  ClusterIP   10.96.158.64    8081/TCP
kube-system   cilium-envoy  ClusterIP   None            9964/TCP
default       kubernetes    ClusterIP   10.96.0.1       443/TCP
```

Deploy a simple server and a client
Create an NGINX server and a client (netshoot) to test connectivity and authentication.

server-deployment-and-service.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: server
  template:
    metadata:
      labels:
        app: server
    spec:
      containers:
      - name: server
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: server-service
spec:
  selector:
    app: server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

client-deployment.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: client
  template:
    metadata:
      labels:
        app: client
    spec:
      # optional: schedule on a particular node if desired:
      # nodeName: my-cluster-worker
      containers:
      - name: client
        image: nicolaka/netshoot
        command: ["sleep", "999999"]
```

Apply the manifests:

```bash theme={null}
kubectl apply -f server-deployment-and-service.yaml
kubectl apply -f client-deployment.yaml
```

Wait until pods are Ready:

```bash theme={null}
kubectl get pods
```

Representative pod output:

````
text
```
NAME                          READY   STATUS    RESTARTS   AGE
client-xxxxx                  1/1     Running   0          12s
server-xxxxx                  1/1     Running   0          8s
```

Test connectivity from client to server
Exec into the client and curl the server service to verify connectivity before mTLS is enforced:

```bash
kubectl exec -it $(kubectl get pod -l app=client -o jsonpath='{.items[0].metadata.name}') -- bash

# inside client shell
curl server-service
```

You should see the NGINX default page, confirming connectivity.

Create a CiliumNetworkPolicy to allow ingress to the server
First create a policy that allows ingress to the server on port 80 (no authentication requirement yet):

policy.yaml

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: all-server
spec:
  endpointSelector:
    matchLabels:
      app: server
  ingress:
  - toPorts:
    - ports:
      - port: "80"
        protocol: TCP
```

Apply the policy:

```bash
kubectl apply -f policy.yaml
# Output:
# ciliumnetworkpolicy.cilium.io/all-server created
```

Connectivity should continue to work because the policy currently does not require authentication.

Require authentication (enable mTLS) in the policy
Update the policy to require authentication (mTLS) for the matched traffic:

policy-mtls.yaml

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: all-server
spec:
  endpointSelector:
    matchLabels:
      app: server
  ingress:
  - toPorts:
    - ports:
      - port: "80"
        protocol: TCP
    authentication:
      mode: required
```

Apply the updated policy:

```bash
kubectl apply -f policy-mtls.yaml
# Output:
# ciliumnetworkpolicy.cilium.io/all-server configured
```

Behavior on first authenticated connection attempt
When a policy requires authentication, the first packet that triggers authentication will be dropped while Cilium performs the authentication handshake via SPIRE. This is expected: Cilium will initiate the SPIRE-based authentication flow and, once identities are validated, subsequent packets for that connection are allowed. Expect a small delay on the first request.

Observe authentication activity in Cilium agent logs
To trace the authentication flow, tail the Cilium agent logs for the node hosting the server pod.

1. Find the server pod's node:

```bash
kubectl get pod -o wide -l app=server
```

2. Get the Cilium agent pod on that node (namespace kube-system) and tail logs, filtering for authentication messages:

```bash
kubectl -n kube-system -c cilium-agent logs <cilium-agent-pod> --timestamps=true -f | grep -E "Policy is requiring authentication|Validating Server SNI|Validated certificate|Successfully authenticated"
```

Example filtered output (representative):

```text
2025-06-05T01:19:09.316809494Z time=2025-06-05T01:19:09Z level=debug msg="Policy is requiring authentication" module=agent.controlplane.auth key="localIdentity=47107, remoteIdentity=35152, remoteNodeID=8555, authType=spire"
2025-06-05T01:19:09.321705678Z time=2025-06-05T01:19:09Z level=debug msg="Validating Server SNI" module=agent.controlplane.auth SNI_ID=35152
2025-06-05T01:19:09.321748394Z time=2025-06-05T01:19:09Z level=debug msg="Validated certificate" module=agent.controlplane.auth uri-san=[spiffe://spiffe.cilium/identity/35152]
2025-06-05T01:19:09.322644706Z time=2025-06-05T01:19:09Z level=debug msg="Successfully authenticated" module=agent.controlplane.auth key="localIdentity=47107, remoteIdentity=35152, remoteNodeID=8555, authType=spire" remote_node_ip=10.0.0.142
```

Authentication flow summary
- First packet is dropped when the policy requires authentication because the mTLS session has not yet been established.
- Cilium detects the required authentication and initiates a SPIRE-based handshake between source and destination workloads.
- The server SNI (Server Name Indication) is validated, SPIFFE identities are retrieved and validated.
- After validation, the agent logs a successful authentication and allows subsequent packets for that connection.

Checklist to enable mTLS in Cilium
1. Enable transparent encryption (ipsec or WireGuard) in Helm values.
2. Set authentication.enabled: true and enable spire: enabled in values.yaml.
3. Helm upgrade and restart Cilium components so configuration is applied.
4. Deploy workloads and create a CiliumNetworkPolicy that selects the target endpoints.
5. Add authentication.mode: required to the policy to enforce mTLS.
6. Enable debug logging and tail agent logs to validate the authentication handshake.

Links and references
- Cilium: https://cilium.io/
- SPIRE: https://spiffe.io/spire/
- SPIFFE: https://spiffe.io/
- CiliumNetworkPolicy reference: https://docs.cilium.io/en/stable/policy/language/
- cilium CLI: https://docs.cilium.io/en/stable/cilium_cli/

<Card title="Watch Video" icon="video" cta="Learn more" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/92e4dc74-6da6-42bf-8677-ae012ffdc3eb"/>
````


# Network Policies with Ingress Gateway API

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Service-Mesh/Network-Policies-with-Ingress-Gateway-API/page

Configuring Cilium network policies for ingress and Gateway API traffic, covering external to ingress and ingress to backend using reserved ingress identity and label scoped rules

In this lesson we explain how Kubernetes network policies interact with ingress controllers and the Gateway API (for example, Cilium's Gateway API implementation). There are two distinct enforcement points you must consider when traffic arrives via an ingress or Gateway:

1. External traffic entering the cluster and reaching the ingress/Gateway service (LoadBalancer or NodePort).
2. Traffic flowing from the ingress/Gateway proxy to backend pods inside the cluster.

Below are example Cilium policies and guidance for each enforcement point, plus recommended scoping patterns to follow for production deployments.

> **lightbulb** When designing policies, consider both the traffic source (external clients vs. the ingress/Gateway identity) and the intended targets (ingress controller pods vs. backend application pods). Scoping policies to specific pod labels is safer than using broad selectors like empty endpointSelector or global entities.

## Enforcement points at a glance

| Enforcement point              | What to allow                                                 | Typical Cilium object                                                                                 |
| ------------------------------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Outside → Ingress/Gateway      | Allow external world to reach ingress controller Service/Pods | CiliumClusterwideNetworkPolicy scoped to ingress labels                                               |
| Ingress/Gateway → Backend pods | Allow ingress/Gateway proxy identity to reach backend pods    | CiliumNetworkPolicy or CiliumClusterwideNetworkPolicy allowing reserved:ingress or ingress pod labels |

## 1) Allow external traffic into the cluster (to your ingress/Gateway)

If you have cluster-wide network restrictions in Cilium, external clients may be prevented from reaching your ingress Service (LoadBalancer/NodePort). A permissive cluster-wide policy that allows traffic from the outside world looks like this:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-external
spec:
  description: "Allow traffic from the outside world to ingress"
  endpointSelector: {}
  ingress:
  - fromEntities:
    - world
```

Notes:

* endpointSelector:  matches all endpoints in the cluster — this is very permissive and not recommended for production.
* Instead, scope the policy to only the ingress/Gateway pods using a label selector (recommended). For example, if your ingress pods use label app: ingress-controller:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-external-to-ingress
spec:
  description: "Allow external traffic from world to ingress controller pods only"
  endpointSelector:
    matchLabels:
      app: ingress-controller
  ingress:
  - fromEntities:
    - world
```

This ensures only ingress controller pods receive traffic from the Internet while other pods remain protected by default-deny or narrower policies.

## 2) Allowing ingress/Gateway to talk to backend pods

Ingress and Gateway API implementations are represented inside Cilium by a reserved identity. Cilium exposes the reserved:ingress identity for traffic originating from the ingress/Gateway proxy. Backend pods must permit traffic from that identity (or from the ingress pod labels) so the proxy can reach application endpoints.

A cluster-wide policy that allows egress from the reserved ingress identity into the cluster:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-ingress-egress
spec:
  description: "Allow all egress traffic from reserved:ingress identity to endpoints in the cluster"
  endpointSelector:
    matchExpressions:
    - key: reserved:ingress
      operator: Exists
  egress:
  - toEntities:
    - cluster
```

How this works:

* The endpointSelector selects endpoints that carry the reserved:ingress identity (this identifies the ingress/Gateway proxy within Cilium).
* The egress rule sends traffic to the entity cluster (all cluster endpoints). For tighter security, replace toEntities: cluster with endpointSelector-based destinations that match only your backend pods.

If your backend pods have their own CiliumNetworkPolicy protecting them, ensure those policies allow traffic from reserved:ingress or from the ingress-controller pod labels. Example allowing only the reserved identity:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-from-ingress
  namespace: my-app
spec:
  description: "Allow traffic from ingress/Gateway to backend"
  endpointSelector:
    matchLabels:
      app: my-backend
  ingress:
  - fromEndpoints:
    - matchExpressions:
      - key: reserved:ingress
        operator: Exists
```

Or allow from the ingress-controller pods using labels:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-from-ingress-controller
  namespace: my-app
spec:
  description: "Allow traffic from ingress controller pods to backend"
  endpointSelector:
    matchLabels:
      app: my-backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: ingress-controller
```

> **lightbulb** Use label-based selectors for least-privilege access. Entity-based allowances like world or cluster are useful for testing, but for production prefer policies that target specific ingress pod labels or backend labels to limit blast radius.

## Practical recommendations

* Prefer CiliumClusterwideNetworkPolicy scoped to ingress labels for allowing external traffic into ingress Services.
* Use reserved:ingress identity or ingress pod label selectors to permit the proxy to reach backend pods.
* Avoid global endpointSelector:  or broad entity allowances (world, cluster) unless you intentionally want cluster-wide access.
* Test policies incrementally: first allow connectivity, then tighten selectors to application-specific labels.

## Summary

* Two enforcement points when using ingress/Gateway API: (1) outside → ingress and (2) ingress → backend.
* Allow external traffic to reach the ingress Service, but scope that access to ingress pods via labels when possible.
* Allow the reserved ingress identity (reserved:ingress) or ingress pod labels to reach backend pods; ensure backend policies explicitly permit that traffic.
* Follow least-privilege practices: prefer label-based selectors and narrow rules in production.

## Links and references

* [Gateway API](https://gateway-api.sigs.k8s.io/)
* [Cilium Gateway API docs](https://docs.cilium.io/en/stable/gateway/)
* [Cilium documentation](https://cilium.io/)
* [Cilium policy language](https://docs.cilium.io/en/stable/policy/language/)
* [Cilium reserved identities](https://docs.cilium.io/en/stable/policy/reserved-identities/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/203dbdef-9a10-4c82-8f11-6058b6af7112)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/0560235c-c52b-4f56-a668-e779c30a55d6)
