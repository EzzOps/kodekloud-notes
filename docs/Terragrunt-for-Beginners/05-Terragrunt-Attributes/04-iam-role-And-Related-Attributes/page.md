# iam role And Related Attributes

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Attributes/iam-role-And-Related-Attributes/page

This lesson explores Terragrunt’s iam_role attribute for assuming AWS IAM roles, enhancing security and credential management in Terraform commands.

In this lesson, we’ll dive into Terragrunt’s `iam_role` attribute, which tells Terraform to assume an AWS IAM role before executing any commands. Leveraging an IAM role helps enforce least privilege, centralize credential management, and maintain clear audit trails for your infrastructure changes.

<Frame>
  ![The image illustrates "iam\_role and Related Attributes," featuring icons for Terraform commands and AWS Identity and Access Management (IAM), with a focus on "Purpose."](../../../../images/kodekloud.com/kk-media/image/upload/v1752884274/notes-assets/images/Terragrunt-for-Beginners-iam-role-And-Related-Attributes/iam-role-attributes-terraform-aws.jpg)
</Frame>

## Key IAM Role Attributes

| Attribute                        | Description                                                                                | Required / Default               |
| -------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------- |
| iam\_role                        | The Amazon Resource Name (ARN) of the IAM role that Terragrunt will assume.                | Required                         |
| aws\_profile                     | The name of the AWS CLI profile to source credentials from. Falls back to default/profile. | Optional                         |
| iam\_assume\_role\_duration      | Session duration (in seconds) for the assumed role.                                        | Optional (default: 3600 seconds) |
| iam\_assume\_role\_session\_name | Custom session name for auditing and logging purposes when assuming the role.              | Optional                         |

<Callout icon="triangle-alert">
  Be careful when extending the `iam_assume_role_duration`. While longer sessions reduce the frequency of re-authentication, they also increase the window of risk if credentials are compromised.
</Callout>

<Frame>
  ![The image shows a diagram related to "iam\_role and Related Attributes," featuring two attributes: "iam\_assume\_role\_duration" and "iam\_assume\_role\_session\_name," with a section labeled "Considerations" below.](../../../../images/kodekloud.com/kk-media/image/upload/v1752884275/notes-assets/images/Terragrunt-for-Beginners-iam-role-And-Related-Attributes/iam-role-attributes-diagram-considerations.jpg)
</Frame>

***

## Troubleshooting: Missing Permissions

If you omit `iam_role` and your AWS user doesn’t have direct permissions, running `terragrunt apply` will fail with an AccessDenied error:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws/?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

inputs = {
  name = "KodeKloud-VPC"
  cidr = "10.100.0.0/16"
}

download_dir    = "../.terragrunt-kodekloud"
prevent_destroy = false
skip            = false
```

```bash theme={null}
$ terragrunt apply
Error: AccessDenied: User is not authorized to perform: ec2:CreateVpc
```

***

## Enabling IAM Role Assumption

1. **Create or identify** an IAM role—for example,\
   `arn:aws:iam::654654587009:role/terragrunt-role`—with the necessary permissions.
2. **Add** the `iam_role` attribute to your Terragrunt configuration:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws/?version=5.8.1"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

inputs = {
  name = "KodeKloud-VPC"
  cidr = "10.100.0.0/16"
}

download_dir    = "../.terragrunt-kodekloud"
prevent_destroy = false
skip            = false

iam_role = "arn:aws:iam::654654587009:role/terragrunt-role"
```

3. **Run** the apply command:

```bash theme={null}
terragrunt apply
```

Terragrunt will first assume the specified role, then execute Terraform:

```text theme={null}
Plan: 4 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

Enter a value: yes

aws_vpc.this[0]: Creating...
...
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
```

<Callout icon="lightbulb">
  By specifying `iam_role`, you restrict deployments to users who can assume the designated role—aligning with AWS security best practices for auditable, least-privilege operations.
</Callout>

## References

* [Terragrunt Documentation: iam\_role Attribute](https://terragrunt.gruntwork.io/docs/reference/config-blocks#iam_role)
* [AWS IAM User Guide: AssumeRole](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html)
* [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/1a2a45b4-e7d1-4af2-a897-7ebf83a4350e/lesson/33e40116-98cf-46bd-a576-5cd34d256bea" />
</CardGroup>
