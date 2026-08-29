# Demo Lifecycle Rules

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/Demo-Lifecycle-Rules/page

This hands-on lesson covers OpenTofu lifecycle rules, including resource dependencies, forced replacements, and destruction control using lifecycle blocks.

Welcome to this hands-on lesson covering OpenTofu lifecycle rules. You’ll learn how OpenTofu determines creation order through resource dependencies, how changing certain arguments forces resource replacement, and how to control destruction using lifecycle blocks.

## 1. Initial Setup for OpenTofu Resources

In the `root/opentofu-projects/project-mysterio` directory, your `main.tf` already defines two resources:

```hcl theme={null}
resource "local_file" "file" {
  filename        = var.filename
  file_permission = var.permission
  content         = random_string.string.id
}

resource "random_string" "string" {
  length  = var.length
  keepers = {
    length = var.length
  }
}
```

Initialize and apply:

```bash theme={null}
cd ~/opentofu-projects/project-mysterio
tofu init

tofu plan
tofu apply
