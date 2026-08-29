# Ephemeral resource that asks Vault's AWS secrets engine to generate temporary credentials.
# This resource is not written to state and returns credentials in memory for the current run.
ephemeral "vault_aws_access_credentials" "creds" {
  backend = vault_aws_secret_backend.aws.path
  role    = vault_aws_secret_backend_role.example.name
  type    = "creds"
  region  = "us-east-1"
}

# AWS provider configured to use the temporary credentials returned by the ephemeral resource.
provider "aws" {
  region     = "us-east-1"
  access_key = ephemeral.vault_aws_access_credentials.creds.access_key
  secret_key = ephemeral.vault_aws_access_credentials.creds.secret_key
}

# Example cloud resource provisioned using the temporary credentials.
resource "aws_instance" "main" {
  ami           = "ami-0c55b159cbfafe1f0" # replace with a valid AMI for your account/region
  instance_type = "t3.micro"
  # ... other config ...
}
```

How the lifecycle works

* On `terraform plan` or `terraform apply`, Terraform authenticates to Vault using the configured auth method.
* Terraform requests dynamic credentials from the relevant Vault secrets engine (e.g., AWS secrets engine).
* Vault vends temporary credentials and returns them to Terraform; Terraform uses them for provider authentication during the run.
* Credentials have a short TTL (minutes or tens of minutes). When the TTL expires Vault revokes the backend credential (in AWS, Azure, GCP, etc.), preventing later misuse even if the credentials were exposed.

Important properties of this pattern

* Credentials are generated on demand and are short-lived (TTL-based).
* Roles in Vault can scope credentials to least privilege.
* Long-lived cloud credentials remain inside Vault; users do not hold platform secrets.
* When using ephemeral resources or provider mechanisms that avoid persisting secrets, credentials can be kept out of Terraform state — they exist only in memory for the run.
* Reduces credential sprawl, simplifies rotation/revocation, and reduces the attack surface.

> **lightbulb** Not all Terraform providers expose ephemeral resource types. Check the [provider documentation](https://registry.terraform.io/browse/providers) to confirm whether ephemeral resources or equivalent data sources are available and how to reference them.

> **warning** Avoid persisting dynamic credentials to state files or logs. If a provider does not support ephemeral constructs, carefully review how credentials are surfaced and ensure they are not saved to persistent state or exposed in CI logs.

Quick reference: components and responsibilities

| Component                | Responsibility                                                                    | Example or note                                                                      |
| ------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Vault                    | Centralized secrets management, dynamic credential generation, policy enforcement | See Vault docs: [https://www.vaultproject.io/docs](https://www.vaultproject.io/docs) |
| Vault secrets engine     | Generates backend credentials (AWS, Azure, GCP, etc.)                             | Configure the appropriate secrets engine for your cloud                              |
| Vault auth method        | Authenticates Terraform to Vault (Kubernetes, AWS, Azure, etc.)                   | Choose based on where Terraform runs                                                 |
| Terraform Vault provider | Retrieves credentials from Vault                                                  | `provider "vault" { ... }`                                                           |
| Ephemeral/data construct | Returns temporary credentials to Terraform without persisting to state            | `data "vault_aws_access_credentials" ...` or provider-specific ephemeral block       |
| Cloud provider           | Uses temporary credentials for API calls                                          | `provider "aws" { access_key = ... secret_key = ... }`                               |

Why use this pattern?

* Centralized secrets management and policy control via Vault.
* Reduced attack surface because credentials are short-lived and revocable.
* No local long-lived credential storage for developers or CI runners.
* Easier to change access controls by updating Vault roles/policies without redistributing credentials.

What you need to know for the Terraform Associate exam

Focus on the conceptual pattern:

* Vault can generate dynamic, short-lived credentials for cloud platforms.
* Terraform uses the Vault provider to retrieve those credentials.
* Combining Vault with ephemeral resources or provider-specific mechanisms avoids writing credentials to state.
* You do not need to be an expert in Vault; understand the integration and security benefits.

Conclusion

The dynamic-credentials pattern—Vault generating temporary credentials on demand, Terraform retrieving them via the Vault provider (and ephemeral resources where available), and cloud providers using those credentials to provision infrastructure—is a mature approach to secrets management. It complements other best practices (sensitive variables, write-only arguments, encrypted state, avoiding secrets in Git). Each layer reduces risk; use them together to strengthen your security posture.

References and further reading

* HashiCorp Vault documentation: [https://www.vaultproject.io/docs](https://www.vaultproject.io/docs)
* Terraform Registry (providers): [https://registry.terraform.io/browse/providers](https://registry.terraform.io/browse/providers)
* Provider-specific Vault integrations (search the registry for `vault_*` data sources/providers)
* [Terraform Associate exam course (reference)](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified)

And that's it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/937ac82e-4dee-466c-92aa-9a731752424e/lesson/85e1212c-a4cb-4128-a9af-21d0335e7ea6)


# Demo Writing and Using Your Own Modules

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Modules/Demo-Writing-and-Using-Your-Own-Modules/page

Guide to creating reusable local Terraform modules and composing them to provision AWS VPC subnet and EC2 resources while managing inputs outputs and module wiring

Welcome. In this lesson you'll learn how to create local Terraform modules and compose them in a parent configuration to provision AWS resources. The focus is on module structure, inputs/outputs, and wiring outputs from one module into another so you can reuse infrastructure code across projects and environments.

## What you'll build

* A parent Terraform configuration that calls local modules.
* Three local modules: `vpc`, `subnet`, and `ec2`.
* Data flow that passes outputs from one module into another (e.g., VPC ID -> Subnet -> EC2).

## Directory and file layout

Create a top-level Terraform directory (this is the parent module). Inside it add common files and a `modules` subdirectory with three child modules.

| Location           | Recommended files                                       |
| ------------------ | ------------------------------------------------------- |
| Top-level (parent) | `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf` |
| `modules/vpc`      | `main.tf`, `variables.tf`, `outputs.tf`                 |
| `modules/subnet`   | `main.tf`, `variables.tf`, `outputs.tf`                 |
| `modules/ec2`      | `main.tf`, `variables.tf`, `outputs.tf`                 |

Below are cleaned-up module implementations and the parent configuration examples. Keep these modules focused and parameterized so they are reusable across accounts and environments.

***

## VPC module

This module creates a VPC and exposes its ID as an output.

modules/vpc/main.tf

```hcl theme={null}
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = var.vpc_name
  }
}
```

modules/vpc/variables.tf

```hcl theme={null}
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = "my-cool-vpc-for-modules"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}
```

modules/vpc/outputs.tf

```hcl theme={null}
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.vpc.id
}
```

***

## Subnet module

This module provisions a subnet and the supporting network resources: an Internet Gateway, a route table, and a route table association. It accepts a `vpc_id` input and returns the `subnet_id`.

modules/subnet/main.tf

```hcl theme={null}
resource "aws_subnet" "subnet" {
  vpc_id            = var.vpc_id
  cidr_block        = var.subnet_cidr
  availability_zone = var.availability_zone

  tags = {
    Name = var.subnet_name
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = var.vpc_id

  tags = {
    Name = "${var.subnet_name}-igw"
  }
}

resource "aws_route_table" "rt" {
  vpc_id = var.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.subnet_name}-rt"
  }
}

resource "aws_route_table_association" "rta" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.rt.id
}
```

<Frame>
  <img alt="The image shows a code editor with a Terraform script being edited, displaying an autocomplete suggestion for resource configuration. The explorer pane on the left shows a directory structure with Terraform files." />
</Frame>

modules/subnet/variables.tf

```hcl theme={null}
variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet_name" {
  description = "Name of the subnet"
  type        = string
  default     = "demo-subnet"
}

variable "availability_zone" {
  description = "Availability zone for the subnet"
  type        = string
  default     = "us-east-1a"
}
```

modules/subnet/outputs.tf

```hcl theme={null}
output "subnet_id" {
  description = "The ID of the subnet"
  value       = aws_subnet.subnet.id
}
```

***

## EC2 module

This module creates a security group and an EC2 instance. Inputs include VPC and subnet IDs plus AMI, instance type, and an instance name. Outputs include the instance ID and public IP.

modules/ec2/main.tf

```hcl theme={null}
resource "aws_security_group" "sg" {
  name        = "allow-ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow-ssh"
  }
}

resource "aws_instance" "instance" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.sg.id]
  associate_public_ip_address = true

  tags = {
    Name = var.instance_name
  }
}
```

modules/ec2/variables.tf

```hcl theme={null}
variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet"
  type        = string
}

variable "ami_id" {
  description = "The AMI ID to use for the instance"
  type        = string
  default     = "ami-0c55b159cbfafe1f0" # example Amazon Linux 2 AMI in us-east-1
}

variable "instance_type" {
  description = "The type of instance to start"
  type        = string
  default     = "t2.micro"
}

variable "instance_name" {
  description = "Name of the EC2 instance"
  type        = string
  default     = "my-instance"
}
```

modules/ec2/outputs.tf

```hcl theme={null}
output "instance_id" {
  description = "The ID of the instance"
  value       = aws_instance.instance.id
}

output "public_ip" {
  description = "The public IP address of the instance"
  value       = aws_instance.instance.public_ip
}
```

***

## Parent configuration

The parent module declares the AWS provider and calls the child modules. Note how we wire outputs into module inputs.

providers.tf (parent)

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}
```

main.tf (parent) — module blocks

```hcl theme={null}
module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
  vpc_name = "demo-vpc"
}

module "subnet_module" {
  source            = "./modules/subnet"
  vpc_id            = module.vpc.vpc_id
  subnet_cidr       = "10.0.1.0/24"
  subnet_name       = "demo-subnet"
  availability_zone = "us-east-1a"
}

module "prod-workload" {
  source        = "./modules/ec2"
  vpc_id        = module.vpc.vpc_id
  subnet_id     = module.subnet_module.subnet_id
  ami_id        = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  instance_name = "bryans-web-server"
}
```

***

## Tooling and basic workflow

After you add or change modules, follow this basic workflow.

1. Initialize the working directory (downloads providers and registers modules)

```bash theme={null}
$ terraform init
Initializing the backend...
Initializing modules...
- vpc in modules/vpc
- subnet_module in modules/subnet
- prod-workload in modules/ec2
Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws v5.89.0...
```

2. Format your files

```bash theme={null}
$ terraform fmt
```

3. Create and review a plan, then apply

```bash theme={null}
$ terraform plan
Plan: X to add, 0 to change, 0 to destroy.
```

Example of a planned resource created by a child module:

```plaintext theme={null}
