# Press Ctrl+P, Ctrl+Q
docker container ls
```

<Callout icon="lightbulb">
  Detaching this way leaves the container running in the background.
</Callout>

## 4. Executing Commands in Running Containers

Run additional commands inside an active container using `exec`:

```bash theme={null}
docker container exec -it 9fe83b47dc1f /bin/bash
root@9fe83b47dc1f:/# ps -ef
```

You can even use partial container IDs:

```bash theme={null}
docker container exec -it 65 cat /etc/lsb-release
```

## 5. Attaching to a Container

Use `attach` to connect to the primary process of a running container:

```bash theme={null}
docker container attach <container_id>
# then:
exit  # This will stop the container
```

<Callout icon="triangle-alert">
  Exiting an attached session (`exit`) will terminate the container’s main process.
</Callout>

## 6. Stopping and Removing Containers

* **Stop** a running container:

  ```bash theme={null}
  docker container stop 14fc5c1661f9
  ```

* **Remove** a stopped container:

  ```bash theme={null}
  docker container rm 14fc5c1661f9
  ```

* **Prune** all stopped containers:

  ```bash theme={null}
  docker container prune
  ```

<Callout icon="triangle-alert">
  `docker container prune` removes *all* stopped containers. Use with caution.
</Callout>

Or combine stop and remove for *all* containers:

```bash theme={null}
docker container stop $(docker container ls -q)
docker container rm $(docker container ls -aq)
```

## 7. Detached Mode and Naming

Run in detached mode (`-d`) and assign a custom name:

```bash theme={null}
docker container run -itd --name=kodekloud ubuntu
```

Rename an existing container:

```bash theme={null}
docker container rename kodekloud yogish-codecloud
```

## 8. Inspecting Container Details

Retrieve full metadata with `inspect`:

```bash theme={null}
docker container inspect yogish-codecloud
```

Sample output:

```json theme={null}
[
  {
    "Id": "5c2b2b5fc32f...",
    "Created": "2020-05-04T07:04:13.230760175Z",
    "Path": "/bin/bash",
    "Args": [],
    "State": {
      "Status": "running",
      "Running": true,
      "Paused": false,
      "Restarting": false,
      "OOMKilled": false,
      "Dead": false,
      "Pid": 14776,
      "ExitCode": 0,
      "StartedAt": "2020-05-04T07:04:13.598111123Z",
      "FinishedAt": "0001-01-01T00:00:00Z"
    },
    "Image": "sha256:1d622ef86b1...",
    "Name": "/yogish-codecloud",
    "Driver": "overlay2"
  }
]
```

## 9. Monitoring Containers

### 9.1 Resource Usage

Display real-time stats:

```bash theme={null}
docker container stats
```

### 9.2 Process List

Show host PIDs inside a container:

```bash theme={null}
docker container top reverent_hopper
```

### 9.3 Logs

View past logs:

```bash theme={null}
docker container logs d52fad69ea76
```

Follow logs live:

```bash theme={null}
docker container logs -f d52fad69ea76
```

## Conclusion

You’ve now mastered:

* Creating, starting, and listing containers
* Interactive sessions with `run`, `exec`, and `attach`
* Naming, renaming, and inspecting container details
* Monitoring resource usage and logs
* Cleaning up with `stop`, `rm`, and `prune`

For more commands, see the [Docker CLI reference](https://docs.docker.com/engine/reference/commandline/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/4156c342-a7b3-4703-bc36-f1241c8782f8" />
</CardGroup>


# Demo Docker Debug Mode

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Demo-Docker-Debug-Mode/page

Learn to enable Docker debug mode, verify its status, and inspect detailed logs during container operations.

In this demo, you’ll learn how to turn on Docker daemon debug mode, verify that it’s active, and inspect verbose logs during container operations.

## 1. Check Current Debug Status

Start by viewing your Docker daemon’s current settings:

```bash theme={null}
docker system info
```

Look for the `Debug Mode` line in the output:

```text theme={null}
Debug Mode: false
```

## 2. Create a Test Container & Inspect Default Logs

Launch a simple HTTPD container:

```bash theme={null}
docker run -d --name test httpd:latest
```

Then review your system log (e.g., `/var/log/messages` or `journalctl -u docker.service`). You should only see high-level entries about container creation:

```bash theme={null}
tail -n 20 /var/log/messages
```

## 3. Enable Docker Debug Mode

To capture detailed debug output, edit the Docker daemon configuration:

1. Open `/etc/docker/daemon.json` (create it if missing) and add:

   ```json theme={null}
   {
     "debug": true
   }
   ```

<Callout icon="lightbulb">
  If the file doesn’t exist, you can create it. Make sure the JSON remains valid—use a JSON linter if needed.
</Callout>

2. Reload the Docker daemon:

```bash theme={null}
sudo systemctl reload docker
```

## 4. Confirm Debug Mode Is Active

Run the inspect command again:

```bash theme={null}
docker system info
```

Now you should see `Debug Mode: true` along with extra metrics:

```text theme={null}
Debug Mode: true
File Descriptors: 23
Goroutines: 36
System Time: 2020-05-21T11:38:33.79317432Z
EventsListeners: 0
```

## 5. Generate and View Verbose Logs

Create a new container called `test_debug`:

```bash theme={null}
docker run -d --name test_debug httpd:latest
```

Then tail your logs to see debug-level details:

```bash theme={null}
tail -n 20 /var/log/messages
```

You’ll notice granular messages describing each step of the container lifecycle.

## 6. Reload Docker with SIGHUP & Disable Debug

If you prefer a manual reload instead of `systemctl`:

1. Update `/etc/docker/daemon.json` to disable debug mode:

   ```json theme={null}
   {
     "debug": false
   }
   ```

2. Identify the Docker daemon PID and send `SIGHUP`:

   ```bash theme={null}
   pid=$(pgrep dockerd)
   sudo kill -SIGHUP $pid
   ```

<Callout icon="triangle-alert">
  Always verify you have the correct PID before sending signals. Killing the wrong process can disrupt your system.
</Callout>

3. Check that debug is now off:

```bash theme={null}
docker system info | grep "Debug Mode"
```

***

## Command Reference

| Action                       | Command                                              |                     |
| ---------------------------- | ---------------------------------------------------- | ------------------- |
| Check debug status           | `docker system info`                                 |                     |
| Launch a container           | `docker run -d --name <name> httpd:latest`           |                     |
| View system logs             | `tail -n 20 /var/log/messages`                       |                     |
| Enable debug in daemon.json  | Add `"debug": true` to `/etc/docker/daemon.json`     |                     |
| Reload Docker via systemd    | `sudo systemctl reload docker`                       |                     |
| Reload Docker via SIGHUP     | `sudo kill -SIGHUP $(pgrep dockerd)`                 |                     |
| Disable debug in daemon.json | Change `"debug": false` in `/etc/docker/daemon.json` |                     |
| Verify debug flag only       | \`docker system info                                 | grep "Debug Mode"\` |

***

## Links and References

* [Docker Daemon Configuration](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)
* [Understanding the Docker Logging Driver](https://docs.docker.com/config/containers/logging/configure/)
* [Docker System Commands](https://docs.docker.com/engine/reference/commandline/system/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/dcebf7a4-f936-41e8-8c5e-930f34cb5b53" />
</CardGroup>
