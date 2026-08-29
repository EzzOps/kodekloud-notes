# Operators and Conditional Expressions

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Read-generate-and-modify-configuration/Operators-and-Conditional-Expressions/page

Explains Terraform operators and how to use conditional (ternary) expressions to select values, validate inputs, and simplify configuration without extra resources.

In this lesson you'll learn the common operators available in Terraform and how to use conditional (ternary) expressions to choose values based on runtime inputs. These constructs are useful when writing dynamic configuration, validating values, or simplifying logic without creating additional resources.

<Frame>
  <img alt="A purple presentation slide with layered hexagon shapes and centered white text that reads &#x22;Operators & Conditional Expressions.&#x22; It appears to be a title slide for a talk or lesson." />
</Frame>

## Supported operator categories

Terraform supports arithmetic, equality, comparison, and logical operators. You can experiment interactively using the terraform console command.

| Operator type         | Operators               | Description                                                                                        | Example             |                                             |                         |
| --------------------- | ----------------------- | -------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------------- | ----------------------- |
| Equality / Inequality | `==`, `!=`              | Test whether values are exactly equal or not equal. Works with strings, numbers, lists, maps, etc. | `"a" == "a"` → true |                                             |                         |
| Comparison            | `>`, `<`, `>=`, `<=`    | Numeric comparisons that return a Boolean.                                                         | `5 > 3` → true      |                                             |                         |
| Logical               | `&&`, \`                |                                                                                                    | `, `!\`             | Combine Boolean expressions (AND, OR, NOT). | `true && false` → false |
| Arithmetic            | `+`, `-`, `*`, `/`, `%` | Numeric operations.                                                                                | `2 + 3` → 5         |                                             |                         |

Note: equality checks can compare values of any type, but comparing values of different types (for example, a number vs a string) will evaluate to false.

## Equality and comparison examples

Try these examples with terraform console to validate behavior:

```bash theme={null}
$ terraform console
> var.a > var.b
true
```

Corresponding variables:

```hcl theme={null}
variable "a" {
  type    = number
  default = 50
}

variable "b" {
  type    = number
  default = 25
}
```

## Logical operators

* AND: `&&` — returns true only if both operands are true.
  * Example: `8 > 7 && 8 < 10` is true.
* OR: `||` — returns true if either operand is true.
  * Example: `8 > 9 || 8 < 10` is true (second condition is true).
* NOT: `!` — inverts a Boolean value.
  * Example: if `var.special = true`, then `!var.special` is false.

Interactive console examples:

```bash theme={null}
$ terraform console
> 8 > 7 && 8 < 10
true
> 8 > 9 || 8 < 10
true
> var.special
true
> !var.special
false
```

## Conditional expressions (ternary operator)

Terraform provides a conditional expression (ternary) to select between two values inline:

condition ? true\_val : false\_val

Use conditional expressions to determine values inside resource arguments, locals, or outputs without creating conditional resources. Important: both `true_val` and `false_val` must be expressions that produce compatible types because the conditional expression must evaluate to a single consistent type.

<Callout icon="lightbulb">
  The true and false branches of a conditional expression must produce compatible types. For example, both should be numbers, both strings, or both lists containing the same element type.
</Callout>

## Practical example — password length validation

Use a conditional expression to ensure a generated password has a minimum length (8 characters). If the user supplies a smaller length, Terraform will use 8 instead.

variables.tf:

```hcl theme={null}
variable "length" {
  type        = number
  description = "The desired length of the password"
  # No default provided; value must be supplied at apply time or via a tfvars file.
}
```

main.tf:

```hcl theme={null}
resource "random_password" "password_generator" {
  # Use 8 if var.length is less than 8, otherwise use var.length
  length = var.length < 8 ? 8 : var.length
}

output "password" {
  value = random_password.password_generator.result
}
```

Shell equivalent (for conceptual comparison):

```bash theme={null}
if [ "$length" -lt 8 ]; then
  length=8
  echo $length
else
  echo $length
fi
```

## Apply and validate

Initialize and apply your configuration while passing a small length (for example, 5). Terraform will evaluate the conditional and choose 8:

```bash theme={null}
$ terraform init
$ terraform apply -var=length=5 -auto-approve
```

If you pass `-var=length=12`, Terraform will use 12 because it satisfies the condition.

## Quick reference and links

* terraform console — interactive REPL for testing expressions and functions.
* random\_password resource — from the random provider (useful for short-lived secrets).
* For more operator details and expression syntax, see the official Terraform documentation:
  * [Terraform language expressions](https://developer.hashicorp.com/terraform/language/expressions)
  * [Terraform CLI: console](https://developer.hashicorp.com/terraform/cli/commands/console)

That covers the basic operators and how to use conditional expressions in Terraform to select values based on input or calculated conditions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/c59e52ed-8a8c-4a6c-8ad0-8dcc38c1598e/lesson/57e88010-91d8-497f-bb4a-a8c8d9e1438e" />
</CardGroup>
