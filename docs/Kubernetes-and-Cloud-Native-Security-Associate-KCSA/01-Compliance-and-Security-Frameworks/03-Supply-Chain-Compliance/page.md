# Supply Chain Compliance

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Compliance-and-Security-Frameworks/Supply-Chain-Compliance/page

This guide covers supply chain security in Kubernetes, focusing on artifacts, metadata, attestations, and policies for compliance and integrity.

Supply chain security extends beyond internal threat modeling—it ensures every external dependency (libraries, container images, third-party APIs) is verified, tamper-free, and compliant. In this guide, we’ll cover the four core areas of supply chain security, show you practical commands, and point to best-in-class tools and standards.

## Core Areas of Supply Chain Security

| Core Area    | Description                       | Tool / Standard            |
| ------------ | --------------------------------- | -------------------------- |
| Artifacts    | Build outputs: images, binaries   | Sigstore Cosign            |
| Metadata     | Software Bill of Materials (SBOM) | SPDX                       |
| Attestations | Signed provenance statements      | in-toto                    |
| Policies     | Automated compliance enforcement  | Sigstore Policy Controller |

## 1. Artifacts: Signing and Verification

Artifacts—your container images, binaries, and libraries—must be signed to prove integrity and origin.

> **lightbulb** Sigstore’s [Cosign](https://docs.sigstore.dev/cosign/) offers a simple, keyless workflow for signing container images.

To sign an image:

```bash theme={null}
cosign sign $IMAGE
```

Sample output:

```text theme={null}
Generating ephemeral keys...
Retrieving signed certificate...
By typing 'y', you attest that you have permission to grant signing.
Are you sure you would like to continue? [y/N] y
Successfully verified SCT...
tlog entry created with index: 12086900
Pushing signature to: $IMAGE
```

To verify a binary or image:

```bash theme={null}
cosign verify-blob "$BINARY" \
  --signature "$BINARY.sig" \
  --certificate "$BINARY.cert" \
  --certificate-identity krel-staging@k8s-releng-prod.iam.gserviceaccount.com \
  --certificate-oidc-issuer https://accounts.google.com
```

## 2. Metadata: Generating and Validating SBOMs

A Software Bill of Materials (SBOM) is an “ingredients list” for your application, detailing file checksums, licenses, and origins.

> **lightbulb** An SBOM (Software Bill of Materials) is often authored in [SPDX](https://spdx.org/) format. It tracks every component and its license.

Example SPDX excerpt:

```spdx theme={null}
FileName: bin/linux/amd64/kube-controller-manager
SPDXID: SPDXRef-File-kube-controller-manager-v1.31.2
FileChecksum: SHA1: c5e8da214abd18e96aabe7d1bab6addf76455
FileChecksum: SHA256: b16b6becee2bc76af97384ca611d8e972aa7ed213ea75255
LicenseConcluded: Apache-2.0
```

Retrieve and verify the Kubernetes SBOM:

```bash theme={null}
