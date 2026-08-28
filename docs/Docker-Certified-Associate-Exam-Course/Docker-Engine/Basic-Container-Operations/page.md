# Basic Container Operations

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Basic-Container-Operations/page

Master the essentials of Docker CLI to create, manage, and troubleshoot containers efficiently.

Master the essentials of Docker CLI to create, manage, and troubleshoot containers efficiently. This guide covers key commands, options, and best practices for container operations.

## Table of Contents

* [Quick Syntax Reference](#quick-syntax-reference)
* [Command Syntax Styles](#command-syntax-styles)
* [Creating a Container](#creating-a-container)
* [Listing Containers](#listing-containers)
* [Starting a Container](#starting-a-container)
* [Create & Start in One Step](#create--start-in-one-step)
* [Ephemeral Containers](#ephemeral-containers)
* [Interactive Shells](#interactive-shells)
* [Exiting Containers](#exiting-containers)
* [Naming Containers](#naming-containers)
* [Detached Mode](#detached-mode)
* [Links and References](#links-and-references)

***

## Quick Syntax Reference

Use this general pattern for Docker commands:

```bash theme={null}
docker [object] [command] [options] [arguments]
```

Examples:

```bash theme={null}
docker image ls
docker container run -it ubuntu
docker image build .
docker container attach <container>
docker container kill <container>
```

***

## Command Syntax Styles

Docker supports both legacy and grouped syntax. We’ll use the **grouped** style throughout this guide.

| Syntax Type   | Example                           |
| ------------- | --------------------------------- |
| Grouped (new) | `docker container run -it ubuntu` |
| Legacy (old)  | `docker run -it ubuntu`           |

***

## Creating a Container

To create (but not start) a container:

```bash theme={null}
docker container create httpd
```

Sample output:

```Docker theme={null}
Unable to find image 'httpd:latest' locally
latest: Pulling from library/httpd
…
Status: Downloaded newer image for httpd:latest
[SECRET_REDACTED]
```

On Linux, Docker stores images and container metadata under `/var/lib/docker/`:

```bash theme={null}
ls /var/lib/docker/
