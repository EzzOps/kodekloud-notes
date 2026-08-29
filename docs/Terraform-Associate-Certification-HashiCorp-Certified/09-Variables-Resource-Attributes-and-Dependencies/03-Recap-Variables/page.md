# Recap Variables

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Variables-Resource-Attributes-and-Dependencies/Recap-Variables/page

This article recaps how variables work in Terraform and demonstrates their usage with practical examples for flexible and maintainable code.

In this article, we recap how variables work in Terraform and demonstrate their usage with practical examples. Instead of hard-coding values directly in your configuration, variables allow you to write more flexible, maintainable code. Although it is common practice to store variable definitions in a separate file named `variables.tf`, you can also declare them in the same file as your resources (e.g., `main.tf`).

***

## Hard-Coded Resource Definitions

Below is an example of defining resources using hard-coded values:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}

resource "random_pet" "my-pet" {
  prefix    = "Mrs"
  separator = "."
  length    = "1"
}
```

***

## Defining Variables in a Separate File

By defining variables in a separate file, you can avoid repetition and make your configuration easier to update. The following example demonstrates how to define corresponding variables in `variables.tf`:

```hcl theme={null}
variable "filename" {
  default = "/root/pets.txt"
}

variable "content" {
  default = "We love pets!"
}

variable "prefix" {
  default = "Mrs"
}

variable "separator" {
  default = "."
}

variable "length" {
  default = "1"
}
```

***

## Using Variables in Resource Configurations

By referencing variables in your resource configurations using the `var.` prefix, you can replace hard-coded values. This makes it easier to change values without having to update each resource block. See the example below:

```hcl theme={null}
