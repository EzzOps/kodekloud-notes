# Base vs Parent Image

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Base-vs-Parent-Image/page

This article explains the concepts of base and parent images in Docker, detailing their roles in image creation and hierarchy.

In Docker, every custom image starts “FROM” another image—its parent. Tracing this chain leads to the special `scratch` image, the true base for all builds.

<Callout icon="lightbulb">
  A **base image** is the origin of an image chain (often `scratch`), while a **parent image** is the one directly referenced by your `FROM` instruction.
</Callout>

## 1. Custom Web Application Image

Create a minimal Apache-based web server by extending the official HTTPD image:

```dockerfile theme={null}
FROM httpd
COPY index.html /usr/local/apache2/htdocs/index.html
```

* **Parent image**: `httpd`
* Your `COPY` command layers application files on top of the Apache HTTPD server.

## 2. Inside the HTTPD Official Image

The official HTTPD image itself builds on Debian:

```dockerfile theme={null}
FROM debian:buster-slim

ENV HTTPD_PREFIX=/usr/local/apache2
ENV PATH=$HTTPD_PREFIX/bin:$PATH
WORKDIR $HTTPD_PREFIX
