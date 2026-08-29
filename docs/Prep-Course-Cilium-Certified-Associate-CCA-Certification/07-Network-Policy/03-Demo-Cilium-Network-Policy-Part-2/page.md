# Exec into app1 in dev
kubectl exec -it app1-75c78488c4-rzf48 -n dev -- bash

# From inside the pod:
telnet 10.0.2.89 3000
# Output:
# Telnet to an IP that does not exist -> will hang (CTRL+C to cancel)
telnet 10.0.2.112 3000
# (hangs, showing that traffic did not get to any pod)
```

Basic L3 ingress policy: allow only app2 (same namespace)

* Important: selectors in a CiliumNetworkPolicy are namespace-scoped by default (selectors without explicit namespace qualifiers match endpoints in the same namespace as the policy).

Example CiliumNetworkPolicy (allow ingress to app1 from app2 in dev):

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-policy
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

Apply and verify:

```bash theme={null}
kubectl apply -f l3-policy.yaml
# Output:
kubectl get ciliumnetworkpolicy -n dev
# NAME       AGE   VALID
# l3-policy  10s   True
```

Testing ingress behavior

* From app2 in dev -> should be allowed (telnet returns "Connection refused").
* From app3 in dev -> should be blocked (telnet will hang).

Example:

```bash theme={null}
# From app2 in dev (allowed)
kubectl exec -it app2-5957957d5b-kgkt6 -n dev -- bash
telnet 10.0.2.88 80
# From app3 in dev (blocked)
kubectl exec -it app3-87d98dbbb-k6xzk -n dev -- bash
telnet 10.0.2.88 80
# (hangs; CTRL+C to cancel)
```

Namespace scoping and cross-namespace rules

* By default, label selectors reference the policy namespace.
* To allow endpoints from another namespace, use the namespace-qualified label: "k8s:io.kubernetes.pod.namespace": "\<namespace>".
* YAML tip: keys containing colons must be quoted.

Example — allow app=app2 from the prod namespace to reach app1 in dev:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-policy
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  ingress:
  - fromEndpoints:
    - matchLabels:
        "k8s:io.kubernetes.pod.namespace": "prod"
        app: app2
```

Apply and test:

* app2 in prod -> allowed.
* app2 in dev -> still allowed due to original matchLabels (if preserved).
* app3 in dev -> still blocked.

Match multiple namespaces (matchExpressions)

* Use matchExpressions when you need to match a label key against multiple values.

Example — allow app2 from prod OR staging:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-policy
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: app2
      matchExpressions:
      - key: "k8s:io.kubernetes.pod.namespace"
        operator: In
        values:
        - prod
        - staging
```

* After applying, app2 in prod and app2 in staging will be allowed.
* app2 in dev will be allowed only if you include dev in the values or keep a matchLabels that matches dev.

Allow all endpoints in the policy namespace

* An empty endpoint selector () in fromEndpoints or toEndpoints matches all endpoints in the same namespace as the CiliumNetworkPolicy.

Example — allow all pods in dev to talk to app1:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-allow-all-dev
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  ingress:
  - fromEndpoints:
    - {}
```

Deny all ingress (default deny for selected endpoints)

* If you select endpoints and provide an empty ingress list, ingress is denied to those endpoints (default deny).

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-deny-all
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  ingress: []
```

Egress rules (toEndpoints, toCIDR, toCIDRSet)

* Egress uses toEndpoints and follows the same matching patterns as ingress (namespace-qualified labels, matchExpressions, empty selector).
* Examples below show common egress controls.

Example — allow app1 in dev to talk only to app2 in dev:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-egress-to-app2
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
  - toEndpoints:
    - matchLabels:
        app: app2
```

Example — allow egress to app2 in prod namespace:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-egress-to-app2-prod
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
  - toEndpoints:
    - matchLabels:
        app: app2
        "k8s:io.kubernetes.pod.namespace": "prod"
```

Allow egress to all endpoints in same namespace:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-egress-allow-all-dev
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
  - toEndpoints:
    - {}
```

Deny all egress:

* Provide an empty egress list to deny all egress from the selected endpoints:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-egress-deny-all
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress: []
```

Egress to CIDR ranges

* Use toCIDR to specify CIDR entries directly.
* Use toCIDRSet to specify CIDRs with an except list.

Example — allow egress to specific CIDRs:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-egress-to-cidrs
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
  - toCIDR:
    - 172.16.1.0/24
    - 10.12.1.0/24
```

Example — allow egress to a large CIDR but exclude specific subranges:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-egress-cidrset-with-except
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
  - toCIDRSet:
    - cidr: 10.0.0.0/8
      except:
      - 10.100.0.0/24
      - 10.200.200.11/32
```

Quick reference table — common policy patterns

| Resource Type                      | Typical Use Case                                | Example snippet                                                                  |
| ---------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------- |
| Allow ingress from same namespace  | Limit ingress to specific app in same namespace | fromEndpoints: - matchLabels: app: app2                                          |
| Allow ingress from other namespace | Cross-namespace allow using namespace label     | fromEndpoints: - matchLabels: "k8s:io.kubernetes.pod.namespace":"prod" app: app2 |
| Allow all in policy namespace      | Permit all pods in namespace                    | fromEndpoints: -                                                                 |
| Deny all ingress                   | Default deny for selected endpoints             | ingress: \[]                                                                     |
| Egress to CIDR                     | Allow external ranges                           | egress: - toCIDR: - 172.16.1.0/24                                                |
| Egress CIDR with exceptions        | Exclude subranges                               | toCIDRSet: - cidr: 10.0.0.0/8 except: - 10.100.0.0/24                            |

Key reminders and best practices

<Callout icon="warning">
  When a CiliumNetworkPolicy selects endpoints, it restricts traffic for those endpoints according to the policy rules. If you intend to keep open communication, do not create overly broad selectors without the desired allow rules (use empty from/to endpoints carefully).
</Callout>

<Callout icon="lightbulb">
  Quick YAML tip: Keys containing special characters (such as colons) must be quoted in YAML. Example: "k8s:io.kubernetes.pod.namespace": "prod"
</Callout>

* Default behavior: without any network policy selecting an endpoint, pods can communicate freely.
* Once a CiliumNetworkPolicy selects an endpoint, traffic is restricted according to the policy rules you define.
* Use endpoint selectors, matchLabels, and matchExpressions for precise targeting.
* To match endpoints in another namespace, use the namespace-qualified label key (quoted).
* fromEndpoints / toEndpoints with  matches all endpoints in the policy namespace.
* To explicitly deny all ingress/egress to selected endpoints, provide an empty ingress/egress list.
* Extend these L3/L3-only examples for L4/L7 controls and service-aware policies as needed. For advanced use cases, consult the official Cilium policy documentation: [https://docs.cilium.io/en/stable/policy/](https://docs.cilium.io/en/stable/policy/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/bf652c52-bb30-4bcc-9d18-c703f7b3e88a/lesson/506a1635-ece0-4c7f-91a5-b9f2baf408fd" />
</CardGroup>


# Demo Cilium Network Policy Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Network-Policy/Demo-Cilium-Network-Policy-Part-2/page

Hands-on guide to Cilium network policies covering L3 L4 and L7 controls, egress and ingress examples, DNS and HTTP filtering, port and CIDR rules, and clusterwide policies

This guide continues the hands-on exploration of Cilium network policies, focusing on Layer 4 (L4) controls and how they combine with Layer 3 (L3) and Layer 7 (L7) capabilities. Examples use egress rules for clarity, but the syntax and behavior are identical for ingress rules where noted.

<Frame>
  <img alt="A presentation slide with the word &#x22;Demo&#x22; on the left. On the right is a teal gradient shape reading &#x22;Cilium Network Policy Part 2&#x22; with a small © KodeKloud notice in the corner." />
</Frame>

## L4 egress: restrict by CIDR and port(s)

You can restrict egress by IP ranges (CIDRs) and/or by specific ports or port ranges. Use CIDR restrictions when you want to limit destinations by address space; use `toPorts` for port-based filtering regardless of destination.

Example: allow egress to two specific CIDR ranges, and also allow a broad CIDR but exclude a few subnets/addresses.

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: l3-policy
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toCIDR:
        - 172.16.1.0/24
        - 10.12.1.0/24
    - toCIDRSet:
        - cidr: 10.0.0.0/8
          except:
            - 10.100.0.0/24
            - 10.200.200.11/32
```

To restrict only by ports (L4) and allow those ports to any destination, use `toPorts`:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: allow-app1-port80
  namespace: dev
spec:
  endpointSelector:
    matchLabels:
      app: app1
  egress:
    - toPorts:
        - ports:
            - port: "80"
              protocol: TCP
```

This policy permits pods with label `app: app1` to make TCP connections only on port 80 to any IP.

Terminal checks from inside an app1 pod (examples):

```bash theme={null}
