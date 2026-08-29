# Demo Detecting State Drift with Refresh Only Mode

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Understading-and-Managing-Terraform-State/Demo-Detecting-State-Drift-with-Refresh-Only-Mode/page

Shows how to detect and handle Terraform state drift using refresh-only plans, choose to enforce configuration or accept provider changes, and update code to keep resources in sync.

In this lesson we show how to detect and handle state drift with the Terraform CLI. You'll learn how to:

* Detect provider-side changes (drift) using `terraform plan -refresh-only`
* Choose whether to enforce configuration or accept external changes into state
* Update Terraform configuration to keep code and real-world resources in sync

## Example Terraform configuration

Below is a minimal Terraform configuration that creates an AWS VPC, a subnet, and an EC2 instance used as a web server:

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

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private.id
  tags = {
    Name        = "web-server"
    Environment = "development"
  }
}
```

> **lightbulb** This snippet omits the `cidr_block` on `aws_subnet` for brevity. In production, `aws_subnet` requires a valid `cidr_block` and usually an `availability_zone`. Always specify those values in real deployments.

Apply the configuration to create the resources:

```bash theme={null}
terraform apply -auto-approve
```

Example (summarized) apply output:

```plaintext theme={null}
Plan: 4 to add, 0 to change, 0 to destroy.
aws_vpc.main: Creating...
...
aws_subnet.public: Creation complete after 11s [id=subnet-09d564c1e1609a06f]
aws_instance.web: Creation complete after 13s [id=i-0c4192b0347156b5c]
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
```

Confirm the instance in the AWS Console — tags should match the configuration (Name = web-server, Environment = development).

<Frame>
  <img alt="The image shows an AWS EC2 management console with a &#x22;web-server&#x22; instance running. The instance, identified by ID i-0c4192b0347156b5c, is of type t2.small and is in an initializing state." />
</Frame>

Everything matches the Terraform configuration at this point.

## Simulate an out-of-band change

Sometimes changes are made directly in the cloud provider (manually or by another team). For this demo:

1. Stop the EC2 instance in the AWS Console.
2. Change its instance type from `t2.small` to `t3.small`.
3. Add a new tag: `Team = dev-app-01`.
4. Start the instance again.

Screenshots of those steps:

<Frame>
  <img alt="The image shows an AWS EC2 dashboard, displaying details of a running instance labeled &#x22;web-server&#x22; with instance ID &#x22;i-0c4192b0347156b5c.&#x22; The instance is of type &#x22;t2.small&#x22; and is in the &#x22;us-east-2a&#x22; availability zone." />
</Frame>

Stop the instance to perform instance-type modifications.

<Frame>
  <img alt="The image shows an AWS EC2 console with a single stopped instance named &#x22;web-server,&#x22; along with various options under the &#x22;Actions&#x22; menu." />
</Frame>

Select the new instance type (`t3.small`) and save.

<Frame>
  <img alt="The image shows an AWS EC2 dashboard where a user is selecting a new instance type, changing from &#x22;t2.small&#x22; to &#x22;t3.small,&#x22; with instance type comparison details shown below." />
</Frame>

After you restart the instance, the provider now reflects state that differs from your Terraform configuration.

## Detecting drift with Terraform

To detect changes made outside of Terraform, run a refresh-only plan. This command refreshes resource attributes from the provider and reports differences between the refreshed state and the configuration without proposing changes to infrastructure:

```bash theme={null}
terraform plan -refresh-only
```

Example summarized output after running `-refresh-only`:

```plaintext theme={null}
Note: Objects have changed outside of Terraform
Terraform detected the following changes made outside of Terraform since the last "terraform apply" which may have affected this plan:
