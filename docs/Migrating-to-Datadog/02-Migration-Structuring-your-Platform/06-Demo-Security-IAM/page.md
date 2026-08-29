# Demo Security IAM

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Demo-Security-IAM/page

Guide to Datadog identity and access management covering users, teams, service accounts, keys, roles, authentication, federation, and best practices for least privilege and secret management

Hello — welcome to the Datadog IAM lesson.

This guide explains how identity and access are managed inside Datadog. We'll cover Organization Settings, users, teams, service accounts, authentication methods, key types, roles, and a few platform integrations. The goal is to give a practical walkthrough of where to configure access and how to apply security best practices.

## Organization Settings → Users

From the Datadog console, open the main menu and go to **Organization Settings** → **Users**. The Users list shows every human and non-human account in the organization. Use filters for status (active, deactivated, service account) and invite new members with the **Invite Users** button (top-right): enter an email and assign a role during invitation.

Clicking an account opens the user detail view with:

* Name, email, creation & modification timestamps
* Team memberships and role assignments
* Security settings (MFA status, password policy)
* Permissions attached to that account

Use the **Edit** action to change roles or disable accounts. For example, a Global Admin will show broad permissions (Management, API & Application Keys, Billing & Usage, Teams, Log Management, etc.).

## Teams

Teams let you mirror your company structure inside Datadog (e.g., Development, SRE, Security, FinOps). Teams can own and be linked to resources (dashboards, notebooks, apps, incidents) so members see only relevant resources.

<Frame>
  <img alt="The image shows a Datadog organization settings page with a focus on managing teams, displaying options for team creation and management on a dashboard." />
</Frame>

Click a team to attach dashboards, notebooks, applications, and incidents — this centralizes access and makes resource ownership explicit.

<Frame>
  <img alt="The image shows a web dashboard interface of a team management tool called Datadog, displaying sections for dashboards, services, and incidents, with options to attach the team to these areas." />
</Frame>

## Service accounts

Service accounts are non-human identities used by automated workflows (Lambda functions, CI/CD pipelines, agents). They can own application keys and receive roles like human users, but are designed for programmatic access.

To create a service account:

* Click **New Service Account**
* Provide a name (optional email)
* Assign the minimum role required for the automation

> **warning** Do not assign a Datadog Admin role to production service accounts. Apply least privilege to reduce blast radius if credentials are exposed.

Service account details include creation metadata, assigned roles, and associated application keys.

<Frame>
  <img alt="This image shows a dashboard interface for managing service accounts, specifically displaying details and settings for a service account within a system, including its email, status, and roles." />
</Frame>

## Application keys

Application keys, used together with an org-level API key, let applications call Datadog APIs. Create app keys for integrations or tools that need to operate on behalf of a user or service account. Application keys identify the calling application; pair them with minimal scopes.

<Frame>
  <img alt="The image displays a screenshot of a service account management interface with details about a specific account, including its name, email, and role. It also shows options for application keys and permissions associated with the service account." />
</Frame>

## Authentication (Login Methods)

Datadog supports multiple login methods and authentication policies. In Organization Settings you can:

* Configure password policies
* Enable/require Multi-Factor Authentication (MFA)
* Set up federated identity providers (Google OAuth, SAML, OIDC)

<Frame>
  <img alt="The image shows the &#x22;Login Methods&#x22; settings page from the Datadog dashboard, detailing authentication options like password, Google, and SAML, along with multi-factor authentication settings." />
</Frame>

## Federation (SAML / Identity Providers)

Federation with SAML/OIDC/Google OAuth allows teams to use existing corporate identities ([Okta](https://www.okta.com/), [Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/active-directory/), [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/)). Benefits:

* Centralized lifecycle management (hire/transfer/terminate)
* Centralized MFA enforcement and conditional access
* Simplified onboarding and offboarding

> **lightbulb** Integrate SAML/OIDC to enforce corporate access controls and centralize user lifecycle, MFA, and group membership management.

### SAML Group Mappings

SAML group mappings convert identity-provider group attributes into Datadog properties and roles. When a user authenticates, the IdP token can include group claims; Datadog maps those claims to platform roles or team memberships (for example, mapping an IdP group to the Log Management role).

<Frame>
  <img alt="The image shows a Datadog dashboard screen for SAML Group Mappings, with the message &#x22;No team mapping rules configured&#x22; and options to create new mappings. There is a navigation menu on the left with various settings options." />
</Frame>

## API keys

API keys authenticate Datadog agents and backend integrations. They are used by agents (metrics, logs, traces) and cluster agents to send telemetry to Datadog.

<Frame>
  <img alt="The image shows a Datadog API Keys management interface, displaying a list of API keys with details such as name, key ID, creation date, and last usage." />
</Frame>

To create an API key: click **New Key**, name it, and copy the value to your secure secrets store. API keys are masked by default — use the eye icon to reveal the key for copying.

<Frame>
  <img alt="The image shows a Datadog API Keys settings page with a pop-up window displaying the creation of a new API key named &#x22;Kodekloud-2-apikey.&#x22;" />
</Frame>

Best practices for API keys:

* Store keys in a secrets manager (e.g., [HashiCorp Vault](https://www.vaultproject.io/), cloud KMS).
* Rotate keys regularly and remove unused keys.
* Revoke immediately if a key is leaked or committed to source control.

## Key types at-a-glance

| Key type        | Primary use                                    | Typical placement       |
| --------------- | ---------------------------------------------- | ----------------------- |
| API key         | Agent and backend telemetry ingestion          | Backend servers, agents |
| Application key | Programmatic API access for tools/integrations | CI/CD, automation apps  |
| Client token    | Frontend RUM/browser identification            | Browser/JS code         |

## Application keys (detailed scopes)

Application keys can be scoped to limit what the key can do. When creating or editing an application key, select the minimal scopes required (e.g., `billing_read` for FinOps tools). Scoping reduces exposure if a key is compromised.

<Frame>
  <img alt="The image shows a Datadog web application interface displaying a list of application keys, with options to filter and view details about each key." />
</Frame>

Edit an application key to adjust permissions and maintain least privilege.

<Frame>
  <img alt="The image shows a software interface with a pop-up window titled &#x22;Edit Key Scope,&#x22; listing various permissions related to API and application keys. This interface is part of an organization settings configuration." />
</Frame>

Example: For a FinOps tool that only needs billing metrics, grant `billing_read` instead of full admin rights.

<Frame>
  <img alt="The image shows a software interface for editing key scopes, specifically related to billing and usage permissions in an application setting. Options include managing and viewing a subscription and payment method." />
</Frame>

## Roles

Roles are reusable permission sets you attach to users, service accounts, or application keys. Create roles to represent job functions (SRE, Developer, FinOps, Executive) and assign only the permissions required.

<Frame>
  <img alt="The image shows a Datadog interface with a focus on organization settings, specifically the &#x22;Roles&#x22; section where permissions for a new role are being configured. The UI displays various management and log-related permissions." />
</Frame>

To create a role:

* Choose a descriptive name
* Select granular permissions (logs, metrics, traces, billing)
* Save and attach the role to users or service accounts

<Frame>
  <img alt="The image shows a web interface for creating a new role in Datadog, displaying options for setting permissions and access management. It includes sections for roles, new role creation, and relevant user and API permissions." />
</Frame>

The Roles list displays roles and how many users are attached, helping you track role usage.

<Frame>
  <img alt="This image shows the roles management section of Datadog's organization settings, displaying various roles and associated user numbers." />
</Frame>

## Client tokens (RUM / frontend)

Client tokens are for browser/JS usage and differ from backend API/application keys. Use client tokens to identify Real User Monitoring (RUM) instances in the frontend. Never embed backend API keys or application keys in client-side code.

<Frame>
  <img alt="The image shows a Datadog client token management screen, listing details of a client token, including its name, creator, and creation date." />
</Frame>

## Events API — Email integration

Datadog’s Events API can send events and reports to email endpoints. Configure **New Email** to specify recipients, tags, formats, and alert types for automated reports (monthly billing, incident digests).

<Frame>
  <img alt="The image shows a Datadog organization settings interface, specifically for creating a new &#x22;Events API Email,&#x22; with options for email format, tags, recipients, and alert type." />
</Frame>

## Cross-Organization Visibility

For companies with multiple Datadog tenants (different business units or acquisitions), Cross-Org Visibility allows tenants to share selected dashboards and resources. Configure cross-org rules to control which resources are shared and which tenants can view them.

<Frame>
  <img alt="The image shows a Datadog interface for Cross-Organization Visibility settings, indicating that the organization does not have access to create cross-organization connections." />
</Frame>

## Wrap-up

This lesson covered Datadog IAM essentials:

* Users and Teams — organize accounts and resources
* Service accounts and Application keys — automate safely
* Federation (SAML/OIDC) — centralize identity and MFA
* API keys, Application keys, Client tokens — choose the right key type
* Roles and Scopes — apply least privilege
* Cross-Org Visibility and Events integrations

Key principles:

* Use least privilege: narrow scopes and roles
* Centralize identity: integrate SAML/OIDC where possible
* Protect secrets: use secrets managers and rotate keys
* Audit regularly: remove unused credentials and review mappings

## Links and references

* Datadog IAM & SSO docs: [https://docs.datadoghq.com/account\_management/](https://docs.datadoghq.com/account_management/)
* SAML and SSO integrations: [https://docs.datadoghq.com/account\_management/saml/](https://docs.datadoghq.com/account_management/saml/)
* HashiCorp Vault: [https://www.vaultproject.io/](https://www.vaultproject.io/)
* Okta: [https://www.okta.com/](https://www.okta.com/)
* Microsoft Entra ID: [https://learn.microsoft.com/en-us/azure/active-directory/](https://learn.microsoft.com/en-us/azure/active-directory/)
* AWS IAM Identity Center: [https://aws.amazon.com/iam/identity-center/](https://aws.amazon.com/iam/identity-center/)

I hope this lesson was helpful.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/a62115c0-be96-4928-8050-985df8cfa163)
