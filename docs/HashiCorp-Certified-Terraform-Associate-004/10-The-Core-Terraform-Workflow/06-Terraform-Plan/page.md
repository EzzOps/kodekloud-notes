# Terraform Plan

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Terraform-Plan/page

Guide explaining Terraform plan command which generates a dry-run execution plan showing resource changes, refresh behavior, symbols, saving plans, and best practices to review before applying

Before running the plan stage, ensure your configuration files are written in HCL and your working directory is initialized (providers downloaded and configured). This guide explains `terraform plan`, which acts as a safety net: it shows exactly what Terraform intends to do before making any real changes. That helps prevent surprises like accidentally deleting resources.

Terraform plan generates an execution plan that lists the actions Terraform will take to bring real-world resources in line with your configuration. This is a dry run — nothing is created, modified, or destroyed during planning.

<Frame>
  <img alt="The image explains the &#x22;terraform plan&#x22; command, highlighting its function to generate an execution plan that shows changes to 'real-world' resources and allows for a dry-run to avoid unintended changes. It features text, icons, and a photo of a checklist." />
</Frame>

Think of `terraform plan` like looking at a map before a drive: you can review the route, spot potential issues, and choose whether to proceed. If the plan shows something unexpected, update your configuration before applying changes.

<Callout icon="lightbulb">
  Always run `terraform plan` to review changes before `terraform apply`. It's a best practice for any environment, and essential in production.
</Callout>

What happens when you run `terraform plan`:

* Terraform refreshes state (by default) by querying provider APIs to get the current real-world resource state.
* Terraform compares the refreshed state with your configuration and state file, then generates an execution plan that lists resource actions.
* The plan shows resource actions with symbols indicating the intended change.

Example `terraform plan` output (representative):

```bash theme={null}
$ terraform plan
vault_generic_secret.example_secret: Refreshing state... [id=secret/example]
random_pet.example: Refreshing state... [id=smashing-mutt]
vault_generic_secret.example_kv: Refreshing state... [id=secret/example1]

Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create
  ~ update in-place
  - destroy
  -/+ destroy and then create replacement

Terraform will perform the following actions:
