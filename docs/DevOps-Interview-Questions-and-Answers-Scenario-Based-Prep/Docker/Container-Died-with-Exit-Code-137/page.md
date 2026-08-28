# Mount a host directory into the container
docker run -v /path/on/host:/path/in/container myimage
```

Drawbacks of bind mounts in production:

* You must ensure the same host path exists on every node in your cluster.
* Permissions and ownership on each host must be configured correctly.
* Coordination across hosts becomes operationally expensive and error-prone.

<Frame>
  <img alt="The image shows three machines with boxes and their data folder statuses: Machine 1 and Machine 2 have /data, while Machine 3 does not. It emphasizes the need for every host to have the same /data." />
</Frame>

In short: bind mounts are excellent for local development and quick iterations, but they can be fragile and difficult to manage across multiple production hosts.

## Option 2 — Named volumes (Docker-managed volumes)

Named volumes are managed by Docker. When you use a named volume Docker creates and controls the directory on the host (typically under Docker’s volumes directory, such as `/var/lib/docker/volumes`), and exposes it to containers. You reference volumes by name and Docker handles the location and permissions.

<Frame>
  <img alt="The image illustrates the &#x22;Named Volumes&#x22; option in Docker architecture, showing the relationship between Docker, the host disk, and a container." />
</Frame>

Example: create and attach a named volume for MySQL

```bash theme={null}
# Create and attach a named volume called "dbdata" to a MySQL container
docker run -v dbdata:/var/lib/mysql mysql
```

How this behaves:

* The first time you run the command Docker will create the `dbdata` volume automatically.
* On subsequent runs you can reuse `dbdata` to attach the same persistent data to a new container.
* If the container is removed, the volume remains on disk and can be re-attached to other containers.

<Frame>
  <img alt="The image illustrates how Docker manages data persistence, showing that when a container dies, the volume remains intact." />
</Frame>

Important production note:

* Named volumes are local to the Docker host where they are created. To share data across multiple hosts you need a volume driver or network-backed storage (NFS, cloud block storage like AWS EBS, Azure Disk, or a distributed filesystem such as GlusterFS or Ceph) that provides a shared backing store.

<Frame>
  <img alt="The image compares &#x22;Bind Mount&#x22; with &#x22;Named Volume&#x22; in Docker, highlighting that with Bind Mount, you manage the host path and permissions, while with Named Volume, Docker owns it and ensures consistency." />
</Frame>

## Quick comparison

| Concern                  | Bind mount                                   | Named volume                                                                               |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Typical use case         | Local development, hot-reload of source code | Persistent app data in production (databases, stateful services)                           |
| Management               | You manage the host path and permissions     | Docker manages location and permissions by volume name                                     |
| Portability across hosts | Low — needs the same host path on each node  | Better on a single host; for multi-host you need a driver or network storage               |
| Creation                 | Must exist on host (or created manually)     | Created automatically by Docker the first time used (`docker volume create` or implicitly) |
| Example                  | `docker run -v /path/on/host:/app`           | `docker run -v dbdata:/var/lib/mysql`                                                      |

## When to use which

* Use bind mounts:
  * For development workflows where editing files on the host should reflect immediately inside the container.
  * When you need to expose specific host files (e.g., SSH keys, host config files).
* Use named volumes:
  * For production data that must survive container recreation.
  * When you want Docker to manage storage location and permissions.
  * When integrating with Docker volume drivers or cloud block storage for multi-host persistence.

For more details, see the official Docker documentation: [https://docs.docker.com/storage/volumes/](https://docs.docker.com/storage/volumes/)

<Callout icon="lightbulb">
  Use bind mounts for local development when you need immediate file sync with the host. Use named volumes in production to let Docker manage the host storage path and permissions, ensuring consistent, portable data persistence.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/1d3d5877-dbf7-4105-8bc2-2c619ac62421/lesson/9c13094e-0dc1-42ad-8bc3-61a4c1923c1d" />
</CardGroup>


# Container Died with Exit Code 137

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Docker/Container-Died-with-Exit-Code-137/page

Explains why Docker containers exit with code 137, identifying SIGKILL causes like OOM killer or orchestrator timeouts and steps to diagnose and investigate

Here's a common interview-style scenario from the Docker world:

Scenario: one of your containers died, its logs are empty, and `docker ps -a` shows exit code 137.

```bash theme={null}
$ docker ps -a
CONTAINER ID        IMAGE               STATUS                      NAMES
a3f9c1de7b8a        myapp:1.2           Exited (137) 4 minutes ago   api
```

What happened?

Exit code 137 is not arbitrary — it usually means the container's main process was terminated by a signal. To decode this, remember the Linux convention for signal-based exit codes: an exit caused by a signal yields `128 + signal_number`. In this case:

* 137 = 128 + 9

<Frame>
  <img alt="The image explains a rule for Linux exit codes, stating that &#x22;Exit Code = 128 + N&#x22; and provides an example of exit code 137, which equals &#x22;128 + 9&#x22;." />
</Frame>

Signal 9 is SIGKILL, so exit code 137 indicates the container's PID 1 (its main process) was forcibly killed with SIGKILL — not a normal exit.

Who can send SIGKILL?

Common senders include:

* The kernel's OOM (Out‑Of‑Memory) killer.
* Docker itself (for example, after a `docker stop` grace period times out).
* Orchestrators like Kubernetes (kubelet follows a SIGTERM → grace period → SIGKILL pattern).
* Systemd on some hosts.
* A person running `docker kill <container-id>`.

<Frame>
  <img alt="The image explains that a container's main process was killed by SIGKILL and asks &#x22;Who sent it?&#x22; with possible sources: OOM Killer, Docker, Kubernetes, and Systemd." />
</Frame>

In production, the OOM killer is often the first suspect, especially when a container has memory limits or memory usage was climbing before the exit. Under memory pressure the kernel frees memory by killing processes, and it uses SIGKILL to do so.

<Frame>
  <img alt="The image shows a graphic illustrating memory usage reaching 100%, with a subtext explaining that as memory climbs, the kernel kills a process." />
</Frame>

How to confirm whether SIGKILL was from the OOM killer

* Inspect the container state for the `OOMKilled` flag.
* Check kernel logs (`dmesg` or `journalctl -k`) for OOM messages.

Example commands:

```bash theme={null}
