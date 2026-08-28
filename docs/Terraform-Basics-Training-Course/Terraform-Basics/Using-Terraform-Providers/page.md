# main.tf
resource "local_file" "pet" {
  filename = var.filename
  content  = var.content
}

resource "random_pet" "my-pet" {
  prefix    = var.prefix
  separator = var.separator
  length    = var.length
}

# variables.tf
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

After these changes, run the standard Terraform workflow:

1. Execute `terraform plan` to view the planned changes.
2. Execute `terraform apply` to deploy the resources with the variable values.

## Updating Variables

You can modify your infrastructure by simply updating the default values in `variables.tf`. For instance, to change the file content and adjust the length of the random pet's name, you might update the file as follows:

```hcl theme={null}
# main.tf
resource "local_file" "pet" {
  filename = var.filename
  content  = var.content
}

resource "random_pet" "my-pet" {
  prefix    = var.prefix
  separator = var.separator
  length    = var.length
}

# variables.tf
variable "filename" {
  default = "/root/pets.txt"
}

variable "content" {
  default = "My favorite pet is Mrs. Whiskers"
}

variable "prefix" {
  default = "Mrs"
}

variable "separator" {
  default = "."
}

variable "length" {
  default = "2"
}
```

Once you run `terraform apply` again, Terraform updates the resources accordingly—the file content will change, and the pet name will now consist of two parts following the prefix.

## Creating an EC2 Instance with Variables

Here's an additional example of using input variables to create an [EC2 instance](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) in AWS with Terraform. This configuration demonstrates the same variable usage pattern, even if some resource block parameters might seem unfamiliar:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = var.ami
  instance_type = var.instance_type
}

variable "ami" {
  default = "ami-0edab43b6fa892279"
}

variable "instance_type" {
  default = "t2.micro"
}
```

For further details on AWS resource management, keep an eye out for our upcoming in-depth coverage.

## Conclusion

Using input variables in Terraform improves code maintainability and allows for dynamic deployments. By defining variable defaults in a dedicated file and referencing them in your resource configurations, you can create more adaptable and scalable infrastructure deployments. Make sure to integrate these practices into your workflows to maximize the efficiency and flexibility of your Terraform projects.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/f88d4131-aec1-4d09-ba28-5846d4621761" />
</CardGroup>


# Using Terraform Providers

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Basics/Using-Terraform-Providers/page

This guide explains how Terraform providers enable resource management across platforms, covering initialization, provider tiers, and source addresses.

Learn how Terraform providers enable you to manage resources across various platforms. This guide explains how to initialize your working directory, understand provider tiers, and interpret provider source addresses—all key steps in leveraging Terraform's plugin-based architecture.

## Initializing Your Working Directory

After creating your Terraform configuration file, initialize your working directory by running the following command:

```bash theme={null}
terraform init
```

When executed in a directory with configuration files, Terraform downloads and installs the necessary provider plugins. These plugins allow Terraform to manage resources from major cloud providers like AWS, GCP, and Azure, as well as simpler providers such as the local provider for managing local file resources. Terraform's plugin-based architecture supports hundreds of infrastructure platforms, and the providers are distributed by HashiCorp via the [Terraform Registry](https://registry.terraform.io).

## Provider Tiers

Terraform providers are organized into three tiers based on ownership and maintenance:

| Provider Tier       | Description                                                                                                             | Examples                                  |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Official Providers  | Maintained by HashiCorp. They include major cloud providers and providers like the local provider used in our examples. | AWS, GCP, Azure, Local                    |
| Partner Providers   | Managed by third-party technology companies that have completed HashiCorp's partner provider process.                   | F5 Networks (BigIP), Heroku, DigitalOcean |
| Community Providers | Developed and maintained by individual contributors within the HashiCorp community.                                     | Various community-driven plugins          |

## Example: Terraform Initialization Output

When you run `terraform init`, Terraform displays the version of each provider plugin being installed. The following example shows the initialization process and output details:

```plaintext theme={null}
$ terraform init
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/local...
- Installing hashicorp/local v2.0.0...
- Installed hashicorp/local v2.0.0 (signed by HashiCorp)

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, we recommend adding version constraints in a required_providers block
in your configuration, with the constraint strings suggested below.

* hashicorp/local: version = "~> 2.0.0"

Terraform has been successfully initialized!
```

<Callout icon="lightbulb">
  The `terraform init` command is safe to run repeatedly. It only updates the local plugin installation without modifying your deployed infrastructure.
</Callout>

## Understanding Provider Source Addresses

The provider name, such as `hashicorp/local`, is the source address Terraform uses to locate and download the plugin from the registry. This identifier consists of:

* An organizational namespace (`hashicorp`)
* A provider name (`local`)

Optionally, you can include a hostname to indicate the location of the registry. If omitted, Terraform defaults to `registry.terraform.io`.

```bash theme={null}
hashicorp/local version = "~> 2.0.0"
```

<Frame>
  ![The image provides instructions for adding version constraints in Terraform configurations to prevent automatic upgrades, with a URL example highlighted.](https://kodekloud.com/kk-media/image/upload/v1752884190/notes-assets/images/Terraform-Basics-Training-Course-Using-Terraform-Providers/frame_200.jpg)
</Frame>

Since the local provider is hosted in the public Terraform Registry under the HashiCorp namespace, you can refer to it in either of the following ways:

* Full source address: `registry.terraform.io/hashicorp/local`
* Simplified: `hashicorp/local`

<Callout icon="triangle-alert">
  Without version constraints, Terraform installs the latest available version by default. Automatic updates may introduce breaking changes. Lock your configuration to a specific provider version to ensure stable and predictable deployments.
</Callout>

<Frame>
  ![The image shows a terminal output indicating the installation of the HashiCorp local provider version 2.0.0, with a recommendation to add version constraints.](https://kodekloud.com/kk-media/image/upload/v1752884192/notes-assets/images/Terraform-Basics-Training-Course-Using-Terraform-Providers/frame_240.jpg)
</Frame>

## Next Steps

To maintain stable deployments and avoid unexpected changes, consider adding version constraints to your provider configurations. This practice will be discussed in more detail later in this documentation.

For further reading, explore the [Terraform Documentation](https://www.terraform.io/docs) to enhance your infrastructure as code strategy and master Terraform providers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/687abdb6-01aa-4903-acca-808e752a4f88" />
</CardGroup>
