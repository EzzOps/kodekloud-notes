# Helm values excerpt (values.yaml)
relay:
  # Enable Hubble Relay (requires hubble.enabled=true)
  enabled: true
  # Roll out Hubble Relay pods automatically when configmap is updated.
  rollOutPods: false
ui:
  # Whether to enable the Hubble UI.
  enabled: true
  standalone:
    # When true, allow installing the Hubble UI only, without checking dependencies.
    enabled: false
```

> **warning** After updating Helm values you must upgrade the release and restart the operator/agents so the new components are started and configuration is picked up.

Upgrade and restart:

```bash theme={null}
helm upgrade cilium cilium/cilium -f values.yaml -n kube-system

kubectl -n kube-system rollout restart deployment/cilium-operator
kubectl -n kube-system rollout restart daemonset/cilium
```

## 3. Verify Hubble components are running

List pods and services in the `kube-system` namespace:

```bash theme={null}
kubectl get pods -n kube-system
```

Example (relevant lines):

```text theme={null}
hubble-relay-59cc4d545b-g6g9v    1/1     Running   0          87s
hubble-ui-76d4965bb6-s8f6r       2/2     Running   0          87s
```

```bash theme={null}
kubectl get svc -n kube-system
```

Example:

```text theme={null}
NAME          TYPE        CLUSTER-IP      PORT(S)
hubble-relay  ClusterIP   10.96.71.111    80/TCP
hubble-ui     ClusterIP   10.96.213.213   80/TCP
```

You can also check status with the Cilium CLI:

```bash theme={null}
cilium status
```

Example (abridged):

```text theme={null}
Cilium:              OK
Operator:            OK
Envoy DaemonSet:     OK
Hubble Relay:        OK

Deployment        hubble-relay   Desired: 1, Ready: 1/1, Available: 1/1
Deployment        hubble-ui      Desired: 1, Ready: 1/1, Available: 1/1
```

<Frame>
  <img alt="A Visual Studio Code window with the Explorer open on the left and an integrated terminal on the right displaying Cilium cluster status (ClusterMesh: disabled), pod/container counts and image versions. The sidebar shows several YAML files and a remote SSH session indicator." />
</Frame>

## 4. Deploy sample applications (generate traffic)

In this demo we use four simple services: `ecom-auth`, `ecom-inventory`, `ecom-products`, and `ecom-user`. From the `hubble/` sample folder:

```bash theme={null}
cd hubble/
kubectl apply -f .
```

Example apply output:

```text theme={null}
deployment.apps/ecom-auth created
service/ecom-auth-service created
deployment.apps/ecom-inventory created
service/ecom-inventory-service created
deployment.apps/ecom-products created
service/ecom-products-service created
deployment.apps/ecom-user created
service/ecom-user-service created
```

Verify deployments and services:

```bash theme={null}
kubectl get deployment
kubectl get svc
```

Example outputs:

```text theme={null}
# Deployments
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
ecom-auth       1/1     1            1           3m
ecom-inventory  1/1     1            1           3m
ecom-products   1/1     1            1           3m
ecom-user       1/1     1            1           3m
```

```text theme={null}
# Services
NAME                   TYPE        CLUSTER-IP     PORT(S)
ecom-auth-service      ClusterIP   10.96.159.11   3000/TCP
ecom-inventory-service ClusterIP   10.96.233.237  3000/TCP
ecom-products-service  ClusterIP   10.96.2.92     3000/TCP
ecom-user-service      ClusterIP   10.96.77.87    3000/TCP
```

Generate traffic by exec'ing into the auth pod and curling the user service:

```bash theme={null}
kubectl get pods
kubectl exec -it ecom-auth-6dcb754fcb-v9rbc -- bash
# inside the pod:
curl ecom-user-service:3000
```

Example response:

```json theme={null}
{"method":"GET","path":"/"}
```

## 5. Install the Hubble CLI and connect to Hubble Relay

Install the Hubble CLI locally (pick the correct architecture). Example Linux script:

```bash theme={null}
# Install Hubble CLI (Linux example)
HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
HUBBLE_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then HUBBLE_ARCH=arm64; fi

curl -L --fail -o hubble-linux-${HUBBLE_ARCH}.tar.gz \
  "https://github.com/cilium/hubble/releases/download/${HUBBLE_VERSION}/hubble-linux-${HUBBLE_ARCH}.tar.gz"
curl -L --fail -o hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum \
  "https://github.com/cilium/hubble/releases/download/${HUBBLE_VERSION}/hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum"

sha256sum --check hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum

tar xzvf hubble-linux-${HUBBLE_ARCH}.tar.gz
sudo mv hubble /usr/local/bin/
rm hubble-linux-${HUBBLE_ARCH}.tar.gz hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum
```

Set up a port-forward from your workstation to Hubble Relay so the local Hubble CLI can reach Relay:

```bash theme={null}
kubectl -n kube-system port-forward service/hubble-relay 4245:80
```

Expected output:

```text theme={null}
Forwarding from 127.0.0.1:4245 -> 4245
Forwarding from [::1]:4245 -> 4245
```

(If you have the Cilium CLI installed you can also use `cilium hubble port-forward`.)

## 6. Observe flows with the Hubble CLI

The primary command is `hubble observe`. It supports powerful filters to narrow flows:

| Filter                                | Use case                              |
| ------------------------------------- | ------------------------------------- |
| --pod, --from-pod, --to-pod           | Show flows for specific pod(s)        |
| --from-label, --to-label, --namespace | Filter by labels or namespace         |
| --port, --protocol (e.g., http)       | Focus on specific ports/protocols     |
| -f / --follow                         | Stream new flows in real time         |
| --since, --last, --all                | Control time window / amount of flows |

To observe all flows related to the user pod (both directions) and follow new flows:

```bash theme={null}
hubble observe --pod default/ecom-user-55b49648b8-bwlsl -f
```

Sample flow output (abridged):

```text theme={null}
May 16 15:01:15.270: default/ecom-auth-6dcb754fcb-v9rbc:51246 (ID:28660) -> default/ecom-user-55b49648b8-bwlsl:3000 (ID:52953) to-endpoint FORWARDED (TCP Flags: SYN)
May 16 15:01:15.270: default/ecom-auth-6dcb754fcb-v9rbc:51246 (ID:28660) <- default/ecom-user-55b49648b8-bwlsl:3000 (ID:52953) to-endpoint FORWARDED (TCP Flags: SYN, ACK)
May 16 15:01:15.271: default/ecom-auth-6dcb754fcb-v9rbc:51246 (ID:28660) -> default/ecom-user-55b49648b8-bwlsl:3000 (ID:52953) to-endpoint FORWARDED (TCP Flags: ACK)
```

To show only HTTP L7 flows to the user pod:

```bash theme={null}
hubble observe --to-pod default/ecom-user-55b49648b8-bwlsl --protocol http -f
```

## 7. Using Hubble to validate network policies (CiliumNetworkPolicy)

Example: allow only `ecom-auth` to contact `ecom-user` on port 3000, and restrict to HTTP GET at L7.

Create `user-policy.yaml`:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: user-policy
spec:
  endpointSelector:
    matchLabels:
      app: ecom-user
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: ecom-auth
    toPorts:
    - ports:
      - port: "3000"
        protocol: TCP
      rules:
        http:
        - method: GET
```

Apply the policy:

```bash theme={null}
kubectl apply -f user-policy.yaml
```

Example output:

```text theme={null}
ciliumnetworkpolicy.cilium.io/user-policy created
```

Test connectivity:

* From the allowed pod (`ecom-auth`):

```bash theme={null}
kubectl exec -it ecom-auth-6dcb754fcb-v9rbc -- bash
curl ecom-user-service:3000     # returns {"method":"GET","path":"/"}
```

* From a denied pod (`ecom-products`):

```bash theme={null}
kubectl exec -it ecom-products-67474db564-q84cs -- bash
curl ecom-user-service:3000
# curl: (28) Failed to connect to ecom-user-service port 3000 after <timeout> ms: Couldn't connect to server
```

Hubble will include policy verdicts in the flow logs:

```text theme={null}
May 16 15:13:19.025: default/ecom-auth-... -> default/ecom-user-... policy-verdict:L3-L4 INGRESS ALLOWED (TCP Flags: SYN)
May 16 15:14:01.783: default/ecom-products-... <> default/ecom-user-... policy-verdict:none INGRESS DENIED (TCP Flags: SYN)
May 16 15:14:01.783: default/ecom-products-... <> default/ecom-user-... Policy denied DROPPED (TCP Flags: SYN)
```

Note: `policy-verdict` indicates whether traffic was allowed or denied and at which layer (L3/L4 vs. L7).

> **lightbulb** To capture and display L7 (HTTP) details in Hubble, include L7 rules (e.g., `rules.http`) in your CiliumNetworkPolicy. When an L7 rule is present, Hubble can report HTTP requests and responses alongside verdicts.

With the HTTP GET-only policy, Hubble can show HTTP-level details:

```text theme={null}
May 16 15:18:34.121: default/ecom-auth-... -> default/ecom-user-... http-request FORWARDED (HTTP/1.1 GET http://ecom-user-service:3000/)
May 16 15:18:34.125: default/ecom-auth-... <- default/ecom-user-... http-response FORWARDED (HTTP/1.1 200 5ms (GET http://ecom-user-service:3000/))
```

If a disallowed L7 method (e.g., POST) is attempted, the application may receive a 403 and Hubble will report the HTTP request/response and the policy-denied status:

```text theme={null}
# POST attempt from auth (policy allows only GET)
http-request FORWARDED (HTTP/1.1 POST http://ecom-user-service:3000/)
http-response DROPPED (HTTP/1.1 403)  # example: access denied
```

## 8. Hubble UI (visualize flows and service graphs)

Cilium includes a Hubble UI for visualizing service graphs, flows, and flow details. Start the UI helper:

```bash theme={null}
cilium hubble ui
```

This command typically sets up a port-forward and prints a local URL you can open in your browser. The UI shows an interactive service graph, a flows table, and detailed per-flow information such as timestamps, verdicts, TCP flags, and HTTP payload metadata.

<Frame>
  <img alt="A Hubble UI screenshot showing a Kubernetes service graph for the &#x22;default&#x22; namespace with nodes labeled ecom-auth, ecom-products, ecom-inventory, ecom-user and an external &#x22;world&#x22; node connected by traffic arrows. A flows table is visible at the bottom and a right-side panel displays flow details (timestamp, verdict, TCP flags, etc.)." />
</Frame>

## Quick reference — useful commands

| Task                             | Command                                                                                                                           |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Check nodes                      | `kubectl get nodes`                                                                                                               |
| Upgrade Cilium with values       | `helm upgrade cilium cilium/cilium -f values.yaml -n kube-system`                                                                 |
| Restart Cilium operator & agents | `kubectl -n kube-system rollout restart deployment/cilium-operator` and `kubectl -n kube-system rollout restart daemonset/cilium` |
| Verify Hubble pods               | `kubectl get pods -n kube-system`                                                                                                 |
| Port-forward Relay               | `kubectl -n kube-system port-forward service/hubble-relay 4245:80`                                                                |
| Stream flows                     | `hubble observe --pod <ns/pod> -f`                                                                                                |
| Show only HTTP flows             | `hubble observe --protocol http -f`                                                                                               |
| Apply Cilium policy              | `kubectl apply -f user-policy.yaml`                                                                                               |
| Start UI helper                  | `cilium hubble ui`                                                                                                                |

## Summary

* Hubble (with Relay and UI) provides cluster-wide visibility into L3/L4 flows, and L7 HTTP details when policies include L7 rules.
* Use `hubble observe` and its filters (`--pod`, `--from-pod`, `--protocol`, `-f`) to stream and inspect flows in real time.
* Combine CiliumNetworkPolicy L7 rules with Hubble to validate application-layer access and troubleshoot policy-related denials.
* The Hubble UI complements the CLI with a visual service graph and interactive flow inspection.

## Links and references

* Hubble (Cilium Observability): [https://docs.cilium.io/en/stable/gettingstarted/hubble/](https://docs.cilium.io/en/stable/gettingstarted/hubble/)
* Hubble CLI releases: [https://github.com/cilium/hubble/releases](https://github.com/cilium/hubble/releases)
* Hubble UI: [https://github.com/cilium/hubble-ui](https://github.com/cilium/hubble-ui)
* Cilium documentation: [https://docs.cilium.io/](https://docs.cilium.io/)
* Helm docs (chart values): [https://helm.sh/docs/topics/charts\_values/](https://helm.sh/docs/topics/charts_values/)
* Kubernetes port-forward docs: [https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b4c15752-3e42-43af-bedf-4a4c204ef5d8/lesson/d5e9a0ec-181f-4f1f-92bb-196324c1a802)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b4c15752-3e42-43af-bedf-4a4c204ef5d8/lesson/2c573ca0-aa8e-4bf6-ac75-9dc52dc99e2a)


# Hubble Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Observability/Hubble-Basics/page

Overview of Hubble observability for Kubernetes networking, covering architecture, deployment, CLI and UI usage, troubleshooting, metrics, and enabling Hubble with Cilium

In this lesson we cover the fundamentals of Hubble — the Cilium observability tool for Kubernetes networking. Hubble uses eBPF to capture and analyze network flows in real time, giving operators and developers rich visibility into service-to-service traffic, HTTP requests, Kafka usage, DNS behavior, and policy-enforced denials.

<Frame>
  <img alt="A slide titled &#x22;Observability&#x22; showing a Kubernetes cluster with two nodes, each hosting a pod and multiple bidirectional network flows between them. A satellite-like probe (Hubble) inspects the traffic while a developer monitors it, with the caption stating Hubble enables real-time traffic flow inspection across the cluster." />
</Frame>

Hubble operates at node and cluster scope, and can aggregate observability across clusters. It answers critical operational questions such as:

* Which services communicate with each other?
* How frequently do they communicate?
* What does the service dependency graph look like?
* Which HTTP endpoints are being called and with what response rates?
* Which Kafka topics are services producing to or consuming from?

<Frame>
  <img alt="A Hubble slide titled &#x22;Service Communication&#x22; showing a network icon of a central service connected to others. To the right is a numbered list of five questions about inter-service communication: which services communicate, how frequently, the dependency graph, what HTTP calls are made, and which Kafka topics are used." />
</Frame>

From a troubleshooting standpoint, Hubble helps you quickly narrow root causes:

* Is the failure DNS-related or a service misconfiguration?
* Is the issue at the application layer (L7/HTTP) or the network/transport layer (L4/TCP)?
* Are packets being dropped or connections reset?
* Which policies are blocking traffic?

<Frame>
  <img alt="A presentation slide from Hubble titled &#x22;Failures and Troubleshooting&#x22; with a wrench-and-screwdriver icon on a blue panel. The right side lists five troubleshooting questions about network communication, DNS, application vs network issues, and layer 4 (TCP) vs layer 7 (HTTP)." />
</Frame>

Hubble can surface recent error events and metrics such as:

* DNS resolution failures in the last N minutes.
* Interrupted TCP connections or connection timeouts.
* Rate of unanswered TCP SYN requests.
* 4xx/5xx HTTP response rates across services and clusters.

<Frame>
  <img alt="A slide titled &#x22;Error Events&#x22; (Hubble logo top-left) with a blue panel showing a code symbol and warning icon. To the right are four numbered questions about recent DNS resolution issues, interrupted TCP connections/unanswered SYN requests, and rates of 4xx/5xx HTTP responses." />
</Frame>

Hubble also exposes SLA-related metrics (p95/p99 latency between requests and responses), identifies poorly performing services, and reveals which connections were blocked by network policies or which DNS names were resolved by specific services.

Architecture and components

Below is a concise overview of the core Hubble components and their roles.

|     Component | Role                                                                        | Typical Deployment                             |
| ------------: | --------------------------------------------------------------------------- | ---------------------------------------------- |
| Hubble server | Collects flows and visibility data using eBPF on each node                  | Runs inside the Cilium agent (no per-node pod) |
|  Hubble relay | Aggregates flows from all Hubble servers and provides a single access point | Deployment (pod) in cluster                    |
|    Hubble CLI | Local client for querying flows and streaming events                        | Installed on developer/operator workstation    |
|     Hubble UI | Web-based visualization for interactive filtering and dependency graphs     | Deployment (pod) in cluster                    |

<Frame>
  <img alt="A diagram titled &#x22;Hubble Components&#x22; showing a Kubernetes cluster with three nodes, each running a Cilium Agent and eBPF Kernel; the middle node also hosts Hubble UI and Hubble relay. At the top an external Graphical UI / developer interacts with the cluster." />
</Frame>

Hubble UI draws dependency graphs (who talks to whom), highlights denied attempts due to policies, and shows statuses you can also obtain via the CLI.

Enabling Hubble

Enable Hubble via your Cilium Helm values (values.yaml). Typical settings:

```yaml theme={null}
hubble:
  # Enable Hubble (true by default).
  enabled: true

  # Enable Hubble Relay (aggregates flows from Hubble servers)
  relay:
    enabled: true

  # Whether to enable the Hubble UI.
  ui:
    enabled: true
```

After changing values.yaml, upgrade the Cilium Helm chart and restart operator/agent to apply the new configuration:

```bash theme={null}
helm upgrade cilium cilium/cilium -n kube-system -f values.yaml
kubectl -n kube-system rollout restart deployment/cilium-operator
kubectl -n kube-system rollout restart ds/cilium
```

Verify Hubble and related components using `cilium status`:

```bash theme={null}
> cilium status
  /--\
 /--\ /--\
 \__/ \__/
 /--\ /--\
 \__/ \__/
  \__/
       Cilium:             OK
       Operator:           OK
       Envoy DaemonSet:    OK
       Hubble Relay:       OK
       ClusterMesh:        disabled

DaemonSet           cilium                 Desired: 3, Ready: 3/3, Available: 3/3
DaemonSet           cilium-envoy           Desired: 3, Ready: 3/3, Available: 3/3
Deployment          cilium-operator        Desired: 2, Ready: 2/2, Available: 2/2
Deployment          hubble-relay           Desired: 1, Ready: 1/1, Available: 1/1
Deployment          hubble-ui              Desired: 1, Ready: 1/1, Available: 1/1
Containers:         cilium                 Running: 3
                    cilium-envoy           Running: 3
                    cilium-operator        Running: 2
                    clustermesh-apiserver
                    hubble-relay           Running: 1
                    hubble-ui              Running: 1
```

You can also inspect Hubble-related pods and services with kubectl:

```bash theme={null}
kubectl get pod -n kube-system | grep -i hubble
