# Demo Kubebuilder Create API For WebApp

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Kubebuilder-Scaffolding/Demo-Kubebuilder-Create-API-For-WebApp/page

Guide to scaffolding a WebApp custom resource, controller, and CRD manifests with Kubebuilder in a Go operator project.

You need a WebApp custom resource type in your operator. Starting from an empty Go project, Kubebuilder scaffolds the Go types, controller, and CRD manifest for you in the expected project layout so you can quickly run `kubectl apply`.

<Frame>
  <img alt="The image shows the Visual Studio Code interface with a file explorer on the left displaying project files, and an open terminal on the right." />
</Frame>

This lesson walks through scaffolding a WebApp API (group `webapp`, version `v1`, kind `WebApp`) and shows how Kubebuilder wires everything together.

## Project overview before scaffolding

When you open the project you should already see:

* `PROJECT` file describing the repository and domain.
* `cmd` directory (entry point).
* `config` tree for manifests and kustomize overlays.

Run the Kubebuilder command to scaffold the API (this also creates a controller and resource):

```bash theme={null}
kubebuilder create api --group webapp --version v1 --kind WebApp --resource --controller
```

With the project domain set to `kodekloud.com` in `PROJECT`, the full API group becomes:
`webapp.kodekloud.com/v1`.

## What Kubebuilder generates

After running the scaffold command, Kubebuilder creates the new API types and controller skeleton. The two primary locations are:

| Path                  | Purpose                                     |
| --------------------- | ------------------------------------------- |
| `api/v1`              | Go types for the CRD schema (Spec & Status) |
| `internal/controller` | Reconciler implementation (controller code) |

Kubebuilder also updates the `PROJECT` metadata used for future scaffolding. Example `PROJECT`-style metadata:

```yaml theme={null}
