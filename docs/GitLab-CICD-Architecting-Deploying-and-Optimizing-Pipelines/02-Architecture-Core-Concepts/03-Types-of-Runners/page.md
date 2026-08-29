# Types of Runners

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Types-of-Runners/page

This guide explores GitLab Runners, detailing Shared and Self-Managed options for executing CI/CD jobs based on organizational needs.

Building on pipeline definitions and execution concepts, GitLab CI/CD consists of three core components:

1. **GitLab Server**
2. **Runner**
3. **Executor**

In this guide, we’ll dive into **Runners**—the agents that pick up and execute your CI/CD jobs. You can choose between **Shared Runners** hosted by GitLab or **Self-Managed Runners** on your own infrastructure.

## Runner Options at a Glance

| Aspect              | Shared Runners                         | Self-Managed Runners                             |
| ------------------- | -------------------------------------- | ------------------------------------------------ |
| Hosting             | Hosted by GitLab                       | On your own servers or cloud instances           |
| Setup & Maintenance | Fully managed by GitLab                | Requires in-house installation and upkeep        |
| Configuration       | Predefined, limited customization      | Fully configurable environment                   |
| Scalability         | Auto-scaled to meet demand             | Manual scaling and provisioning                  |
| Security Boundary   | Shared across multiple projects        | Isolated per project or group                    |
| Cost                | Included in GitLab subscription tiers  | Infrastructure, licensing, and maintenance costs |
| Ideal Use Case      | General-purpose workloads, small teams | Strict compliance, custom tooling, high control  |

![The image is a comparison table of GitLab Runners, detailing features of Shared Runners and Self-Managed Runners, including aspects like hosting, setup, maintenance, control, scalability, security, cost, and suitability for different team sizes.](https://kodekloud.com/kk-media/image/upload/v1752877039/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Types-of-Runners/gitlab-runners-comparison-table.jpg)

Choosing between Shared and Self-Managed Runners depends on your organization’s size, security requirements, and operational preferences.

***

## Shared Runners

Shared Runners are provided as a service by GitLab. They serve jobs from any project in a GitLab SaaS instance on a first-come, first-served basis.

### Pros

* **Zero setup**: Ready to use out of the box.
* **Cost-effective**: Included in most GitLab subscription tiers.
* **Auto-scaled**: Capacity adjusts automatically to meet job demand.

### Cons

* **Limited customization**: Cannot install additional software or change low-level settings.
* **Resource contention**: Performance may vary under heavy load.
* **Shared security boundary**: All projects share the same runner environment.

> **lightbulb** Shared Runners are ideal for small teams or open-source projects where ease of use outweighs the need for deep customization.

***

## Self-Managed Runners

Self-Managed Runners run on your own infrastructure—whether on-premises or in the cloud—giving you total control over configuration, security, and performance.

### Pros

* **Full control**: Install custom software, tune performance, and manage updates.
* **Dedicated resources**: Reduce job wait times and ensure consistent build performance.
* **Isolated environment**: Minimize cross-project interference and meet strict compliance requirements.

### Cons

* **Operational overhead**: Requires expertise to set up, monitor, and maintain.
* **Manual scaling**: You must provision or decommission machines as demand fluctuates.
* **Additional costs**: Includes hardware, licensing, and ongoing maintenance expenses.

> **triangle-alert** Ensure you implement proper security measures (firewalls, secrets management, network policies) when exposing self-managed runners to public or untrusted networks.

***

## Links and References

* [GitLab Runner Documentation](https://docs.gitlab.com/runner/)
* [GitLab CI/CD Overview](https://docs.gitlab.com/ee/ci/)
* [Best Practices for GitLab CI/CD](https://docs.gitlab.com/ee/ci/best_practices/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/d271ea06-640f-4a4c-8c4e-4e53bc0bd10b)
