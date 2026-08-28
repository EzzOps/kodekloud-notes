# aws_instance.webserver is tainted, so must be replaced
-/+ resource "aws_instance" "webserver-3" {
```

<Callout icon="triangle-alert">
  Double-check your resource configuration and provisioner commands to avoid unintentional resource replacement.
</Callout>

## Forcing a Resource Rebuild

There are situations where you might want to deliberately force a resource rebuild. For example, if manual changes—such as updating the Nginx version—were made on an AWS instance, you can efficiently trigger the recreation of that resource without performing a full destroy and apply cycle.

### Tainting the Resource

Run the following command to mark the resource as tainted:

```bash theme={null}
$ terraform taint aws_instance.webserver
Resource instance aws_instance.webserver has been marked as tainted.
```

### Confirming the Change with Terraform Plan

After tainting, a terraform plan will show that the resource is scheduled for replacement:

```bash theme={null}
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be persisted to local or remote state storage.

aws_instance.webserver: Refreshing state... [id=i-0fd3946f5b3ab8af8]
--------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
    -/+ destroy and then create replacement

Terraform will perform the following actions:

  # aws_instance.webserver is tainted, so must be replaced
  -/+ resource "aws_instance" "webserver" {
```

## Reversing Taint: Using the Untaint Command

If you later decide that a resource should not be replaced, you can remove its tainted state by using the untaint command. This prevents Terraform from destroying and recreating the resource during the next apply.

```bash theme={null}
$ terraform untaint aws_instance.webserver
Resource instance aws_instance.webserver has been successfully untainted.
```

## Summary Table

| Command           | Action                           | Description                                           |
| ----------------- | -------------------------------- | ----------------------------------------------------- |
| terraform taint   | Mark resource as tainted         | Forces the resource to be replaced on the next apply  |
| terraform untaint | Remove taint from resource       | Prevents resource replacement during the next apply   |
| terraform plan    | Verify resource replacement plan | Confirms which resources are marked for replacement   |
| terraform apply   | Apply configuration changes      | Executes resource creation and replacement operations |

By leveraging the taint and untaint commands, you can manage resource lifecycle events efficiently, ensuring that your infrastructure remains consistent with your desired state.

For further details, explore the [Terraform Documentation](https://www.terraform.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/29825b4d-c0d3-4732-a4e0-ec3a2988e2a3/lesson/bec58f8f-0c05-40f4-baaa-c19827185899" />
</CardGroup>


# Creating and Using a Module

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Modules/Creating-and-Using-a-Module/page

This guide explains how to create a reusable Terraform module for deploying a payroll application across multiple AWS regions.

In this guide, we will create a reusable Terraform module to deploy multiple environments for the same infrastructure. Imagine an organization called FlexIT Consulting that has developed a prototype payroll software. This software needs to be deployed in several countries on AWS Cloud using the same core architecture.

The simplified architecture leverages the default VPC and incorporates the following components:

* An EC2 instance (using a custom AMI) that hosts the application server.
* A DynamoDB NoSQL database to store employee and payroll data.
* An S3 bucket to store documents such as pay stubs and tax forms.
* Users accessing the application on the EC2 instance.

These components integrate to form a basic deployment model for the payroll application.

<Frame>
  ![The image depicts a simplified AWS architecture with a VPC, an EC2 instance, an S3 bucket, and a DynamoDB table for a payroll application.](https://kodekloud.com/kk-media/image/upload/v1752884194/notes-assets/images/Terraform-Basics-Training-Course-Creating-and-Using-a-Module/frame_60.jpg)
</Frame>

The goal is to encapsulate this setup into a Terraform module so that the same stack can be deployed across different regions. Based on the high-level design outlined above, let’s create the corresponding Terraform configuration.

<Callout icon="lightbulb">
  Some values, such as the instance type, are hard-coded for consistency, while others — like the AMI and region-specific naming — are configurable via variables.
</Callout>

## Module Directory Structure

We will create a module under a directory named `modules`. For instance, you might place the module in the following path:

```text theme={null}
/root/terraform-projects/modules/payroll-app
```

Within this directory, you will create configuration files for the necessary AWS resources: an EC2 instance, an S3 bucket, and a DynamoDB table. Execute these commands to set up the module directory and create the required files:

```bash theme={null}
$ mkdir -p /root/terraform-projects/modules/payroll-app
