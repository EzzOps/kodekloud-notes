# Istio mTLS Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Istio-mTLS-Basics/page

This article explains how Istio's mutual TLS secures communication between microservices in Kubernetes.

In modern microservices architectures, securing traffic between pods is critical. Istio’s mutual TLS (mTLS) ensures that every call between services is both encrypted and authenticated.

## How Istio mTLS Works

Istio leverages a sidecar container pattern. Each application pod has an Envoy proxy injected beside it. When mTLS is enabled:

1. The client‐side Envoy obtains a certificate from Istio’s Citadel (the mesh CA).
2. It initiates a TLS handshake with the server‐side Envoy.
3. Both proxies verify each other’s certificates.
4. Once verified, traffic is encrypted in transit and then decrypted before reaching the application.

By default, Istio:

* Automatically detects injected workloads and negotiates mTLS.
* Leaves traffic to non-injected pods in plaintext.

<Callout icon="lightbulb">
  Make sure your pods are annotated or labeled for automatic sidecar injection. See [Istio Automatic Injection](https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/).
</Callout>

## Example Pod Topology

Consider three pods in your cluster:

* **Pod A** and **Pod B**: Part of the Istio mesh (sidecar injected). Traffic between them is encrypted with mTLS.
* **Pod C**: Not part of the mesh (no sidecar). Traffic between Pod B and Pod C is sent in plaintext over HTTP.

## Configuring PeerAuthentication

Istio uses the `PeerAuthentication` API to control mTLS behavior at namespace or workload level. A basic resource looks like this:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: PERMISSIVE
```

### PeerAuthentication Modes

| Mode       | Description                               | Behavior                                 |
| ---------- | ----------------------------------------- | ---------------------------------------- |
| PERMISSIVE | Allows both mTLS and plaintext            | mTLS inside mesh, plaintext from outside |
| STRICT     | Enforces mTLS for all inbound connections | Rejects any plaintext                    |
| DISABLE    | Disables mTLS entirely                    | All traffic is plaintext                 |

<Callout icon="triangle-alert">
  Switching from **PERMISSIVE** to **STRICT** may break clients that don’t support mTLS. Roll out changes carefully and monitor with [Kiali](https://istio.io/latest/docs/ops/visualization/kiali/).
</Callout>

#### 1. PERMISSIVE Mode

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: PERMISSIVE
```

#### 2. STRICT Mode

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  mtls:
    mode: STRICT
```

#### 3. DISABLE Mode

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  mtls:
    mode: DISABLE
```

## Next Steps

1. Apply each `PeerAuthentication` in a test namespace.
2. Use `kubectl logs` on Envoy sidecars to verify TLS handshakes.
3. Visualize service-to-service traffic in the [Kiali dashboard](https://istio.io/latest/docs/ops/visualization/kiali/).

## Links and References

* [Istio mTLS Migration Guide](https://istio.io/latest[AWS_SECRET_ACCESS_KEY]-migration/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Istio Security Concepts](https://istio.[SECRET_REDACTED]/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/468738c7-5bb9-42d8-91fd-c6aabf6c7bc2" />
</CardGroup>
