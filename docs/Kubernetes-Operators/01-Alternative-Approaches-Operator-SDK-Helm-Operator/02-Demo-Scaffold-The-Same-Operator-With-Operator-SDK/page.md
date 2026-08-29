# Example of what make install runs:
# kustomize build config/crd | kubectl apply -f -
```

Example output:

```text theme={null}
customresourcedefinition.apiextensions.k8s.io/nginxes.demo.example.com created
```

Start the operator in the foreground (leave this running in one terminal):

```bash theme={null}
make run
```

Example operator logs when starting:

```json theme={null}
{"level":"info","ts":"2026-06-16T11:34:35+02:00","logger":"controller-runtime.metrics","msg":"Serving metrics server","bindAddress":":8080","secure":false}
{"level":"info","ts":"2026-06-16T11:34:35+02:00","msg":"Starting EventSource","controller":"nginx-controller","source":"kind source: unstructured.Unstructured{}"}
{"level":"info","ts":"2026-06-16T11:34:35+02:00","msg":"Starting Controller","controller":"nginx-controller"}
{"level":"info","ts":"2026-06-16T11:34:35+02:00","msg":"Starting workers","controller":"nginx-controller","worker count":16}
```

## Create a release by applying the sample CR

In another terminal, apply the generated sample custom resource that represents an NGINX release:

```bash theme={null}
kubectl apply -f config/samples/demo_v1_nginx.yaml
```

Example output:

```text theme={null}
nginxes.demo.example.com/nginx-sample created
```

What happens:

* The controller sees the new `Nginx` object.
* It reads `.spec` from the CR and passes those values into Helm rendering.
* Helm templates are rendered and the resulting Kubernetes resources (Deployment, Service, ConfigMap, etc.) are created.

No custom Go reconciler code is needed; the operator uses Helm to manage the release lifecycle.

## Verify the release and troubleshoot

Wait for the generated deployment to become available:

```bash theme={null}
kubectl wait --for=condition=Available deploy/nginx-sample --timeout=120s
```

Inspect replicas and ready replicas:

```bash theme={null}
kubectl get deploy nginx-sample -o jsonpath='{.spec.replicas}{"/"}{.status.readyReplicas}{"\n"}'
```

List resources associated with this Helm release using the instance label:

```bash theme={null}
kubectl get deploy -l app.kubernetes.io/instance=nginx-sample
```

If you need to inspect the full generated Deployment:

```bash theme={null}
kubectl get deploy nginx-sample -o yaml
```

## Update desired state by patching the CR

To change desired state, patch the custom resource. For example, update the replica count:

```bash theme={null}
kubectl patch nginx nginx-sample --type=merge -p '{"spec":{"replicaCount":4}}'
```

The Helm operator will reconcile the change and upgrade the Helm release. Confirm the deployment scaled:

```bash theme={null}
kubectl get deploy nginx-sample -o json
```

## Delete the release by deleting the CR

To uninstall the release, delete the custom resource:

```bash theme={null}
kubectl delete nginx nginx-sample
```

The operator will uninstall the associated Helm release and clean up API objects created by the chart.

## Summary and when to choose Helm vs Go operators

Helm-based operators are ideal when:

* You already have a Helm chart that represents the application lifecycle.
* The CR only needs to expose chart values (mapping `spec` → Helm values).
* You want to avoid writing reconciliation code.

Consider a Go-based controller when:

* You need advanced reconciliation logic.
* You must call external APIs or implement complex status updates.
* Custom status computation or multi-resource coordination is required.

Useful references:

* Operator SDK (Helm plugin): [https://sdk.operatorframework.io/docs/helm/overview/](https://sdk.operatorframework.io/docs/helm/overview/)
* Helm: [https://helm.sh](https://helm.sh)
* Kubernetes CRDs: [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/d2537d70-4008-4d53-ad04-b7731ca0f7c0/lesson/d73a38de-90cd-446d-9c96-0653e88167c8)


# Demo Scaffold The Same Operator With Operator SDK

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Alternative-Approaches-Operator-SDK-Helm-Operator/Demo-Scaffold-The-Same-Operator-With-Operator-SDK/page

Guide to scaffolding a Go WebApp Kubernetes operator with Operator SDK, covering installation, project initialization, API and controller creation, generated code inspection, manifests, and layout comparison with Kubebuilder

You previously built a web app operator using Kubebuilder. In this lesson you'll scaffold the same Go operator with the Operator SDK and compare the resulting project layout. The objective is to observe the initial scaffold and reconcile model—this is not a walkthrough to re-implement the web app logic.

This guide covers:

* Prerequisites
* Installing the operator-sdk CLI (Linux / macOS)
* Initializing a new Go operator project
* Creating the WebApp API and controller
* Inspecting generated code and manifests
* Comparing the generated PROJECT layout and plugins

## Prerequisites

* Go toolchain installed and configured (Go 1.19+ recommended)
* Git and curl available
* Optional: a disposable workspace (example: an ephemeral container or temporary directory)

## Install operator-sdk

### Linux installation (recommended steps)

Download the release binary for your architecture, verify the signed checksums, and place the binary on your PATH as `operator-sdk`.

```bash theme={null}
export OPERATOR_SDK_VERSION=v1.42.2
export OPERATOR_SDK_DL_URL="https://github.com/operator-framework/operator-sdk/releases/download/${OPERATOR_SDK_VERSION}"
curl -LO "${OPERATOR_SDK_DL_URL}/operator-sdk_linux_amd64"
curl -LO "${OPERATOR_SDK_DL_URL}/checksums.txt"
curl -LO "${OPERATOR_SDK_DL_URL}/checksums.txt.asc"
```

Import and verify the release signing key, then verify the checksums:

```bash theme={null}
gpg --keyserver keyserver.ubuntu.com --recv-keys 052996E2A20B5C7E
gpg --verify checksums.txt.asc checksums.txt
sha256sum --check --ignore-missing checksums.txt
