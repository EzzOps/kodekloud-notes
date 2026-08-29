# Imperative steps (conceptual)
aws ec2 run-instances --image-id ami-0123456789abcdef0 --count 1 --instance-type t2.micro
# SSH into the instance and run provisioning commands
# Manually attach networking/security settings if needed
```

In the imperative workflow, you must manage order, retries, and idempotency yourself.

<Callout icon="lightbulb">
  Because you describe the desired final state rather than the steps to get there, Terraform can compute an efficient change plan, manage dependencies automatically, and provide a predictable `plan`/`apply` workflow.
</Callout>

## Benefits of Terraform's declarative model

* Focus on intent: declare *what* you want; avoid scripting *how* to do it.
* Dependency graph: Terraform understands inter-resource relationships and orders operations correctly.
* Minimal changes: Terraform computes the smallest set of actions to reconcile current and desired state.
* Safe workflow: `terraform plan` lets you review proposed changes before applying them.
* State management: Terraform stores state to map configuration to real resources; remote state and locking enable collaboration.

## Declarative vs Imperative — quick comparison

| Aspect              | Declarative (Terraform)           | Imperative (CLI / scripts)         |
| ------------------- | --------------------------------- | ---------------------------------- |
| Primary intent      | Describe final state              | Describe steps/commands            |
| Change computation  | Engine computes diff and plan     | You control changes and order      |
| Idempotency         | Built-in via plan/apply and state | Must be implemented in scripts     |
| Dependency handling | Automatic dependency graph        | Manually managed by scripting      |
| Review before apply | `terraform plan`                  | Depends on tooling / manual checks |

## Typical Terraform workflow

1. Write configuration files (`.tf`) that declare resources and inputs.
2. Initialize the working directory: `terraform init`.
3. Preview planned actions: `terraform plan`.
4. Apply changes: `terraform apply`.
5. Manage state: use remote state backends (e.g., S3, Terraform Cloud) and enable locking for team workflows.

## When to choose declarative vs imperative

* Choose declarative (Terraform) when you want reproducible, version-controlled infrastructure and automatic dependency resolution across multiple resources and providers.
* Choose imperative scripts when performing one-off ad-hoc operations or when you need very fine-grained procedural control that cannot be easily expressed in a declarative model.

## References and further reading

* [Terraform documentation](https://www.terraform.io/docs)
* [Kubernetes: Declarative vs Imperative](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/a4e5f0e2-a9a1-4bf8-a592-0157c396577b" />
</CardGroup>


# Introduction to Terraform

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Introduction-to-Terraform/page

Introductory guide to HashiCorp Terraform, explaining HCL, infrastructure as code, benefits, provider ecosystem, provisioning workflows, modules, state management, and practical next steps

All right, welcome.

In this lesson we'll dive into HashiCorp Terraform. Whether you're new to infrastructure automation or expanding your DevOps skills, this article introduces Terraform's core concepts and explains why it is an industry-standard tool for managing infrastructure as code (IaC).

Let's start with Terraform's foundations and what makes it different from manual provisioning.

Terraform was created by HashiCorp as part of their suite of infrastructure tools and has transformed how teams provision and manage infrastructure. What sets Terraform apart is its declarative model: instead of scripting step-by-step imperative actions, you declare the desired end state of infrastructure and Terraform computes the required changes to reach that state.

<Frame>
  <img alt="The image provides a brief introduction to Terraform, mentioning its creation by HashiCorp and its use of a declarative approach. It also displays various logos of HashiCorp tools." />
</Frame>

Core ideas: HCL and Infrastructure as Code

You describe resources and relationships using HCL — the HashiCorp Configuration Language. HCL is readable, expressive, and intended to be both human-friendly and machine-friendly. Think of HCL as the blueprint for your infrastructure: structured, reusable, and versionable.

Infrastructure as Code (IaC) means defining your infrastructure with text files instead of manual clicks in cloud consoles. IaC files are version-controlled, reviewable, and reproducible, which enables safer automation and better collaboration.

Three core Terraform capabilities:

* Codify infrastructure: Capture manual cloud steps in maintainable, repeatable code that can be applied or destroyed on demand.
* Standardize workflows: Reuse patterns and modules to enforce consistent infrastructure practices across teams.
* Platform-agnostic execution: Apply the same workflow across providers—AWS, Azure, Google Cloud, Kubernetes, and many API-backed services.

<Frame>
  <img alt="The image explains Terraform as an industry-standard Infrastructure as Code (IaC) tool that automates provisioning, management, and versioning of infrastructure. It highlights benefits such as codifying infrastructure and standardizing workflows." />
</Frame>

Key benefits of using Terraform

Version control and auditability

* Treat infrastructure like application code. Changes are tracked in a VCS, producing an auditable history that simplifies troubleshooting and rollbacks.

Automation and efficiency

* Terraform removes repetitive manual provisioning, reduces human error, and accelerates deployments. Once codified, configurations are consistently reproducible.

Scalability and flexibility

* Scale by changing code (instance counts, sizes, subnets). Manage multiple environments from a single codebase using variables, workspaces, or backend configurations.

Collaboration

* Teams collaborate using pull requests, code reviews, and shared modules, bringing software engineering practices to infrastructure management.

Consistency and repeatability

* Infrastructure manifests produce identical environments every time, closing the gap between testing and production.

Summary table — What Terraform gives you

| Benefit         | Why it matters            | Example                                             |
| --------------- | ------------------------- | --------------------------------------------------- |
| Version control | Full history and rollback | Use `git` to track `.tf` files                      |
| Consistency     | Repeatable environments   | Same HCL yields identical infra                     |
| Reuse           | Reduce duplication        | Publish modules for common patterns                 |
| Parallelism     | Faster provisioning       | Terraform creates independent resources in parallel |
| Cost control    | Ephemeral environments    | Spin up tests and destroy to avoid charges          |

<Frame>
  <img alt="The image outlines the benefits of Terraform, highlighting version control, scalability, collaboration, automation, and consistency. It includes explanations for each feature, emphasizing efficiency and transparency in infrastructure management." />
</Frame>

Platform-agnostic design

Terraform’s provider system enables management of resources across many platforms using the same declarative approach. Providers translate HCL into API calls for services like AWS, Azure, Google Cloud, Kubernetes, GitHub, and Infoblox.

This single control plane is powerful for multi-cloud deployments and migrations because you can reuse knowledge and patterns across providers.

<Callout icon="lightbulb">
  Terraform automates provisioning but does not replace domain knowledge. Be familiar with the platform you’re targeting (networking, compute, identities) before automating it with Terraform.
</Callout>

<Frame>
  <img alt="The image illustrates Terraform's platform agnostic nature, showing its compatibility with various cloud platforms like Kubernetes, AWS, Azure, Google Cloud, and other services such as GitHub and Infoblox." />
</Frame>

Provisioning: console vs. Terraform

Traditional/manual provisioning

* Typically done by clicking through cloud consoles or running ad-hoc commands. This approach is error-prone, slow, and hard to reproduce across environments.

<Frame>
  <img alt="The image illustrates the traditional process of provisioning resources using Microsoft Azure, highlighting the creation of virtual machines, containers, and networks." />
</Frame>

Terraform provisioning

* With Terraform, you declare resources, attributes, and relationships in HCL files. Terraform reads those files, computes a change plan, and executes the actions required to match the declared state.

Example resource (EC2 instance) in HCL:

```hcl theme={null}
resource "aws_instance" "ubuntu_server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public_subnets["public_subnet_1"].id
  vpc_security_group_ids      = [aws_security_group.vpc_ping.id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.generated.key_name

  connection {
    user        = "ubuntu"
    private_key = tls_private_key.generated.private_key_pem
    host        = self.public_ip
  }
}
```

Apply this same HCL definition whenever you need the same resource; Terraform manages lifecycle and reduces configuration drift.

Code reusability and variables

Terraform encourages modular design. You can write a generic resource or module and change its inputs using variables to produce different outcomes for different environments or roles.

Example using variables:

```hcl theme={null}
resource "aws_instance" "basic_server" {
  ami                         = data.aws_ami.image.id
  instance_type               = var.instance_size
  subnet_id                   = aws_subnet.public_subnets.id
  vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.generated.key_name
}
```

By adjusting `var.instance_size`, `ami`, or `subnet` inputs, the same tested codebase can deploy different server types.

Collaboration with IaC and Git workflows

Terraform integrates well with Git-based workflows. Teams work in feature branches, submit pull requests for infrastructure changes, and use CI to run `terraform fmt`, `terraform validate`, and `terraform plan` before applying to production. This enforces peer review and reduces configuration mistakes.

<Frame>
  <img alt="The image is a visual representation of &#x22;Infrastructure as Code&#x22; with a progression diagram labeled &#x22;Main Branch,&#x22; featuring Terraform logos on a purple background." />
</Frame>

Why organizations adopt IaC with Terraform

* Speed and parallelism: Terraform creates independent resources in parallel (respecting dependencies), reducing overall provisioning time.
* Standardized, shareable components: Reusable modules increase consistency across teams and products.
* Ephemeral environments and cost control: Quickly spin up test environments, run validations, and tear them down to avoid unnecessary charges.
* Predictability and observability: Plans and state enable predictable updates and easier reasoning about changes.

Practical next steps

* Learn HCL syntax and Terraform core commands: `terraform init`, `terraform plan`, `terraform apply`, `terraform destroy`.
* Practice with a cloud provider account and small modules.
* Integrate Terraform into your Git workflows and CI pipelines.

<Callout icon="warning">
  Protect Terraform state and secrets: state files can contain sensitive information. Use secure remote backends (e.g., `s3` with encryption or HashiCorp Cloud) and enable state locking to prevent concurrent modifications.
</Callout>

Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Documentation](https://www.terraform.io/docs)
* [KodeKloud — AWS Networking Fundamentals](https://learn.kodekloud.com/user/courses/aws-networking-fundamentals)
* [KodeKloud — Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [KodeKloud — AWS IAM](https://learn.kodekloud.com/user/courses/aws-iam)

Overall, Infrastructure as Code with Terraform drives speed, consistency, and collaboration across teams—making infrastructure provisioning more predictable and maintainable. As you continue learning Terraform, apply these concepts in small, repeatable projects to see these benefits realized in real deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/ad20a8c8-1323-495c-8835-c52288feda6a" />
</CardGroup>
