# Legacy
docker service create -p 80:5000 my-web-server

# New explicit
docker service create \
  --publish published=80,target=5000 \
  my-web-server

# With UDP protocol
docker service create \
  --publish published=80,target=5000,protocol=udp \
  my-web-server
```

## Links and References

* [Docker Networking Overview](https://docs.docker.com/network/)
* [Docker Swarm Mode](https://docs.docker.com/engine/swarm/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
* [VXLAN Protocol](https://en.wikipedia.org/wiki/Virtual_Extensible_Local_Area_Network)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/667d3636-67d3-4ee9-9dc6-c06e71196559" />
</CardGroup>


# Docker Stack

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Docker-Stack/page

This guide explains transitioning from single-host Docker Compose to multi-node orchestration using Docker Stack in a Swarm cluster.

In this comprehensive guide, you'll learn how to move from single-host Docker Compose deployments to robust, multi-node orchestration using Docker Stack on a Swarm cluster. We’ll compare `docker run` vs. Compose, introduce Docker Swarm concepts, and walk through a real-world voting application example—complete with replicas, placement constraints, resource limits, and health checks.

## 1. Docker Run vs. Docker Compose

When you start with containers, you often use `docker run` for each service:

```bash theme={null}
docker run simple-webapp
docker run mongodb
docker run redis:alpine
```

However, for multi-service applications, Docker Compose simplifies management by defining services in a single YAML file:

```yaml theme={null}
