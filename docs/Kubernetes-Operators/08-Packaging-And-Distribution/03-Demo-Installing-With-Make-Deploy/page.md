# Build the manager binary
FROM golang:1.25 AS builder
ARG TARGETOS
ARG TARGETARCH

WORKDIR /workspace

# Copy Go module manifests first so dependencies can be cached
COPY go.mod go.sum ./
RUN go mod download

# Copy the Go source (relies on .dockerignore to filter)
COPY . .

# Build a static binary suitable for a distroless image
RUN CGO_ENABLED=0 GOOS=${TARGETOS:-linux} GOARCH=${TARGETARCH} go build -a -o manager cmd/main.go
```

Key notes about this stage:

* Copying `go.mod` and `go.sum` before the rest of the source enables Docker to cache dependencies. Changing application source code afterwards won’t force a re-download of modules.
* `CGO_ENABLED=0` produces a statically-linked binary, required when using distroless base images that lack C libraries.
* `TARGETOS` and `TARGETARCH` are build arguments that let Buildx inject platform values for multi-architecture images.

### Second stage — runtime (minimal image containing only the binary)

```dockerfile theme={null}
# Use distroless as minimal base image to package the manager binary
# See https://github.com/GoogleContainerTools/distroless for details
FROM gcr.io/distroless/static:nonroot
WORKDIR /

# Copy the compiled manager from the builder stage
COPY --from=builder /workspace/manager .

# Run as non-root user (keeps the container more secure)
USER 65532:65532

ENTRYPOINT ["/manager"]
```

Why this works well for operators:

* The final image contains only the compiled `manager` binary — no package managers, shells, or interpreters — reducing image size and attack surface.
* Running as a non-root user increases runtime security.
* Distroless images are ideal for production but limit in-container debugging because typical tooling is absent.

> **lightbulb** Using a distroless image with a static binary improves security and minimizes image size, but it also means debugging inside the container is limited since shells and typical tooling are absent.

## Makefile targets for building and publishing

The Makefile in the project exposes basic single-architecture build/push targets and a Buildx-based cross-platform workflow for producing multi-architecture images.

### Simple single-architecture build and push

```makefile theme={null}
.PHONY: docker-build
docker-build: ## Build docker image with the manager.
	$(CONTAINER_TOOL) build -t ${IMG} .

.PHONY: docker-push
docker-push: ## Push docker image with the manager.
	$(CONTAINER_TOOL) push ${IMG}
```

Use these targets when you only need a single-architecture image (for example, `linux/amd64`). Do not run these if you intend to publish multi-architecture images — use the Buildx workflow instead.

### Cross-platform build and push (buildx)

```makefile theme={null}
PLATFORMS ?= linux/arm64,linux/amd64,linux/s390x,linux/ppc64le

.PHONY: docker-buildx
docker-buildx: ## Build and push docker image for the manager for cross-platform support
	# Create a temporary Dockerfile that ensures buildkit uses the build platform for the FROM line
	sed -e '1 s|^FROM|FROM --platform=$${BUILDPLATFORM}|' Dockerfile > Dockerfile.cross
	- $$(CONTAINER_TOOL) buildx create --name webapp-operator-builder
	- $$(CONTAINER_TOOL) buildx use webapp-operator-builder
	- $$(CONTAINER_TOOL) buildx build --push --platform=$${PLATFORMS} --tag $${IMG} -f Dockerfile.cross
	- $$(CONTAINER_TOOL) buildx rm webapp-operator-builder
	- rm Dockerfile.cross
```

Why this Buildx workflow matters:

* `PLATFORMS` enumerates the CPU architectures to include in the image manifest list served by the registry.
* The `sed` command writes a temporary `Dockerfile.cross` that forces BuildKit to respect the `BUILDPLATFORM` on each `FROM` instruction. This is critical so that the correct base image for each target architecture is used during the multi-arch build.
* `buildx build --push --platform=...` builds images for multiple architectures and pushes a single tag that points to a manifest list (multi-arch image). The registry then serves the appropriate architecture image for each node automatically.

Table: Makefile targets summary

| Target          | Purpose                                         | Example                                          |
| --------------- | ----------------------------------------------- | ------------------------------------------------ |
| `docker-build`  | Build a single-arch image locally               | `make docker-build IMG=example/operator:dev`     |
| `docker-push`   | Push a single-arch image to registry            | `make docker-push IMG=example/operator:dev`      |
| `docker-buildx` | Build & push a multi-arch image (manifest list) | `make docker-buildx IMG=example/operator:latest` |

> **warning** If a tag only points to an `amd64` image, an `arm64` node cannot run that image. Use a multi-arch manifest list (via Buildx) to support heterogeneous clusters.

## Separating image and install manifests

It’s important to keep the container image build pipeline distinct from Kubernetes installation manifests:

* Image: contains only the controller binary and runtime configuration (Dockerfile, build process).
* Install manifests: CRDs, RBAC, Deployment, Service, and sample manifests are under `config/` and are generated or applied by other Make targets.

This separation simplifies CI/CD: image builds and registry publishing are one concern; packaging and installing the operator into a cluster are another.

## What’s next

This article toured the Dockerfile and Makefile pieces used to produce a minimal, secure operator image and explained how to produce a multi-architecture manifest list using Buildx. Later you can perform the end-to-end build and push flow:

* Choose an image tag and registry (for example, `docker.io/<your-org>/webapp-operator:v0.1.0`).
* Run the `docker-buildx` target to publish a multi-arch image.
* Update your operator Deployment manifests under `config/` to reference the published image tag.

Further reading and references

* [Kubebuilder documentation](https://kubebuilder.io)
* [Distroless images (GitHub)](https://github.com/GoogleContainerTools/distroless)
* [Docker Buildx documentation](https://docs.docker.com/buildx/working-with-buildx/)
* [Container image best practices (Google)](https://cloud.google.com/container-registry/docs/best-practices)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/e84aeab2-57ea-4683-8b73-2dd39c38cf57)


# Demo Installing With Make Deploy

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Packaging-And-Distribution/Demo-Installing-With-Make-Deploy/page

Deploying a Kubernetes operator using make deploy to set the image via Kustomize, apply CRDs, RBAC, Service and Deployment, then verify rollout and CRD registration

The operator image has been pushed. The next step is to install the in-cluster manifests that reference that image: a CustomResourceDefinition (CRD), RBAC roles/bindings, a Service for metrics, and the controller Deployment. The operator scaffold's Makefile provides a `deploy` target that generates and applies these manifests, using the `IMG` variable to set the controller image used by Kustomize.

<Frame>
  <img alt="The image is a slide titled &#x22;Installing With Make Deploy,&#x22; featuring a large dark blue shape on the right with the word &#x22;Demo.&#x22; It includes a copyright notice for KodeKloud." />
</Frame>

## Key Makefile fragments

Top of the Makefile (trimmed) defines the default image and the container tooling:

```makefile theme={null}
