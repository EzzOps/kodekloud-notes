# Using Input Variables

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Basics/Using-Input-Variables/page

Terraform input variables enhance code reusability and flexibility by allowing parameterization of configurations for dynamic values during execution.

Terraform input variables enhance code reusability and flexibility by allowing you to parameterize your configurations. Instead of hard-coding values—such as the file name and content for a local file resource or the prefix, separator, and length for a random pet resource—you can pass dynamic values during execution. This approach is similar to using variables in scripting languages like Bash or PowerShell.

## Why Use Input Variables?

Hard-coding values limits the adaptability of your configuration. By leveraging input variables, you can easily update resource configurations without modifying multiple code sections. This not only improves maintenance but also supports better scaling practices.

<Callout icon="lightbulb">
  Using variables makes your configuration files more modular and easier to manage. Adjust values in a single file to propagate changes across your infrastructure.
</Callout>

## Traditional Hard-Coded Resources

Consider the following example where resource attributes are hard-coded:

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

## Parameterizing with Variables

To parameterize these values, create a configuration file named `variables.tf`. In this file, you define each variable using the `variable` keyword and can optionally assign a default value:

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

Once your variables are declared, update your `main.tf` file to reference these variables. You achieve this by prefixing the variable name with `var.`:

```hcl theme={null}
