# Mutable vs Immutable Infrastructure

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Working-with-Terraform/Mutable-vs-Immutable-Infrastructure/page

This article explains the differences between mutable and immutable infrastructure, focusing on their implications for Infrastructure as Code and tools like Terraform.

In this lesson, we dive into the fundamental differences between mutable and immutable infrastructure. Understanding these differences is essential when implementing Infrastructure as Code (IaC) and using tools like [Terraform](https://www.terraform.io/).

Terraform handles resource updates—such as modifying the permissions of a local file—by destroying an existing resource and then re-creating it with the updated settings. Consider the following example:

```hcl theme={null}
resource "local_file" "pet" {
  filename        = "/root/pets.txt"
  content         = "We love pets!"
  file_permission = "0700"
}
```

When you run Terraform to apply this configuration, the output might look like:

```bash theme={null}
$ terraform apply
