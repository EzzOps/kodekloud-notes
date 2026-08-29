# Placeholder environment variables for local tests
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder

EXPOSE 3000
CMD ["npm", "start"]
```

This configuration:

* Starts from the lightweight Node.js 18 Alpine image
* Sets `/usr/app` as the working directory
* Installs dependencies from `package.json`
* Copies the rest of your application code
* Defines default environment variables for MongoDB
* Exposes port 3000 and launches the app using `npm start`

## Application Health Endpoints

Ensure your Express app exposes a simple `/live` endpoint for the workflow test. Example in `app.js`:

```javascript theme={null}
const express = require('express');
const path = require('path');
const os = require('os');
const app = express();

app.get('/live', (req, res) => {
  res.json({ status: "live" });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/os', (req, res) => {
  res.json({
    os: os.hostname(),
    env: process.env.NODE_ENV
  });
});

app.get('/ready', (req, res) => {
  res.json({ status: "ready" });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});

module.exports = app;
```

> **triangle-alert** Be sure your placeholder environment variables in the Dockerfile match those used in your test commands to avoid runtime errors.

## Workflow Run Results

Once the workflow is committed, GitHub Actions will execute the build-and-test job. You’ll see output like this:

![GitHub Actions page showing the "Solar System Workflow" runs with statuses and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752876009/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Build-and-Test/github-actions-solar-system-workflow.jpg)

![GitHub Actions interface for the "docker build and test" job running under the "solar-system" workflow, showing progress and success of each step.](https://kodekloud.com/kk-media/image/upload/v1752876010/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Build-and-Test/github-actions-solar-system-docker-workflow.jpg)

Example build logs:

```bash theme={null}
/usr/bin/docker buildx build \
  --iidfile /tmp/docker-actions-toolkit/iidfile \
  --tag youruser/solar-system:abcdef \
  --metadata-file /tmp/docker-actions-toolkit/metadata-file .

#1 [auth] library/node:pull token for registry-1.docker.io
#6 [1/5] FROM docker.io/library/node:18-alpine3.17
...
#11 DONE 1.6s
```

And container test output:

```bash theme={null}
$ docker images
REPOSITORY                   TAG      IMAGE ID       SIZE
youruser/solar-system        abcdef   e7789ef9a9...  110MB

$ docker run --name solar-system-app -d -p 3000:3000 \
    -e MONGO_URI=uriPlaceholder \
    -e MONGO_USERNAME=usernamePlaceholder \
    -e MONGO_PASSWORD=usernamePlaceholder \
    youruser/solar-system:abcdef

$ echo "Testing /live endpoint"
$ wget -q -O - http://127.0.0.1:3000/live | grep live
live
```

Since all steps pass, your Docker image is successfully built and tested locally. Next up: pushing it to Docker Hub and deploying!

***

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Docker Build-Push Action](https://github.com/docker/build-push-action)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/6c67d5e4-b1b3-4cf8-9f06-e105774726c5)


# Workflow Docker Login

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Workflow-Docker-Login/page

This guide explains integrating Docker Hub authentication into GitHub Actions for automatic Docker image building and pushing after tests.

In this guide, you’ll learn how to integrate Docker Hub authentication into your GitHub Actions CI/CD pipeline. By the end, your workflow will automatically build and push a Docker image once unit tests and code coverage checks have passed.

## Prerequisites

* A GitHub repository containing your application code and a `Dockerfile`.
* Unit tests and code coverage steps already configured in your workflow.
* Docker Hub account with repository access.

## 1. Existing Workflow Overview

Below is an example workflow that runs unit tests and measures code coverage on every push to `main` or any `feature/*` branch:

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
  unit-testing: …
  code-coverage: …
```

## 2. Dockerfile for the Application

Ensure your repository includes a `Dockerfile` like this:

```dockerfile theme={null}
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

## 3. Add the Containerization Job

We’ll create a new job named `containerization` that depends on the previous jobs. This job will:

1. Check out the repository.
2. Authenticate to Docker Hub.
3. Build and push the Docker image.

```yaml theme={null}
jobs:
  unit-testing: …
  code-coverage: …

  containerization:
    name: Containerization
    needs: [unit-testing, code-coverage]
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}

      - name: Build Docker Image
        run: |
          docker build -t my-app:${{ github.sha }} .
          
      - name: Push Docker Image
        run: |
          docker push my-app:${{ github.sha }}
```

> **lightbulb** Replace `my-app` with your Docker Hub repository name (e.g., `username/solar-system`).\
  You can also tag with `:latest` or semantic versions.

## 4. Store Credentials as Variables and Secrets

To prevent exposing your Docker Hub credentials in the workflow, add them via the GitHub UI:

| Name                | Type     | Location                                               |
| ------------------- | -------- | ------------------------------------------------------ |
| DOCKERHUB\_USERNAME | Variable | Settings → Secrets and variables → Actions → Variables |
| DOCKERHUB\_PASSWORD | Secret   | Settings → Secrets and variables → Actions → Secrets   |

1. Go to **Settings > Secrets and variables > Actions**.
2. Under **Repository variables**, click **New repository variable** and add `DOCKERHUB_USERNAME`.
3. Under **Repository secrets**, click **New repository secret** and add `DOCKERHUB_PASSWORD`.

![Add a new secret in GitHub repository settings](https://kodekloud.com/kk-media/image/upload/v1752876011/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Login/github-repo-settings-add-secret.jpg)

![Manage Actions secrets and variables in GitHub repository settings](https://kodekloud.com/kk-media/image/upload/v1752876012/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Login/github-repo-settings-actions-secrets.jpg)

![Add a new Actions variable for Docker Hub username](https://kodekloud.com/kk-media/image/upload/v1752876013/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Login/github-settings-action-variable-dockerhub.jpg)

![Overview of Actions secrets and variables management](https://kodekloud.com/kk-media/image/upload/v1752876014/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Login/github-repo-settings-actions-secrets-2.jpg)

> **triangle-alert** Never hardcode sensitive credentials in your workflow files. Always use **Secrets** for passwords and **Variables** for non-sensitive values.

## 5. Commit and Push

After updating `.github/workflows/ci.yml` (or your workflow filename), commit your changes and push to the repository:

```bash theme={null}
git add .github/workflows/ci.yml
git commit -m "chore: add Docker login and image push"
git push
```

## 6. Verify the Workflow Run

1. Navigate to the **Actions** tab in your repository.
2. Select the latest run of your workflow.
3. Confirm that:
   * The `containerization` job starts only after `unit-testing` and `code-coverage`.
   * The Docker Hub login step completes without printing your password.

![List of workflow runs in GitHub Actions](https://kodekloud.com/kk-media/image/upload/v1752876015/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Login/github-actions-solar-system-workflows.jpg)

![Successful containerization job with Docker Hub login step](https://kodekloud.com/kk-media/image/upload/v1752876016/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Login/github-actions-workflow-docker-containerization.jpg)

Congratulations! You have successfully set up Docker Hub login within your GitHub Actions pipeline, enabling automatic building and publishing of your container images.

***

## Links and References

* [docker/login-action](https://github.com/docker/login-action)
* [GitHub Actions Secrets and variables](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [Docker Hub Documentation](https://docs.docker.com/docker-hub/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/1b596692-1438-444d-b75b-db956f270a83)
