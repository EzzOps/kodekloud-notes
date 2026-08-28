# Setting a Container Hostname

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Setting-a-Container-Hostname/page

This article explains how to set a hostname for a Docker container and the difference between container name and hostname.

When you start a Docker container, you often assign it a name with `--name`, but this doesn’t change the hostname inside the container. Understanding the difference between a container’s name and its hostname is crucial when your application uses hostname-based logic for logging, inter-service communication, or constructing URLs.

## Container Name vs Hostname

| Option              | Scope         | Affects                                                  |
| ------------------- | ------------- | -------------------------------------------------------- |
| `--name <name>`     | Docker Engine | User-friendly container identifier at the CLI            |
| `--hostname <name>` | Container OS  | The hostname returned by `hostname` inside the container |

<Callout icon="lightbulb">
  The container *name* and *hostname* serve different purposes. Some applications generate logs or metrics based on the hostname, so setting it appropriately simplifies debugging and monitoring.
</Callout>

## Default Hostname Behavior

By default, Docker sets the hostname to the short version of the container’s unique ID. For example:

```bash theme={null}
docker container run -it --name webapp ubuntu
```

Inside that container, checking the hostname shows the truncated ID:

```bash theme={null}
root@3484d738:/# hostname
3484d738
```

Here, `3484d738` is the container ID—not the friendly `webapp` name you provided.

## Overriding the Hostname

To assign a meaningful hostname inside your container, use the `--hostname` (or `-h`) flag. This helps when services rely on consistent hostnames:

```bash theme={null}
docker container run -it \
  --name webapp \
  --hostname webapp \
  ubuntu
```

Now, the `hostname` command returns your custom name:

```bash theme={null}
root@webapp:/# hostname
webapp
```

Your application can now reference a predictable, human-readable hostname.

## References

* [Docker Run Reference](https://docs.docker.com/engine/reference/commandline/run/)
* [Docker Container CLI](https://docs.docker.[SECRET_REDACTED]/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/96b95286-4480-4f66-a78c-fde820e1c226" />
</CardGroup>
