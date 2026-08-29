# Hands on

Source: https://notes.kodekloud.com/docs/Virtualization-and-Containers/Hands-on/Hands-on/page

Hands-on walkthrough comparing virtual machines and containers, demonstrating boot time, isolation, resource usage, persistence, Docker examples, and real-world use cases.

So far we've covered the theory of virtual machines and containers. Now we'll put that into practice to observe differences in boot time, isolation, resource usage, and persistence. This walkthrough shows how to create and run a VM and containers, measure their behavior, and outline real-world use cases.

What we'll cover

* Create and run a virtual machine and observe behavior.
* Create and run containers with Docker and observe behavior.
* Compare boot time, isolation, resource usage, and persistence.
* Wrap up with real-life use cases for VMs and containers.

<Frame>
  <img alt="The image shows a person wearing a &#x22;KodeKloud&#x22; shirt against a black background with purple gear icons." />
</Frame>

## Virtual machines (VMs) — demo with UTM (type‑2 hypervisor)

Virtual machines run a full operating system in a hosted environment. For this demo we use UTM (a type‑2 hypervisor). Other common hypervisors include VirtualBox and VMware Fusion depending on your OS.

Key considerations when creating a VM

* Resource allocation: assign RAM and disk space carefully — e.g., assigning 0.5 GB RAM and \~1.7 GB disk requires that the host have at least that much free memory and storage.
* Never assign more RAM to a VM than the host physically has if you want predictable performance. Some hypervisors support memory overcommit, but that can lead to swapping and degraded performance.

Boot time

* A VM boots a full OS. In this setup, Windows XP boots in \~1 minute. We'll compare this to container startup times later.

Isolation and security

* VMs provide strong isolation: if a VM becomes compromised, you can delete the virtual disk and rebuild the VM.
* Isolation is not absolute: network-enabled VMs remain reachable from the internet unless you restrict access. Avoid using real accounts or sensitive data inside unpatched or unsupported VMs.

> **warning** Unpatched or unsupported VMs (older OS builds) can be vulnerable to attacks. Treat any VM with internet access as potentially unsafe—do not store real credentials or sensitive data inside them.

Persistence example

* VMs use a virtual hard disk. Files you create inside the VM persist across reboots and power cycles because they are written to the VM's virtual disk.
* Example: saving a Minesweeper high score inside the VM, shutting down, and restarting — the score remains.

Common VM use cases

* Home: test risky apps or try a new OS without altering your main system.
* Workplace: run legacy systems that cannot be updated.
* Cloud: rent full VMs from cloud providers (e.g., AWS EC2) to host dev/test or production workloads.

## Containers with Docker

For containers this demo uses Docker Desktop. Docker Desktop runs on macOS, Windows, and Linux and provides an easy way to build, share, and run containerized apps.

* Docker Hub is a public registry for container images (like an app store for images). Images pack the application code, dependencies, configuration, and runtime instructions.
* When you run an image that isn't present locally, Docker pulls it from Docker Hub automatically.

<Frame>
  <img alt="The image features a person standing next to the Docker logo and an illustration of a container on a dark background." />
</Frame>

### Basic Docker examples

1. One-shot container: rancher/cowsay

This runs a short-lived container that prints a message then exits.

Command:

```bash theme={null}
docker run rancher/cowsay kode-kow
```

Typical output (Docker pulls the image, runs the container, prints the cowsay message, then the container exits):

```bash theme={null}
Unable to find image 'rancher/cowsay:latest' locally
latest: Pulling from rancher/cowsay
cbdeb7a5b2a2: Pull complete
dd0e5d8c62a1: Pull complete
34d5e986175: Pull complete
13eefddf168: Pull complete
Digest: sha256:5dab61268c18da56feb585b6189161cd806dbc49a22a36128ca26f0bfd94
Status: Downloaded newer image for rancher/cowsay:latest

< kode-kow >
 ________
< moo >
 --------
       \   ^__^
        \  (oo)\_______
           (__)\       )\/\
               ||----w |
               ||     ||
```

Confirm the container ran by listing all containers:

```bash theme={null}
docker ps -a
```

Example output:

```text theme={null}
CONTAINER ID   IMAGE              COMMAND             CREATED         STATUS                       PORTS   NAMES
d1c6d2f02526   rancher/cowsay     "cowsay kode-kow"   8 seconds ago   Exited (0) 7 seconds ago             brave_diffie
```

Note: One-shot containers commonly run, produce output, and exit immediately — unlike a VM that stays booted.

2. Long-running container: nginx

Run Nginx detached and map host port 8888 to container port 80:

```bash theme={null}
docker run -d -p 8888:80 nginx
```

What the flags do:

* `-d` runs the container in detached mode (background).
* `-p 8888:80` maps port 8888 on the host to port 80 inside the container.

Sample pull and run output (truncated):

```bash theme={null}
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
59e2267830b: Pull complete
1404da4789dc: Extracting [=============================>] 30.28MB/43.97MB
96e47e79401e: Pull complete
...
Status: Downloaded newer image for nginx:latest
93afc397f64c  # container id returned
```

Confirm the container is running and the port mapping:

```bash theme={null}
docker ps -a
```

Example output:

```text theme={null}
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                     NAMES
93afc397f64c   nginx     "nginx -g 'daemon of…"   10 seconds ago  Up 9 seconds   0.0.0.0:8888->80/tcp      optimistic_wilson
```

Open your browser to [http://localhost:8888](http://localhost:8888) and you should see the default Nginx welcome page.

Isolation and resource usage

* Containers share the host kernel but run in isolated user-space environments. On Linux, containers use the host kernel directly. On macOS and Windows, Docker Desktop runs a lightweight VM that provides a Linux kernel for containers.
* Containers cannot access other containers or the host unless you explicitly grant filesystem mounts, network access, or extra capabilities.
* Docker Desktop provides per-container CPU and memory statistics for monitoring resource usage.

Hands-on in the browser

* If you prefer not to install Docker locally, use a browser-based Docker playground to run the same commands. Behavior is the same: one-shot containers exit after producing output; long-running containers stay active and can be accessed via the playground's port-forwarding UI.

### Persistence inside containers

By default, files written inside a container's writable layer are ephemeral: removing the container deletes those files. To persist data, mount a host directory or use a Docker named volume.

Example: add a file inside a running Nginx container

```bash theme={null}
