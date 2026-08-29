# Variables Resource Attributes and Dependencies

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Variables-Resource-Attributes-and-Dependencies/Variables-Resource-Attributes-and-Dependencies/page

Learn to mark variables and outputs as sensitive in Terraform for secure handling of critical information like passwords and API keys.

In this lesson, you'll learn how to mark variables and outputs as sensitive in Terraform, ensuring secure handling of critical information such as passwords, API keys, and other secrets. Terraform provides built-in mechanisms to safeguard sensitive data, preventing accidental exposure in logs or terminal outputs.

![The image shows a HashiCorp Terraform interface for defining sensitive information, with options for passwords, API keys, and other data.](https://kodekloud.com/kk-media/image/upload/v1752884175/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Variables-Resource-Attributes-and-Dependencies/frame_30.jpg)

## Marking a Variable as Sensitive

Designating a variable as sensitive is straightforward. Simply include the `sensitive = true` attribute within its declaration. Consider the example below:

```hcl theme={null}
variable "ami" {
  default   = "ami-06178cf887597869c"
  sensitive = true
}

variable "instance_type" {
  default = "t3.micro"
}

variable "region" {
  default = "eu-west-2"
}

resource "aws_instance" "test-servers" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

With this configuration, Terraform treats the `ami` variable as sensitive. This causes Terraform to mask the actual value during both planning and apply phases, which prevents sensitive details from being displayed in logs or terminal outputs.

## Demonstrating Sensitive Handling in Terraform Plan

When you run a plan, Terraform automatically hides the sensitive value for the AMI. Here’s an example of what you might see:

```console theme={null}
> terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
 + create

Terraform will perform the following actions:
