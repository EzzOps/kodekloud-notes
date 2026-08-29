# Demo Docker Container Operations

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Demo-Docker-Container-Operations/page

This tutorial covers essential Docker container lifecycle commands using the Docker CLI for creating, starting, listing, interacting with, monitoring, and cleaning up containers.

In this tutorial, we’ll cover essential Docker container lifecycle commands using the Docker CLI. You’ll learn how to create, start, list, interact with, monitor, and clean up containers.

## 1. Creating and Starting a Container

1. **Create a container** from the official `httpd` image.\
   If the image isn’t available locally, Docker pulls it from Docker Hub.

   ```bash theme={null}
   docker container create httpd
   ```

2. **List containers** (none are running yet):

   ```bash theme={null}
   docker container ls
   ```

3. **Include stopped containers** with `-a`:

   ```bash theme={null}
   docker container ls -a
   ```

4. **Start the container** by its CONTAINER ID:

   ```bash theme={null}
   docker container start d52fad69ea76
   ```

5. **Verify it’s running**:

   ```bash theme={null}
   docker container ls
   ```

### Table: `docker container ls` Field Descriptions

| Field        | Description                     |
| ------------ | ------------------------------- |
| CONTAINER ID | Short 12-character container ID |
| IMAGE        | Name of the image               |
| COMMAND      | Entrypoint command              |
| CREATED      | Timestamp when created          |
| STATUS       | Current state and uptime        |
| PORTS        | Exposed ports                   |
| NAMES        | Auto-generated container name   |

## 2. Listing Options

Use different flags with `docker container ls` to customize output:

| Flag | Description                                        |
| ---- | -------------------------------------------------- |
| -a   | Show all containers (running and stopped)          |
| -l   | Show the latest created container                  |
| -q   | Only display numeric IDs of running containers     |
| -aq  | Display numeric IDs of all containers (all states) |

Example—list only IDs of running containers:

```bash theme={null}
docker container ls -q
```

## 3. Running Containers Interactively

Combine create and start with `run`:

```bash theme={null}
docker container run -it ubuntu
```

If `ubuntu:latest` isn’t local, you’ll see the pull progress, then a shell prompt:

```bash theme={null}
root@0afdaf794887:/# ps -ef
UID        PID PPID  C STIME TTY          TIME CMD
root         1     0  0 06:47 pts/0    00:00:00 /bin/bash
root         9     1  0 06:48 pts/0    00:00:00 ps -ef
root@0afdaf794887:/# exit
```

Exiting the shell stops the container:

```bash theme={null}
docker container ls -l
```

### Detaching Without Stopping

To leave a container running and return to the host shell, press `Ctrl+P` then `Ctrl+Q`:

```bash theme={null}
docker container run -it ubuntu
