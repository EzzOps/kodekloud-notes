# Output Variables

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Output-Variables/page

This article explains how to define, view, and use output variables in OpenTofu configurations.

Output variables make it easy to expose values from your OpenTofu configuration—such as resource attributes—to users, scripts, or other tools. In this guide, you’ll learn how to define, view, and leverage output variables effectively.

## Table of Contents

* [Defining an Output Variable](#defining-an-output-variable)
* [Generic Output Syntax](#generic-output-syntax)
* [Output Block Arguments](#output-block-arguments)
* [Complete Example](#complete-example)
* [Viewing Outputs](#viewing-outputs)
* [Use Cases](#use-cases)
* [Links and References](#links-and-references)

***

## Defining an Output Variable

Use the `output` block with a unique name and the `value` argument set to the expression you want to expose. You can also include optional arguments like `description` and `sensitive`:

```hcl theme={null}
output "pub_ip" {
  value       = aws_instance.cerberus.public_ip
  description = "The public IPv4 address of the EC2 instance"
}
```

> **lightbulb** Output names must be unique within a module. Use descriptive names to make them easy to reference in other modules or scripts.

***

## Generic Output Syntax

Below is the general form of an output block in OpenTofu:

```hcl theme={null}
output "<NAME>" {
  value       = <EXPRESSION>
  description = "<DESCRIPTION>"      # optional
  sensitive   = true | false        # optional
}
```

* **NAME**: The identifier for this output.
* **EXPRESSION**: Any valid expression or reference, such as `aws_instance.foo.id`.
* **description**: A human-readable summary (optional).
* **sensitive**: When set to `true`, the value is omitted from CLI output (optional).

***

## Output Block Arguments

| Argument    | Description                                              | Required |
| ----------- | -------------------------------------------------------- | -------- |
| value       | Expression or reference whose result you want to expose. | Yes      |
| description | A short human-readable explanation.                      | No       |
| sensitive   | Hides the value in CLI output when set to `true`.        | No       |

> **triangle-alert** Mark any output containing secrets or credentials as `sensitive = true` to prevent leaking them in logs or console output.

***

## Complete Example

This minimal configuration creates an EC2 instance and then outputs its public IPv4 address:

```hcl theme={null}
resource "aws_instance" "cerberus" {
  ami           = var.ami
  instance_type = var.instance_type
}

output "pub_ip" {
  value       = aws_instance.cerberus.public_ip
  description = "The public IPv4 address of the EC2 instance"
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}

variable "region" {
  default = "eu-west-2"
}
```

***

## Viewing Outputs

After running `tofu apply`, OpenTofu automatically displays all configured outputs:

```bash theme={null}
$ tofu apply
...
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
pub_ip = 54.214.145.69
```

You can also list or fetch outputs at any time:

```bash theme={null}
