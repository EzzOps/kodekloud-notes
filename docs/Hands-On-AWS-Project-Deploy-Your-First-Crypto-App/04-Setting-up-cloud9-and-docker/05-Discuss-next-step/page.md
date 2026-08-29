# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask development server
CMD ["flask", "run"]
```

## Build the Docker image

Build the image locally and tag it (example tag: `my-app`):

```bash theme={null}
docker build -t my-app .
```

Sample (trimmed) build output:

```bash theme={null}
$ docker build -t my-app .
[+] Building 2.6 (4/8)
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 638B
 => [internal] load .dockerignore
 => => transferring context: 2B
 => [internal] load metadata for docker.io/library/python:3.10-slim
 => CACHED [1/4] FROM docker.io/library/python:3.10-slim
 => CACHED [2/4] RUN pip install --no-cache-dir -r requirements.txt
 => CACHED [3/4] COPY . .
 => CACHED [4/4] CMD ["flask", "run"]
 => exporting to image
 => => naming to docker.io/library/my-app
```

After the build completes, the image resides on the EC2 instance backing Cloud9.

## Run the container

Start the container and map container port 5000 to the EC2 instance port 5000:

```bash theme={null}
docker run -p 5000:5000 my-app
```

Sample runtime output (Flask development server):

```bash theme={null}
* Serving Flask app 'app.py' (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Running on http://172.17.0.2:5000/ (Press CTRL+C to quit)
172.17.0.1 - - [17/Feb/2024 12:15:15] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [17/Feb/2024 12:15:16] "GET /favicon.ico HTTP/1.1" 404 -
```

> **lightbulb** Do not use Flask's built-in development server in production. For external deployments, use a production-ready WSGI server such as Gunicorn or uWSGI (for example, `gunicorn -w 4 app:app`).

## Make the app reachable from your browser

Cloud9 runs on an EC2 instance. To access the containerized app from your browser:

1. Find the EC2 instance that backs your Cloud9 environment and open its instance details.
2. If port 5000 is not allowed in the instance's security group, add an inbound rule for TCP port 5000 (or restrict access to your IP).

<Frame>
  <img alt="The image shows an AWS EC2 console with a running instance, displaying details such as instance ID, type (t2.micro), and public IPv4 address." />
</Frame>

Edit the security group inbound rules to add Custom TCP port 5000, then save the changes.

<Frame>
  <img alt="The image shows the AWS EC2 console on the &#x22;Edit inbound rules&#x22; page, where a Custom TCP rule is being configured with port 5000. There's an option to save or preview changes." />
</Frame>

> **warning** Opening ports to the public internet increases attack surface. Prefer restricting inbound access to a specific IP range (your workstation IP) when adding port 5000 to the security group.

After the security group change, copy the EC2 public IPv4 address and open `http://<PUBLIC_IP>:5000` in your browser. The app should load and behave like a local run.

Example flow inside the sample app:

* Log in using the sample credentials.
* Browse the product page, place an order, submit order details, and confirm the order — the shipped/confirmation flow is implemented by the app.

## Default credentials and sample Flask routes

The sample app implements a simple login and order flow with these default credentials:

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if provided credentials match the default ones
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/welcomepage')
def welcome():
    return render_template('product.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    product_id = request.form.get('product')
    # Render order form for product (example)
    return render_template('order_form.html', product_id=product_id)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    address = request.form.get('address')
    quantity = request.form.get('quantity')
    # Here you would process the order, e.g., save it to a database
    return render_template('order_confirmation.html', product_id=product_id, name=name)
```

## Commit the Dockerfile back to Git

From the Cloud9 terminal, verify status, add, commit, and push the Dockerfile and any related changes:

```bash theme={null}
git status
```

Sample `git status` showing untracked files:

```bash theme={null}
$ git status
On branch master
Your branch is up to date with 'origin/master'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    Dockerfile
    requirements.txt

nothing added to commit but untracked files present (use "git add" to track)
```

Add, commit, and push:

```bash theme={null}
git add .
git commit -m "create Dockerfile"
git push origin master
```

Then confirm the files are present in your remote repository.

<Frame>
  <img alt="This image shows an AWS CodeCommit repository named &#x22;aws-microservice-project&#x22; with folders like &#x22;static&#x22; and &#x22;templates&#x22; and files including &#x22;app.py&#x22; and &#x22;Dockerfile.&#x22; The README notes it's an educational website for buying and selling cloud crypto coins." />
</Frame>

## Next steps — production deployment

The image stored on the Cloud9 EC2 instance is local to that instance. For production deployment you should:

* Push the image to a container registry (for example, Amazon ECR).
* Deploy to a container service such as Amazon ECS, Amazon EKS, or AWS Fargate.

Useful links:

* Amazon ECR: [https://aws.amazon.com/ecr/](https://aws.amazon.com/ecr/)
* Amazon ECS: [https://aws.amazon.com/ecs/](https://aws.amazon.com/ecs/)
* Amazon EKS: [https://aws.amazon.com/eks/](https://aws.amazon.com/eks/)
* AWS Fargate: [https://aws.amazon.com/fargate/](https://aws.amazon.com/fargate/)

Quick reference — common commands

| Action                                 | Command                                                                                                                                                                                                                                            |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Build image                            | `docker build -t my-app .`                                                                                                                                                                                                                         |
| Run container (map port)               | `docker run -p 5000:5000 my-app`                                                                                                                                                                                                                   |
| List images                            | `docker images`                                                                                                                                                                                                                                    |
| Push local image to ECR (example flow) | Authenticate: `aws ecr get-login-password ... \| docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com`<br />Tag & push: `docker tag my-app:latest <ECR_REPO_URI>:latest` then `docker push <ECR_REPO_URI>:latest` |

That is it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/f2cfee46-980a-49cb-b81a-dd46bfce3824/lesson/cab57260-fd9a-4fb0-9721-e3112861341d)


# Discuss next step

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Setting-up-cloud9-and-docker/Discuss-next-step/page

Guide to transition from local Cloud9 Docker development to automated AWS CI/CD with CodeCommit, CodeBuild, ECR, and deployment options like ECS EKS or EC2

Hello and welcome back.

Let's review the current project architecture and where we stand.

So far we have:

* Enabled access to the [AWS CodeCommit](https://aws.amazon.com/codecommit/) repository for our developers and ourselves.
* Set up an [AWS Cloud9](https://aws.amazon.com/cloud9/) environment and cloned the CodeCommit repository into it.
* Created a Dockerfile, built the image, and tested the application locally using the [EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) instance that backs Cloud9.

These tasks are complete and the application runs locally inside the Cloud9 environment.

<Frame>
  <img alt="The image shows a project architecture status diagram with AWS Cloud components involving AWS CodeCommit, AWS Cloud9, and Dockerfile, along with key tasks related to setting up Cloud9 and working with Dockerfiles." />
</Frame>

Next, we need to plan the steps required to move from local development to an automated, cloud-based build and deployment process. Below are the primary topics to address, with recommended actions and considerations for each:

1. Where and how to store our Docker artifacts in AWS
   * Source code (including the `Dockerfile`) should remain in your source control repository — `CodeCommit`.
   * Built images should be pushed to Amazon Elastic Container Registry (`ECR`). Use semantic tagging (for example `v1.0.0`, `latest`, or commit SHA) so you can trace deployments to source commits.
   * Configure ECR lifecycle policies to expire old image tags and enable encryption at rest. Consider immutable tags or image scanning to improve supply-chain security.

2. How to create a CI/CD pipeline that automatically builds and publishes the Docker image
   * A typical pipeline flow:
     1. Source: `CodeCommit` (or GitHub) detects a commit.
     2. Build: `CodeBuild` builds the Docker image and runs tests.
     3. Publish: `CodeBuild` authenticates to `ECR` and pushes the image.
     4. Deploy: A deployment stage (ECS/EKS/EC2) pulls the image and updates the running service.
   * Recommended tools:
     * Native AWS: `CodePipeline` + `CodeBuild` → full AWS-managed CI/CD with direct integration to `ECR`.
     * Alternative: GitHub Actions with `ECR` push steps (useful if your team prefers GitHub).
   * Automate container image tagging and versioning, and make sure build logs and artifacts are retained for debugging.

3. Which AWS services and features will implement the end-to-end flow (commit → build → registry → deployment)
   * Common stack:
     * Source: `CodeCommit` or GitHub
     * CI: `CodeBuild`
     * Orchestration: `CodePipeline` (or GitHub Actions)
     * Registry: `ECR`
     * Deployment Targets: `Amazon ECS`, `AWS EKS`, or `EC2` (with Auto Scaling)
   * Evaluate tradeoffs: cost, operational complexity, scalability, and team familiarity.

> **lightbulb** Plan the pipeline with reproducibility and security in mind: use immutable image tags, enable image scanning in `ECR`, and store build artifacts/logs for traceability. Automate tagging using the commit SHA or semantic versioning.

Use the following quick comparison when choosing a deployment target:

| Resource Type           |                        Best for | Notes / When to choose                                                      |
| ----------------------- | ------------------------------: | --------------------------------------------------------------------------- |
| Amazon ECS              | Simpler container orchestration | Low operational overhead; integrates with Fargate for serverless containers |
| AWS EKS                 |            Kubernetes workloads | Choose when you need Kubernetes features or portability across clouds       |
| EC2 (with Auto Scaling) |                VM-based control | Good for lift-and-shift or when you need low-level control of instances     |

Security and permissions are critical for an automated pipeline:

> **warning** Ensure your CI/CD service principal (CodeBuild or GitHub Actions runner) has least-privilege IAM permissions: access to `ECR` push/pull, `CodeCommit`/`S3` as needed, and any deployment APIs. Misconfigured permissions can cause broken builds or expose credentials.

Suggested next steps to implement the pipeline (practical checklist)

* Create an `ECR` repository and set up repository policies and lifecycle rules.
* Create a `CodeBuild` project with a buildspec that builds, tags, and pushes the image to `ECR`.
* Create a `CodePipeline` (or GitHub Actions workflow) that triggers on commits and orchestrates build + push + deploy.
* Pick a deployment target (ECS/Fargate recommended for quick container deployments) and create a task/service definition that references the `ECR` image URI.
* Test the full flow: push a commit → verify `CodeBuild` builds and pushes image → verify the deployment pulls the new image and updates.

Links and references

* [AWS CodeCommit](https://aws.amazon.com/codecommit/)
* [AWS Cloud9](https://aws.amazon.com/cloud9/)
* [Amazon ECR](https://aws.amazon.com/ecr/)
* [AWS CodeBuild](https://aws.amazon.com/codebuild/)
* [AWS CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* [Amazon ECS](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs)
* [AWS EKS](https://learn.kodekloud.com/user/courses/aws-eks)
* [Amazon EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

<Frame>
  <img alt="The image outlines three questions as next steps related to storing a Dockerfile, building a CI pipeline, and using AWS features. It includes numbered steps with corresponding icons." />
</Frame>

That is it for this lesson. Stick with me.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/f2cfee46-980a-49cb-b81a-dd46bfce3824/lesson/36597c01-7d15-4d77-9a00-9e02e0fafd30)
