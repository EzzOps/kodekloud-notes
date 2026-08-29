# Other Terragrunt Functions

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Functions/Other-Terragrunt-Functions/page

Terragrunt offers built-in utilities to streamline configurations, reduce repetition, and integrate with AWS and other environments.

Terragrunt comes packed with a variety of built-in utilities beyond the core functions you’ve already learned. These helpers can streamline your configurations, reduce repetition, and integrate seamlessly with AWS and other environments.

## Official Documentation

Always keep an eye on the latest features and advanced utilities in the Terragrunt docs:

* Terragrunt Functions & Helpers: [https://terragrunt.gruntwork.io/docs/functions/](https://terragrunt.gruntwork.io/docs/functions/)
* Advanced Usage: [https://terragrunt.gruntwork.io/docs/advanced-usage/](https://terragrunt.gruntwork.io/docs/advanced-usage/)

## Common Built-In Functions

| Function                    | Description                                                     | Example                                         |
| --------------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| `getenv("VAR_NAME")`        | Retrieve the value of an environment variable.                  | `locals { region = getenv("AWS_REGION") }`      |
| `get_aws_account_id()`      | Fetch the AWS account ID for the current credentials.           | `locals { account_id = get_aws_account_id() }`  |
| `get_aws_caller_identity()` | Return AWS caller identity details (user/role ARN, account ID). | `locals { caller = get_aws_caller_identity() }` |

## Creating Custom Functions

If your scenario demands logic beyond built-ins, Terragrunt’s plugin system lets you author custom helpers in Go.

<Callout icon="lightbulb">
  When writing custom plugins:

  * Follow Go module conventions.
  * Respect Terragrunt’s plugin API.
  * Version and distribute via your internal registry.
</Callout>

<Callout icon="triangle-alert">
  Custom plugins can introduce breaking changes if not versioned properly.\
  Always pin plugin versions in your `terragrunt.hcl` and test in a sandbox environment.
</Callout>

## Best Practices & Tips

* Organize functions into logical groups (e.g., AWS, GCP, environment variables).
* Keep `locals` blocks concise and well-documented.
* Reuse common logic through shared modules or parent configurations.

## Links and References

* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [Terraform Registry](https://registry.terraform.io/)
* [Go Plugin Overview](https://golang.org/pkg/plugin/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/5775621f-5504-4da8-835d-661cda37a852/lesson/01e9987d-846a-45a0-883c-ecd9bcd8f915" />
</CardGroup>
