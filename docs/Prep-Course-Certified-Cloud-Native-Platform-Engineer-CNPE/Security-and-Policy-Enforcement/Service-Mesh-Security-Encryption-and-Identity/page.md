# Scan an image and print detected vulnerabilities
trivy image registry.company.com/app:v1.2

# Fail the pipeline on any CRITICAL or HIGH vulnerabilities
trivy image --exit-code 1 \
  --severity CRITICAL,HIGH \
  registry.company.com/app:v1.2
```

Trivy exit codes:

* 0: no vulnerabilities found at the specified severities (pipeline can continue)
* 1: matching vulnerabilities found (pipeline should fail)
* 2: scanner error or unexpected problem (treat as a failure and investigate)

<Callout icon="warning">
  Treat a scanner error (exit code 2) as a pipeline failure. Silent failures or degraded scanners can let vulnerable images slip through.
</Callout>

## Image signing with Cosign (Sigstore)

Signing artifacts proves provenance and integrity. Sigstore's Cosign is a broadly adopted tool for signing container images and storing signatures in a registry.

Why sign?

* Provenance: shows the artifact originated from your pipeline.
* Integrity: proves the artifact hasn't been altered since signing.
* Trust: restricts which identities/keys can create valid signatures.

Key-based signing example:

```bash theme={null}
# Generate a key pair (one-time)
cosign generate-key-pair

# Sign an image after it passes scanning
cosign sign --key cosign.key registry.company.com/app:v1.2

# Verify a signature using the public key
cosign verify --key cosign.pub registry.company.com/app:v1.2
```

Keyless signing

* Cosign also supports keyless signing using Sigstore Fulcio and Rekor with CI OIDC tokens, removing the need to manage long-lived private keys. Keyless is typically recommended for CI automation where secret key management is harder to secure.

## Complete automated flow

A typical automated flow in CI/CD:

1. Build the image with minimal base layers and reproducibility in mind.
2. Scan the image with Trivy; if disallowed severities are found, fail the pipeline.
3. Upon a clean scan, sign the image with Cosign (keyed or keyless).
4. Push the signed image and stored signatures/attestations to your registry.
5. Deploy—admission controls in the cluster verify signatures/attestations before allowing workloads.

Any failure at a gate prevents the artifact from reaching production.

<Frame>
  <img alt="The image illustrates the complete pipeline for image signing with Cosign, involving stages such as coding, building, scanning with Trivy, signing with Cosign, pushing to a registry, and deploying." />
</Frame>

## Admission control: verifying signatures with Kyverno

Enforce policy at runtime by validating image signatures and attestations. The Kyverno ClusterPolicy below rejects Pod creation for images from your registry unless they verify against the embedded public key.

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: Enforce
  background: false
  rules:
    - name: check-image-signature
      match:
        resources:
          kinds: ["Pod"]
      verifyImages:
        - imageReferences:
            - "registry.company.com/*"
          attestors:
            - entries:
                - keys:
                    - |
                      -----BEGIN PUBLIC KEY-----
                      ...
                      -----END PUBLIC KEY-----
```

If an image is unsigned or the signature does not verify against the provided public key(s), Pod creation is rejected—closing the loop: Trivy ensures images are clean, Cosign proves provenance, and Kyverno enforces acceptance at runtime.

<Callout icon="lightbulb">
  Use a secure key management strategy (or keyless signing) and automate signing only after a successful scan to prevent accidental acceptance of unverified images.
</Callout>

## SLSA and SBOM — what they are and why they matter

* SLSA (Supply-chain Levels for Software Artifacts) provides a maturity model for build integrity:
  * Level 1: documented builds and basic evidence
  * Level 4: hermetic, reproducible builds with tamper-proof review and enforced provenance
    SLSA helps you reason about how much assurance your pipeline provides.

* SBOM (Software Bill of Materials) lists components used in your software. When a CVE is disclosed, SBOMs help you quickly identify impacted services. Common SBOM formats include `SPDX` and `CycloneDX`. Tools such as `Syft` and `Trivy` can generate SBOMs for images and artifacts.

<Frame>
  <img alt="The image compares SLSA's supply-chain levels for software artifacts with SBOM's software bill of materials, highlighting key aspects and tools for each." />
</Frame>

## Quick reference and recommended commands

* Block images with unacceptable vulnerabilities:

```bash theme={null}
trivy image --exit-code 1 --severity CRITICAL,HIGH registry.company.com/app:v1.2
```

* Sign images with Cosign (key-based example):

```bash theme={null}
cosign generate-key-pair
cosign sign --key cosign.key registry.company.com/app:v1.2
cosign verify --key cosign.pub registry.company.com/app:v1.2
```

* Enforce signed images with Kyverno by verifying signatures at admission.

## Further reading and references

* Trivy: [https://github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)
* Cosign / Sigstore: [https://sigstore.dev/](https://sigstore.dev/)
* Kyverno: [https://kyverno.io/](https://kyverno.io/)
* SLSA: [https://slsa.dev/](https://slsa.dev/)
* SBOM formats: [https://spdx.dev/](https://spdx.dev/), [https://cyclonedx.org/](https://cyclonedx.org/)
* Syft (SBOM generation): [https://github.com/anchore/syft](https://github.com/anchore/syft)

## Wrap up

A secure delivery pipeline enforces the four gates—build, scan, sign, and admit—automatically. Implement these controls to move security left into CI/CD, reduce the risk of supply-chain compromises, and ensure only verified artifacts reach your cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/4fa48a7f-b1e6-4e09-bded-51f38be9355d" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/b53de961-c16f-40c3-bae8-75ab707cb814" />
</CardGroup>


# Service Mesh Security Encryption and Identity

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Service-Mesh-Security-Encryption-and-Identity/page

Explains Istio mTLS, SPIFFE identities, PeerAuthentication and AuthorizationPolicy to secure and control encrypted pod-to-pod traffic in Kubernetes service meshes

We have already secured who can access the cluster (RBAC), what configurations are allowed (Admission Control), and what pods can do at runtime (Pod Security Standards). The next layer is securing network traffic between workloads inside the cluster.

Mutual TLS (mTLS) encrypts all pod-to-pod communication and gives each workload a cryptographic identity. Without mTLS, traffic inside the cluster is plaintext and a compromised pod could sniff sensitive data or impersonate other services.

In this article we use Istio Service Mesh as an example to demonstrate:

* How mTLS works with sidecar proxies and SPIFFE identities.
* How to configure mTLS modes with `PeerAuthentication`.
* How to apply service-level access control using `AuthorizationPolicy` and SPIFFE identities.

<Frame>
  <img alt="The image lists learning objectives related to mTLS and Istio, including its importance, implementation with sidecar proxies and SPIFFE identities, PeerAuthentication for configuring modes, and AuthorizationPolicy for access control." />
</Frame>

## Why mTLS matters

Kubernetes networking is plaintext by default. That creates three main risks:

* A compromised pod can sniff node-local traffic — exposing API keys, credentials, and user data.
* There is no built-in service identity, so pods can impersonate one another.
* There is no native, easy way to enforce which services are allowed to call which.

mTLS addresses these problems by providing:

* Encryption: traffic is encrypted in transit.
* Identity: each workload receives a SPIFFE certificate that encodes its trust domain, namespace, and service account.
* Authentication: callers are verified before connections are established.

Learn more about SPIFFE: [https://spiffe.io/](https://spiffe.io/)

## How Istio implements mTLS

Istio’s control plane (Istiod) acts as a certificate authority. It issues short-lived X.509 certificates to each pod’s Envoy sidecar. Each certificate contains a SPIFFE URI identity such as:

spiffe://cluster.local/ns/frontend/sa/web-app

When pod A talks to pod B, the Envoy sidecars perform mutual TLS and validate each other’s certificates. Application code doesn’t need changes — apps continue to send plain HTTP. Encryption and identity verification happen at the sidecar layer.

<Frame>
  <img alt="The image illustrates how Istio mTLS works, showing the flow from Istiod issuing certificates, to the Envoy Sidecar (Source) encrypting and sending traffic, and the Envoy Sidecar (Destination) receiving, verifying, and forwarding the traffic." />
</Frame>

## Controlling mTLS with PeerAuthentication

Istio’s `PeerAuthentication` resource determines the mTLS mode for inbound traffic. The key field is `spec.mtls.mode`.

Common modes and recommended usage:

| Mode         | Description                                                                  | When to use                                                      |
| ------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `STRICT`     | Require mTLS for all inbound traffic. Connections failing mTLS are rejected. | Production (recommended once all services are meshed)            |
| `PERMISSIVE` | Accept both mTLS and plaintext.                                              | Safe migration stage — allows mixed workloads                    |
| `DISABLE`    | Turn off mTLS entirely for the scoped workloads.                             | Rarely recommended; use only for troubleshooting or legacy cases |

Example `PeerAuthentication` to enforce strict mTLS for the `payments` namespace:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: payments
spec:
  mtls:
    mode: STRICT
```

Scope rules for `PeerAuthentication`:

* A `PeerAuthentication` named `default` in `istio-system` typically sets a mesh-wide default.
* A `PeerAuthentication` named `default` in a namespace affects only that namespace.
* A `PeerAuthentication` with a `selector` applies only to matching workloads (labels).

If you want strict mTLS for a specific namespace, create a `PeerAuthentication` named `default` in that namespace with `mode: STRICT`.

<Frame>
  <img alt="The image is about configuring mTLS with PeerAuthentication in different scopes: mesh-wide, namespace, and workload levels. It details how each scope enforces the STRICT policy." />
</Frame>

## AuthorizationPolicy: service-level RBAC using SPIFFE identities

While `PeerAuthentication` ensures encryption and identity, Istio’s `AuthorizationPolicy` enforces access control based on those identities. Policies reference SPIFFE URIs from mTLS certificates inside the `principals` field.

Example: allow only the `web-app` service account in the `frontend` namespace to call the `payment-api` service, and permit only GET and POST to `/api/*`:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-api-only
  namespace: payments
spec:
  selector:
    matchLabels:
      app: payment-api
  rules:
  - from:
    - source:
        principals:
        - "spiffe://cluster.local/ns/frontend/sa/web-app"
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

Notes:

* The `principals` value is the SPIFFE URI that the Envoy sidecars present during mTLS.
* The default trust domain is often `cluster.local` in typical Istio installs; adjust if your cluster uses a different trust domain.

## Verifying mTLS and sidecar injection

Check that `PeerAuthentication` resources are present and inspect their modes:

```bash theme={null}
