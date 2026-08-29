# Whats New in the Terraform Associate 004 Exam

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Course-Introduction/Whats-New-in-the-Terraform-Associate-004-Exam/page

Overview of changes from Terraform Associate 003 to 004 exam, highlighting four new focus areas and study guidance

If you're reading this lesson, you're likely in one of two situations: you already passed the Terraform Associate 003 exam and want to know whether to upgrade, or you're new to Terraform and need to understand what's different in the 004 exam. This lesson explains the differences between the Terraform Associate 003 and 004 exams, highlights what remains the same, and shows how those changes should shape your study plan.

We cover:

* Exam availability and validity
* What stayed the same (format, delivery, question types)
* Four major additions in 004 and short examples
* Study guidance and recommended focus areas

## Exam availability and validity

The Terraform Associate 003 exam was retired on January 8, 2026 and replaced by the 004 version. After that date, the 004 exam is the only available Associate-level test. If you currently hold the 003 certification, it remains valid until its original expiration — you only need to take 004 when you recertify or upgrade.

> **lightbulb** If you currently hold the 003 certification, it remains valid for its original two-year period. When it’s time to recertify, you will take the 004 exam.

> **warning** Follow all candidate instructions on exam day (name matching, test room rules, ID requirements, etc.). Delivery providers changed in 2025 from PSI to Certiverse; adhering to the rules prevents delivery delays or disqualification.

## What stayed the same

Many core aspects of the Associate-level exam remain unchanged:

* Objectives are mostly the same but reorganized; many topics carry over with additional sub-objectives.
* Testing format, number of questions, and total time limit remain unchanged.
* Question types: multiple choice, multiple select, and true/false. HashiCorp removed fill-in-the-blank questions to reduce ambiguity.
* Delivery: online, proctored through Certiverse (migrated from PSI in 2025).
* Certification validity remains two years.

<Frame>
  <img alt="The image outlines the unchanged aspects of a Terraform certification exam, including format, delivery, question types, and validity, with 70% content overlap between versions. It features icons and text describing exam objectives, testing format, question types, delivery method, and certification validity." />
</Frame>

## High-level comparison

| Area              | 003 (Retired)              | 004 (Current)                                                                                                                          |
| ----------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Delivery provider | PSI                        | Certiverse                                                                                                                             |
| Question types    | includes fill-in-the-blank | removed fill-in-the-blank; multiple choice, multiple select, true/false                                                                |
| Coverage emphasis | Classic Associate topics   | Adds stronger emphasis on `depends_on`, lifecycle rules, `validation`, ephemeral/write-only handling, and Terraform Cloud/HCP features |
| Validity          | 2 years                    | 2 years                                                                                                                                |

## What changed — four major additions in 004

The 004 exam adds emphasis in four specific areas. These reflect Terraform language and platform evolution and should guide focused study.

<Frame>
  <img alt="The image outlines four major updates to the Terraform Associate exam, including new rules on explicit dependencies, custom validation conditions, ephemeral values, and expanded HCP Terraform coverage." />
</Frame>

1. Explicit dependencies and lifecycle rules

* 004 explicitly tests `depends_on` usage and lifecycle behaviors such as `create_before_destroy` and `prevent_destroy`. Know differences between implicit graph dependencies (resource references) and explicit `depends_on`, and how lifecycle meta-arguments change resource replacement and ordering.

Example: explicit dependency and lifecycle usage

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_lb_target_group.web_tg]
}
```

2. Custom validation conditions

* Expect questions about constraining inputs using `validation` blocks inside variable declarations and other configuration-level guards. Understand how to craft expressions that validate values before apply, and how errors surface to the user.

Example: variable validation

```hcl theme={null}
variable "environment" {
  type    = string
  default = "dev"

  validation {
    condition     = contains(["dev","staging","prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod"
  }
}
```

3. Ephemeral values and write-only arguments

* Handling secrets and preventing sensitive values from being written to state is emphasized. Learn about `sensitive = true`, input-only/write-only arguments in providers/resources, and patterns to avoid storing secrets (e.g., data sources, external secret stores, or ephemeral workflows).

Example: marking a variable as sensitive

```hcl theme={null}
variable "db_password" {
  type      = string
  sensitive = true
}
```

Also know provider/resource-specific write-only behaviors where the provider never stores the secret in state.

4. Expanded HashiCorp Terraform Cloud (HCP Terraform) coverage

* Terraform Cloud (HCP Terraform) topics receive wider coverage: workspaces, VCS integration, runs/workspaces lifecycle, policy & governance (e.g., Sentinel or OPA-style enforcement), projects, and collaboration features. Understand when to use Terraform Cloud managed capabilities versus self-hosted solutions.

Tip: Hands-on practice with Terraform Cloud workspaces, runs, and governance controls will help you answer platform-related questions confidently. For an introduction, see the Terraform Cloud learning resources linked below.

These four areas represent most of the new emphasis compared to 003. If you already understand the remaining Associate-level content, focusing on these topics will prepare you for 004.

## Study guidance and recommended focus

How you study will depend on your starting point:

* If you passed 003 previously:
  * Approximately 70% of content transfers directly. Prioritize the four new focus areas listed above.
  * Practice examples:
    * Create small configurations that force Terraform to replace resources, and test `create_before_destroy` vs default behavior.
    * Add `validation` blocks to variables and intentionally trigger validation errors.
    * Mark variables as `sensitive` and examine plan/state behavior; explore provider docs for write-only arguments.
    * Use Terraform Cloud: create workspaces, connect a VCS repo, and inspect run logs and policy checks.

<Frame>
  <img alt="The image features a promotional graphic for Terraform Certified Associate, including study tips for advancing knowledge, alongside two individuals studying, each wearing headphones and working with notebooks and laptops in a cozy environment." />
</Frame>

* If you are new to Terraform or didn’t take 003:
  * Follow the 004 exam objectives end-to-end: read the objectives list, complete hands-on labs, and emphasize the four highlighted topics as you progress.
  * Build practical exercises: create simple infra changes, test lifecycle behavior, validate variables, and integrate Terraform Cloud workflows.

Overall, the candidate experience is familiar, but the 004 exam shifts focus toward recent Terraform language features and Terraform Cloud platform capabilities. Prioritize hands-on practice in the four areas above, and review the standard Associate topics (state, modules, providers, CLI workflow, and basic resource management).

## Useful links and references

* HashiCorp: Terraform documentation — [https://www.terraform.io/docs](https://www.terraform.io/docs)
* Terraform Cloud overview — [https://www.terraform.io/cloud](https://www.terraform.io/cloud)
* Terraform language reference (graph, lifecycle, validation, sensitive) — [https://www.terraform.io/language](https://www.terraform.io/language)
* Practice Terraform Cloud: [HashiCorp : Terraform Cloud](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud)

So let’s get into the actual content and get started.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/ab6bded4-e4cf-4208-9368-f5313fcfcf03/lesson/7d47d4d2-367b-4b32-b8a8-b172d0b2b40e)
