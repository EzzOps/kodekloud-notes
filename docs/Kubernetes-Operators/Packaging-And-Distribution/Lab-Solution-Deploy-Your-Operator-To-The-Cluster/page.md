# example snippet
containers:
  - name: manager
    image: 127.0.0.1:5000/course/webapp-operator@sha256:[SECRET_REDACTED]
```

Using the digest above ensures the cluster pulls the exact content you pushed.

## Links and references

* [Docker Buildx imagetools](https://docs.docker.com/buildx/working-with-buildx/#imagetools)
* [Kubernetes Documentation — Images](https://kubernetes.io/docs/concepts/containers/images/)
* [Docker Registry (distribution) GitHub](https://github.com/distribution/distribution)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/fa37ed3b-f8dd-4a7b-8859-c344c18d5ed1" />
</CardGroup>


# Lab Solution Deploy Your Operator To The Cluster

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Packaging-And-Distribution/Lab-Solution-Deploy-Your-Operator-To-The-Cluster/page

Guide to build, push, and deploy a Kubernetes operator image, install operator manifests, and verify in-cluster reconciliation of a WebApp custom resource.

A "local" operator is a workshop build of your controller. A "deployed" operator is a shipped artifact: a container image in a registry plus manifests installed into the cluster. This lesson walks the full packaging and deployment path and verifies that the in-cluster controller can still reconcile a WebApp custom resource.

## Overview

High-level steps:

1. Choose an image registry and tag that the cluster nodes can pull.
2. Build the controller image and tag it with that value.
3. Push the image to the registry so cluster nodes can fetch it.
4. Deploy the operator manifests (CRDs, RBAC, ServiceAccount, Deployment) with the image patched to the pushed tag.
5. Verify the operator's Deployment becomes available.
6. Create a demo WebApp custom resource and confirm the in-cluster controller reconciles it.

Important: use a single `IMG` value for build, push, and deploy. A common packaging mistake is using different tags at each step: you might push one image but deploy another.

## Set the registry and image tag

Choose a registry reachable from your cluster nodes and export the environment values used by the Makefile:

```bash theme={null}
export IMG_REGISTRY="127.0.0.1:5000/course"
export IMG="${IMG_REGISTRY}/webapp-operator:lab"
```

This `IMG` value will be used for building, pushing, and deploying the controller image.

## Build the controller image

Run the Makefile target that builds and tags the manager image:

```bash theme={null}
make docker-build IMG="$IMG"
```

Notes:

* The Kubebuilder-generated Makefile passes the tag into Docker.
* Docker builds the manager image from the project Dockerfile. The resulting image contains the compiled manager binary (not your live source directory).

## Push the image to the registry

Push the image so cluster nodes can pull it by name:

```bash theme={null}
make docker-push IMG="$IMG"
```

Pushing makes the image available outside the local Docker cache. Example push output:

```text theme={null}
bdfd7f7e5bf6: Layer already exists
99515e7b4345: Layer already exists
d6b1b89eccac: Layer already exists
52630fc75a18: Layer already exists
47de5dd0b812: Layer already exists
b73845f3dba: Layer already exists
7c12895b777b: Layer already exists
99ba982a9142: Layer already exists
b839dfa016: Layer already exists
936c2190efa: Pushed
c172f21411df: Layer already exists
3214c2f345c0: Layer already exists
2780902e5dbf: Layer already exists
d6dbfd62d1f4: Layer already exists
ebdcc565facc: Layer already exists
lab: digest: sha256:[SECRET_REDACTED] size: 856
```

## Deploy the operator manifests

Apply the CRDs, RBAC, ServiceAccount, and the Deployment for the controller manager, and patch the manager image to the `IMG` value:

```bash theme={null}
make deploy IMG="$IMG"
```

You may see the Makefile invoke kustomize to set the image reference, for example:

```bash theme={null}
cd config/manager && "/home/student/work/Labs/090-004_lab_deploy_your_operator_to_the_cluster/webapp-operator/bin/kustomize" edit set image controller=127.0.0.1:5000/course/webapp-operator:lab
```

## Wait for the operator Deployment to become available

This is an important runtime check: if the image tag is wrong, the registry is unreachable, or the image cannot start, the rollout will fail and surface the error here.

```bash theme={null}
kubectl -n webapp-operator-system wait --for=condition=Available deploy/webapp-operator-controller-manager --timeout=180s
```

If the wait completes, validate:

* The Deployment and pods indicate the controller is running as a cluster workload.
* The CRD is installed so the API server recognizes the `WebApp` (or `webapp`) resource.

## Smoke test: create a WebApp CR and verify reconciliation

Create a demo namespace and apply a sample WebApp custom resource to confirm the installed operator responds to cluster objects (a successful `make deploy` is not sufficient proof on its own):

```bash theme={null}
kubectl create namespace webapp-demo
kubectl apply -f ../webapp-site.yaml -n webapp-demo
```

You should see the CR creation:

```text theme={null}
webapp.webapp.kodekloud.com/site created
```

Wait for the child Deployment (the site deployment created by the operator) to become available. This Deployment is created by the in-cluster operator controller and proves it is watching and reconciling the WebApp resource:

```bash theme={null}
kubectl -n webapp-demo wait --for=condition=Available deploy/site --timeout=180s
```

Finally, check the WebApp `Ready` condition from the resource status to confirm the operator reported success:

```bash theme={null}
kubectl -n webapp-demo get webapp site -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
```

Expected output: `True`

When that condition is `True`, the packaging loop is closed: the operator image was built, pushed, installed, and the in-cluster controller reconciled the custom resource and its child resources.

<Callout icon="lightbulb">
  Ensure the registry referenced by `IMG_REGISTRY` is reachable from your cluster nodes (for example, a local registry may require special configuration or a registry running inside the cluster). If the cluster cannot pull the image, the controller deployment will remain unavailable.
</Callout>

## Quick reference: common commands

| Purpose                                        | Command / Example                                                                                                           |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Set registry and image tag                     | `export IMG_REGISTRY="127.0.0.1:5000/course"`<br />`export IMG="${IMG_REGISTRY}/webapp-operator:lab"`                       |
| Build image                                    | `make docker-build IMG="$IMG"`                                                                                              |
| Push image                                     | `make docker-push IMG="$IMG"`                                                                                               |
| Deploy manifests (and patch image)             | `make deploy IMG="$IMG"`                                                                                                    |
| Wait for controller Deployment to be available | `kubectl -n webapp-operator-system wait --for=condition=Available deploy/webapp-operator-controller-manager --timeout=180s` |
| Create demo namespace                          | `kubectl create namespace webapp-demo`                                                                                      |
| Apply sample WebApp CR                         | `kubectl apply -f ../webapp-site.yaml -n webapp-demo`                                                                       |
| Wait for child Deployment to be available      | `kubectl -n webapp-demo wait --for=condition=Available deploy/site --timeout=180s`                                          |
| Check WebApp Ready condition                   | `kubectl -n webapp-demo get webapp site -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'`                      |

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker](https://www.docker.com/)
* [Kustomize](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Kubebuilder Book](https://book.kubebuilder.io/)
* [Operator SDK](https://sdk.operatorframework.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/fbae7306-4a7e-4f95-8f4f-00dc16f24103" />
</CardGroup>
