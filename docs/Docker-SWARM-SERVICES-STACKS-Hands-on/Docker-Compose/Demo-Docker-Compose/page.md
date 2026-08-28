# Inside the container:
touch temp.txt
```

<Frame>
  ![A person is explaining container layers, with a diagram showing "Read Write" and "Read Only" sections, and a file named "temp.txt" in the writable area.](https://kodekloud.com/kk-media/image/upload/v1752874058/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Storage-and-Filesystems/frame_350.jpg)
</Frame>

Even though image layers are immutable, Docker uses a "copy-on-write" mechanism to enable modifications. In this process, if you attempt to change a file within an image layer (such as editing `app.py`), Docker first copies the file to the writable layer and then applies your modifications. This method ensures that the original image remains unchanged while allowing each container to keep its own changes.

<Frame>
  ![The image explains the "Copy-On-Write" concept, showing container and image layers with read-write and read-only files, alongside a person presenting.](https://kodekloud.com/kk-media/image/upload/v1752874059/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Storage-and-Filesystems/frame_410.jpg)
</Frame>

<Callout icon="lightbulb">
  When a container is removed, its writable layer, along with all modifications, is deleted. To preserve critical data, such as database files, mount an external volume.
</Callout>

## Persisting Data with Volumes and Bind Mounts

Persisting data is crucial for stateful applications. To create a volume:

```bash theme={null}
docker volume create data_volume
```

This command creates a volume directory under `/var/lib/docker/volumes`. Then, run a container with the volume mounted to a specific directory:

```bash theme={null}
docker run -v data_volume:/var/lib/mysql mysql
```

In this example, MySQL writes data to `data_volume`, ensuring data persistence even if the container is removed. Docker will also automatically create the volume if it does not exist, and you can verify this by listing the contents of `/var/lib/docker/volumes`.

Alternatively, if you prefer using an existing directory on the Docker host (for example, `/data/mysql`), use a bind mount:

```bash theme={null}
docker run -v /data/mysql:/var/lib/mysql mysql
```

This maps the host directory directly to the container.

<Callout icon="lightbulb">
  Although the `-v` flag is widely used for mounting volumes, the newer `--mount` option is preferred for its explicit syntax. For example:

  ```bash theme={null}
  docker run --mount type=bind,source=/data/mysql,target=/var/lib/mysql mysql
  ```
</Callout>

## Docker Storage Drivers

The layered architecture, writable container layers, and copy-on-write features are all made possible by Docker storage drivers. Popular storage drivers include:

| Storage Driver   | Description                           | Common Use Case            |
| ---------------- | ------------------------------------- | -------------------------- |
| AUFS             | Advanced multi-layer union filesystem | Default on Ubuntu          |
| BTRFS            | Modern Copy-on-Write filesystem       | Advanced usage scenarios   |
| VFS              | Simple filesystem used for debugging  | Limited to specific cases  |
| Device Mapper    | Uses Linux's device-mapper            | Fedora/CentOS defaults     |
| Overlay/Overlay2 | Efficient copy-on-write drivers       | Modern Linux distributions |

The choice of storage driver depends on your host operating system and performance requirements. For instance, Ubuntu generally uses AUFS by default, whereas Fedora or CentOS might lean towards Device Mapper. Docker automatically selects the most optimized driver for your system, although you can configure a specific driver if needed.

<Frame>
  ![A person stands beside a list of storage drivers on a blue background, including AUFS, ZFS, BTRFS, Device Mapper, Overlay, and Overlay2.](https://kodekloud.com/kk-media/image/upload/v1752874060/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Storage-and-Filesystems/frame_690.jpg)
</Frame>

This concludes our exploration of Docker's storage and file system architecture. For further reading on these storage drivers and additional Docker concepts, please refer to the official [Docker Documentation](https://docs.docker.com/).

See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/01c6c0f6-50bd-495b-a164-52a82eeebd79/lesson/e1b5f1f7-5798-48ee-b5cd-19c121966055" />
</CardGroup>


# Demo Docker Compose

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Docker-Compose/Demo-Docker-Compose/page

This article explains how to upgrade a Docker Compose file from version 1 to version 3 for enhanced features.

In this article, we explore how to enhance and upgrade a Docker Compose file. We start with a basic Compose file (version 1) and then upgrade it to version 3 to leverage advanced features like automatic network creation and improved DNS resolution.

## Original Compose File (Version 1)

Below is the initial Docker Compose file (version 1):

```yaml theme={null}
redis:
  image: redis

db:
  image: postgres:9.4

vote:
  image: voting-app
  ports:
    - 5000:80
  links:
    - redis

worker:
  image: worker-app
  links:
    - db
    - redis

result:
  image: result-app
  ports:
    - 5011:80
  links:
    - db
```

While this version is simple, it lacks support for many of Docker Compose's advanced features. In this tutorial, we will upgrade the file to version 3 by adding a version declaration at the top and moving all configurations under a new "services" section.

## Upgrading to Docker Compose Version 3

To update the file, start by referencing the [Docker Compose file documentation](https://docs.docker.com/compose/compose-file/). The documentation provides a comprehensive compatibility matrix that details the relationships between Compose file versions and Docker Engine requirements.

### Minimal Update to Version 3

Here is the updated file with only minimal modifications:

```yaml theme={null}
redis:
  image: redis

db:
  image: postgres:9.4

vote:
  image: voting-app
  ports:
    - 5000:80

worker:
  image: worker-app

result:
  image: result-app
  ports:
    - 5011:80
```

Notice that the manual "links" sections have been removed. With version 3, Docker Compose automatically creates a network and provides DNS resolution between containers, eliminating the need for explicit linking.

### Creating a "services" Section with the Version Declaration

The next step is to add the version declaration and create a "services" block. For example, you can update the file in an editor like VS Code by indenting all configuration lines under a new block. The revised file looks like this:

```yaml theme={null}
version: "3"
services:
  redis:
    image: redis

  db:
    image: postgres:9.4

  vote:
    image: voting-app
    ports:
      - "5000:80"

  worker:
    image: worker-app

  result:
    image: result-app
    ports:
      - "5001:80"
```

<Callout icon="lightbulb">
  When you deploy this updated configuration with the `docker-compose up` command, Docker automatically creates a network for the containers. All containers join the same network allowing services to refer to each other by name.
</Callout>

### Deploying the Updated File

Deploy the application using the following command:

```bash theme={null}
admin@docker-host $ docker-compose up
```

You might see output similar to the following:

```bash theme={null}
WARNING: The Docker Engine you're using is running in swarm mode.
...
Creating network "code_default" with the default driver
Creating code_worker_1 ... done
Creating code_redis_1 ... done
Creating code_result_1 ... done
Creating code_db_1 ... done
Creating code_vote_1 ... done
```

In this example, "code" (derived from the directory name) prefixes the network and service names.

## Handling PostgreSQL Environment Variables

When running the updated file, you may encounter an error where the worker or result apps cannot connect to the database. This issue is due to recent changes in the PostgreSQL image which now require the `POSTGRES_PASSWORD` environment variable to be set. Without it, the database fails to initialize properly.

<Callout icon="triangle-alert">
  Ensure that you update the database service with the required environment variables. Without `POSTGRES_PASSWORD`, dependent services may fail to establish a connection.
</Callout>

To resolve this, update the DB service configuration as follows:

```yaml theme={null}
version: '3'
services:
  redis:
    image: redis

  db:
    image: postgres:9.4
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  vote:
    image: voting-app
    ports:
      - "5000:80"

  worker:
    image: worker-app

  result:
    image: result-app
    ports:
      - "5001:80"
```

After saving the changes, bring the services up once more:

```bash theme={null}
admin@docker-host $ docker-compose up
```

You'll see a similar output indicating the services and network are created successfully:

```bash theme={null}
WARNING: The Docker Engine you're using is running in swarm mode.
Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.
To deploy your application across the swarm, use `docker stack deploy`.
Creating network "code_default" with the default driver
Creating code_worker_1 ... done
Creating code_redis_1 ... done
Creating code_result_1 ... done
Creating code_db_1 ... done
Creating code_vote_1 ... done
```

## Verifying the Deployment

Once the deployment is successful, you can access the voting application via localhost on port 5000 and the results application on port 5001. For example, cast a vote for "cats" and verify that the results page shows 100% for cats. Changing the vote to "dogs" should update the results accordingly, confirming that your containerized setup is functioning as intended.

## Conclusion

This article has demonstrated how to upgrade a Docker Compose file from version 1 to version 3, enabling modern features like automatic networking and enhanced DNS resolution. Happy containerizing, and see you in the next article!

<Frame>
  ![The image shows a section of the Docker documentation website, displaying a compatibility matrix for Docker Compose versions and their corresponding Docker versions.](https://kodekloud.com/kk-media/image/upload/v1752874062/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Docker-Compose/frame_30.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/43e8db99-9bc6-4277-88b0-a6f699d2fd76/lesson/6e4c3b2b-bf94-4acb-8eda-cfcb22fff9d0" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/43e8db99-9bc6-4277-88b0-a6f699d2fd76/lesson/99ceddba-ce66-428e-81a2-193fbd7a7e73" />
</CardGroup>
