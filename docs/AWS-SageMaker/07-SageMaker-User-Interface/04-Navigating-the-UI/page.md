# Example Jupyter notebook cell
a = 7
b = 3
print(a + b)
```

Output:

```text theme={null}
10
```

Opening "JupyterLab" launches the modern, flexible interface that supports multiple notebooks, terminals, file previews (CSV, Markdown), and extensions.

<Frame>
  <img alt="A screenshot of the JupyterLab launcher in a web browser, showing tiles for notebooks, consoles, terminals and file types (Python, R, Markdown) with kernel icons. A file browser pane is visible on the left and a large cursor is near the top." />
</Frame>

From JupyterLab you can open a terminal on the managed instance and run commands such as pip list to inspect installed Python packages. Example (truncated) pip list output:

```text theme={null}
Package                Version
---------------------- -------
boto3                  1.26.0
jupyterlab             4.0.0
matplotlib             3.7.1
numpy                  1.26.2
pandas                 2.2.2
sagemaker              2.241.0
sagemaker-experiments  0.1.45
seaborn                0.13.2
```

You can also clone Git repositories using JupyterLab’s Git extensions, open multiple notebooks simultaneously, and add extensions such as table-of-contents or notebook templates.

## Typical SDK setup in a notebook

Notebooks that use the SageMaker Python SDK typically include setup code to get the execution role, region, and a SageMaker session. Example:

```python theme={null}
import boto3
import sagemaker
from sagemaker import get_execution_role

aws_role = get_execution_role()
aws_region = boto3.Session().region_name
sess = sagemaker.Session()
```

This code:

* Retrieves the IAM execution role available in the notebook environment (if present).
* Determines the current AWS region from boto3.
* Creates a SageMaker session object used by higher-level SageMaker SDK APIs (Estimator, Model, Pipeline, etc.).

<Callout icon="warning">
  Remember: legacy notebook instances are charged while they are InService. Stop or delete instances when not in use to avoid unnecessary charges.
</Callout>

## Summary — what you’ll remember from this lesson

* Where to find Processing jobs, Training jobs, Models, and Endpoints in the SageMaker console.
* How to create and open legacy managed Notebook instances.
* The difference between classic Jupyter Notebook and JupyterLab on managed instances.
* Model artifacts appear under Inference → Models and deployed endpoints appear under Endpoints.
* Recommendation: prefer SageMaker Studio for a more integrated JupyterLab experience in production workflows.

We’ve now covered where core SageMaker entities appear in the console and how to launch and use legacy managed notebook instances. For multi-user collaboration, built-in versioning, and a richer integrated experience, review SageMaker Domains and SageMaker Studio.

## Links and references

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [Amazon EC2 instance types](https://aws.amazon.com/ec2/instance-types/)
* [SageMaker SDK (boto3/sagemaker) documentation](https://sagemaker.readthedocs.io/)
* [AWS Pricing](https://aws.amazon.com/pricing/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/8ccbf014-6e79-4cfa-8c37-50be856b9097" />
</CardGroup>


# Navigating the UI

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/Navigating-the-UI/page

Explains navigating the Amazon SageMaker console, differences between Studio and legacy notebooks, and where processing, training, models, endpoints, and notebooks appear.

In this lesson we explore the Amazon SageMaker AI console and where to find the resources you’ll interact with during a typical machine learning workflow. The SageMaker Management Console is primarily a dashboard that reports resources and their status rather than a step-by-step wizard. Much of the activity in SageMaker is code-driven (for example, via the SageMaker SDK in Jupyter notebooks), so the console will often appear sparse until you create resources programmatically.

Begin in the AWS Management Console and use the top search bar to find SageMaker. You may see two entries: Amazon SageMaker AI and Amazon SageMaker Platform. This guide focuses on the core SageMaker AI features used for processing, training, and hosting models.

<Frame>
  <img alt="A slide titled &#x22;Problem: Unintuitive SageMaker UI&#x22; showing an AWS Console Home screenshot. The console's &#x22;Recently visited&#x22; list is visible with &#x22;Amazon SageMaker AI&#x22; highlighted." />
</Frame>

## Console mindset: code-first, dashboard-oriented

The SageMaker console is best thought of as a monitoring and management dashboard. Unlike EC2, which prominently shows “Create instance,” SageMaker expects you to create processing jobs, training jobs, and endpoints from code (Jupyter notebooks, CI/CD pipelines, or SDK scripts). After you run jobs from code, the console is where you monitor status, logs, and metrics.

* If you haven’t created resources, pages like Processing, Training, and Models will be empty.
* The console surfaces outputs from programmatic actions: processing jobs, training jobs, models, and endpoints.

If you haven’t yet run any jobs, the Training view will look empty:

<Frame>
  <img alt="A slide titled &#x22;Problem: Unintuitive SageMaker UI&#x22; showing an AWS SageMaker console screenshot. The screenshot highlights the Training jobs page with the left navigation menu and an empty jobs table." />
</Frame>

Similarly, the Models page (Inference → Models) remains empty until you train and register models:

<Frame>
  <img alt="A slide titled &#x22;Problem: Unintuitive SageMaker UI&#x22; showing an AWS SageMaker console screenshot with the Models page empty and the left-hand navigation visible. The page displays controls like &#x22;Create endpoint&#x22; but no resources are listed." />
</Frame>

Endpoints are production-hosted resources used for inference. If you haven’t deployed a model, the Endpoints page will be empty. The console is useful for monitoring and managing endpoints, but endpoint creation typically comes from SDK calls.

## Quick-reference: console sections and when you’ll see entries

| Console Section       | What it shows                | When it becomes populated                         |
| --------------------- | ---------------------------- | ------------------------------------------------- |
| Processing            | Batch data processing jobs   | After you start Processing jobs via SDK/console   |
| Training              | Training job runs and status | After you start training jobs (SDK/Notebooks/CLI) |
| Inference → Models    | Registered model artifacts   | After you create/register models                  |
| Inference → Endpoints | Deployed inference endpoints | After you deploy models to endpoints              |
| Notebooks             | Legacy Notebook instances    | After you create Notebook instances               |

Useful links:

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker Studio overview](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)

## Notebook instances (legacy) vs. SageMaker Studio

SageMaker provides two ways to run notebooks from the console:

* Legacy Notebook instances — managed EC2-backed Jupyter servers you create from the console.
* SageMaker Studio — the modern, integrated IDE for notebooks, experiments, and ML lifecycle management. Studio is the recommended interface for most new workflows.

Creating a Notebook instance launches a managed VM with Jupyter/JupyterLab. You choose a name and an instance type (e.g., t3.medium). Notebook instances are primarily for interactive development; heavy training and processing should use separate SageMaker jobs that run on appropriately sized compute.

<Frame>
  <img alt="A presentation slide showing the Amazon SageMaker &#x22;Notebooks and Git repos&#x22; console with an empty Notebook instances list and a &#x22;Create notebook instance&#x22; button. The caption below notes that hosted Jupyter notebooks can be launched on demand and you can control the compute sizing." />
</Frame>

When a Notebook instance reaches InService, use the Actions column to open Jupyter (classic) or JupyterLab. JupyterLab offers a multi-tab interface with a launcher, file browser, terminals, and kernels (conda Python, R, Spark, etc.). The notebook server URL follows a predictable pattern:

```text theme={null}
Notebook URL: https://my-notebook-server-<unique_id>.notebook.<region>.sagemaker.aws
```

The JupyterLab launcher lets you open new notebooks with different kernels, start terminals, and explore files. You can install additional packages from a terminal on the managed instance if needed.

<Frame>
  <img alt="A screenshot of a JupyterLab interface inside a browser, showing the Launcher with notebook and console kernel options (conda Python, R, Spark) and a file browser pane. The image is titled &#x22;Results: Notebook Instance&#x22; with &#x22;JupyterLab&#x22; labeled below." />
</Frame>

### Practical tips for Notebook instances

* Keep the notebook instance size modest for interactive tasks. Use dedicated SageMaker training/processing jobs for heavy compute.
* Billing for Notebook instances runs while the instance is InService — stop or delete when not in use.
* Keep your notebooks in Git (GitHub, GitLab, or CodeCommit) so you can recreate instances without losing work.

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Notebook Instance&#x22; showing a billing icon and the note &#x22;Billing continues while the instance is InService.&#x22; It also lists three cost-saving tips: &#x22;Use small instances,&#x22; &#x22;Stop instances when not in use,&#x22; and &#x22;Delete if not needed.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Consider using SageMaker Studio for an integrated experience (notebooks, experiments, and model management), and reserve legacy Notebook instances for simple or legacy workflows. Keep your work in Git to make instance reprovisioning painless.
</Callout>

<Callout icon="warning">
  Be mindful of costs: Notebook instances and endpoints incur charges while running. Enable billing alerts and routinely stop or delete resources you no longer need.
</Callout>

## Summary — where to look for common artifacts

1. Processing: batch data preprocessing and feature engineering jobs.
2. Training: training job runs, logs, and metrics.
3. Inference → Models / Endpoints: registered models and hosted endpoints for production inference.
4. Notebooks: legacy Notebook instances (or prefer SageMaker Studio for new projects).

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; listing four numbered items: locate data processing jobs; track training jobs in progress; manage hosted models (endpoints); and create and access Jupyter Notebook servers. The items are shown with turquoise numbered markers on a dark left sidebar." />
</Frame>

Next steps: in the demo you'll see a notebook use the SageMaker SDK to create and run a simple training job. This will demonstrate the typical code-first workflow: start a training job from a notebook, then monitor the job and inspect artifacts in the SageMaker console.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/dcce238d-9f49-489f-bb24-12592ad2bf3b" />
</CardGroup>
