# 1. Infrequently changed – cached once
RUN apt-get update && \
    apt-get install -y \
      python \
      python-dev \
      python3-pip=20.0.2

# 2. Dependencies – rebuild when you add/remove libs
RUN pip3 install flask flask-mysql

# 3. Code – fastest iteration on changes
COPY app.py /opt/source-code

ENTRYPOINT ["flask", "run"]
```

By contrast, placing `COPY app.py` first forces Docker to rerun all subsequent layers on every code update, significantly slowing builds.

***

## Further Reading

* [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [Docker Build Cache Documentation](https://docs.docker.com/engine/reference/commandline/build/#use-build-cache)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/33eeb774-1540-49e9-b5ee-dc051102a116" />
</CardGroup>


# Build Contexts

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Build-Contexts/page

This article explains build contexts in Docker, their impact on build processes, and how to manage them effectively.

In this lesson, we'll explore what a **build context** is and how it influences the Docker build process. Understanding build contexts helps you optimize build times and reduce image size by sending only the necessary files to the Docker daemon.

## What Is a Build Context?

The *build context* is the set of files and folders the Docker CLI packages and sends to the Docker daemon when running `docker build`. By default, Docker uses the current directory (`.`) as the build context.

```bash theme={null}
docker build . -t my-custom-app
```

This command:

1. Archives everything under `.`.
2. Sends it to the Docker daemon.
3. Unpacks it into a temporary directory (e.g., `/var/lib/docker/tmp/...`).
4. Executes the instructions in your `Dockerfile`.

<Callout icon="lightbulb">
  If you omit the `-t` (tag) flag, Docker builds the image and assigns the `latest` tag by default:

  ```bash theme={null}
  docker build .
  # results in an image tagged: IMAGE_ID:latest
  ```
</Callout>

## Example Dockerfile for a Flask App

```dockerfile theme={null}
FROM ubuntu
