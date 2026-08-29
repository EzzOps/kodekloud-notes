# registry returns digest: sha256:ABC...
```

2. Use the digest in manifests to lock deployments:

```yaml theme={null}
image: `<registry>/<repo>@sha256:ABC...`
```

Example Kubernetes container spec snippet:

```YAML theme={null}
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: my-app
    image: `<registry>/<repo>@sha256:ABC...`
```

## Warning about protecting signing keys

> **warning** Private signing keys must be stored and rotated securely. If an attacker obtains a private key they can sign malicious images that will pass verification. Use hardware-backed keys, secure secret management, or Sigstore keyless workflows where appropriate.

## Summary

* Image tags (for example, `latest`) are movable pointers and cannot be trusted as a security boundary.
* The immutable image digest (for example, `sha256:...`) is the true identity of an image.
* Cryptographic signing provides authenticity and integrity by binding a signer to an image digest.
* Kyverno acts as a verifier, integrating with tools like [Sigstore Cosign](https://github.com/sigstore/cosign) and [Notary](https://github.com/theupdateframework/notary) to enforce image-signature policies at admission.

<Frame>
  <img alt="The image is a summary of steps for ensuring image integrity, highlighting the problem with image tags, the solution of using cryptographic signatures, Kyverno's role in verification, and the signing process involving private and public keys." />
</Frame>

## Next steps

We will now put this theory into practice and walk through the actual commands and Kyverno policy examples used to sign images in CI/CD and enforce verification at admission.

## Links and References

* [Kyverno](https://kyverno.io/) — Kyverno documentation and image verification features
* [Sigstore Cosign](https://github.com/sigstore/cosign) — Image signing and verification tool
* [Notary (The Update Framework)](https://github.com/theupdateframework/notary) — Trusted signing framework
* [Kubernetes Documentation](https://kubernetes.io/docs/) — Kubernetes resources and admission controllers

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/29b815f2-6996-4693-b4b5-993ad2c6659e/lesson/3adc55ba-928a-465e-95df-d8ead92857b0)


# Image Signature using Notary

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/ImageVerify-Rules/Image-Signature-using-Notary/page

Guide to signing container images with Notation, inspecting Notary v2 signatures, and verifying integrity using image digests and trust stores, with notes on demo keys and Kyverno verification policies

In the previous lesson we covered why signing container images matters. This article walks through the practical steps to sign a container image using Notation, inspect the resulting signature artifact, and verify the signature (locally and conceptually how a verifier like Kyverno checks it). The workflow emphasizes operating on an image's immutable content-addressable digest so the signature binds to the exact image content.

> **lightbulb** Always sign and verify an image by its immutable digest (for example, `registry.example.com/app@sha256:...`) rather than a mutable tag. This ensures the signature cryptographically covers the exact image bytes.

## Quick checklist

* Use the image digest (not a tag) when signing and verifying.
* Provision keys/certificates securely in production (see warning below).
* Notation stores signatures in the registry as Notary v2 signature artifacts associated with the image digest.

## Set the image variable and check for existing signatures

Start by pointing to the image’s immutable digest and list any existing signatures. For a freshly built image, `notation ls` should return nothing.

```bash theme={null}
