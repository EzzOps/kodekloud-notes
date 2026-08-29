# Demo Define The WebApp Go Types

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Demo-Define-The-WebApp-Go-Types/page

Defines Go types for a WebApp Kubernetes custom resource with image and replicas, explains kubebuilder markers and regenerating code and CRD schema generation

The WebApp types file is where your Custom Resource becomes a Go type. Kubebuilder scaffolds this file with placeholder fields; in this lesson we replace the placeholder with a minimal, useful API consisting of `image` and `replicas`.

Open the WebApp types file. It already contains Go structs for `WebApp`, `WebAppSpec`, `WebAppStatus`, and `WebAppList`. In Go, a struct groups named fields together (similar to a small data-holding class in other languages) and each field must have an explicit type.

Replace the placeholder `foo` field with:

* an `Image` field of type `string` (exposed as `spec.image` in YAML/JSON), and
* a `Replicas` field of type `int32` with a default value.

The updated spec and an empty status look like this:

```go theme={null}
// WebAppSpec defines the desired state of WebApp
type WebAppSpec struct {
    // +kubebuilder:validation:Required
    Image    string `json:"image"`
    // +kubebuilder:default=1
    Replicas int32  `json:"replicas,omitempty"`
}

// WebAppStatus defines the observed state of WebApp.
type WebAppStatus struct {
    // INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
    // Important: Run "make" to regenerate code after modifying this file
}
```

Why these fields and tags matter

* `Image string` becomes `spec.image` in the Kubernetes API, and the JSON struct tag controls the YAML/JSON field name.
* Exported Go field names (capitalized) are required so controller tooling and code generation can see and process them.
* Marker comments like `// +kubebuilder:validation:Required` and `// +kubebuilder:default=1` are read by controller-tools to populate the CRD validation schema and defaults.

Summary of markers and JSON tag behavior:

| Marker / Tag                          | Purpose                                               | Example / Effect                                            |
| ------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------- |
| `// +kubebuilder:validation:Required` | Marks the field required in the CRD OpenAPI schema    | Ensures `spec.image` must be provided                       |
| `// +kubebuilder:default=1`           | Sets API-server default when omitted by user          | `spec.replicas` defaults to `1`                             |
| `json:"replicas,omitempty"`           | Controls serialized field name and omitempty behavior | Omitted when zero value unless API server applies a default |
| Capitalized Go field names            | Required to export fields to code generators          | `Image`, `Replicas` (not `image` or `replicas`)             |

> **lightbulb** Run the code generators after changing types so [controller-tools](https://github.com/kubernetes-sigs/controller-tools) can update the generated helpers and the CRD schema.

Regenerate generated code and manifests

After updating your types run the code generators so the deepcopy helpers, CRDs, RBAC, and other artifacts reflect your changes.

1. Generate deepcopy helpers and other generated code:

```bash theme={null}
make generate
```

Typical abbreviated output:

```bash theme={null}
mkdir -p "/home/student/work/Labs/040-002_demo_define_the_webapp_go_types/bin"
Downloading sigs.k8s.io/controller-tools/cmd/controller-gen@v0.20.1
"/home/student/work/Labs/040-002_demo_define_the_webapp_go_types/bin/controller-gen" object:headerFile="hack/boilerplate.go.txt" paths="./..."
```

2. Regenerate manifests (CRDs, roles, webhooks, etc.):

```bash theme={null}
make manifests
```

Typical abbreviated output:

```bash theme={null}
"/home/student/work/Labs/040-002_demo_define_the_webapp_go_types/bin/controller-gen" rbac:roleName=manager-role crd webhooks output:crd:artifacts:config=config/crd/bases
```

What controller-gen produces

`controller-gen` reads your Go structs and Kubebuilder marker comments to generate the CustomResourceDefinition YAML. The CRD's OpenAPIv3 schema will include the new `image` and `replicas` fields and will reflect the `replicas` default. Conceptually, the generated CRD schema for `spec` will look like:

```yaml theme={null}
spec:
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        properties:
          spec:
            properties:
              image:
                type: string
              replicas:
                type: integer
                format: int32
                default: 1
```

This confirms your Go fields are published in the Kubernetes API schema: the WebApp contract now consists of `image` and `replicas`.

Next steps

Now that the types and CRD are in place, the next task is to use `spec.image` and `spec.replicas` inside your controller's reconcile loop so your controller can create and manage underlying resources (Deployments, Services, etc.) to match the desired WebApp state.

Links and references

* [Kubebuilder Book](https://book.kubebuilder.io/)
* [controller-tools (controller-gen)](https://github.com/kubernetes-sigs/controller-tools)
* [Kubernetes CustomResourceDefinition docs](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* [OpenAPI v3 validation for CRDs](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/693d583d-ea0d-4691-ad56-bb7fa814a106)
