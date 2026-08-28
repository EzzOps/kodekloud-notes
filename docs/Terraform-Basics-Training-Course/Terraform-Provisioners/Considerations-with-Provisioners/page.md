# aws_instance.webserver will be created
+ resource "aws_instance" "webserver" {
    + ami                    = "ami-0edab43b6fa892279"
    + instance_type          = "t2.micro"
    + ipv6_address_count     = (known after apply)
    + public_ip              = (known after apply)
    + source_dest_check      = true
    + subnet_id              = (known after apply)
    + tags                   = {
        + "Description" = "An NGINX WebServer on Ubuntu"
        + "Name"        = "webserver"
      }
    + tenancy                = (known after apply)
    + user_data              = "527516162d9d8675a26b6ca97664226e6e2bff82"
    + volume_tags            = (known after apply)
    + vpc_security_group_ids = (known after apply)
}
...
aws_instance.webserver: Creating...
aws_instance.webserver: Still creating... [20s elapsed]
aws_instance.webserver: Creation complete after 22s [id=i-0085e5d0f442f7c4f]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

## Accessing the EC2 Instance

Since the instance runs Ubuntu, SSH is the preferred method for remote access. However, the default Terraform configuration does not include an IP address, key pair, or security group settings for SSH, making direct SSH access impossible at this stage.

When launching an instance manually using the AWS Management Console, you typically create or assign an SSH key pair. In the sections below, we demonstrate how to enable this with Terraform.

<Frame>
  ![The image illustrates setting up an SSH key pair for an Ubuntu web server, highlighting user access and port 22, with instructions for creating and downloading a key pair.](https://kodekloud.com/kk-media/image/upload/v1752884196/notes-assets/images/Terraform-Basics-Training-Course-AWS-EC2-with-Terraform/frame_90.jpg)
</Frame>

## Configuring Key-Based SSH Access

To enable SSH access, add an AWS Key Pair resource that uses an existing public key file (in this example, `web.pub`) from the local machine. You have the option to load the public key using the file function or simply include its content directly.

Below is the Terraform configuration that introduces the key pair resource:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An Nginx WebServer on Ubuntu"
  }
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install nginx -y
    systemctl enable nginx
    systemctl start nginx
  EOF
}

resource "aws_key_pair" "web" {
  public_key = file("/root/.ssh/web.pub")
}
```

Integrate the key pair into the EC2 resource by referencing its ID, as shown below:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An Nginx WebServer on Ubuntu"
  }
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install nginx -y
    systemctl enable nginx
    systemctl start nginx
  EOF
  key_name = aws_key_pair.web.id
}

resource "aws_key_pair" "web" {
  public_key = file("/root/.ssh/web.pub")
}
```

## Configuring the Security Group

To allow SSH connections (port 22) from the internet to your web server, configure a security group. In previous examples, the EC2 instance was deployed in the default VPC and subnet, with a security group named "SSH access" allowing inbound SSH connections from any source (`0.0.0.0/0`). While this setup is acceptable in a demo environment, it is not recommended for production.

Below is the Terraform configuration that incorporates the security group resource:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami                    = "ami-0edab43b6fa892279"
  instance_type          = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An Nginx WebServer on Ubuntu"
  }
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install nginx -y
    systemctl enable nginx
    systemctl start nginx
  EOF
  key_name               = aws_key_pair.web.id
  vpc_security_group_ids = [ aws_security_group.ssh-access.id ]
}

resource "aws_key_pair" "web" {
  public_key = file("/root/.ssh/web.pub")
}

resource "aws_security_group" "ssh-access" {
  name        = "ssh-access"
  description = "Allow SSH access from the Internet"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

<Callout icon="lightbulb">
  Ensure that the `cidr_blocks` value is exactly `"0.0.0.0/0"` as shown. This setting is suitable for demonstration purposes only.
</Callout>

## Retrieving the Instance Public IP

For convenient management and remote access, add an output variable to retrieve the public IP address of the web server instance. This IP address can be used along with your SSH private key (paired with the provided public key) to access the server.

After running `terraform apply`, Terraform creates the key pair, security group, and EC2 instance. Due to configuration changes, Terraform might recreate the EC2 instance. Once complete, you can use the output public IP and your private key to establish an SSH connection from your local machine.

With these configurations, you have successfully deployed an AWS EC2 instance with key-based SSH access and a security group that allows SSH connections. This setup provides a robust starting point for deploying applications on AWS using Terraform.

## Additional Resources

* [Terraform Documentation](https://www.terraform.io/docs)
* [AWS EC2 Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)
* [Ubuntu Official Site](https://ubuntu.com/)

Happy coding and deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/9fcbd3cd-b06d-4816-8646-3639ca3d19cd/lesson/c528041b-a2b7-4a0a-9e1a-f16b1d910dc0" />
</CardGroup>


# Considerations with Provisioners

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Provisioners/Considerations-with-Provisioners/page

This article explores considerations for using provisioners in Terraform, emphasizing their complexity and recommending resource-native features for better infrastructure management.

In this lesson, we explore key considerations when using provisioners in Terraform. Provisioners can be very useful for executing tasks such as bootstrapping with a Remote Exec script; however, their use should be limited. Terraform advises caution when using them due to several reasons.

<Callout icon="lightbulb">
  Provisioners often add complexity to your configuration. Their nature of executing arbitrary system-supported commands means that Terraform cannot fully simulate or validate these actions during the planning phase.
</Callout>

## Why Use Provisioners Sparingly?

Provisioners in Terraform can execute any system-supported command via the command or inline arguments. This flexibility makes them powerful but also creates challenges:

1. They increase the overall complexity of your Terraform configuration.
2. Due to the dynamic nature of these commands, Terraform cannot accurately predict the outcome during the plan phase.

### Example: Remote Exec Provisioner

Below is an example Terraform configuration that employs the `remote-exec` provisioner to append the host's IP address to a file on the remote instance.

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edadb43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An NGINX WebServer on Ubuntu"
  }
  provisioner "remote-exec" {
    inline = ["echo $(hostname -i) >> /tmp/ips.txt"]
  }
}
```

## Connection Block Requirement

For provisioners such as Remote Exec, it is essential to define a connection block to establish network connectivity and authenticate to the target instance. The connection details must be configured correctly on the local machine before the provisioner runs, which might not always be feasible.

Consider the following sample configuration:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An NGINX WebServer on Ubuntu"
  }
  
  provisioner "remote-exec" {
    inline = ["echo $(hostname -i) >> /tmp/ips.txt"]
  }
}
```

## Best Practices: Use Resource-Native Features

To mitigate the challenges associated with provisioners, Terraform recommends leveraging resource-native features. For instance, when working with [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2), you can utilize the User Data feature, ensuring that required tasks are executed during instance launch without an explicit connection block.

### Example: Using User Data

The following Terraform configuration uses the User Data feature to install and configure NGINX during instance launch:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edadb43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An NGINX WebServer on Ubuntu"
  }
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install nginx -y
    systemctl enable nginx
    systemctl start nginx
  EOF
}
```

<Callout icon="triangle-alert">
  While using provisioners like remote-exec or User Data can be helpful, it is recommended to limit post-provisioning tasks. Over-relying on them can lead to configuration drift and harder maintenance.
</Callout>

## Custom Images and Templating Tools

A best practice is to build custom images that include all the necessary software and configurations from the start. This approach minimizes the need for post-provisioning tasks during instance initialization. For example, instead of installing NGINX during launch with User Data or remote-exec, you could use a custom Ubuntu AMI that already has NGINX installed:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edad43b6fa892279"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An NGINX WebServer on Ubuntu"
  }
}
```

Templating tools come in handy when creating custom AMIs. You can generate these images by capturing an instance that has the required software and configuration, or by using tools like [Packer](https://www.packer.io/). Packer provides a declarative approach to image building, and once the custom AMI is built, you can refer to it directly in your Terraform configuration:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-XYZ"
  instance_type = "t2.micro"
  tags = {
    Name        = "webserver"
    Description = "An NGINX WebServer on Ubuntu"
  }
}
```

By favoring resource-specific configurations and custom-built images, you can reduce the reliance on provisioners and build a more robust, maintainable infrastructure with Terraform.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/9fcbd3cd-b06d-4816-8646-3639ca3d19cd/lesson/173688e4-8af2-4dd6-b7e1-60b3d8c68fa4" />
</CardGroup>
