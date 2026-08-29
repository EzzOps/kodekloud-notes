# Types of IaC Tools

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Infrastructure-as-Code-Fundamentals/Types-of-IaC-Tools/page

Overview of Infrastructure as Code tools and categories covering configuration management, server templating, and provisioning with examples and usage guidance

Infrastructure as Code (IaC) tools automate the provisioning, configuration, and lifecycle of cloud infrastructure. Before we explore specific tools, consider this real-world analogy to ground the concepts.

Imagine a university during admissions season. Thousands of applicants submit forms, transcripts, and identity proofs. If handled manually, the process becomes slow, error-prone, and inconsistent: files are misplaced, duplicate checks occur, and scaling requires more people who may interpret rules differently.

Now imagine the same process automated: standardized digital forms, automatic validation, and a repeatable approval workflow. Infrastructure as code does the same for cloud environments—automating the creation, configuration, and management of infrastructure reliably and at scale.

Common IaC solutions include Docker, Ansible, Bicep, Terraform, Salt, Puppet, Vagrant, and Packer:

<Frame>
  <img alt="The image displays logos of various Infrastructure as Code (IaC) tools, including Docker, Ansible, SaltStack, Terraform, Puppet, Vagrant, and Packer." />
</Frame>

Broadly, IaC tools fall into three main categories: configuration management, server templating, and provisioning. Below each category is explained using the university admissions analogy and concrete cloud examples.

Configuration management

Configuration management tools manage the state and software inside systems after they exist. Using the admissions analogy, this corresponds to enforcing rules for naming documents, storage locations, mandatory validations, and consistent formats—so every record conforms to the same standards regardless of who submitted it.

In cloud environments, configuration management ensures servers have the correct packages, services running, and consistent configuration across many machines. These tools are built to be idempotent: applying the same configuration repeatedly will converge the system to the desired state without creating duplicates or unintended side effects. Configuration tools may be agent-based or agentless (for example, Ansible is agentless) and typically support remote execution, drift detection, and continuous enforcement.

<Callout icon="lightbulb">
  Idempotence matters: running the same configuration multiple times should result in the same desired state, not duplicated changes or errors.
</Callout>

Examples: Ansible, Puppet, Salt.

<Frame>
  <img alt="The image is an infographic titled &#x22;Types of IaC Tools,&#x22; highlighting three aspects of configuration management: Package Management, Standard Structure, and Version Control and Idempotent." />
</Frame>

Server templating

Server templating prepares fully configured images before deployment. In the admissions analogy, this is like issuing a pre-filled application package that already contains required fields, validation rules, and workflows so every applicant receives the same, preconfigured experience.

Technically, server templating creates machine images, virtual machine snapshots, or container images that include the OS, runtime, dependencies, and application code. This supports an immutable-infrastructure approach: instead of patching a running instance, you build a new image and redeploy.

Examples: Packer (image building), Docker (container images), Vagrant (developer VM images).

<Callout icon="lightbulb">
  Immutable infrastructure increases reliability: updates are delivered by creating and deploying a new image rather than modifying running instances in place.
</Callout>

<Frame>
  <img alt="The image outlines types of Infrastructure as Code (IaC) tools, specifically server templating tools, featuring pre-installed packages, images, and immutable infrastructure. Each type is briefly described and associated with an icon." />
</Frame>

Provisioning tools

Provisioning tools operate at a higher level by creating and orchestrating the resources that make a system run. In the university example, provisioning is like building the admissions portal itself—creating the application forms, database, storage, and access controls that students use.

In the cloud, provisioning tools manage resources such as virtual machines, networks, storage accounts, databases, and load balancers. Many provisioning tools use a declarative approach: you define the desired state (number of systems, how they connect, required properties) and the tool calculates and applies the changes to reach that state. Many provisioning tools also enable immutable deployments, broad resource coverage (compute, networking, identity, security), and multi-cloud portability.

Examples: Terraform (multi-cloud declarative tool), Bicep (Azure-focused declarative language), ARM templates (Azure).

<Frame>
  <img alt="The image describes types of Infrastructure as Code (IaC) tools, focusing on provisioning tools which offer immutable deployment, resource variety, and multi-cloud support." />
</Frame>

Quick reference table

|                 Category | Purpose                                                     | Typical features                                  | Common tools                    |
| -----------------------: | ----------------------------------------------------------- | ------------------------------------------------- | ------------------------------- |
| Configuration management | Enforce and maintain software/config inside running systems | Idempotence, drift detection, remote execution    | Ansible, Puppet, Salt           |
|        Server templating | Build pre-configured images for immutable deployments       | Image building, reproducibility, faster boot      | Packer, Docker, Vagrant         |
|             Provisioning | Declare and orchestrate cloud resources and topology        | Declarative syntax, state management, multi-cloud | Terraform, Bicep, ARM templates |

Summary

* Configuration management: enforce and maintain desired state inside systems (Ansible, Puppet, Salt).
* Server templating: build immutable images or containers for consistent deployments (Packer, Docker, Vagrant).
* Provisioning: declare and orchestrate cloud resources and their relationships (Terraform, Bicep, ARM).

Next steps and references

So far we’ve covered the main types of IaC tools and when to use each approach. Next, we’ll dive into Terraform Cloud and how Terraform fits into provisioning and multi-cloud workflows.

* Terraform: [https://www.terraform.io/](https://www.terraform.io/)
* Ansible: [https://www.ansible.com/](https://www.ansible.com/)
* Docker: [https://www.docker.com/](https://www.docker.com/)
* Packer: [https://www.packer.io/](https://www.packer.io/)
* Bicep: [https://docs.microsoft.com/azure/azure-resource-manager/bicep/overview](https://docs.microsoft.com/azure/azure-resource-manager/bicep/overview)
* Azure Resource Manager (ARM) templates: [https://docs.microsoft.com/azure/azure-resource-manager/templates/](https://docs.microsoft.com/azure/azure-resource-manager/templates/)

If you want targeted examples or a comparison of tools for a specific use case (e.g., multi-cloud provisioning vs. Azure-only deployments), tell me your environment and goals and I’ll provide recommended workflows and sample configurations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ba3df1b5-1b9a-4f11-b32a-218c32aa1614/lesson/b389de20-683e-4a31-9f93-f0b3cd580790" />
</CardGroup>
