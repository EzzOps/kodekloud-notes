# aws_dynamodb_table.cars will be created
+ resource "aws_dynamodb_table" "cars" {
    + arn              = (known after apply)
    + billing_mode     = "PAY_PER_REQUEST"
    + hash_key         = "VIN"
    + id               = (known after apply)
    + name             = "cars"
    + stream_arn       = (known after apply)
    + stream_label     = (known after apply)
    + stream_view_type = (known after apply)

    + attribute {
        + name = "VIN"
        + type = "S"
      }
    
    + point_in_time_recovery {
        + enabled = (known after apply)
      }
}
aws_dynamodb_table.cars: Creating...
aws_dynamodb_table.cars: Creation complete after 0s [id=cars]
```

<Callout icon="lightbulb">
  Remember, on-demand billing is ideal for workloads with unpredictable traffic, as you only pay for the read/write operations you use.
</Callout>

## Inserting Items into the Table

Once the DynamoDB table is created, the next step is to insert items into it. Terraform provides the `aws_dynamodb_table_item` resource for adding entries to your DynamoDB table. This resource requires the table name and hash key (which can be referenced from the table resource) along with the item data.

Below is an example configuration that includes both the table creation and the insertion of a single item into the table. Note the use of heredoc syntax (`<<EOF ... EOF`) for defining the item in valid JSON format, including the types for each attribute (e.g., "S" for string and "N" for number).

```hcl theme={null}
resource "aws_dynamodb_table" "cars" {
  name         = "cars"
  hash_key     = "VIN"
  billing_mode = "PAY_PER_REQUEST"
  attribute {
    name = "VIN"
    type = "S"
  }
}

resource "aws_dynamodb_table_item" "car-items" {
  table_name = aws_dynamodb_table.cars.name
  hash_key   = aws_dynamodb_table.cars.hash_key
  item       = <<EOF
{
  "Manufacturer": {"S": "Toyota"},
  "Make": {"S": "Corolla"},
  "Year": {"N": "2004"},
  "VIN": {"S": "4Y1SL65848Z411439"}
}
EOF
}
```

Apply the configuration to insert the item:

```bash theme={null}
$ terraform apply
```

Terraform will produce output indicating that the `aws_dynamodb_table_item.car-items` resource is being created. The process will output values similar to this:

```bash theme={null}
# aws_dynamodb_table_item.car-items will be created.
+ resource "aws_dynamodb_table_item" "car-items" {
    + hash_key  = "VIN"
    + id        = (known after apply)
    + item      = jsonencode(
        {
          Manufacturer = {
            + S = "Toyota"
          }
          Make = {
            + S = "Corolla"
          }
          VIN = {
            + S = "4Y1SL65848Z411439"
          }
          Year = {
            + N = "2004"
          }
        }
      )
    + table_name = "cars"
}
Plan: 1 to add, 0 to change, 0 to destroy.
```

<Callout icon="triangle-alert">
  This method is intended for managing a few items. For large-scale data management or bulk operations, consider alternative solutions or data migration strategies.
</Callout>

## Hands-On Lab

Now that you have learned how to create a DynamoDB table and insert data using Terraform, it's time for a practical hands-on lab. Follow along with the lab instructions to reinforce your understanding of managing DynamoDB tables with Terraform.

For further reading and more advanced Terraform configurations, refer to the following resources:

* [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [AWS DynamoDB Documentation](https://aws.amazon.com/dynamodb/)

Happy building with Terraform and DynamoDB!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e1d12378-f838-46c9-9b2e-28d86daa1e1e/lesson/74690b8e-93ec-4ed5-bf09-621199fc3db0" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e1d12378-f838-46c9-9b2e-28d86daa1e1e/lesson/4d16fcae-204c-453f-b5eb-c685fede6343" />
</CardGroup>


# Getting Started with AWS

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-with-AWS/Getting-Started-with-AWS/page

This article provides an introduction to AWS, its services, global infrastructure, and how to manage resources using Terraform.

AWS is one of the world’s most popular and innovative cloud computing platforms. According to Gartner’s Infrastructure and Platform Services Magic Quadrant, AWS has been recognized as the cloud leader for a decade, including its 10th consecutive win in 2020. This recognition is a testament to AWS’s robust and continuously evolving service offerings.

AWS provides a vast range of services—from core infrastructure technologies such as compute, storage, and databases, to modern innovations like machine learning, artificial intelligence, data lakes and analytics, and the Internet of Things. This extensive portfolio makes it faster, simpler, and more cost-effective to deploy applications, or even to migrate existing on-premises environments to the cloud.

<Frame>
  ![The image showcases AWS services categorized into Compute, Databases, Storage, Machine Learning, Analytics, and IoT, each represented by icons.](https://kodekloud.com/kk-media/image/upload/v1752884235/notes-assets/images/Terraform-Basics-Training-Course-Getting-Started-with-AWS/frame_40.jpg)
</Frame>

## Global Infrastructure

One of AWS’s major strengths is its extensive global cloud infrastructure. AWS operates across numerous globally distributed regions, with multiple data centers, known as availability zones, within each region. This global distribution ensures high availability, resilience, and the ability to scale applications dynamically.

<Frame>
  ![The image shows a world map highlighting AWS regions globally, with a list of specific regions like US East, Europe, and Asia Pacific.](https://kodekloud.com/kk-media/image/upload/v1752884236/notes-assets/images/Terraform-Basics-Training-Course-Getting-Started-with-AWS/frame_60.jpg)
</Frame>

As of the time of this recording, AWS operates 77 availability zones within 24 geographic regions, making it one of the most robust cloud infrastructures available.

## AWS Service Overview

Below is a summary of some key AWS service categories:

| Service Category         | Description                                                                | Example Use Case                      |
| ------------------------ | -------------------------------------------------------------------------- | ------------------------------------- |
| Compute & Storage        | Core infrastructure for application hosting and data storage               | Deploying web applications            |
| Databases                | Managed database services for structured and unstructured data             | Running relational or NoSQL databases |
| Machine Learning & AI    | Tools and frameworks for predictive analytics and intelligent applications | Automating customer service           |
| Data Lakes & Analytics   | Services for large-scale data processing and visualization                 | Business intelligence solutions       |
| Internet of Things (IoT) | Solutions for connecting devices and sensors                               | Smart home applications               |

## Managing AWS with Terraform

Terraform by HashiCorp is an Infrastructure as Code (IaC) tool designed to simplify the provisioning and management of AWS resources. As an advanced tier technology partner in the Amazon Partner Network, HashiCorp offers a dedicated AWS provider that allows users to define and manage infrastructure using the HashiCorp Configuration Language (HCL). These configuration files are human-readable, version-controlled, and seamlessly integrated with source control systems for enhanced manageability and reusability.

<Callout icon="lightbulb">
  For more details on Terraform and its AWS provider, visit the [Terraform Documentation](https://www.terraform.io/docs/providers/aws/index.html).
</Callout>

## Learning Path and Course Outline

In this article, our journey begins with the fundamentals of AWS. We will guide you through setting up an AWS account and navigating the AWS Management Console. The initial lectures and demonstrations are specifically designed for beginners using AWS.

Starting with Identity and Access Management (IAM), you will learn the basics of access control and security. Once you’re comfortable with IAM, we will demonstrate how to deploy IAM resources using Terraform. As you progress, additional AWS services such as S3 and DynamoDB will be introduced, along with practical examples of how to configure and manage these resources with Terraform.

<Callout icon="lightbulb">
  Each lecture and demonstration is complemented by hands-on labs, giving you practical experience in deploying AWS resources using Terraform.
</Callout>

This step-by-step approach helps you build a strong foundation in AWS while simultaneously gaining proficiency in Terraform—a powerful tool to manage and automate your cloud infrastructure.

## Additional Resources

* [AWS Documentation](https://aws.amazon.com/documentation/)
* [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
* [Terraform Documentation](https://www.terraform.io/docs)

With this knowledge, you are now ready to explore AWS and harness the power of Infrastructure as Code with Terraform. Enjoy your journey into cloud computing and modern infrastructure management!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e1d12378-f838-46c9-9b2e-28d86daa1e1e/lesson/32ddc88e-d4bb-4ddd-b632-44f914ea9be6" />
</CardGroup>
