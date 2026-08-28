# Docker Volume

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Storage/Docker-Volume/page

Learn to inspect, remove, prune, and configure Docker volumes for effective data persistence and host system cleanliness.

In this tutorial, you’ll learn how to inspect, remove, prune, and configure Docker volumes. Managing volumes effectively helps persist data across container lifecycles and keeps your host system clean.

## Table of Contents

* [Inspecting a Volume](#inspecting-a-volume)
* [Removing a Volume](#removing-a-volume)
* [Pruning Unused Volumes](#pruning-unused-volumes)
* [Verifying Mount Options](#verifying-mount-options)
* [Mounting a Volume as Read-Only](#mounting-a-volume-as-read-only)
* [References](#references)

***

## Inspecting a Volume

Use `docker volume inspect` to retrieve metadata about your volume, including driver, mount point, labels, and scope:

```bash theme={null}
docker volume inspect data_volume
```

Sample output:

```json theme={null}
[
  {
    "CreatedAt": "2020-01-20T19:52:34Z",
    "Driver": "local",
    "Labels": {},
    "Mountpoint": "/var/lib/docker/volumes/data_volume/_data",
    "Name": "data_volume",
    "Options": {},
    "Scope": "local"
  }
]
```

This command is essential for troubleshooting mount permissions and verifying where Docker stores your volume data on the host.

***

## Removing a Volume

To delete a volume that’s no longer used by any container:

```bash theme={null}
docker volume rm data_volume
```

If the volume is active, Docker returns an error:

```bash theme={null}
Error response from daemon: remove data_volume: volume is in use - [2be4d9182296…]
```

Stop or remove the container first, then run the same command again:

```bash theme={null}
docker volume rm data_volume
