# Use an official Python runtime as a parent image
FROM python:3.10-slim
```

Explanation: `python:3.10-slim` provides a small footprint image with the Python runtime you need. Using a slim base reduces build time and image size.

2. Set the working directory inside the container

```dockerfile theme={null}
# Set the working directory in the container
WORKDIR /usr/src/app
```

Explanation: `WORKDIR` sets the working directory for subsequent commands and the process run inside the image. It helps keep paths consistent.

3. Copy the application source code and install dependencies from `requirements.txt`

```dockerfile theme={null}
# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
```

Explanation: `COPY . .` copies your project into the image. The `RUN pip install --no-cache-dir -r requirements.txt` installs dependencies without caching to keep the image lean.

4. Expose the Flask default port (5000) and define environment variables and the run command

```dockerfile theme={null}
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]
```

Explanation: `EXPOSE 5000` documents the port the app listens on. Setting `FLASK_RUN_HOST=0.0.0.0` ensures the Flask development server listens on all network interfaces inside the container so the service is reachable from outside the container. The `CMD` runs the Flask development server by default.

<Callout icon="lightbulb">
  If you want to avoid sending build-context files into the image (for example `.git` or local virtualenvs), add a `.dockerignore` file listing those paths.
</Callout>

Warning: development server vs production

<Callout icon="warning">
  The Flask development server is not intended for production use. For production deployments, replace the `flask run` command with a production-grade WSGI server such as `gunicorn` (for example: `CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]`), and ensure proper configuration for logging, health checks, and process management.
</Callout>

Final combined Dockerfile

```dockerfile theme={null}
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

# Run the Flask application
CMD ["flask", "run"]
```

Quick reference table: Dockerfile directives and purpose

| Directive | Purpose                                          | Example / Notes                                      |
| --------- | ------------------------------------------------ | ---------------------------------------------------- |
| `FROM`    | Base image with runtime                          | `FROM python:3.10-slim`                              |
| `WORKDIR` | Sets working directory inside container          | `WORKDIR /usr/src/app`                               |
| `COPY`    | Copies project files into the image              | `COPY . .`                                           |
| `RUN`     | Runs commands at build time (e.g., install deps) | `RUN pip install --no-cache-dir -r requirements.txt` |
| `EXPOSE`  | Documents the port the container listens on      | `EXPOSE 5000`                                        |
| `ENV`     | Set environment variables inside the image       | `ENV FLASK_APP=app.py`                               |
| `CMD`     | Default command to run when container starts     | `CMD ["flask", "run"]`                               |

Build and test locally

1. Build the image (run from the project root where the Dockerfile resides):

```bash theme={null}
docker build -t flask-app .
```

2. Run the container and map the port to your host:

```bash theme={null}
docker run -p 5000:5000 flask-app
```

3. Visit `http://localhost:5000` in your browser to verify the app is running.

Troubleshooting tips

* If dependencies fail to install, check `requirements.txt` for platform-specific packages or missing packages.
* Use `docker build --no-cache -t flask-app .` to rebuild from scratch if you suspect a caching issue.
* Inspect the running container logs with `docker logs <container-id>`.

Links and references

* [Dockerfile reference — Docker Docs](https://docs.docker.com/engine/reference/builder/)
* [Flask documentation](https://flask.palletsprojects.com/)
* [Gunicorn — Python WSGI HTTP Server](https://gunicorn.org/)

With the Dockerfile in place you can now build and run the image locally to verify the containerized app works as expected. The next section can walk you through pushing the image to a registry or deploying it to a container platform.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/f2cfee46-980a-49cb-b81a-dd46bfce3824/lesson/9eacc776-f8d1-40e5-9269-a9fef1a9b4d3" />
</CardGroup>


# Project architecture status

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodeBuild-and-ECR/Project-architecture-status/page

Overview of using AWS CodeBuild, CodeCommit, and Amazon ECR to build, tag, push, and validate Docker images using buildspec.yml and EC2 or local testing

Welcome back.

This lesson reviews the current project status and recaps what we've completed so far. The focus is on how CodeBuild, CodeCommit, and Amazon ECR fit together in our CI workflow, how the Docker image is produced and validated, and the commands you can reuse to reproduce or debug the flow.

We have completed the following:

* Set up AWS CodeBuild and integrated it with AWS CodeCommit for automated builds.
* Configured CodeBuild to use a `buildspec.yml` file to produce Docker images during the build lifecycle.
* Pushed the resulting Docker image into Amazon ECR (Elastic Container Registry).
* Validated the Docker image by running it on an EC2 instance.
* Learned how to authenticate locally to ECR so developers can pull and test images on their machines.

<Frame>
  <img alt="The image shows a project architecture status diagram with components including AWS CodeBuild, AWS CodeCommit, and a Registry, along with key tasks completed such as setting up ECR and testing Docker images." />
</Frame>

What to remember

* CodeBuild reads the `buildspec.yml` in your repository root (or a path you specify in the CodeBuild project). It executes the standard phases: `install`, `pre_build`, `build`, and `post_build`. Make sure `buildspec.yml` is in the intended location and correctly formatted YAML.
* The Docker image produced during the build must be tagged for your ECR repository and pushed using authenticated Docker commands. Typical steps are to obtain ECR auth token, log in Docker, tag the image, and push.
* To validate images on EC2, authenticate the instance to ECR the same way you authenticate locally, then `docker pull` the image and run it with `docker run`.

Quick reference: common commands and snippets

* Authenticate Docker to ECR (Linux/macOS):

```bash theme={null}
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<REGION>.amazonaws.com
```

* Tag and push the image:

```bash theme={null}
docker tag my-app:latest <account-id>.dkr.ecr.<REGION>.amazonaws.com/my-repo:latest
docker push <account-id>.dkr.ecr.<REGION>.amazonaws.com/my-repo:latest
```

* Pull and run on EC2 (after authenticating on the instance):

```bash theme={null}
docker pull <account-id>.dkr.ecr.<REGION>.amazonaws.com/my-repo:latest
docker run -d -p 80:80 <account-id>.dkr.ecr.<REGION>.amazonaws.com/my-repo:latest
```

* Minimal `buildspec.yml` example (used by CodeBuild to build and push a Docker image):

```yaml theme={null}
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
  build:
    commands:
      - echo Build started on `date`
      - docker build -t my-repo:latest .
      - docker tag my-repo:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/my-repo:latest
  post_build:
    commands:
      - echo Pushing the Docker image...
      - docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/my-repo:latest
artifacts:
  files:
    - '**/*'
```

Checklist: where to find things and why they matter

| Artifact          |                                    Purpose | Example / Notes                                               |
| ----------------- | -----------------------------------------: | ------------------------------------------------------------- |
| `buildspec.yml`   |   Defines CodeBuild lifecycle and commands | Place in repository root or reference it in CodeBuild project |
| ECR repository    |                 Stores built Docker images | Use `docker tag` and `docker push` to upload images           |
| CodeBuild project |             Runs the build & push pipeline | Connects to CodeCommit, GitHub, or other source providers     |
| EC2 validation    | Confirms the image runs in a real instance | Authenticate to ECR from EC2 before `docker pull`             |

<Callout icon="warning">
  Do not commit credentials, tokens, or long-lived secrets into your repository. Use IAM roles (for CodeBuild and EC2) or secrets managers to provide secure access to ECR and other resources.
</Callout>

<Callout icon="lightbulb">
  Summary of completed tasks: ECR setup, CodeBuild project creation and integration with CodeCommit, `buildspec.yml`-driven Docker builds, pushing images to ECR, and validating images from both EC2 and local development environments.
</Callout>

Further reading and references

* AWS CodeBuild documentation: [https://docs.aws.amazon.com/codebuild/](https://docs.aws.amazon.com/codebuild/)
* Amazon ECR documentation: [https://docs.aws.amazon.com/AmazonECR/](https://docs.aws.amazon.com/AmazonECR/)
* Docker CLI documentation: [https://docs.docker.com/engine/reference/commandline/cli/](https://docs.docker.com/engine/reference/commandline/cli/)

That’s it for this lesson — see you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/37195f61-a068-4f6c-9ccc-0bd66b358449/lesson/a87b294a-1760-4e00-9f94-708455617b60" />
</CardGroup>
