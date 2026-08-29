# Pulls the Ubuntu image with the default 'latest' tag
docker pull ubuntu

# Both commands are equivalent
docker run ubuntu
docker run ubuntu:latest
```

To pull a specific version, specify its tag. For example, Ubuntu 18.04 is tagged as `bionic`, and Ubuntu 14.04 as `trusty`:

```bash theme={null}
docker pull ubuntu:bionic
```

## Listing and Searching Images from the CLI

### List Local Images

To display all images on your host:

```bash theme={null}
docker image ls
```

Example output:

```bash theme={null}
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
ubuntu       latest    549b9b86cb8d   4 weeks ago     64.2MB
```

### Search Docker Hub from Terminal

```bash theme={null}
docker search httpd
```

By default, this returns up to 25 results. To limit the output (maximum 100):

```bash theme={null}
docker search httpd --limit 2
```

### Filter Search Results

Use filters like `stars` and `is-official` to refine results:

```bash theme={null}
# HTTPD images with at least 10 stars
docker search httpd --filter stars=10

# Only official HTTPD images
docker search httpd --filter is-official=true

# Combine multiple filters
docker search httpd --filter stars=10 --filter is-official=true
```

## Pulling Images Without Running Containers

If you only want to download an image without starting a container:

```bash theme={null}
docker image pull httpd
```

Example output:

```bash theme={null}
Using default tag: latest
latest: Pulling from library/httpd
8ec398bc0356: Pull complete
354e6904d655: Pull complete
27298e4c749a: Pull complete
10e27104ba69: Pull complete
36412f6b2f6e: Pull complete
Digest: sha256:[SECRET_REDACTED]
Status: Downloaded newer image for httpd:latest
docker.io/library/httpd:latest
```

Verify the image is present:

```bash theme={null}
docker image ls
```

***

That concludes this lesson on Docker image registries. In the next lesson, we’ll dive into container management.

## References

* [Docker Hub](https://hub.docker.com/)
* [Docker Trusted Registry](https://docs.docker.com/enterprise/registry/)
* [Google Container Registry](https://cloud.google.com/container-registry)
* [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/)
* [Azure Container Registry](https://azure.microsoft.com/services/container-registry/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/5beff39a-71c3-425e-8cb0-14e914c67626" />
</CardGroup>


# Docker commit method

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Docker-commit-method/page

Learn to create a Docker image from a running container using docker container commit for rapid prototyping or debugging changes.

In this guide, you’ll learn how to create a Docker image from a running container using `docker container commit`. This technique can be useful for rapid prototyping or debugging changes without writing a Dockerfile. For production-grade images, you should still prefer the Dockerfile approach to ensure repeatability and version control.

## Overview

Typically, custom images are built with a Dockerfile:

```bash theme={null}
docker build -t myapp:latest .
```

Alternatively, you can:

1. Launch a container from a base image (e.g., `httpd`).
2. Modify files or install packages inside the container.
3. Commit the container’s state as a new image.

<Callout icon="triangle-alert">
  The `docker commit` workflow is not recommended for production systems. Use a Dockerfile for maintainability, readability, and versioning.
</Callout>

## When to Use `docker commit`

| Scenario                        | Recommended? | Alternative           |
| ------------------------------- | ------------ | --------------------- |
| One-off experiments             | Yes          | Dockerfile (optional) |
| Capturing state for debugging   | Yes          | Volumes, logging      |
| Production-ready, repeatable CI | No           | Dockerfile            |

## Step-by-Step Example

1. **Run an `httpd` container in detached mode**
   ```bash theme={null}
   docker run -d --name httpd httpd
   ```

2. **Enter the container and update the default web page**
   ```bash theme={null}
   docker exec -it httpd bash
   root@container:/# cat > /usr/local/apache2/htdocs/index.html <<EOF
   Welcome to my custom web application
   EOF
   root@container:/# exit
   ```

3. **Commit the container state to a new image**
   ```bash theme={null}
   docker container commit -a "Ravi" httpd customhttpd
   ```

4. **Verify the new image**
   ```bash theme={null}
   docker image ls
   REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
   customhttpd   latest    adac0f56a7df   5 seconds ago   138MB
   httpd         latest    417af7dc28bc   8 days ago      138MB
   ```

## Comparison: Dockerfile vs. `docker commit`

| Feature                      | Dockerfile       | `docker commit`    |
| ---------------------------- | ---------------- | ------------------ |
| Version control              | Yes (plain text) | No                 |
| Automation                   | CI/CD pipelines  | Manual or scripted |
| Reproducibility              | High             | Low                |
| Ease of simple tweaks        | Moderate         | Very fast          |
| Best practice for production | ✔                | ✖                  |

## References

* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [docker container commit](https://docs.docker.com/engine/reference/commandline/container_commit/)
* [docker exec documentation](https://docs.docker.com/engine/reference/commandline/exec/)
* [Docker image management](https://docs.docker.com/engine/reference/commandline/image_ls/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/d27a2ba1-260e-4ec8-b4b1-098db4ef3216" />
</CardGroup>
