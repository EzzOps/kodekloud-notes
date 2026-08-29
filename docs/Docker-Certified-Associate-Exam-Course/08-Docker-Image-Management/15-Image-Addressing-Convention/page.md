# Builder stage
FROM golang:1.19-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Final stage
FROM alpine:latest
COPY --from=builder /app/myapp /usr/local/bin/myapp
ENTRYPOINT ["myapp"]
```

<Callout icon="lightbulb">
  You can name and reuse stages to optimize builds and caching.
</Callout>

## 5. Optimize Your Build Context with .dockerignore

Every file in your build context is sent to the Docker daemon. Exclude unnecessary files to speed up builds and reduce image bloat.

```text theme={null}
# .dockerignore
node_modules
.git
.DS_Store
tests
```

<Callout icon="triangle-alert">
  Forgetting to exclude large directories (e.g., `.git` or `node_modules`) can dramatically increase build time and image size.
</Callout>

***

## Links and References

* [Docker Documentation](https://docs.docker.com/)
* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/bf0b2394-1106-4f4f-8ef6-b61fec69f6be" />
</CardGroup>


# Image Addressing Convention

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Image-Addressing-Convention/page

This article explains how Docker interprets image names, helping avoid naming conflicts and ensuring correct image retrieval from registries.

In this lesson, you’ll learn how Docker interprets image names when you pull or reference them. Understanding these conventions helps you avoid naming conflicts and ensures you’re pulling or pushing images to the correct registry.

## Pulling an Image

For example, running:

```bash theme={null}
docker image pull httpd
```

might look simple—but what does `httpd` actually represent, and where does Docker retrieve it from?

## Docker Image Naming Components

A complete Docker image reference can include up to three parts:

| Component  | Description                                       | Example                         |
| ---------- | ------------------------------------------------- | ------------------------------- |
| Registry   | Hostname of the registry (defaults to Docker Hub) | `docker.io`                     |
| Namespace  | User or organization under which the image lives  | `library` (for official images) |
| Repository | Name of the image project                         | `httpd`                         |

### Implicit Namespace

When you specify only `httpd`, Docker assumes you want the official image from Docker Hub’s **library** namespace.\
Effectively, Docker interprets:

```yaml theme={null}
image: library/httpd
```

Here, `library` is the namespace for curated, official images on Docker Hub, and `httpd` is the repository name.

### Default Registry

By default, Docker pulls from Docker Hub (`docker.io`). Omitting the registry is shorthand for:

```yaml theme={null}
image: docker.io/library/httpd
```

The registry is where images are stored. When you build and push an image, it goes to this registry; when you pull, it comes from here.

<Callout icon="lightbulb">
  You can verify the full reference of an existing image with:

  ```bash theme={null}
  docker image inspect httpd --format '{{.RepoDigests}}'
  ```
</Callout>

## Referencing Other Registries

If your image lives in a different registry—such as Google Container Registry or a private registry—you must prepend the registry hostname:

```yaml theme={null}
