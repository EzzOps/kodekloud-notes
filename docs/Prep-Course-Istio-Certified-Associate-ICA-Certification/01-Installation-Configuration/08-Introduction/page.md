# download Istio release into a new directory (example: 1.26.3)
$ curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.26.3 sh -
```

Change into the newly created directory and add `istioctl` to your PATH:

```bash theme={null}
$ cd istio-1.26.3
$ export PATH=$PWD/bin:$PATH
$ istioctl version
1.26.3
# If Istio control plane is not installed, you may also see:
# no running Istio pods in "istio-system"
```

Note: `istioctl` is the client binary. The control plane components are installed into the cluster separately (via `istioctl install` or Helm).

Install `kubectl` (if needed)
Examples for Linux downloads (adjust release and arch as required):

```bash theme={null}
# download amd64 linux kubectl
$ curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
$ chmod +x kubectl
$ sudo mv kubectl /usr/local/bin/

# download arm64 linux kubectl
$ curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/arm64/kubectl"
$ chmod +x kubectl
$ sudo mv kubectl /usr/local/bin/
```

On macOS, you can also use Homebrew:

```bash theme={null}
$ brew install kubectl
$ brew install istioctl
```

If you install `istioctl` via Homebrew, confirm the version matches the one required for your tasks (e.g., `1.26.3`).

## Istio installation profiles

Istio provides multiple install profiles suitable for different use cases:

|                        Profile | Use case                                                    |
| -----------------------------: | ----------------------------------------------------------- |
|                      `default` | General-purpose production-like install                     |
|                         `demo` | Useful for learning, examples, includes gateways and addons |
|                      `minimal` | Only the control plane (istiod)                             |
|                      `ambient` | Ambient Mesh model (sidecarless)                            |
| `remote` / `empty` / `preview` | Special deployment variants                                 |

In this guide we use the `demo` profile for quick examples and reference `ambient` conceptually where relevant.

## Install Istio with istioctl (recommended for most labs)

Install the `demo` profile:

```bash theme={null}
$ istioctl install --set profile=demo -y
✔ Istio core installed
✔ Istiod installed
✔ Egress gateways installed
✔ Ingress gateways installed
✔ Installation complete

Please verify that Istio is running:
kubectl get pods -n istio-system
```

Verify control plane pods:

```bash theme={null}
$ kubectl get pods -n istio-system
NAME                                           READY   STATUS    RESTARTS   AGE
istio-egressgateway-6db9994577-sn95p          1/1     Running   0          79s
istio-ingressgateway-58649bfd4-cs4fk          1/1     Running   0          79s
istiod-dd4b7db5-nxrjv                         1/1     Running   0          111s
```

Installing Istio does not automatically update application workloads. Sidecar injection (automatic or manual) is required to add the Envoy sidecar to application pods.

> **warning** Avoid mixing widely different `istioctl` and control plane versions. Use compatible versions to prevent unexpected behavior. When in doubt, match `istioctl` to your desired control plane version.

## Install Istio with Helm (modular approach)

When you prefer Helm, install three logical charts: `base`, `istiod`, and gateway (ingress/egress). First add the Istio Helm repository:

```bash theme={null}
$ helm repo add istio https://istio-release.storage.googleapis.com/charts
$ helm repo update
```

Install the base (cluster resources):

```bash theme={null}
$ helm install istio-base istio/base --namespace istio-system --version 1.26.3 --create-namespace --wait
```

Install the control plane:

```bash theme={null}
$ helm install istiod istio/istiod --namespace istio-system --version 1.26.3 --wait
```

Install an ingress gateway (example):

```bash theme={null}
$ helm install istio-ingress istio/gateway --namespace istio-ingress --version 1.26.3 --create-namespace --wait
```

Verify Helm releases:

```bash theme={null}
$ helm ls -A
NAME        NAMESPACE     REVISION    UPDATED                                 STATUS      CHART                 APP VERSION
istio-base  istio-system  1           2022-01-01 00:00:00.000000 +0000 UTC    deployed    istio-base-1.26.3
...
```

Note: Both `istioctl install` and Helm produce functionally equivalent installations. Sidecar injection is still required for application pods.

## Deploy and validate the Bookinfo sample application

Apply the Bookinfo sample for Istio release `1.26`:

```bash theme={null}
$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/platform/kube/bookinfo.yaml
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
details-v1-7c5d957895-mkf1q           1/1     Running   0          8s
productpage-v1-f47f868c8-v6qdl        1/1     Running   0          7s
ratings-v1-85cf8d8647-8cqxS           1/1     Running   0          8s
reviews-v1-5fc874d67c-lpg76           1/1     Running   0          8s
reviews-v2-f6d449f65-hwtz9            1/1     Running   0          8s
reviews-v3-76f75877b9-q7d75           1/1     Running   0          8s
```

At this point each pod shows `1/1` READY because the application pods have not had an Istio sidecar injected yet.

### Enable automatic sidecar injection (namespace labeling)

Label the namespace to enable automatic sidecar injection (example: `default`):

```bash theme={null}
$ kubectl label namespace default istio-injection=enabled
$ kubectl get ns default --show-labels
NAME     STATUS   AGE   LABELS
default  Active   20h   istio-injection=enabled,kubernetes.io/metadata.name=default
```

After labeling, existing pods must be restarted (recreated) to receive the sidecar. Delete and reapply manifests or use rollout restart on Deployments.

Recreate Bookinfo pods to pick up injected sidecars:

```bash theme={null}
$ kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/platform/kube/bookinfo.yaml
$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/platform/kube/bookinfo.yaml
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
details-v1-7c5d957895-pss97           2/2     Running   0          8s
productpage-v1-f47f868c8-wtkx2        2/2     Running   0          7s
ratings-v1-85cf8d8647-tl6cr           2/2     Running   0          8s
reviews-v1-5fc87d67c-h8925            2/2     Running   0          7s
reviews-v2-f6d449f65-p4zwc            2/2     Running   0          7s
reviews-v3-76f75877b-gn88k            2/2     Running   0          7s
```

`2/2` indicates the application container plus the injected `istio-proxy` sidecar.

### Inspect a pod to verify the sidecar

Describe a pod to check containers and images:

```bash theme={null}
$ kubectl describe pod details-v1-7c5d957895-pss97
Containers:
  details:
    Image:          docker.io/istio/examples-bookinfo-details-v1:1.20.2
    Port:           9080/TCP
    State:          Running
    ...
  istio-proxy:
    Image:          docker.io/istio/proxyv2:1.26.3
    Port:           15000/TCP
    State:          Running
    ...
```

### Manual sidecar injection (alternative)

If you prefer to inject sidecars only for selected manifests, use manual injection (note that commands and tooling have evolved across versions):

```bash theme={null}
$ wget https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/platform/kube/bookinfo.yaml -O bookinfo.yaml
$ istioctl kube-inject -f bookinfo.yaml | kubectl apply -f -
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
details-v1-7c5d957895-pss97           2/2     Running   0          8s
productpage-v1-f47f868c8-wtx2         2/2     Running   0          7s
ratings-v1-85cf8d8647-tl6cr           2/2     Running   0          8s
reviews-v1-5fc87d67c-h8925            2/2     Running   0          7s
reviews-v2-f6d449f65-p4zwc            2/2     Running   0          7s
reviews-v3-7675787b9-gn88k            2/2     Running   0          7s
```

Manual injection is useful when you want sidecars only on selected workloads. Always consult the Istio docs for the preferred injection workflow for your Istio version.

## Validate and analyze Istio configuration

Istio provides commands to validate YAML and analyze in-cluster configuration. Prefer `istioctl analyze` as it is the recommended diagnostic tool.

```bash theme={null}
# validate a YAML file (older command; may be deprecated)
$ istioctl validate -f filename.yaml
"filename.yaml" is valid

# analyze a file
$ istioctl analyze -f filename.yaml

# analyze installed/in-cluster configuration (all namespaces)
$ istioctl analyze -A

# analyze a specific namespace
$ istioctl analyze -n default

# verify installation
$ istioctl verify-install
```

`istioctl analyze` helps catch configuration issues (missing references, invalid fields, etc.). Make it part of your workflow when authoring Istio YAML, during CI, or while preparing for labs and exams.

## Quick reference tables

Installation methods comparison:

| Method                                         | Pros                                                | Cons                                      |
| ---------------------------------------------- | --------------------------------------------------- | ----------------------------------------- |
| `istioctl install`                             | Simple, recommended for labs and quick installs     | Less modular for advanced customization   |
| Helm (`istio/base`, `istiod`, `istio/gateway`) | Modular, integrates well with GitOps/Helm workflows | Slightly more steps to install and manage |

Common validation commands:

|                            Command | Purpose                                                      |
| ---------------------------------: | ------------------------------------------------------------ |
|              `istioctl analyze -A` | Analyze in-cluster Istio configuration across all namespaces |
|          `istioctl verify-install` | Verify that installation resources are present and healthy   |
| `kubectl get pods -n istio-system` | Confirm control plane pods are running                       |
|       `kubectl describe pod <pod>` | Inspect containers to confirm sidecar injection              |

## Summary

* Prepare `kubectl` and `istioctl` and ensure versions are compatible.
* Install Istio either with `istioctl` (simple/demo installs) or Helm (modular installs).
* Enable sidecar injection via namespace labels for automatic injection, or use manual injection for selective workloads.
* Use `istioctl analyze` and `istioctl verify-install` to validate configuration and catch issues early.
* Deploy the Bookinfo sample to verify sidecar injection and gateway behavior.

Links and references

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Istio Helm charts repository](https://istio-release.storage.googleapis.com/charts)
* ICA exam reference: [https://learn.kodekloud.com/user/courses/istio-certified-associate](https://learn.kodekloud.com/user/courses/istio-certified-associate)

Now that installation concepts are covered, proceed to hands-on practice in your lab environment using the example commands above.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/fa19694a-32dd-4e5d-bf0f-cd0cb6a11dc6)


# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Introduction/page

Guide to installing, configuring, customizing, and managing Istio on Kubernetes, covering istioctl, Helm, Istio Operator, Ambient Mode, ztunnel, upgrades and uninstall strategies.

In this module we'll cover everything you need to install, configure, customize, and manage Istio in a Kubernetes environment. The sequence follows a practical install-first, customize-next approach so you can apply what you learn in real clusters.

What we'll cover (in order)

* Prerequisites and environment requirements (spoiler: you need Kubernetes).
* Install `istioctl` and use it to install and enable Istio.
* Review Istio installation profiles, including Ambient Mode.
* Install Istio with Helm as an alternative.
* Customize Istio using the Istio Operator (important for production).
* Install Ambient Mode and get started with the ztunnel.
* Perform upgrades and uninstall Istio using canary upgrade patterns.

> **lightbulb** Before you begin, make sure you have a running Kubernetes cluster and `kubectl` configured with cluster-admin privileges. Typical minimums:

  * Kubernetes 1.21+ recommended.
  * `kubectl` and `helm` CLI installed locally.
  * `istioctl` for the quick-install path (we'll show how to install it).

<Frame>
  <img alt="The image lists three objectives related to Istio: installing it using Helm, customizing it with the Istio Operator, and installing and configuring Ambient Mode." />
</Frame>

Module overview (quick reference)

| Topic                       | Purpose                                                          | Example / Command                                                                   |
| --------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Install using `istioctl`    | Fast path, recommended for most users                            | `istioctl install --set profile=demo`                                               |
| Install using Helm          | Integrates with Helm workflows                                   | `helm repo add istio https://istio-release.storage.googleapis.com/charts`           |
| Istio Profiles              | Choose components and features (default, demo, minimal, ambient) | `istioctl profile dump`                                                             |
| Istio Operator              | Declarative customization and lifecycle management               | `kubectl apply -f istio-operator.yaml`                                              |
| Ambient Mode                | Sidecarless service mesh alternative                             | Enable via profile or operator configuration                                        |
| ztunnel                     | Data-plane component used in Ambient Mode                        | Configure `ztunnel` as described in the Ambient Mode docs                           |
| Canary upgrades & uninstall | Safe upgrade/uninstall strategies                                | Canary: roll out control-plane revisions; Uninstall: `istioctl x uninstall --purge` |

Additional links and references

* [Istio Official Documentation](https://istio.io/latest/docs/)
* [Installing Istio with istioctl](https://istio.io/latest/docs/setup/install/istioctl/)
* [Istio Helm Charts](https://istio.io/latest/docs/setup/install/helm/)

> **warning** This is definitely going to be on the exam.

This is definitely going to be on the exam.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/65f60295-4ffb-477b-b3da-7f086e533016)
