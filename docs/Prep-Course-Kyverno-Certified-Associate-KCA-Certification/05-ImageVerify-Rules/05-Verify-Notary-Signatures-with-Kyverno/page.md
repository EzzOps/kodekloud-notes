# Verify Notary Signatures with Kyverno

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/ImageVerify-Rules/Verify-Notary-Signatures-with-Kyverno/page

Explains configuring Kyverno verifyImages rules to validate Notary image signatures, resolve tags to digests, use attestors and caching for efficient cryptographic verification.

Earlier we covered why image signing matters and how to sign images using the [Notary CLI](https://github.com/theupdateframework/notary). In this lesson we automate signature verification using Kyverno's image verification capabilities.

Kyverno exposes a specialized rule block, `verifyImages`, for validating image signatures and attestations. Each verification statement includes a few important fields:

* `type` — the signature system (for example, [Notary](https://github.com/theupdateframework/notary) or [Cosign](https://docs.sigstore.dev/cosign/)).
* `imageReferences` — which images the rule should check (wildcards supported).
* `attestors` — the trusted signers (public keys, certificates, etc.).

Minimum example `verifyImages` rule:

```yaml theme={null}
spec:
  rules:
    - name: verify-my-image
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages: # The specialized rule block
        - type: Notary # or Cosign
          imageReferences:
            - "ghcr.io/my-org/my-app:*"
          attestors:
            count: 1
            entries:
              - certificates:
                  cert: |- # Dev Team Cert (PEM)
                    -----BEGIN CERTIFICATE-----
                    ...
                    -----END CERTIFICATE-----
```

The `imageReferences` list tells Kyverno which images to protect. In the example above we target all tags of `ghcr.io/my-org/my-app`.

The `attestors` block is the core of your trust policy — it declares which keys or certificates Kyverno accepts as valid signers.

<Frame>
  <img alt="The image shows a text box explaining that an attestor represents a trusted source, typically a public certificate for Notary. It is labeled &#x22;Configuring Attestors.&#x22;" />
</Frame>

You can list multiple trusted entries and control how many must validate using `count`. If `count` is omitted, Kyverno requires all listed entries to pass (logical AND). Setting `count: 1` requires at least one entry to pass (logical OR across entries).

```yaml theme={null}
verifyImages: # The specialized rule block
  - type: Notary
    imageReferences:
      - "ghcr.io/my-org/my-app:*"
    attestors:
      count: 1 # Require at least one of the entries to pass
      entries:
        - certificates:
            cert: |-
              -----BEGIN CERTIFICATE-----
              ...  # Dev Team Cert
              -----END CERTIFICATE-----
        - certificates:
            cert: |-
              -----BEGIN CERTIFICATE-----
              ...  # Security Team Cert
              -----END CERTIFICATE-----
```

Use `count` to support flexible trust models, for example accepting images signed by either a dev team key or a security team key.

<Callout icon="warning">
  If you omit `count`, Kyverno requires all listed attestors to validate (logical AND). This can be stricter than intended — explicitly set `count` to express OR semantics or multi-signer requirements.
</Callout>

Complete ClusterPolicy example

The policy below matches Pods, resolves image tags to immutable digests during admission mutation, and enforces Notary signature verification using a PEM certificate:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-signature-notary
spec:
  background: false
  rules:
    - name: verify-signature-notary
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - type: Notary
          imageReferences:
            - "ghcr.io/kyverno/test-verify-image:*"
          failureAction: Enforce
          attestors:
            count: 1
            entries:
              - certificates:
                  cert: |-
                    -----BEGIN CERTIFICATE-----
                    ...
                    -----END CERTIFICATE-----
```

The `cert` field holds the PEM-encoded public certificate that pairs with the private key used to sign the image. Kyverno uses this certificate to cryptographically verify signatures associated with the resolved image digest.

How verification works (two stages)

1. Mutation (tag → digest)
   When a Pod is submitted, the Kyverno admission webhook intercepts the request and scans container images. If an image tag matches `imageReferences`, Kyverno resolves that tag to the immutable digest stored in the registry. Kyverno mutates the Pod in-memory to replace the tag with that digest, effectively locking the exact image that will be pulled — preventing tag rebinding after verification.

<Frame>
  <img alt="The image depicts the verification workflow for mutation, broken down into five steps: &#x22;Admission Request,&#x22; &#x22;Kyverno Intercepts,&#x22; &#x22;Finds a Match,&#x22; &#x22;Resolves the Tag,&#x22; and &#x22;Mutates the Digest.&#x22; The result is the image reference being &#x22;locked in&#x22; to a specific version." />
</Frame>

2. Validation (fetch signature → cryptographic check)
   After mutation, Kyverno connects to the registry to fetch the Notary signature associated with the resolved digest. Using the certificate(s) in the policy `attestors`, Kyverno verifies the signature. Kyverno then confirms the Pod's image reference still uses the same digest. If all checks pass, admission is allowed.

<Frame>
  <img alt="The image illustrates a verification workflow, detailing connection and validation steps involving a registry and cryptographic checks using a policy's attestations." />
</Frame>

If verification fails at any step — for example, the signature is missing, invalid, or signed by an untrusted key — Kyverno denies the admission request and the Pod is not created.

<Frame>
  <img alt="The image shows a diagram of a verification workflow process involving final validation and checks for an image reference. It indicates that if the signature is missing or invalid, the request is denied; otherwise, the request is allowed." />
</Frame>

Performance and caching

Fetching signatures and performing cryptographic verification on every Pod admission can be expensive. Kyverno uses an image verification cache to improve performance; this cache is enabled by default.

How the cache helps:

* The first time a specific image digest is successfully verified for a given policy, Kyverno stores a positive result in an in-memory TTL cache.
* Subsequent Pods using the same image digest will hit the cache and be allowed immediately, avoiding a remote registry call and expensive crypto operations.

<Callout icon="lightbulb">
  The cache trades freshness for performance. The default TTL (60m) may allow a revoked signature to be accepted until the cache entry expires. Choose cache settings based on your operational risk tolerance.
</Callout>

<Frame>
  <img alt="The image describes performance and caching strategies, highlighting image verification caching by default and the benefits of using cached results for policy evaluation. It includes cache configuration details such as enabling cache, max size, and TTL duration." />
</Frame>

Admission Controller cache-related flags

| Flag                            | Default | Description                                    |
| ------------------------------- | ------- | ---------------------------------------------- |
| `--imageVerifyCacheEnabled`     | `true`  | Enable or disable the image verification cache |
| `--imageVerifyCacheMaxSize`     | `1000`  | Maximum number of cache entries                |
| `--imageVerifyCacheTTLDURATION` | `60m`   | Time-to-live for cache entries                 |

Summary

* `verifyImages` is Kyverno's mechanism for supply-chain image verification (Notary, Cosign, etc.).
* Define `type`, protected `imageReferences`, and trusted `attestors` to express your trust policy.
* Use `attestors.count` to control logical AND vs OR behavior across attestors.
* Verification is two-phase: mutation (resolve tag → digest) and validation (fetch signature → cryptographic verification).
* Kyverno uses an in-memory TTL cache to reduce verification overhead — tune cache settings to match your security posture.

<Frame>
  <img alt="The image shows a summary of key points about enforcing image trust using Kyverno, detailing specific rules, workflows, and performance considerations. It includes five main points, each highlighted with numbered icons." />
</Frame>

You are now ready to author Kyverno policies that verify Notary image signatures. In later sections we will cover verifying attestations and Cosign-based verification.

Links and references

* Kyverno verifyImages documentation: [https://kyverno.io/docs](https://kyverno.io/docs)
* Notary (The Update Framework): [https://github.com/theupdateframework/notary](https://github.com/theupdateframework/notary)
* Cosign: [https://docs.sigstore.dev/cosign/](https://docs.sigstore.dev/cosign/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/29b815f2-6996-4693-b4b5-993ad2c6659e/lesson/72fe9077-7c56-40be-9863-379150e924da" />
</CardGroup>
