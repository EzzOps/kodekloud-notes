# aws_iam_user.admin-user will be created
+ resource "aws_iam_user" "admin-user" {
    + arn           = (known after apply)
    + force_destroy = false
    + id            = (known after apply)
    + name          = "Lucy"
    + path          = "/"
    + tags          = {
        + "Description" = "Technical Team Leader"
      }
    + unique_id     = (known after apply)
}

Plan: 1 to add, 0 to change, 0 to destroy.
```

After verifying the plan, apply the changes using:

```bash theme={null}
terraform apply
```

Terraform will then create the IAM user as described in your configuration.

## Best Practices for Managing Credentials

Hardcoding credentials in your Terraform configuration is not recommended, especially when storing files in version control. Instead, consider one of the following alternatives:

<Callout icon="lightbulb">
  Avoid embedding sensitive information directly into your Terraform files. Instead, use environment variables or CLI configurations to manage your credentials securely.
</Callout>

### AWS CLI Configuration

Configure the AWS CLI on your machine using:

```bash theme={null}
aws configure
```

This creates a credentials file (typically located at `~/.aws/credentials`):

```ini theme={null}
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Terraform will automatically use these stored credentials.

### Environment Variables

Alternatively, you can set environment variables for your AWS credentials and region:

```bash theme={null}
export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=us-west-2
```

These methods enhance security by removing sensitive information from your Terraform configurations.

## Summary

By following these steps, you can efficiently provision and manage AWS IAM resources using Terraform, ensuring a more secure and maintainable infrastructure as code. For more detailed information, check out the [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

Happy provisioning!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e1d12378-f838-46c9-9b2e-28d86daa1e1e/lesson/9aed1294-d2a8-455d-b8c1-1d87f28e4f5d" />
</CardGroup>


# Demo Dynamodb

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-with-AWS/Demo-Dynamodb/page

This guide demonstrates creating and managing a DynamoDB table using the AWS Management Console, including adding items and filtering results.

This guide demonstrates how to create and manage a DynamoDB table using the AWS Management Console. We'll walk through accessing DynamoDB, creating a table to store employee data, adding items, and filtering results efficiently.

## Accessing DynamoDB

1. Click on the **Services** tab in the top left corner.
2. Under **Databases**, select **DynamoDB**.
3. Click the **Create Table** button.

## Creating a Table

To get started, provide a table name to store employee information. In this example, name the table **employee\_data**. Next, specify the primary key (hash key) by using **employee\_id** with the data type set to **Number**.

Leave the other settings at their default values and click the **Create** button.

<Frame>
  ![The image shows the AWS Console interface for creating a DynamoDB table named "employee\_data" with "employee\_id" as the primary key.](https://kodekloud.com/kk-media/image/upload/v1752884215/notes-assets/images/Terraform-Basics-Training-Course-Demo-Dynamodb/frame_50.jpg)
</Frame>

After a few seconds, the table is created and its name appears in the left sidebar. Click on the **Items** tab to view the table contents (initially, there are no items).

## Adding Items

Next, add items to the **employee\_data** table:

1. Click on the **Create Item** tab. The **employee\_id** field (the primary key) is already populated.
2. Modify the **employee\_id** to `1`.
3. Click the **Append** button to add additional attributes:
   * **name** (String) for the employee's name.
   * **age** (Number) for the employee's age.
   * **role** (String) for the employee's role.

After adding the necessary details, click **Save**. The created item will include an employee\_id of `1` along with the corresponding attributes. Below is a sample JSON representation:

```json theme={null}
{
  "employee_id": 1,
  "name": "lucy",
  "age": 42,
  "role": "team lead"
}
```

You can similarly insert more items. For instance, to add details for another user named Lee, use the following input:

```json theme={null}
{
  "employee_id": 2,
  "name": "abdul",
  "age": 33
}
```

<Callout icon="lightbulb">
  In DynamoDB, only the primary key is required when inserting items; all other attributes are optional. This allows flexibility when modeling your data.
</Callout>

<Frame>
  ![The image shows an AWS DynamoDB console displaying an "employee\_data" table with three entries, including employee IDs, ages, names, and roles.](https://kodekloud.com/kk-media/image/upload/v1752884216/notes-assets/images/Terraform-Basics-Training-Course-Demo-Dynamodb/frame_170.jpg)
</Frame>

## Filtering Items

To easily locate specific items, you can apply filters to the table. For example, to list all employees with the role of "Developer", apply a filter using the **role** attribute.

<Frame>
  ![The image shows an AWS DynamoDB console displaying an "employee\_data" table with entries filtered by the role "Developer."](https://kodekloud.com/kk-media/image/upload/v1752884216/notes-assets/images/Terraform-Basics-Training-Course-Demo-Dynamodb/frame_200.jpg)
</Frame>

## Next Steps

This concludes the demo on how to create and manage a DynamoDB table using the AWS Management Console. In forthcoming tutorials, we will explore how to create DynamoDB tables using Terraform for automated infrastructure management.

For additional information on AWS and DynamoDB, consider visiting:

* [AWS Documentation](https://docs.aws.amazon.com/)
* [DynamoDB Developer Guide](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]/)

Enhance your cloud solutions by exploring these resources and leveraging AWS services in your infrastructure projects.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e1d12378-f838-46c9-9b2e-28d86daa1e1e/lesson/db960de1-6815-4207-b63a-789de7da612a" />
</CardGroup>
