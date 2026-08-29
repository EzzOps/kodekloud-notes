# Enterprise Managed Users EMUs

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Authentication-and-Security/Enterprise-Managed-Users-EMUs/page

Explains GitHub Enterprise Managed Users, centralized IdP-controlled accounts that automate provisioning, authentication, offboarding, enforce enterprise ownership, compliance, and restrict external collaboration to protect IP.

In this lesson we’ll cover Enterprise Managed Users (EMUs) — a GitHub Enterprise Cloud feature that gives organizations centralized, enterprise-owned control over user identities and the account lifecycle. EMUs eliminate individually owned GitHub accounts in favor of accounts provisioned, authenticated, and revoked by your corporate identity provider (IdP).

Enterprise Managed Users (EMUs) are a premium capability of [GitHub Enterprise Cloud](https://docs.github.com/en/enterprise-cloud) designed for organizations that require strict ownership, compliance, and automation for developer accounts. EMUs are created and managed by the enterprise via an external IdP such as [Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis) or [Okta](https://www.okta.com/). Users do not self-register; their GitHub account lifecycle is derived from their corporate identity.

How EMUs work — provisioning, authentication, and offboarding:

* Provisioning: The IdP provisions accounts based on enterprise policies and group memberships.
* Authentication: Users sign in through the IdP (SSO). GitHub trusts the enterprise-managed identity for access.
* Offboarding: Removing a user from the IdP immediately revokes their GitHub access and membership in orgs/teams.

Mapping GitHub teams to IdP groups automates membership: adding a user to an IdP group places them into the corresponding GitHub team; removing them from the IdP group immediately revokes access to enterprise resources.

<Frame>
  <img alt="The image shows two labeled sections: &#x22;Joining&#x22; in blue, describing automatic syncing of a user to a GitHub team upon joining an IdP group, and &#x22;Offboarding&#x22; in purple, explaining immediate access revocation from GitHub resources when removing a user from the IdP." />
</Frame>

Why use Enterprise Managed Users?

| Benefit                            | What it solves                                                       | Example outcome                                           |
| ---------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------- |
| Strict compliance and ownership    | Ensures accounts are enterprise-owned for regulatory and legal needs | Enterprise retains ownership of accounts and audit trails |
| Automated lifecycle management     | Removes manual provisioning/offboarding and reduces human error      | Onboarding completes when a user is added to an IdP group |
| Traceability and auditing          | Centralized identity and activity logs improve investigations        | Consistent audit records tied to enterprise identity      |
| Centralized administrative control | IT/security control who has access and when it is revoked            | Policy-driven access removal across all orgs and teams    |
| Corporate ownership of work        | Prevents developer accounts from becoming personal assets            | Code and contributions remain enterprise property         |

<Frame>
  <img alt="The image contains two colored boxes with text: one stating &#x22;All accounts are owned by the enterprise&#x22; and the other stating &#x22;Access is automatically granted or removed based on IdP membership,&#x22; under the heading &#x22;EMUs help ensure that.&#x22;" />
</Frame>

Controlled collaboration and IP protection

EMUs are optimized for internal collaboration. By design, managed users operate within enterprise boundaries to reduce the risk of accidental data exposure and to maintain governance. Typical enterprise restrictions for managed users include:

* No forking of private repositories outside the enterprise.
* No ability to push to repositories owned by external accounts.
* Network and repository-level policies that limit interactions to internal users and resources.

These restrictions help ensure intellectual property remains a corporate asset and that collaboration stays inside approved channels.

<Callout icon="warning">
  Managed users are intentionally restricted to internal collaboration. Before enabling EMUs, review your organization’s collaboration and CI/CD workflows to ensure external integrations and open-source contribution processes are compatible with enterprise-only accounts.
</Callout>

<Frame>
  <img alt="The image describes restrictions on managed users within an enterprise context, stating they cannot push code or fork repositories outside the enterprise and can only interact with internal users and resources." />
</Frame>

Implementation notes and best practices

<Callout icon="lightbulb">
  Plan your IdP-to-GitHub mapping strategy before enabling EMUs. Common best practices:

  * Map IdP groups to GitHub teams for role-based access control.
  * Use group lifecycle automation (HR system → IdP → GitHub) for reliable onboarding/offboarding.
  * Audit group memberships and SSO logs regularly to verify policy enforcement.
</Callout>

Links and further reading

* [GitHub Enterprise Cloud documentation — Identity and access management](https://docs.github.com/en/enterprise-cloud)
* [Microsoft Entra ID (Azure AD) overview](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis)
* [Okta Identity Cloud](https://www.okta.com/)

This overview explains why organizations adopt EMUs, how EMUs automate identity lifecycles via an IdP, and which controls help protect corporate IP while maintaining compliance and traceability.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/ea947699-ceb4-48b5-bde9-d0de4c959c2e/lesson/29fac003-d0d7-471f-b7e3-adc7f1ad5d49" />
</CardGroup>
