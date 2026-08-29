# Demo Customize Istio Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Demo-Customize-Istio-Installation/page

Guide to customizing Istio installations using the Istio Operator CR to configure profiles, gateways, resource overrides, enable automatic sidecar injection, and deploy Bookinfo with istioctl commands

In this lesson you will use the Istio Operator (IstioOperator CR) to customize an Istio installation. The workflow covers:

1. Inspecting the cluster and current workloads
2. Creating a custom `IstioOperator` manifest (`demo.yaml`)
3. Validating and applying the manifest with `istioctl`
4. Verifying pods and resource overrides
5. Enabling automatic sidecar injection and redeploying Bookinfo

This approach is preferable to using `--set` flags because it centralizes configuration in a declarative manifest that the operator will reconcile.

***

## Prerequisites

* `kubectl` configured to your target cluster
* `istioctl` on your PATH
* A running Kubernetes cluster with some sample workloads (e.g., Bookinfo)

***

## 1) Inspect cluster state

Example: the cluster already has Bookinfo pods running:

```bash theme={null}
kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
details-v1-65599dcf88-qjhsw       1/1     Running   0          12m
productpage-v1-9487c29c5b-2k9mf   1/1     Running   0          12m
ratings-v1-59b99c644-7w272        1/1     Running   0          12m
reviews-v1-5985999584-gms7g       1/1     Running   0          12m
reviews-v1-86d6cc668-l2pvr        1/1     Running   0          12m
reviews-v1-db5fb5bd-bzxt4         1/1     Running   0          12m
```

Verify `istioctl` can talk to the cluster:

```bash theme={null}
istioctl version
Istio is not present in the cluster: no running Istio pods in namespace "istio-system"
client version: 1.26.3
```

***

## 2) Create a minimal IstioOperator manifest

Create and edit `demo.yaml`:

```bash theme={null}
touch demo.yaml
vim demo.yaml
```

A minimal manifest that selects the `demo` profile:

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
```

Validate the manifest:

```bash theme={null}
istioctl validate -f demo.yaml
"demo.yaml" is valid
```

Install using the operator manifest:

```bash theme={null}
istioctl install -f demo.yaml -y
```

Verify Istio system pods:

```bash theme={null}
kubectl get pods -n istio-system
NAME                                      READY   STATUS    RESTARTS   AGE
istio-egressgateway-fbdbf94c6-j64m7      1/1     Running   0          20s
istio-ingressgateway-7f9cb54c46-lzfcv    1/1     Running   0          19s
istiod-6699bd67b9-swz6j                  1/1     Running   0          24s
```

Inspect an ingress gateway pod to view resource requests/limits and environment. Example excerpt from `kubectl describe pod`:

```text theme={null}
Limits:
  cpu: 2
  memory: 1Gi
Requests:
  cpu: 10m
  memory: 40Mi
Readiness: http-get http://:15021/healthz/ready delay=1s timeout=1s period=2s #success=1 #failure=30
Environment:
  PILOT_CERT_PROVIDER: istiod
  CA_ADDR: istiod.istio-system.svc:15012
  NODE_NAME: (v1:spec.nodeName)
  POD_NAME: istio-ingressgateway-7f9cb54c46-lzfcv (v1:metadata.name)
  POD_NAMESPACE: istio-system (v1:metadata.namespace)
  INSTANCE_IP: (v1:status.podIP)
  HOST_IP: (v1:status.hostIP)
Mounts:
  /etc/istio/config from config-volume (rw)
  ...
```

***

> **warning** Kubernetes Deployments cannot be renamed. To change the name of a gateway deployment managed by the operator you must disable the old gateway and enable a new one with the desired name. The operator will delete and recreate the deployment.

***

## 3) Example: Customize gateways and resource overrides

To change gateway names (e.g., add `-gateway`) and reduce resource sizes, update `demo.yaml`. The operator will handle removing disabled resources and creating the newly named ones.

Example `IstioOperator` manifest (add to or replace your `demo.yaml` as needed):

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  components:
    egressGateways:
      - enabled: false
        name: istio-egressgateway
        k8s:
          resources:
            requests:
              cpu: 10m
              memory: 40Mi
      - enabled: true
        name: istio-egress-gateway
        k8s:
          resources:
            requests:
              cpu: 20m
              memory: 40Mi
            limits:
              cpu: 40m
              memory: 80Mi
    ingressGateways:
      - enabled: false
        name: istio-ingressgateway
        k8s:
          resources:
            requests:
              cpu: 10m
              memory: 40Mi
      - enabled: true
        name: istio-ingress-gateway
        k8s:
          resources:
            requests:
              cpu: 20m
              memory: 40Mi
            limits:
              cpu: 40m
              memory: 80Mi
          service:
            ports:
              - name: status-port
                port: 15021
                targetPort: 15021
              - name: http2
                port: 80
                targetPort: 80
              - name: https
                port: 443
                targetPort: 8443
              - name: tcp
                port: 31400
                targetPort: 31400
              - name: tls
                port: 15443
                targetPort: 15443
```

Validate the updated manifest:

```bash theme={null}
istioctl validate -f demo.yaml
"demo.yaml" is valid
```

Upgrade/reconcile the installation (confirm `y` when prompted):

```bash theme={null}
istioctl upgrade -f demo.yaml
This will install the Istio 1.26.3 profile "demo" into the cluster. Proceed? (y/N) y
✓ Istio core installed
✓ Istiod installed
Processing resources for Egress gateways, Ingress gateways. Waiting for Deployment/istio-system/istio-egress-gateway, Deployment/istio-system/istio-ingress-gateway...
```

During rollout you will often see both old and new pods (old terminating, new running):

```bash theme={null}
kubectl get pods -n istio-system
NAME                                       READY   STATUS        RESTARTS   AGE
istio-egress-gateway-7949ccd449-r6wcn     1/1     Running       0          24s
istio-egressgateway-fdbbf964c-j6dm7       0/1     Terminating   0          4m51s
istio-ingress-gateway-64bf9dfb-rn5jk      1/1     Running       0          24s
istio-ingressgateway-7f9cb54c46-lzfcv     0/1     Terminating   0          4m50s
istiod-6699bd67b-swz6j                    1/1     Running       0          4m55s
```

Verify resource overrides applied to the new ingress gateway:

```text theme={null}
Limits:
  cpu: 40m
  memory: 80Mi
Requests:
  cpu: 20m
  memory: 40Mi
```

***

<Frame>
  <img alt="The image shows a webpage from the Istio documentation, featuring sections on &#x22;ConfigMapKeySelector&#x22; and &#x22;ContainerResourceMetricSource&#x22; with corresponding tables detailing fields, types, and requirements. The page also includes a navigation menu on the right." />
</Frame>

***

## 4) Enable automatic sidecar injection for your namespace

Check current namespaces and labels:

```bash theme={null}
kubectl get ns --show-labels
NAME              STATUS    AGE    LABELS
default           Active    26m    kubernetes.io/metadata.name=default
istio-system      Active    11m    kubernetes.io/metadata.name=istio-system
kube-node-lease   Active    26m    kubernetes.io/metadata.name=kube-node-lease
kube-public       Active    26m    kubernetes.io/metadata.name=kube-public
kube-system       Active    26m    kubernetes.io/metadata.name=kube-system
```

Analyze the namespace (suggests enabling injection if not enabled):

```bash theme={null}
istioctl analyze -n default
Info [IST102] (Namespace default) This namespace is not enabled for Istio injection. Run 'kubectl label namespace default istio-injection=enabled' to enable it, or 'kubectl label namespace default istio-injection=disabled' to explicitly mark it as not needing injection.
```

Enable injection:

```bash theme={null}
kubectl label namespace default istio-injection=enabled
```

***

## 5) Redeploy Bookinfo so pods get sidecar-injected

Delete any existing Bookinfo resources, then re-apply the sample manifest so the pods are recreated with the Istio sidecar:

```bash theme={null}
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
