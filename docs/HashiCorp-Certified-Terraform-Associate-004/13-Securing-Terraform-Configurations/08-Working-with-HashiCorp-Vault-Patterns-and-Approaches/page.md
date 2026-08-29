# Working with HashiCorp Vault Patterns and Approaches

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Working-with-HashiCorp-Vault-Patterns-and-Approaches/page

Using HashiCorp Vault to provide dynamic short-lived credentials for Terraform to reduce credential sprawl, improve auditability, and avoid persisting secrets in state.

In this lesson we wrap up the Vault section by explaining a common production pattern used in enterprises: using HashiCorp Vault to generate dynamic, short-lived credentials for Terraform. This complements concepts you’ve already seen — sensitive variables, encrypted state, ephemeral values, and write-only arguments — and shows how to reduce credential sprawl and improve auditability.

This is a high-level overview to help you understand how Terraform integrates with Vault. You do not need deep Vault expertise for the [Terraform Associate exam](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified), but you should understand the pattern and its benefits.

The problem

Traditionally, Terraform requires credentials to provision infrastructure. Teams often distribute long-lived credentials to each user (AWS access keys, Azure service principals, GCP service account keys, Kubernetes tokens, etc.). These credentials are frequently:

* Highly privileged
* Stored locally on developer machines or CI runners
* Hard to rotate or revoke
* Difficult to audit

If a user leaves or a credential is compromised, it can remain valid for months or years — increasing the attack surface.

What if credentials were short-lived and generated on demand?

<Frame>
  <img alt="The image discusses issues with using static credentials in a traditional approach, highlighting risks such as local storage and difficulty in credential management. It suggests considering short-lived, on-demand generated credentials." />
</Frame>

How Vault changes the model

Vault enables dynamic credential generation so Terraform no longer needs long-lived platform credentials on every client. Typical flow:

1. Terraform authenticates to Vault via an identity-based auth method (AWS Auth, Azure roles, Kubernetes service account token, etc.), chosen based on where Terraform runs.
2. Vault uses the appropriate secrets engine (AWS, Azure, GCP, Kubernetes, etc.) to generate credentials on demand.
3. Vault returns temporary credentials to Terraform.
4. Terraform uses these temporary credentials to authenticate to the cloud provider for the current run.

These credentials are TTL-based (short-lived), scoped to least privilege via Vault roles, and can be revoked automatically when the TTL expires. Long-lived platform credentials remain stored only inside Vault; Terraform clients receive ephemeral credentials in memory during the run.

Example Terraform flow and code

Below is a consolidated illustrative example showing the pieces involved:

* Vault provider configuration (how Terraform connects to Vault and authenticates).
* An ephemeral construct that fetches dynamic credentials from Vault (conceptual in this example).
* A cloud provider block that consumes the temporary credentials returned by that ephemeral construct.
* A normal resource that is provisioned with those credentials.

Note: different environments use different Vault auth methods (AWS auth, Kubernetes, Azure, etc.). Not all providers expose ephemeral resource types — some expose data sources (for example `data "vault_aws_access_credentials"`) or provider-specific constructs to obtain temporary credentials without persisting them to state. Check the provider docs for exact syntax.

```hcl theme={null}
provider "vault" {
  # Vault server address (e.g. https://vault.example.com:8200)
  address = "https://vault.example.com:8200"

  # Configure identity-based authentication (AWS auth, Kubernetes, Azure, etc.)
  # Example: authenticate via the appropriate auth method for wherever Terraform runs.
  # (Fill in according to your environment / Vault auth setup)
}
