# State Store Systems

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/State-Store-Systems/page

Explains using OCI registries as unified state stores for GitOps, hosting images, Helm charts, manifests, and policies with examples and best practices.

A State Store System is the canonical source for the desired state of your system: configurations, application manifests, and infrastructure definitions. In GitOps workflows this authoritative state is most commonly a Git repository because Git provides provenance, immutability, branching, and pull requests for collaborative change management.

However, Git is not the only option. OCI (Open Container Initiative) registries can act as a unified state store for many artifact types used in Kubernetes ecosystems — container images, Helm charts, plain manifests, overlays, policy bundles, and more — letting you reuse the same registry, authentication, and access controls across those artifact types.

Why use OCI as a state store?

* Consolidates multiple artifact types into a single registry.
* Reuses existing authentication/authorization and lifecycle tooling.
* Enables GitOps operators (Flux, Argo CD) to pull artifacts from registries that support OCI artifacts.

OCI defines standards for container image formats and runtimes. The OCI Artifact model extends container images so registries can store arbitrary artifact types (images, Helm charts, manifest bundles, policies) as first-class artifacts.

<Frame>
  <img alt="The image explains OCI Artifacts, showing how various data types like images, Helm charts, and Kubernetes manifests are stored and distributed using OCI registries. It includes a diagram illustrating the structure of a registry with different artifact versions." />
</Frame>

A single OCI registry can host multiple repositories; each repository can contain multiple artifacts and versions. Common OCI registry providers include GitHub Container Registry, Docker Hub, Azure Container Registry, and Google Artifact Registry.

Table: Typical storage locations vs. OCI as a consolidated option

|                   Resource type | Typical storage                                                    | OCI alternative                                        |
| ------------------------------: | ------------------------------------------------------------------ | ------------------------------------------------------ |
|                Container images | Container registries (e.g., [Docker Hub](https://hub.docker.com/)) | OCI registry repository (image manifests)              |
|                     Helm charts | Chart repositories or registries                                   | Helm charts stored as OCI artifacts                    |
| Kubernetes manifests / overlays | Git repositories (manifests, kustomize overlays)                   | Manifest bundles pushed as OCI artifacts (Flux/others) |
|      Policy bundles (e.g., OPA) | Policy stores / Git                                                | Policies packaged and stored as OCI artifacts          |

Callouts

<Callout icon="lightbulb">
  Using a single OCI registry for multiple artifact types simplifies access management: you can reuse the same credentials, RBAC rules, and audit trails for images, charts, and other artifacts.
</Callout>

<Callout icon="warning">
  Do not embed long-lived credentials in scripts. Prefer short-lived tokens, OIDC-based flows, or CI/CD secret managers. Always revoke or rotate Personal Access Tokens (PATs) used for registry access.
</Callout>

Below are practical examples showing how to push images, Helm charts, and plain Kubernetes manifests into an OCI-compliant registry. The examples use GitHub Container Registry (`ghcr.io`) but the commands and concepts apply to other OCI registries (Docker Hub, Azure Container Registry, Google Artifact Registry).

## Pushing container images to an OCI registry

Steps:

1. Authenticate to the registry (use a Personal Access Token or other secure credentials).
2. Tag the local image using the registry repository name.
3. Push the tagged image.

Example (replace `<<GITHUB_PERSONAL_ACCESS_TOKEN>>` with your token):

```bash theme={null}
