# What is Infrastructure as Code

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Infrastructure-as-Code-Fundamentals/What-is-Infrastructure-as-Code/page

Explains Infrastructure as Code, its declarative approach, benefits, common tools, best practices, and examples for automating and versioning cloud infrastructure.

Infrastructure as Code

What exactly is infrastructure as code (IaC)?

Infrastructure as Code (IaC) is the practice of defining, provisioning, and managing infrastructure using machine-readable configuration files instead of manually clicking through cloud consoles or running ad-hoc CLI commands. These configuration files—typically written in HCL, YAML, or JSON—act as the single source of truth describing the desired infrastructure state, enabling automation, repeatability, and versioning.

At its core, IaC treats infrastructure like software: definitions are stored in version control, reviewed, tested, and deployed through CI/CD pipelines. When an IaC tool applies your configuration, it reconciles the actual cloud state with the declared desired state—creating, updating, or destroying resources as needed.

<Frame>
  <img alt="The image explains Infrastructure as Code (IaC), highlighting its use of machine-readable files for infrastructure management and code for managing servers, networks, configurations, and deployments." />
</Frame>

Servers, networks, access rules, configuration items, and deployments are typically declared (what you want) rather than scripted imperatively (how to do it). This declarative approach enables several important properties that make IaC effective at scale.

Key IaC properties

| Property                  | What it means                                                  | Why it matters                                  |
| ------------------------- | -------------------------------------------------------------- | ----------------------------------------------- |
| Idempotency               | Re-applying the same configuration yields the same result      | Safe retries, predictable provisioning          |
| Immutability patterns     | Prefer replacing resources over in-place mutation              | Simpler rollbacks and cleaner state transitions |
| Drift detection           | Detects when live infrastructure diverges from declared config | Enables remediation and compliance              |
| Versioning & auditability | Configurations live in Git (or similar) with history           | Traceability, code review, and rollback         |

> **lightbulb** IaC can be declarative (you describe the desired end state) or imperative (you script the steps to get there). Most modern IaC tools favor declarative approaches because they simplify reconciliation and reduce complexity.

Key benefits of Infrastructure as Code

* Speed and efficiency\
  Reusable definitions let you provision entire environments in minutes instead of hours or days, reducing manual effort and human error.

* Consistency and standardization\
  Shared configuration files ensure environments are built consistently, minimizing configuration drift and differences across environments.

* Version control and auditability\
  Storing infrastructure definitions in Git enables change tracking, code reviews, and controlled rollbacks.

* Collaboration and automation\
  Teams can collaborate on infrastructure changes and integrate provisioning into CI/CD pipelines, aligning infrastructure changes with DevOps practices.

<Frame>
  <img alt="The image is an infographic titled &#x22;Benefits of IaC&#x22; highlighting four key advantages: Speed and Efficiency, Consistency and Standardization, Version Control and Auditability, and Collaboration and Automation." />
</Frame>

These advantages explain why IaC is the foundational approach for managing cloud infrastructure at scale.

Common IaC approaches and tools

Below is a concise guide to common approaches and representative tools used in practice.

| Tool / Project                 | Approach                                   | Typical use case                                                     |
| ------------------------------ | ------------------------------------------ | -------------------------------------------------------------------- |
| Terraform                      | Declarative (HCL)                          | Multi-cloud provisioning and orchestration                           |
| CloudFormation / ARM templates | Declarative (YAML/JSON)                    | AWS or Azure native resource provisioning                            |
| Pulumi                         | Imperative or declarative (multi-language) | Infrastructure in general-purpose languages (TypeScript, Python, Go) |
| Ansible                        | Imperative / declarative mix (YAML)        | Configuration management, app deployment, and provisioning           |
| Kubernetes manifests / Helm    | Declarative (YAML & templating)            | Container orchestration and app configuration                        |

Examples — configuration snippets

Terraform (HCL) example:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
  }
}
```

CloudFormation (YAML) snippet:

```yaml theme={null}
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-example-bucket
```

Best practices for IaC

* Keep state and secrets secure: use remote state backends with encryption (e.g., Terraform state in S3 with DynamoDB locking) and secret stores (HashiCorp Vault, AWS Secrets Manager).
* Modularize configurations: create reusable modules or templates for common patterns (VPCs, networks, databases).
* Enforce code review and CI: apply linters, validation, and plan/review steps in pipelines before applying changes.
* Implement drift detection and monitoring: schedule checks or use automation to detect and correct drift.
* Test infrastructure code: use unit tests, integration tests, and ephemeral test environments to validate changes.

> **warning** Be careful with state, locking, and secrets. Mismanaged state files or unencrypted secrets in configs can lead to security risks or resource conflicts. Always use remote state locking and secure secret storage.

Links and references

* Terraform: [https://www.terraform.io/](https://www.terraform.io/)
* Pulumi: [https://www.pulumi.com/](https://www.pulumi.com/)
* AWS CloudFormation: [https://docs.aws.amazon.com/cloudformation/](https://docs.aws.amazon.com/cloudformation/)
* Azure Resource Manager (ARM) templates: [https://docs.microsoft.com/azure/azure-resource-manager/](https://docs.microsoft.com/azure/azure-resource-manager/)
* Ansible: [https://www.ansible.com/](https://www.ansible.com/)

These resources will help you explore IaC tooling and patterns that fit your team’s needs and cloud strategy.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ba3df1b5-1b9a-4f11-b32a-218c32aa1614/lesson/ff9624bd-1873-417d-9b8e-8ff39dd061ac)
