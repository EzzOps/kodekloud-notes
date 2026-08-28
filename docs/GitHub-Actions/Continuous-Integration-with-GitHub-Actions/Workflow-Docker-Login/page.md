# Placeholder environment variables for MongoDB credentials
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder

EXPOSE 3000
CMD ["npm", "start"]
```

Key steps:

* Start from an official Node.js Alpine base image.
* Install dependencies before copying the rest of the source code.
* Expose port **3000** and set `npm start` as the default command.

## 4. Run Container Tests

After building the image, verify that the application starts and responds to its health endpoint. Replace placeholders with your actual GitHub Secrets or repository variables.

```yaml theme={null}
      - name: Docker Image Testing
        run: |
          # List built images
          docker images

          # Run the container in detached mode
          docker run --name solar-system-app -d \
            -p 3000:3000 \
            -e MONGO_URI=$MONGO_URI \
            -e MONGO_USERNAME=$MONGO_USERNAME \
            -e MONGO_PASSWORD=$MONGO_PASSWORD \
            ${{ vars.DOCKERHUB_USERNAME }}/solar-system:${{ github.sha }}

          # Display container IP address
          echo "Container IP:" $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' solar-system-app)

          # Test the /live endpoint
          echo "Testing /live endpoint"
          wget -q -O - http://127.0.0.1:3000/live | grep live
```

<Callout icon="triangle-alert">
  Ensure that your application exposes health endpoints like `/live` or `/ready` to prevent false positives during automated testing.
</Callout>

## 5. Implement Health Endpoints in Your App

Add health-check routes in your Express application so the workflow can validate container readiness:

```javascript theme={null}
const express = require('express');
const os = require('os');
const path = require('path');
const app = express();

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/os', (req, res) => {
  res.json({ os: os.hostname(), env: process.env.NODE_ENV });
});

app.get('/live', (req, res) => {
  res.json({ status: 'live' });
});

app.get('/ready', (req, res) => {
  res.json({ status: 'ready' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});

module.exports = app;
```

## 6. Monitor the Workflow in GitHub Actions

Once you push your changes, go to the **Actions** tab in your repository to review the workflow run.

<Frame>
  ![The image shows a GitHub Actions page for a project called "Solar System Workflow," displaying a list of workflow runs with their statuses and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752876542/notes-assets/images/GitHub-Actions-Workflow-Docker-Build-and-Test/github-actions-solar-system-workflow.jpg)
</Frame>

Select the **Containerization** job to inspect its steps:

<Frame>
  ![The image shows a GitHub Actions workflow interface for a project named "solar-system," displaying a "docker build and test" process in progress with unit testing and code coverage jobs.](https://kodekloud.com/kk-media/image/upload/v1752876543/notes-assets/images/GitHub-Actions-Workflow-Docker-Build-and-Test/github-actions-solar-system-docker-workflow.jpg)
</Frame>

Watch each step transition to **success**:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a successful "docker build and test" job, including steps like unit testing, code coverage, and containerization.](https://kodekloud.com/kk-media/image/upload/v1752876544/notes-assets/images/GitHub-Actions-Workflow-Docker-Build-and-Test/github-actions-docker-build-test-workflow.jpg)
</Frame>

You can also inspect logs to confirm build arguments, container startup, and endpoint testing:

```bash theme={null}
/usr/bin/docker build --iidfile /tmp/docker-actions-toolkit/iidfile \
  --tag siddharth67/solar-system:[SECRET_REDACTED] .

docker images
docker run --name solar-system-app -d \
  -p 3000:3000 \
  -e MONGO_URI=$MONGO_URI \
  -e MONGO_USERNAME=$MONGO_USERNAME \
  -e MONGO_PASSWORD=$MONGO_PASSWORD \
  siddharth67/solar-system:6127158d890b757e9a46396d6de393edf228

export IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' solar-system-app)
echo $IP

wget -q -O - http://127.0.0.1:3000/live | grep live
```

<Frame>
  ![The image shows a GitHub Actions interface displaying a successful containerization job with details of Docker image testing, including repository names, tags, image IDs, creation times, and sizes.](https://kodekloud.com/kk-media/image/upload/v1752876546/notes-assets/images/GitHub-Actions-Workflow-Docker-Build-and-Test/github-actions-containerization-job-success.jpg)
</Frame>

***

With your image successfully built and validated, you’re now ready to push it to Docker Hub. Continue to the next article to configure the push step in your workflow.

## Links and References

* [GitHub Actions: docker/login-action](https://github.com/docker/login-action)
* [GitHub Actions: docker/build-push-action](https://github.com/docker/build-push-action)
* [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [Express.js Health Checks](https://expressjs.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/a4b43f0a-4c4a-4231-98e1-e975987e2077" />
</CardGroup>


# Workflow Docker Login

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Workflow-Docker-Login/page

This guide explains how to authenticate with Docker Hub in a GitHub Actions pipeline before building and pushing a Docker image.

In this guide, you’ll learn how to extend your GitHub Actions pipeline to authenticate with Docker Hub (or any OCI registry) before building and pushing a Docker image. We assume you already have unit tests and code coverage set up; our focus here is adding a **containerization** job that logs into Docker.

## 1. Current Workflow and Dockerfile

### 1.1. GitHub Actions Workflow

The following workflow runs on pushes to `main` or `feature/*` branches, and can be triggered manually via `workflow_dispatch`:

```yaml theme={null}
name: Solar System Workflow

on:
  push:
    branches:
      - main
      - 'feature/*'
  workflow_dispatch:

env:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
  MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}

jobs:
  unit-testing:
    # … your unit testing steps
  code-coverage:
    # … your coverage steps
```

### 1.2. Dockerfile

Keep this `Dockerfile` at the repository root to build your Node.js image:

```Dockerfile theme={null}
FROM node:18-alpine3.17
WORKDIR /usr/app

COPY package*.json /usr/app/
RUN npm install

COPY . .
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder

EXPOSE 3000
CMD ["npm", "start"]
```

## 2. Add the Containerization Job

Insert a new job named `containerization` after your existing steps. It will:

1. Checkout the repository
2. Authenticate with Docker Hub (or any registry)

```yaml theme={null}
jobs:
  # … unit-testing and code-coverage as before

  containerization:
    name: Containerization
    runs-on: ubuntu-latest
    needs: [unit-testing, code-coverage]
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Docker Login
        uses: docker/login-action@v2
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}
```

<Callout icon="lightbulb">
  The [`docker/login-action`](https://github.com/docker/login-action) supports Docker Hub, GitHub Container Registry, AWS ECR, Google GCR, Azure ACR, and more. It performs `docker login` in the workflow and handles logout post-job.
</Callout>

## 3. Configure Secrets and Variables

You’ll need:

* **Secrets** for sensitive data: `DOCKERHUB_PASSWORD`, `MONGO_PASSWORD`
* **Variables** for non-sensitive values: `DOCKERHUB_USERNAME`, `MONGO_USERNAME`

| Type     | Purpose              | Example              |
| -------- | -------------------- | -------------------- |
| Secret   | Password or token    | `DOCKERHUB_PASSWORD` |
| Variable | Non-sensitive string | `DOCKERHUB_USERNAME` |

1. In your repo, go to **Settings → Secrets and variables**.
2. Under **Actions secrets**, add `DOCKERHUB_PASSWORD`.
3. Under **Actions variables**, add `DOCKERHUB_USERNAME`.

<Frame>
  ![The image shows a GitHub repository settings page for managing "Actions secrets and variables," with options to add new repository secrets and manage existing ones. It lists two repository secrets: "DOCKERHUB\_PASSWORD" and "MONGO\_PASSWORD."](https://kodekloud.com/kk-media/image/upload/v1752876548/notes-assets/images/GitHub-Actions-Workflow-Docker-Login/github-repo-settings-actions-secrets.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub settings page where a new action variable named "DOCKERHUB\_USERNAME" is being added. The interface includes fields for the variable name and value, with guidelines for naming conventions.](https://kodekloud.com/kk-media/image/upload/v1752876548/notes-assets/images/GitHub-Actions-Workflow-Docker-Login/github-settings-add-dockerhub-username.jpg)
</Frame>

## 4. Observe Your Workflow Run

After committing and pushing these changes:

1. Open the **Actions** tab in GitHub.
2. Select your workflow; you’ll see builds triggered by your push.

<Frame>
  ![The image shows a GitHub Actions page displaying a list of workflow runs for a project named "solar-system," with various statuses and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752876550/notes-assets/images/GitHub-Actions-Workflow-Docker-Login/github-actions-solar-system-workflows.jpg)
</Frame>

3. Click on a run to view job dependencies. Notice **Containerization** waits for **unit-testing** and **code-coverage**:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a list of jobs, including unit testing and code coverage, for a project named "solar-system." The current job highlighted is "Unit Testing (20, macos-latest)."](https://kodekloud.com/kk-media/image/upload/v1752876551/notes-assets/images/GitHub-Actions-Workflow-Docker-Login/github-actions-solar-system-workflow.jpg)
</Frame>

4. Once earlier jobs pass, the Docker login step executes:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a successful containerization job, including unit testing and Dockerhub login steps.](https://kodekloud.com/kk-media/image/upload/v1752876552/notes-assets/images/GitHub-Actions-Workflow-Docker-Login/github-actions-workflow-containerization-job.jpg)
</Frame>

Your workflow is now authenticated to Docker Hub. In the next lesson, we’ll build, tag, and push the Docker image.

## Links and References

* [docker/login-action](https://github.com/docker/login-action)
* [GitHub Actions: Variables and Secrets](https://docs.github.com/actions/learn-github-actions/variables#about-environment-variables)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/b8265ed1-9c84-49ba-9a6d-216a0200037b" />
</CardGroup>
