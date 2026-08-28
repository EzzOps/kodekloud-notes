# /etc/resolv.conf inside pod
nameserver 10.96.0.10  # kube-dns Service IP (example)
search my-namespace.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

If `nameserver` points to the node's DNS (the node's `/etc/resolv.conf`) rather than the cluster DNS, the pod will resolve internet names but not Kubernetes service names. That happens when the pod will inherit the node resolver instead of using cluster DNS.

## The culprit: dnsPolicy

Kubernetes exposes `dnsPolicy` on pods to control how DNS is configured. Common values:

* `ClusterFirst` (default for most pods): kubelet configures `/etc/resolv.conf` to use the cluster DNS so pods can resolve internal service names such as `kubernetes.default`.
* `Default`: the pod inherits the node's DNS configuration (the node's `/etc/resolv.conf`). This allows internet name resolution via the node, but internal Kubernetes service names will not be resolved by that DNS.
* `ClusterFirstWithHostNet`: special policy for host-networked pods that still directs DNS to the cluster DNS.

Example pod spec using ClusterFirst (default):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: app
      image: app:1.0
  dnsPolicy: ClusterFirst
```

Example pod spec that will use the node DNS (and thus likely fail to resolve cluster service names):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: app
      image: app:1.0
  dnsPolicy: Default
```

<Callout icon="lightbulb">
  The `Default` dnsPolicy is misleading: it does not mean “use the Kubernetes default behavior.” It means “use the node’s resolver.” If you need cluster DNS resolution, do not use `dnsPolicy: Default`.
</Callout>

## Host networking adds a wrinkle

When `hostNetwork: true` is set, the pod uses the node's network namespace. By default kubelet adjusts the dnsPolicy to `ClusterFirstWithHostNet` for these pods so they still use cluster DNS. Problems arise when `dnsPolicy` is explicitly set to `Default` on a host-networked pod — such pods will use the node resolver and lose ability to resolve cluster service names.

Host-networked pod that will run into the DNS problem:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-hostnet-app
spec:
  hostNetwork: true
  containers:
    - name: app
      image: app:1.0
  dnsPolicy: Default   # Uses node DNS — problematic for cluster service name resolution
```

Fix by using `ClusterFirstWithHostNet`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-hostnet-app
spec:
  hostNetwork: true
  containers:
    - name: app
      image: app:1.0
  dnsPolicy: ClusterFirstWithHostNet  # ← the fix
```

## How to debug this issue

1. Check `/etc/resolv.conf` inside the pod:

```bash theme={null}
kubectl exec -it <pod-name> -- cat /etc/resolv.conf
```

Look for:

* `nameserver` — is it the cluster DNS IP (e.g., `10.96.0.10`) or the node IP?
* `search` — does it include `<namespace>.svc.cluster.local` and `cluster.local`?
* `options ndots` — ensure it’s reasonable (commonly `ndots:5`).

2. Inspect the pod spec:

```bash theme={null}
kubectl get pod <pod-name> -o yaml
```

Check `spec.dnsPolicy` and `spec.hostNetwork`.

3. If the pod uses host networking, ensure `dnsPolicy` is `ClusterFirstWithHostNet` (unless you intentionally want node DNS).

## Quick checklist

| Step | What to check                                | Example/What it means                                                                                                        |
| ---- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1    | Inspect `/etc/resolv.conf` inside the pod    | `nameserver` should point to cluster DNS; `search` should include `svc.cluster.local`                                        |
| 2    | Check `spec.dnsPolicy`                       | `ClusterFirst` (normal pods) or `ClusterFirstWithHostNet` (hostNetwork pods). Avoid `Default` if you need cluster DNS.       |
| 3    | For host-networked pods, confirm `dnsPolicy` | Use `ClusterFirstWithHostNet` when `hostNetwork: true` and cluster service resolution is required                            |
| 4    | Validate CoreDNS/kube-dns                    | Ensure CoreDNS pods and Service are healthy: `kubectl get pods -n kube-system` and `kubectl get svc -n kube-system kube-dns` |

## References

* [Kubernetes DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* [CoreDNS — DNS server](https://coredns.io/)

Use the checklist above to quickly identify whether a pod is pointed at the node resolver by mistake, and update `dnsPolicy` or the pod spec accordingly to restore cluster DNS resolution.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/c1eb3967-23d3-4a34-b23d-14a892f95e1d/lesson/efdad69a-4abb-4985-aa8b-7053297d5939" />
</CardGroup>


# ndots5 Trap

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Networking/ndots5-Trap/page

Explains ndots behavior in Kubernetes pods, how ndots 5 multiplies DNS queries causing latency, and fixes like trailing dots or reducing ndots to cut unnecessary lookups.

If DNS lookups from inside a pod succeed but external calls are slow, DNS itself may not be failing — the pod may simply be generating many extra DNS queries. A frequent root cause is the pod’s DNS `options` setting, commonly `ndots:5`. This article explains what `ndots` does, shows how it multiplies lookups, and describes practical fixes for Kubernetes pods.

## What `ndots` means

The `ndots` option sets a threshold for how many dots must appear in a hostname before the resolver treats it as "absolute" and queries it as-is. If a name has fewer dots than the `ndots` value, the resolver first appends the configured search domains and tries each candidate before falling back to the original name.

For example: `api.github.com` contains two dots. With `ndots:5`, 2 is less than 5, so the resolver will treat `api.github.com` like a short (potentially cluster-local) name and attempt the search-domain-expanded names first.

<Frame>
  <img alt="The image is a graphic explaining that a threshold of &#x22;ndots&#x22; equals 5, showing an example with &#x22;api.github.com&#x22; which has 2 dots, indicating 2 is less than 5." />
</Frame>

## How the resolver expands names

With `ndots:5`, a query for `api.github.com` will cause the resolver to try the search domains before the actual external name. Typical candidates (for a cluster with default search domains) are:

* `api.github.com.default.svc.cluster.local`
* `api.github.com.svc.cluster.local`
* `api.github.com.cluster.local`
* finally `api.github.com`

This sequence increases the number of queries for a single name. Example `dig` output for these attempts:

```bash theme={null}
$ dig api.github.com.default.svc.cluster.local A +short
; <<>> DiG 9.11.3 <<>> api.github.com.default.svc.cluster.local A +short
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 12345

$ dig api.github.com.svc.cluster.local A +short
; <<>> DiG 9.11.3 <<>> api.github.com.svc.cluster.local A +short
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 12346

$ dig api.github.com.cluster.local A +short
; <<>> DiG 9.11.3 <<>> api.github.com.cluster.local A +short
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 12347

$ dig api.github.com A +short
151.101.129.140
```

If the client requests both A (IPv4) and AAAA (IPv6) records, the resolver repeats the sequence for each record type, potentially doubling the number of queries. For high-volume applications, this flood of extraneous lookups can overload DNS servers such as CoreDNS.

<Frame>
  <img alt="The image is a diagram highlighting the complexity of DNS lookups for IPv4 and IPv6, showing that a single name requires 8 lookups in total." />
</Frame>

## Common mitigations

There are two straightforward mitigations to reduce unnecessary search-domain lookups:

1. Use a trailing dot. Writing a fully qualified domain name (FQDN) with a trailing dot — for example, `api.github.com.` — tells the resolver the name is absolute and it will query that exact name immediately (no search-domain expansion).

2. Lower `ndots` in the pod’s DNS configuration. Setting `ndots` to `1` or `2` keeps the ability to resolve short, cluster-local names while preventing most external hostnames from triggering the full search list.

<Frame>
  <img alt="The image describes two fixes related to domain name completion: adding a trailing dot and lowering ndots, with an example using &#x22;api.github.com&#x22; to illustrate." />
</Frame>

Example pod spec that sets `ndots` to 2:

```yaml theme={null}
spec:
  dnsConfig:
    options:
      - name: ndots
        value: "2"
```

## Quick comparison

| Strategy                                         | When to use                                                     | Pros                                                 | Cons                                                                                    |
| ------------------------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Trailing dot (`api.github.com.`)                 | Quick fix in application config or callers that build hostnames | No resolver-side changes; immediate absolute lookup  | Requires changing callers or libraries; easy to forget                                  |
| Lower `ndots` (`dnsConfig: ndots: "1"` or `"2"`) | Pod-level fix for many apps in a pod                            | Centralized; preserves short cluster-name resolution | Needs pod spec modification or redeploy; be careful with apps relying on search domains |
| Reduce search domains                            | Cluster-level optimization                                      | Fewer candidate lookups for every query              | May impact resolution of legitimate short names                                         |

<Callout icon="lightbulb">
  Kubernetes default `ndots` is commonly 5 (the “ndots:5 trap”). Lowering `ndots` to `1` or `2` reduces wasted search-domain lookups for typical external hostnames while still allowing short cluster-local names to resolve.
</Callout>

<Callout icon="warning">
  Avoid globally setting `ndots` too low without testing: some legacy apps rely on search-domain expansion to resolve internal services. Validate behavior in a staging environment before changing production pod specs.
</Callout>

## Additional resources

* [CoreDNS documentation](https://coredns.io/)
* [Kubernetes DNS policy and `dnsConfig`](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* `man resolv.conf` — explains `ndots`, `search`, and other resolver options

By understanding `ndots` and how search domains are applied, you can eliminate a common source of DNS-related latency inside Kubernetes pods and reduce load on your cluster DNS service.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/c1eb3967-23d3-4a34-b23d-14a892f95e1d/lesson/940f3a20-1f31-4e53-9479-f0ff2a4aa86f" />
</CardGroup>
