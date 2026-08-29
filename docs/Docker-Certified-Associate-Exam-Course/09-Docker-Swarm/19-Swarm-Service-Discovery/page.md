# Swarm Service Discovery

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Swarm-Service-Discovery/page

Service discovery in Docker Swarm allows containers to communicate by name, enhancing reliability and simplifying microservices architecture.

Service discovery in Docker Swarm enables containers and services to locate and communicate with each other by name, rather than by changing IP addresses. This improves reliability and simplifies your microservices architecture.

## Container-to-Container Communication

By default, Docker Engine allows containers on the same node to resolve each other by container name via its built-in DNS server at `127.0.0.11`. Relying on container names prevents issues when IPs change after restarts.

```python theme={null}
