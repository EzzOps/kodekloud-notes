# Aliases

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Terraform-Provider-Basics/Aliases/page

This article explains how to use provider aliases in Terraform for managing resources across multiple AWS regions.

In this lesson, we delve into using provider aliases in Terraform to manage resources across multiple regions. Previously, we covered specifying provider versions using version constraints. Now, we will see how to provision resources in different AWS regions by configuring multiple instances of the same provider.

Consider the following scenario: you have a simple Terraform configuration with two resource blocks. The first block creates an AWS EC2 key pair in the US East 1 region, while the second block is intended to create a key pair in the CA Central 1 region. By default, if you only define one provider block (e.g., for the US East 1 region), both resource blocks would be provisioned in that same region.

> **lightbulb** Without any modifications, Terraform uses the default provider configuration for all resources. This means that if you don't specify otherwise, all resources will be created in the defined default region.

To create a resource in the CA Central 1 region using an aliased provider configuration, you need to define a second provider block with the appropriate region and an alias. Below is an example of how to set up the providers and resources:

```hcl theme={null}
resource "aws_key_pair" "alpha" {
  key_name   = "alpha"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...alpha@a-server"
}

resource "aws_key_pair" "beta" {
  key_name   = "beta"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQAB"
}

provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  region = "ca-central-1"
  alias  = "central"
}
```

Notice the alias "central" in the second provider block. To ensure that the "beta" resource is created in the CA Central region, add a `provider` argument within its configuration that references the aliased provider using the syntax: `provider_name.alias`. For instance:

```hcl theme={null}
resource "aws_key_pair" "beta" {
  provider   = aws.central
  key_name   = "beta"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQAB"
}
```

> **lightbulb** By specifying the `provider = aws.central` argument in the "beta" resource block, Terraform knows to use the aliased provider configured for the CA Central 1 region, while resources without a provider argument use the default provider (US East 1).

After running `terraform apply`, Terraform provisions the resources as specified:

* The key pair "alpha" is created in the US East 1 region.
* The key pair "beta" is created in the CA Central 1 region using the aliased provider.

To view the details of the provisioned resources, execute:

```plaintext theme={null}
$ terraform show
