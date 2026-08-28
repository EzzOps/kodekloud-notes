# Authenticate to Terraform Cloud

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Setup/Authenticate-to-Terraform-Cloud/page

This guide explains how to authenticate with Terraform Cloud using the web interface, CLI, and API, along with token types and security policies.

Terraform Cloud requires secure authentication for all users and automation workflows. In this guide, you’ll learn how to authenticate with Terraform Cloud using:

* Web interface
* Terraform CLI
* Terraform Cloud API

We’ll also review the three types of API tokens and organizational policies for enforcing security.

***

## Web Interface

A Terraform Cloud account gives you full access to the web UI. After logging in:

1. Select your Organization.
2. Navigate to **Workspaces** to view or manage configurations.
3. Use the **Settings** menu to configure access controls and policies.

Terraform Cloud’s web UI provides an intuitive way to manage infrastructure without installing additional tools.

***

## Command Line Interface (CLI)

Authenticate your local Terraform CLI to Terraform Cloud or Enterprise by generating and storing an API token.

```bash theme={null}
