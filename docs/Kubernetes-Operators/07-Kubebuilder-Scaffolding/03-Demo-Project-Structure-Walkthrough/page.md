# make it executable and move into a directory on PATH, for example:
$ chmod +x kubebuilder
$ sudo mv kubebuilder /usr/local/bin/
$ kubebuilder version
```

> **lightbulb** Make sure `kubebuilder` is executable and located in a directory that is on your `PATH` (for example `/usr/local/bin`).

> **warning** Kubebuilder will not scaffold into a directory that already contains files. Always run `kubebuilder init` from an empty project folder (check your editor or run `ls -la` first). If the folder contains files, create a clean directory before continuing.

## Verify toolchain

Confirm both Kubebuilder and Go are installed and reporting compatible versions. If versions differ significantly, the project layout and generated imports may vary.

```bash theme={null}
$ kubebuilder version && go version
KubeBuilder:        v4.14.0
Kubernetes:         1.35.0
Git Commit:         505d63f3b272472b5556ff650f03ba64d885cf3a
Build Date:         2026-04-29T07:19:23Z
Go OS/Arch:         linux/amd64
go version go1.26.3 linux/amd64
```

## Initialize the project

`kubebuilder init` scaffolds a new operator project. The most important flags:

| Flag             | Purpose                                          | Example                                       |
| ---------------- | ------------------------------------------------ | --------------------------------------------- |
| `--domain`       | API group suffix (used in CRD API groups)        | `--domain kodekloud.com`                      |
| `--repo`         | Go module path (becomes `module` in `go.mod`)    | `--repo github.com/kodekloud/webapp-operator` |
| `--project-name` | Project name saved in Kubebuilder `PROJECT` file | `--project-name webapp-operator`              |

Pick these values carefully: `domain` and `repo` are embedded into package import paths and generated manifests.

Example init command:

```bash theme={null}
$ kubebuilder init --domain kodekloud.com --repo github.com/kodekloud/webapp-operator --project-name webapp-operator
```

Typical scaffold output:

```text theme={null}
INFO    Writing kustomize manifests
INFO    Writing scaffold for you to follow
INFO    Get controller runtime
INFO    Update dependencies
Next:  define a resource with:
$ kubebuilder create api
```

## What Kubebuilder creates

After `kubebuilder init` completes, you'll see a small project layout with source, build, and configuration files. Key files and directories:

| Path                        | Purpose                                                                       |
| --------------------------- | ----------------------------------------------------------------------------- |
| `cmd/main.go`               | Manager entry point — starts the controller-runtime manager.                  |
| `config/`                   | Kustomize manifests for deploying the manager, CRDs, RBAC, and webhooks.      |
| `Dockerfile` and `Makefile` | Build, test, and packaging targets (e.g., `make build`, `make docker-build`). |
| `PROJECT`                   | Kubebuilder metadata that tracks CLI options and layout choices.              |

A sample `PROJECT` file:

```yaml theme={null}
cliVersion: 4.14.0
domain: kodekloud.com
layout:
  - go.kubebuilder.io/v4
projectName: webapp-operator
repo: github.com/kodekloud/webapp-operator
version: "3"
```

## Build the scaffold

The scaffold is intended to compile immediately. If `make build` succeeds, your Go toolchain and module path are configured correctly.

Scaffold and build:

```bash theme={null}
$ kubebuilder create api
$ make build
mkdir -p "/home/student/work/labs/bin"
Downloading sigs.k8s.io/controller-tools/cmd/controller-gen@v0.20.1
"/home/student/work/labs/bin/controller-gen"
rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
"/home/student/work/labs/bin/controller-gen" object:headerFile="hack/boilerplate.go.txt",year=2026 paths="./..."
```

If the build completes successfully, the manager binary compiles and you’re ready to scaffold APIs, controllers, and webhooks.

## Next steps

Now that the skeleton is in place and the manager compiles, continue with:

* A tour of the directories and files Kubebuilder `init` created (`cmd/`, `config/`, `api/`, `controllers/`)
* Using `kubebuilder create api` to define your first CustomResource and controller
* Implementing reconcile logic in the generated controller

References and further reading:

* Kubebuilder Quick Start: [https://book.kubebuilder.io/quick-start.html](https://book.kubebuilder.io/quick-start.html)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Go installation: [https://go.dev/doc/install](https://go.dev/doc/install)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/20a4ec01-fde8-466d-83c7-2f74f6def1f0/lesson/890865bb-b83d-494c-a64b-b96ca96194fb)


# Demo Project Structure Walkthrough

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Kubebuilder-Scaffolding/Demo-Project-Structure-Walkthrough/page

A walkthrough of a Kubebuilder scaffolded operator project explaining files, directories, and where to add APIs, controllers, and deployment manifests

You just ran `kubebuilder init`. When you open the generated folder it can feel like Kubebuilder dumped a lot of files at once.

Think of this project as a labeled workbench: Kubebuilder has already placed the tools and drawers before you build the operator. You don't need to memorize every file — just know which drawer to open for each job.

> **lightbulb** Treat this layout as a simple map: knowing where startup code, API types, reconcile logic, deployment manifests, and helper targets live is enough to get productive.

Start at the root.

PROJECT is the label on this workbench. It records the domain, repo path, project name, and every API you add later. Kubebuilder regenerates it as needed, so you generally should not hand-edit it.

> **warning** The `PROJECT` file is code-generated. Avoid manual edits unless you fully understand the implications—let Kubebuilder and plugins manage this file.

A typical generated `PROJECT` file looks like:

```yaml theme={null}
