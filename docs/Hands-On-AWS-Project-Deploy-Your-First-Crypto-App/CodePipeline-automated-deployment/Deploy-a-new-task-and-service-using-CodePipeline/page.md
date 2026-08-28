# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if provided credentials match the default ones
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/webpage')
def welcome():
    return render_template('product.html')

@app.route('/place_order')
def place_order():
    product_id = request.args.get('product')
    return render_template('place_order.html', product_id=product_id)
```

We resolved this by restoring the required lines in the main repository (uncommenting the necessary code) and committing the corrected version.

## Create the pipeline in the AWS Console

Follow these step-by-step instructions to create a simple pipeline that fetches code from CodeCommit and runs CodeBuild.

1. Open the AWS Management Console and navigate to **CodePipeline** (located near CodeBuild).
2. Click Pipelines -> **Create pipeline**.
3. Give the pipeline a descriptive name.
4. Open **Advanced settings** and keep defaults unless you need to change encryption, service role, or artifact store settings.
5. Click **Next** to configure the Source stage.

<Frame>
  <img alt="The image shows an AWS CodePipeline interface, highlighting features for visualizing and automating software release processes. It includes options to create a pipeline and provides pricing and getting started information." />
</Frame>

### Source stage: AWS CodeCommit

* For Source provider, select **AWS CodeCommit**.
* Choose the repository `aws-microservice-project`.
* Select the branch `master`.

<Frame>
  <img alt="The image shows an AWS CodePipeline interface where a user is adding a source stage, selecting AWS CodeCommit as the source provider, with options to enter repository and branch names." />
</Frame>

6. Click **Next** to configure the Build stage.

### Build stage: AWS CodeBuild

* For Build provider select **AWS CodeBuild**.
* Choose the appropriate project (for example `AWS MicroserviceProject`).
* Click **Next**.

We do not want to deploy to ECS yet for this pipeline, so choose **Skip deploy stage**, then click **Create pipeline**.

When the pipeline is created it starts an initial execution automatically to validate the configured stages. You can monitor progress from the pipeline detail page.

<Frame>
  <img alt="This image shows an AWS CodePipeline interface for a project named &#x22;crypto-app,&#x22; displaying the status of source and build stages. The &#x22;Source&#x22; stage has succeeded, while the &#x22;Build&#x22; stage is in progress." />
</Frame>

The Source stage should complete first, followed by the Build stage. In CodeBuild logs you'll see initialization commands and other build steps—for example:

```bash theme={null}
# Example log line from CodeBuild
Running command aws --version
```

Tip: you can disable transitions between stages if you need to pause pipeline progression (for example, temporarily disable the transition from Source to Build).

After the run completes successfully, the pipeline will display a successful status and show the commit hash that was built.

<Frame>
  <img alt="The image shows an AWS CodePipeline interface with one pipeline, &#x22;crypto-app,&#x22; which has a status of &#x22;Succeeded.&#x22; The interface provides options to view history, release changes, and create a new pipeline." />
</Frame>

You can cross-check the commit details directly in CodeCommit—open the repository and view the commits list to confirm the pipeline picked up the intended commit.

<Frame>
  <img alt="The image shows an AWS CodeCommit interface displaying a list of commits for the &#x22;aws-microservice-project&#x22; repository, with details like commit ID, message, date, author, and actions available." />
</Frame>

## Pipeline summary

| Stage  | AWS Service    | Purpose                                                      |
| ------ | -------------- | ------------------------------------------------------------ |
| Source | AWS CodeCommit | Fetch code from `aws-microservice-project` on `master`       |
| Build  | AWS CodeBuild  | Run build commands, tests, and produce artifacts             |
| Deploy | (skipped)      | Not included in this pipeline; manual ECS update shown later |

## Fix code in Cloud9 and push to trigger the pipeline

Make your code edits in Cloud9 (or your local environment), commit, and push to `master`. CodePipeline will automatically start a new execution when it detects the new commit.

Example Git workflow in your Cloud9 environment:

```bash theme={null}
# Inspect repo status
git status

# Stage all changes
git add .

# Commit fixes with a meaningful message
git commit -m "Fix: restore correct routes and templates"

# Ensure Git user is configured (example)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Push to master so CodePipeline can detect the change
git push origin master
```

<Callout icon="lightbulb">
  CodePipeline automatically detects changes in the configured source repository and triggers a pipeline execution for each new commit on the tracked branch.
</Callout>

## Corrected application example

Below is the final (corrected) application code that was pushed to the repository and picked up by CodePipeline:

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if provided credentials match the default ones
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/webpage')
def welcome():
    return render_template('product.html')

@app.route('/place_order')
def place_order():
    product_id = request.args.get('product')
    return render_template('place_order.html', product_id=product_id)
```

## Update ECS service (manual step)

After the pipeline build completes successfully and produces a new image/task definition revision (for example, revision 8), update your ECS service to use that task definition:

1. Open the ECS console and select your cluster.
2. Choose the service you want to update.
3. Click **Update** -> Select the new task definition revision (e.g., v8).
4. Click **Update Service** to start the deployment.
5. Monitor the deployment until it reaches a steady state.

A future lesson will show how to add an automated Deploy stage to CodePipeline to have this update done automatically.

## Links and references

* [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [AWS CodeCommit Documentation](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)
* [Amazon ECS Documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)

This lesson demonstrated creating a CI pipeline with Source and Build stages, validating a build, and pushing code changes to automatically trigger pipeline executions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d608c5f9-ae0c-4023-864f-b30b3099cd6f/lesson/bc66f992-acb5-42e8-b3fe-8a2ca6ab02b1" />
</CardGroup>


# Deploy a new task and service using CodePipeline

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodePipeline-automated-deployment/Deploy-a-new-task-and-service-using-CodePipeline/page

Guide to add an ECS Deploy stage in CodePipeline, update buildspec to produce imagedefinitions.json, and automate rolling deployments via CodeBuild, ECR, and ECS.

Welcome back. In this guide we'll extend the pipeline we built earlier by adding a Deploy stage to automatically push new images to an ECS service. The flow covered here: update the pipeline, ensure CodeBuild produces the required artifact, and confirm ECS performs a rolling deployment.

## 1) Add a Deploy stage in CodePipeline

Edit the pipeline in the CodePipeline console and add a new stage after Build:

* Click Add stage and name it **Deploy**.
* Inside the Deploy stage, click Add action group and provide an action name (for example, `Deploy`).
* For Provider select **Amazon ECS** — do not select the ECR Blue/Green option because this tutorial uses rolling deployments (ECS rolling updates).
* For Input artifacts, pick the artifact produced by the Build stage.
* Choose the Production cluster and the ECS service to deploy.

<Frame>
  <img alt="The image shows a configuration screen for an AWS CodePipeline, with settings for ECS deployment, including fields for action name, region, input artifacts, cluster name, and service name." />
</Frame>

<Callout icon="warning">
  When selecting the provider, pick **Amazon ECS** (rolling deployments). Choosing ECR Blue/Green will switch CodePipeline to a different deployment model that requires a different setup.
</Callout>

In the action configuration, set the Image Definitions filename to `imagedefinitions.json`. Click Done and then Save the pipeline.

<Frame>
  <img alt="The image displays an AWS CodePipeline configuration screen, showing sections for editing pipeline properties, variables, triggers, and source. The pipeline type is listed as V2 with an execution mode of QUEUED." />
</Frame>

## 2) Update the buildspec so CodeBuild produces the required artifact

CodePipeline’s ECS deploy action consumes an artifact named `imagedefinitions.json`. Update the `buildspec.yml` in your Cloud9 (or local) editor to:

* authenticate to ECR,
* build and push the image (tagged by commit hash),
* write the `imagedefinitions.json` artifact,
* replace a placeholder in the ECS task definition, and
* register an updated task definition (optional but useful).

Use this concise buildspec:

```yaml theme={null}
