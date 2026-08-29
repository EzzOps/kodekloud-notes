# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Infrastructure-as-Code-Fundamentals/Introduction/page

Overview of Infrastructure as Code fundamentals, IaC tooling categories, and when to use Terraform versus other tools.

Infrastructure as Code (IaC) fundamentals

This lesson establishes the core concepts you’ll need for the rest of the course. Infrastructure as Code (IaC) lets teams define cloud infrastructure using code instead of manual clicks in provider consoles. That shift enables faster, repeatable, auditable, and consistent deployments across environments — the same engineering discipline you apply to application code (versioning, code review, testing).

We will cover three things in this lesson:

* What IaC means and why it matters in modern cloud environments.
* The main categories of IaC tooling and when to use each type.
* Where Terraform fits in the IaC ecosystem and the problems it solves best.

Next, we’ll review the categories of IaC tools so you can choose the right tool for the right problem. Not every tool targets the same layer of the stack: some provision cloud resources, others manage configuration, and some combine both responsibilities.

| Category                          | Primary goal                                                                      | Common examples                   |
| --------------------------------- | --------------------------------------------------------------------------------- | --------------------------------- |
| Provisioning / Orchestration      | Create and manage cloud resources (networks, VMs, managed services) declaratively | Terraform, CloudFormation, Pulumi |
| Configuration Management          | Configure and maintain OS-level and application state on machines                 | Ansible, Chef, Puppet             |
| Immutable image builders          | Produce hardened machine images as artifacts                                      | Packer                            |
| GitOps / Continuous Delivery      | Reconcile cluster state from Git (declarative delivery)                           | ArgoCD, Flux                      |
| Imperative scripting / Automation | Ad-hoc automation and glue for workflows                                          | Shell scripts, SDK scripts        |

Where Terraform fits

* Declarative provisioning across multiple cloud providers and services.
* Manages infrastructure state and implements predictable change plans.
* Strong provider ecosystem and reusable modules for composability.
* Excels at multi-cloud or multi-service orchestration where a single tool should manage resource lifecycles.

<Frame>
  <img alt="The image is a slide titled &#x22;Introduction&#x22; detailing topics related to Infrastructure as Code (IaC), including explaining IaC, describing types of IaC tools, and identifying Terraform's role within the IaC ecosystem." />
</Frame>

We’ll also cover when Terraform is the right choice and when other tools might be a better fit — for example, when you need fine-grained configuration management (Ansible) or a GitOps-driven cluster delivery model (ArgoCD/Flux).

By the end of this lesson you’ll have:

* A clear mental model of IaC and tooling categories.
* Criteria to choose Terraform versus other IaC tools.
* Context for how Terraform is used in real-world cloud deployments.

<Callout icon="lightbulb">
  IaC is not just automation — it’s a way to treat your infrastructure with the same software engineering practices (versioning, code review, testing) you use for application code. This leads to more reliable and maintainable environments.
</Callout>

## Links and references

* [Terraform documentation](https://www.terraform.io/docs)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Ansible documentation](https://docs.ansible.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ba3df1b5-1b9a-4f11-b32a-218c32aa1614/lesson/e5723f7f-9239-4366-a522-1210069f425f" />
</CardGroup>
