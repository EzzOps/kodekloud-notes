# Publishing Ports

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Publishing-Ports/page

This article explores how Docker publishes container ports to the host system, covering basic and advanced port mapping techniques.

In this lesson, we’ll explore how Docker publishes container ports to the host system. We begin with basic port mapping, then move on to advanced options like interface binding, dynamic port allocation, and automatic exposure. By the end, you’ll understand how Docker leverages `iptables` to route traffic between host and container.

## 1. Container vs Host IP

A containerized web application typically listens on an internal port (e.g., `5000`). Every container receives an internal IP (for example, `172.17.0.2`), which is only reachable from the Docker host:

```bash theme={null}
curl http://172.17.0.2:5000
```

However, this IP isn’t accessible from other machines. To allow external access, you must map the container port to a port on the host (e.g., `192.168.1.5`).

## 2. Publishing a Fixed Port (`-p`)

To map container port `5000` to host port `80`, run:

```bash theme={null}
docker run -p 80:5000 kodekloud/simple-webapp
```

Now your application is accessible at:

```text theme={null}
http://192.168.1.5:80
```

### Multiple Instances on Different Ports

You can launch multiple containers binding the same internal port to different host ports:

```bash theme={null}
docker run -d -p 8000:5000 kodekloud/simple-webapp
docker run -d -p 8001:5000 kodekloud/simple-webapp
```

For database services:

```bash theme={null}
docker run -d -p 3306:3306 mysql
docker run -d -p 8306:3306 mysql
