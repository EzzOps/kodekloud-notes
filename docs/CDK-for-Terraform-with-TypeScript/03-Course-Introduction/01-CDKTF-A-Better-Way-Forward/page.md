# CDKTF A Better Way Forward

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/CDKTF-A-Better-Way-Forward/page

Introduces CDKTF, using general-purpose languages to generate Terraform configuration for reusable, testable infrastructure while preserving Terraform providers, state, and CLI workflows.

In this lesson we introduce CDKTF (Cloud Development Kit for Terraform) as a practical alternative to authoring infrastructure purely in HCL. CDKTF enables you to define infrastructure using familiar programming languages (TypeScript, Python, Java, C#, Go) while still leveraging Terraform’s provider ecosystem, state model, and CLI workflows. This hybrid approach helps teams build reusable, testable abstractions without losing compatibility with existing Terraform modules.

## Layered architecture of CDKTF

Below is a concise, layered view of how CDKTF maps language constructs to Terraform execution:

|                          Layer | Purpose                                                                                                                 | Notes                                                                                 |
| -----------------------------: | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
|    Top — Programming languages | Write infrastructure-as-code using general-purpose languages (TypeScript, Python, Java, C#, Go).                        | Use loops, classes, functions, modules, packages, and existing testing frameworks.    |
|     Second — CDKTF abstraction | CDKTF maps high-level language constructs to Terraform configuration using jsii-based bindings and reusable constructs. | Synthesizes your code into Terraform JSON/HCL that can interoperate with HCL modules. |
|  Third — Terraform core engine | Terraform consumes the generated configuration to plan, manage state, build a resource graph, and apply changes.        | Typical commands: `terraform init`, `terraform plan`, `terraform apply`.              |
| Fourth — Providers & ecosystem | Terraform’s extensive provider catalog enables provisioning across clouds and services.                                 | CDKTF-generated configs can use any provider supported by Terraform.                  |

## How CDKTF works (workflow)

1. Author infrastructure using your language of choice and CDKTF constructs.
2. Synthesize the project with CDKTF tooling to generate Terraform configuration (JSON/HCL).
3. Use the Terraform CLI against the generated configuration:
   * `terraform init` — initialize providers and backend
   * `terraform plan` — preview changes
   * `terraform apply` — apply changes

This workflow keeps Terraform’s proven execution model while letting developers express infrastructure in full-featured programming languages.

<Callout icon="lightbulb">
  CDKTF bridges the gap between application developers and infrastructure operators: you gain the expressiveness and tooling available in general-purpose languages while retaining Terraform’s robust provider ecosystem and execution model.
</Callout>

## Why this approach helps

* Reuse and abstraction: Leverage language features (functions, classes, modules) to create higher-level constructs and shareable libraries.
* Testability: Use existing unit and integration testing frameworks for infrastructure code.
* Compatibility: Maintain full interoperability with Terraform providers, state management, and CLI workflows.
* Incremental adoption: Synthesize to standard Terraform artifacts to interoperate with existing HCL modules and teams.

## Summary

CDKTF allows teams to define infrastructure in languages they already know while producing standard Terraform configuration that benefits from Terraform’s planning, state management, and large provider catalog. The result is infrastructure automation that’s more approachable, testable, and extensible—without losing the strengths of Terraform.

## Links and references

* CDK for Terraform course: [https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript)
* Terraform basics course: [https://learn.kodekloud.com/user/courses/terraform-basics-training-course](https://learn.kodekloud.com/user/courses/terraform-basics-training-course)
* Terraform docs: [https://www.terraform.io/docs/index.html](https://www.terraform.io/docs/index.html)
* CDKTF official: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/213dc04d-3f86-4e0a-831f-021da5dc1d44" />
</CardGroup>
