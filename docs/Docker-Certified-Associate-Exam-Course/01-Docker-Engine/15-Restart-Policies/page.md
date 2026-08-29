# The next command fails if port 8306 is in use:
docker run -d -p 8306:3306 mysql
```

<Callout icon="triangle-alert">
  Host ports must be unique. Attempting to bind the same host port twice will cause Docker to error out.
</Callout>

## 3. Binding to Specific Host Interfaces

If your machine has multiple network interfaces, you can restrict port binding to a particular IP:

```bash theme={null}
# Bind only on 192.168.1.5
docker run -p 192.168.1.5:8000:5000 kodekloud/simple-webapp

# Bind only on loopback (accessible locally)
docker run -p 127.0.0.1:8000:5000 kodekloud/simple-webapp
```

## 4. Dynamic Host Port Allocation

Omitting the host port lets Docker assign a random port (default range 32768–60999):

```bash theme={null}
docker run -d -p 5000 kodekloud/simple-webapp
```

To view the port range:

```bash theme={null}
cat /proc/sys/net/ipv4/ip_local_port_range
# Example output:
# 32768 60999
```

## 5. Publishing All Exposed Ports (`-P`)

If an image’s Dockerfile declares one or more `EXPOSE` ports, you can automatically map them to random host ports:

```Dockerfile theme={null}
# Dockerfile snippet
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask
COPY app.py /opt/
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
```

Build and run:

```bash theme={null}
docker build -t simple-webapp .
docker run -P simple-webapp
```

You can also expose additional ports at runtime:

```bash theme={null}
docker run -P --expose=8080 simple-webapp
```

Inspect the exposed ports:

```bash theme={null}
docker inspect simple-webapp --format '{{json .NetworkSettings.Ports}}'
# Example output:
# {"5000/tcp":[{"HostIp":"0.0.0.0","HostPort":"32768"}],
#  "8080/tcp":[{"HostIp":"0.0.0.0","HostPort":"32769"}]}
```

## 6. Port Publishing Options at a Glance

| Option     | Description                                      | Syntax                                  |
| ---------- | ------------------------------------------------ | --------------------------------------- |
| `-p`       | Map specific host and container ports            | `-p [host_ip:]host_port:container_port` |
| `-P`       | Publish all `EXPOSE`d ports to random host ports | `-P`                                    |
| `--expose` | Expose additional container ports (no host bind) | `--expose=port[/protocol]`              |

## 7. Under the Hood: iptables NAT

Docker uses Linux `iptables` to forward traffic from host ports to container IPs. It creates custom chains (`DOCKER`, `DOCKER-USER`) in the `nat` table:

1. Packet arrives on the host port.
2. PREROUTING chain directs it to the `DOCKER` chain.
3. A DNAT rule rewrites the packet’s destination to the container’s IP and port.
4. The packet is forwarded to the container.
5. Response packets are SNAT’d or MASQUERADE’d back to the host.

Inspect Docker’s NAT rules:

```bash theme={null}
iptables -t nat -S DOCKER
# Sample output:
# -N DOCKER
# -A DOCKER ! -i docker0 -p tcp -m tcp --dport 41232 \
#     -j DNAT --to-destination 172.17.0.3:5000
```

<Callout icon="lightbulb">
  You can insert custom rules in the `DOCKER-USER` chain to filter or modify traffic before Docker’s own rules apply.
</Callout>

***

Further Reading and References

* [Docker Networking Overview](https://docs.docker.com/network/)
* [Docker Run Reference](https://docs.docker.com/engine/reference/commandline/run/)
* [iptables Manual](https://linux.die.net/man/8/iptables)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/cc1e3b40-f4a6-47a4-acff-e6c9182cafd8" />
</CardGroup>


# Restart Policies

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Restart-Policies/page

Docker restart policies control automatic restarts of containers after failures or daemon restarts, ensuring reliability for services and jobs.

Docker restart policies let you control if and when a container is automatically restarted. Whether you’re running a critical web service or a batch job, these policies ensure your containers recover from failures or daemon restarts.

## Why Containers Stop

A container can exit for several reasons:

1. **Normal completion**\
   The primary process finishes successfully (exit code 0), for example, a script completes its task.
2. **Failure**\
   The process crashes or throws an error, exiting with a non-zero code (e.g., bad input).
3. **Manual intervention**\
   Running `docker container stop` sends a SIGTERM, then a SIGKILL after a timeout:
   * If the process traps SIGTERM and exits cleanly, it may return code 0.
   * If it’s killed with SIGKILL, it usually exits with a non-zero code.

When you need a container—say, a production API or CI runner—to restart immediately after a crash, Docker’s restart policies come into play.

## Docker Restart Policies

Specify a restart policy with `--restart` when you run a container:

| Policy         | Behavior                                                                                                        | CLI Flag                   |
| -------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------- |
| no (default)   | Never restart automatically.                                                                                    | `--restart=no`             |
| on-failure     | Restart only if exit code ≠ 0. Optionally limit retries: `on-failure[:<max-retries>]`.                          | `--restart=on-failure:5`   |
| always         | Always restart regardless of exit status. If you manually stop the container, it will restart on daemon reboot. | `--restart=always`         |
| unless-stopped | Like `always`, but honors manual stops across daemon restarts.                                                  | `--restart=unless-stopped` |

<Callout icon="lightbulb">
  Use `on-failure[:<max-retries>]` to prevent infinite restart loops. Docker immediately retries with no backoff delay.
</Callout>

### Quick Reference

* **no**: No auto-restart.
* **on-failure**: Auto-restart only on errors (non-zero exit).
* **always**: Auto-restart on any exit.
* **unless-stopped**: Auto-restart on any exit, but not after a manual stop.

## Examples

### 1. Default (`no`)

```bash theme={null}
docker run --name test-no --restart=no ubuntu \
  expr 3 + 5
