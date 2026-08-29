# Using Variables in Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Basics/Using-Variables-in-Terraform/page

Learn techniques to pass input variables in Terraform, including default values, command line input, environment variables, and variable definition precedence.

In this lesson, you'll learn various techniques to pass input variables in Terraform. We'll cover several methods including setting default values in your variable blocks, providing values interactively or via the command line, using environment variables, and defining variables in separate files. Additionally, we'll explore the variable definition precedence rules when multiple sources assign values to the same variable. These techniques offer flexibility and control when managing your Terraform configurations.

***

## Using Default Values with Variable Blocks

By assigning default values directly within your variable blocks, you ensure that Terraform uses these values if no alternative is provided. For example, consider the following configuration that creates a local file resource and a random pet resource:

```hcl theme={null}
