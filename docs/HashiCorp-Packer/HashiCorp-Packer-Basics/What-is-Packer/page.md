# What is Packer

Source: https://notes.kodekloud.com/docs/HashiCorp-Packer/HashiCorp-Packer-Basics/What-is-Packer/page

Packer automates the creation of machine images for various platforms using a single source configuration, streamlining deployment processes.

Packer by HashiCorp is an open-source tool that automates the creation of **machine images** for various platforms—AWS, Azure, Docker, and more—using a single source configuration. Instead of manually configuring each virtual machine or container, Packer enables you to bake your desired packages, dependencies, and application code into a **golden image** that’s ready for deployment.

<Frame>
  ![The image illustrates how Packer creates images for AWS, Azure, and Docker, showing the flow from source to deployment.](https://kodekloud.com/kk-media/image/upload/v1752878647/notes-assets/images/HashiCorp-Packer-What-is-Packer/packer-image-creation-aws-azure-docker.jpg)
</Frame>

## Key Benefits of Packer

* **Consistency**: Build identical images every time.
* **Speed**: Automate provisioning and eliminate manual steps.
* **Portability**: Use a single HCL template across multiple cloud and container platforms.
* **Scalability**: Integrate into CI/CD pipelines for fully automated image builds.

<Callout icon="lightbulb">
  Before you begin, ensure you have the latest [Packer CLI](https://www.packer.io/downloads) installed and your cloud provider credentials configured (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, etc.).
</Callout>

## Packer Configuration Components

A typical Packer template consists of three primary sections:

| Component       | Purpose                                                                                  | Example                                                       |
| --------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Builders        | Defines the target platform and base image (e.g., AWS AMI, Azure Managed Image, Docker). | `source "amazon-ebs" "ubuntu" { ... }`                        |
| Provisioners    | Runs scripts or commands to install dependencies, copy code, and configure services.     | `provisioner "shell" { inline = ["sudo apt install nginx"] }` |
| Post-Processors | Optional steps to compress artifacts, upload images to registries, or tag images.        | `post-processor "docker-tag" { ... }`                         |

## Example: Building an Ubuntu AMI with Nginx

Below is a simple HCL template (`template.pkr.hcl`) that launches an EC2 instance from an Ubuntu AMI, installs Nginx, clones application code, and then creates a new AMI.

```hcl theme={null}
source "amazon-ebs" "ubuntu" {
  ami_name      = "my-first-packer-image"
  instance_type = "t2.micro"
  region        = "us-east-1"
  source_ami    = "ami-0557a15b87f6559cf"
  ssh_username  = "ubuntu"
}

build {
  name    = "ubuntu-nginx-image"
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt update -y",
      "sudo apt install nginx -y",
      "git clone https://github.com/example/my-app.git /home/ubuntu/app",
      "sudo ufw allow 'Nginx HTTP'",
      "sudo systemctl enable nginx",
      "sudo systemctl start nginx"
    ]
  }
}
```

### Build Commands

Run these commands in your project directory:

```bash theme={null}
