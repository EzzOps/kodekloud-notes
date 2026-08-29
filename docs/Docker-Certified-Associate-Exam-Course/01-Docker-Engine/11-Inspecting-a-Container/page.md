# Launch daemon in foreground
dockerd

# Enable debug logging
dockerd --debug
```

Sample debug output:

```text theme={null}
INFO[2020-10-24T08:29:00.331Z] Starting up
DEBU[2020-10-24T08:29:00.332Z] Listener created for HTTP on unix (/var/run/docker.sock)
DEBU[2020-10-24T08:29:00.333Z] Golang's threads limit set to 6930
WARN[2020-10-24T08:29:00.364Z] Your kernel does not support cgroup runtime
```

<Callout icon="lightbulb">
  Foreground mode is ideal for capturing logs in CI pipelines or debugging startup failures.
</Callout>

***

## Default Unix Socket

By default, Docker listens on a Unix domain socket. This restricts access to local clients only:

* Socket path: `/var/run/docker.sock`
* Access: Local IPC (no remote connections)

The Docker CLI uses this socket unless `DOCKER_HOST` is overridden.

***

## Exposing the Daemon on TCP

To allow remote management, bind `dockerd` to both the Unix socket and a TCP port:

```bash theme={null}
dockerd \
  --host=unix:///var/run/docker.sock \
  --host=tcp://192.168.1.10:2375
```

On a remote client:

```bash theme={null}
export DOCKER_HOST="tcp://192.168.1.10:2375"
docker ps
```

<Callout icon="triangle-alert">
  Port 2375 is unencrypted and unauthenticated. Exposing it publicly invites unauthorized access and potential malicious use. Only enable on secured networks or for testing.
</Callout>

***

## Securing the Daemon with TLS

Encrypt and authenticate connections on port 2376 by enabling TLS:

1. Generate CA, server, and client certificates.
2. Place `server.pem` and `serverkey.pem` in a secure directory.
3. Start `dockerd` with TLS options:

```bash theme={null}
dockerd \
  --host=unix:///var/run/docker.sock \
  --host=tcp://192.168.1.10:2376 \
  --tls=true \
  --tlscert=/var/docker/server.pem \
  --tlskey=/var/docker/serverkey.pem
```

Clients must reference the CA and their own certs:

```bash theme={null}
docker --tlsverify \
  --tlscacert=ca.pem \
  --tlscert=client.pem \
  --tlskey=client-key.pem \
  -H=tcp://192.168.1.10:2376 info
```

<Callout icon="lightbulb">
  Using TLS ensures confidentiality, integrity, and authentication for remote Docker API calls.
</Callout>

***

## Persisting Configuration in daemon.json

Avoid long startup flags by defining options in `/etc/docker/daemon.json`:

```json theme={null}
{
  "debug": true,
  "hosts": [
    "unix:///var/run/docker.sock",
    "tcp://192.168.1.10:2376"
  ],
  "tls": true,
  "tlscert": "/var/docker/server.pem",
  "tlskey": "/var/docker/serverkey.pem"
}
```

Then reload Docker:

```bash theme={null}
sudo systemctl restart docker
```

***

## Flag vs Configuration File Conflicts

Mixing CLI flags and `daemon.json` entries can lead to startup errors:

```bash theme={null}
# Conflicting debug settings
dockerd --debug=false
```

Error:

```text theme={null}
unable to configure the Docker daemon with file /etc/docker/daemon.json:
the following directives are specified both as a flag and in the configuration file:
 debug: (from flag: false, from file: true)
```

**Resolution:** Keep all overrides in one place—either CLI flags or the JSON file.

***

## References

* [Docker Daemon Configuration](https://docs.docker.[AWS_SECRET_ACCESS_KEY]/)
* [Docker CLI Environment Variables](https://docs.docker.com/engine/reference/commandline/cli/#environment-variables)
* [Systemd Service Files](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)
* [Docker Security Best Practices](https://docs.docker.com/engine/security/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/989d70f4-a69f-4b52-a8b9-61adde7bcf24" />
</CardGroup>


# Inspecting a Container

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Inspecting-a-Container/page

This guide teaches how to explore and troubleshoot Docker containers using built-in inspection commands.

In this guide, you’ll learn how to explore and troubleshoot Docker containers by using built-in inspection commands. We’ll cover:

* Listing containers
* Retrieving detailed JSON metadata
* Monitoring live resource usage
* Viewing in-container processes
* Fetching and streaming logs
* Streaming Docker system events

***

## 1. List Running Containers

Before diving deeper, get a quick overview of containers on your host:

```bash theme={null}
docker container ls
```

You can extend this with flags:

| Command                        | Description                         |
| ------------------------------ | ----------------------------------- |
| `docker container ls`          | Show running containers             |
| `docker container ls -a`       | Include stopped containers          |
| `docker container ls --filter` | Filter by status, name, label, etc. |

***

## 2. Inspect Container Details

To view in-depth information—configuration, network settings, volumes—use:

```bash theme={null}
docker container inspect <container_name_or_ID>
```

This outputs a JSON array. Example:

```json theme={null}
[
  {
    "Id": "[SECRET_REDACTED]",
    "Created": "2020-01-14T13:23:01.225868339Z",
    "Path": "/bin/bash",
    "Args": [],
    "State": {
      "Status": "running",
      "Running": true,
      "Paused": false,
      "Restarting": false,
      "IPAddress": "172.17.0.5",
      "IPPrefixLen": 16,
      "MacAddress": "02:42:ac:11:00:05"
    }
  }
]
```

| JSON Field | Description                                       |
| ---------- | ------------------------------------------------- |
| `Id`       | Unique container identifier                       |
| `Created`  | Timestamp when the container was instantiated     |
| `Path`     | Entrypoint command executed in the container      |
| `Args`     | Arguments passed to the entrypoint                |
| `State`    | Current runtime status and networking information |

<Callout icon="lightbulb">
  Use `-f json` to pipe this output into `jq` or other JSON parsers for selective querying.
</Callout>

***

## 3. Monitor Resource Usage

Docker can stream real-time metrics—CPU, memory, network I/O, block I/O—across all running containers:

```bash theme={null}
docker container stats
```

Sample output:

```bash theme={null}
CONTAINER ID   NAME           CPU %     MEM USAGE / LIMIT   MEM %   NET I/O        BLOCK I/O
59aa5eacd88c   webapp         50.00%    400KiB / 989.4MiB   0.04%   656B / 0B      0B / 0B
```

<Callout icon="lightbulb">
  The `stats` command runs continuously. Press <kbd>Ctrl+C</kbd> to stop the stream.
</Callout>

***

## 4. List Processes Inside a Container

Identify which processes are consuming resources within a specific container:

```bash theme={null}
docker container top webapp
```

Example:

```bash theme={null}
UID     PID    PPID  C STIME TTY TIME     CMD
root    17001  16985 0 13:23 ?   00:00:00 stress
```

This shows the `stress` process (host PID 17001) running inside `webapp`.

***

## 5. Fetch and Stream Container Logs

To retrieve application logs:

```bash theme={null}
docker container logs <container_name_or_ID>
```

Follow logs in real time with:

```bash theme={null}
docker container logs -f <container_name_or_ID>
```

<Callout icon="triangle-alert">
  If your logs are large, consider limiting output with options like `--since` or `--tail` to avoid overwhelming your terminal.
</Callout>

***

## 6. Stream Docker Events

Docker records events for containers, networks, volumes, and more. To see recent events—for example, within the last hour—run:

```bash theme={null}
docker system events --since 60m
```

Sample output:

```bash theme={null}
2020-01-14T18:30:30Z network connect ... (container=68649c8b..., name=bridge)
2020-01-14T18:30:30Z container start ... (image=ubuntu, name=casethree)
```

All resource lifecycle events can be retrieved using `docker system events`.

***

## Summary of Inspection Commands

| Command                            | Purpose                                    |
| ---------------------------------- | ------------------------------------------ |
| `docker container ls`              | List active containers                     |
| `docker container inspect <id>`    | Show detailed JSON metadata                |
| `docker container stats`           | Stream live resource usage                 |
| `docker container top <name>`      | List processes inside the container        |
| `docker container logs <id>`       | Retrieve container logs                    |
| `docker container logs -f <id>`    | Follow logs in real time                   |
| `docker system events --since 60m` | Stream Docker engine events from last hour |

***

## Links and References

* [Docker Inspect Documentation](https://docs.docker.[AWS_SECRET_ACCESS_KEY]/)
* [Docker Stats Documentation](https://docs.docker.com/engine/reference/commandline/stats/)
* [Docker Logs Documentation](https://docs.docker.com/engine/reference/commandline/logs/)
* [Docker Events Documentation](https://docs.docker.com/engine/reference/commandline/events/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/292ab898-d1dd-4c2f-ae4f-cee3df59bf1c" />
</CardGroup>
