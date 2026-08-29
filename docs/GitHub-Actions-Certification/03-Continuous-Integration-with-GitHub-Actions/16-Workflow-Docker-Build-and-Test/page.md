# Workflow Docker Build and Test

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Workflow-Docker-Build-and-Test/page

This guide explains how to build a Docker image and run tests using GitHub Actions before publishing to Docker Hub.

In this guide, you'll learn how to build a Docker image and run container tests in a GitHub Actions workflow before publishing it to Docker Hub. This end-to-end CI setup ensures your application image is validated automatically on each commit.

## Prerequisites

Ensure you have the following jobs configured in your workflow:

* **unit-testing**
* **code-coverage**

You’ll also need a step to authenticate with Docker Hub:

```yaml theme={null}
jobs:
  docker:
    name: Containerization
    needs: [unit-testing, code-coverage]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v2.2.0
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}
```

## Using `docker/build-push-action` for Build & Test

We’ll leverage Docker’s official [build-push-action](https://github.com/docker/build-push-action) to compile and test the image locally (`push: false`). This action supports multiple platforms and advanced build features via Buildx.

![GitHub Marketplace page for docker/build-push-action showing usage, examples, customizing, troubleshooting, and contributing sections.](https://kodekloud.com/kk-media/image/upload/v1752876007/notes-assets/images/GitHub-Actions-Certification-Workflow-Docker-Build-and-Test/github-marketplace-docker-images-guide.jpg)

> **lightbulb** By setting `push: false` you prevent the image from being sent to a registry, enabling quick feedback on build and tests.

### Workflow Snippet

```yaml theme={null}
jobs:
  docker:
    name: Containerization
    needs: [unit-testing, code-coverage]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v2.2.0
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}

      - name: Set up QEMU emulator
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker Image for Testing
        uses: docker/build-push-action@v5
        with:
          context: .
          load: true
          push: false
          tags: ${{ vars.DOCKERHUB_USERNAME }}/solar-system:${{ github.sha }}

      - name: Run Container and Test `/live` Endpoint
        run: |
          docker run --rm --name solar-system-app -d \
            -p 3000:3000 \
            -e MONGO_URI=$MONGO_URI \
            -e MONGO_USERNAME=$MONGO_USERNAME \
            -e MONGO_PASSWORD=$MONGO_PASSWORD \
            ${{ vars.DOCKERHUB_USERNAME }}/solar-system:${{ github.sha }}

          echo "Verifying /live endpoint"
          wget -q -O - http://127.0.0.1:3000/live | grep live
```

#### Build & Test Action Summary

| Step                               | Action                          | Key Inputs                        |
| ---------------------------------- | ------------------------------- | --------------------------------- |
| Authenticate to Docker Hub         | `docker/login-action@v2.2.0`    | `username`, `password`            |
| Prepare QEMU for multi-arch builds | `docker/setup-qemu-action@v3`   | (none)                            |
| Enable Buildx                      | `docker/setup-buildx-action@v3` | (none)                            |
| Build & Load Image                 | `docker/build-push-action@v5`   | `context`, `load`, `push`, `tags` |
| Container Sanity Test              | shell command                   | `docker run`, `wget`, `grep`      |

## Dockerfile

Place this `Dockerfile` in your repository root to define the container:

```dockerfile theme={null}
FROM node:18-alpine3.17

WORKDIR /usr/app
COPY package*.json ./
RUN npm install

COPY . .
