# Docker version 19.03.5, build 633a0ea
```

And get system-wide details:

```bash theme={null}
docker system info
```

Sample excerpt:

```bash theme={null}
Server:
 Containers: 0
 Running: 0
 Images: 0
 Server Version: 19.03.5
 Storage Driver: overlay2
```

***

## References

* [Docker Official Documentation](https://docs.docker.com/)
* [Open Container Initiative](https://opencontainers.org/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/a5f2fdd6-86ad-44d2-a4e0-e9c164f4ae3a)


# Docker Service Configuration

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Docker-Service-Configuration/page

Master the essentials of configuring the Docker daemon on Linux, covering systemd management, debugging, socket tuning, remote access, TLS security, and persistent configuration.

Master the essentials of configuring the Docker daemon (`dockerd`) on Linux. This guide covers systemd management, foreground debugging, socket tuning, remote access, TLS security, and persistent configuration.

## Table of Contents

1. [Managing Docker with systemd](#managing-docker-with-systemd)
2. [Running the Daemon in Foreground](#running-the-daemon-in-foreground)
3. [Default Unix Socket](#default-unix-socket)
4. [Exposing the Daemon on TCP](#exposing-the-daemon-on-tcp)
5. [Securing the Daemon with TLS](#securing-the-daemon-with-tls)
6. [Persisting Configuration in daemon.json](#persisting-configuration-in-daemonjson)
7. [Flag vs Configuration File Conflicts](#flag-vs-configuration-file-conflicts)
8. [References](#references)

***

## Managing Docker with systemd

Use systemd to start, stop, and inspect the Docker service. By default, Docker is enabled to launch on boot.

| Command                         | Description                  |
| ------------------------------- | ---------------------------- |
| `sudo systemctl start docker`   | Start the Docker service     |
| `sudo systemctl stop docker`    | Stop the Docker service      |
| `sudo systemctl restart docker` | Restart the service          |
| `sudo systemctl status docker`  | Show current status and logs |
| `sudo systemctl enable docker`  | Enable docker at startup     |
| `sudo systemctl disable docker` | Disable automatic startup    |

Example status output:

```text theme={null}
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2020-10-21 04:21:01 UTC; 3 days ago
     Docs: https://docs.docker.com
 Main PID: 4197 (dockerd)
    Tasks: 13
   Memory: 129.7M
      CPU: 9min 6.980s
   CGroup: /system.slice/docker.service
           └─4197 /usr/bin/dockerd -H fd:// -H tcp://0.0.0.0 --containerd=/run/containerd/containerd.sock
```

> **lightbulb** If you make changes to `/etc/docker/daemon.json`, restart Docker with `sudo systemctl restart docker` to apply them.

***

## Running the Daemon in Foreground

Troubleshoot or capture real-time logs by launching `dockerd` interactively.

```bash theme={null}
