# Handling Providers

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Providers/Handling-Providers/page

Explains how Terraform discovers, downloads, versions, initializes, and reuses providers, plus using terraform init, provider sources, version locking, and registry best practices for reproducible workflows

In this lesson you'll learn how Terraform discovers, downloads, versions, initializes, and reuses providers across runs. Mastering this flow helps with reliable team workflows, reproducible CI runs, and faster troubleshooting when provider plugins cause issues.

Start with the core command:

```bash theme={null}
$ terraform init
```

terraform init prepares the working directory — it initializes the backend, locates required providers from your configuration, and downloads provider plugins into the project. Importantly, terraform init does not change infrastructure; it sets up the environment so subsequent commands like terraform plan and terraform apply can run.

Example configuration referencing multiple providers:

```hcl theme={null}
