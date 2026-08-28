# Types of IAC Tools

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Introduction-to-Infrastructure-as-Code/Types-of-IAC-Tools/page

This article explains the three main categories of Infrastructure as Code tools and their purposes in the automated infrastructure lifecycle.

Before diving into OpenTofu, it’s helpful to understand the three main categories of Infrastructure as Code (IaC) tools. Each category addresses a different stage of the automated infrastructure lifecycle:

| Category                     | Purpose                                           | Examples                            |
| ---------------------------- | ------------------------------------------------- | ----------------------------------- |
| Configuration Management     | Install and manage software on existing resources | Ansible, Puppet, SaltStack          |
| Server Templating            | Build immutable VM or container images            | Packer, Vagrant, Docker             |
| Provisioning & Orchestration | Declaratively provision and manage infrastructure | OpenTofu, Terraform, CloudFormation |

***

## Configuration Management Tools

Configuration management tools automate the installation and configuration of software on servers, databases, and network devices. They ensure a consistent state across multiple hosts by defining **idempotent** code that only applies necessary changes.

<Frame>
  ![The image lists types of Infrastructure as Code (IAC) tools, highlighting features like software management, standard structure, version control, and idempotency, alongside logos for Ansible, Puppet, and SaltStack.](https://kodekloud.com/kk-media/image/upload/v1752882820/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Types-of-IAC-Tools/iac-tools-features-ansible-puppet-saltstack.jpg)
</Frame>

<Callout icon="lightbulb">
  Idempotency guarantees that running the same playbook multiple times will not alter resources that are already in the desired state.
</Callout>

Example: An Ansible playbook checks for a package before installing:

```yaml theme={null}
- name: Ensure Nginx is installed
  hosts: webservers
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
```

***

## Server Templating Tools

Server templating tools create fully configured, **immutable images**—such as VM snapshots, AWS AMIs, or Docker containers—that bundle all necessary software and dependencies. By baking the environment beforehand, you eliminate runtime configuration drift.

<Frame>
  ![The image describes types of Infrastructure as Code (IAC) tools, focusing on server templating with examples like Packer, Vagrant, and Docker. It highlights pre-installed software, dependencies, and virtual machine or Docker images.](https://kodekloud.com/kk-media/image/upload/v1752882822/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Types-of-IAC-Tools/iac-tools-server-templating-examples.jpg)
</Frame>

Key benefits:

* Consistent deployment artifacts
* Faster boot times
* Simplified rollout of updates via new image versions

***

## Provisioning & Orchestration Tools

Provisioning tools—also called orchestration tools—allow you to **declare** the desired state of your entire infrastructure: servers, databases, networking, and more. The tool then computes and applies only the changes needed to reach that state.

<Frame>
  ![The image describes types of Infrastructure as Code (IAC) tools, focusing on provisioning tools like OpenTofu, CloudFormation, and Terraform, used for deploying immutable infrastructure resources such as servers, databases, and network components.](https://kodekloud.com/kk-media/image/upload/v1752882823/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Types-of-IAC-Tools/iac-tools-provisioning-open-tofu-terraform.jpg)
</Frame>

For example, CloudFormation offers a native AWS experience, whereas OpenTofu (a Terraform fork) supports a broad ecosystem of provider plugins for multi-cloud and hybrid deployments.

### Procedural vs. Declarative Provisioning

Configuration management tools can provision resources procedurally. In Ansible, you might write:

```yaml theme={null}
- name: Provision AWS Resources
  hosts: localhost
  tasks:
    - name: Launch EC2 instances
      ec2:
        key_name: appserver
        instance_type: t2.micro
        image: ami-0d8ad3ab25e7abc51
        exact_count: 2
        region: us-east-1
```

To remove instances, you need an explicit task:

```yaml theme={null}
    - name: Terminate instances
      ec2:
        state: absent
        instance_ids: '{{ ec2.instance_ids }}'
```

<Callout icon="triangle-alert">
  Procedural scripts may inadvertently create duplicate resources if you omit repeat protection (`exact_count`) or forget teardown tasks.
</Callout>

Orchestration tools use a declarative model. In OpenTofu, you simply define:

```hcl theme={null}
resource "aws_instance" "app" {
  ami           = "ami-0d8ad3ab25e7abc51"
  instance_type = "t2.micro"
  count         = 2
  key_name      = "appserver"
  tags = {
    Name = "appserver"
  }
}
```

Running `tofu apply` ensures the actual infrastructure matches this block:

```plaintext theme={null}
> tofu apply
No changes. Your infrastructure matches the configuration.
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

***

## Choosing the Right IaC Tool

There’s no single best IaC tool. Consider:

* **AWS-only environments**: AWS CloudFormation may offer deep native integration.
* **Multi-cloud or hybrid**: OpenTofu or Terraform provide vendor-agnostic provisioning.
* **Post-provisioning configuration**: Combine orchestration tools with configuration management (e.g., OpenTofu + Ansible).

## Links and References

* [Infrastructure as Code (IaC) Concepts](https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code)
* [Terraform Registry](https://registry.terraform.io/)
* [Ansible Documentation](https://docs.ansible.com/)
* [Packer by HashiCorp](https://www.packer.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/08619b50-aae4-4bf4-a1b5-f35b400a7a72/lesson/2d085244-211b-44eb-b114-f9eb77ad50e9" />
</CardGroup>
