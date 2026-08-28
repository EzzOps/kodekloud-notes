# This policy uses the Sentinel tfplan/v2 import to require that
import "tfplan-functions" as plan

# Allowed EC2 Instance Types
# Include "null" to allow missing or computed values
allowed_types = ["t2.micro"]

# Get all EC2 instances
allEC2Instances = plan.find_resources("aws_instance")

# Filter to EC2 instances with violations (prints warnings for violations)
violatingEC2Instances = plan.filter_attribute_not_in_list(allEC2Instances, "instance_type", allowed_types, true)

# Count violations
violations = length(violatingEC2Instances["messages"])

# Main rule: no violations allowed
main = rule {
    violations == 0
}
```

This policy permits only instances with the type `t2.micro`. The enforcement level is set to **soft-mandatory**, which informs you of policy violations while still allowing you to override them if necessary.

A typical Sentinel policy module configuration might look like:

```hcl theme={null}
module "tfplan-functions" {
  source = "../common-functions/tfplan-functions.sentinel"
}

module "tfstate-functions" {
  source = "../common-functions/tfstate-functions.sentinel"
}

module "tfconfig-functions" {
  source = "../common-functions/tfconfig-functions.sentinel"
}

module "aws-functions" {
  source = "./aws-functions/aws-functions.sentinel"
}

policy "restrict-ec2-instance-type.sentinel" {
  source            = "./restrict-ec2-instance-type.sentinel"
  enforcement_level = "soft-mandatory"
}
```

Update your policy set configuration with the correct custom paths for your policy definitions and click **Update Policy Set**.

<Frame>
  ![The image shows the "Policy Sets" page in Terraform Cloud, displaying a policy set named "policyset1" with options for managing Sentinel policies.](https://kodekloud.com/kk-media/image/upload/v1752884138/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Cloud-Demo/frame_1430.jpg)
</Frame>

To test policy enforcement, update your workspace's variable for `instance_type` from `t2.micro` to another value, such as `m5.large`, then run a new execution plan.

<Frame>
  ![The image shows a Terraform Cloud interface displaying workspace variables, including keys like "ami," "region," and "instance\_type," with some marked as sensitive.](https://kodekloud.com/kk-media/image/upload/v1752884139/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Cloud-Demo/frame_1610.jpg)
</Frame>

During the plan execution, Terraform Cloud will perform a policy check. Since `m5.large` is not allowed according to the Sentinel policy, the check will soft-fail and produce an error message similar to:

```text theme={null}
1 points evaluated.

## Policy 1: policyset1/restrict-ec2-instance-type.sentinel (soft-mandatory)

Result: false

Description:
This policy uses the Sentinel tfplan/v2 import to require that all EC2 instances have instance types from an allowed list

Print messages:
aws_instance.terraform-cloud-demo has instance_type with value m5.large that is not in the allowed list: [t2.micro]

./restrict-ec2-instance-type.sentinel:24:1 - Rule "main"
Description:
Main rule

Value:
false
```

<Callout icon="lightbulb">
  As the organization owner, you have the ability to override the policy error and proceed with the updated configuration.
</Callout>

Upon confirmation, the resource is recreated with the modified instance type, and the updated state is visible in the **State** tab.

***

## 6. Organization Settings and Final Thoughts

Review and update your organization settings by navigating to your organization page (e.g., `KodeKloud-Terraform-Cloud-Demo01`). Here, you can adjust details, manage teams, and view billing information.

<Frame>
  ![The image shows a Terraform Cloud workspace interface with one workspace named "terraform-cloud," which has a run status of "Applied" and indicates success.](https://kodekloud.com/kk-media/image/upload/v1752884140/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Cloud-Demo/frame_1040.jpg)
</Frame>

<Frame>
  ![The image shows a Terraform Cloud settings page for version control, connected to a GitHub repository, with options for automatic run triggering and speculative plans.](https://kodekloud.com/kk-media/image/upload/v1752884123/notes-assetshttps://kodekloud.com/kk-media/image/upload/v1752884123/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Cloud-Demo/frame_1000.jpg)
</Frame>

This lesson provided a comprehensive walkthrough of using Terraform Cloud—from account creation to advanced policy enforcement with Sentinel. For further insights, explore the accompanying multiple-choice quiz to test your knowledge of Terraform Cloud features.

Happy provisioning!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/5a83b210-e98f-4f9b-9c4e-a2b03d28d619/lesson/b4f0a62d-042e-4619-90a8-53134e3da7d1" />
</CardGroup>


# Terraform Cloud Introduction

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Terraform-Cloud/Terraform-Cloud-Introduction/page

Learn how organizations can run Terraform in production using Terraform Cloud for team collaboration and secure state management.

In this lesson, you will learn how organizations can run Terraform in production using Terraform Cloud. Up until now, you have seen how to provision, manage, and destroy infrastructure with Terraform. However, all these operations have been from the perspective of a single user—typically a developer using Terraform configuration files stored locally. Consequently, the state file generated during these operations is also stored on your local machine.

<Callout icon="triangle-alert">
  Storing local state files is not recommended for team environments. While it is technically possible to share both configuration and state files with your team, doing so exposes sensitive information about your infrastructure, posing significant security risks. Instead, always keep configuration files in your version control system (VCS) and store state files using remote backends like Amazon S3, Google Cloud Storage, Azure RM, or Terraform Cloud.
</Callout>

<Frame>
  ![The image illustrates HCP Terraform's integration with version control systems, showing .tf files are managed, while terraform.tfstate files are not.](https://kodekloud.com/kk-media/image/upload/v1752884141/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Cloud-Introduction/frame_60.jpg)
</Frame>

Consider this scenario: you and a colleague are collaborating on a new Terraform project. You develop the configuration files and verify that everything works using Terraform version 1. At the same time, your colleague is using an older Terraform version from previous projects. When attempting to update the configuration and apply changes, your colleague encounters an error due to backward incompatibility. To resolve this issue, they must upgrade their local Terraform binary, potentially causing unexpected issues in other projects.

Terraform Cloud addresses these challenges by providing a Software as a Service (SaaS) environment that supports team collaboration on Terraform workflows. With Terraform Cloud, you gain the following benefits:

* Shared state management without the need for external remote backends.
* Secure storage of state files within Terraform Cloud.
* Execution of the core Terraform workflow—"terraform init", "terraform plan", and "terraform apply"—on remote Terraform Cloud servers, ensuring that all team members work in a consistent and reliable environment.
* Elimination of compatibility issues associated with different local Terraform versions.

In addition to shared state and consistent environments, Terraform Cloud offers several features that enhance team collaboration:

* A user-friendly interface to manage Terraform workflows.
* Access controls to ensure proper permissions management.
* Secret management for securely storing sensitive information.
* A private registry for sharing reusable modules.
* Policy controls for enforcing compliance standards.

<Frame>
  ![The image lists features of HCP Terraform, including shared state, consistent environment, UI interface, secret management, access controls, private registry, and policy controls.](https://kodekloud.com/kk-media/image/upload/v1752884143/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Cloud-Introduction/frame_180.jpg)
</Frame>

In the upcoming sections and demos, we will explore these features in much more detail. For more information on Terraform and its ecosystem, consider visiting the following resources:

* [Terraform Documentation](https://www.terraform.io/docs)
* [Terraform Cloud Overview](https://www.terraform.io/cloud)

Happy exploring!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/5a83b210-e98f-4f9b-9c4e-a2b03d28d619/lesson/5f80351e-e44e-469f-a423-fd24c10704b7" />
</CardGroup>
