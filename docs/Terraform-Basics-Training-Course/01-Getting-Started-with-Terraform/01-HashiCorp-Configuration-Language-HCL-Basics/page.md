# aws_instance.test-servers will be created
+ resource "aws_instance" "test_servers" {
  + ami                                  = (sensitive value)
  + arn                                  = (known after apply)
  + associate_public_ip_address          = (known after apply)
  + availability_zone                    = (known after apply)
  + cpu_core_count                       = (known after apply)
  + cpu_threads_per_core                 = (known after apply)
  + disable_api_termination              = (known after apply)
  + ebs_optimized                        = (known after apply)
  + get_password_data                    = false
  + host_id                              = (known after apply)
  + id                                   = (known after apply)
  + instance_initiated_shutdown_behavior = (known after apply)
  + instance_state                       = (known after apply)
}
```

This output confirms that the `ami` value is redacted, maintaining confidentiality by preventing accidental data leaks.

## Receiving Sensitive Inputs

If you leave a sensitive variable without a default value, Terraform prompts for the input during the plan or apply process. The input remains hidden as you type:

```hcl theme={null}
variable "ami" {
  type      = string
  sensitive = true
}
```

```console theme={null}
> terraform plan
var.ami
Enter a value: 
```

To streamline processes and avoid manual input each time, store the secret values in a separate `.tfvars` file and provide them via the `-var-file` parameter:

```console theme={null}
> terraform apply -var-file=secret.tfvars

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
 + create

Terraform will perform the following actions:

# aws_instance.test-servers will be created
+ resource "aws_instance" "test_servers" {
  + ami                                  = (sensitive value)
  + arn                                  = (known after apply)
  + associate_public_ip_address          = (known after apply)
  + availability_zone                    = (known after apply)
  + cpu_core_count                       = (known after apply)
  + cpu_threads_per_core                 = (known after apply)
  + disable_api_termination              = (known after apply)
  + ebs_optimized                        = (known after apply)
  + get_password_data                    = false
  + host_id                              = (known after apply)
  + id                                   = (known after apply)
  + instance_initiated_shutdown_behavior = (known after apply)
  + instance_state                       = (known after apply)
  + instance_type                        = "t3.micro"
  + ipv6_address_count                   = (known after apply)
}
```

> **lightbulb** Storing sensitive values in a dedicated `.tfvars` file and using the `-var-file` option significantly reduces the risk of accidentally exposing secret information.

Alternatively, you can export sensitive values as environment variables. This approach is especially useful in CI/CD pipelines, where Terraform can securely access sensitive data without manual input.

## Handling Errors When Exposing Sensitive Outputs

Terraform prevents sensitive information from being exposed in outputs. If you try to output sensitive details without explicitly marking them as such, Terraform will throw an error. For instance, the following output configuration attempts to expose the sensitive `ami` value:

```hcl theme={null}
output "info_string" {
  description = "Information regarding provisioned resources"
  value       = "AMI=${var.ami} Instance Type=${var.instance_type}"
}
```

When you run the apply command, Terraform redacts the sensitive output:

```console theme={null}
> terraform apply
aws_instance.test-servers: Refreshing state... [id=i-a15264c034b27b3d3]

Changes to Outputs:
  + info_string = (sensitive value)

You can apply this plan to save these new output values to the Terraform state, without changing any real infrastructure.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

Enter a value: yes

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:
info_string = <sensitive>
```

To view the actual value of a sensitive output variable, use the `terraform output` command followed by the variable name:

```bash theme={null}
terraform output info_string
"AMI=ami-06178cf087598769c; Instance Type=t3.micro"
```

> **triangle-alert** Remember that even if sensitive attributes are masked in terminal outputs, they are stored as plain text in the Terraform state file. Ensure that you manage access to your state file securely and consider using encryption to protect it.

That's it for this lesson on marking variables as sensitive in Terraform. Continue exploring Terraform best practices to further enhance your infrastructure security and efficiency.

![The image shows a selection interface for securing a state file, with options: "Sensitive attributes hidden," "Plain text in state file" (highlighted), and "Secure state file."](https://kodekloud.com/kk-media/image/upload/v1752884177/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Variables-Resource-Attributes-and-Dependencies/frame_200.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/cca81ade-f05a-42b2-af56-1926cade6582/lesson/fdb35cae-60fd-43c6-a997-b981b359efbd)


# HashiCorp Configuration Language HCL Basics

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Getting-Started-with-Terraform/HashiCorp-Configuration-Language-HCL-Basics/page

Learn the fundamentals of HCL, including syntax, creating resources, and essential Terraform commands for managing infrastructure configurations.

In this article, you'll learn the fundamentals of HCL—the language used to define infrastructure with Terraform. We demonstrate HCL syntax, create a simple local file resource, and walk through essential Terraform commands to initialize, plan, and apply configurations.

## Understanding HCL Syntax

HCL files consist of blocks and arguments. Blocks are defined using curly braces and contain key-value pair arguments that represent configuration data. In Terraform, each block describes a specific aspect of your infrastructure and lists the resources you wish to create. For instance, you might want to create a file on the local system where Terraform is installed.

First, create a directory for your configuration file in the `/root` directory:

```bash theme={null}
$ mkdir /root/terraform-local-file
$ cd /root/terraform-local-file
```

Within this directory, create a configuration file (e.g., `local.tf`) and define a generic block structure:

```hcl theme={null}
<block> <parameters> {
    key1 = value1
    key2 = value2
}
```

## Creating a Local File Resource

Next, define a resource block in `local.tf` to create a local file. Inside the block, specify the file name and content using block arguments:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

### Breaking Down the Configuration

1. **Block Identification**\
   The block starts with the `resource` keyword and is identified by curly braces. It consists of three parts:

   * **Resource Type:**\
     `local_file` indicates that the local provider is used.

   * **Resource Name:**\
     The logical name `pet` uniquely identifies this resource.

   * **Block Arguments:**\
     These key-value pairs specify resource parameters. For example:

     * `filename` sets the absolute path `/root/pets.txt` where the file is created.
     * `content` provides the text content for the file.

2. **Resource Type Requirements**\
   The `local_file` resource requires the arguments `filename` and `content`. When working with other providers such as AWS, Azure, or GCP, different resource types may require a different set of arguments. Consult Terraform's documentation for details on the necessary arguments for each resource type.

Below are additional examples for other providers:

### AWS EC2 Instance Example

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0c2f25c1f66a1ff4d"
  instance_type = "t2.micro"
}
```

### AWS S3 Bucket Example

```hcl theme={null}
resource "aws_s3_bucket" "data" {
  bucket = "webserver-bucket-org-2207"
  acl    = "private"
}
```

## Terraform Workflow

A typical Terraform workflow involves the following steps:

1. **Write the Configuration File:**\
   Create and edit your Terraform configuration file (e.g., `local.tf`).

2. **Initialize the Working Directory:**\
   This step checks your configuration file and downloads the necessary provider plugins.

   ```bash theme={null}
   $ terraform init
   ```

> **lightbulb** When running `terraform init`, Terraform identifies the use of the local provider based on your resource configuration.

Example output:

```Terraform theme={null}
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/local...
- Installing hashicorp/local v1.4.0...
- Installed hashicorp/local v1.4.0 (signed by HashiCorp)

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, we recommend adding version constraints in a required_providers block
in your configuration, with the constraint strings suggested below.

* hashicorp/local: version = "~> 1.4.0"

Terraform has been successfully initialized!
```

3. **Review the Execution Plan:**\
   Use the `terraform plan` command to see the proposed actions before applying changes.

   ```bash theme={null}
   $ terraform plan
   ```

   The output provides a diff-like summary showing what will be created, modified, or destroyed. For example, a plus symbol (`+`) next to the `local_file.pet` resource indicates that it will be created.

   Example excerpt:

   ```Terraform theme={null}
   An execution plan has been generated and is shown below.
   Resource actions are indicated with the following symbols:
      + create

   Terraform will perform the following actions:

     # local_file.pet will be created
     + resource "local_file" "pet" {
         + content              = "We love pets!"
         + directory_permission = "0777"
         + file_permission      = "0777"
         + filename             = "/root/pets.txt"
         + id                   = (known after apply)
       }

   Plan: 1 to add, 0 to change, 0 to destroy.
   ```

4. **Apply the Configuration:**\
   Execute the following command to apply the configuration and create the resource:

   ```bash theme={null}
   $ terraform apply
   ```

   Confirm the execution by typing `yes` when prompted.

   Example output:

   ```Terraform theme={null}
   An execution plan has been generated and is shown below.
   Resource actions are indicated with the following symbols:
       + create

   Terraform will perform the following actions:

       # local_file.pet will be created
       + resource "local_file" "pet" {
           + content             = "We love pets!"
           + directory_permission = "0777"
           + file_permission      = "0777"
           + filename            = "/root/pets.txt"
           + id                  = (known after apply)
       }

   Plan: 1 to add, 0 to change, 0 to destroy.

   Do you want to perform these actions?
   Terraform will perform the actions described above.
   Only 'yes' will be accepted to approve.

   Enter a value: yes
   local_file.pet: Creating...
   local_file.pet: Creation complete after 0s [id=521c5c732c78cb42cc9531ecc7c0638c4a115b55]
   Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
   ```

After applying the configuration, verify the creation of the file using the `cat` command or inspect the resource details with:

```bash theme={null}
$ terraform show
```

Example `terraform show` output:

```Terraform theme={null}
