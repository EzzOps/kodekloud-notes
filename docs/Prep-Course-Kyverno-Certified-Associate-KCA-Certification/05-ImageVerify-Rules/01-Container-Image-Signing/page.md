# Container Image Signing

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/ImageVerify-Rules/Container-Image-Signing/page

Explains why container image tags are insecure and how cryptographic signing and Kyverno verification with tools like Cosign enforce image authenticity and integrity

Alex's critical challenge is ensuring a container image is authentic and untampered. Before writing [Kyverno](https://kyverno.io/) policies, it's essential to understand why image signing matters and which open-source tools Kyverno integrates with to enforce signature-based policies.

## Why we can't trust an image tag for security

A tag such as `latest` is a human-friendly label — not a permanent identifier. Because tags are mutable, relying on them introduces three major risks:

* Simple mistakes: a developer may accidentally reference a similarly named public image instead of your internal image.
* Malicious fakes: an attacker can publish a malicious image using the same name and tag as a popular image to trick users.
* Moving tags: an operator, CI system, or malicious actor can push a different image and update the tag to point to it. Your Kubernetes manifest may remain unchanged while the image pulled later is completely different.

## Digest vs. tag

Every container image has two identifiers:

* Digest: the image’s permanent fingerprint (for example, `sha256:...`). It’s a hash computed from the image content and is immutable—changing any byte changes the digest.
* Tag: a friendly name such as `my-app:latest`. It’s a mutable pointer in the registry that maps to a digest.

A tag is just a pointer that can be updated. To uniquely identify an image, reference it by digest:

* `my-app@sha256:<digest>`

Comparison:

| Identifier |                                             Purpose | Example                |
| ---------- | --------------------------------------------------: | ---------------------- |
| Digest     | Immutable image identity; exact content fingerprint | `my-app@sha256:ABC...` |
| Tag        |                Human-readable pointer that can move | `my-app:latest`        |

## How tag movement creates risk (step-by-step)

1. Your trusted CI builds a good image and pushes `my-app:latest`. The registry points `latest` to the good digest `sha256:ABC...`.
2. Later, an attacker or broken process pushes a different image with digest `sha256:XYZ...` using the same tag `my-app:latest`.
3. The registry updates the `latest` pointer to `sha256:XYZ...`. Your Kubernetes manifest still references `my-app:latest`; when the cluster schedules a new Pod it may pull the malicious image.

<Frame>
  <img alt="The image illustrates the process of moving a tag's pointer in a container registry, showing how a good image is initially tagged, followed by a bad image being pushed with the same tag, leading to an update of the tag's pointer." />
</Frame>

This demonstrates why tags alone cannot provide security guarantees.

## The solution: cryptographic signatures

Cryptographic signatures bind a signer to an image digest and provide two guarantees:

* Authenticity: who created (or signed) the image. A valid signature proves the image was signed by an entity that controls a trusted private key (for example, your CI/CD pipeline).
* Integrity: whether the image has been altered. The signature is associated with the image’s immutable digest; if the image is modified, the digest changes and signature verification fails.

<Frame>
  <img alt="The image explains cryptographic proof, focusing on authenticity (&#x22;who created it?&#x22;) and integrity (&#x22;has it been changed?&#x22;). It describes how signatures verify an image's origin and ensure it hasn't been altered." />
</Frame>

## End-to-end signing and verification flow

A typical signing and verification flow:

1. The CI/CD pipeline (the signer) builds the image and uses a tool — for example, [Sigstore Cosign](https://github.com/sigstore/cosign) — with a private key (or keyless attestation) to sign the image.
2. The pipeline pushes the image and its signature (or attestation) to the container registry.
3. A developer submits a Kubernetes manifest that references the image to the cluster.
4. Kyverno, acting as the verifier via an admission webhook, intercepts the admission request and checks the configured image verification rules.
5. Kyverno fetches the signature from the registry and verifies it using the configured trust material (public keys or trust roots). If verification succeeds and the signer is trusted, the admission is allowed; otherwise it is denied.

<Frame>
  <img alt="The image explains a CI/CD pipeline process that involves building an image, using a tool like Cosign with a private key to generate a signature, and pushing both the image and its signature to a container registry." />
</Frame>

## Kyverno's role — verifier, not signer

Kyverno does not generate signatures. Its responsibility is to verify signatures and enforce policies at admission time. Kyverno integrates with tools like [Sigstore Cosign](https://github.com/sigstore/cosign) and [Notary](https://github.com/theupdateframework/notary) by fetching signatures/attestations from the registry and validating them against configured trust material (public keys or trust roots).

> **lightbulb** Kyverno verifies image signatures during admission using configured trust sources. Signing is typically done by your CI/CD pipeline or a dedicated signing process.

<Frame>
  <img alt="The image outlines the process Kyverno uses to verify signatures: intercepting the request, connecting to a container registry, using a public key for validation, and deciding whether to allow or deny pod creation." />
</Frame>

## Quick example: signing and verification commands

Below are concise examples showing how to sign an image with Cosign and how Kyverno/your pipeline can verify it. Replace placeholders with your actual values (`<registry>`, `<repo>`, `<TAG>`, `<PATH-TO-KEY>`, etc.).

Sign an image using a local key:

```bash theme={null}
cosign sign --key /path/to/cosign.key `<registry>/<repo>:<TAG>`
```

Verify the signature using the public key:

```bash theme={null}
cosign verify --key /path/to/cosign.pub `<registry>/<repo>:<TAG>`
```

Sign and reference by digest (recommended for immutable deployments):

1. Push the image and capture its digest (example output shows the digest):

```bash theme={null}
docker push `<registry>/<repo>:<TAG>`
