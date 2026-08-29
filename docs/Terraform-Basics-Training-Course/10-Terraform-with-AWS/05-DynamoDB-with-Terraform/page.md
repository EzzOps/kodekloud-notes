# DynamoDB with Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-with-AWS/DynamoDB-with-Terraform/page

Learn to create and manage DynamoDB tables using Terraform, including table creation and data insertion. Gain practical experience with the Terraform AWS provider for DynamoDB.

In this guide, you will learn how to create and manage DynamoDB tables using Terraform. We will walk through creating a DynamoDB table that stores vehicle information and then inserting data into that table. By following these steps, you'll gain practical experience with the Terraform AWS provider for DynamoDB.

## Creating the DynamoDB Table

To begin, we create a DynamoDB table using the AWS DynamoDB table resource in Terraform. In this example, we create a table named "cars" that holds data about vehicles. The table requires a name and a hash key that serves as the primary key—in our case, the vehicle identification number (VIN). Additionally, an attribute block is specified to detail the attribute (VIN) and the billing mode is set to on-demand (PAY\_PER\_REQUEST).

Below is the Terraform configuration for creating the "cars" DynamoDB table with on-demand billing:

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
```

When using provisioned capacity (the default mode), you would need to declare the read and write capacity units. However, this example uses PAY\_PER\_REQUEST (on-demand mode).

After saving your configuration, run the Terraform plan and apply commands to create the table:

```bash theme={null}
$ terraform apply
```

Terraform will output something similar to the following, confirming the creation of the table:

```Terraform theme={null}
Terraform will perform the following actions:
