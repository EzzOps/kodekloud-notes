# Connect a container to a custom network
docker network connect custom-net my-container

# Disconnect a container from a network
docker network disconnect custom-net my-container
```

These commands make it easy to adjust a container’s network access on the fly.

***

## Removing Networks

Clean up unused networks to avoid clutter:

```bash theme={null}
# Remove a specific network
docker network rm custom-net

# Remove all unused networks
docker network prune
```

<Callout icon="triangle-alert">
  This will remove **all** networks not used by at least one container.\
  Are you sure you want to continue? \[y/N]
</Callout>

***

## Links and References

* [Docker Networking Overview](https://docs.docker.com/network/)
* [Docker CLI: network commands](https://docs.docker.com/engine/reference/commandline/network/)
* [Docker Compose Networking](https://docs.docker.com/compose/networking/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/ddc7602c-93a8-4a6f-900c-a5cf6f7b0716/lesson/de119e3f-37e8-4286-97be-55bd35702e84" />
</CardGroup>


# CGroups

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Security/CGroups/page

Linux control groups (cgroups) provide control over system resources by organizing processes into hierarchical groups, essential for container platforms like Docker.

Linux control groups (cgroups) are a critical **Linux kernel feature** that provides fine-grained control over system resources—such as CPU, memory, network bandwidth, and block I/O—by organizing processes into hierarchical groups. Container platforms like Docker rely on cgroups to enforce resource constraints, ensuring each container consumes only its allocated share of host resources. This isolation improves performance predictability, security, and density on shared infrastructure.

<Callout icon="lightbulb">
  Before you begin, verify that your host kernel supports the desired cgroups version. Modern distributions default to cgroups v2, while Docker remains compatible with both v1 and v2.
</Callout>

| Resource Type | Docker Flag                 | Description                                         |
| ------------- | --------------------------- | --------------------------------------------------- |
| CPU           | `--cpus`, `--cpu-shares`    | Limit CPU cores or adjust relative CPU weight       |
| Memory        | `--memory`, `--memory-swap` | Set maximum RAM usage and optional swap space       |
| Block I/O     | `--blkio-weight`            | Control disk I/O priority (range: 10–1000)          |
| Network       | `docker run --network`      | Configure network mode; use `tc` for bandwidth caps |

In the following sections, we will demonstrate how to apply cgroup-based resource limits to Docker containers, with practical examples for **CPU**, **memory**, **block I/O**, and **network** configurations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/59a97752-06d2-4cac-a4d0-ad4240730912/lesson/b1259c25-e914-429d-bcf4-047da1ad0f74" />
</CardGroup>
