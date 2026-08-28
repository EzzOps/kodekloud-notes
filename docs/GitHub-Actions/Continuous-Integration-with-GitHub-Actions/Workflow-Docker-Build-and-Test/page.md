# Workflow Docker Build and Test

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Workflow-Docker-Build-and-Test/page

This guide explains a GitHub Actions workflow for building, testing, and preparing Docker images for publishing to Docker Hub.

In this guide, we’ll walk through a GitHub Actions workflow that builds a Docker image, validates it with runtime tests, and prepares it for publishing to Docker Hub.

## 1. Authenticate with Docker Hub

Before building your container, log in to Docker Hub securely using the official `docker/login-action`.

```yaml theme={null}
jobs:
  docker:
    name: Containerization
    needs: [unit-testing, code-coverage]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Docker Hub Login
        uses: docker/login-action@v2.2.0
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}
```

<Callout icon="lightbulb">
  Store your Docker Hub credentials as [GitHub Secrets](/docs/github/creating-secrets-for-workflows) or repository variables to avoid exposing sensitive data in your workflow YAML.
</Callout>

## 2. Build the Image for Testing

Use the `docker/build-push-action` to build your image locally without pushing it immediately. This allows you to run integration or health checks before publishing.

<Frame>
  ![The image shows a webpage from GitHub Marketplace detailing sections on usage, examples, customizing, troubleshooting, and contributing for building and pushing Docker images.](https://kodekloud.com/kk-media/image/upload/v1752876541/notes-assets/images/GitHub-Actions-Workflow-Docker-Build-and-Test/github-marketplace-docker-images-guide.jpg)
</Frame>

```yaml theme={null}
      - name: Build Docker Image for Testing
        uses: docker/build-push-action@v4
        with:
          context: .
          push: false
          tags: ${{ vars.DOCKERHUB_USERNAME }}/solar-system:${{ github.sha }}
```

For more customization options, refer to the official documentation: [docker/build-push-action](https://github.com/docker/build-push-action).

## 3. Define Your Dockerfile

Place a `Dockerfile` at the root of your repository to specify the container environment:

```dockerfile theme={null}
FROM node:18-alpine3.17

WORKDIR /usr/app

COPY package*.json ./
RUN npm install

COPY . .
