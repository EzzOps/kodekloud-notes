# Demo Building The Operator Container Image

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Packaging-And-Distribution/Demo-Building-The-Operator-Container-Image/page

Explains building and publishing a minimal multi-architecture Kubernetes operator container image using Dockerfile, distroless runtime, and Makefile buildx workflows.

The `make run` command is convenient for local development, but to deploy the operator to another Kubernetes cluster you must publish a container image that cluster nodes can pull and run.

Kubebuilder has already scaffolded the important pieces for building that image: a Dockerfile, Makefile targets, and Kubernetes manifests under `config/`. This document inspects the Dockerfile and Makefile pieces that go into the operator image. Building and pushing the image will be covered later in an end-to-end flow.

References

* [Kubebuilder](https://kubebuilder.io)
* [Distroless images (GoogleContainerTools)](https://github.com/GoogleContainerTools/distroless)

## Dockerfile overview

The repository Dockerfile uses a multi-stage build pattern:

* Stage 1 (builder): compiles the Go-based operator manager binary using an official Go image.
* Stage 2 (runtime): packages only the compiled binary into a minimal runtime image (distroless).

This produces a small, secure runtime image suitable for production clusters.

### First stage — builder (compiles the manager binary)

```dockerfile theme={null}
