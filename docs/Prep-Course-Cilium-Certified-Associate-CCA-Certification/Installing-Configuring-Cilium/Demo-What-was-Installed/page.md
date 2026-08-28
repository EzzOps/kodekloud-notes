# removed k8s-require-ipv6-pod-cidr
```

After saving the edit you should see:

```text theme={null}
configmap/cilium-config edited
```

<Callout icon="warning">
  If Cilium is managed by Helm, the `cilium-config` ConfigMap may be owned by the Helm release. Direct edits with `kubectl` can be overwritten by future `helm upgrade` or `helm rollback` actions. Prefer updating Helm values when possible or coordinate ConfigMap edits with your Helm values.
</Callout>

## 4 — Restart Cilium components so changes take effect

After modifying the ConfigMap (or after a Helm upgrade), restart the operator and agent so they pick up the new configuration.

Restart the operator (Deployment) and the agent (DaemonSet):

```bash theme={null}
kubectl rollout restart deployment cilium-operator -n kube-system
kubectl rollout restart daemonset cilium -n kube-system
```

Example outputs:

```text theme={null}
deployment.apps/cilium-operator restarted
daemonset.apps/cilium restarted
```

Monitor pod status while they restart:

```bash theme={null}
kubectl get pods -A --watch
```

Wait until the new Cilium pods reach `Running` status. Init containers may take a short while to complete.

<Callout icon="lightbulb">
  After changing the Cilium ConfigMap, you must restart the operator and agent pods so the new configuration is applied.
</Callout>

## 5 — Verify the change (example: confirm IPv6 disabled)

Create a test pod:

```bash theme={null}
kubectl run nginx --image=nginx --restart=Never
kubectl get pods -w
```

Describe the test pod to inspect assigned IP(s):

```bash theme={null}
kubectl describe pod nginx
```

Relevant excerpt showing only an IPv4 address (IPv6 disabled):

```text theme={null}
IP:             10.0.2.163
IPs:
  IP:           10.0.2.163
```

## Troubleshooting tips

* If changes do not appear to apply:
  * Verify you edited the correct ConfigMap and namespace.
  * Confirm the Cilium Helm release is not overwriting settings (check `helm get values <release> -n <ns>`).
  * Check operator and agent logs for errors:
    ```bash theme={null}
    kubectl logs -l k8s-app=cilium -n kube-system --tail=200
    kubectl logs deployment/cilium-operator -n kube-system --tail=200
    ```
* For transient issues after restart, allow a few minutes for init containers and datapath programs to reinitialize.

## Summary

* Prefer updating the Helm `values.yaml` and running `helm upgrade` when Cilium was installed with Helm—this preserves configuration in the release.
* Editing the `cilium-config` ConfigMap is useful for quick runtime changes or on clusters where Cilium was not installed with Helm. After editing, restart the `cilium-operator` deployment and the `cilium` daemonset so changes take effect.
* Always validate changes by creating test pods and checking their assigned IPs and Cilium logs.

## Links and references

* [Cilium Documentation](https://docs.cilium.io/)
* [Kubernetes Documentation — Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
* [Helm Documentation](https://helm.sh/docs/)
* [KodeKloud Helm course](https://learn.kodekloud.com/user/courses/helm-for-beginners)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/99b26348-588c-4672-afd9-92851a2b81fe" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/abfc64d5-1dba-4802-a679-e5857635ef8b" />
</CardGroup>


# Demo What was Installed

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Demo-What-was-Installed/page

Overview of Kubernetes resources Cilium installs and how to inspect components, ConfigMaps, Secrets, RBAC, CRDs, DaemonSets, Deployments and optional Hubble observability

In this lesson we inspect the Kubernetes resources that Cilium creates when deployed. You'll see how Cilium components (agents, Envoy proxies, operator), configuration (ConfigMaps, Secrets), RBAC (Roles / ClusterRoles / Bindings), and CRDs are laid out in the cluster and which commands to use to verify them.

<Frame>
  <img alt="A presentation slide reading &#x22;What was Installed&#x22; on the left and a teal curved shape on the right with the word &#x22;Demo.&#x22; The bottom-left corner shows a small &#x22;© Copyright KodeKloud&#x22; label." />
</Frame>

## Key Cilium components

* Cilium agent: runs as a DaemonSet (one agent per node) and provides datapath, policy enforcement, and connectivity.
* Envoy proxies: run as a DaemonSet for L7 and load-balancing features.
* Cilium Operator: deployed as a Deployment and manages Cilium CRs and cluster-wide tasks.
* Hubble (optional): observability/flow-visibility components (server/relay) when enabled.

Use the following table to quickly map installed resources to their roles and typical names:

| Resource Type                    | Purpose                                  | Example resource(s)                                                |
| -------------------------------- | ---------------------------------------- | ------------------------------------------------------------------ |
| DaemonSet                        | Per-node agent or proxy                  | `cilium`, `cilium-envoy`                                           |
| Deployment                       | Cluster operator                         | `cilium-operator`                                                  |
| ConfigMap                        | Runtime configuration for agents/proxies | `cilium-config`, `cilium-envoy-config`                             |
| Secret                           | TLS certificates, Helm release info      | `cilium-ca`, `hubble-server-certs`, `sh.helm.release.v1.cilium.v1` |
| ServiceAccount                   | API authentication for components        | `cilium`, `cilium-envoy`, `cilium-operator`                        |
| ClusterRole / Role               | RBAC permissions                         | `cilium`, `cilium-operator`                                        |
| ClusterRoleBinding / RoleBinding | Bind permissions to ServiceAccounts      | `cilium`, `cilium-operator`                                        |
| CRD                              | Cilium-specific resources                | `ciliumendpoints.cilium.io`, `ciliumidentities.cilium.io`, ...     |

## Verify DaemonSets

List DaemonSets in the kube-system namespace:

```bash theme={null}
kubectl get daemonset -n kube-system
```

Example output:

```text theme={null}
NAME           DESIRED  CURRENT  READY  UP-TO-DATE  AVAILABLE  NODE SELECTOR               AGE
cilium         3        3        3      3           3          kubernetes.io/os=linux     5h53m
cilium-envoy   3        3        3      3           3          kubernetes.io/os=linux     5h53m
kube-proxy     3        3        3      3           3          kubernetes.io/os=linux     6h2m
```

## Inspect running pods

List pods in kube-system to confirm running instances:

```bash theme={null}
kubectl get pod -n kube-system
```

Representative output (trimmed):

```text theme={null}
NAME                                                  READY   STATUS    RESTARTS   AGE
cilium-2sj75                                          1/1     Running   0          5h53m
cilium-envoy-cpsft                                    1/1     Running   0          5h53m
cilium-envoy-j9gx9                                    1/1     Running   0          5h53m
cilium-envoy-vm54m                                    1/1     Running   0          5h53m
cilium-k8bvb                                          1/1     Running   0          5h53m
cilium-mt449                                          1/1     Running   0          5h53m
cilium-operator-59944f4b8f-kwkbc                      1/1     Running   0          5h53m
cilium-operator-59944f4b8f-wqxw7                      1/1     Running   0          5h53m
coredns-668d6bf9bc-4bqmj                              1/1     Running   0          6h3m
coredns-668d6bf9bc-h8kzk                              1/1     Running   0          6h3m
...
```

Describe a single Cilium agent pod to view container details (image, args, mounts, etc.):

```bash theme={null}
kubectl describe pod cilium-2sj75 -n kube-system
```

Important excerpt (trimmed for clarity):

```text theme={null}
Containers:
  cilium-agent:
    Container ID:  containerd://c05cc9963bfe284e57...
    Image:         quay.io/cilium/cilium:v1.17.2@sha256:3c4c9932b5d8368619cb922a497ff2ebc8def5f41c18e410bcc84025fcd385b1
    Command:
      cilium-agent
    Args:
      --config-dir=/tmp/cilium/config-map
    State:         Running
    Started:       Tue, 25 Mar 2025 21:26:48 +0000
    Ready:         True
    Restart Count: 0
Mounts:
  /host/opt/cni/bin from cni-path (rw)
  /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-kgxtt (ro)
```

Note: the Cilium agent reads configuration from a ConfigMap mounted into the container under the path passed to `--config-dir`.

## Inspect ConfigMaps and runtime configuration

List ConfigMaps in kube-system:

```bash theme={null}
kubectl get configmap -n kube-system
```

Example output:

```text theme={null}
NAME                                                     DATA   AGE
cilium-config                                            145    5h59m
cilium-envoy-config                                      1      5h59m
coredns                                                  1      6h9m
...
```

Describe (or view) the main Cilium ConfigMap to see keys and values originating from your Helm `values.yaml`:

```bash theme={null}
kubectl describe configmap cilium-config -n kube-system
```

Example snippets (trimmed):

```text theme={null}
enable-l7-proxy:
----
true

enable-ipv6:
----
true

arping-refresh-period:
----
30s
```

When you change values in your Helm `values.yaml` and reinstall or upgrade Cilium, those values are populated into these ConfigMaps. The Cilium agent and Envoy pick up configuration from the mounted files; some settings are read at process start and may require a pod restart.

## Cilium Operator (Deployment)

List deployments in kube-system:

```bash theme={null}
kubectl get deployment -n kube-system
```

Example:

```text theme={null}
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
cilium-operator           2/2     2            2           6h1m
coredns                   2/2     2            2           6h11m
```

## Secrets, ServiceAccounts, and RBAC

List Secrets in kube-system:

```bash theme={null}
kubectl get secret -n kube-system
```

Example output:

```text theme={null}
NAME                               TYPE                                DATA   AGE
bootstrap-token-abcdef             bootstrap.kubernetes.io/token       6      6h11m
cilium-ca                          Opaque                              2      6h1m
hubble-server-certs                kubernetes.io/tls                   3      6h1m
sh.helm.release.v1.cilium.v1       helm.sh/release.v1                  1      6h1m
```

List ServiceAccounts:

```bash theme={null}
kubectl get sa -n kube-system
```

Look for Cilium-related accounts:

```text theme={null}
NAME            SECRETS   AGE
cilium          0         6h2m
cilium-envoy    0         6h2m
cilium-operator 0         6h2m
...
```

Cilium requires specific permissions to interact with cluster resources. These are defined via Roles / ClusterRoles and bound to ServiceAccounts through RoleBindings / ClusterRoleBindings.

List Roles:

```bash theme={null}
kubectl get roles -n kube-system
```

Find Cilium ClusterRoles:

```bash theme={null}
kubectl get clusterroles | grep -i cilium
```

Example output:

```text theme={null}
cilium                                         2025-03-25T21:26:26Z
cilium-operator                                2025-03-25T21:26:26Z
```

Describe a ClusterRole to inspect granted verbs/resources:

```bash theme={null}
kubectl describe clusterrole cilium
```

Representative excerpt:

```text theme={null}
PolicyRule:
  Resources                                      Non-Resource URLs  Resource Names  Verbs
  ---------                                      -----------------  --------------  -----
  endpoints                                      []                 []              [get list watch]
  namespaces                                     []                 []              [get list watch]
  nodes                                          []                 []              [get list watch]
  pods                                           []                 []              [get list watch]
  services                                       []                 []              [get list watch]
  endpointslices.discovery.k8s.io                []                 []              [get list watch]
  networkpolicies.networking.k8s.io              []                 []              [get list watch]
  ciliumnodes.cilium.io/status                   []                 []              [get update]
  ciliumendpoints.cilium.io                      []                 []              [list watch create delete get patch]
  ...
```

Check ClusterRoleBindings that bind ClusterRoles to ServiceAccounts:

```bash theme={null}
kubectl get clusterrolebinding | grep -i cilium
```

Example:

```text theme={null}
cilium                                  6h5m    ClusterRole/cilium
cilium-operator                         6h5m    ClusterRole/cilium-operator
```

Describe a binding to confirm subjects:

```bash theme={null}
kubectl describe clusterrolebinding cilium
```

Excerpt:

```text theme={null}
Subjects:
  Kind             Name      Namespace
  ----             ----      ---------
  ServiceAccount   cilium    kube-system
```

## CustomResourceDefinitions (CRDs)

Cilium installs multiple CRDs used for policy, endpoints, identities, and other Cilium-specific resources:

```bash theme={null}
kubectl get crd
```

Example output (trimmed):

```text theme={null}
NAME                                           CREATED AT
ciliumcidrgroups.cilium.io                    2025-03-25T21:26:33Z
ciliumclusterwidenetworkpolicies.cilium.io    2025-03-25T21:26:33Z
ciliumendpoints.cilium.io                     2025-03-25T21:26:33Z
ciliumexternalworkloads.cilium.io             2025-03-25T21:26:33Z
ciliumidentities.cilium.io                    2025-03-25T21:26:33Z
...
```

## Hubble (optional)

Hubble provides observability and flow visibility. If Hubble server/relay was not enabled in Helm values during installation, you will not see Hubble pods/services. Enabling Hubble in your Helm `values.yaml` creates additional resources (server, relay, certificates, etc.).

<Callout icon="lightbulb">
  ConfigMap and Secret contents are available inside running Cilium containers because the files are mounted as volumes. Updating a ConfigMap updates the file contents inside the pod, but some components only read their config at process start—so you may need to restart pods for those changes to take effect.
</Callout>

## Links and references

* [Kubernetes documentation](https://kubernetes.io/docs/)
* [Cilium documentation](https://cilium.io/docs/)
* [Helm for beginners (KodeKloud)](https://learn.kodekloud.com/user/courses/helm-for-beginners)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/1448f3dc-8b74-4844-86e2-c8342175e92d" />
</CardGroup>
