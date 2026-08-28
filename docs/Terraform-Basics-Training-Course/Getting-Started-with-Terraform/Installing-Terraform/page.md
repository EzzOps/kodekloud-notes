# local_file.pet:
resource "local_file" "pet" {
  content              = "We love pets!"
  directory_permission = "0777"
  file_permission      = "0777"
  filename             = "/root/pets.txt"
  id                   = "[AWS_SECRET_ACCESS_KEY]"
}
```

## Reviewing the Configuration

Let's recap the key components of the `local.tf` file:

* **Resource Block:** Uses the `local_file` resource type (local provider) to create a file.
* **Required Arguments:** The `filename` and `content` arguments are mandatory.
* **Optional Arguments:** Directory and file permissions can also be specified and are evident during the plan stage.

For additional resource types and their required arguments, refer to the [Terraform documentation](https://www.terraform.io/docs/providers/index.html).

<Frame>
  ![The image shows a diagram and text detailing a provider's argument reference, including optional and required arguments for file creation and permissions.](https://kodekloud.com/kk-media/image/upload/v1752884178/notes-assets/images/Terraform-Basics-Training-Course-HashiCorp-Configuration-Language-HCL-Basics/frame_590.jpg)
</Frame>

## Conclusion

In this article, we explored the basics of HCL by creating our first Terraform resource. We discussed HCL syntax, detailed the configuration for a local file resource, and walked through the Terraform workflow—from initialization and planning to applying changes. Now it's time to dive into hands-on labs and further your understanding of HCL and Terraform.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/385de3de-cd58-4925-9a24-207ebd7844b3/lesson/0ceefa60-2911-4a4e-a6b0-9d8efdca7700" />
</CardGroup>


# Installing Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Getting-Started-with-Terraform/Installing-Terraform/page

Learn how to install Terraform, a tool for managing infrastructure as code, on a Linux system.

In this lesson, you'll learn how to install Terraform—a powerful tool for managing infrastructure as code. Terraform is distributed as a single binary that you can download from the official [Terraform website](https://www.terraform.io/downloads.html). Once downloaded, simply place the executable in your system's PATH and verify the installation by checking its version.

Terraform supports Windows, macOS, and a range of Linux distributions. For the purposes of this lesson, all examples and labs will use Terraform version 0.13 on a Linux machine.

<Callout icon="lightbulb">
  This lesson uses Terraform v0.13. Ensure you download the correct version for your operating system.
</Callout>

## Installing Terraform 0.13 on Linux

Follow these steps to install Terraform 0.13 on a Linux system:

1. Open your terminal.
2. Download the Terraform 0.13 binary.
3. Unzip the downloaded file.
4. Move the Terraform executable to `/usr/local/bin` so that it is accessible from anywhere.
5. Verify the installation by checking the Terraform version.

Run the following commands:

```bash theme={null}
wget https://releases.hashicorp.com/terraform/0.13.0/terraform_0.13.0_linux_amd64.zip
unzip terraform_0.13.0_linux_amd64.zip
mv terraform /usr/local/bin
terraform version
```

You should see output similar to:

```console theme={null}
Terraform v0.13.0
```

## Working with Terraform

After installing Terraform, you can begin deploying resources using configuration files written in the HashiCorp Configuration Language (HCL). These files have a `.tf` extension and can be edited with any text editor or IDE.

For example, consider the following HCL snippet that defines an AWS EC2 instance resource:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0c2f25c1f66a1ff4d"
  instance_type = "t2.micro"
}
```

### Understanding Terraform Resources

A resource in Terraform represents an object managed by the tool. This can range from local files to virtual machines, cloud services, and beyond. Here’s a quick overview of some common resource types:

| Resource Type | Description              | Example         |
| ------------- | ------------------------ | --------------- |
| EC2 Instance  | Virtual machine on AWS   | `aws_instance`  |
| S3 Bucket     | Cloud storage on AWS     | `aws_s3_bucket` |
| IAM Role      | Access management in AWS | `aws_iam_role`  |

Terraform enables you to provision hundreds of resources across multiple cloud providers (such as AWS, GCP, or Azure) as well as manage on-premises infrastructure.

## Getting Started with Simple Resources

In the initial sections of this lesson, we focus on two simple resource types:

* A local file resource.
* A special resource called a random pet.

These examples are designed to help you understand key concepts such as resource lifecycle management and the basics of HCL syntax. Once you have a solid grasp of these fundamentals, you'll be better prepared to deploy more complex, real-world infrastructure scenarios later in the lesson.

<Callout icon="lightbulb">
  With these basic concepts in hand, you're now ready to explore more advanced Terraform configurations and resource management techniques.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/385de3de-cd58-4925-9a24-207ebd7844b3/lesson/705722ca-8f44-4c90-b62e-079fb8c634ee" />
</CardGroup>
