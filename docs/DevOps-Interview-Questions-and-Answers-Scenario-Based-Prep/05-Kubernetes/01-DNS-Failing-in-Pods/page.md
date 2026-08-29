# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
```

Apply the manifest to the cluster:

```bash theme={null}
kubectl apply -f deployment.yaml
```

After applying, Kubernetes will ensure three running pods that match your Deployment. If a node fails and a pod is lost, controllers detect the discrepancy and create another pod to restore the declared state. You declare the desired state; Kubernetes continuously works to reach and maintain it.

The control plane — the brain of Kubernetes

Several components together form the control plane. They coordinate to accept your desired state, store it, and reconcile the actual cluster state with that desired state.

<Frame>
  <img alt="The image illustrates a Kubernetes control plane diagram with components like the API server, etcd, and controllers, organized in a triangle, with the title &#x22;The control plane&#x22; and stick figures labeled &#x22;INTERVIEWER&#x22; and &#x22;CANDIDATE.&#x22;" />
</Frame>

* API server: the front door for all requests and the primary interface for components and users. Every command and component talks to the API server.
* etcd: the distributed key-value store where Kubernetes persists cluster state (both desired and observed).
* Controllers: control loops that continuously compare desired state vs. actual state and take actions to reconcile them.
* Scheduler: assigns pods to appropriate nodes based on resource needs, affinity/anti-affinity, taints/tolerations, and other constraints.
* Kubelet: the node agent that ensures containers for assigned pods are running on a specific node.

Quick reference table

| Component   | Primary role             | Responsibilities                                                              |
| ----------- | ------------------------ | ----------------------------------------------------------------------------- |
| API server  | Cluster frontend         | Accepts RESTful requests, validates & persists objects                        |
| `etcd`      | Cluster storage          | Stores desired and observed cluster state                                     |
| Controllers | Reconciliation loops     | Watch API state and create/update/delete resources to match the desired state |
| Scheduler   | Placement decision maker | Chooses the best node for unscheduled pods                                    |
| Kubelet     | Node agent               | Starts containers, configures networking, and reports status                  |

etcd stores both:

* the desired state you submit (for example, the `Deployment` with `replicas: 3`), and
* the current observed state of the cluster.

<Callout icon="lightbulb">
  Controllers are declarative reconcilers: they continuously observe API state and make changes until the cluster matches the desired specification.
</Callout>

Scheduling: how Kubernetes picks a node

<Frame>
  <img alt="The image is a diagram illustrating a scheduling system with components like ETCD, scheduler, and controllers, and it shows nodes with different memory capacities where Node B is labeled as &#x22;too small.&#x22;" />
</Frame>

When a pod is created, it initially exists in the API server in an unscheduled state (no `nodeName` set). The scheduler watches for unscheduled pods and processes each in two main phases:

1. Filter (pre-score): Exclude nodes that cannot run the pod. Filters include:
   * Insufficient CPU/memory or other resource constraints
   * Taints on nodes that the pod does not tolerate
   * Node selectors, node affinity, or other constraints
2. Score (prioritize): Rank the remaining nodes using scoring rules — for example, packing vs. balanced placement, affinity/anti-affinity, or custom scoring plugins — and pick the best fit.

Once a node is chosen, the scheduler writes the chosen node’s name into the PodSpec via the API server. The scheduler decides placement only; it does not start containers.

Kubelet: making scheduling decisions real on a node

<Frame>
  <img alt="The image illustrates a Kubernetes setup with two nodes, showing pod IPs and kubelet processes, alongside an interviewer and candidate represented by stick figures." />
</Frame>

When a pod becomes assigned to a node, the kubelet on that node notices the new PodSpec via the API server. The kubelet:

* Pulls container images using the container runtime (for example, `containerd`).
* Starts and supervises containers for the pod.
* Configures pod networking and mounts volumes.
* Periodically reports pod and node status back to the API server.

Together: the control loop

The core control loop of Kubernetes can be summarized as:

1. You declare the desired state (create a Deployment, Service, etc.).
2. The API server stores the spec in `etcd`.
3. Controllers and the scheduler watch the API, compare desired vs actual state, and take actions (create pods, assign nodes).
4. Kubelets on nodes execute the runtime actions to realize the desired state and report status.
5. Controllers continue reconciling until the actual state matches the desired state.

Further reading and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [kube-scheduler concept](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)
* [kubelet documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
* [etcd documentation](https://etcd.io/docs/)

This overview is a compact refresher ideal for interview prep: explain the desired-state model, name the core control plane components, and describe the scheduler + kubelet flow end-to-end.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/b171f2a5-552f-44a7-a82e-e1770f1f9b53/lesson/630beed8-ec79-4817-b586-3f31a1584993" />
</CardGroup>


# DNS Failing in Pods

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Kubernetes/DNS-Failing-in-Pods/page

Guide to diagnosing and troubleshooting DNS resolution failures in Kubernetes pods with lookup flows, debugging steps, example outputs, and a concise troubleshooting checklist.

A common Kubernetes interview and on-call scenario: a pod cannot resolve DNS names. This guide walks through why DNS is critical in Kubernetes, how DNS lookups flow, quick debugging steps, example outputs, and a concise troubleshooting checklist to help you find the root cause quickly.

Why DNS matters in Kubernetes

* Pods and Services in Kubernetes rarely rely on fixed IPs; they use DNS names because the cluster is dynamic—pods are recreated and IPs change.
* When a pod needs to contact another service or external host, it asks the cluster DNS (CoreDNS) to translate a human-readable name into an IP address. If DNS fails, service discovery and inter-pod communication break.

<Frame>
  <img alt="The image illustrates a cluster scenario where an &#x22;orders pod&#x22; with IP 10.0.4.7 is removed and replaced by a new &#x22;orders pod&#x22; with IP 10.0.9.2, highlighting the role of DNS in managing these changes." />
</Frame>

How a DNS lookup flows in Kubernetes

* A pod reads `/etc/resolv.conf` to determine which nameserver to query.
* Typically the configured nameserver is the `kube-dns` Service ClusterIP (for example, `10.96.0.10`), which forwards the query to a CoreDNS pod.
* CoreDNS resolves Kubernetes-internal names (for example, `kubernetes.default.svc.cluster.local`) and forwards external queries to upstream resolvers for internet names.

<Frame>
  <img alt="The image illustrates the DNS lookup path in a Kubernetes cluster, showing the flow from a client pod through the kube-dns service and CoreDNS, with forwarding to an upstream DNS on the internet." />
</Frame>

Quick debugging tip — two lookups to isolate the problem
From inside the failing pod, run two DNS lookups:

1. `kubernetes.default` — verifies cluster-internal DNS (the Kubernetes API Service always exists and should resolve through cluster DNS).
2. `google.com` — verifies external resolution / DNS forwarding to upstream servers.

<Callout icon="lightbulb">
  Run these lookups from inside the failing pod. For example, open a shell into the pod and run nslookup:

  * `kubectl exec -it <pod> -- sh` (then run nslookup inside the shell), or
  * `kubectl exec -it <pod> -- nslookup <name>` (if nslookup is available in the image).

  If the pod image lacks DNS utilities, run a temporary debug pod that includes them:

  * `kubectl run -i --tty --rm debug --image=nicolaka/netshoot -- /bin/bash`
    or use a lightweight image such as busybox that includes basic DNS tools.
</Callout>

Example lookups

```bash theme={null}
$ nslookup kubernetes.default
Server:         10.96.0.10
Name:           kubernetes.default.svc.cluster.local
Address:        10.96.0.1

$ nslookup google.com
Server:         10.96.0.10
Name:           google.com
Address:        142.250.4.100
```

Interpreting results — mapping symptoms to next checks

* Both lookups fail
  * Symptom: Pod cannot reach cluster DNS at all.
  * Likely causes: CoreDNS pods down, `kube-dns` Service missing, network policy/firewall blocking DNS, or incorrect `/etc/resolv.conf`.
  * Next checks: CoreDNS pod health/logs, `kube-dns` Service & endpoints, pod `resolv.conf`, cluster network rules.

* `kubernetes.default` succeeds, `google.com` fails
  * Symptom: Cluster DNS resolves internal names but cannot forward external queries.
  * Likely causes: CoreDNS forwarding misconfigured, upstream resolvers unreachable, firewall blocking outbound DNS.
  * Next checks: CoreDNS `Corefile`, upstream resolvers, node egress access.

* `kubernetes.default` fails, `google.com` succeeds
  * Symptom: The pod reaches some DNS server but not the cluster DNS.
  * Likely causes: Pod uses node or external resolver instead of `kube-dns`, `dnsPolicy` overridden in pod spec, or `resolv.conf` has wrong nameserver.
  * Next checks: Inspect `/etc/resolv.conf` inside pod, check pod spec `dnsPolicy` and `dnsConfig`, validate node-level DNS settings.

* Both succeed but DNS is slow
  * Symptom: Resolution works but with high latency.
  * Likely causes: CoreDNS overloaded, too many queries, or slow upstream resolvers.
  * Next checks: CoreDNS metrics/CPU/memory, rate-limiting, caching, or upstream performance.

Troubleshooting checklist and commands

* Check pod resolv.conf:
  * `kubectl exec -it <pod> -- cat /etc/resolv.conf`
* Check CoreDNS pods and logs:
  * `kubectl -n kube-system get pods -l k8s-app=kube-dns`
  * (Some clusters use `k8s-app=coredns`) `kubectl -n kube-system logs <coredns-pod>`
* Verify `kube-dns` Service and endpoints:
  * `kubectl -n kube-system get svc kube-dns -o yaml`
  * `kubectl -n kube-system get endpoints kube-dns -o yaml`
* Run DNS lookups from a debug pod:
  * `kubectl run -i --tty --rm debug --image=nicolaka/netshoot -- /bin/bash`
  * From inside: `nslookup kubernetes.default` and `nslookup google.com`
* Inspect network policies / iptables / kube-proxy if DNS requests are being dropped or redirected:
  * `iptables -t nat -L -n -v` (run on affected node) — trace kube-proxy rules if necessary.

Table: Common DNS failure modes and checks

| Symptom                                 | Probable cause                                         | Quick checks & commands                                                                                     |
| --------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| No DNS at all (timeouts)                | CoreDNS crashed, Service missing, network blocking DNS | `kubectl -n kube-system get pods -l k8s-app=kube-dns` <br /> `kubectl -n kube-system describe svc kube-dns` |
| Internal names resolve, external do not | CoreDNS forwarding to upstream broken                  | Check CoreDNS `Corefile` and upstream servers: `kubectl -n kube-system describe configmap coredns`          |
| External resolves, internal does not    | Pod not using cluster DNS                              | `kubectl exec -it <pod> -- cat /etc/resolv.conf` <br /> Check pod `dnsPolicy` in spec                       |
| Intermittent or slow resolution         | Resource exhaustion or upstream slowness               | `kubectl -n kube-system top pod` (CoreDNS) <br /> Check CoreDNS logs and metrics                            |

Watch for specific error responses

* "no such host" — CoreDNS returned NXDOMAIN; the name truly doesn't exist in the queried domain.
* Timeout — the pod never reached the DNS server (network or nameserver misconfiguration).

<Frame>
  <img alt="The image is a troubleshooting guide for DNS issues in Kubernetes, illustrating different scenarios of DNS failures and their possible causes. It uses color-coded boxes to indicate whether the Kubernetes (k8s) and web components are OK or FAIL." />
</Frame>

Further diagnostic steps and tracing

* Trace requests through iptables/kube-proxy if DNS packets are being redirected or dropped.
* Use CoreDNS logs to inspect failed queries and forwarding errors:
  * `kubectl -n kube-system logs <coredns-pod>`
* If DNS appears to work but service discovery fails, trace connection paths from the client pod to the target service IP and check kube-proxy rules, service endpoints, and target pod readiness.

<Callout icon="warning">
  Be cautious when editing cluster DNS settings. Incorrect changes to CoreDNS `ConfigMap` or Service cluster IPs can disrupt all name resolution in the cluster. Always test changes in a staging environment and keep backups of configuration before editing.
</Callout>

Useful links and references

* [Kubernetes DNS concepts](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* [CoreDNS documentation](https://coredns.io/)
* [Troubleshooting DNS in Kubernetes (guide)](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)

Summary
Two quick lookups—one for a known internal name (`kubernetes.default`) and one for an internet name (`google.com`)—rapidly pinpoint whether the problem is cluster DNS, forwarding, or pod-level configuration. From there, inspect `/etc/resolv.conf`, CoreDNS pods and ConfigMap, `kube-dns` Service and endpoints, and any network rules that could interfere with DNS traffic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/60905e58-3a8e-4423-9743-081b4959f0a0/lesson/1a546aeb-c666-40de-bede-002633ff51ca" />
</CardGroup>
