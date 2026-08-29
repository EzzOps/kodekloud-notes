# Installation Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Installation-Overview/page

Overview of Kubernetes resources and manifests created by Cilium, explaining agents, Envoy, operator, ConfigMaps, ServiceAccounts, RBAC, CRDs, and installation methods

This lesson explains what Kubernetes resources Cilium creates during installation and why each one exists. Later lessons will cover installation methods in depth (Cilium CLI vs. Helm) and guidance for choosing the right option for your environment.

At a high level, installing Cilium will create:

* A DaemonSet to run the Cilium agent on every node
* A DaemonSet to run Envoy (per-node) for L7 functionality
* A Deployment for the cilium-operator (cluster-scoped controller)
* ConfigMaps for agent and Envoy configuration
* ServiceAccounts for each component
* RBAC ClusterRoles and ClusterRoleBindings
* CustomResourceDefinitions (CRDs) used by Cilium (for policies and observability)

Below are representative Kubernetes manifests and concise explanations for the primary components so you can recognize what gets deployed and why.

Table: primary Cilium resources and their purpose

| Resource Type                | Purpose                                                                                   | Example / Notes                                  |
| ---------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------ |
| DaemonSet (cilium)           | Runs one Cilium agent per node to manage datapath, identity, and policy enforcement       | See DaemonSet example below                      |
| DaemonSet (cilium-envoy)     | Runs Envoy on each node for L7 proxying and telemetry                                     | Envoy provides HTTP/gRPC L7 functionality        |
| Deployment (cilium-operator) | Cluster-scoped controller for CRD reconciliation, garbage collection, and node management | Typically deployed with multiple replicas for HA |
| ConfigMap                    | Holds agent and Envoy configuration consumed at runtime                                   | cilium-config, cilium-envoy-config               |
| ServiceAccount               | Isolates permissions for each component                                                   | One per component (agent, envoy, operator)       |
| RBAC (ClusterRole/Binding)   | Grants cluster-wide permissions required by Cilium components                             | Watches/gets/lists nodes, pods, endpoints, etc.  |
| CRDs                         | Enable Cilium-specific APIs (policies, endpoints, telemetry)                              | CiliumNetworkPolicy, CiliumEndpoint, etc.        |

DaemonSet: Cilium agent

```yaml theme={null}
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: cilium
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: cilium
  template:
    metadata:
      labels:
        k8s-app: cilium
    spec:
      containers:
      - name: cilium-agent
        image: "quay.io/cilium/cilium:latest"
        # additional args, env, volume mounts, and securityContext omitted for brevity
```

This DaemonSet ensures a Cilium agent runs on every node. The agent manages datapath programming, identity allocation, policy enforcement, node-local telemetry, and other responsibilities tied to the node's networking stack.

DaemonSet: Cilium Envoy (L7 proxy)

```yaml theme={null}
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: cilium-envoy
  namespace: kube-system
  labels:
    k8s-app: cilium-envoy
spec:
  selector:
    matchLabels:
      k8s-app: cilium-envoy
  template:
    metadata:
      labels:
        k8s-app: cilium-envoy
    spec:
      containers:
      - name: cilium-envoy
        image: "quay.io/cilium/cilium-envoy:latest"
        # Envoy configuration, args, mounts, and readiness/liveness probes omitted
```

The Envoy DaemonSet provides per-node L7 proxying for HTTP/gRPC and richer telemetry. Envoy runs alongside the Cilium agent and handles L7 policies and observability when those features are enabled.

Deployment: Cilium operator

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cilium-operator
  namespace: kube-system
  labels:
    io.cilium/app: operator
spec:
  replicas: 2
  selector:
    matchLabels:
      io.cilium/app: operator
  template:
    metadata:
      labels:
        io.cilium/app: operator
    spec:
      containers:
      - name: cilium-operator
        image: "quay.io/cilium/operator-generic:latest"
        # operator args and RBAC-related permissions are required
```

The operator is a cluster-scoped controller that reconciles Cilium CRDs, performs garbage collection, coordinates node state, and manages cluster-wide workflows. Running multiple replicas improves availability.

ConfigMap: cilium-config (agent settings)

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: cilium-config
  namespace: kube-system
data:
  identity-allocation-mode: crd
  identity-heartbeat-timeout: "30m0s"
  identity-gc-interval: "15m0s"
  cilium-endpoint-gc-interval: "5m0s"
  nodes-gc-interval: "5m0s"
  debug: "false"
  enable-policy: "default"
```

This ConfigMap holds agent configuration values (identity mode, GC intervals, debugging, policy mode, datapath/tunneling options, etc.). You can customize many more settings depending on your cluster topology and feature needs.

ConfigMap: cilium-envoy-config (Envoy bootstrap)

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: cilium-envoy-config
  namespace: kube-system
data:
  # Keep the key name as bootstrap-config.json to avoid breaking changes
  bootstrap-config.json: |
    {
      "admin": {
        "address": {
          "pipe": {
            "path": "/var/run/cilium/envoy/sockets/admin.sock"
          }
        },
        "applicationLogConfig": {
          "logFormat": {
            "textFormat": "[%Y-%m-%d %T.%e][%t][%l][%n] [%g:%#] %v"
          }
        }
      },
      "bootstrapExtensions": [
        {
          "name": "envoy.bootstrap.internal_listener",
          "typedConfig": {}
        }
      ]
    }
```

Envoy requires a bootstrap configuration (JSON/YAML). The key name must remain bootstrap-config.json for compatibility; the snippet above shows a minimal structure for Envoy’s admin interface and bootstrap extensions.

ServiceAccounts

```yaml theme={null}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: "cilium"
  namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: "cilium-envoy"
  namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: "cilium-operator"
  namespace: kube-system
```

Each component uses a dedicated ServiceAccount so you can grant the minimal RBAC permissions required for its tasks.

RBAC: ClusterRole and Binding (example for the agent)

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cilium
  labels:
    app.kubernetes.io/part-of: cilium
rules:
  # rules omitted for brevity: Cilium requires permissions to watch/get/list nodes, pods, endpoints, etc.

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cilium
  labels:
    app.kubernetes.io/part-of: cilium
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cilium
subjects:
- kind: ServiceAccount
  name: "cilium"
  namespace: kube-system
```

ClusterRole and ClusterRoleBinding grant cluster-wide privileges to the component ServiceAccounts. Similar RBAC objects are created for the operator and other components.

> **warning** Cilium requires elevated cluster privileges to watch and manipulate Kubernetes objects (nodes, pods, endpoints, CRDs). Review the RBAC rules before applying manifests in production clusters and follow your security policy for least-privilege access.

CustomResourceDefinitions (CRDs)

Cilium installs several CRDs that enable high-level APIs for policy, visibility, and endpoint resources (for example: CiliumNetworkPolicy, CiliumClusterwideNetworkPolicy, CiliumEndpoint). These CRDs allow controllers and the operator to persist and reconcile Cilium-specific state.

For more on Kubernetes CRDs, see: [https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

Putting it together — what to expect after installation

* Node-local pods: cilium and cilium-envoy run across nodes via DaemonSets.
* Cluster controller: cilium-operator runs as a Deployment with replicas.
* Configuration: cilium-config and cilium-envoy-config ConfigMaps are created.
* Security: ServiceAccounts and RBAC ClusterRoles/Bindings grant required permissions.
* APIs: Cilium CRDs are registered for policy and resource management.

> **lightbulb** If you inspect a cluster after installing Cilium, look in the kube-system namespace for DaemonSets (cilium, cilium-envoy), the cilium-operator Deployment, ConfigMaps (cilium-config, cilium-envoy-config), component ServiceAccounts, and multiple Cilium-related CRDs.

Installation methods — CLI vs. Helm

There are two primary ways to install Cilium on Kubernetes:

1. Cilium CLI
   * The Cilium project provides a dedicated CLI (cilium) that generates and applies per-environment manifests.
   * The CLI bundles necessary tooling and renders Helm templates internally, so you do not need to install Helm separately.
   * See: [https://docs.cilium.io/en/stable/gettingstarted/cilium-cli/](https://docs.cilium.io/en/stable/gettingstarted/cilium-cli/)

2. Helm
   * Install Cilium by adding the official Helm repository and deploying the chart for a specific version.
   * Helm gives granular control over chart values and integrates naturally with GitOps workflows.
   * See: [https://github.com/cilium/helm-charts](https://github.com/cilium/helm-charts) and [Helm documentation](https://helm.sh/docs/)

> **lightbulb** Note: The Cilium CLI internally uses Helm templates to render manifests. Whether you install via the CLI or Helm directly, Helm templates are involved in producing the manifests applied to the cluster.

References and further reading

* Cilium documentation: [https://docs.cilium.io/](https://docs.cilium.io/)
* Cilium CLI getting started: [https://docs.cilium.io/en/stable/gettingstarted/cilium-cli/](https://docs.cilium.io/en/stable/gettingstarted/cilium-cli/)
* Envoy proxy: [https://www.envoyproxy.io/](https://www.envoyproxy.io/)
* Kubernetes CRDs: [https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* Helm: [https://helm.sh/docs/](https://helm.sh/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/9987f86b-1de8-4f71-b0fc-340d906bdb63)
