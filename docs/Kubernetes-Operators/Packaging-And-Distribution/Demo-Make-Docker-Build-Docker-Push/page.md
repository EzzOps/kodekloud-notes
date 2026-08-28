# Image URL to use for all build/push image targets
IMG ?= controller:latest

# Get the currently used golang install path (in GOPATH/bin, unless GOBIN is set)
ifeq (, $(shell go env GOBIN))
GOBIN := $(shell go env GOPATH)/bin
else
GOBIN := $(shell go env GOBIN)
endif

# CONTAINER_TOOL defines the container tool to be used for building images (e.g. docker, podman)
CONTAINER_TOOL ?= docker
```

Inspect the `deploy` target — the important step is `kustomize edit set image`, which updates the manager image in `config/manager` before building and applying the customized manifests:

```makefile theme={null}
.PHONY: deploy
deploy: manifests kustomize ## Deploy controller to the K8s cluster specified in ~/.kube/config.
	cd config/manager && "$(KUSTOMIZE)" edit set image controller=${IMG}
	"$(KUSTOMIZE)" build config/default | "$(KUBECTL)" apply -f -
```

<Callout icon="lightbulb">
  Always pass the exact `IMG` value to `make deploy` that you used when building and pushing the image. If `IMG` is omitted or incorrect, the generated Deployment can reference a placeholder image and your pods may fail to pull.
</Callout>

## Run make deploy

Set `IMG` to the registry image you pushed and run `make deploy`. The Make target generates CRDs and RBAC, updates the manager image in Kustomize, builds the final manifests, and applies them to the cluster.

```bash theme={null}
export IMG="127.0.0.1:5000/course/webapp-operator:v0.1.0"
printenv IMG
make deploy IMG="$IMG"
```

Example trimmed output showing resources being created:

```bash theme={null}
clusterrole.rbac.authorization.k8s.io/webapp-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/webapp-operator-webapp-admin-role created
rolebinding.rbac.authorization.k8s.io/webapp-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/webapp-operator-manager-rolebinding created
service/webapp-operator-controller-manager-metrics-service created
deployment.apps/webapp-operator-controller-manager created
```

If the image reference is wrong or your cluster cannot pull from the registry, pod events will typically show `ImagePullBackOff` or similar error messages.

<Callout icon="warning">
  Ensure the registry referenced by `IMG` is accessible from the cluster nodes (network and authentication). Private registries often require imagePullSecrets or registry credentials configured on the nodes.
</Callout>

## Verify rollout and controller readiness

Wait for the controller manager Deployment to roll out. A successful rollout means the controller pod was created and its manager container became ready.

```bash theme={null}
kubectl -n webapp-operator-system rollout status deploy/webapp-operator-controller-manager --timeout=180s
kubectl get pods -n webapp-operator-system
# NAME                                                   READY   STATUS    RESTARTS   AGE
# webapp-operator-controller-manager-566cd8df5c-tsb9x    1/1     Running   0          38s
```

The controller is now running in-cluster as a Pod (not via `make run`). Inspect its logs to confirm it became leader and started workers:

```bash theme={null}
kubectl -n webapp-operator-system logs deploy/webapp-operator-controller-manager
```

Typical startup log lines include leader election, metrics server binding, and controller startup, for example:

```bash theme={null}
2026-06-15T19:45:41Z DEBUG events ... became leader  {"type":"Normal", ... "reason":"LeaderElection"}
2026-06-15T19:45:42Z INFO  controller-runtime.metrics Serving metrics server {"bindAddress":":8443","secure":true}
2026-06-15T19:45:41Z INFO  Starting Controller {"controller":"webapp","controllerGroup":"webapp.kodekloud.com"}
```

Worker startup indicates the controller runtime is ready to reconcile WebApp resources.

## Confirm the CRD is registered

Verify the API server now understands the `webapp` custom resource:

```bash theme={null}
kubectl get crd webapps.webapp.kodekloud.com

# NAME                            CREATED AT
# webapps.webapp.kodekloud.com    2026-06-15T19:45:40Z
```

A present CRD proves the cluster can accept WebApp objects and the in-cluster controller can reconcile them.

## Quick reference: what `make deploy` creates

| Resource type                                           | Purpose                                                    | Example / note                                       |
| ------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| CRD                                                     | Adds the `WebApp` API to the cluster                       | `webapps.webapp.kodekloud.com`                       |
| RBAC (Role/ClusterRole, RoleBinding/ClusterRoleBinding) | Grants permissions to the controller                       | Roles like `webapp-operator-webapp-admin-role`       |
| Service                                                 | Exposes metrics for scraping                               | `webapp-operator-controller-manager-metrics-service` |
| Deployment                                              | Runs the controller manager Pod using the image from `IMG` | `webapp-operator-controller-manager`                 |

## Summary / Checklist

* Build and push your operator image to a registry reachable by the cluster.
* Use the same image reference when running `make deploy` via `IMG`.
* `make deploy` updates the Kustomize manager image, builds manifests, and applies them.
* Wait for the Deployment rollout and confirm the controller Pod is Running.
* Check controller logs for leader election and worker startup messages.
* Verify the CRD exists so custom resources can be created and reconciled.

## Links and references

* [Kustomize documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
* [Kubernetes CRD concepts](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/c25b009f-0952-4fdb-8dbc-e57ade3dfc37" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/9b287938-25fd-40eb-990d-13e36b711ef2" />
</CardGroup>


# Demo Make Docker Build Docker Push

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Packaging-And-Distribution/Demo-Make-Docker-Build-Docker-Push/page

Building, tagging, pushing a Docker image to a registry and verifying its manifest for Kubernetes deployments.

A Kubernetes cluster cannot run a locally-built binary — it needs an image reference that the cluster can pull from a registry. In this lesson you'll:

* set a concrete image tag that points to a registry,
* build a controller image via the project's Makefile,
* push that image to a registry, and
* confirm the registry contains a manifest for the tag.

## 1) Set the image reference

Set the `IMG` environment variable to a registry path and a version tag. In this recording we use a local registry at `127.0.0.1:5000` and tag `v0.1.0`:

```bash theme={null}
export IMG=127.0.0.1:5000/course/webapp-operator:v0.1.0
```

## 2) Build the image

Use the Makefile target that forwards `IMG` into Docker. The Makefile injects the tag into the Docker build so the resulting image is named as above.

```bash theme={null}
make docker-build IMG=$IMG
```

The project uses a multi-stage Dockerfile. The build usually compiles a `manager` binary in the builder stage, then copies that into a minimal runtime image in a later stage. Example (truncated) build output:

```console theme={null}
=> CACHED [builder 6/7] COPY . .
=> CACHED [builder 7/7] RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -o manager cmd/main.go
=> CACHED [stage-1 2/3] COPY --from=builder /workspace/manager .
exporting to image
=> exporting layers
=> exporting manifest sha256:8a81b15d6d50b0094af375f659be04fdcb422a84ccd50d7e5b5968dcf220ab6a
=> exporting config sha256:31b190ab9c56c6b65483f180bbce9c28a5f51b8eafc8ee78608f35f47675f90e
=> exporting attestation manifest sha256:5adf21588e94c411886136fcad009a7cfa809ab043dd059a09e22b
=> naming to 127.0.0.1:5000/course/webapp-operator:v0.1.0
=> unpacking to 127.0.0.1:5000/course/webapp-operator:v0.1.0
```

Summary:

* Builder stage compiles the `manager` binary.
* Runtime stage packages that binary into the final controller image.

## 3) Push the image to the registry

Push the tag you just built so the registry stores the layers and writes an image manifest:

```bash theme={null}
make docker-push IMG=$IMG
```

Push output will show each layer uploaded and a final digest for the pushed tag. Example:

```console theme={null}
2780920e5dbf: Pushed
9b2e9c4f5243: Pushed
c172f21814df: Pushed
47de5dd0b812: Pushed
d6b1b89eccac: Pushed
52630fc75a18: Pushed
3214c34f5c0c: Pushed
b839dfae016f: Pushed
99ba982a9142: Pushed
ebdc5f54cdc: Pushed
v0.1.0: digest: sha256:db81233d7799521a10305a9e722847a1920e2ceec4f67fdd43bae2c23ba50086 size: 856
```

The registry manifest written for `v0.1.0` is what Kubernetes later uses when resolving the image reference during deployment.

## 4) Verify the registry tag and manifest

To confirm the tag and its digest are visible in the registry (i.e., not just in your local Docker cache), inspect the image with Docker Buildx imagetools:

```bash theme={null}
docker buildx imagetools inspect $IMG
```

Example output shows the tag's digest and the platform manifests it references:

```console theme={null}
Digest: sha256:db81233d7799521a10305a9e722847a1920e2ceec4f67fdd43bae2c23ba50086

Manifests:
  Name: 127.0.0.1:5000/course/webapp-operator:v0.1.0@sha256:8a81b15d6d50b0094af375f659be04fdcb422a84ccd50d7e5b5968dcf220ab6a
  MediaType: application/vnd.oci.image.manifest.v1+json
  Platform:
    linux/amd64

  Name: 127.0.0.1:5000/course/webapp-operator:v0.1.0@sha256:5adf21588e94c411886136fcad009a7cfa809ab043dd059a09e22b
  MediaType: application/vnd.oci.image.manifest.v1+json
  Platform: unknown/unknown
```

<Callout icon="lightbulb">
  Tags (like `v0.1.0`) are mutable references, while the digest (`sha256:...`) is the immutable content identifier. Using the digest (for example `image: 127.0.0.1:5000/course/webapp-operator@sha256:<digest>`) in manifests or deployment specs guarantees the exact image bytes that will be pulled.
</Callout>

<Callout icon="warning">
  If you're using a local registry (e.g., `127.0.0.1:5000`) make sure the registry service is running and your Docker daemon is configured to allow pushing to that host (insecure registry settings may be required). Pushing to remote registries may also require authentication.
</Callout>

## Quick reference — common commands

| Step          | Command                                                   | Purpose                                                    |
| ------------- | --------------------------------------------------------- | ---------------------------------------------------------- |
| Set image tag | `export IMG=127.0.0.1:5000/course/webapp-operator:v0.1.0` | Point `IMG` at the registry and tag to use                 |
| Build         | `make docker-build IMG=$IMG`                              | Build the multi-stage Docker image with the provided tag   |
| Push          | `make docker-push IMG=$IMG`                               | Upload layers and create a registry manifest for the tag   |
| Inspect       | `docker buildx imagetools inspect $IMG`                   | Verify tag, digest, and platform manifests in the registry |

## Deploying with the pushed image

Now that the controller image is available from the registry, pass the same `IMG` value into your deployment step (for example):

```bash theme={null}
make deploy IMG=$IMG
```

Or pin by digest in Kubernetes manifests:

```yaml theme={null}
