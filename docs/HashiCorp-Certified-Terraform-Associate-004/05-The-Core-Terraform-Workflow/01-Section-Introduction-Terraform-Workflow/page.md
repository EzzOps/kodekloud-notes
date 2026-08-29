# Initialize working directory and download providers/modules
terraform init

# Show execution plan without making changes
terraform plan

# Execute the plan and create/update resources
terraform apply
```

Quick reference table

| Stage      | Purpose                                                          | Typical command   |
| ---------- | ---------------------------------------------------------------- | ----------------- |
| Initialize | Download providers/modules and prepare the working directory     | `terraform init`  |
| Plan       | Compare configuration against current state and preview changes  | `terraform plan`  |
| Apply      | Execute changes to reach the desired state                       | `terraform apply` |
| Write      | Create or modify `.tf` files (HCL) to declare intended resources | edit `.tf` files  |

Links and references

* [Terraform CLI documentation](https://www.terraform.io/cli)
* [Terraform providers](https://registry.terraform.io/browse/providers)

Now let’s focus on the first stage in more detail: writing configuration.

Write — authoring Terraform configuration (HCL)

The write stage is where you create one or more `.tf` files describing the desired state. The key principle is declarative configuration: you describe the end state you want, and Terraform determines API calls and operation order to achieve that state.

Best practices and workflow tips

* Start small: create a minimal resource (for example, a single VM or instance) and iterate.
* Iterate frequently: after each change, run `terraform plan` and `terraform apply` to converge toward the desired state.
* Keep state and sensitive data secure: use remote state backends (e.g., S3, Azure Storage, or Terraform Cloud) and avoid embedding secrets in plain text.
* Group related resources into modules for reusability and organization.

Simple HCL example

```hcl theme={null}
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
  tags = {
    Name = "example-web"
  }
}
```

Terraform configurations are iterative — add networking, storage, load-balancing, or other resources incrementally and re-run the workflow (init if needed, then plan and apply) to update infrastructure.

<Frame>
  <img alt="The image explains developing Terraform configuration, focusing on creating configuration files to define desired infrastructure states and the iterative nature of Terraform configurations." />
</Frame>

Further reading

* [Terraform: Getting Started](https://www.terraform.io/intro)
* [HashiCorp Learn: Terraform](https://learn.hashicorp.com/terraform)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/e8966855-1524-4525-a63a-140c847684ac)


# Section Introduction Terraform Workflow

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Section-Introduction-Terraform-Workflow/page

Overview of the Terraform workflow and best practices for writing configurations, managing state, planning, applying, destroying, and integrating infrastructure as code into CI/CD

Welcome — in this lesson you'll learn the core Terraform workflow for managing cloud infrastructure reliably and repeatably. Terraform (Infrastructure as Code) uses HashiCorp Configuration Language (HCL) to declare desired resource state, then reconciles real infrastructure to match that state. A concise, consistent workflow reduces drift, eases reviews, and enables safe automation with CI/CD.

Core workflow steps (high level)

* Write configuration: define resources and desired state in `.tf` files (HCL).
* Initialize the workspace: download provider plugins and configure the backend.
* Plan changes: generate an execution plan that previews changes.
* Apply changes: execute the plan to change real infrastructure.
* Destroy (optional): remove infrastructure created by Terraform.

Each step exists to make infrastructure changes deliberate and auditable. In practice you should also: manage state (local or remote), use version control for configurations, review plans before applying, and integrate Terraform into CI/CD.

> **lightbulb** Always review a `terraform plan` output (or plan file) before running `terraform apply`. Plans are your primary safety check to avoid unintended changes.

Common commands summary

```bash theme={null}
