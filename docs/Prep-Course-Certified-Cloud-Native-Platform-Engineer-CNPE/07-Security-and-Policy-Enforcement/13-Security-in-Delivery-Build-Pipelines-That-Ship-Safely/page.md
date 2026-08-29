# Can I create deployments in payments?
kubectl auth can-i create deployments -n payments
# => yes
```

* Can user `alice` delete Secrets in `production`?

```bash theme={null}
kubectl auth can-i delete secrets -n production --as=alice
# => no
```

* What can the `deploy-bot` service account do in `payments`?

```bash theme={null}
kubectl auth can-i --list -n payments --as=system:serviceaccount:cicd:deploy-bot
```

Quick tips:

* Impersonate a user: `--as=<user>`
* Impersonate a service account: `--as=system:serviceaccount:<namespace>:<name>`
* Enumerate all permissions: `--list`
* After applying Roles/Bindings, run `kubectl auth can-i` to confirm expected behavior.

Practical examples table

| Goal                                                      | Command                                                                                   |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Check if current user can update deployments in `default` | `kubectl auth can-i update deployments -n default`                                        |
| See all permissions for a service account                 | `kubectl auth can-i --list --as=system:serviceaccount:my-namespace:my-sa -n my-namespace` |
| Impersonate a specific user for a single check            | `kubectl auth can-i get pods -n prod --as=alice`                                          |

Wrap-up: core concepts

* Role and ClusterRole define permissions (rules built from `apiGroups`, `resources`, optional `resourceNames`, and `verbs`).
* RoleBinding and ClusterRoleBinding grant those permissions to subjects.
* Prefer namespace-scoped `Role` + `RoleBinding` for day-to-day access.
* Use `kubectl auth can-i` to validate and debug RBAC policies.

<Frame>
  <img alt="The image presents three key takeaways about RBAC, highlighting core resources, namespace-scoped access, and the definition of rules using apiGroups, resources, and verbs." />
</Frame>

Further reading

* Kubernetes RBAC documentation: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* Best practices: favor least-privilege, prefer namespace-scoped roles, and regularly audit bindings.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/997cda2d-bff5-4d6c-af4d-47784cdd3498)


# Security in Delivery Build Pipelines That Ship Safely

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Security-in-Delivery-Build-Pipelines-That-Ship-Safely/page

Hardening CI/CD delivery pipelines by building, scanning, signing, and enforcing admission of container images to prevent supply chain attacks

Earlier guidance often focused on securing what runs inside the cluster—RBAC, admission control, PSS, mTLS. This document shifts the emphasis to what gets into the cluster in the first place by hardening the delivery pipeline, container images, dependencies, and build artifacts. If attackers cannot get through your runtime protections, they will try your supply chain. This lesson covers practical controls—image scanning, signing, admission enforcement—and how SLSA and SBOMs fit into a robust pipeline.

<Frame>
  <img alt="The image outlines four learning objectives related to software security and integrity, including image scanning, signing, enforcement policies, and SLSA/SBOM concepts." />
</Frame>

## Why supply-chain attacks are high-impact

Supply chain attacks are particularly damaging because they break trust at the source. Common supply-chain risks include:

* Vulnerable base images — pulling a public image that contains many known CVEs.
* Compromised dependencies — malicious packages injected into npm, PyPI, or Go modules during the build.
* Tampered artifacts — images or binaries modified between build and deploy.
* Unscanned images — artifacts reaching production without any vulnerability checks.

These threats target the build process rather than runtime components. To mitigate them, security must shift left into CI/CD and artifact management.

<Frame>
  <img alt="The image outlines the supply chain attack surface, highlighting vulnerabilities such as vulnerable base images, compromised dependencies, tampered artifacts, and unscanned images in production. Each point explains potential risks like CVEs, malicious packages, and unchecked vulnerabilities." />
</Frame>

## Four pipeline gates to enforce

A practical, enforceable delivery pipeline includes four gates. Each gate addresses a different threat class and should be automated in CI:

| Gate  | Goal                                               | Common tools & practices                                                                                                                                                                                 |
| ----- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Build | Produce minimal, reproducible images               | Multi-stage Dockerfiles, pinned dependencies, minimal base images (e.g., [distroless](https://github.com/GoogleContainerTools/distroless), [Alpine](https://alpinelinux.org/)), reproducible build flags |
| Scan  | Detect known vulnerabilities and misconfigurations | `Trivy`, `Grype`, `Anchore`; fail pipelines on disallowed severities                                                                                                                                     |
| Sign  | Prove provenance and integrity of artifacts        | `Cosign` (key-based or keyless with Sigstore Fulcio/Rekor), recorded attestations                                                                                                                        |
| Admit | Enforce that only scanned & signed artifacts run   | Admission controllers like `Kyverno`, `OPA/Gatekeeper` validating signatures and SBOM attestation                                                                                                        |

<Frame>
  <img alt="The image outlines a secure pipeline with four gates: Build, Scan, Sign, and Admit, each accompanied by relevant tools and practices." />
</Frame>

Make sure code and artifacts flow through these gates before deployment. The sections below provide concrete tools, commands, and an end-to-end flow you can adopt.

## Image scanning with Trivy

Use image scanning as a hard gate in CI—not just informational output. Trivy is a widely used open-source scanner that finds vulnerabilities in OS packages, application dependencies, and common misconfigurations.

Key CI behavior:

* Fail the pipeline when unacceptable severities are found.
* Treat scanner errors as failures (don’t allow unknown scanner state to be an implicit pass).

Example usage:

```bash theme={null}
