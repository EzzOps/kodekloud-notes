# Demo Cilium Network Policy Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Network-Policy/Demo-Cilium-Network-Policy-Part-1/page

Demonstrates creating and testing L3 Cilium network policies to control namespace-scoped ingress and egress, including cross-namespace rules, CIDR egress, and default deny behaviors.

In this lesson we'll demonstrate how to create and test L3 (IP/label-based) Cilium network policies. Examples cover common scenarios: namespace scoping, allowing/denying ingress and egress, matching multiple namespaces, and CIDR-based egress.

<Frame>
  <img alt="A presentation slide showing the word &#x22;Demo&#x22; on the left and a teal graphic on the right that reads &#x22;Cilium Network Policy Part 1.&#x22; A small copyright notice for KodeKloud appears in the bottom-left corner." />
</Frame>

Overview

* Goal: Apply an L3 ingress policy to the app1 pod in the dev namespace so only pods with label app=app2 (in specific namespaces) can talk to app1.
* Test image: nicolaka/netshoot (contains telnet, curl, and other troubleshooting tools).
* Environment: three namespaces (dev, prod, staging), each with app1, app2, app3.

Useful links

* Cilium Network Policy docs: [https://docs.cilium.io/en/stable/policy/](https://docs.cilium.io/en/stable/policy/)
* netshoot image: [https://hub.docker.com/r/nicolaka/netshoot](https://hub.docker.com/r/nicolaka/netshoot)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

Environment: example deployment
Use one Deployment per app (adjust name/namespace/labels accordingly). Example manifest for app1 in dev:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1
  namespace: dev
  labels:
    app: app1-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
      - name: app1
        image: nicolaka/netshoot
        command: ["sleep", "999999"]
```

Repeat the same pattern for app2 and app3 in dev, and similarly for prod and staging.

Verify cluster namespaces and pods

* Check namespaces:

```bash theme={null}
kubectl get ns
NAME                   STATUS    AGE
cilium-secrets         Active    34m
default                Active    36m
dev                    Active    31m
kube-node-lease        Active    36m
kube-public            Active    36m
kube-system            Active    36m
local-path-storage     Active    36m
prod                   Active    31m
staging                Active    32m
```

* List all pods (excluding kube-system) to view IPs and nodes:

```bash theme={null}
kubectl get pod -A -o wide | grep -iv kube-system
NAMESPACE   NAME                                 READY   STATUS    RESTARTS   AGE   IP           NODE
dev         app1-75c78488c4-rzf48                1/1     Running   0          31m   10.0.2.88    my-cluster-worker
dev         app2-5957957d5b-kgkt6                1/1     Running   0          31m   10.0.2.89    my-cluster-worker
dev         app3-87d98dbbb-k6xzk                 1/1     Running   0          31m   10.0.2.26    my-cluster-worker
prod        app1-75c78488c4-2v5jp                1/1     Running   0          31m   10.0.0.76    my-cluster-worker2
prod        app2-5957957d5b-lkwt6                1/1     Running   0          31m   10.0.2.70    my-cluster-worker
prod        app3-87d98dbbb-ldkfl                 1/1     Running   0          31m   10.0.0.50    my-cluster-worker2
staging     app1-75c78488c4-6kptd                1/1     Running   0          31m   10.0.2.122   my-cluster-worker
staging     app2-5957957d5b-lzn4j                1/1     Running   0          31m   10.0.0.93    my-cluster-worker2
staging     app3-87d98dbbb-5fwjw                 1/1     Running   0          31m   10.0.2.136   my-cluster-worker
```

* Check labels in the dev namespace:

```bash theme={null}
kubectl get pod -n dev --show-labels
NAME                        READY   STATUS    RESTARTS   AGE   LABELS
app1-75c78488c4-rzf48       1/1     Running   0          39m   app=app1,pod-template-hash=75c78488c4
app2-5957957d5b-kgkt6       1/1     Running   0          39m   app=app2,pod-template-hash=5957957d5b
app3-87d98dbbb-k6xzk        1/1     Running   0          39m   app=app3,pod-template-hash=87d98dbbb
```

Connectivity testing with telnet

* Exec into a pod and use telnet to test TCP connectivity.
* Two possible outcomes to interpret:
  * "Connection refused" — the TCP SYN reached the destination pod (no process listening on that port). This confirms network reachability.
  * Telnet hangs without response — the packet was likely dropped before reaching the pod (network reachability blocked).

> **lightbulb** Telnet note: "Connection refused" means the traffic reached the destination pod (but no process is listening on that port). A hanging telnet indicates the traffic was blocked or dropped.

Example telnet test

```bash theme={null}
