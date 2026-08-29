# Using interpolation in a string expression
greeting = "Hello, ${var.name}!"
bio = "My name is ${var.name}, I'm your instructor!"
# Evaluates to: My name is Bryan, I'm your instructor!
```

Constructing names and identifiers from data + variables

```hcl theme={null}
variable "environment" {
  type    = string
  default = "dev"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

# Example resource name assembled from region and environment
name = "server-${data.aws_region.current.name}-${var.environment}"
# Example bucket name that includes account ID for global uniqueness
bucket_name = "s3-${data.aws_caller_identity.current.account_id}-backups"
# Example evaluated value: s3-123456789012-backups
```

<Callout icon="warning">
  S3 bucket names must be globally unique across all AWS accounts. Include account IDs, environment prefixes (e.g. `dev`, `prod`), or timestamps in bucket names to avoid naming collisions.
</Callout>

Best practices and patterns

* Use `locals` for values repeated across resources (instance types, common tags).
* Use `data` blocks for provider metadata (AMIs, regions, account IDs).
* Prefer interpolation or the newer expression forms over hard-coded strings.
* Validate variable inputs with `validation` blocks to prevent invalid configurations.
* For global resources (S3), ensure deterministic uniqueness using account IDs, regions, timestamps, or hashes.

Quick reference: Terraform variable types and common usage

| Variable type | Use case                             | Example                                                                         |
| ------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| string        | Names, ARNs, single values           | `variable "app" { type = string }`                                              |
| number        | Sizing, counts, ports                | `variable "instance_count" { type = number }`                                   |
| bool          | Feature toggles                      | `variable "enable_monitoring" { type = bool }`                                  |
| list          | Ordered collections (subnets, zones) | `variable "subnets" { type = list(string) }`                                    |
| map           | Key/value pairs for tags or mappings | `variable "tags" { type = map(string) }`                                        |
| object        | Structured compound inputs           | `variable "db_config" { type = object({ engine = string, version = string }) }` |

Practical next steps

* Practice by converting an existing static Terraform module into a dynamic one: replace literals with `var.*`, `local.*`, and `data.*`.
* Create small lab folders for AWS, Azure, and GitHub:
  * Add a README with instructions.
  * Add starter Terraform files and exercises to modify interpolation and data lookups.
* Experiment with naming patterns to ensure uniqueness across accounts and regions.

Links and references

* [Terraform Language: Variables](https://www.terraform.io/docs/language/values/variables.html)
* [Terraform Data Sources](https://www.terraform.io/docs/language/data-sources/index.html)
* [Terraform Locals](https://www.terraform.io/docs/language/values/locals.html)
* [AWS S3 Naming Guidelines](https://docs.aws.amazon.[SECRET_REDACTED].html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/67cd2d98-955a-4d03-8271-6896a6ba8560" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/34148477-db36-4c58-9d21-b837cf4fd5d6/lesson/557863de-ca5e-4312-bf8e-0ba095ea2ee2" />
</CardGroup>


# Using Built In Functions to Standardize Code

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Marking-Code-Reusable/Using-Built-In-Functions-to-Standardize-Code/page

Guide on using Terraform built-in functions to standardize infrastructure-as-code by simplifying naming, sizing, network calculations, and collection type conversions for reusable, consistent modules.

This guide explains how Terraform's built-in functions help you standardize infrastructure-as-code. By leveraging functions for strings, numbers, collections, and network calculations, you can avoid repetitive configuration, keep naming and sizing consistent across environments, and simplify logic across your Terraform codebase.

Mastering a compact set of functions — numeric, string, network, and type conversions — will make your Terraform configurations more maintainable, readable, and reliable in production.

<Frame>
  <img alt="The image is an informational graphic about the benefits of built-in functions in Terraform, highlighting their role in simplifying infrastructure code by reducing repetitive tasks, simplifying logic, and ensuring consistent deployment patterns." />
</Frame>

<Callout icon="lightbulb">
  Terraform functions follow a consistent pattern: `function_name(arg1, arg2, ...)`. In real modules you typically pass variables, resource attributes, or data lookups into these functions — not hard-coded literals. Using functions centralizes logic and reduces duplication.
</Callout>

## Basic function pattern

Terraform functions accept zero or more arguments and return a computed value. The most common usage patterns include string formatting for resource names, numeric decisions for sizing, and collection transformations to support `for_each` or indexing.

<Frame>
  <img alt="The image explains core Terraform functions, specifically Numeric Functions, String Functions, and Type Conversions, with examples and descriptions for each category." />
</Frame>

Examples:

```hcl theme={null}
