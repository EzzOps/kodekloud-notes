# Lab Solution Build The WebApp Operator Scaffold

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Kubebuilder-Scaffolding/Lab-Solution-Build-The-WebApp-Operator-Scaffold/page

Guide to recreate a Kubebuilder webapp-operator scaffold, generate CRDs and RBAC, register API scheme, and build the manager binary to verify the project compiles.

This lesson walks through recreating the webapp-operator scaffold using Kubebuilder. The objective is to:

* Initialize the project with the exact course identifiers,
* Generate CRD manifests from your API types,
* Build the manager binary to verify the scaffold compiles.

Follow the numbered steps below in order and watch for common slip points noted along the way.

1. Initialize the Kubebuilder project scaffold

Run kubebuilder init with the exact domain, repository, and project name. These identifiers are critical because downstream labs and generated import paths depend on them.

```bash theme={null}
kubebuilder init --domain kodekloud.com --repo github.com/kodekloud/webapp-operator --project-name webapp-operator
```

<Callout icon="lightbulb">
  Make sure the `--domain`, `--repo`, and `--project-name` values exactly match the course. If these are incorrect, the fully qualified group names and import paths will differ and later steps will fail.
</Callout>

2. Add the WebApp API

Create the API group, version, and kind. Use `--resource` to generate API types and `--controller` to scaffold a reconciler:

```bash theme={null}
kubebuilder create api --group webapp --version v1 --kind WebApp --resource --controller
```

* `--resource` generates the Go types for the custom resource (CR).
* `--controller` scaffolds the reconciler (controller) skeleton that watches and reconciles WebApp objects.

After this command completes, confirm the following generated files and locations:

| File / Path                        | Purpose                                            |
| ---------------------------------- | -------------------------------------------------- |
| `api/v1/webapp_types.go`           | API type definitions (CR spec/status structs)      |
| `api/v1/groupversion_info.go`      | Group/version registration helpers                 |
| `controllers/webapp_controller.go` | Reconciler scaffold and reconcile logic entrypoint |
| `controllers/suite_test.go`        | Test harness for the controllers                   |
| `cmd/main.go`                      | Manager bootstrap, including scheme registration   |

3. Inspect scheme registration in cmd/main.go

Open `cmd/main.go` and ensure your API package registers with the manager's scheme. This registration lets controller-runtime encode/decode `webapp.kodekloud.com/v1` objects.

A typical snippet looks like:

```go theme={null}
package main

import (
    utilruntime "k8s.io/apimachinery/pkg/util/runtime"
    "k8s.io/apimachinery/pkg/runtime"
    clientgoscheme "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    webappv1 "github.com/kodekloud/webapp-operator/api/v1"
)

var (
    scheme   = runtime.NewScheme()
    setupLog = ctrl.Log.WithName("setup")
)

func init() {
    utilruntime.Must(clientgoscheme.AddToScheme(scheme))
    utilruntime.Must(webappv1.AddToScheme(scheme))
}

// main continues with manager setup...
```

If the call to `webappv1.AddToScheme(scheme)` is missing, the manager will not recognize your CRD types at runtime.

4. Generate CRD manifests

Generate CRD YAML and RBAC manifests using the project's Makefile target, which runs `controller-gen` and produces artifacts under `config/`:

```bash theme={null}
make manifests
```

You should see output similar to:

```plaintext theme={null}
/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
```

Confirm the CRD YAML exists in `config/crd/bases` and follows the naming pattern `group_domain_plural.yaml`, for example:

* `webapp.kodekloud.com_webapps.yaml`

<Callout icon="lightbulb">
  If the CRD file is missing or out of date, you most likely edited the Go type definitions without rerunning `make manifests`. Always regenerate manifests after changing API types.
</Callout>

5. Sanity build the manager binary

Compile the project to verify it builds cleanly:

```bash theme={null}
make build
```

This runs a build that produces `bin/manager`. You can also run the equivalent steps manually:

```bash theme={null}
go fmt ./...
go vet ./...
go build -o bin/manager ./cmd/main.go
```

If the build fails, examine the compiler errors for missing imports or incorrectly defined types in `api/` or `controllers/`.

6. Confirm project metadata (PROJECT file)

Kubebuilder stores project-wide settings in the `PROJECT` file at the repository root. Verify the domain, repo, project name, and resources entry. A representative `PROJECT` YAML:

```yaml theme={null}
cliVersion: 4.14.0
domain: kodekloud.com
layout:
  - go.kubebuilder.io/v4
projectName: webapp-operator
repo: github.com/kodekloud/webapp-operator
resources:
  - api:
      crdVersion: v1
      namespaced: true
      controller: true
      domain: kodekloud.com
      group: webapp
      kind: WebApp
      path: github.com/kodekloud/webapp-operator/api/v1
      version: v1
version: "3"
```

Verify the `resources` entry lists `group: webapp`, `version: v1`, `kind: WebApp`, and the correct `domain` and `path`. Mismatches here lead to incorrect scaffold behavior and import path errors.

7. Summary & next steps

* `kubebuilder init` sets up the project with the correct domain/repo/project name.
* `kubebuilder create api` adds the API types and controller scaffold.
* `make manifests` generates CRD YAML from API markers.
* `make build` compiles the manager binary to confirm the scaffold is valid.

This scaffold is the skeleton of your operator. After validating it, implement the controller logic in `controllers/webapp_controller.go`, update your API types in `api/v1/webapp_types.go`, and keep regenerating manifests whenever you modify the API.

Links and references

* Kubebuilder: [https://book.kubebuilder.io/](https://book.kubebuilder.io/)
* controller-runtime: [https://pkg.go.dev/sigs.k8s.io/controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* controller-gen: [https://pkg.go.dev/sigs.k8s.io/controller-tools/cmd/controller-gen](https://pkg.go.dev/sigs.k8s.io/controller-tools/cmd/controller-gen)
* Go tooling: [https://golang.org/doc/](https://golang.org/doc/) and `go build`, `go vet`, `go fmt` documentation

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/20a4ec01-fde8-466d-83c7-2f74f6def1f0/lesson/f616b402-bc78-4ed6-af13-1c4f7b96beae" />
</CardGroup>
