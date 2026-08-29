# Demo Docker Volume

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Storage/Demo-Docker-Volume/page

This tutorial covers creating, inspecting, mounting, and removing Docker volumes for persistent container data management.

In this tutorial, you’ll learn how to create, inspect, mount, and remove Docker volumes. Volumes are the preferred mechanism for persisting container data, ensuring it lives beyond the lifecycle of individual containers.

## 1. List and Create a Volume

Before you begin, list existing volumes (you should see none):

```bash theme={null}
$ docker volume ls
DRIVER    VOLUME NAME
```

Create a new volume called `testvol`:

```bash theme={null}
$ docker volume create testvol
testvol

$ docker volume ls
DRIVER    VOLUME NAME
local     testvol
```

## 2. Mounting a Volume with `-v`

You can mount `testvol` into a container at `/yogesh` using the shorthand `-v` flag:

```bash theme={null}
$ docker run -itd --name test -v testvol:/yogesh centos:7
```

> **lightbulb** The `-v` shorthand syntax is concise but less explicit than `--mount`. For new scripts, consider using `--mount` (see Section 5).

Verify the mount inside the container:

```bash theme={null}
$ docker exec -it test df -h | grep /yogesh
/dev/mapper/centos-root  50G  1.2G   49G   3% /yogesh
```

## 3. Inspect Volume Details

On the host, inspect `testvol` to discover its data directory:

```bash theme={null}
$ docker volume inspect testvol
[
  {
    "CreatedAt": "2020-05-04T17:34:47Z",
    "Driver": "local",
    "Mountpoint": "/var/lib/docker/volumes/testvol/_data",
    "Name": "testvol",
    "Scope": "local"
  }
]
```

Create sample files inside the volume:

```bash theme={null}
$ docker exec test bash -c "touch /yogesh/abc /yogesh/def"
```

## 4. Removing Containers vs. Volumes

Stopping or removing the container does *not* delete the attached volume:

```bash theme={null}
$ docker stop test
$ docker rm test

$ docker volume ls
DRIVER    VOLUME NAME
local     testvol
```

To remove the volume and reclaim space:

```bash theme={null}
$ docker volume rm testvol
testvol
```

> **triangle-alert** Removing a volume deletes all data stored in it. Make sure you no longer need its contents before running `docker volume rm`.

## 5. Mounting a Volume with `--mount`

For clearer syntax and advanced options, use `--mount`:

```bash theme={null}
$ docker volume create testvol
testvol

$ docker run -itd --name test \
    --mount source=testvol,destination=/yogesh \
    centos:7
```

Check that your files persist:

```bash theme={null}
$ docker exec -it test ls /yogesh
abc  def
```

### Comparing `-v` vs `--mount`

| Option    | Syntax                                                               | When to Use          |
| --------- | -------------------------------------------------------------------- | -------------------- |
| `-v`      | `-v volume_name:/container_path`                                     | Quick tests          |
| `--mount` | `--mount type=volume,source=volume_name,destination=/container_path` | Production & scripts |

## 6. Handling Volume-in-Use Errors

If you try to remove a volume that’s still attached, you’ll see an error:

```bash theme={null}
$ docker volume rm testvol
Error response from daemon: remove testvol: volume is in use - [container_id]
```

Stop and remove the container, then retry:

```bash theme={null}
$ docker stop test
$ docker rm test
$ docker volume rm testvol
testvol
```

You can also remove **all** unused volumes in one command:

```bash theme={null}
$ docker volume prune
WARNING! This will remove all local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Total reclaimed space: 0B
```

## 7. Read-Write vs Read-Only Mounts

By default, mounts are read-write (`rw`). Here’s how to confirm:

```bash theme={null}
$ docker volume create data_vol1
data_vol1

$ docker run -itd --name volume_rw \
    --mount source=data_vol1,destination=/yogesh \
    centos:7

$ docker inspect volume_rw --format '{{json .Mounts}}'
[{"Destination":"/yogesh","Mode":"rw", ...}]
```

To mount that same volume as read-only (`ro`):

```bash theme={null}
$ docker run -itd --name volume_ro \
    --mount source=data_vol1,destination=/yogesh,readonly=true \
    centos:7

$ docker inspect volume_ro --format '{{json .Mounts}}'
[{"Destination":"/yogesh","Mode":"ro", ...}]
```

Clean up:

```bash theme={null}
$ docker stop volume_rw volume_ro
$ docker rm volume_rw volume_ro
$ docker volume prune -f
```

## 8. Bind Mounts

Bind mounts let you map any host directory directly into a container:

```bash theme={null}
$ mkdir /data

$ docker run -itd --name bindtest \
    --mount type=bind,source=/data,destination=/yogesh \
    centos:7
```

Inside `bindtest`, the path `/yogesh` is backed by `/data` on the host. Note that bind mounts do not show up in `docker volume ls`.

> **lightbulb** Use bind mounts when you need to share host files or configuration with a container. For managed, portable storage, prefer Docker volumes.

***

## Links and References

* [Docker Volumes](https://docs.docker.com/storage/volumes/)
* [Bind Mounts](https://docs.docker.com/storage/bind-mounts/)
* [Docker Run Reference](https://docs.docker.com/engine/reference/commandline/run/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/44e269a4-bbba-4b6a-9540-696a6f90bace/lesson/6df0a523-7670-4591-b86a-2f78ed1ccb4f)
