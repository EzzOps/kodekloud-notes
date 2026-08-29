# expected output:
# operator-sdk_linux_amd64: OK
```

Make the binary executable and move it into a location on your PATH:

```bash theme={null}
chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/local/bin/operator-sdk
```

### macOS (Homebrew)

You can also install via Homebrew on macOS:

```bash theme={null}
brew install operator-sdk
```

Verify the CLI is available and inspect the binary metadata:

```bash theme={null}
operator-sdk version
# sample output:
# operator-sdk version: "v1.42.2", commit: "[AWS_SECRET_ACCESS_KEY]", kubernetes version: "1.33.1", go version: "go1.25.7", GOOS: "linux", GOARCH: "amd64"
```

Note: the reported "kubernetes version" refers to the Kubernetes client libraries bundled with the SDK binary, not your cluster version.

<Callout icon="lightbulb">
  If you are already familiar with the [Kubebuilder](https://learn.kodekloud.com/user/courses/kubernetes-operators) scaffold, the operator-sdk Go scaffold will feel familiar: you still write API types and a reconciler, and you still run a controller manager. operator-sdk layers additional tooling and plugins (manifests, scorecard, OLM) around that shared foundation.
</Callout>

## Initialize a clean Go operator-sdk project

Start from an empty directory (for disposable workspaces you may run `rm -rf *`).

```bash theme={null}
rm -rf *
operator-sdk init --domain=kodekloud.com --repo=github.com/kodekloud/webapp-sdk --plugins=go/v4
```

What to watch for as the project initializes:

* controller-runtime and Go module setup (the same controller-runtime library Kubebuilder uses).
* Code generation steps (e.g., `make generate`, `go generate`) and `go mod tidy`.

This confirms the operator runtime foundation (manager, client, event watching, reconcile loop) is shared between Kubebuilder and operator-sdk.

## Create the WebApp API and controller

Scaffold the API group `webapp`, version `v1`, and kind `WebApp`. Use `--resource` to scaffold the CRD types and `--controller` to add a reconciler skeleton.

```bash theme={null}
operator-sdk create api --group webapp --version v1 --kind WebApp --resource --controller
```

Typical generated artifacts:

* `api/v1/webapp_types.go`
* `internal/controller/webapp_controller.go`
* `internal/controller/webapp_controller_test.go`

The SDK also runs `go mod tidy` and the codegen tasks to produce boilerplate.

## Inspect the generated code

API types are located under `api/v1`. The reconciler skeleton is under `internal/controller` (in some layouts it may appear under `controllers`). This separation mirrors the conceptual boundaries used by Kubebuilder.

A corrected sample of the generated list type (ensure your generated `WebAppList` resembles this):

```go theme={null}
package v1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// WebAppList contains a list of WebApp
type WebAppList struct {
    metav1.TypeMeta `json:",inline"`
    metav1.ListMeta `json:"metadata,omitempty"`
    Items           []WebApp `json:"items"`
}

func init() {
    SchemeBuilder.Register(&WebApp{}, &WebAppList{})
}
```

## Generate manifests

After you implement API fields and reconciliation logic, generate the manifests (CRDs, RBAC, webhook manifests if applicable):

```bash theme={null}
make manifests
```

This produces the CRD YAML, RBAC roles, and other required manifests for deploying your operator.

## Comparing the PROJECT layout

The `PROJECT` file is the most useful artifact when comparing scaffolds. It records the project layout and plugins the scaffold used. operator-sdk, when configured with the Kubebuilder Go layout, will include entries reflecting the Go layout plus operator-sdk plugins (manifests, scorecard, OLM).

Representative `PROJECT` fragment:

```yaml theme={null}
domain: kodekloud.com
layout:
  - go.kubebuilder.io/v4
plugins:
  manifests.sdk.operatorframework.io/v2: {}
  scorecard.sdk.operatorframework.io/v2: {}
projectName: webapp-sdk
repo: github.com/kodekloud/webapp-sdk
resources:
  - api:
      crdVersion: v1
      namespaced: true
      controller: true
      domain: kodekloud.com
      group: webapp
      kind: WebApp
      path: github.com/kodekloud/webapp-sdk/api/v1
      version: v1
version: "3"
```

Quick comparison table: Kubebuilder vs operator-sdk scaffolds

| Area                   | Kubebuilder               | Operator SDK (Go plugin)                              |
| ---------------------- | ------------------------- | ----------------------------------------------------- |
| Controller runtime     | controller-runtime (same) | controller-runtime (same)                             |
| Project layout         | Kubebuilder Go layout     | Kubebuilder Go layout (via plugin)                    |
| Extra tooling          | Minimal by default        | Plugins for manifests, scorecard, OLM, packaging      |
| Common files           | `api/`, `controllers/`    | `api/`, `internal/controller/` (layout may vary)      |
| Packaging & validation | Manual or external        | Built-in plugin support for OLM, scorecard, manifests |

Files you typically see after scaffold:

| Path                                       | Purpose                                           |
| ------------------------------------------ | ------------------------------------------------- |
| `api/v1/webapp_types.go`                   | API type definitions and CRD annotations          |
| `api/v1/webapp_webhook.go`                 | (Optional) Webhook scaffolding                    |
| `internal/controller/webapp_controller.go` | Reconciler skeleton and business logic entrypoint |
| `PROJECT`                                  | Records layout, plugins, and resources            |
| `config/` or `make` targets                | Generated manifests and deployment resources      |

## Key takeaway

The operator-sdk Go plugin uses the same controller-runtime and Kubebuilder-style project layout. The primary differences are the tooling additions and plugins operator-sdk provides for packaging, validation, and distribution (OLM/scorecard). If you understand the Kubebuilder workflow, the operator-sdk Go scaffold will be immediately recognizable and comfortable to work with.

## Links and references

* [Operator SDK Releases](https://github.com/operator-framework/operator-sdk/releases)
* [Kubebuilder / Kubernetes Operators course](https://learn.kodekloud.com/user/courses/kubernetes-operators)
* [controller-runtime documentation](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/d2537d70-4008-4d53-ad04-b7731ca0f7c0/lesson/0a8c350b-f62f-4772-8899-ee7f3c567bf6" />
</CardGroup>


# Helm Based Operators Wrap A Chart As An Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Alternative-Approaches-Operator-SDK-Helm-Operator/Helm-Based-Operators-Wrap-A-Chart-As-An-Operator/page

Describes wrapping Helm charts as operators to expose Kubernetes CRDs that automate chart install upgrade and uninstall by reconciling custom resources to Helm releases

Helm-based operators solve a common operational question: what if your application is already packaged as a Helm chart, but you want a Kubernetes-native API (CRDs) to manage it instead of running Helm commands manually?

<Frame>
  <img alt="The image is a slide that discusses already having an &#x22;Application Helm Chart&#x22; but expressing a need for an API. It includes a document icon labeled &#x22;HELM&#x22; with a Helm logo." />
</Frame>

Conceptually, a chart stays useful: the operator simply runs a control loop that renders and applies the chart on behalf of Kubernetes users.

Think of a Helm chart as a recipe book. With plain Helm, a human or CI pipeline runs the recipe:

```bash theme={null}
$ helm install my-release ./my-chart
```

A Helm-based operator instead puts that recipe behind a Kubernetes API. A user creates a custom resource (CR), and the operator continuously reconciles that CR into the corresponding Helm release:

```yaml theme={null}
apiVersion: myapp.io/v1
kind: MyApp
spec:
  replicas: 3
```

Plain Helm requires someone or some pipeline to run install/upgrade/uninstall at the right time. A Helm-based operator watches the cluster and reacts automatically: when a CR is created, updated, or deleted, the operator performs the corresponding Helm workflow.

<Frame>
  <img alt="The image compares &#x22;Plain Helm&#x22; and &#x22;Helm-Based Operator,&#x22; highlighting that Plain Helm involves manual command execution by a person or pipeline, while Helm-Based Operator continuously watches the cluster and reacts through Helm workflows when changes occur." />
</Frame>

This pattern is especially valuable for teams that already trust a chart: the chart remains the canonical source of manifests while the operator exposes a Kubernetes-native API for create/update/delete operations.

<Frame>
  <img alt="The image explains the benefits of wrapping a chart, highlighting that it is useful for teams that already trust a chart and that the chart remains the source of Kubernetes manifests." />
</Frame>

The key technical bridge is the mapping between the custom resource spec and the chart values. A chart typically exposes settings like image, replica count, service type, and port. In a Helm-based operator, these chart values become fields on the custom resource spec:

```yaml theme={null}
apiVersion: myapp.io/v1
kind: MyApp
spec:
  image: myapp:v1.2.0
  replicaCount: 3
  service:
    type: ClusterIP
    port: 8080
```

When a field changes, the next reconcile renders the chart with updated values and applies the resulting manifests to the cluster.

<Frame>
  <img alt="The image depicts a workflow diagram showing a user interacting with a Kubernetes API, specifically with Helm actions. It describes the process of a user creating, updating, or deleting a custom resource that is managed by an operator." />
</Frame>

Operator SDK includes a Helm plugin that scaffolds this style of project. Instead of writing a custom Go reconcile loop, the project contains chart content and a watches configuration to link a Kubernetes group/version/kind to a specific Helm chart.

Initialize a Helm-based operator with Operator SDK:

```bash theme={null}
$ operator-sdk init --plugins=helm/v1
```

Then map the custom resource to the chart in `watches.yaml`:

```yaml theme={null}
