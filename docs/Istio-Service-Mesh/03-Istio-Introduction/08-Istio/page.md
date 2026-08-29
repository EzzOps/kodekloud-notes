# Download the latest Istio release (this creates a directory like istio-1.10.3)
curl -L https://istio.io/downloadIstio | sh -
```

Be aware: this downloads the Istio release into your current directory, so run it from a location where you want the release folder to be created.

Sample download output and inspection of the folder:

```bash theme={null}
Istio 1.10.3 Download Complete!

Istio has been successfully downloaded into the istio-1.10.3 folder on your system.

Next Steps:
See https://istio.io/latest/docs/setup/install/ to add Istio to your Kubernetes cluster.

To configure the istioctl client tool for your workstation,
add the /Users/istiotraining/istio-1.10.3/bin directory to your environment path variable with:
    export PATH="$PATH:/Users/istiotraining/istio-1.10.3/bin"

Begin the Istio pre-installation check by running:
    istioctl x precheck

Need more information? Visit https://istio.io/latest/docs/setup/install/

istiotraining@local ~ $ cd istio-1.10.3/
istiotraining@local istio-1.10.3 $ ls
LICENSE        README.md        bin        manifest.yaml    manifests    samples    tools

istiotraining@local istio-1.10.3 $ ls bin/
istioctl

istiotraining@local istio-1.10.3 $ ls samples/
README.md    custom-bootstrap    helloworld    multicluster    sleep
addons    extauthz    httpbin    operator    tcp-echo
bookinfo    external    jwt-server    ratelimit    websockets
certs    health-check    kubernetes-blog    security

istiotraining@local istio-1.10.3 $ ls tools/
_istioctl    certs    istioctl.bash
```

## 3) Add istioctl to your PATH

Add the release `bin` directory to your PATH (example for Linux/macOS):

```bash theme={null}
export PATH=$PWD/bin:$PATH
```

Confirm the `istioctl` client is available and check its version:

```bash theme={null}
istiotraining@local istio-1.10.3 $ istioctl version
no running Istio pods in "istio-system"
1.10.3
```

The client reports its version (here `1.10.3`) and notes whether it sees any running Istio pods in the cluster.

## 4) Verify the cluster is ready for Istio

Run verification and preflight checks:

```bash theme={null}
istiotraining@local istio-1.10.3 $ istioctl verify-install
0 Istio control planes detected, checking --revision "default" only
error while fetching revision : the server could not find the requested resource
0 Istio injectors detected
Error: could not load IstioOperator from cluster: the server could not find the requested resource. Use --filename
```

Explanation:

* `istioctl verify-install` attempts to detect an installed control plane and will fail if no control plane manifests have been applied.
* After download, you should run `istioctl x precheck` to confirm cluster prerequisites and then install a control plane (for example, using `istioctl install` or the Istio Operator).

## Quick reference table

| Command                                                                    | Purpose                                          | Notes / Link                                                                                                       |                                                |
| -------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `minikube start`                                                           | Start a Minikube cluster (auto-selects a driver) | See Minikube docs: [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/)                        |                                                |
| `minikube addons enable ingress`                                           | Enable the ingress addon                         | On macOS Docker driver this may fail — use a VM driver                                                             |                                                |
| `minikube delete`                                                          | Remove the local Minikube cluster                | Recreates VM if you restart with a different driver                                                                |                                                |
| \`curl -L [https://istio.io/downloadIstio](https://istio.io/downloadIstio) | sh -\`                                           | Download latest Istio release and `istioctl`                                                                       | Creates `istio-<version>` in current directory |
| `export PATH=$PWD/bin:$PATH`                                               | Add `istioctl` to PATH                           | Run from inside the downloaded Istio folder                                                                        |                                                |
| `istioctl x precheck`                                                      | Pre-installation checks                          | Ensures cluster meets Istio prerequisites                                                                          |                                                |
| `istioctl install` or Istio Operator                                       | Install Istio control plane                      | See Istio install docs: [https://istio.io/latest/docs/setup/install/](https://istio.io/latest/docs/setup/install/) |                                                |

## Recommended next steps

1. Run `istioctl x precheck` to ensure your cluster meets prerequisites.
2. Install an Istio control plane:
   * Use `istioctl install` for a quick, configurable install, or
   * Use the Istio Operator for lifecycle management.
3. Follow the official Istio installation guide: [https://istio.io/latest/docs/setup/install/](https://istio.io/latest/docs/setup/install/)
4. If you ran into a Minikube ingress limitation on macOS, follow the related issue for updates: [https://github.com/kubernetes/minikube/issues/7332](https://github.com/kubernetes/minikube/issues/7332)

Related resources:

* Istio installation docs: [https://istio.io/latest/docs/setup/install/](https://istio.io/latest/docs/setup/install/)
* Minikube documentation: [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-service-mesh/module/dc0a9efc-09ce-4310-86e9-1c7aaab6a7d8/lesson/12a627c5-7aec-43ae-a211-1980cf9a9255)


# Istio

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Istio-Introduction/Istio/page

This lesson explores Istios architecture, operation, and key components to enhance microservices environments.

In this lesson, we explore Istio—its architecture, operation, and key components—to help you understand how it enhances microservices environments.

Istio is an open-source service mesh that simplifies securing, connecting, and monitoring services within both Kubernetes and traditional workloads. It provides universal traffic management, telemetry, and security for complex deployments, and is widely supported by major cloud providers and consulting firms.

> **lightbulb** Istio leverages an open-source, high-performance proxy called Envoy. These Envoy proxies offload critical tasks from microservices, ensuring efficient communication between services as part of the data plane.

## Istio Architecture

Istio's architecture is divided into two main parts: the data plane and the control plane.

### Data Plane

The data plane consists of Envoy proxies that are deployed alongside each service instance (or pod). These proxies handle crucial functions such as load balancing, security, and observability.

### Control Plane

The control plane manages and configures the proxies to route traffic, enforce policies, and collect telemetry data. Originally, Istio’s control plane was composed of three separate components:

* **Citadel:** Responsible for generating and managing certificates for secure communications.
* **Pilot:** Handles service discovery and maintains routing configurations.
* **Galley:** Validates configuration files to ensure correct settings.

Later, these components were consolidated into a single daemon called Istiod, streamlining the architecture and simplifying management.

![The image is a diagram of a microservices architecture using Istio, showing a control plane with Istiod, Citadel, Pilot, and Galley, and a data plane with services like Product Page, Details, Reviews, and Ratings, each with an Envoy proxy.](https://kodekloud.com/kk-media/image/upload/v1752879340/notes-assets/images/Istio-Service-Mesh-Istio/microservices-istio-architecture-diagram.jpg)

Within each pod, an Istio agent works in tandem with the Envoy proxy. The agent is responsible for delivering configuration secrets and other necessary data to ensure that the proxy operates correctly.

> **lightbulb** This overview of Istio's architecture provides the groundwork for understanding its installation process and advanced features, which will be covered in subsequent sections.

In the next sections, we will delve into the installation process for Istio and explore its comprehensive features and functionalities in detail.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-service-mesh/module/dc0a9efc-09ce-4310-86e9-1c7aaab6a7d8/lesson/59b3de7e-9646-414d-a5b8-0f3a262f4a74)
