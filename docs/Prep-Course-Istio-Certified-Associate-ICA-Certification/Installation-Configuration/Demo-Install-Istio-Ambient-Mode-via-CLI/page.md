# then re-apply
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
```

During startup you will observe pods initializing and the init container running for proxy injection (READY changes from 0/2 to 2/2 once injection completes):

```bash theme={null}
kubectl get pods
NAME                                   READY   STATUS        RESTARTS   AGE
details-v1-65599dcf88-gt4m2           0/2     Init:0/1     0          2s
productpage-v1-9487c9c5b-214vf        0/2     Init:0/1     0          2s
ratings-v1-59b99c644-h82fc            0/2     Init:0/1     0          2s
reviews-v1-5985995844-t87r1           1/2     Running      0          2s
reviews-v2-86d6cc668-pnr4b            1/2     Running      0          2s
```

Eventually pods should reach `2/2 READY`:

```bash theme={null}
kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
details-v1-65599dcf88-gt4m2           2/2     Running   0          30s
productpage-v1-9487c9c5b-214vf        2/2     Running   0          30s
ratings-v1-59b99c644-h82fc            2/2     Running   0          30s
reviews-v1-5985995844-t87r1           2/2     Running   0          30s
reviews-v2-86d6cc668-pnr4b            2/2     Running   0          30s
```

***

## Notes on `istioctl profile` and operator fields

Recent `istioctl` releases removed the `profile` subcommand. If you run `istioctl profile` you may see:

```bash theme={null}
istioctl profile
Error: unknown command "profile" for "istioctl"
Run "istioctl --help" for usage.
```

Use the Operator API and the Istio documentation to find profile defaults, available fields, and examples. The operator supports configuration for: profiles, image hub/tag, revisions, components, meshConfig, and more.

***

## Quick reference: common commands

| Task                                  | Command                                                                                                                    |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Validate operator manifest            | `istioctl validate -f demo.yaml`                                                                                           |
| Install/upgrade Istio via Operator    | `istioctl install -f demo.yaml -y` or `istioctl upgrade -f demo.yaml`                                                      |
| Analyze namespace for Istio issues    | `istioctl analyze -n <namespace>`                                                                                          |
| Label namespace for sidecar injection | `kubectl label namespace <ns> istio-injection=enabled`                                                                     |
| (Re)deploy Bookinfo sample            | `kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml` |

***

## Links and references

* Istio operator API and examples: [https://istio.io/latest/docs/setup/install/operator/](https://istio.io/latest/docs/setup/install/operator/)
* Bookinfo sample (used above): [https://github.com/istio/istio/tree/release-1.11/samples/bookinfo](https://github.com/istio/istio/tree/release-1.11/samples/bookinfo)
* Istio documentation (profiles, configuration, operator): [https://istio.io/docs/](https://istio.io/docs/)

That completes this demo on customizing Istio installations using the Istio Operator (IstioOperator CR).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/68d83bec-a2d9-4373-9027-b7df4f3fb748" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/2714c649-e381-44a3-8c51-2e34408d6ab9" />
</CardGroup>


# Demo Install Istio Ambient Mode via CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Demo-Install-Istio-Ambient-Mode-via-CLI/page

Guide to install and verify Istio Ambient Mode using istioctl, configure namespaces and ztunnel and istio-cni L4 interception, and optionally deploy waypoint proxies for L7 via Gateway API

This guide walks through installing Istio in ambient mode using the CLI, verifying dataplane behavior (ztunnel and CNI), labeling namespaces for ambient dataplane mode, running a test pod to confirm layer‑4 interception, and optionally deploying a waypoint proxy for layer‑7 features.

<Callout icon="lightbulb">
  Ambient mode removes the sidecar proxy from workloads and uses a host‑level daemon (ztunnel) plus the Istio CNI for transparent L4 interception. Use waypoint proxies when you need layer‑7 features (HTTP routing, mirroring, fault injection).
</Callout>

## 1 — Download Istio and add istioctl to PATH

Download the desired Istio version (example uses 1.26.3) and add the `bin` folder to your PATH:

```bash theme={null}
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.26.3 sh -
export PATH=$PWD/bin:$PATH
```

Verify the client version (before install the cluster will not show control plane pods):

```bash theme={null}
istioctl version
