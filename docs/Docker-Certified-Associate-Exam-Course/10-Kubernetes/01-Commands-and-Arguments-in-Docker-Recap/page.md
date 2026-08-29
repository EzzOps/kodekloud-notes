# Commands and Arguments in Docker Recap

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Commands-and-Arguments-in-Docker-Recap/page

This guide explains Docker commands, arguments, and entrypoints, covering default processes, command overrides, and the differences between CMD and ENTRYPOINT.

In this guide, we’ll dive into how Docker handles **commands**, **arguments**, and **entrypoints**. You’ll learn to:

* Understand why `docker run ubuntu` exits immediately
* See how Docker images set a default process with `CMD`
* Override the default command at runtime
* Bake custom commands into your own image
* Differentiate between `CMD` and `ENTRYPOINT`
* Combine `CMD` and `ENTRYPOINT` for flexible defaults
* Replace an entrypoint on the fly

***

## 1. Why `docker run ubuntu` Exits Immediately

First, run the following:

```bash theme={null}
docker run ubuntu
docker ps
docker ps -a
```

You’ll observe:

* `docker run ubuntu` starts a container, then it exits right away.
* `docker ps` shows no active containers.
* `docker ps -a` lists your Ubuntu container with an **Exited** status.

Containers are designed to run a single process. When that process ends, the container stops.

<Callout icon="triangle-alert">
  Without an interactive shell or long-running process, the default `/bin/bash` has no TTY and quits immediately—so does the container.
</Callout>

***

## 2. How Images Define Default Commands (`CMD`)

Docker images declare a default executable in their `Dockerfile` using `CMD`. For example:

```dockerfile theme={null}
