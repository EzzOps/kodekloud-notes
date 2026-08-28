# Complete Lifecycle Workflow

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Cloud-Service-Models/Complete-Lifecycle-Workflow/page

Guide to the complete lifecycle workflow for AWS CloudFormation templates covering authoring, linting, validating, deploying, verifying resources, and iterative best practices for safe infrastructure as code

Welcome — this guide outlines the complete lifecycle workflow for Amazon CloudFormation templates. It explains the common cycle you follow when authoring, validating, deploying, and iterating on CloudFormation templates so you can reliably build and manage infrastructure-as-code.

The lifecycle follows these primary steps:

1. Write the template source code
   * Author a CloudFormation template (commonly YAML, sometimes JSON). Define core sections: `Resources`, `Parameters`, `Mappings`, and `Outputs`. Optionally include `Metadata`, `Conditions`, and `Transform` sections as required by your design. Keep templates focused and modular to simplify testing and reuse.

2. Lint and validate the template
   * Use tools such as cfn-lint to detect schema errors and common best-practice issues early:
     * cfn-lint: [https://github.com/aws-cloudformation/cfn-lint](https://github.com/aws-cloudformation/cfn-lint)
   * Validate syntax and intrinsic correctness using the CloudFormation console or AWS CLI:
     * Example AWS CLI validation:
     ```bash theme={null}
     aws cloudformation validate-template --template-body file://template.yml
     ```
   * Early validation prevents failed deployments and reduces troubleshooting time.

3. Deploy the template on CloudFormation
   * Create or update a CloudFormation stack from your validated template. Use change sets to preview the impact of updates to an existing stack:
     * Example (create change set):
     ```bash theme={null}
     aws cloudformation create-change-set --stack-name my-stack \
       --template-body file://template.yml --change-set-name preview
     ```

4. CloudFormation provisions the application stack
   * CloudFormation creates and configures the defined resources (EC2, VPCs, IAM roles, S3 buckets, Lambda, etc.), handling dependency ordering and lifecycle actions automatically.

5. Verify access and behavior of created resources
   * Confirm resources are available and behaving as expected. For example, test network connectivity, check IAM permissions, and verify application endpoints. Capture outputs and update templates to expose needed metadata via `Outputs`.

6. Iterate and repeat the process
   * Add features, fix issues, and evolve the template. Each iteration should follow the author → lint/validate → deploy → verify loop to keep changes safe and incremental.

<Frame>
  <img alt="A flowchart titled &#x22;Complete Lifecycle Workflow&#x22; showing five steps: write source code for template, lint and validate the template, deploy the template on CloudFormation, create the application stack, and access resources. Below it is an additional box labeled &#x22;Repeat the process.&#x22;" />
</Frame>

Why iterate repeatedly?

* Start with small, simple templates to validate the end-to-end flow and surface early issues. A minimal first template helps you confirm IAM roles, networking, and resource dependencies without complexity.
* Incrementally add reusability: introduce `Parameters`, `Mappings`, `Conditions`, `Metadata`, and intrinsic functions (`Ref`, `Fn::GetAtt`, `Fn::Sub`, `Fn::Join`, etc.) so the template supports multiple environments and configurations.
* Iteration builds confidence for production infrastructure: gradually introduce EC2 instances, IAM policies, networking, autoscaling, and monitoring while refining permissions and resource sizing.

Common template sections and when to use them

| Template Section | Purpose                                             | Example / When to Add                                                |
| ---------------- | --------------------------------------------------- | -------------------------------------------------------------------- |
| Parameters       | Make templates configurable at deploy time          | `InstanceType` parameter to switch between `t3.micro` and `t3.small` |
| Mappings         | Provide static environment-specific values          | Map AMI IDs per region                                               |
| Conditions       | Control resource creation based on parameter values | Create resources only for `Production=true`                          |
| Resources        | Define actual AWS resources to provision            | `AWS::EC2::Instance`, `AWS::S3::Bucket`                              |
| Outputs          | Expose values after deployment                      | Public IP, load balancer DNS                                         |
| Metadata         | Store template-level metadata or tooling hints      | cfn-nag suppressions or documentation                                |

<Callout icon="lightbulb">
  Iterative cycles let you catch mistakes early, increase template reusability, and safely evolve infrastructure. Use linting and validation on every change before deployment.
</Callout>

Best practices summary

* Validate and lint every change — include CI jobs that run `cfn-lint` and `aws cloudformation validate-template`.
* Use small, incremental changes with change sets to preview updates to running stacks.
* Parameterize environment-specific values and avoid hardcoding ARNs or region-specific AMIs.
* Keep templates modular: split large templates into nested stacks when logical grouping makes sense.
* Store templates in version control and tag releases to track deployed versions.

<Frame>
  <img alt="A slide titled &#x22;Why Do We Repeat the Process?&#x22; that outlines three numbered steps for working with CloudFormation: write, lint, validate and deploy simple templates; add metadata, intrinsic functions, parameters and mappings to make templates reusable; and apply skills to build real infrastructure (EC2, permission policies). The slide includes KodeKloud copyright at the bottom." />
</Frame>

<Callout icon="warning">
  Never skip validation or testing in a non-production environment. Changes to IAM, networking, or shared services can have wide impact — always review changes with a change set and, when appropriate, a peer review or automated policy checks.
</Callout>

Links and references

* [cfn-lint (GitHub)](https://github.com/aws-cloudformation/cfn-lint) — template linting tool
* AWS CloudFormation validate-template — [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-validate-template.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-validate-template.html)
* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)

Further reading

* Explore CloudFormation change sets and nested stacks for safer updates and modularization.
* Consider integrating policy-as-code (e.g., cfn-nag, AWS Config Rules, or AWS IAM Access Analyzer) into your CI to prevent accidental misconfigurations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/c89fc2ec-13f2-4ccc-9c2d-9a8e6c97a55a/lesson/34e8ee7d-0849-4ad3-9f46-17c0261aef93" />
</CardGroup>
