# This file is used to track the info used to scaffold
# and allow the plugins to properly work.
cliVersion: 4.13.1
domain: kodekloud.com
layout:
  - go.kubebuilder.io/v4
projectName: webapp-operator
repo: github.com/kodekloud/webapp-operator
resources:
  api:
```

When scaffolding runs, you'll see informative logs about files created and dependency updates, for example:

```bash theme={null}
INFO  internal/controller/webapp_controller.go
INFO  internal/controller/webapp_controller_test.go
INFO  Update dependencies
INFO  Running make
Downloading sigs.k8s.io/controller-tools/cmd/controller-gen@v0.20.1
```

## Generated Go types (example)

Kubebuilder scaffolds `api/v1/webapp_types.go` with placeholder fields. The `WebAppSpec` currently contains a `Foo` example field and `WebAppStatus` includes a `Conditions` slice prepared for status conditions. Keep these placeholders while following this lesson; a later lab replaces `Foo` with real fields such as `image` and `replicas`.

Example generated types:

```go theme={null}
package v1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required. Any new fields you add must have json tags
// so the fields can be serialized.

// WebAppSpec defines the desired state of WebApp
type WebAppSpec struct {
    // INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
    // Important: Run "make" to regenerate code after modifying this file
    // The following markers will use OpenAPI v3 schema to validate the value
    // More info: https://book.kubebuilder.io/reference/markers/crd-validation.html

    // Foo is an example field of WebApp. Edit webapp_types.go to remove/update
    // +optional
    Foo *string `json:"foo,omitempty"`
}

// WebAppStatus defines the observed state of WebApp.
type WebAppStatus struct {
    // For Kubernetes API conventions, see:
    // https://github.com/kubernetes/[AWS_SECRET_ACCESS_KEY]/
    // sig-architecture/api-conventions.md#typical-status-properties
    //
    // conditions represent the current state of the WebApp resource.
    // Each condition has a unique type and reflects the status of a specific
    // aspect of the resource.
    //
    // Standard condition types include:
    // - "Available": the resource is fully functional
    // - "Progressing": the resource is being created or updated
    // - "Degraded": the resource failed to reach or maintain its desired state
    //
    // The status of each condition is one of True, False, or Unknown.
    // +listType=map
    // +listMapKey=type
    // +optional
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status

// WebApp is the Schema for the webapps API
type WebApp struct {
    metav1.TypeMeta   `json:",inline"`
    // metadata is standard object metadata
    // +optional
    metav1.ObjectMeta `json:"metadata,omitempty"`

    // spec defines the desired state of WebApp
    Spec WebAppSpec `json:"spec,omitempty"`
    // status defines the observed state of WebApp
    // +optional
    Status WebAppStatus `json:"status,omitempty"`
}
```

<Callout icon="lightbulb">
  Kubebuilder marker comments such as `+kubebuilder:object:root=true` and
  `+kubebuilder:subresource:status` are directives for the code generator (controller-gen).
  They control what gets generated in the CRD YAML and client code.
</Callout>

## Generate CRD YAML from types

To convert the Go types (the single source of truth) into a Kubernetes CustomResourceDefinition (CRD) YAML, run:

```bash theme={null}
make manifests
```

Under the hood, `make manifests` runs `controller-gen` which parses the Kubebuilder markers and writes the CRD base file into `config/crd/bases`. Kubebuilder names the CRD file using the group and plural form, for example:

`config/crd/bases/webapp.kodekloud.com_webapps.yaml`

A small excerpt of the generated CRD (shows identity and inferred schema):

```yaml theme={null}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.20.1
  name: webapps.webapp.kodekloud.com
spec:
  group: webapp.kodekloud.com
  names:
    kind: WebApp
    listKind: WebAppList
    plural: webapps
    singular: webapp
  scope: Namespaced
  versions:
    - name: v1
      schema:
        openAPIV3Schema:
          description: WebApp is the Schema for the webapps API
          properties:
            apiVersion:
              description: |-
                APIVersion defines the versioned schema of this representation
                of an object.
              type: string
            kind:
              description: |-
                Kind is a string value representing the REST resource this
                object represents.
```

From this CRD YAML you can immediately read:

* metadata `name: webapps.webapp.kodekloud.com`
* `group: webapp.kodekloud.com`
* `kind: WebApp`, `listKind: WebAppList`
* `plural: webapps`, `singular: webapp`
* version `v1` and status subresource enabled

## Verify compilation & development loop

Before editing types and controller logic, ensure the scaffold builds cleanly. A typical development loop is:

1. Scaffold the API:
   ```bash theme={null}
   kubebuilder create api --group webapp --version v1 --kind WebApp --resource --controller
   ```
2. Regenerate CRD manifests:
   ```bash theme={null}
   make manifests
   ```
3. Build and test the controller:
   ```bash theme={null}
   make build
   # or build a container image:
   make docker-build
   # or run locally
   make run
   ```

## Next steps

* Re-run `kubebuilder create api` if you need to add more APIs for the same project.
* Replace placeholder fields in `api/v1/webapp_types.go` with real spec fields (for example `image` and `replicas`).
* Implement controller logic in `internal/controller` to create and manage child resources such as `Service`, `Deployment`, and `ConfigMap` for each WebApp.

Recommended references:

* Kubebuilder docs: [https://book.kubebuilder.io/](https://book.kubebuilder.io/)
* controller-tools (controller-gen): [https://github.com/kubernetes-sigs/controller-tools](https://github.com/kubernetes-sigs/controller-tools)
* Kubernetes API conventions: [https://github.com/kubernetes/[AWS_SECRET_ACCESS_KEY]/sig-architecture/api-conventions.md](https://github.com/kubernetes/[AWS_SECRET_ACCESS_KEY]/sig-architecture/api-conventions.md)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/20a4ec01-fde8-466d-83c7-2f74f6def1f0/lesson/d932751a-9d7f-4073-980a-8e0b11d2ac32" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/20a4ec01-fde8-466d-83c7-2f74f6def1f0/lesson/0c4c1572-2b9f-4864-906e-fd837e90b838" />
</CardGroup>


# Demo Kubebuilder Init

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Kubebuilder-Scaffolding/Demo-Kubebuilder-Init/page

Guide to initializing a Kubebuilder operator project, scaffolding a Go-based Kubernetes operator skeleton, and verifying build and tooling

Where do you actually start when building a Kubernetes operator?

Handwriting the Go module, Makefile, directory tree, and all the wiring that connects your controller to the Kubernetes API can be hours of boilerplate before a single line of real logic. Kubebuilder solves that problem by scaffolding a complete operator project so you can skip straight to the interesting parts.

In this guide you'll initialize a new Kubebuilder project and verify the generated skeleton builds. By the end you will have:

* A buildable Go module
* A working `Makefile`
* The controller-runtime manager entry point

This is a practical first step toward creating APIs, controllers, and webhooks with Kubebuilder.

## Prerequisites

* Go installed and available on your `PATH`. If `go version` fails, install Go from the official Go installation page: [https://go.dev/doc/install](https://go.dev/doc/install)

Check Go:

```bash theme={null}
$ go version
go version go1.26.3 linux/amd64
```

## Install Kubebuilder

Kubebuilder is not installed by default. Follow the Kubebuilder quick-start installation instructions:

* Official docs: [https://book.kubebuilder.io/quick-start.html](https://book.kubebuilder.io/quick-start.html)

Example install (fetches the latest binary compatible with your OS):

```bash theme={null}
$ curl -L -o kubebuilder "https://go.kubebuilder.io/dl/latest/$(go env GOOS)"
