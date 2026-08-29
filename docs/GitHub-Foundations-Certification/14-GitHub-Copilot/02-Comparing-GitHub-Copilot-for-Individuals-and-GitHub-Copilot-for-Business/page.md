# Save local edits, stage, commit, and push to the remote repository
git add .
git commit -m "Describe changes made in the Codespace"
git push origin HEAD
```

Tip: commit frequently and push before stopping or deleting a Codespace to avoid accidental data loss.

## Deletion and end of lifecycle

Deletion is final: when a Codespace is deleted, its VM and persistent storage are removed and cannot be recovered.

* You can create multiple Codespaces per branch but watch account and organization limits — you may need to delete older Codespaces when limits are reached.
* Consider exporting or merging important changes into branches or pull requests before deleting an environment.

<Frame>
  <img alt="The image shows a diagram illustrating the lifecycle of a Codespace, including stages like creation, rebuilding, stopping, and deletion. A circular flowchart and a sidebar with labeled steps are present." />
</Frame>

> **warning** Before stopping or deleting a Codespace, verify that all necessary work has been committed and pushed to the remote repository. Unpushed changes that exist only on the Codespace will be lost upon deletion.

## Links and references

* [GitHub Codespaces documentation](https://docs.github.com/codespaces)
* [Dev Containers (devcontainer.json) reference](https://containers.dev/)
* [Git basics](https://git-scm.com/book/en/v2)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/ba455f92-d934-485a-83d3-272d1965fc17)


# Comparing GitHub Copilot for Individuals and GitHub Copilot for Business

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Copilot/Comparing-GitHub-Copilot-for-Individuals-and-GitHub-Copilot-for-Business/page

Comparing GitHub Copilot Individual versus Business and Enterprise plans, highlighting differences in administration, privacy, governance, integrations, and suitability for solo developers versus organizations.

This lesson compares GitHub Copilot for Individuals with GitHub Copilot for Business (and Enterprise) to help you choose the plan that best fits your needs. Both plans use the same underlying AI models, but Business and Enterprise tiers add governance, privacy, and administrative capabilities built for teams and organizations.

> **lightbulb** This article focuses on functional and administrative differences between the Individual and Business/Enterprise plans. For the latest pricing, exact feature availability, and up-to-date limits, consult GitHub’s official Copilot documentation: [GitHub Copilot docs](https://docs.github.com/en/copilot).

## At-a-glance comparison

| Area                      | GitHub Copilot for Individuals         | GitHub Copilot for Business / Enterprise                                             |
| ------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------ |
| Target users              | Solo developers, students, freelancers | Teams, organizations, and enterprises                                                |
| Billing & seats           | Personal subscription billed per user  | Centralized billing and seat management                                              |
| Admin controls            | Per-user account settings              | Organization-wide admin controls and role-based access                               |
| Authentication            | Standard GitHub authentication         | Enterprise SSO (`SAML` / `SCIM` provisioning) and stronger identity controls         |
| Privacy & data governance | Standard privacy protections           | Admin policies, `audit logs`, and controls to limit how org data is used             |
| Code personalization      | Context from local and public code     | Deeper integration with private repos and internal libraries (subject to org policy) |
| Integrations              | Common IDE and CLI extensions          | Deeper GitHub Enterprise Cloud integrations and enterprise support channels          |
| Scaling & quotas          | Single-user usage limits               | Organization-level seat and rate-limit management (varies by plan)                   |

## Target audience and administration

* Individual: ideal for single developers who manage their own account, billing, and settings. Setup is straightforward and focused on personal productivity.
* Business / Enterprise: built for organizations requiring centralized administration. Key capabilities include:
  * Centralized seat provisioning and deprovisioning
  * Centralized billing and invoicing
  * Role-based access and admin controls
  * Integration with identity providers (`SSO`, `SAML`) and user provisioning (`SCIM`)

## Security, privacy, and compliance

* Individual: includes GitHub’s standard privacy and safety protections suitable for personal use.
* Business / Enterprise: adds enterprise-grade controls to meet compliance needs:
  * Organization-wide policy enforcement and configuration
  * Administrative `audit logs` and activity monitoring
  * Options to restrict how organization code is used for training
  * Enterprise authentication (SSO) and centralized provisioning

> **warning** If your organization needs to prevent internal source code from being used to improve public models, choose Business/Enterprise and configure your data usage policies and repository settings accordingly. Always review the subscription terms and data handling controls in GitHub’s documentation.

## Code personalization and context

* Individual: suggestions leverage the local file context and general public knowledge sources to offer context-aware completions.
* Business / Enterprise: provides enhanced personalization by integrating with private repositories and internal knowledge (e.g., internal libraries and coding patterns). These suggestions respect the organization’s data usage policies and governance settings.

## Usage, scaling, and rate limits

* Individual: licensed per user for personal productivity—suitable for individual workflows and development environments.
* Business / Enterprise: designed to scale across teams and organizations with features for:
  * Central seat management and bulk provisioning
  * Enterprise-appropriate rate limits and usage allowances (detailed in plan terms)
  * Administrative controls around usage monitoring and reporting

## Integrations and tooling

* Individual: supports the common editor extensions (VS Code, JetBrains, etc.) and CLI workflows most developers use daily.
* Business / Enterprise: offers deeper integration with GitHub Enterprise Cloud and other enterprise tools, including:
  * Organization-wide synchronizations and policy enforcement
  * Access to enterprise support channels and SLAs
  * Potential integrations with collaboration tools and GitHub Mobile Chat depending on plan

## When to choose which plan

* Choose GitHub Copilot for Individuals if:
  * You are a solo developer or student
  * You prefer a simple, per-user subscription with personal account management
  * You don’t need centralized billing, provisioning, or organizational governance

* Choose GitHub Copilot for Business or Enterprise if:
  * You manage teams and need centralized billing or seat control
  * You require enterprise authentication (`SSO`) and provisioning (`SCIM`)
  * You must enforce organization-wide privacy and data usage policies
  * You want deeper integration with private repos and enterprise support

## Summary

* Both tiers deliver the same core AI-powered coding experience.
* The Individual plan focuses on personal productivity and ease of setup.
* Business and Enterprise tiers add centralized administration, stronger privacy and governance controls, deeper internal code personalization, and integrations suitable for team-based workflows.

## Links and references

* [GitHub Copilot documentation](https://docs.github.com/en/copilot)
* [GitHub Enterprise Cloud](https://docs.github.com/en/enterprise-cloud)
* [Identity providers and SAML/SCIM provisioning](https://docs.github.com/en/enterprise-cloud@latest/admin/authentication)

> **lightbulb** Choosing between Individual and Business/Enterprise comes down to scale and governance needs. Pick Individual for a personal, per-user experience; pick Business/Enterprise for centralized billing, seat provisioning, advanced privacy controls, and administrative governance.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/10478142-ccb7-4c4e-9a4d-7d9820bb8db6/lesson/c3df3d98-6a20-42cd-9ed4-8af39db3fc18)
