# follow prompts to scaffold a provider
```

Use unit tests and the cloudformation-cli contract tests to validate lifecycle behavior before registering types in your account.

## Versioning and activation

* Types support multiple versions. Register new versions when you update schema or handler code.
* Activation is explicit: you can register versions without immediately activating them for production stacks.
* Inspect versions and activation state with `describe-type` and `list-type-registrations`.
* Follow semantic versioning and document breaking changes. Activate new versions in a controlled fashion (CI/CD pipeline) to reduce disruption.

## Security and IAM

<Callout icon="warning">
  Registering types and executing handler code requires [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) permissions. Handler code might run in your account (for private types) and will need the appropriate execution environment permissions. Always review handler behavior and grant least privilege.
</Callout>

Additional security recommendations:

* Review public third‑party extension source and required permissions before use.
* Store SHPs in private, access‑controlled S3 buckets with encryption and restricted IAM roles.
* Use separate IAM execution roles for provider handlers and scope permissions using least privilege.
* Audit CloudFormation stack events and provider logs to detect unexpected behavior.

## Best practices

* Test providers thoroughly using the cloudformation-cli local and contract tests prior to registration.
* Document the provider schema and examples for consumers.
* Use semantic versioning and keep release notes for each registered type version.
* Prefer private types for internal automations; adopt public types only after security and functional review.
* Automate registration and activation via CI/CD pipelines with gating and automated tests.

## Links and references

* [CloudFormation Registry overview — AWS Docs](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [CloudFormation CLI (cloudformation-cli)](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html)
* [CloudFormation template anatomy](https://docs.aws.amazon.[SECRET_REDACTED]-anatomy.html)
* [IAM documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
* [Amazon S3](https://aws.amazon.com/s3/)

This lesson covered the CloudFormation Registry: its purpose, how to author and register resource providers, the commands you’ll commonly use, security considerations, and recommended best practices for developing and operating custom CloudFormation types.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/0a4a5ad0-b216-4c7f-9603-8ecd45254371/lesson/f657eee0-9bd1-46ed-9ab4-20136f19bd6e" />
</CardGroup>


# Demo A brief overview of the CloudFormation registry

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Registry/Demo-A-brief-overview-of-the-CloudFormation-registry/page

Overview of the AWS CloudFormation Registry showing how to find and inspect activated and public extensions, view configuration schemas, and register as a publisher.

In this demo we'll tour the AWS CloudFormation Registry to discover and inspect resource types, modules, and publishers. You’ll learn how to find activated extensions in your account, examine configuration schemas, browse public extensions, and register as a publisher.

## Navigate to the Registry

1. Open the CloudFormation console.
2. In the left-hand navigation, scroll to the **Registry** section.
3. Start with **Activated extensions** to see what’s already available in your account.

## Activated extensions — what you’ll see

Activated extensions lists resource types and modules that are available in your account. For each entry the console shows:

* Type name (for example, AWS::S3::AccessPoint)
* Whether the entry is public or private
* The publisher (AWS or third party)
* A short description and a "Learn more" link pointing to the resource documentation

To narrow the list, search by extension prefix. For example, to show EC2-related types, type:

* AWS::EC2

and press Enter. You can also filter by publisher type (AWS, third-party, or private).

### Example: resource schema (Configuration tab)

Below is a representative JSON schema snippet for the AWS::S3::AccessPoint resource shown in the console. You can copy similar schema directly from the Configuration tab for any activated extension.

```json theme={null}
{
  "typeName": "AWS::S3::AccessPoint",
  "description": "The AWS::S3::AccessPoint resource is an Amazon S3 resource type that you can use to access buckets through an access point.",
  "sourceUrl": "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-s3",
  "definitions": {
    "VpcConfiguration": {
      "description": "The Virtual Private Cloud (VPC) configuration for a bucket access point.",
      "type": "object",
      "properties": {
        "VpcId": {
          "description": "If this field is specified, this access point will only allow connections from the specified VPC.",
          "type": "string"
        }
      }
    }
  }
}
```

The Configuration tab indicates whether additional configuration is required and exposes the full resource schema for reference or copy.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing the Registry → Activated extensions page for the AWS::S3::AccessPoint resource. The Configuration tab is selected and shows a &#x22;Configuration schema&#x22; panel stating that this extension does not require any configuration." />
</Frame>

## Browse Public extensions

The Registry also lists public extensions — resource types published by AWS and third-party publishers (including verified AWS Marketplace publishers). From the public extensions view you can:

* Inspect extension details and schemas
* View publisher information and documentation links
* Activate extensions into your account so they can be used in templates

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Registry: Public extensions&#x22; page showing listed public resource types such as AWSSQS::Kubernetes::Resource and Atlassian::Opsgenie::Integration. The left navigation menu and a Windows taskbar with apps and system tray are visible." />
</Frame>

<Callout icon="warning">
  Many public extensions are not activated by default. You must explicitly activate a public or third‑party extension before using its resource types in CloudFormation templates.
</Callout>

## Modules vs. resource types

You can change the registry filter to show modules instead of resource types. Modules are reusable, composable building blocks that can include multiple resources behind a simplified interface. Public module availability varies by region and publisher.

## Quick search example

Use the extension prefix to quickly find related resource types. For example, searching for S3-related resources looks like:

```text theme={null}
Search by extension prefix (eg. Amazon Simple Storage Service (Amazon S3))
RESOURCE TYPE | PUBLIC
AWS::ACMPCA::Certificate
Published by AWS
The AWS::ACMPCA::Certificate resource is used to issue a certificate using your private certificate authority. For more information, see the IssueCertificate API.
```

## Registry publisher — publish your own extensions

If you want to publish resource types, modules, or hooks, register as a publisher. The Publisher page displays your registration status and provides a guided workflow to register and publish.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Registry: Publisher&#x22; page showing a Publisher registration prompt that says the account is not registered, with a &#x22;Register publisher&#x22; button. The left sidebar menu and top browser tabs are also visible." />
</Frame>

Registering as a publisher enables you to:

* Publish resource types and modules to the CloudFormation Registry
* Share extensions publicly or keep them private to your account(s)
* Manage versioning and documentation for your extensions

## Registry summary (at-a-glance)

| Registry view        | Purpose                                             | Typical actions                                      |
| -------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| Activated extensions | Resources/modules already available in your account | Inspect schema, copy configuration, use in templates |
| Public extensions    | Browse AWS and third-party published types          | Inspect details, activate into your account          |
| Modules              | Reusable compositions of multiple resources         | Discover and activate composable building blocks     |
| Publisher            | Register and manage publisher identity              | Register, publish resource types/modules/hooks       |

## Tips & resources

<Callout icon="lightbulb">
  Search by extension prefix (for example, Amazon S3 prefixes like `AWS::S3`) to quickly locate related resource types. Always activate any public or third‑party extension you plan to use in templates, and consult the Configuration tab for the resource schema before authoring templates.
</Callout>

Further reading:

* [AWS CloudFormation Registry documentation](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [IssueCertificate API (ACM PCA)](https://docs.aws.amazon.com/acm-pca/latest/APIReference/API_IssueCertificate.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/0a4a5ad0-b216-4c7f-9603-8ecd45254371/lesson/95aed065-a7ba-4a47-9834-386231779eae" />
</CardGroup>
