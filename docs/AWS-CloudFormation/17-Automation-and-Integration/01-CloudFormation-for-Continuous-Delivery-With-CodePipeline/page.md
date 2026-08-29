# CloudFormation for Continuous Delivery With CodePipeline

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Automation-and-Integration/CloudFormation-for-Continuous-Delivery-With-CodePipeline/page

Automating CloudFormation infrastructure deployments with AWS CodePipeline for validation, change sets, testing, approvals, and secure auditable continuous delivery.

Hi everyone — welcome to this lesson on using [AWS CodePipeline (CI/CD Pipeline)](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline) together with [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) to implement continuous delivery for infrastructure. Below we explain what CodePipeline does, how it integrates with CloudFormation, and best practices for automating safe, auditable stack deployments.

[AWS CodePipeline (CI/CD Pipeline)](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline) is a managed CI/CD service that models your release process as a sequence of stages (source → build/test → deploy). By automating each stage, CodePipeline helps you deliver infrastructure and application changes more quickly and reliably.

CodePipeline integrates with many tools and services: GitHub or CodeCommit for source, AWS CodeBuild for build/validation, and AWS CloudFormation (or CodeDeploy, Lambda, etc.) for deployment. This lets you build a pipeline that validates CloudFormation templates, runs tests, and then creates or updates stacks automatically.

<Frame>
  <img alt="A diagram for AWS CodePipeline illustrating Continuous Integration and Continuous Delivery with linked gear and infinity-loop icons. Below it are buttons labeled Building, Testing, and Deployment to show pipeline stages." />
</Frame>

What you automate with CodePipeline + CloudFormation

* Source control of templates and application code.
* Template validation and automated testing prior to deployment.
* Creation or update of CloudFormation stacks, optionally using change sets for controlled deployments.
* Auditable, repeatable deployments with manual approvals where needed.

Typical manual lifecycle, and how CodePipeline automates it:

1. Write or change a CloudFormation template.
2. Push changes to your source repository.
3. The pipeline pulls the change, validates/test the template, then triggers CloudFormation to create/update the stack.
4. Application runs inside the provisioned resources; pipeline records artifacts and results.

<Frame>
  <img alt="A three-step diagram titled &#x22;CloudFormation With CodePipeline&#x22; showing: 1) write code for a CloudFormation template, 2) deploy the template on CloudFormation (facilitated by CodePipeline), and 3) create the application stack." />
</Frame>

Pipeline stages for CloudFormation deployments

| Stage                  | Purpose                                        | Typical Tools / Actions                                            |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------------ |
| Source                 | Retrieve templates and application code        | GitHub, CodeCommit, S3                                             |
| Build / Validate       | Lint templates, unit tests, produce artifacts  | CodeBuild (cfn-lint, unit tests), CloudFormation validate-template |
| Change-set / Approvals | Prepare safe changes and pause for reviews     | CloudFormation CreateChangeSet, Manual approval actions            |
| Deploy                 | Execute change sets or create/update stacks    | CloudFormation Action, CodeBuild/Lambda calling CloudFormation API |
| Post-deploy            | Integration tests, monitoring, rollback-checks | CodeBuild tests, CloudWatch alarms, automated rollback logic       |

Build/validate examples

* Validate templates and run cfn-lint (in CodeBuild or locally):

```bash theme={null}
