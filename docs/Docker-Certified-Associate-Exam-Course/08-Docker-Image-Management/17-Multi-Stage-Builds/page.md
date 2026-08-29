# Output: amd64 linux
```

### Retrieving Exposed Ports

To list all ports exposed by an image:

```bash theme={null}
docker image inspect httpd \
  -f '{{range $p := .ContainerConfig.ExposedPorts}}{{printf "%s " $p}}{{end}}'
```

Example output:

```bash theme={null}
80/tcp 
```

## References

* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
* [Docker Inspect](https://docs.docker.com/engine/reference/commandline/inspect/)
* [JSONPath Guide](https://kubernetes.io/docs/reference/kubectl/jsonpath/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/50617d16-47a8-40d2-8c3c-4d5a32117922" />
</CardGroup>


# Multi Stage Builds

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Multi-Stage-Builds/page

This article explains how to use Dockers multi-stage builds to streamline the containerization of Node.js applications, producing smaller and more efficient images.

Containerizing a Node.js web application often involves separate build and packaging steps. Docker’s **multi-stage builds** streamline this process into a single, maintainable Dockerfile that produces smaller, more consistent images.

## 1. Local Build and Basic Containerization

First, you might compile your app locally:

```bash theme={null}
npm run build
```

This generates a `dist/` folder with your production assets. To serve it via Nginx, you could write:

```dockerfile theme={null}
