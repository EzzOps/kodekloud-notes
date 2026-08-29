# Demo Issue A Tls Cert With Cert Manager

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Consuming-Popular-Operators/Demo-Issue-A-Tls-Cert-With-Cert-Manager/page

Guide to installing cert-manager on Kubernetes and using Issuer and Certificate resources to automate TLS certificate issuance, secret creation, and renewal

Manual TLS certificate handling does not scale: someone must create the certificate object, store it in a Secret, track expiry, and rotate it before traffic breaks. cert-manager models this workflow as Kubernetes resources and runs a controller to reconcile them: you create custom resources (Issuer, Certificate) and the operator performs key generation, signing, Secret creation, and renewal.

This guide shows how to:

* Install cert-manager from a release manifest
* Create a self-signed Issuer
* Request a Certificate resource
* Verify cert-manager created the TLS Secret

Prerequisite: ensure your cluster can access the cert-manager release manifest URL and that `kubectl` is configured to talk to the target cluster.

## 1) Verify the cert-manager manifest URL

Confirm the release manifest URL is set in your environment:

```bash theme={null}
$ printenv CERT_MANAGER_MANIFEST_URL
https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml
```

## 2) Install cert-manager

Apply the approved cert-manager release manifest. The manifest installs the CRDs for cert-manager (Certificate, Issuer, etc.) and deploys the cert-manager controller, webhook, and CA injector into the `cert-manager` namespace.

```bash theme={null}
$ kubectl apply -f "$CERT_MANAGER_MANIFEST_URL"
namespace/cert-manager created
customresourcedefinition.apiextensions.k8s.io/challenges.acme.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/orders.acme.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/certificaterequests.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/certificates.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/clusterissuers.cert-manager.io created
```

<Callout icon="warning">
  Wait for cert-manager deployments to become available before creating Issuer or Certificate resources. The API server contacts the cert-manager webhook on resource creation; if the webhook is not ready, the API server may reject valid objects.
</Callout>

Wait for the cert-manager deployments (controller, webhook, cainjector) to be ready:

```bash theme={null}
$ kubectl -n cert-manager wait --for=condition=Available \
  deploy/cert-manager deploy/cert-manager-webhook deploy/cert-manager-cainjector --timeout=240s
deployment.apps/cert-manager condition met
deployment.apps/cert-manager-webhook condition met
deployment.apps/cert-manager-cainjector condition met
```

## 3) Create a self-signed Issuer

An Issuer is a namespaced resource that defines how certificates are signed. For demos or local testing, a self-signed Issuer is convenient because it does not require an external CA.

issuer.yaml:

```yaml theme={null}
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned
spec:
  selfSigned: {}
```

Apply the Issuer and wait for it to become Ready:

```bash theme={null}
$ kubectl apply -f issuer.yaml
issuer.cert-manager.io/selfsigned created

$ kubectl wait --for=condition=Ready issuer/selfsigned --timeout=120s
issuer.cert-manager.io/selfsigned condition met

$ kubectl get issuer selfsigned
NAME         READY   AGE
selfsigned   True    25s
```

<Callout icon="lightbulb">
  Use a `ClusterIssuer` when you want an issuer available cluster-wide. For simple demos and per-namespace control, a namespaced `Issuer` is preferable.
</Callout>

## 4) Request a Certificate

Create a Certificate resource which tells cert-manager:

* the Secret name to write
* the DNS names the certificate should cover
* which Issuer to use to sign the certificate

certificate.yaml:

```yaml theme={null}
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: webapp-tls
spec:
  secretName: webapp-tls-cert
  dnsNames:
    - apps.kodekloud.com
  issuerRef:
    name: selfsigned
    kind: Issuer
```

Apply the Certificate and wait for it to be ready:

```bash theme={null}
$ kubectl apply -f certificate.yaml
Warning: spec.privateKey.rotationPolicy: In cert-manager >= v1.18.0, the default value changed from `Never` to `Always`.
certificate.cert-manager.io/webapp-tls created

$ kubectl wait --for=condition=Ready certificate/webapp-tls --timeout=120s
certificate.cert-manager.io/webapp-tls condition met
```

Check the Certificate resource to see the Secret name, readiness, and age:

```bash theme={null}
$ kubectl get certificate webapp-tls -o wide
NAME        READY   SECRET            AGE
webapp-tls  True    webapp-tls-cert   29s
```

## 5) Inspect the TLS Secret

cert-manager writes the signed certificate and key into a Kubernetes Secret of type `kubernetes.io/tls`. The Secret usually contains these keys: `tls.crt`, `tls.key`, and often `ca.crt`.

```bash theme={null}
$ kubectl get secret webapp-tls-cert
NAME                TYPE                DATA   AGE
webapp-tls-cert     kubernetes.io/tls   3      41s
```

You can view a specific key (base64-decoded) or mount this Secret into an Ingress, Pod, or any Kubernetes resource that accepts TLS credentials:

```bash theme={null}
