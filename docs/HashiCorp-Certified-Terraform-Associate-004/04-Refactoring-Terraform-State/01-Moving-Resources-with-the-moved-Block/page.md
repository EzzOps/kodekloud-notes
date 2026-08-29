# Moving Resources with the moved Block

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Refactoring-Terraform-State/Moving-Resources-with-the-moved-Block/page

Explains Terraform's moved block for safely refactoring resource addresses to rename or relocate resources into modules by updating state without recreating or destroying infrastructure.

In this lesson we cover the Terraform `moved` block — a safe, declarative way to refactor resource addresses in your configuration without modifying the underlying infrastructure or manually editing the state file. Use this when you want to rename resources or move them into modules while keeping the existing cloud objects intact.

Why you need it

* During early development you might give resources short or ambiguous names (for example `vpc` and `vpc1`). As the project grows you’ll want clearer names (for example `sbx_vpc` and `test_vpc`).
* Simply renaming a resource in HCL makes Terraform think the old address was removed and a new one created. The result: Terraform plans to destroy the existing resource and create a new one — potentially causing downtime or data loss.

Initial example — two VPCs in a simple configuration:

```hcl theme={null}
resource "aws_vpc" "vpc" {
  cidr_block = var.sandbox_vpc_cidr
  tags = {
    Name        = var.sbx_vpc_name
    Environment = "sandbox_network"
    Terraform   = "true"
  }
}

resource "aws_vpc" "vpc1" {
  cidr_block = var.test_vpc_cidr
  tags = {
    Name        = var.test_vpc
    Environment = "testing_network"
    Terraform   = "true"
  }
}
```

If you rename `aws_vpc.vpc` to `aws_vpc.sbx_vpc` directly in your HCL, Terraform will show a plan that destroys the old address and creates a new one:

```hcl theme={null}
resource "aws_vpc" "sbx_vpc" {
  cidr_block = var.sandbox_vpc_cidr
  tags = {
    Name        = var.sbx_vpc_name
    Environment = "sandbox_network"
    Terraform   = "true"
  }
}
```

Sample plan output (illustrative):

```bash theme={null}
$ terraform plan
Terraform will perform the following actions:
