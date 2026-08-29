# aws_instance.web:
resource "aws_instance" "web" {
  ami                                 = "ami-05efc83cb5512477c"
  arn                                 = "arn:aws:ec2:us-east-2:603991114860:instance/i-07289d6c1b924df1c"
  associate_public_ip_address         = false
  availability_zone                   = "us-east-2a"
  ebs_optimized                       = false
  get_password_data                   = false
  id                                  = "i-07289d6c1b924df1c"
  instance_initiated_shutdown_behavior = "stop"
  private_dns                         = "ip-10-0-5-245.us-east-2.compute.internal"
  private_ip                          = "10.0.5.245"
  public_dns                          = null
  public_ip                           = null
  region                              = "us-east-2"
  subnet_id                           = "subnet-0d0fdf0bdf3680113"
  tags                                = {
    "Environment" = "development"
    "Name"        = "web-server"
  }
}
```

Note: For large states this output can be verbose. When possible, scope your inspection to a specific resource address to reduce noise.

## 3. Inspect a single resource from state

To view only one resource's recorded attributes, run `terraform state show` with a resource address printed by `terraform state list`. For example, inspect the EC2 instance:

```bash theme={null}
$ terraform state show aws_instance.web
ami                                       = "ami-05efc83cb5512477c"
arn                                       = "arn:aws:ec2:us-east-2:603991114860:instance/i-07289d6c1b924df1c"
associate_public_ip_address               = false
availability_zone                         = "us-east-2a"
ebs_optimized                             = false
get_password_data                         = false
id                                        = "i-07289d6c1b924df1c"
instance_initiated_shutdown_behavior      = "stop"
placement_partition_number                = 0
primary_network_interface_id              = "eni-021f0bd1d36d8a756"
private_dns                               = "ip-10-0-5-245.us-east-2.compute.internal"
private_ip                                = "10.0.5.245"
public_dns                                = null
public_ip                                 = null
region                                    = "us-east-2"
secondary_private_ips                     = []
security_groups                           = []
source_dest_check                         = true
subnet_id                                 = "subnet-0d0fdf0bdf3680113"
tags                                      = {
  "Environment" = "development"
  "Name"        = "web-server"
}
vpc_security_group_ids                    = [
  "sg-0a6bf794da82ceca4",
]
```

This output shows concrete values (IDs, networking details, tags) exactly as stored in the Terraform state.

## 4. Example: inspect a subnet

A common workflow is to list resources and then inspect a specific subnet to verify IDs, tagging, and VPC association.

List resources:

```bash theme={null}
$ terraform state list
aws_instance.web
aws_subnet.private
aws_subnet.public
aws_vpc.main
$
```

Then inspect the private subnet:

```bash theme={null}
$ terraform state show aws_subnet.private
id                                  = "subnet-0d0fdf0bdf3680113"
ipv6_cidr_block                      = null
ipv6_cidr_block_association_id       = null
ipv6_native                          = false
map_customer_owned_ip_on_launch      = false
map_public_ip_on_launch              = false
outpost_arn                          = null
owner_id                             = "603991114860"
private_dns_hostname_type_on_launch  = "ip-name"
region                               = "us-east-2"
tags                                 = {
  "Environment" = "development"
  "Name"        = "main-subnet"
}
vpc_id                               = "vpc-0e419xxxxxxx"
```

This reveals the subnet ID, owner, tagging, region, and its associated VPC.

> **warning** Avoid editing the state file manually. If you need to adjust state (move, remove, or import resources), use Terraform state subcommands like `terraform state mv`, `terraform state rm`, or `terraform import` to keep state consistent and avoid corruption.

## Summary

* Use `terraform state list` to enumerate resource addresses present in the state.
* Use `terraform state show <address>` to inspect a single resource’s recorded attributes.
* Use `terraform show` to produce a full, human-readable dump of the entire state or a saved plan.
* Prefer Terraform state subcommands for state modifications; do not edit state files by hand.

## Links and references

* [Terraform State Commands — HashiCorp Documentation](https://www.terraform.io/cli/commands/state)
* [terraform show — Terraform CLI](https://www.terraform.io/cli/commands/show)
* [State management and backends — Terraform Docs](https://www.terraform.io/docs/state/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/2470872e-2566-4903-992b-b9fedc8c5739/lesson/19d563ce-7667-4c81-acdf-f5ff1321083d)


# Demo Migrate Your State to a Remote State Configuration

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Understading-and-Managing-Terraform-State/Demo-Migrate-Your-State-to-a-Remote-State-Configuration/page

Guide to migrating Terraform state between local files and an S3 remote backend, including configuration, migration commands, and optional DynamoDB state locking

This guide shows how to migrate an existing local Terraform state to a remote backend (Amazon S3 in this example) and how to move it back to local when needed. The steps below assume you already have a working Terraform configuration and are currently using a local `terraform.tfstate` file.

## Example resources

Here is a minimal Terraform configuration that creates a VPC and a subnet. This is the kind of configuration whose state you might be managing locally:

```hcl theme={null}
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "dev-main-vpc"
    Environment = "development"
  }
}

resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id
}
```

## Configure the S3 backend

To switch to an S3 remote backend, add a `terraform` block to your configuration (for example in `backend.tf` or `main.tf`) that references the S3 backend and the target bucket/key:

```hcl theme={null}
terraform {
  backend "s3" {
    bucket       = "krausen-terraform-state-bucket"
    key          = "prd/terraform.tfstate"
    region       = "us-east-2"
    dynamodb_table = "terraform-locks"
  }
}
```

* `bucket` — the S3 bucket to store the state file
* `key` — path/object name inside the bucket (e.g. `prd/terraform.tfstate`)
* `region` — AWS region containing the bucket
* `dynamodb_table` — optional DynamoDB table name to enable state locking

For more details, see the Terraform backend documentation: [Backends](https://developer.hashicorp.com/terraform/language/settings/backends) and the S3 backend guide: [S3 Backend](https://developer.hashicorp.com/terraform/language/settings/backends/s3).

> **lightbulb** To enable safe concurrent operations, create a DynamoDB table and reference it via `dynamodb_table`. This ensures Terraform can lock state while applying changes to prevent concurrent modifications.

## Migrate local state to S3

1. Save the backend configuration in your repo (for example `backend.tf`).
2. Initialize the working directory and migrate the state with the `-migrate-state` flag:

```bash theme={null}
terraform init -migrate-state
```

Terraform will detect a pre-existing local state and prompt whether to copy it to the newly configured backend. The prompt looks like:

```bash theme={null}
Initializing the backend...
Do you want to copy existing state to the new backend?
Pre-existing state was found while migrating the previous "local" backend to the newly configured "s3" backend. No existing state was found in the newly configured "s3" backend. Do you want to copy this state to the new "s3" backend? Enter "yes" to copy and "no" to start with an empty state.
Enter a value:
```

> **lightbulb** Type `yes` to copy your current (local) state to the S3 backend so Terraform continues managing the same resources remotely. Type `no` to start with an empty state in the remote backend.

After you answer `yes`, Terraform will configure the backend and upload the state file to the specified S3 bucket and key. You can verify the state object appears in the S3 console at `bucket` → `key`.

For example, after a successful migration you will see the `prd/terraform.tfstate` object in the S3 bucket:

<Frame>
  <img alt="The image shows an Amazon S3 console interface displaying a bucket named &#x22;krausen-terraform-state-bucket&#x22; in the &#x22;prd&#x22; directory, containing a single object named &#x22;terraform.tfstate&#x22; of type &#x22;tfstate,&#x22; last modified on February 15, 2026, with a size of 11.4 KB." />
</Frame>

## Move state back to local

If you later decide to revert to a local backend:

1. Remove or comment out the S3 backend block from your Terraform configuration. For example:

```hcl theme={null}
// terraform {
// //  backend "s3" {
// //    bucket       = "krausen-terraform-state-bucket"
// //    key          = "prd/terraform.tfstate"
// //    region       = "us-east-2"
// //    dynamodb_table = "terraform-locks"
// //  }
// }
```

2. Re-run initialization with migration enabled:

```bash theme={null}
terraform init -migrate-state
```

3. When prompted, answer `yes` to copy the state from S3 back to your local `terraform.tfstate`. Terraform will migrate the remote state back into the local backend and populate the local state file.

## Example of a migrated state file (top)

A minimal example of the top of a migrated state file looks like this:

```json theme={null}
{
  "version": 4,
  "terraform_version": "0.12.2",
  "serial": 1,
  "lineage": "d010f298-6128-653c-2eca-d54d0e33594d",
  "outputs": {},
  "resources": []
}
```

## Quick reference

| Action                     | Command / file                                           | Notes                                                                |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------- |
| Add S3 backend             | Add `terraform { backend "s3" { ... } }` to `backend.tf` | Configure `bucket`, `key`, `region`, and optionally `dynamodb_table` |
| Initialize & migrate to S3 | `terraform init -migrate-state`                          | Answer `yes` to copy local state to S3                               |
| Remove S3 backend          | Comment/remove `terraform { backend "s3" { ... } }`      | Prepare to migrate state back to local                               |
| Migrate back to local      | `terraform init -migrate-state`                          | Answer `yes` to copy S3 state to local `terraform.tfstate`           |

## Links and references

* [Terraform Backends](https://developer.hashicorp.com/terraform/language/settings/backends)
* [Terraform S3 Backend](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
* [State Locking](https://developer.hashicorp.com/terraform/language/state/locking)
* [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

That's it — migrating between local and remote backends is straightforward: add or remove the backend configuration and use `terraform init -migrate-state` to copy the state to the target backend.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/2470872e-2566-4903-992b-b9fedc8c5739/lesson/43f42492-4cd5-4b42-8ddd-a01363cf60ea)
