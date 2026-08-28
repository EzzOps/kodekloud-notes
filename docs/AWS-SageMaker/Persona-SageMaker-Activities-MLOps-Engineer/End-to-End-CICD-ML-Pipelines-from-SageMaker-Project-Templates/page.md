# model-build/codebuild-buildspec.yml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.11
    commands:
      - pip install --upgrade --force-reinstall . "awscli==1.20.30"

  build:
    commands:
      - export PYTHONUNBUFFERED=TRUE
      - export SAGEMAKER_PROJECT_NAME_ID="${SAGEMAKER_PROJECT_NAME}-${SAGEMAKER_PROJECT_ID}"
      - |
        run-pipeline --module-name pipelines.abalone.pipeline \
          --role-arn ${SAGEMAKER_PIPELINE_ROLE_ARN} \
          --tags "[{\"Key\":\"sagemaker:project-name\", \"Value\":\"${SAGEMAKER_PROJECT_NAME}\"}, {\"Key\":\"sagemaker:project-id\", \"Value\":\"${SAGEMAKER_PROJECT_ID}\"}]" \
          --kwargs "{\"region\":\"${AWS_REGION}\",\"role\":\"${SAGEMAKER_PIPELINE_ROLE_ARN}\",\"default_bucket\":\"${ARTIFACT_BUCKET}\",\"pipeline_name\":\"${SAGEMAKER_PROJECT_NAME_ID}\",\"model_package_group_name\":\"${SAGEMAKER_PROJECT_NAME_ID}\",\"base_job_prefix\":\"${SAGEMAKER_PROJECT_NAME_ID}\",\"sagemaker_project_name\":\"${SAGEMAKER_PROJECT_NAME}\"}"
      - echo "Create/Update of the SageMaker Pipeline and execution completed."
```

CodeBuild logs show the dependency installation and the `run-pipeline` invocation which creates and starts the SageMaker Pipeline:

```text theme={null}
[Container] 2025/05/09 09:39:05.763546 Running command pip install --upgrade --force-reinstall . "awscli==1.20.30"
...
[Container] 2025/05/09 09:39:45.956346 Running command export PYTHONUNBUFFERED=TRUE
[Container] 2025/05/09 09:39:45.964010 Running command export SAGEMAKER_PROJECT_NAME_ID="${SAGEMAKER_PROJECT_NAME}-${SAGEMAKER_PROJECT_ID}"
[Container] 2025/05/09 09:39:45.971495 Running command run-pipeline --module-name pipelines.abalone.pipeline \
  --role-arn ${SAGEMAKER_PIPELINE_ROLE_ARN} \
  --tags ...
/root/.pyenv/versions/3.11.11/lib/python3.11/site-packages/sagemaker/workflow/pipeline_context.py:194: UserWarning: Running within a PipelineSession, there will be No Wait, No Logs, and No Job being started.
warnings.warn(
Job Name: kodekloud-sm-project-p-ihy4fevyl862/skl-2025-05-09-09-39-47-116
Inputs: [...]
Outputs: [...]
```

The `run-pipeline` call builds the SageMaker Pipeline in the same account/region. That pipeline orchestrates Processing, Training, and Evaluation jobs.

## SageMaker Pipelines: Processing → Training → Evaluation → Model Registry

Open SageMaker Pipelines in the console to inspect the generated pipeline and its execution. A typical pipeline graph includes nodes for Preprocess, Train, Evaluate, a model‑quality check (e.g., CheckMSE), and RegisterModel.

<Frame>
  <img alt="A screenshot of Amazon SageMaker Studio showing the Pipelines &#x22;Executions&#x22; view for a project named &#x22;kodekloud-sm-project-p-ihy4fevyl862,&#x22; listing a single pipeline execution currently marked &#x22;Executing&#x22; with elapsed time and timestamps. The left sidebar shows SageMaker apps and navigation items." />
</Frame>

Click into Processing and Training jobs from the execution view to inspect logs, instance types, role ARNs, and S3 artifact locations. Example pipeline graph and evaluation details:

<Frame>
  <img alt="A screenshot of Amazon SageMaker Studio showing a pipeline execution graph for an &#x22;Abalone&#x22; ML workflow with nodes like PreprocessAbaloneData, TrainAbaloneModel, EvaluateAbaloneModel, CheckMSEAbaloneEvaluation, and RegisterAbaloneModel. The right-hand pane displays detailed information for the EvaluateAbaloneModel step." />
</Frame>

When complete, Processing jobs appear in the Processing Jobs list.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console showing a list of processing jobs with columns for name, ARN, creation time, duration, and status (Completed/Failed). The left sidebar displays SageMaker navigation options with the &#x22;Processing jobs&#x22; entry highlighted." />
</Frame>

If evaluation conditions meet the template thresholds (for example, MSE below the configured limit), the pipeline registers a model package in the SageMaker Model Registry. By default (in this template), new model packages enter the registry in a “Pending manual approval” state.

<Frame>
  <img alt="Screenshot of the AWS SageMaker Studio &#x22;Models&#x22; page showing a registered model (kodekloud-sm-project-...) with a &#x22;Pending manual approval&#x22; deployment status. The left navigation pane and a hand-cursor icon pointing at the model entry are also visible." />
</Frame>

At this point the model build pipeline has executed end‑to‑end: Source → CodeBuild → run‑pipeline (SageMaker Pipeline) → Processing/Training/Eval → Model Registry.

## Approve the Model; Trigger the Model Deploy Pipeline

Approving the model package in the Model Registry will trigger the deploy pipeline if an EventBridge rule or pipeline trigger is configured. Approve the model in the SageMaker console by changing the model package status from pending to approved and adding an optional comment.

<Frame>
  <img alt="A screenshot of AWS SageMaker Studio showing a &#x22;Change Inference Status&#x22; dialog with the model status set to &#x22;Approved&#x22; and the comment &#x22;Good to deploy now.&#x22; A large mouse cursor is hovering over the Save button." />
</Frame>

Approving the model triggers the model‑deploy CodePipeline which runs a CodeBuild project. That build prepares CloudFormation templates for staging and production, packages artifacts, and emits deployable artifacts consumed by CloudFormation in later pipeline stages.

Typical tasks in the model‑deploy buildspec:

* Run a helper (e.g., build.py) to generate endpoint configuration CloudFormation templates for staging and prod.
* Package templates with `aws cloudformation package` and upload artifacts to the project S3 bucket.
* Emit packaged template files as pipeline artifacts.

A cleaned, representative deploy buildspec:

```yaml theme={null}
# model-deploy/codebuild-buildspec.yml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.11
    commands:
      - pip install --upgrade --force-reinstall "botocore==1.21.30" "boto3==1.18.30" "awscli==1.20.30"

  build:
    commands:
      - python build.py \
          --model-execution-role "$MODEL_EXECUTION_ROLE_ARN" \
          --model-package-group-name "$SOURCE_MODEL_PACKAGE_GROUP_NAME" \
          --sagemaker-project-id "$SAGEMAKER_PROJECT_ID" \
          --sagemaker-project-name "$SAGEMAKER_PROJECT_NAME" \
          --s3-bucket "$ARTIFACT_BUCKET" \
          --export-staging-config $EXPORT_TEMPLATE_STAGING_CONFIG \
          --export-prod-config $EXPORT_TEMPLATE_PROD_CONFIG

      - aws cloudformation package \
          --template-file endpoint-config-template.yml \
          --s3-bucket $ARTIFACT_BUCKET \
          --output-template-file $EXPORT_TEMPLATE_NAME

      - cat $EXPORT_TEMPLATE_STAGING_CONFIG
      - cat $EXPORT_TEMPLATE_PROD_CONFIG

artifacts:
  files:
    - $EXPORT_TEMPLATE_NAME
    - $EXPORT_TEMPLATE_STAGING_CONFIG
    - $EXPORT_TEMPLATE_PROD_CONFIG
```

When the deploy stage runs, CodePipeline starts CloudFormation stacks that create the SageMaker Model, EndpointConfiguration, and Endpoint resources. The pipeline deploys staging first, executes tests (often a CodeBuild smoke test), and then pauses for a manual approval before creating the production stack.

You can approve the pipeline deployment from the CodePipeline console (Review & Approve).

<Frame>
  <img alt="A screenshot of an AWS CodePipeline &#x22;Review&#x22; dialog for an ApproveDeployment action in a SageMaker pipeline, showing the decision options with &#x22;Approve&#x22; selected. The comments box contains &#x22;Yes good for prod.&#x22; and there's a highlighted Submit button." />
</Frame>

After approval, CodePipeline proceeds to create the production CloudFormation stack and production endpoint. Monitor CloudFormation events and the SageMaker Endpoints page while the endpoint warms up (this can take several minutes).

## Inspect CodeBuild Projects

Both pipelines use CodeBuild. In the CodeBuild console you can open each build project to examine its environment, source settings, and buildspec.

<Frame>
  <img alt="A screenshot of the AWS CodeBuild &#x22;Build projects&#x22; page showing a list of build projects, their source provider (AWS CodePipeline), and latest build statuses (one Succeeded, one Failed). A pointer/hand cursor is hovering over one of the project names." />
</Frame>

Buildspecs are the authoritative instructions for CodeBuild: they install dependencies, run helper scripts or `run-pipeline`, and package or deploy CloudFormation templates.

## Third‑Party Git Integration (Optional)

If you prefer to use GitHub, GitLab, Bitbucket, or GitHub Enterprise, choose a template that supports third‑party Git. You must first create a CodeStar connection between your AWS account and the Git provider (Developer Tools → Settings → Connections). The project creation dialog will then request repository URLs and branch names instead of creating CodeCommit repos.

<Frame>
  <img alt="A screenshot of the AWS SageMaker Studio &#x22;Create Project&#x22; page showing form fields for ModelBuild and ModelDeploy code repository info, with a large cursor icon over the URL field. The left sidebar shows navigation items and app icons like JupyterLab and RStudio." />
</Frame>

Manage or create CodeStar connections in the AWS console to link your Git provider; the connection name is referenced in the SageMaker Project dialog.

<Frame>
  <img alt="A browser screenshot of the AWS Management Console displaying a CodeCommit repository named &#x22;sagemaker-kodekloud-sm-project-...&#x22; with a file/folder list and README section. The right side shows the Amazon Q generative AI assistant panel, and the left shows the Developer Tools navigation." />
</Frame>

## Resources Created by the Template

| Resource Type                | Use Case                                                                   | Example / Notes                                         |
| ---------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------- |
| S3 Bucket                    | Artifacts and packaged CloudFormation templates                            | sagemaker-project-\<project-id>                         |
| CodeCommit / Third‑party Git | Source code for model build & deploy                                       | seed code includes pipelines, buildspecs, CFN templates |
| CodeBuild                    | Executes buildspecs: installs deps, runs run-pipeline, packages templates  | model-build & model-deploy projects                     |
| CodePipeline                 | Orchestrates CI/CD stages (Source → Build → Deploy)                        | build triggers SageMaker Pipeline creation              |
| SageMaker Pipelines          | End‑to‑end ML workflow: Processing → Training → Evaluation → RegisterModel | registers model packages into Model Registry            |
| CloudFormation               | Declarative infra provisioning (models, endpoints, event rules)            | used by templates produced by build                     |

## Summary

What we accomplished:

1. Reviewed SageMaker Project templates and selected one that provisions both model build and model deploy CI/CD pipelines.
2. Created a SageMaker Project, which launched a CloudFormation stack to provision S3, source repos, CodeBuild projects, CodePipeline pipelines, SageMaker Pipelines, and IAM roles.
3. Followed the CI/CD flow: CodeCommit → CodePipeline → CodeBuild → run‑pipeline (SageMaker Pipeline) → Processing/Training/Evaluation → Model Registry.
4. Approved a registered model to trigger the deploy pipeline; observed staging deployment, automated tests, and a manual approval gate before production.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; listing four numbered items: reviewed built-in SageMaker project templates, deployed a SageMaker project template, identified the CloudFormation stack deploying resources, and reviewed the CI/CD pipeline for automation. The slide uses teal numbered badges on a vertical timeline against a dark left panel." />
</Frame>

This project template provides a fully integrated CI/CD workflow for ML on AWS. For production systems:

* Prefer third‑party Git hosts and CodeStar connections,
* Define branching and approval policies,
* Consider cross‑account deployments and more robust testing (canaries, blue/green),
* Add monitoring and Model Monitor checks for production model behavior.

Links and references

* SageMaker Projects & Templates: [https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html)
* SageMaker Pipelines: [https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
* SageMaker Model Registry: [https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
* AWS CodePipeline: [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)
* AWS CodeBuild: [https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* AWS CloudFormation: [https://docs.aws.amazon.com/cloudformation/index.html](https://docs.aws.amazon.com/cloudformation/index.html)
* CodeStar Connections (Git integrations): [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/93134cea-b5a8-4352-8fe1-0a76c58699bb" />
</CardGroup>


# End to End CICD ML Pipelines from SageMaker Project Templates

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/End-to-End-CICD-ML-Pipelines-from-SageMaker-Project-Templates/page

Describes SageMaker project templates that provision CloudFormation CI and CD stacks, link Git repos and CodeBuild to SageMaker Pipelines, automating model build, registry, deployment and governance.

In this lesson you'll learn how SageMaker project templates connect a CI/CD system with SageMaker Pipelines to automate repeatable ML workflows. The goal is to standardize and scale ML development so teams can manage many projects without multiplying operational complexity.

We’ll cover:

* What SageMaker project templates provide
* How templates provision and link AWS resources (Git repos, CI/CD, SageMaker Pipelines)
* Typical model build and model deploy workflows created by templates
* Where [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) and AWS Service Catalog fit into the workflow
* Best practices and tradeoffs (including Git repository options)

SageMaker project templates help teams adopt consistent repo layouts, CI/CD triggers, and SageMaker Pipelines behavior so data scientists, data engineers, and MLOps professionals can collaborate using the same patterns.

Why consistency matters

* Faster onboarding: a predictable repo structure and pipeline behavior shortens ramp-up for engineers moving between projects.
* Reliable governance: consistent experiment tracking and model versioning simplifies auditing and model comparisons.
* Lower engineering overhead: reusable templates reduce bespoke automation work and help enforce compliance and reproducibility.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Challenges in Scaling and Managing ML Workflows&#x22; that lists four issues: lack of standardization in development/deployment, inconsistent CI/CD for ML, collaboration challenges among data engineers/scientists/MLOps/DevOps, and complexity in experiment tracking and model versioning." />
</Frame>

<Callout icon="lightbulb">
  Choose one Git provider and be consistent across your organization. SageMaker project templates give you the scaffolding to enforce a single, supported Git workflow (CodeCommit or an external provider like GitHub/GitLab/Bitbucket).
</Callout>

## What SageMaker project templates provide

SageMaker project templates are CloudFormation-based blueprints that provision and link the AWS resources required for an ML project. They automate infrastructure provisioning and CI/CD glue so teams can begin development with a standardized stack.

Typical components provisioned by templates:

* Source repository (AWS CodeCommit or an external Git-compatible provider)
* CI/CD orchestration (AWS CodePipeline or integrations with Jenkins, etc.)
* Build/runtime orchestration (CodeBuild or an external build server)
* SageMaker Pipelines for preprocessing, training, and model registry lifecycle
* Optional MLOps components, like Model Monitor and deployment automation

Table — Common resources created by SageMaker project templates:

| Resource Type              | Purpose                                           | Example                               |
| -------------------------- | ------------------------------------------------- | ------------------------------------- |
| Source repo                | Store code/artifacts and trigger CI               | CodeCommit, GitHub, GitLab, Bitbucket |
| CI/CD Orchestrator         | Manage pipeline stages (source/build/deploy)      | CodePipeline, Jenkins                 |
| Build worker               | Runs build steps; invokes SageMaker Pipelines     | CodeBuild, external CI                |
| SageMaker Pipelines        | Data processing, training, and model registration | SageMaker Pipelines DSL               |
| Model registry & endpoints | Store and deploy model artifacts                  | SageMaker Model Registry, Endpoints   |

When you deploy a template, it often creates a CodePipeline and CodeBuild project tied to a repo. CodeBuild commonly serves as the bridge that starts a SageMaker Pipeline (via SDK or CLI) to run data processing, training, and model registration.

<Frame>
  <img alt="A diagram titled &#x22;Solution: SageMaker Projects&#x22; showing SageMaker Project Templates in the center connected by arrows to AWS services and CI/CD tools: AWS CodeCommit, CodePipeline, CodeBuild, Git-compatible repos, and Jenkins. The image illustrates integration points for SageMaker project templates with version control and build/deployment pipelines." />
</Frame>

## High-level flow (example)

1. A SageMaker project template (CloudFormation) provisions required AWS and CI/CD resources.
2. A source commit to the provisioned Git repo triggers a CodePipeline source stage.
3. CodePipeline runs a build stage (e.g., CodeBuild).
4. CodeBuild invokes a SageMaker Pipeline that performs data processing, training, and model registration.
5. A separate model-deploy pipeline picks up registered models from the model registry and deploys to an endpoint.

This layered approach lets you customize or extend specific stages (e.g., swap CodeBuild for a Jenkins build server) while keeping a consistent provisioning mechanism.

## CloudFormation and infrastructure-as-code

SageMaker project templates are implemented with [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) templates. CloudFormation is AWS’s native Infrastructure-as-Code (IaC) tool: you declare resources in YAML/JSON and CloudFormation creates and configures them. While other IaC tools such as [Terraform](https://learn.kodekloud.com/user/courses/terraform-basics-training-course) are popular, the SageMaker project templates rely on CloudFormation under the hood.

## Model build vs model deploy separation

Templates often create separate repos and pipelines for build and deploy. This separation is intentional:

* Model build repository and pipeline: preprocessing, feature engineering, training, experiment tracking, and model registration into the model registry.
* Model deploy repository and pipeline: deployment manifests and scripts that consume model registry artifacts to create or update SageMaker endpoints.

Separating build and deploy gives teams control over lifecycle stages (e.g., allow data scientists to register models while a separate ops team approves deploys).

## Build orchestration with CodeBuild (bridge to SageMaker Pipelines)

Within CodePipeline, CodeBuild commonly runs the build steps. The repository includes a Buildspec.yml file that directs CodeBuild—typically its main responsibility is to start the SageMaker Pipeline using the AWS SDK/CLI.

Example minimal buildspec snippet:

```yaml theme={null}
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.8
    commands:
      - pip install -r requirements.txt
  build:
    commands:
      - |
        aws sagemaker start-pipeline-execution \
          --pipeline-name my-sagemaker-pipeline \
          --region $AWS_DEFAULT_REGION
artifacts:
  files:
    - '**/*'
```

CodeBuild acts as the orchestrator that converts a Git commit into a running SageMaker Pipeline execution.

<Frame>
  <img alt="A flow diagram titled &#x22;Solution: SageMaker Templates&#x22; that maps model build and deploy pipelines using CodeCommit, CodePipeline, CodeBuild, and S3 feeding SageMaker Pipelines into a model registry and finally a SageMaker endpoint. The left side shows SageMaker Project and CloudFormation templates." />
</Frame>

<Callout icon="warning">
  Some SageMaker templates provision AWS CodeCommit repositories automatically; others expect you to supply an external Git repo URL. Choose the Git provider that aligns with your organization’s policies and developer workflows. If using GitHub/GitLab/Bitbucket, create the repo externally and pass its URL to the template during deployment.
</Callout>

## Third-party Git providers and template behavior

* Templates can link to any Git-compatible repository, but SageMaker does not create external third-party repos for you. You must create those repos (or ensure they exist) and supply the URL when deploying a project template.
* Templates that reference CodeCommit can create a repo automatically in supported accounts—this explains why some older or default templates may assume CodeCommit.

## Model-build workflow example

A typical model-build repo (for example, hosted on Bitbucket) might include:

* preprocessing scripts: process.py
* feature engineering: feature.py
* training driver: train.py
* a Buildspec.yml to instruct CodeBuild to start the SageMaker Pipeline

Workflow:

* A developer modifies feature.py and pushes to main.
* The pipeline source stage detects the change and starts the pipeline.
* CodeBuild runs Buildspec.yml and invokes the SageMaker Pipeline, which runs: Clean data → Feature engineering → Train → Register (→ optional deploy or test).

<Frame>
  <img alt="A workflow diagram titled &#x22;SageMaker Templates&#x22; showing a model-build Git repo with files (process.py, feature.py, train.py, Buildspec.yml) connected to a CodePipeline (Source → Build). The pipeline feeds a sequence of steps at the bottom: Clean Data, Feature Engineer, Train, Register, and Deploy." />
</Frame>

## Provisioning a SageMaker project from Studio

You can create a project directly from SageMaker Studio:

* Studio → Deployments → Projects → Create project
* Choose a template and supply project details (including third-party Git repo URLs when requested)

The Studio UI lists built-in templates. Note: some templates may be legacy or unavailable in certain accounts/regions—review template details and pick options that match your organization’s support and compliance posture.

## Available template variations

Common built-in template patterns include:

* Model build & train with third-party Git using CodePipeline (build-only)
* Model build, train & deploy with third-party Git using CodePipeline (build + deploy)
* Model build/train/deploy with Jenkins (requires an existing Jenkins server)
* Model build/train/deploy with integrated Model Monitor
* Simple model deployment using CodePipeline and a third-party Git repo

Table — Example template types and when to use them:

| Template Type                 | Use Case                       | Considerations                             |
| ----------------------------- | ------------------------------ | ------------------------------------------ |
| Build-only (CodePipeline)     | CI for training & registry     | Good for automated training workflows      |
| Build + Deploy (CodePipeline) | End-to-end automation          | Use when automated deployments are allowed |
| Jenkins-based                 | Existing Jenkins infra         | Requires Jenkins integration setup         |
| With Model Monitor            | Production monitoring included | Adds monitoring/alerting stages            |
| Simple deploy                 | Lightweight endpoint updates   | Fast iteration for simple workloads        |

### Organization templates

Under the Organization Templates tab you can publish custom templates tailored to your enterprise policies. These enforce configuration, IAM, and networking defaults so teams start projects that already conform to organizational standards.

<Frame>
  <img alt="A slide titled &#x22;Workflow: SageMaker Projects&#x22; showing the AWS SageMaker &#x22;Create project&#x22; UI with a Templates panel listing MLOps project templates. A highlighted callout reads &#x22;Launch custom project templates.&#x22;" />
</Frame>

## Using AWS Service Catalog with SageMaker projects

Many enterprises expose SageMaker project templates through AWS Service Catalog. Service Catalog provides a controlled, app-store-like interface where authorized users request pre-approved templates without needing direct console permissions. The Service Catalog item can launch a SageMaker project CloudFormation template on behalf of the requester—enforcing governance, role separation, and pre-approved configurations.

<Frame>
  <img alt="A slide titled &#x22;Workflow: SageMaker Projects&#x22; with a left-side flowchart showing AWS Service Catalog → SageMaker Project Template → CloudFormation Template. The right side lists four points: simplifies provisioning, offers a storefront-like experience, lets users request services without direct permissions, and example options (3-tier web app, Hadoop cluster, SageMaker Project)." />
</Frame>

## Benefits of SageMaker project templates

* Faster project setup — get a working scaffold on day zero.
* Consistent CI/CD — easier to maintain, debug, and scale.
* Stronger governance — enforce templates, policies, and compliance.
* Easier cross-team collaboration — standard patterns reduce re-learning.
* Scalable operations — automation minimizes manual provisioning and custom engineering.

Many organizations pre-populate repositories with standard scripts, linters, and testing utilities so teams have a repeatable, organizationally-aligned starting point.

<Frame>
  <img alt="A slide titled &#x22;Results: SageMaker Projects&#x22; showing five numbered panels that list benefits: faster ML development with automation; consistent CI/CD workflow management; better governance and compliance; easier collaboration across teams; and scalable ML deployment with monitoring and retraining. Each panel includes an icon and brief explanatory text." />
</Frame>

## Recap

* SageMaker project templates use [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) to provision and link required resources: source repos, [CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline), CodeBuild (or external CI), and SageMaker Pipelines.
* Templates typically separate build and deploy pipelines; CodeBuild often acts as the bridge that invokes SageMaker Pipelines.
* Use built-in templates or publish organization-specific templates. For enterprise-level governance, surface templates via AWS Service Catalog.
* Choose your Git provider based on organizational policy and developer workflows. Templates may provision CodeCommit repos automatically, or accept external repo URLs (GitHub, GitLab, Bitbucket, etc.) as inputs.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing five numbered points about SageMaker project templates and deployment. The points mention CI/CD and SageMaker Pipelines, customizable templates, migrating away from CodeCommit, using CloudFormation for IaC, and sharing templates via Service Catalog." />
</Frame>

This concludes the lesson. A demonstration will follow to show creating a SageMaker project from a template and walking through the template deployment and pipeline execution.

Further reading and references:

* [AWS SageMaker Projects documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html)
* [AWS CloudFormation documentation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [AWS CodePipeline basics](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* [Terraform (alternative IaC)](https://learn.kodekloud.com/user/courses/terraform-basics-training-course)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/21a4003b-9b79-46a9-82eb-303d1bd8a847" />
</CardGroup>
