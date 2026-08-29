# Demo Destination Rules

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Destination-Rules/page

Guide demonstrating Istio DestinationRule usage to define subsets, configure traffic splitting with VirtualService, and manage load balancing, connection pools, outlier detection, and TLS modes.

DestinationRules in Istio enable advanced traffic management for services. They define subsets used for traffic splitting, configure load balancing and connection pools, enable circuit breaking and outlier detection, and set client TLS modes. In this guide we'll walk through a common workflow: deploying two versions of a HelloWorld service, defining subsets via a DestinationRule, and splitting traffic with a VirtualService.

## Prerequisites

Verify Istio sidecar injection is enabled for your namespace(s):

```bash theme={null}
kubectl get ns --show-labels
```

Example output:

```text theme={null}
NAME              STATUS   AGE   LABELS
default           Active   25m   istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   22m   kubernetes.io/metadata.name=istio-system
kube-node-lease   Active   25m   kubernetes.io/metadata.name=kube-node-lease
kube-public       Active   25m   kubernetes.io/metadata.name=kube-public
kube-system       Active   25m   kubernetes.io/metadata.name=kube-system
```

<Callout icon="lightbulb">
  Namespaces must be labeled for Istio sidecar injection (or the pods must have the sidecar injected) for VirtualService/DestinationRule routing to take effect across namespaces.
</Callout>

## Deploy the HelloWorld sample (v1 and v2)

Deploy two versions of a HelloWorld application (v1 and v2). Confirm the pods are running and each pod shows `2/2` (application container + Envoy sidecar):

```bash theme={null}
kubectl get pods --show-labels
```

Example output:

```text theme={null}
NAME                              READY   STATUS    RESTARTS   AGE     LABELS
helloworld-v1-7459d7b54b-wxfnj    2/2     Running   0          2m31s   app=helloworld,version=v1,...
helloworld-v2-654d97458-twmkh     2/2     Running   0          2m31s   app=helloworld,version=v2,...
```

Inspect the service and pod labels — DestinationRule subsets will match pod labels (for example `version: v1` and `version: v2`):

```bash theme={null}
kubectl get svc --show-labels
kubectl get pods --show-labels
```

Example abbreviated output:

```text theme={null}
