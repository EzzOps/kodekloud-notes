# (Terraform will show "Refreshing state..." and then a plan indicating ~ public_network_access_enabled = true -> false)
```

5. Example: apply while skipping refresh

```bash theme={null}
terraform apply --refresh=false
```

Outcomes to expect:

* If your state still showed `true` (and Azure is `true`), skipping refresh will still apply the change and update state.
* If your state already showed `false`, but someone manually changed Azure back to `true`, then `--refresh=false` will skip detection and do nothing—leaving Azure and state/config out of sync. This is the risky scenario.

Observe the Azure portal
After applying a change, confirm it in the portal. For example, open the storage account in the Azure portal, go to Security and Networking → Networking, and verify the public network access setting reflects Terraform's change.

<Frame>
  <img alt="This image shows a Microsoft Azure portal interface for managing a storage account named &#x22;ststaterefreshdemo,&#x22; displaying properties like resource group, location, and security settings. Various features and settings related to the storage account are also shown, including Blob service configurations, security, and networking." />
</Frame>

If you manually toggle that setting back to Enabled in the portal and save it, Terraform will detect that drift the next time it refreshes the state and will plan to reconcile it (unless you use `-refresh=false`).

<Frame>
  <img alt="The image shows a Microsoft Azure settings page for configuring public network access, with options to enable or restrict access for a resource. It features selections for the scope of access, including options for all networks or selected networks." />
</Frame>

Summary — Key takeaways

* Default Terraform behavior is to refresh state before planning or applying; this ensures plans reflect live infrastructure and detect out-of-band changes.
* `-refresh=false` can speed up execution but is risky: it relies solely on the state file and can hide drift.
* In production, prefer the default refresh behavior for safety, accuracy, and predictable outcomes.

Further reading and references

* Terraform state and remote backends: [https://www.terraform.io/docs/language/state/index.html](https://www.terraform.io/docs/language/state/index.html)
* AzureRM provider documentation: [https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])
* Azure Storage Account networking docs: [https://learn.microsoft.com/azure/storage/common/storage-network-security-overview](https://learn.microsoft.com/azure/storage/common/storage-network-security-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/d0fef6dd-c271-403d-b4ac-ee1f20c1839b/lesson/7e31901f-16e5-435c-9f0a-6aff7e3ad43c" />
</CardGroup>


# Security Considerations

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-State-Fundamentals/Security-Considerations/page

Best practices for securely managing Terraform state to protect secrets, using encrypted remote backends, RBAC, locking, sensitive outputs, and avoiding committing state files.

When working with Terraform, one of the most critical concerns is the security of the Terraform state. The Terraform state file is not just a harmless JSON blob — it frequently contains highly sensitive information such as passwords, keys, connection strings, private IPs, and other secrets. Storing that file on a laptop, a shared drive, or in a Git repository can create a severe security exposure.

Why state is sensitive

* State may contain resource attributes that include secrets (access keys, connection strings, certificates).
* It often represents a complete inventory of infrastructure that attackers can use for lateral movement.
* Backing up or copying state without encryption or access control can create additional attack surfaces.

Sanitized example showing how secret-like values can appear in state:

```json theme={null}
{
  "primary_access_key": "REDACTED",
  "secondary_access_key": "REDACTED",
  "shared_access_key_enabled": true
}
```

Key guidelines and best practices

* Store Terraform state in a secure, access-controlled, encrypted, and versioned remote backend for team or production environments (examples below).
* Use backend locking to prevent concurrent `apply` conflicts (the AzureRM backend supports locking via blob leases when configured properly).
* Apply RBAC and least-privilege permissions for the backend. Prefer Azure AD principals or Managed Identities scoped narrowly rather than broad storage account keys.
* Enable encryption at rest for the backend. For stronger control and auditability, consider customer-managed keys (CMK) stored in Key Vault.
* Never commit `terraform.tfstate` or plaintext copies to source control. Add it to `.gitignore`.
* Use the Terraform CLI subcommands to inspect state safely instead of opening raw files.

Table — Best practices at a glance

| Concern              | Recommended action                                         | Example / Notes                                            |
| -------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| Remote state storage | Use a secure remote backend with versioning and encryption | Terraform Cloud, `azurerm` backend with encryption enabled |
| Concurrency          | Enable backend locking                                     | AzureRM blob lease locking                                 |
| Access control       | Use RBAC, Managed Identity, or short-lived credentials     | Avoid distributing storage account keys widely             |
| Sensitive outputs    | Mark outputs as sensitive                                  | See HCL example below                                      |
| Source control       | Do not commit state files                                  | Add `terraform.tfstate` to `.gitignore`                    |
| Inspection           | Use Terraform CLI commands                                 | `terraform show`, `terraform state pull`                   |

Commands for safe inspection

* `terraform state pull` — fetch the raw state from the configured backend.
* `terraform show` — produce a human-readable representation of a plan or state.
* `terraform state list` and `terraform state show <resource>` — query resources and attributes from state.

Examples:

| Command                           | Purpose                                                                |
| --------------------------------- | ---------------------------------------------------------------------- |
| `terraform state pull`            | Pull raw state from backend (beware of sensitive values in the output) |
| `terraform show`                  | Render plan or state in human-readable form                            |
| `terraform state list`            | List resources tracked in state                                        |
| `terraform state show <resource>` | Show attributes for a specific resource                                |

Mark sensitive outputs so they are redacted from CLI output and logs:

```hcl theme={null}
output "storage_account_primary_key" {
  value     = azurerm_storage_account.example.primary_access_key
  sensitive = true
}
```

Security-focused backend example (Azure RM)

* Example backend configuration that stores state in an Azure Storage Account container. This configuration should be paired with proper RBAC on the storage account, blocking public access, and enabling encryption and soft-delete as required.

```hcl theme={null}
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

<Callout icon="warning">
  Never commit `terraform.tfstate` or copies of state to source control. Treat state files like any other secret: add them to `.gitignore`, ensure CI logs do not capture their contents, and limit access to the minimal set of principals that need it.
</Callout>

Additional recommendations

* Prefer short-lived credentials, managed identities, or federated authentication over embedding long-lived secrets in automation.
* Rotate credentials and keys regularly and ensure access to state is auditable.
* Consider Terraform Cloud/Enterprise for built-in remote state management, locking, encryption, access controls, and audit logs.
* When automating state inspection or migration, avoid writing sensitive values to logs or insecure temporary files. If you must write state to disk, restrict file permissions and securely delete artifacts after use.

<Callout icon="lightbulb">
  If you must inspect values from the state, prefer `terraform show` or `terraform state` subcommands instead of opening the raw state file. Mark outputs with `sensitive = true` to prevent accidental exposure in CLI output and logs.
</Callout>

Summary
Terraform state is both powerful and sensitive. Mishandling state can expose secrets and put your entire infrastructure at risk. Secure state management — using encrypted, access-controlled remote backends with locking, RBAC, and auditability — is mandatory for production environments.

References and further reading

* Terraform backends: [https://www.terraform.[AWS_SECRET_ACCESS_KEY].html](https://www.terraform.[AWS_SECRET_ACCESS_KEY].html)
* Terraform state documentation: [https://www.terraform.io/docs/state/index.html](https://www.terraform.io/docs/state/index.html)
* Azure Storage security best practices: [https://learn.microsoft.com/azure/storage/common/storage-security-guide](https://learn.microsoft.com/azure/storage/common/storage-security-guide)
* Terraform Cloud: [https://www.hashicorp.com/products/terraform/cloud](https://www.hashicorp.com/products/terraform/cloud)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/d0fef6dd-c271-403d-b4ac-ee1f20c1839b/lesson/5af2910e-66fe-4508-8577-f7da9e090617" />
</CardGroup>
