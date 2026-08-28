# Exits with 0; Docker does not restart.
```

### 2. On Failure

```bash theme={null}
docker run --name test-fail --restart=on-failure:3 ubuntu \
  expr three + 5
# Exits with 1; Docker retries up to 3 times, then stops.
```

### 3. Always

```bash theme={null}
docker run --name test-always --restart=always ubuntu \
  sleep 5
```

* After `sleep 5` finishes (exit 0), Docker restarts immediately.
* `docker stop test-always` prevents restart only until the next Docker daemon reboot.

### 4. Unless-Stopped

```bash theme={null}
docker run --name test-unless --restart=unless-stopped ubuntu \
  sleep 5
```

* Behaves like `always` on crashes or normal exit.
* Honors manual `docker stop` even if the daemon restarts later.

## Live Restore of Containers

By default, stopping the Docker daemon halts all containers. With **live restore**, containers remain running when the daemon is down.

1. Edit or create `/etc/docker/daemon.json`:
   ```json theme={null}
   {
     "live-restore": true
   }
   ```
2. Restart the Docker service:
   ```bash theme={null}
   sudo systemctl restart docker
   # or
   sudo systemctl reload docker
   ```

### Verifying Live Restore

Without live restore:

```bash theme={null}
docker run --name web httpd
sudo systemctl stop docker
# Containers stop when daemon stops.
sudo systemctl start docker
docker ps
# web is not running
```

With live restore enabled:

```bash theme={null}
docker run --name web httpd
sudo systemctl stop docker
# web stays running.
sudo systemctl start docker
docker ps
# web is still running
```

<Callout icon="triangle-alert">
  Live restore requires compatible Docker versions and proper permissions. Check the [Docker daemon.json reference][1] before enabling.
</Callout>

## Links and References

* [Docker Restart Policy Documentation][2]
* [Docker Daemon Configuration][1]
* [Docker Live Restore Deep Dive][3]

[1]: https://docs.docker.[AWS_SECRET_ACCESS_KEY]/#live-restore

[2]: https://docs.docker.com/config/containers/start-containers-automatically/

[3]: https://docs.docker.com/engine/admin/live-restore/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/8457eaae-6187-4eab-8612-c78fec3abdf9" />
</CardGroup>


# Section Introduction

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Section-Introduction/page

This article provides a comprehensive understanding of Docker Engine, covering architecture, installation, container management, storage, and networking.

Welcome to our in-depth exploration of Docker Engine. In this lesson, you’ll gain a comprehensive understanding of:

* Docker Engine architecture
* Installation steps and daemon configuration
* Container and image lifecycle management
* Storage backends and volume handling
* Networking models and security best practices

<Callout icon="lightbulb">
  You should be comfortable with basic Docker concepts covered in the [Beginner’s Docker Course](https://example.com/beginners-course) before proceeding.
</Callout>

## Key Learning Outcomes

| Topic                               | Description                                                            |
| ----------------------------------- | ---------------------------------------------------------------------- |
| Docker Engine Architecture          | How the client, daemon, and registry interact                          |
| Installation & Daemon Configuration | Installing Docker Engine on Linux, Windows, macOS, and tuning          |
| Container & Image Management        | Building, tagging, and pushing images; running and managing containers |
| Storage & Volume Strategies         | Local volumes, bind mounts, and advanced storage drivers               |
| Networking & Security               | Bridge, overlay, MACVLAN networks, and securing containers             |

## Advanced Concepts

Once you’ve mastered the fundamentals, we’ll dive deeper into:

* Restart policies and container troubleshooting
* Customizing the Docker Daemon (`daemon.json`) and choosing logging drivers
* Crafting optimized, minimal images using build context, cache layers, and Multi-Stage Builds
* Designing robust networking topologies and scalable storage solutions

Let’s get started on building a rock-solid Docker Engine foundation!

## Links and References

* [Docker Engine Documentation](https://docs.docker.com/engine/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
* [Understanding Docker Storage Drivers](https://docs.docker.com/storage/storagedriver/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/45bbbbd4-1412-4eb9-94c6-138f327c742f" />
</CardGroup>
