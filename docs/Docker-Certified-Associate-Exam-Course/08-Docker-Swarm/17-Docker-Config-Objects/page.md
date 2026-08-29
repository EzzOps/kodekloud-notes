# This node joined a swarm as a worker.
```

Back on **managerone**, verify:

```bash theme={null}
docker node ls
# ID       HOSTNAME    STATUS  AVAILABILITY  MANAGER STATUS  ENGINE VERSION
# ...      managerone  Ready   Active        Leader          19.03.8
# ...      workerone   Ready   Active                        19.03.8
```

## 3. Add the Second Worker (`workertwo`)

### 3.1. Prepare `workertwo`

Ensure OS, CPU, memory, Docker version, and connectivity:

```bash theme={null}
cat /etc/centos-release
nproc
free -m
docker --version
systemctl status docker
ping -c3 managerone
ping -c3 workerone
```

### 3.2. Retrieve and Run the Join Token

On **managerone**, print the worker join command:

```bash theme={null}
docker swarm join-token worker
```

Copy the `docker swarm join --token …` line and execute it on **workertwo**. Then confirm on **managerone**:

```bash theme={null}
docker node ls
# ... workertwo   Ready   Active   19.03.8
```

## 4. Promote a Worker to Manager

1. List current nodes:

   ```bash theme={null}
   docker node ls
   ```

2. Promote **workerone**:

   ```bash theme={null}
   docker node promote workerone
   # Node workerone promoted to a manager in the swarm.
   ```

3. Verify the new manager status:

   ```bash theme={null}
   docker node ls
   # workerone now shows MANAGER STATUS: Reachable
   ```

4. (Optional) Inspect **workerone** in detail:

   ```bash theme={null}
   docker node inspect workerone --pretty
   ```

## 5. Demote a Manager back to Worker

If you need to revert **workerone** to a purely worker role:

```bash theme={null}
docker node demote workerone
docker node ls
# workerone returns to no MANAGER STATUS
```

## 6. Drain and Reactivate a Node

To prevent new tasks from scheduling on **workerone**:

```bash theme={null}
docker node update --availability drain workerone
docker node ls
# AVAILABILITY: Drain
```

When you’re ready to allow tasks again:

```bash theme={null}
docker node update --availability active workerone
docker node ls
# AVAILABILITY: Active
```

## 7. Remove a Node from the Swarm

1. Drain **workerone**:

   ```bash theme={null}
   docker node update --availability drain workerone
   ```

2. Attempt removal (will fail if the node is still up):

   ```bash theme={null}
   docker node rm workerone
   # Error: node is not down and can't be removed
   ```

3. On **workerone**, leave the swarm:

   ```bash theme={null}
   docker swarm leave
   # Node left the swarm.
   ```

4. Back on **managerone**, remove the node:

   ```bash theme={null}
   docker node rm workerone
   docker node ls
   # Only managerone and workertwo remain.
   ```

Congratulations! You’ve successfully created, scaled, and managed a Docker Swarm cluster on CentOS 7.6.

***

## References and Further Reading

* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Get Started with Swarm Mode](https://docs.docker.com/get-started/swarm/)
* [Docker Engine Installation Guide](https://docs.docker.com/engine/install/centos/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/0780e900-ee0f-4afc-8c0e-7355a335dcb7)


# Docker Config Objects

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Docker-Config-Objects/page

Explains Docker Swarm Config objects for distributing small read only configuration files to services, why they replace host bind mounts for replicated services, and how to manage them.

Let’s explore Docker Config objects in Docker Swarm and why they are a better fit than host bind mounts for distributing configuration files to replicated services.

<Frame>
  <img alt="A dark presentation slide with the title &#x22;Docker Config&#x22; centered, featuring blue and purple wavy shapes at the bottom and faint circular and container-like graphics in the background." />
</Frame>

## Single-host bind mount example

On a single Docker host (not in a Swarm), you can run an NGINX container that uses a custom configuration file by bind-mounting the file from the host into the container:

```bash theme={null}
docker run -v /tmp/nginx.conf:/etc/nginx/nginx.conf nginx
```

This mounts `/tmp/nginx.conf` from the host into `/etc/nginx/nginx.conf` inside the container so NGINX uses your custom configuration.

## Why bind mounts are problematic in a Swarm

In a Swarm, you deploy services (not standalone containers). If you try to bind-mount a host file into a replicated service, every node that might run a replica must have the file at the same host path. For example:

```bash theme={null}
docker service create --replicas=4 -v /tmp/nginx.conf:/etc/nginx/nginx.conf nginx
```

This will fail if `/tmp/nginx.conf` exists only on one node. Docker cannot bind-mount a host file that does not exist on the node where a replica gets scheduled. Maintaining identical host paths and files across many nodes is error-prone and fragile.

## Use Docker Config objects to distribute configuration

Docker Configs are designed to distribute small, mostly static configuration files across the Swarm. Create the config on a manager node (the contents are stored in the Swarm and propagated to worker nodes), then attach it to services.

1. Create a config from a manager:

```bash theme={null}
docker config create nginx-conf /tmp/nginx.conf
```

2. Create the service and attach the config. To place the config at a specific path inside the container (for example, `/etc/nginx/nginx.conf`), specify `src` and `target`:

```bash theme={null}
docker service create --replicas=4 --config src=nginx-conf,target=/etc/nginx/nginx.conf nginx
```

If you add a config without a `target`, Docker will create a file at the container root named after the config (for example, `/nginx-conf`).

> **lightbulb** Docker Config objects are a Swarm-only feature and can only be attached to services (not to standalone `docker run` containers). Always create configs from a manager node so the Swarm stores and distributes the data to worker nodes.

## Configs vs volumes

Configs are for small, read-only configuration data that should be injected into service tasks. They are not intended to replace volumes when you need persistent read-write storage.

| Resource Type | Best for                                                          | Example usage                                                      |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| Config        | Small, static configuration files or secrets (read-only to tasks) | `docker config create nginx-conf /tmp/nginx.conf`                  |
| Volume        | Persistent read-write storage shared by containers                | `docker volume create data` and `--mount source=data,target=/data` |

## Managing configs and rotating them

Common operations when working with configs:

* Detach (remove) a config from a service:

```bash theme={null}
docker service update --config-rm nginx-conf nginx
```

* Remove the config object (only allowed when no service is using it):

```bash theme={null}
docker config rm nginx-conf
```

* Rotate a config for an existing service: create the new config, then update the service to remove the old config and add the new one in a single update:

```bash theme={null}
docker config create nginx-conf-new /tmp/nginx-new.conf
docker service update \
  --config-rm nginx-conf \
  --config-add src=nginx-conf-new,target=/etc/nginx/nginx.conf \
  nginx
```

This ensures service tasks receive the updated configuration on redeploy.

> **warning** You cannot remove a config object while any service is using it. Remove the config from all services first (`--config-rm`), then delete the config object (`docker config rm`). Failing to do so will produce an error.

## Quick commands reference

| Action                          | Command                                                       |
| ------------------------------- | ------------------------------------------------------------- |
| Create config                   | `docker config create <name> <file>`                          |
| List configs                    | `docker config ls`                                            |
| Inspect config                  | `docker config inspect <name>`                                |
| Remove config                   | `docker config rm <name>`                                     |
| Attach config to service        | `docker service create --config src=<name>,target=<path> ...` |
| Update service to remove config | `docker service update --config-rm <name> <service>`          |

## Summary

* Bind mounts work on a single host but are brittle in a Swarm because each node must have the same host path and file.
* Docker Configs let you centrally store and distribute configuration files across the Swarm and mount them into service tasks.
* Use `--config src=<name>,target=<path>` to control where the file appears inside the container.
* Configs are available only to Swarm services and must be created from a manager node.

## Links and references

* [Docker Docs — Configs](https://docs.docker.com/engine/swarm/configs/)
* [Docker Docs — Services and Swarm mode](https://docs.docker.com/engine/swarm/)
* [Docker Best Practices](https://docs.docker.com/develop/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/142aebcc-9c35-463f-bd83-79297c18419f)
