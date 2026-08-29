# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Packaging-And-Distribution/Section-Overview/page

Guide to packaging and distributing a Kubernetes operator by building and pushing the controller image, deploying install manifests, verifying the in-cluster manager, and introducing Operator Lifecycle Manager

Up to this point you've been developing and testing the web app Operator primarily from a developer workflow: running the manager locally, watching reconciliation logs, adding status and finalizers, implementing CEL validation, and validating behavior inside a Kubernetes cluster.

This lesson shifts the focus from "does the operator work?" to "how do other people install and run it?" In other words: how do you package the controller into a container image, publish it, and deliver repeatable install manifests so others (and CI/CD systems) can deploy and run the operator in their clusters?

Packaging begins with the controller image. The operator manager is a Go binary, but Kubernetes runs containers. Kubebuilder scaffolds a Dockerfile that builds the manager and copies the compiled binary into a lightweight runtime image. Your tasks in this section are:

* Inspect the Dockerfile build path and verify the binary ends up in the runtime image.
* Connect the image tag you produce to the Deployment used by the operator manager.
* Use the provided Makefile targets (scaffolded by Kubebuilder) to build, push, and deploy the operator.

Key Makefile targets you will use:

| Target              | Purpose                                                                                                                | Example                                                           |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `make docker-build` | Build the OCI image using the `IMG` value you provide.                                                                 | `make docker-build IMG=myregistry.example.com/webapp-operator:v1` |
| `make docker-push`  | Push the tagged image to the configured registry so clusters can pull it.                                              | `make docker-push IMG=myregistry.example.com/webapp-operator:v1`  |
| `make deploy`       | Run the configured Kustomize build and apply CRDs, RBAC, the manager Deployment, Service, and other install resources. | `make deploy IMG=myregistry.example.com/webapp-operator:v1`       |

Example workflow (end-to-end):

```bash theme={null}
