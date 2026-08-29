# Only default namespace
root@cilium# hubble observe --namespace default

# From the admin pod
root@cilium# hubble observe --namespace default --from-pod admin

# Last 30 minutes
root@cilium# hubble observe --since 30m

# Follow live updates
root@cilium# hubble observe --follow

# JSON output
root@cilium# hubble observe -o json | jq .
[
  {
    "time": "2024-08-01T00:49:41.474560859Z",
    "source": {
      "pod": "admin",
      "namespace": "default"
    },
    "destination": {
      "pod": "demo-deployment-7ccd685fcc-6grkd",
      "namespace": "default",
      "port": 80
    },
    "Type": "L3_L4",
    "Summary": "TCP SYN"
  }
]
```

## Conclusion

Cilium Hubble delivers powerful network observability through both a rich UI and command-line interface. Integrate Hubble with Prometheus and Grafana for long-term monitoring or use the `hubble` CLI for on-the-fly troubleshooting.

## Links and References

* [Cilium Documentation](https://docs.cilium.io/)
* [Hubble Getting Started](https://docs.cilium.io/en/stable/gettingstarted/hubble/)
* [Prometheus Official Site](https://prometheus.io)
* [Grafana Labs](https://grafana.com)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5a70ab6c-2094-4bf2-9f49-e441919fc8c2/lesson/6736c481-fea1-4607-acb6-c8ab2618ce98)


# Demo Cilium Network Policies

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Network-Security/Demo-Cilium-Network-Policies/page

This tutorial secures a sample application using Cilium Network Policies, progressing from Kubernetes NetworkPolicy to advanced L7 HTTP policies with access control.

In this tutorial, we’ll secure a sample application using Cilium Network Policies. We’ll progress from a default Kubernetes NetworkPolicy (Layer 3) to a full L7 HTTP policy with header-based access control.

Table of Contents

1. [Demo App Overview](#demo-app-overview)
2. [Default Kubernetes NetworkPolicy](#1-default-kubernetes-networkpolicy)
3. [Cilium Layer 3 Policy](#2-cilium-layer-3-policy)
4. [Cilium Layer 4 Policy](#3-cilium-layer-4-policy)
5. [Cilium Layer 7 HTTP Policy](#4-cilium-layer-7-http-policy)
6. [Adding an API Key Header](#5-adding-an-api-key-header)
7. [Further Reading](#further-reading)

***

## Demo App Overview

Our demo application runs as a single Pod with two containers listening on ports **5000** and **80**. It exposes two corresponding ClusterIP Services.

```bash theme={null}
kubectl get all
```

```text theme={null}
NAME                                  READY   STATUS    RESTARTS   AGE
pod/demo-deployment-7ccd685fcc-7z9wf  2/2     Running   0          5m

NAME                   TYPE        CLUSTER-IP       PORT(S)    AGE
service/app-svc-5000   ClusterIP   10.111.51.97     5000/TCP   5m
service/app-svc-80     ClusterIP   10.102.122.72     80/TCP    5m
service/kubernetes     ClusterIP   10.96.0.1         443/TCP  10m
```

Both containers serve the same Flask app. We'll lock down access so only Pods labeled `app=admin` can communicate.

***

## 1. Default Kubernetes NetworkPolicy

We begin with a basic Kubernetes NetworkPolicy named `demo-netpol`. It selects Pods labeled `app=demo` and allows ingress from Pods labeled `app=admin` on **all ports**.

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: demo-netpol
spec:
  podSelector:
    matchLabels:
      app: demo
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: admin
```

### Verifying the Default Policy

1. **Allowed**: Pod with `app=admin` can reach both ports.

   ```bash theme={null}
   kubectl run --rm -i --tty admin --image=curlimages/curl \
     --labels app=admin --restart=Never -- \
     curl --connect-timeout 2 app-svc-80
   # → Have a great day!

   kubectl run --rm -i --tty admin --image=curlimages/curl \
     --labels app=admin --restart=Never -- \
     curl --connect-timeout 2 app-svc-5000
   # → Have a great day!
   ```

2. **Denied**: Pod *without* the label is blocked.

   ```bash theme={null}
   kubectl run --rm -i --tty client --image=curlimages/curl \
     --restart=Never -- \
     curl --connect-timeout 2 app-svc-80
   # → curl: (28) Failed to connect...
   ```

> **lightbulb** Before applying Cilium policies, delete the existing Kubernetes NetworkPolicy so that Cilium’s default behavior (allow all) is restored.

```bash theme={null}
kubectl delete networkpolicy demo-netpol
```

***

## 2. Cilium Layer 3 Policy

Create `cilium-l3.yaml` to reimplement the same L3 selector using Cilium’s CRD:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: demo-cilium-l3
spec:
  endpointSelector:
    matchLabels:
      app: demo
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: admin
```

Apply and test:

```bash theme={null}
kubectl apply -f cilium-l3.yaml
