# builder  buildkit  containers  image  network  overlay2  plugins  runtimes  swarm  tmp  trust  volumes
```

Each container’s data lives in `containers/<container-ID>/`.

***

## Listing Containers

Use `docker container ls` with options to filter the output:

| Command                   | Description                              |
| ------------------------- | ---------------------------------------- |
| `docker container ls`     | Show running containers                  |
| `docker container ls -a`  | Show all containers (running & stopped)  |
| `docker container ls -l`  | Show the most recently created container |
| `docker container ls -q`  | Display only container IDs (running)     |
| `docker container ls -aq` | Display all container IDs                |

```bash theme={null}
docker container ls -a
```

Sample output:

```text theme={null}
CONTAINER ID   IMAGE     COMMAND              CREATED         STATUS                     NAMES
36a391532e10   httpd     "httpd-foreground"   2 minutes ago   Created                    charming_wiles
```

Docker assigns a random human-readable name if you don’t provide one.

***

## Starting a Container

Start an existing container by its ID or name:

```bash theme={null}
docker container start 36a391532e10
docker container ls
```

***

## Create & Start in One Step

Pull the image, create, and start the container:

```bash theme={null}
docker container run httpd
```

***

## Ephemeral Containers

Some images (like `ubuntu`) don’t run a persistent process:

```bash theme={null}
docker container run ubuntu
docker container ls -a
```

Output:

```text theme={null}
CONTAINER ID   IMAGE    COMMAND     CREATED         STATUS                     NAMES
d969ecdb44ea   ubuntu   "/bin/bash" 2 minutes ago   Exited (0) 2 minutes ago   intelligent_almeida
```

Once the primary process exits, the container stops.

***

## Interactive Shells

Keep STDIN open and allocate a pseudo-TTY with `-it`:

```bash theme={null}
docker container run -it ubuntu
```

Inside the container:

```text theme={null}
root@6caba272c8f5:/# hostname
6caba272c8f5
```

On the host:

```bash theme={null}
docker container ls
```

Shows:

```text theme={null}
CONTAINER ID   IMAGE    COMMAND      CREATED          STATUS              NAMES
6caba272c8f5   ubuntu   "/bin/bash"  About a minute   Up About a minute   quizzical_austin
```

<Callout icon="lightbulb">
  Always place options (`-i`, `-t`, `-d`, `--name`) **before** the image name. Anything after the image name is interpreted as the container’s command.
</Callout>

***

## Exiting Containers

Running `exit` inside an interactive shell stops the container:

```bash theme={null}
docker container run -it ubuntu
root@6caba272c8f5:/# exit
exit
docker container ls -a
```

***

## Naming Containers

Assign a custom name at creation:

```bash theme={null}
docker container run -itd --name webapp ubuntu
docker container ls -l
```

Output:

```text theme={null}
CONTAINER ID   IMAGE    COMMAND      CREATED          STATUS             NAMES
59aa5eacd88c   ubuntu   "/bin/bash"  20 seconds ago   Up 19 seconds      webapp
```

Rename an existing container:

```bash theme={null}
docker container rename intelligent_almeida webapp2
```

***

## Detached Mode

Run containers in the background with `-d`:

```bash theme={null}
docker container run -d httpd
```

Sample output:

```text theme={null}
[SECRET_REDACTED]
```

To reattach:

```bash theme={null}
docker container attach 11cbd7fe7e65
```

A unique ID prefix is sufficient if it’s unambiguous.

***

## Links and References

* [Docker CLI Reference][Docker CLI Reference]
* [Docker Container Commands][Docker Container Commands]
* [Docker Official Documentation](https://docs.docker.com/)

[Docker CLI Reference]: https://docs.docker.com/engine/reference/commandline/cli/

[Docker Container Commands]: https://docs.docker.[SECRET_REDACTED]/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/f68d9089-8ddb-476a-90ca-4dd7dd9ae6ed" />
</CardGroup>


# Copying Contents into Container

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Copying-Contents-into-Container/page

This guide explains how to transfer files and directories between a Docker host and a running container using the docker container cp command.

In this guide, you’ll learn how to transfer files and directories between your Docker host and a running container using the `docker container cp` command. This utility works in both directions:

* Host → Container
* Container → Host

Assume you have:

* A container named `webapp` running on your Docker host
* A file on the host at `/tmp/web.conf`

***

## Copying from Host to Container

### Syntax

```bash theme={null}
docker container cp [HOST_PATH] [CONTAINER_NAME]:[CONTAINER_PATH]
```

### Example

```bash theme={null}
docker container cp /tmp/web.conf webapp:/etc/web.conf
```

* **Source (host):** `/tmp/web.conf`
* **Destination (container):** `webapp:/etc/web.conf`

<Callout icon="lightbulb">
  If you specify a directory as the destination, ensure that directory already exists inside the container.
</Callout>

***

## Copying from Container to Host

Simply reverse the source and destination:

```bash theme={null}
docker container cp webapp:/etc/web.conf /tmp/web.conf
```

* **Source (container):** `webapp:/etc/web.conf`
* **Destination (host):** `/tmp/web.conf`

<Callout icon="triangle-alert">
  Any existing file at the destination path will be overwritten without confirmation.
</Callout>

***

## Copying Entire Directories

To copy a complete directory (including its contents), include trailing slashes:

```bash theme={null}
docker container cp ./config/ webapp:/etc/config
```

This command transfers your local `config` folder into `/etc/config` inside the `webapp` container. Ensure `/etc/config` exists in the container before running the command.

***

## Command Reference

| Direction        | Command Syntax                                                        | Description                              |
| ---------------- | --------------------------------------------------------------------- | ---------------------------------------- |
| Host → Container | `docker container cp /path/on/host container_name:/path/in/container` | Copy files or directories into container |
| Container → Host | `docker container cp container_name:/path/in/container /path/on/host` | Copy files or directories to host        |

***

## Links and References

* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/)
* [docker container cp Documentation](https://docs.docker.com/engine/reference/commandline/cp/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/9963b700-821b-4ca4-91d3-11ee36c2c99a" />
</CardGroup>
