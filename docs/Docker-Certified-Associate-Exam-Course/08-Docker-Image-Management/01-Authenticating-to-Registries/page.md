# data_volume
```

***

## Pruning Unused Volumes

Clean up all dangling volumes in one step to free up disk space:

```bash theme={null}
docker volume prune
```

You'll see a confirmation prompt:

```bash theme={null}
WARNING! This will remove all local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Deleted Volumes:
  data_vol3
  data_vol1
  data_vol2
Total reclaimed space: 12MB
```

<Callout icon="triangle-alert">
  Pruning removes **all** unused volumes. Ensure you have backups of any critical data before proceeding.
</Callout>

***

## Verifying Mount Options

By default, volumes are mounted read-write. To inspect a container’s mount configuration:

```bash theme={null}
docker container inspect my-container
```

Look for the `Mounts` section:

```json theme={null}
"Mounts": [
  {
    "Type": "volume",
    "Name": "data_vol1",
    "Source": "/var/lib/docker/volumes/data_vol1/_data",
    "Destination": "/var/www/html/index.html",
    "Driver": "local",
    "Mode": "z",
    "RW": true,
    "Propagation": ""
  }
]
```

<Callout icon="lightbulb">
  The `"RW": true` field confirms the volume is mounted read-write inside the container.
</Callout>

***

## Mounting a Volume as Read-Only

To ensure data integrity, you can mount a volume as read-only. Use the `--mount` flag with `readonly`:

```bash theme={null}
docker container run \
  --mount type=volume,source=data_vol1,target=/var/www/html,index.html,readonly \
  httpd
```

This is useful for scenarios where containers should not modify shared data.

***

## Common Docker Volume Commands

| Command                       | Description                       | Example                             |
| ----------------------------- | --------------------------------- | ----------------------------------- |
| docker volume ls              | List all volumes                  | `docker volume ls`                  |
| docker volume inspect \[NAME] | Show detailed info about a volume | `docker volume inspect data_volume` |
| docker volume rm \[NAME]      | Remove a specific volume          | `docker volume rm data_volume`      |
| docker volume prune           | Remove all unused volumes         | `docker volume prune`               |

***

## References

* [Docker Volumes Overview](https://docs.docker.com/storage/volumes/)
* [Use Bind Mounts or Volumes](https://docs.docker.com/storage/bind-mounts-vs-volumes/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/volume/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/44e269a4-bbba-4b6a-9540-696a6f90bace/lesson/05b25198-16e2-48c7-bf27-57fcff207044" />
</CardGroup>


# Authenticating to Registries

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Authenticating-to-Registries/page

This guide explains how to authenticate to Docker registries, pull and push images, retag images, and check disk usage.

In this guide, you’ll learn how to:

* Pull images from public and private registries
* Authenticate with `docker login`
* Retag (rename) images
* Push images to private registries
* Inspect actual disk usage with Docker

***

## 1. Pulling Images from a Public Registry

Pulling from a public registry (for example, the official Ubuntu image on Docker Hub) requires no authentication:

```bash theme={null}
docker pull ubuntu
```

<Callout icon="lightbulb">
  By default, `docker pull ubuntu` retrieves the `latest` tag. To pull a specific version, append the tag (e.g., `ubuntu:20.04`).
</Callout>

***

## 2. Accessing Private Repositories

Attempting to pull an image from a private registry without logging in will result in an **access denied** error:

```bash theme={null}
docker pull gcr.io/organization/ubuntu
```

```plaintext theme={null}
Using default tag: latest
Error response from daemon: pull access denied for gcr.io/organization/ubuntu, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
```

Similarly, pushing without authentication will fail:

```bash theme={null}
docker push ubuntu
```

```plaintext theme={null}
The push refers to repository [docker.io/library/ubuntu]
128fa0b0fb81: Layer already exists
c0151ca45f27: Layer already exists
b2fd17df2071: Layer already exists
[DEPRECATION NOTICE] registry v2 schema1 support will be removed...
errors:
  denied: requested access to the resource is denied
  unauthorized: authentication required
```

<Callout icon="triangle-alert">
  You must authenticate before pulling from or pushing to private registries.\
  Make sure your credentials have the necessary permissions.
</Callout>

***

## 3. Logging In to a Registry

Use `docker login` to authenticate. By default, it targets Docker Hub (`docker.io`).

```bash theme={null}
docker login docker.io
```

Example:

```plaintext theme={null}
Username: registry-user
Password:
WARNING! Your password will be stored unencrypted in /home/vagrant/.docker/config.json.
Login Succeeded
```

For other registries such as Google Container Registry:

```bash theme={null}
docker login gcr.io
```

Once logged in, subsequent `docker pull` and `docker push` commands will use your credentials.

***

## 4. Retagging (Renaming) an Image

Docker images cannot be renamed directly. Instead, you can create a new tag—a “soft link” to the same image ID.

1. List local images:
   ```bash theme={null}
   docker image ls
   ```
2. Retag `httpd:alpine` to `httpd:customv1`:
   ```bash theme={null}
   docker image tag httpd:alpine httpd:customv1
   ```
3. Confirm the new tag:
   ```bash theme={null}
   docker image ls
   ```

Example output:

```plaintext theme={null}
REPOSITORY  TAG        IMAGE ID       CREATED       SIZE
httpd       alpine     52862a02e4e9   2 weeks ago   112MB
httpd       customv1   52862a02e4e9   2 weeks ago   112MB
httpd       latest     c2aa7e16edd8   2 weeks ago   165MB
ubuntu      latest     549b9b86cb8d   4 weeks ago   64.2MB
```

Notice `httpd:alpine` and `httpd:customv1` share the same IMAGE ID—no duplicate layers are created.

***

## 5. Pushing to a Private Registry

To push your retagged image:

```bash theme={null}
docker image tag httpd:customv1 gcr.io/organization/httpd:customv1
docker push gcr.io/organization/httpd:customv1
```

Make sure you are logged in (`docker login gcr.io`) before pushing.

***

## 6. Checking Actual Disk Usage

Use `docker system df` to inspect disk usage across images, containers, volumes, and build cache:

```bash theme={null}
docker system df
```

Example:

```plaintext theme={null}
TYPE                TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images              3         0         341.9MB   341.9MB (100%)
Containers          0
Local Volumes       0
Build Cache         0
```

Even if `docker image ls` lists four tags, `docker system df` shows only three unique images. The `SIZE` column reflects unique layers, and `RECLAIMABLE` indicates potential space savings.

***

## Command Reference Table

| Action                         | Command Example                                  |
| ------------------------------ | ------------------------------------------------ |
| Pull a public image            | `docker pull ubuntu`                             |
| Pull a private image           | `docker pull gcr.io/myorg/ubuntu`                |
| Login to Docker Hub            | `docker login docker.io`                         |
| Login to Google Container Reg. | `docker login gcr.io`                            |
| Retag an image                 | `docker image tag httpd:alpine httpd:customv1`   |
| Push to a private registry     | `docker push gcr.io/organization/httpd:customv1` |
| View disk usage                | `docker system df`                               |

***

## Links and References

* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
* [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
* [Google Container Registry Auth](https://cloud.google.com/container-registry/docs/advanced-authentication)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/b50342c2-d18a-4868-b0bc-a7d06c33d647" />
</CardGroup>
