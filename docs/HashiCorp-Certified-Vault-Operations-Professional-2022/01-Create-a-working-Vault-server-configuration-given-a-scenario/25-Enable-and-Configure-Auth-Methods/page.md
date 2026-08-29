# Enable and Configure Auth Methods

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Enable-and-Configure-Auth-Methods/page

This guide introduces Vaults authentication methods, their workflow, supported options, and management via CLI and API.

As a Vault Operations professional, you must enable, configure, and integrate Vault’s authentication methods for daily operations and certification exams. This guide introduces auth methods, explains their workflow, reviews supported options, and shows how to manage them via CLI and API.

***

## What Are Auth Methods?

Auth methods in Vault validate credentials, assign identities, and issue client tokens. Every interaction with Vault—whether by a person or a machine—begins with authentication. Vault maps your credentials (from an external identity provider or an internal user store) to one or more policies, then issues a token that inherits those policies with a time-to-live (TTL).

![The image is a slide titled "Introduction to Auth Methods," explaining Vault's authentication components, identity management, and token issuance. It includes a certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878436/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/introduction-to-auth-methods-vault.jpg)

***

## Auth Methods Workflow

1. Client (human or system) submits credentials to an auth method (e.g., LDAP, userpass, JWT).
2. Vault validates credentials internally or with an external provider.
3. On success, Vault creates a token, attaches policies, and sets TTLs.
4. The client uses the token to read secrets, write data, or generate dynamic credentials until the token expires.

![The image illustrates an "Auth Methods Workflow" showing a step-by-step process for authenticating with credentials, validating them against a provider, generating a vault token with policy and TTL, and accessing secrets in a vault using the token.](https://kodekloud.com/kk-media/image/upload/v1752878437/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/auth-methods-workflow-authentication-process.jpg)

***

## Supported Auth Methods

Vault supports a wide range of authentication methods, including cloud platforms, OIDC/OAuth providers, identity services, and built-in options.

| Category                  | Methods                                                           |
| ------------------------- | ----------------------------------------------------------------- |
| External (human/system)   | AWS, Azure, Kubernetes, GitHub, Okta, OIDC, JWT, RADIUS, and more |
| Internal (built-in Vault) | AppRole, userpass, token, TLS                                     |

> **lightbulb** On Vault certification exams, focus on built-in methods (AppRole, userpass, token) since they don’t require external integrations.

![The image displays various authentication methods and services, including logos and names like AWS, Kubernetes, GitHub, Okta, and Microsoft Azure, among others.](https://kodekloud.com/kk-media/image/upload/v1752878439/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/authentication-methods-aws-kubernetes-logos.jpg)

***

## Human vs. System Authentication

Human-based auth methods integrate with identity providers or prompt users for credentials and MFA.

![The image describes human-based authentication methods, highlighting integration with identity providers and platforms like GitHub, Okta, and RADIUS, and mentions userpass and JWT/OIDC.](https://kodekloud.com/kk-media/image/upload/v1752878440/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/human-authentication-methods-identity-providers.jpg)

Examples:

* GitHub
* JWT/OIDC
* Okta
* RADIUS
* userpass

System-based auth methods rely on machine-friendly credentials issued by platform services.

![The image is a presentation slide about system-based authentication methods, featuring various cloud platforms and technologies like AWS, Azure, Kubernetes, and others. It highlights the integration of these methods with existing platforms and the validation of credentials by Vault.](https://kodekloud.com/kk-media/image/upload/v1752878442/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/system-authentication-cloud-platforms-presentation.jpg)

Examples:

* AWS, Azure, GCP, Kubernetes, Alibaba, Oracle Cloud
* Kerberos (via Active Directory)
* TLS certificates

***

## Managing Auth Methods in Vault

By default, Vault enables only two auth methods: `identity` and `token`. You can enable additional methods (even the same type at different paths). The token method is always active and cannot be disabled. To make changes, you need a valid Vault token with appropriate policies.

> **triangle-alert** All auth method operations require a Vault token with the `sys/auth/*` capability. Without it, enable/disable and configuration commands will fail.

![The image is a slide titled "Working with Auth Methods," explaining the requirements and default settings for authentication methods in Vault deployments. It includes bullet points about enabling auth methods, using multiple methods, and the default token auth method.](https://kodekloud.com/kk-media/image/upload/v1752878443/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/working-with-auth-methods-vault.jpg)

![The image is a slide titled "Working with Auth Methods," explaining that authentication methods can be managed using the UI, API, or CLI, and a valid token with proper privileges is required. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878444/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Auth-Methods/working-with-auth-methods-slide.jpg)

***

### CLI: Enable, Disable, and List Auth Methods

Enable the AppRole method at its default path:

```bash theme={null}
vault auth enable approle
