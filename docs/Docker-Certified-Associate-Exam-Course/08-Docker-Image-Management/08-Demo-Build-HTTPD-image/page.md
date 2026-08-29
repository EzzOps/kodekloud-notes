# Downloads to /testdir/app.tar.xz
ADD http://example.com/app.tar.xz /testdir

# Extract & build in a separate step
RUN tar -xJf /testdir/app.tar.xz -C /tmp/app \
    && make -C /tmp/app
```

<Callout icon="lightbulb">
  For clarity and layer reduction, consider using a single `RUN` with `curl` and `tar` instead of `ADD`.
</Callout>

***

## Best Practices

* Use `COPY` for straightforward file and directory transfers.
* Reserve `ADD` for:
  * Local archive auto-extraction (`.tar`, `.tar.gz`, etc.).
  * Quick remote downloads without further processing.
* Combine commands in a single `RUN` to minimize image layers and overall size.

***

## Links and References

* [Dockerfile reference: COPY](https://docs.docker.com/engine/reference/builder/#copy)
* [Dockerfile reference: ADD](https://docs.docker.com/engine/reference/builder/#add)
* [Docker best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/d919e735-ad69-48d7-9186-bd69290c4c7f" />
</CardGroup>


# Demo Build HTTPD image

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Demo-Build-HTTPD-image/page

This tutorial teaches how to build a lightweight custom Docker image for an HTTPD web server on CentOS 7.

In this tutorial, you’ll learn how to build a lightweight, custom Docker image for an HTTPD (Apache) web server on CentOS 7. We’ll cover:

* Setting up the build context
* Crafting an optimized `Dockerfile`
* Adding a simple `index.html`
* Building, testing, and pushing your image to Docker Hub

By following these steps, you’ll gain hands-on experience with multi-layered Docker images and best practices for containerized web servers.

***

## 1. Prepare the Build Context

First, create an isolated directory for all build artifacts. This ensures that nothing outside the folder is accidentally added to your image.

```bash theme={null}
cd /tmp
mkdir firstimage && cd firstimage
ls -1
