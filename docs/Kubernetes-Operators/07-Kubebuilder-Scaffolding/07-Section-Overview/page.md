# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Kubebuilder-Scaffolding/Section-Overview/page

Guide to using Kubebuilder to scaffold, generate, and manage a Go-based Kubernetes operator project including APIs, controllers, CRD and RBAC generation, and CLI commands.

By the end of this section you will have a working operator project on disk: scaffolded, compiled, and ready to grow into the WebApp operator we build throughout this course. The scaffold provides a clear layout for your Go module, CRD types, controller logic, manifests, and packaging.

```text theme={null}
text
operator-project/
├── Makefile
├── PROJECT
├── go.mod
├── api/v1/
│   └── webapp_types.go
├── controllers/
│   └── webapp_controller.go
└── config/
    ├── crd/
    └── manager/
```

Kubebuilder provides a repeatable scaffolding workflow that organizes every artifact in a predictable place: project metadata, API types, controller code, generated manifests, a Dockerfile for packaging, and Makefile targets for common tasks. This section shows how to use Kubebuilder to create that scaffold so subsequent lessons can focus on operator logic instead of project plumbing.

<Frame>
  <img alt="The image illustrates Kubebuilder, highlighting its function as a code generator and thin runtime layer, built on top of the controller-runtime which handles resource watching." />
</Frame>

Why use Kubebuilder? If you want to build a Kubernetes operator—software that watches custom resources and reconciles cluster state—you usually start with an empty directory and many structural decisions. Kubebuilder automates that: it bootstraps the manager, wires the controller to the manager, generates CRD manifests from Go types, and emits RBAC rules from annotations.

Kubebuilder is a generator and thin runtime layer built on top of controller-runtime, which is the library that actually watches resources, keeps caches, and runs reconciliation loops.

<Frame>
  <img alt="The image is a graphic explaining how Kubebuilder organizes project components, listing files like go.mod, Makefile, and Dockerfile, and explaining their purposes such as project identity and packaging." />
</Frame>

Quick reference — common scaffold files and their purpose:

| File / Directory | Purpose                                                             |
| ---------------- | ------------------------------------------------------------------- |
| `go.mod`         | Go module identity for the operator project                         |
| `Makefile`       | Repeatable build/test/manifest targets                              |
| `PROJECT`        | Kubebuilder project metadata (scaffold history)                     |
| `api/<version>/` | Go structs (CRD types) live here, e.g. `api/v1/webapp_types.go`     |
| `controllers/`   | Reconciler implementations, e.g. `controllers/webapp_controller.go` |
| `config/`        | Generated manifests (CRD, RBAC, manager, samples)                   |
| `Dockerfile`     | Image build instructions for the operator container                 |

Starter controller code is already wired to the manager. Before adding your custom APIs and reconcile logic, it helps to compare Kubebuilder with the Operator SDK: both leverage controller-runtime but provide different developer experiences and tooling. For this course, Kubebuilder is the primary scaffold tool.

<Frame>
  <img alt="The image compares Kubebuilder and Operator SDK, indicating that both operate on the controller-runtime but have different feels." />
</Frame>

Getting started — CLI commands

1. Verify your toolchain and install Kubebuilder.
2. Initialize a new project and create an API for the WebApp kind.

Example shell session:

```bash theme={null}
$ mkdir webapp-operator && cd webapp-operator
$ ls
