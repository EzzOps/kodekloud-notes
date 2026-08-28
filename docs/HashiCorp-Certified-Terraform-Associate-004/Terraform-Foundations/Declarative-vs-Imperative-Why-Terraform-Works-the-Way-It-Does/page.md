# Declarative vs Imperative Why Terraform Works the Way It Does

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Declarative-vs-Imperative-Why-Terraform-Works-the-Way-It-Does/page

Describes why Terraform uses a declarative infrastructure model versus imperative scripts, highlighting dependency graph, state management, minimal changes, and plan before apply workflow

Terraform follows a declarative model. But what does "declarative" actually mean in infrastructure-as-code, and why does Terraform prefer this approach?

## Declarative vs Imperative — the core idea

* Declarative: You describe the desired *end state* of your infrastructure. Terraform figures out what actions are necessary to reach that state.
* Imperative: You list the exact *steps* to perform (create VM, run commands, attach network, etc.). You control the workflow.

With Terraform, you write configuration files that declare resources and their properties. Terraform then builds a dependency graph, computes a plan of changes to reconcile the real world with your declared state, and applies only the minimal, necessary operations.

## Example: Declarative Terraform configuration

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t2.micro"
  tags = {
    Name = "web-server"
  }
}
```

Run these commands to preview and apply changes:

* `terraform plan` — show the proposed set of actions without making changes
* `terraform apply` — execute the planned actions and update state

## Equivalent Imperative steps (conceptual)

```bash theme={null}
