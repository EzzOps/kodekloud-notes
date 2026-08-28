# Pause Apache httpd
kill -SIGSTOP 11663

# Resume it
kill -SIGCONT $(pgrep httpd)

# Graceful shutdown
kill -SIGTERM $(pgrep httpd)

# Forceful kill
kill -SIGKILL $(pgrep httpd)
# shorthand
kill -9 $(pgrep httpd)
```

<Callout icon="lightbulb">
  `SIGTERM` is the preferred way to stop a process because it allows cleanup. `SIGKILL` should be used only if the process does not terminate gracefully.
</Callout>

***

## 2. Docker Container Equivalents

Docker uses similar primitives at the container level. The table below shows the mappings:

| Action | Linux Signal      | Docker Command                    |
| ------ | ----------------- | --------------------------------- |
| Pause  | SIGSTOP/SIGCONT   | `docker pause` / `docker unpause` |
| Stop   | SIGTERM → SIGKILL | `docker stop`                     |
| Kill   | SIGKILL           | `docker kill --signal=SIGKILL`    |
| Remove | —                 | `docker rm`                       |

### 2.1 Running an HTTPD Container

```bash theme={null}
docker run --name web httpd
```

### 2.2 Pause and Resume

```bash theme={null}
docker pause web
docker unpause web
```

### 2.3 Stop (SIGTERM then SIGKILL)

```bash theme={null}
docker stop web
```

Docker sends `SIGTERM`, waits the default 10 seconds, then sends `SIGKILL` if the container is still running.

***

## 3. Sending Custom Signals

You can target any signal to a container’s main process:

```bash theme={null}
# Send SIGKILL by name
docker kill --signal=SIGKILL web

# Or by number
docker kill --signal=9 web
```

***

## 4. Removing a Container

Containers must be stopped before removal:

```bash theme={null}
docker stop web
docker rm web
```

Attempting to remove a running container yields an error:

```bash theme={null}
$ docker rm web
Error response from daemon:
You cannot remove a running container ... Stop the container before attempting removal or use --force
```

***

## 5. Batch Stopping and Removing

When managing multiple containers, leverage `docker ps -q` and `docker ps -aq`:

```bash theme={null}
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers (running & exited)
docker rm $(docker ps -aq)
```

***

## 6. Pruning Stopped Containers

To delete **all stopped** containers and free disk space:

```bash theme={null}
docker container prune
```

<Callout icon="triangle-alert">
  `docker container prune` permanently deletes **all** stopped containers. There is no undoing this action.
</Callout>

***

## 7. Automatic Cleanup with --rm

For ephemeral containers, use `--rm` to remove them automatically after exit:

```bash theme={null}
docker run --rm ubuntu expr 4 + 5
# Output: 9
```

This is ideal for one-off tasks, CI jobs, or simple shell commands.

***

## Links and References

* [Docker CLI Commands](https://docs.docker.com/engine/reference/commandline/cli/)
* [Docker Pause Documentation](https://docs.docker.com/engine/reference/commandline/pause/)
* [Linux Signals](https://man7.org/linux/man-pages/man7/signal.7.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/66fe45cb-0d58-4f47-a003-4bf944fc38db" />
</CardGroup>


# Troubleshooting Docker Daemon

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Troubleshooting-Docker-Daemon/page

This article provides steps to diagnose and resolve issues when Docker commands fail to communicate with the Docker daemon.

When Docker commands fail to communicate with the Docker daemon, follow these steps to diagnose and resolve the issue.

## 1. “Cannot connect to the Docker daemon” Error

If you encounter:

```bash theme={null}
$ docker ps
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

the Docker Engine service (daemon) isn’t reachable. Determine if you’re targeting a local socket or a remote host.

### a. Remote Access via `DOCKER_HOST`

Set the `DOCKER_HOST` environment variable to point at your remote Docker endpoint:

```bash theme={null}
export DOCKER_HOST="tcp://192.168.1.10:2376"
docker ps
```

| Port | Encryption | Description         |
| ---- | ---------- | ------------------- |
| 2375 | None       | Unencrypted traffic |
| 2376 | TLS        | Secure, encrypted   |

<Callout icon="lightbulb">
  When using port 2376, ensure you have valid certificates configured on both client and server.
</Callout>

If the error persists, SSH into the remote host and check the Docker service status.

## 2. Checking the Docker Service Status

On most Linux distributions with `systemd`, Docker runs as a service. Verify its state:

```bash theme={null}
sudo systemctl status docker
```

A healthy daemon appears as:

```plaintext theme={null}
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; preset: enabled)
   Active: active (running) since Wed 2020-10-21 04:21:01 UTC; 3 days ago
     Docs: https://docs.docker.com
 Main PID: 4197 (dockerd)
    Tasks: 13
   Memory: 130M
     CPU: 9min 6.980s
 CGroup: /system.slice/docker.service
         └─4197 /usr/bin/dockerd -H fd:// -H tcp://0.0.0.0 --containerd=/run/containerd/containerd.sock
```

If you see **inactive** or **dead**:

```plaintext theme={null}
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; preset: enabled)
   Active: inactive (dead) since Sat 2020-10-24 07:42:08 UTC; 21s ago
     Docs: https://docs.docker.com
  Process: 4197 ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0 --containerd=/run/containerd/containerd.sock (code=exited, status=0/SUCCESS)
```

Start or restart the service:

```bash theme={null}
sudo systemctl start docker
```

## 3. Inspecting Service Logs

Use `journalctl` to pinpoint errors and warnings:

```bash theme={null}
sudo journalctl -u docker.service --since "1 hour ago"
```

Example log excerpt:

```plaintext theme={null}
Oct 21 04:05:42 ubuntu-xenial systemd[1]: Starting Docker Application Container Engine...
Oct 21 04:05:42 time="2020-10-21T04:05:42.565Z" level=info msg="parsed scheme: \"unix\""
Oct 21 04:05:42 time="2020-10-21T04:05:42.847Z" level=warning msg="Your kernel does not support cgroup cfs"
Oct 21 04:05:43 time="2020-10-21T04:05:43.873Z" level=error msg="Error (Unable to complete operation)"
```

<Callout icon="lightbulb">
  Adjust the `--since` flag to narrow down log entries for faster troubleshooting.
</Callout>

## 4. Verifying Daemon Configuration

Inspect `/etc/docker/daemon.json` for JSON syntax errors or conflicting settings:

```json theme={null}
{
  "debug": true,
  "hosts": ["tcp://192.168.1.10:2376"],
  "tls": true,
  "tlscert": "/var/docker/server.pem",
  "tlskey": "/var/docker/serverkey.pem"
}
```

<Callout icon="triangle-alert">
  A conflict between daemon flags (in `daemon.json`) and CLI or systemd overrides can prevent Docker from starting. Remove duplicate host or TLS settings.
</Callout>

After any change, reload and restart:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 5. Ensuring Sufficient Disk Space

Docker stores images, containers, and volumes under `/var/lib/docker`. A full filesystem can crash the daemon.

1. Check disk usage:

   ```bash theme={null}
   df -h
   ```

   Example:

   ```plaintext theme={null}
   Filesystem     Size  Used Avail Use% Mounted on
   /dev/sda1       19G   14.7G   15M  99% /
   tmpfs          369M     0  369M   0% /dev/shm
   ```

2. Clean up unused resources:

   ```bash theme={null}
   docker container prune   # remove all stopped containers
   docker image prune       # remove dangling images
   ```

| Command                  | Description                      |
| ------------------------ | -------------------------------- |
| `docker container prune` | Delete stopped containers        |
| `docker image prune`     | Remove dangling or unused images |
| `docker volume prune`    | Clean up unused volumes          |

<Callout icon="triangle-alert">
  Pruning operations are irreversible. Use `docker system df` to preview reclaimable space.
</Callout>

## 6. Examining System Information and Events

Once the daemon is running, validate your environment:

```bash theme={null}
docker system info
```

Sample output:

```plaintext theme={null}
Client:
 Debug Mode: false

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 19.03.5
 Storage Driver: overlay2
 Backing Filesystem: xfs
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
```

To view real-time Docker events (container lifecycle, network changes, etc.):

```bash theme={null}
docker system events
```

## Further Reading

* [Docker Engine overview](https://docs.docker.com/engine/)
* [Docker daemon.json reference](https://docs.docker.[AWS_SECRET_ACCESS_KEY]/#daemon-configuration-file)
* [Docker CLI commands](https://docs.docker.com/engine/reference/commandline/cli/)
* [Managing Docker storage](https://docs.docker.com/config/pruning/)

With these steps—verifying connection methods, service status, logs, configuration, disk space, and system information—you can reliably troubleshoot Docker daemon issues.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/0052c859-4035-409c-aff8-f1e4d35d59f9" />
</CardGroup>
