# Set a variable for the immutable image digest
IMAGE=localhost:5001/net-monitor@sha256:073b7598...555a

# List existing signatures (should be empty for a new image)
notation ls $IMAGE
```

If nothing is returned, the image is unsigned and ready for signing.

## Generate test keys and certificate (development/demo)

Notation can generate a test RSA key and a self-signed certificate for demonstrations:

```bash theme={null}
notation cert generate-test --default "wabbit-networks.io"
```

This command:

* Creates an RSA private key.
* Generates a self-signed certificate (CN=wabbit-networks.io).
* Sets the new key as Notation's default signing key.
* Adds the public certificate to a local trust store used by Notation.

<Frame>
  <img alt="The image illustrates the process of signing an image using a private key and verifying it with a public certificate, as part of generating a private key and certificate." />
</Frame>

> **warning** The `generate-test` command is intended for development and demos only. In production, provision signing keys and certificates securely (for example, using an internal CA, hardware-backed keys, or a cloud KMS). Restrict access and audit usage.

## Sign the image

Notation signs the image manifest (the immutable digest) with the configured private key and pushes a signature artifact to the registry.

<Frame>
  <img alt="The image illustrates &#x22;Step 3: The Signing Operation,&#x22; highlighting the core action in a signing process, with a note about using a private key to sign an image digest and pushing the signature to the registry." />
</Frame>

Run the sign command (uses the default key you configured with `generate-test`):

```bash theme={null}
notation sign $IMAGE
```

What happens under the hood:

* Notation fetches the image manifest from the registry.
* It computes a digital signature over the manifest’s digest using the private key.
* It pushes the signature artifact (Notary v2 media type) to the registry and associates it with the image digest.

## Confirm and inspect the signature

After signing, list the artifacts to confirm a Notation signature exists and inspect the signature metadata.

```bash theme={null}
# List Notation signature artifacts for the image
notation ls $IMAGE
```

Example output:

```bash theme={null}
$ notation ls $IMAGE
localhost:5001/net-monitor@sha256:073b...
└── application/vnd.cncf.notary.v2.signature
    └── sha256:ba3a68a28648ba18c51a4791...
```

Inspect the signature contents (the evidence a verifier would evaluate):

```bash theme={null}
notation inspect $IMAGE
```

Typical inspection output (summary):

```bash theme={null}
signature algorithm: RSASSA-PSS-SHA-256
certificates
 └── issued to: CN=wabbit-networks.io
signed artifact
 └── digest: sha256:073b7598...
```

This output shows:

* The signature algorithm.
* The certificate used to sign (subject CN).
* The image digest covered by the signature — the cryptographic link that guarantees integrity.

<Frame>
  <img alt="The image shows a step in a process titled &#x22;Step 4: Inspecting the Result,&#x22; with the task &#x22;1. Confirm the Signature Exists.&#x22;" />
</Frame>

## Verify the signature

Notation can perform verification locally; Kyverno automates this verification inside the cluster using trusted certificates configured in its policy.

Verification steps (what a verifier does):

1. Fetch the image and the signature artifact from the registry.
2. Locate a trusted public certificate that can validate the signature.
3. Perform the cryptographic verification: ensure the signature is valid for the image digest.

Run local verification:

```bash theme={null}
notation verify $IMAGE
```

If verification succeeds, the signature was created by the private key for a certificate present in the trust store, and the digest matches the signed artifact — providing cryptographic proof of authenticity and integrity.

## Commands and purpose

| Command                                        | Purpose                                                                                              | Example                                                      |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `notation ls <image>`                          | List signature artifacts attached to an image digest                                                 | `notation ls $IMAGE`                                         |
| `notation cert generate-test --default "<CN>"` | Create a demo key/cert and set default signing key (development only)                                | `notation cert generate-test --default "wabbit-networks.io"` |
| `notation sign <image>`                        | Sign an image digest with the configured private key and push the signature artifact to the registry | `notation sign $IMAGE`                                       |
| `notation inspect <image>`                     | Show signature metadata (algorithm, cert info, signed digest)                                        | `notation inspect $IMAGE`                                    |
| `notation verify <image>`                      | Verify a signature using certificates in the configured trust store                                  | `notation verify $IMAGE`                                     |

## Summary — Signing workflow

1. Preparation — Obtain or generate signing key material and the public certificate (trust material).
2. Action — Run `notation sign` to sign the image digest and push the signature to the registry.
3. Result — The registry stores the Notation signature artifact associated with the image digest; use `notation ls` and `notation inspect` to examine it.
4. Verification — A verifier (for example, Kyverno inside the cluster) validates the signature against configured trusted certificates (`notation verify` demonstrates this manually).

<Frame>
  <img alt="The image is a summary diagram outlining four steps for a signing process: Preparation, Action, Result, and Verification, along with brief descriptions for each step." />
</Frame>

## Links and references

* Notation (Notary v2): [https://notaryproject.dev/notation/](https://notaryproject.dev/notation/)
* Kyverno: [https://kyverno.io/](https://kyverno.io/)
* Notation documentation: [https://github.com/notaryproject/notation](https://github.com/notaryproject/notation)

You now have a practical, step-by-step understanding of image signing with Notation and how a verifier validates those signatures. Translate this process into Kyverno image verification policies to automate verification inside your Kubernetes cluster.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/29b815f2-6996-4693-b4b5-993ad2c6659e/lesson/3e0e3f32-3b02-4cf0-a6f6-5615c852ea3c)


# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/ImageVerify-Rules/Section-Introduction/page

Guide to Kyverno image verification using Sigstore cosign and Notary to cryptographically validate container image signatures and attestations so clusters run only trusted build artifacts.

So far, we've become proficient at writing Kyverno policies: validating, mutating, and generating Kubernetes resources. However, a critical piece of the supply chain remains unaddressed—the software artifacts themselves.

How can you trust the container image a pod is configured to run?

This guide explores one of Kyverno's most powerful security capabilities: container image verification. It shows how to cryptographically ensure that only images produced and signed by your trusted build system can run in your cluster.

Let's return to Alex's story. Alex has secured deployment manifests and set up a robust CI/CD pipeline that builds, tests,

<Frame>
  <img alt="The image presents a flowchart addressing &#x22;Alex's New Challenge,&#x22; depicting a process involving Alex's organization, a secure CI/CD pipeline, and trusted container images." />
</Frame>

and pushes official application images. Now Alex is focused on the software supply chain.

A simple manifest typo can cause a pod to pull an image from Docker Hub instead of the private registry. Image tags are mutable—tags like `latest` are just pointers. What prevents an attacker from pushing a malicious image using the same tag? Or a broken build from overwriting a stable tag?

Validate policies can inspect the image name in a manifest, but they cannot prove the image’s identity or integrity. Alex needs to answer a crucial question:

<Frame>
  <img alt="The image presents a challenge faced by someone named Alex about cryptographically proving an image's authenticity and integrity in a CI pipeline. It includes a quote outlining the dilemma." />
</Frame>

How can I be certain that the image about to run in my cluster was actually signed by my trusted build system and hasn't been altered since?

Image signature verification solves this problem by enabling admission-time checks that confirm both the identity and integrity of container images.

> **lightbulb** Learn how to cryptographically verify container images so your cluster only runs artifacts produced (and signed) by your trusted build pipeline.

What this guide covers

* Fundamentals: What container image signing means and why it matters. We introduce two widely adopted solutions Kyverno integrates with—[SIGSTORE](https://sigstore.dev) (and its CLI tool, [cosign](https://github.com/sigstore/cosign)) and [Notary](https://notaryproject.dev)—and explain core concepts like public keys, certificates, and attestations.
* Practical verification: How to solve Alex’s problem by writing Kyverno verifyImages policies for cosign and Notary. Learn how to configure policies that reference public keys and certificates so only images signed by your trusted authority are allowed to run.
* Attestations: How to validate claims about images (for example, provenance, vulnerability scan results, or SBOMs). We show examples of policies that verify attestations produced by cosign and Notary.

Key topics at a glance

| Topic                 |                                                           What you’ll learn | Example / Tool                                           |
| --------------------- | --------------------------------------------------------------------------: | -------------------------------------------------------- |
| Signing basics        |                Why image signing matters and how signatures prove integrity | [SIGSTORE / cosign](https://sigstore.dev)                |
| Verification policies | How to author Kyverno `verifyImages` policies that enforce signature checks | Kyverno verifyImages + public key/certificate references |
| Attestations          | How to validate claims (SBOMs, scan results, provenance) attached to images | cosign attestations, Notary attestations                 |

With these capabilities, you can enforce cryptographic provenance checks during admission control so your cluster only accepts images that meet your supply-chain policies.

Links and references

* [SIGSTORE — official site](https://sigstore.dev)
* [cosign — GitHub](https://github.com/sigstore/cosign)
* [Notary — official site](https://notaryproject.dev)
* [Kyverno documentation — policies and verifyImages](https://kyverno.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/29b815f2-6996-4693-b4b5-993ad2c6659e/lesson/1087e7b8-8d52-496d-b20c-331458c3e714)
