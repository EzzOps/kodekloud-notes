# ... truncated output showing single container "details" and no istio-proxy container ...
Annotations: <none>
Status: Running
IP: 10.50.0.4
Controlled By: ReplicaSet/details-v1-65599dcf88
Containers:
  details:
    Image: docker.io/istio/examples-bookinfo-details-v1:1.16.2
    Port: 9080/TCP
    State: Running
    Ready: True
    Restart Count: 0
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-67k5r (ro)
```

## 2) Install istioctl client (if not already installed)

Check for the `istioctl` client:

```bash theme={null}
root@controlplane:~# istioctl version
-bash: istioctl: command not found
```

Download the chosen Istio release (example: `1.26.3`) and add `istioctl` to your `PATH`:

```bash theme={null}
root@controlplane:~# curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.26.3 sh -
# Download completes and places files in ./istio-1.26.3 directory
root@controlplane:~# cd istio-1.26.3
root@controlplane:~/istio-1.26.3# export PATH=$PWD/bin:$PATH
```

Verify the client is available and that Istio is not yet installed in the cluster:

```bash theme={null}
root@controlplane:~/istio-1.26.3# istioctl version
Istio is not present in the cluster: no running Istio pods in namespace "istio-system"
client version: 1.26.3
```

> **warning** Version compatibility note: Use an `istioctl` client that matches (or is compatible with) the Istio control plane version you will install. Mixing incompatible versions can cause install or runtime issues.

## 3) Install the Istio control plane (demo profile)

Install Istio into the cluster using the `demo` profile for an easier, feature-rich setup suitable for demos and labs:

```bash theme={null}
root@controlplane:~/istio-1.26.3# istioctl install --set profile=demo -y
✔ Istio core installed
✔ Istiod installed
✔ Egress gateways installed
✔ Ingress gateways installed
✔ Installation complete
```

Confirm `istio-system` pods are running:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl get pods -n istio-system
NAME                                         READY   STATUS    RESTARTS   AGE
istio-egressgateway-fbdbf94c6-nqzj5         1/1     Running   0          24s
istio-ingressgateway-7f9cb54c46-nff5v       1/1     Running   0          24s
istiod-6699bd67b9-64dt9                     1/1     Running   0          34s
```

## 4) Enable automatic sidecar injection for the `default` namespace

Run an analysis to detect if the namespace is enabled for injection:

```bash theme={null}
root@controlplane:~/istio-1.26.3# istioctl analyze -n default
Info [IST0102] (Namespace default) The namespace is not enabled for Istio injection. Run 'kubectl label namespace default istio-injection=enabled' to enable it, or 'kubectl label namespace default istio-injection=disabled' to explicitly mark it as not needing injection.
```

Label the `default` namespace to enable automatic sidecar injection:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl label namespace default istio-injection=enabled
```

Re-run the analyzer. It will warn about existing pods that were created before the namespace was labeled and are therefore missing the proxy:

```bash theme={null}
root@controlplane:~/istio-1.26.3# istioctl analyze -n default
Warning [IST0103] (Pod default/details-v1-65599dcf88-k44bb) The pod default/details-v1-65599dcf88-k44bb is missing the Istio proxy. This can often be resolved by restarting or redeploying the workload.
# ... similar warnings for other pods created before labeling ...
```

Since automatic injection is applied at pod creation time, restart or redeploy any existing workloads so the injector can add the `istio-proxy`. One simple way is to do a rollout restart for the relevant deployments:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl rollout restart deployment details-v1 productpage-v1 -n default
```

After restarting, the affected pods should show two containers (application + `istio-proxy`). The terminal screenshot below demonstrates the change from `1/1` to `2/2` for injected pods.

<Frame>
  <img alt="The image shows a terminal displaying the status of Kubernetes pods and deployments, with commands such as kubectl get pods and kubectl get deployments.apps being executed." />
</Frame>

Verify pods and deployments:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl get pods
NAME                                    READY   STATUS    RESTARTS   AGE
details-v1-86994d6f5b-qbw44             2/2     Running   0          10s
productpage-v1-768d845896-gg7d74        1/2     Running   0          6s
ratings-v1-59b99c644-fhsp8              1/1     Running   0          3m57s
reviews-v1-598599584-k4lph              1/1     Running   0          3m57s
reviews-v2-86d6cc668-ntqwq              1/1     Running   0          3m57s
reviews-v3-dbb5f5bd-ffg9v               1/1     Running   0          3m57s

root@controlplane:~/istio-1.26.3# kubectl get deployments.apps
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
details-v1       1/1     1            1           4m2s
productpage-v1   1/1     1            1           4m1s
ratings-v1       1/1     1            1           4m2s
reviews-v1       1/1     1            1           4m2s
reviews-v2       1/1     1            1           4m2s
reviews-v3       1/1     1            1           4m2s
```

Describe a restarted pod to see the added `istio-proxy` container (snippet):

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl describe pod details-v1-86994d6f5b-qbw44
Containers:
  details:
    Image: docker.io/istio/examples-bookinfo-details-v1:1.16.2
    Port: 9080/TCP
    Ready: True
  istio-proxy:
    Image: docker.io/istio/proxyv2:1.26.3
    Port: 15090/TCP
    Args:
      proxy
      sidecar
      --domain
      $(POD_NAMESPACE).svc.cluster.local
      --proxyLogLevel=warning
    State: Running
    Ready: True
    Limits:
      cpu: 2
      memory: 1Gi
    Requests:
      cpu: 10m
      memory: 40Mi
    Readiness: http-get http://:15021/healthz/ready delay=0s timeout=3s period=15s #success=1 #failure=4
    Environment:
      PILOT_CERT_PROVIDER: istiod
      CA_ADDR: istiod.istio-system.svc:15012
      POD_NAME: details-v1-86994d6f5b-qbw44
      POD_NAMESPACE: default
      INSTANCE_IP: $(status.podIP)
      SERVICE_ACCOUNT: $(spec.serviceAccountName)
```

## 5) Reinstall Bookinfo (optional)

If you prefer to recreate the Bookinfo app so that all pods are freshly created with the proxy already injected, delete and reapply the Bookinfo manifest:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
# ... deletion output ...
root@controlplane:~/istio-1.26.3# kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
# ... creation output ...
```

After reapplying, pods will be created in the labeled `default` namespace and will automatically include the sidecar.

## 6) Demonstrate manual (per-workload) injection

Automatic injection is namespace-scoped. You can also inject sidecars for individual manifests when you cannot or do not want to label a namespace.

Create a new namespace and confirm it has no `istio-injection` label:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl create ns db
namespace/db created

root@controlplane:~/istio-1.26.3# kubectl get ns --show-labels
NAME              STATUS   AGE    LABELS
db                Active   2s     kubernetes.io/metadata.name=db
default           Active   9m22s  istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   4m22s  kubernetes.io/metadata.name=istio-system
# ...
```

Run a Redis pod in the `db` namespace without injection:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl run redis-no-proxy --image=redis -n db
pod/redis-no-proxy created

root@controlplane:~/istio-1.26.3# kubectl get pods -n db
NAME             READY   STATUS              RESTARTS   AGE
redis-no-proxy   0/1     ContainerCreating   0          7s
```

Prepare a manifest for a second Redis pod using `--dry-run=client` and save it to `pod.yaml`:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl run redis-istio-proxy --image=redis -n db --dry-run=client -o yaml > pod.yaml
```

Inject the Istio sidecar into that manifest and create the pod:

```bash theme={null}
root@controlplane:~/istio-1.26.3# istioctl kube-inject -f pod.yaml | kubectl apply -f -
pod/redis-istio-proxy created
```

Verify both pods in the `db` namespace:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl get pods -n db
NAME               READY   STATUS    RESTARTS   AGE
redis-no-proxy     1/1     Running   0          90s
redis-istio-proxy  2/2     Running   0          30s
```

Describe the manually injected pod to confirm the `istio-proxy` container and its configuration:

```bash theme={null}
root@controlplane:~/istio-1.26.3# kubectl describe pod redis-istio-proxy -n db
Containers:
  redis:
    Image: redis
    Ready: True
  istio-proxy:
    Image: docker.io/istio/proxyv2:1.26.3
    Args:
      proxy
      sidecar
      --domain
      $(POD_NAMESPACE).svc.cluster.local
      --proxyLogLevel=warning
    Ready: True
    Limits:
      cpu: 2
      memory: 1Gi
    Environment:
      PILOT_CERT_PROVIDER: istiod
      CA_ADDR: istiod.istio-system.svc:15012
      POD_NAME: redis-istio-proxy
      POD_NAMESPACE: db
      ISTIO_META_INTERCEPTION_MODE: REDIRECT
      ISTIO_META_WORKLOAD_NAME: redis-istio-proxy
```

> **lightbulb** Manual injection (via `istioctl kube-inject`) is useful when you cannot or do not want to label a namespace for automatic injection. Generate a YAML manifest with `kubectl --dry-run=client -o yaml` and run `istioctl kube-inject -f pod.yaml | kubectl apply -f -`.

## Quick reference — common commands

| Task                                     | Command / Example                                                     |                      |
| ---------------------------------------- | --------------------------------------------------------------------- | -------------------- |
| Check pods                               | `kubectl get pods`                                                    |                      |
| Describe pod                             | `kubectl describe pod <pod-name>`                                     |                      |
| Install Istio (demo)                     | `istioctl install --set profile=demo -y`                              |                      |
| Enable automatic injection               | `kubectl label namespace <ns> istio-injection=enabled`                |                      |
| Restart deployments to trigger injection | `kubectl rollout restart deployment <deploy-name> -n <ns>`            |                      |
| Generate pod YAML                        | `kubectl run redis --image=redis --dry-run=client -o yaml > pod.yaml` |                      |
| Manual injection from manifest           | \`istioctl kube-inject -f pod.yaml                                    | kubectl apply -f -\` |

## Summary

* Install `istioctl` and use it to install Istio into your cluster (`istioctl install`).
* Enable automatic sidecar injection on a namespace with `kubectl label namespace <ns> istio-injection=enabled` (replace `<ns>` with your namespace).
* Restart or redeploy workloads created prior to labeling so the sidecar injector can modify their pod specs.
* Use `istioctl kube-inject -f pod.yaml | kubectl apply -f -` to inject a sidecar into individual manifests for per-workload injection.

This concludes the demo of installing Istio via the CLI and injecting sidecars both automatically and manually.

## Links and references

* [Istio Installation Guide](https://istio.io/latest/docs/setup/install/)
* [istioctl reference](https://istio.io/latest/docs/reference/commands/istioctl/)
* [Bookinfo sample manifests (Istio GitHub)](https://github.com/istio/istio/tree/release-1.11/samples/bookinfo)
* [Kubernetes kubectl documentation](https://kubernetes.io/docs/reference/kubectl/overview/)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/f9286a62-5585-445c-b649-8323b83fae22)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/eb471648-119e-4abc-b769-4b7f99bfadd1)


# Demo Install Istio via Helm

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Demo-Install-Istio-via-Helm/page

Guide to installing Istio on Kubernetes using Helm, covering base istiod and gateway charts, CRD verification, automatic sidecar injection, sample workload deployment, and Helm value customization.

Installing Istio with Helm is a reliable way to get the control plane and gateway running in your cluster. This guide walks through a minimal, reproducible workflow: add the Istio Helm repo, install the three required charts (base, istiod, gateway), verify CRDs, enable automatic sidecar injection for a namespace, deploy a sample workload, and extract/modify Helm values for customization.

Prerequisites

* A Kubernetes cluster (start from a clean cluster to follow this demo).
* kubectl configured to talk to the cluster.
* Helm installed on the control plane or a machine with cluster access.

Verify your cluster has only default workloads:

```bash theme={null}
kubectl get pods -A
```

Confirm Helm is available:

```bash theme={null}
which helm
