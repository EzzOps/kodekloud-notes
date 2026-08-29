# Terraform workspace

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Use-the-Terraform-CLI/Terraform-workspace/page

Terraform workspaces allow management of multiple environments using a single configuration directory by isolating state files for different environments.

Terraform workspaces enable you to manage multiple environments—such as development and production—using a single configuration directory. In this guide, you'll learn how to leverage workspaces to isolate state files for different environments and adjust resource configurations accordingly.

Every Terraform configuration maintains a state file (either locally or remotely) to track resources. Traditionally, there is a one-to-one mapping between a configuration directory and its associated state file. Consider the following example of an AWS instance resource block named "webserver":

```hcl theme={null}
