# Run container as a specific user
docker run --user=1001 ubuntu sleep 3600

# Grant a Linux capability
docker run --cap-add MAC_ADMIN ubuntu
```

Kubernetes adopts the same principles, but you configure them in your Pod spec.

***

## Security Context Levels

Kubernetes lets you apply security contexts at two scopes:

| Level           | Applies To              | Common Settings                                         |
| --------------- | ----------------------- | ------------------------------------------------------- |
| Pod-level       | All containers in a Pod | `runAsUser`, `runAsGroup`, `fsGroup`                    |
| Container-level | A single container      | `runAsUser`, `runAsGroup`, `capabilities`, `privileged` |

***

## Pod-Level Security Context

A Pod-level security context propagates settings to every container within that Pod. This is ideal for defining a consistent user and group ID across all containers.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
```

<Callout icon="lightbulb">
  You cannot set Linux capabilities (`capabilities.add`) at the Pod level. To grant capabilities, use a container-level security context.
</Callout>

***

## Container-Level Security Context

When you need fine-grained control—such as adding or dropping specific Linux capabilities—apply the security context directly to the container:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        capabilities:
          add: ["MAC_ADMIN", "NET_RAW"]
          drop: ["ALL"]
        privileged: false
```

<Callout icon="triangle-alert">
  Running containers in `privileged` mode grants all Linux capabilities and should be avoided unless absolutely necessary.
</Callout>

***

## Best Practices

* Always run containers as non-root users (`runAsUser` ≥ 1000).
* Use Pod-level context for uniform settings; override at the container level only when needed.
* Drop unnecessary capabilities (`capabilities.drop: ["ALL"]`) and add only those required.

***

## Further Reading

* [Kubernetes Pods Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
* [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
* [Understanding Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)

Keep practicing with these configurations to strengthen your cluster’s security. See you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/87ba5cde-ab72-444a-a323-6cd6a9d1bafd" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/ae705c0e-4b0f-4921-a49d-b02b75cb12d7" />
</CardGroup>


# Network Policies

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Network-Policies/page

This guide explains securing pod communication in Kubernetes using NetworkPolicies, including ingress and egress rules, and access restrictions by namespace and IP range.

In this guide, you’ll learn how to secure communication between pods using Kubernetes NetworkPolicies. We’ll start with a permissive default, then restrict access to a database (DB) pod so that only an API pod can connect on port 3306. Finally, you’ll see how to scope access by namespace, IP range, and even add egress rules.

## 1. Default “Allow-All” Behavior

By default, Kubernetes does **not** restrict pod-to-pod traffic. Any pod in the cluster can communicate with any other pod on any port. To secure your DB pod:

1. Deny all incoming traffic.
2. Explicitly allow only the API pod to connect on port 3306.

## 2. Deny All Ingress to the DB Pod

First, create a policy that selects pods with label `role=db` and blocks **all** ingress:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
```

<Callout icon="lightbulb">
  This policy ensures no traffic can reach the DB pod until you add explicit `ingress` rules.
</Callout>

## 3. Allow Ingress from the API Pod on Port 3306

Next, extend `db-policy` to permit traffic from the API pod:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
      ports:
        - protocol: TCP
          port: 3306
```

<Callout icon="lightbulb">
  Responses from the DB pod back to the API pod are automatically allowed—no `egress` rule is required for reply traffic.
</Callout>

## 4. Restrict API Access by Namespace

If you have multiple namespaces (`dev`, `test`, `prod`), the preceding policy allows API pods from **all** namespaces. To limit to the `prod` namespace, add a `namespaceSelector`:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
          namespaceSelector:
            matchLabels:
              name: prod
      ports:
        - protocol: TCP
          port: 3306
```

<Callout icon="triangle-alert">
  The target namespace must have the label `name=prod` before this selector will match.
</Callout>

## 5. Allow Traffic from an External IP Range

To permit a backup server (e.g., `192.168.5.10/32`) outside your cluster to read from the DB, use an `ipBlock`:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
          namespaceSelector:
            matchLabels:
              name: prod
        - ipBlock:
            cidr: 192.168.5.10/32
      ports:
        - protocol: TCP
          port: 3306
```

Here, matching **either** condition (API pod in `prod` **OR** external IP) grants access.

### Selector Logic

| Combination                                | Semantics                     |
| ------------------------------------------ | ----------------------------- |
| `podSelector` + `namespaceSelector` (same) | AND (both must match)         |
| Multiple entries under `from` or `to`      | OR  (any one entry may match) |

## 6. Adding Egress Rules

If your DB pod must initiate outbound connections (e.g., pushing backups), include `Egress` in `policyTypes` and define an `egress` rule:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
      ports:
        - protocol: TCP
          port: 3306
  egress:
    - to:
        - ipBlock:
            cidr: 192.168.5.10/32
      ports:
        - protocol: TCP
          port: 80
```

This allows the DB pod to send TCP traffic on port 80 to the backup server at `192.168.5.10`.

## Summary of Policy Types

| Policy Type | Controls                            |
| ----------- | ----------------------------------- |
| Ingress     | Incoming traffic to selected pods   |
| Egress      | Outgoing traffic from selected pods |

***

## References

* [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/34baae73-2cab-46bc-b5aa-688076e57052" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/749eb79d-ebfc-40ad-af35-8639abfd721e" />
</CardGroup>
