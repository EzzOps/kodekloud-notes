# Google Container Registry (GCR)
image: gcr.io/your-project/httpd

# Private registry
image: registry.example.com/your-namespace/httpd
```

Before interacting with private registries, authenticate using:

```bash theme={null}
docker login <registry-hostname>
```

<Callout icon="triangle-alert">
  Always ensure you’re logged in to the correct registry. Pushing to the wrong registry can overwrite critical images.
</Callout>

***

## Links and References

* [Docker Image Overview](https://docs.docker.com/engine/reference/commandline/image/)
* [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
* [Google Container Registry](https://cloud.google.com/container-registry)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/e8931b12-5d64-4451-baf3-49a6376bad10" />
</CardGroup>


# Inspecting a Docker Image

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Inspecting-a-Docker-Image/page

This guide explores essential Docker CLI commands for optimizing, debugging, and securing container workflows by inspecting Docker images.

Understanding how Docker images are built from multiple layers can help you optimize, debug, and secure your container workflows. In this guide, we’ll explore essential Docker CLI commands to:

* List local images
* Examine image history
* Inspect detailed metadata
* Filter output with JSONPath

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Listing Local Images](#listing-local-images)
3. [Viewing Image History](#viewing-image-history)
4. [Inspecting Image Metadata](#inspecting-image-metadata)
5. [Filtering with JSONPath](#filtering-with-jsonpath)
6. [References](#references)

## Prerequisites

<Callout icon="lightbulb">
  Ensure you have Docker installed and running. Check your version with `docker version`.\
  For full installation steps, visit the [Docker Docs](https://docs.docker.com/get-docker/).
</Callout>

## Listing Local Images

To see all images stored on your host machine, use:

```bash theme={null}
docker image list
```

Example output:

```bash theme={null}
REPOSITORY    TAG       IMAGE ID       CREATED       SIZE
httpd         latest    c2aa7e16edd8   2 weeks ago   165MB
ubuntu        latest    549b9b86cb8d   4 weeks ago   64.2MB
```

| Command             | Description             |
| ------------------- | ----------------------- |
| `docker image list` | List all images locally |

## Viewing Image History

Examining an image’s history reveals each layer and the command that created it. This is especially valuable if the Dockerfile isn’t available.

```bash theme={null}
docker image history ubuntu
```

Sample output:

```bash theme={null}
IMAGE          CREATED        CREATED BY                                      SIZE
549b9b86cb8d   4 weeks ago    /bin/sh -c #(nop) CMD ["/bin/bash"]             0B
<missing>      4 weeks ago    /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>      4 weeks ago    /bin/sh -c set -xe && echo '#!/bin/sh' > ./…    745B
<missing>      4 weeks ago    /bin/sh -c [ -z "$(apt-get indextargets)" ]      987kB
<missing>      4 weeks ago    /bin/sh -c #(nop) ADD file:53f100793e6c0adfc…   63.2MB
```

| Command                        | Description                        |
| ------------------------------ | ---------------------------------- |
| `docker image history <IMAGE>` | Show layer-by-layer build commands |

## Inspecting Image Metadata

The `inspect` command returns comprehensive image metadata in JSON format, including environment variables, exposed ports, volumes, and more.

```bash theme={null}
docker image inspect ubuntu
```

Abbreviated example:

```json theme={null}
[
  {
    "Id": "549b9b86cb8d...",
    "RepoTags": ["ubuntu:latest"],
    "Created": "2020-09-15T23:05:57.348340124Z",
    "ContainerConfig": {
      "ExposedPorts": {
        "80/tcp": {}
      }
    },
    "DockerVersion": "18.09.7",
    "Architecture": "amd64",
    "Os": "linux",
    "Size": 137532780
  }
]
```

<Callout icon="triangle-alert">
  Inspecting very large images may output extensive JSON. Use filtering (see next section) or redirect output to a file:

  ```bash theme={null}
  docker image inspect ubuntu > ubuntu-inspect.json
  ```
</Callout>

| Command                        | Description                        |
| ------------------------------ | ---------------------------------- |
| `docker image inspect <IMAGE>` | Display full image metadata (JSON) |

## Filtering with JSONPath

Docker’s `inspect` supports the `-f` flag with [JSONPath](https://kubernetes.io/docs/reference/kubectl/jsonpath/) templates to extract specific fields.

### Common Filters

| Filter Template                  | Description                 |
| -------------------------------- | --------------------------- |
| `-f '{{.Os}}'`                   | Display the OS              |
| `-f '{{.Architecture}}'`         | Show the architecture       |
| `-f '{{.Architecture}} {{.Os}}'` | Combine architecture and OS |

```bash theme={null}
docker image inspect httpd -f '{{.Os}}'
docker image inspect httpd -f '{{.Architecture}}'
docker image inspect httpd -f '{{.Architecture}} {{.Os}}'
