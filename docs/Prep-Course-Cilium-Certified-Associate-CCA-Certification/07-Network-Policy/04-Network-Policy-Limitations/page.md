# Attempt to reach port 90 -> should fail (connection refused or timeout)
telnet 10.0.2.89 90

# Attempt to reach port 80 -> should succeed (if target accepts TCP)
telnet 10.0.2.89 80
```

### Port ranges

Allow a contiguous port range using `endPort` (inclusive):

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: allow-app1-port-range
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toPorts:
        - ports:
            - port: "80"
              endPort: 100
              protocol: TCP
```

This permits TCP ports 80–100; ports outside that range (e.g., 101) are denied.

## Combine L3 (endpoints/CIDR) with L4 (ports)

For precise allowances, combine `toEndpoints` (L3 pod selectors) or `toCIDR` with `toPorts`. Example: allow app1 to talk to app2 only on TCP port 80.

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: app1-to-app2-port80
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toEndpoints:
        - matchLabels:
            app: app2
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
```

Behavior summary:

* app1 -> app2 on TCP/80: allowed
* app1 -> app2 on other ports (e.g., 90): blocked
* app1 -> any other pod: blocked (regardless of port)

## L4 with CIDR destinations

You can combine L4 and L3-by-CIDR — for example, permit app1 to contact IPs in a subnet only on a specific port.

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: app1-to-subnet-port80
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toCIDR:
        - 192.168.1.0/24
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
```

This allows TCP port 80 traffic from app1 to addresses in 192.168.1.0/24 only.

<Callout icon="lightbulb">
  Egress policies are deny-by-default: when you add egress rules, Cilium blocks anything not explicitly allowed. Common control-plane traffic (for example DNS) will be blocked unless you permit it.
</Callout>

## DNS gets blocked by default — add an explicit rule

Because egress is deny-by-default, restrictive egress policies often break DNS resolution inside pods. You must explicitly allow DNS to the cluster’s DNS service (typically CoreDNS) on port 53.

Example symptom after applying a restrictive policy:

```text theme={null}
;; communications error to 10.96.0.10#53: timed out
```

Steps to allow DNS for app1:

1. Find CoreDNS pod labels:

```bash theme={null}
kubectl get pod -n kube-system --show-labels | grep -i coredns
```

2. Create a namespaced policy that permits egress from app1 to the CoreDNS pods on port 53. DNS often uses UDP/TCP, so `protocol: ANY` is acceptable:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: allow-dns-for-app1
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toEndpoints:
        - matchLabels:
            k8s.io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
```

After applying the rule, DNS queries from app1 should succeed:

```text theme={null}
Server:  10.96.0.10
Address: 10.96.0.10#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.176.206
```

<Callout icon="warning">
  If you forget to allow DNS, many higher-level application behaviors will fail (package downloads, image pulls inside pods, service discovery, etc.). Always include DNS allowances when applying restrictive egress policies.
</Callout>

## L7: DNS filtering (match names / patterns)

Cilium's L7 rules can match DNS queries by name or pattern. Use `rules.dns` to allow only specific domain names to be resolved.

Example: allow only \*.google.com and yahoo.com queries from app1 to CoreDNS:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: dns-l7-restrict
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toEndpoints:
        - matchLabels:
            k8s.io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
      rules:
        dns:
          - matchPattern: "*.google.com"
          - matchName: "yahoo.com"
```

Result:

* Queries for \*.google.com and yahoo.com: allowed
* Queries for other domains (e.g., amazon.com): refused/blocked

Example from app1 after applying policy:

```text theme={null}
# Allowed
nslookup google.com

# Refused
nslookup amazon.com
;; communications error to 10.96.0.10#53: timed out
```

## L7: HTTP filtering (method, path, headers, host)

Cilium can perform HTTP-aware L7 filtering. You can allow or deny requests based on HTTP method, path, headers, and host. The following policy lets only GET /auth requests from app1 to app2 on port 80.

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: app1-to-app2-http-get-auth
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app2
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: app1
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: /auth
```

Test plan:

* Start packet capture or application logs on app2 to observe incoming requests.
* From app1:
  * curl http\://\<app2-ip>/auth  => allowed
  * curl http\://\<app2-ip>/products => blocked by L7 policy

Note: If app2 has no HTTP server running, you may see connection refused. Policy enforcement can still be verified by checking whether requests are accepted or dropped at the network policy layer.

## Ingress from other pods and external entities

Ingress policies follow the same selector patterns. Example: allow ingress to app1 only from pods labeled `app: app2`:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: app1-ingress-from-app2
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: app2
```

If you expose a pod with a NodePort or similar, external traffic is treated as an entity outside the cluster. Use `fromEntities` to allow traffic from those external sources:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: allow-nodeport-world
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  ingress:
    - fromEntities:
        - world
```

Example NodePort service exposing app1 on nodePort 30007:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: dev
spec:
  type: NodePort
  selector:
    app: app1
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30007
```

If your cluster has a restrictive ingress policy, external curl to \<nodeIP>:30007 will be blocked unless you permit `fromEntities: ["world"]` (or another appropriate ingress allowance).

## Cilium Cluster-wide Network Policies (CCNP)

A CiliumClusterwideNetworkPolicy (CCNP) applies across all namespaces. Use a CCNP when you want the same policy to affect pods in every namespace — for example, to allow DNS cluster-wide.

Example: allow all pods cluster-wide to query CoreDNS on port 53:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-dns-clusterwide
spec:
  endpointSelector: {}   # matches all pods in all namespaces
  egress:
    - toEndpoints:
        - matchLabels:
            k8s.io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
```

Notes:

* A namespaced CiliumNetworkPolicy applies only to pods in that namespace. A CCNP applies cluster-wide.
* To include or exclude specific namespaces in endpoint selectors, use the `k8s.io.kubernetes.pod.namespace` label in `fromEndpoints`/`toEndpoints`.

## Quick reference: L3 vs L4 vs L7

| Layer            | What it controls                   | Cilium fields                        | Common use cases                               |
| ---------------- | ---------------------------------- | ------------------------------------ | ---------------------------------------------- |
| L3 (Network)     | Destination IPs / pods             | `toCIDR`, `toCIDRSet`, `toEndpoints` | Restrict to specific pods or subnets           |
| L4 (Transport)   | Ports and protocols                | `toPorts`, `port`, `endPort`         | Allow only specific TCP/UDP ports or ranges    |
| L7 (Application) | Protocol methods, paths, DNS names | `rules: { http:, dns: }`             | HTTP method/path filtering, DNS name filtering |

## Summary

* Use `toPorts` for L4 port-based restrictions and `toCIDR`/`toEndpoints` for L3 (IP/pod) restrictions.
* Combine L3 + L4 to express fine-grained policies (e.g., app1 → app2 on TCP/80).
* Cilium policies are deny-by-default for egress; always explicitly allow control-plane traffic such as DNS.
* Cilium supports L7 policies (DNS, HTTP, etc.) for application-aware controls.
* Use CiliumClusterwideNetworkPolicy to apply consistent rules cluster-wide.

## Links and references

* Cilium Network Policy documentation: [https://docs.cilium.io/en/stable/policy/](https://docs.cilium.io/en/stable/policy/)
* Kubernetes DNS (CoreDNS) overview: [https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)

For advanced tactics like entities, additional L7 rules, HTTP header or host matching, consult the Cilium policy documentation above.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/bf652c52-bb30-4bcc-9d18-c703f7b3e88a/lesson/09fd7ca2-c277-4ef1-b77c-3616cbc9d2c0" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/bf652c52-bb30-4bcc-9d18-c703f7b3e88a/lesson/0e692f32-82dd-433b-a0dd-8ff541c33f67" />
</CardGroup>


# Network Policy Limitations

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Network-Policy/Network-Policy-Limitations/page

Explains limitations of Kubernetes native NetworkPolicy and why extended engines like Cilium add CRDs for L7 filtering, FQDN rules, richer selectors, explicit deny and cluster scoped policies.

In this lesson we examine the limitations of the standard Kubernetes NetworkPolicy API and explain why extended policy engines (for example, Cilium) introduce CRDs to fill those gaps. Understanding these constraints helps when you design secure cluster networking and select a CNI or policy engine that meets your requirements.

## What native Kubernetes NetworkPolicy supports

Kubernetes NetworkPolicy works at Layer 3 (IP) and Layer 4 (TCP/UDP/SCTP). It can restrict traffic using pod selectors, namespace selectors, IPBlocks, and ports. A common L3/L4 NetworkPolicy looks like this:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  policyTypes:
  - Ingress
  podSelector:
    matchLabels:
      role: db
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
```

<Callout icon="lightbulb">
  Standard NetworkPolicy is L3/L4-only. It cannot inspect or filter Layer 7 protocol semantics (for example, HTTP method or HTTP path), and it does not support DNS/FQDN-based matching, service-account selectors, or cluster-wide policies out of the box.
</Callout>

## Key limitations of networking.k8s.io/v1 NetworkPolicy

* No Layer 7 (L7) protocol awareness

  * Native NetworkPolicy cannot express rules such as “allow only HTTP GET to /users.” It can allow TCP port 80, but it cannot validate HTTP methods, paths, headers, or other L7 attributes.

  Conceptual (illustrative) L7-aware policy example — not supported by native NetworkPolicy:

  ```yaml theme={null}
  # Conceptual example (not supported by native networking.k8s.io/v1 NetworkPolicy)
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: allow-http-get-users
  spec:
    policyTypes:
    - Ingress
    podSelector:
      matchLabels:
        app: web
    ingress:
    - from:
      - podSelector:
          matchLabels:
            role: frontend
      ports:
      - protocol: TCP
        port: 80
      # Native NetworkPolicy cannot specify HTTP method/path here
      # This block is a conceptual L7 match: method GET, path /users
  ```

* DNS / FQDN matching limitations

  * NetworkPolicy cannot match on DNS names or FQDNs. To allow egress to an external service that resolves to multiple IPs, you must enumerate all IPs in ipBlock entries and update the policy whenever DNS resolves to new addresses.

  Conceptual FQDN match (native NetworkPolicy does not support this):

  ```yaml theme={null}
  # Conceptual example (native NetworkPolicy does not support fqdn)
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: test-network-policy
    namespace: default
  spec:
    podSelector:
      matchLabels:
        role: db
    policyTypes:
    - Ingress
    ingress:
    - from:
      - fqdn:
          matchDNS: external-service.com
    ports:
    - protocol: TCP
      port: 6379
  ```

  To illustrate the problem: suppose external-service.com resolves to multiple IPs (e.g., 192.168.1.1 and 172.16.1.1). With native policies you must list those IPs explicitly, and update the policy when the service endpoints change.

  <Frame>
    <img alt="A slide titled &#x22;DNS Matching&#x22; showing a green &#x22;External Service&#x22; box with a server icon and two IP addresses listed (192.168.1.1 above and 172.16.1.1 below). The slide includes a small © KodeKloud notice in the corner." />
  </Frame>

* Limited pod attribute selectors
  * Native NetworkPolicy can only match pods by labels and namespaces. It cannot select by other pod attributes such as serviceAccountName, or match richer metadata fields without label workarounds.

* Protocol matching constraints
  * The protocol field supports TCP, UDP, and SCTP in the Kubernetes API. ICMP or other protocol-specific matches and application-protocol-specific filtering (for example, DNS query matching) are not standardized in networking.k8s.io/v1. Some CNIs may extend behavior, but it is not portable.

* No explicit deny rules

  * Native NetworkPolicy is primarily a whitelist model: you define what is allowed. It does not provide explicit deny rules that take precedence. You cannot express “allow everything from X except pods labeled env=staging” using only networking.k8s.io/v1 constructs.

  Conceptual deny model (illustrative; not supported by native NetworkPolicy):

  ```yaml theme={null}
  # Conceptual/extended policy model (native NetworkPolicy can't express 'ingressDeny')
  apiVersion: cilium.io/v2
  kind: CiliumNetworkPolicy
  metadata:
    name: backend-policy-with-deny
  spec:
    endpointSelector:
      matchLabels:
        app: backend
    ingress:
    - fromEndpoints:
      - matchLabels:
          app: frontend
    ingressDeny:
    - fromEndpoints:
      - matchLabels:
          env: staging
  ```

* Namespace scoping (no cluster-scoped NetworkPolicy)
  * NetworkPolicy objects are namespace-scoped. To apply the same policy across multiple namespaces, you must replicate the object in each namespace. There is no native cluster-scoped NetworkPolicy in networking.k8s.io/v1.

* Multi-cluster awareness

  * NetworkPolicy is cluster-local. It cannot inherently distinguish source cluster origin across multiple clusters; cross-cluster policies require labeling and replication strategies outside the API.

  Example of a cluster-local policy (works within a single cluster only):

  ```yaml theme={null}
  # This is a cluster-local NetworkPolicy example - it does not express cross-cluster origin
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: allow-from-project-and-cluster1
  spec:
    podSelector:
      matchLabels:
        role: db
    policyTypes:
    - Ingress
    ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            project: myproject
      - podSelector:
          matchLabels:
            cluster: cluster1
    ports:
    - protocol: TCP
      port: 6379
  ```

## Summary comparison: native NetworkPolicy vs extended policy engines

| Feature                          | networking.k8s.io/v1 NetworkPolicy | Cilium (CiliumNetworkPolicy / CiliumClusterwideNetworkPolicy) |
| -------------------------------- | ---------------------------------: | ------------------------------------------------------------- |
| L3/L4 filtering                  |                                Yes | Yes                                                           |
| L7 filtering (HTTP, gRPC, Kafka) |                                 No | Yes (methods, paths, headers)                                 |
| FQDN / DNS-based rules           |                                 No | Yes (toFQDNs)                                                 |
| Service account selection        |                                 No | Yes                                                           |
| Explicit deny semantics          |                                 No | Yes (ingressDeny/egressDeny)                                  |
| Cluster-scoped policies          |                                 No | Yes (CiliumClusterwideNetworkPolicy)                          |
| Protocol variety                 |                       TCP/UDP/SCTP | Extended support depending on Cilium features                 |

## Why Cilium and other enhanced engines exist

Cilium provides CRDs such as CiliumNetworkPolicy and CiliumClusterwideNetworkPolicy to address the functional gaps in native NetworkPolicy:

* L7-aware rules: match HTTP methods, paths, headers; support for gRPC and Kafka.
* FQDN-based egress: toFQDNs allow DNS-driven policies that follow changing IPs.
* Rich selectors: service accounts, identity-based selectors, and metadata-aware matching.
* Explicit deny semantics and more flexible precedence models.
* Cluster-wide policies for consistent rules across namespaces and clusters.

### Cilium policy examples (illustrative of capabilities)

* L7 HTTP allow (Cilium can match method/path):

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend-http
spec:
  endpointSelector:
    matchLabels:
      app: myservice
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/users"
```

* FQDN-based egress (toFQDNs):

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-external-service
spec:
  endpointSelector:
    matchLabels:
      role: db
  egress:
  - toFQDNs:
    - matchName: "external-service.com"
    toPorts:
    - ports:
      - port: "6379"
        protocol: TCP
```

* Deny and advanced matching:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: backend-policy-with-deny
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
  ingressDeny:
  - fromEndpoints:
    - matchLabels:
        env: staging
```

* Cluster-scoped policy example placeholder:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: example-clusterwide-policy
spec:
  # spec similar to CiliumNetworkPolicy, applied cluster-wide
```

## Final notes

* Native Kubernetes NetworkPolicy is intentionally simple and broadly supported by many CNIs. That simplicity means it is portable but functionally limited (no L7, no FQDN matching, limited selectors, no explicit deny, no cluster-scoped definitions).
* If your security requirements include L7 filtering, DNS-aware egress, service-account selectors, explicit denies, or cluster-wide rules, evaluate an extended policy engine such as Cilium and its CRDs: CiliumNetworkPolicy and CiliumClusterwideNetworkPolicy.

## Links and references

* [Kubernetes NetworkPolicy documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Cilium documentation](https://docs.cilium.io/)
* [CiliumNetworkPolicy reference](https://docs.cilium.io/en/stable/policy/language/)
* [CiliumClusterwideNetworkPolicy reference](https://docs.cilium.io/en/stable/policy/clusterwide/)

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy

apiVersion: "cilium.io/v2"
kind: CiliumClusterwideNetworkPolicy
```

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/bf652c52-bb30-4bcc-9d18-c703f7b3e88a/lesson/f2670466-592b-42d0-9e94-09433ea15324" />
</CardGroup>
