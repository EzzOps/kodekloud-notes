# Containers

Source: https://notes.kodekloud.com/docs/Virtualization-and-Containers/Containers/Containers/page

Explains containers as lightweight isolated environments for single apps, image and Dockerfile basics, networking, persistence with volumes, benefits like portability and speed, and security trade offs.

Last time we saw how virtual machines let one physical computer act like many by running full operating systems side by side. That approach is powerful but can be slow: each VM boots an entire guest OS before your app runs.

<Frame>
  <img alt="The image shows a person standing next to a digital representation of laptops connected to a VM (virtual machine) box, with Apple and Windows logos on the laptop screens." />
</Frame>

Booting a VM adds noticeable overhead. If you only need to run a single process or quickly scale many identical services, starting a full OS each time is overkill.

<Frame>
  <img alt="The image shows a person standing next to a graphic of a laptop displaying virtual machines, with the KodeKloud logo on their shirt." />
</Frame>

Containers solve this by removing the guest OS from the runtime path. They package an application and its dependencies and launch in seconds.

<Frame>
  <img alt="The image illustrates two containers labeled &#x22;App01&#x22; and &#x22;App02&#x22; with a cartoon cat standing on them. It includes the text &#x22;Containers don’t have their own OS,&#x22; and a person is standing on the right side." />
</Frame>

In this lesson we'll:

* Define what a container is and how it isolates a single application.
* Explain why containers are popular (speed, portability, consistency).
* Cover storage and networking basics for containers.

## What is a container?

A container is a lightweight, self-contained environment for running one application or service. It bundles the application code, runtime, libraries, and configuration so the app runs predictably across environments. Crucially, a container does not include a full guest OS. Instead it shares the host machine’s OS kernel—the component that schedules CPU, manages memory, and controls hardware access.

<Frame>
  <img alt="The image shows a person standing in front of a graphic depicting a computer screen with a container symbol crossed out, and a &#x22;Host Kernel&#x22; label. The person is wearing a &#x22;KodeKloud&#x22; t-shirt." />
</Frame>

Most containers rely on Linux kernel features (namespaces, cgroups) for isolation and resource control, so Linux is the dominant platform. On macOS and Windows, tools like Docker Desktop run a lightweight Linux VM behind the scenes so you can use Linux-based containers. Windows also supports native Windows containers that use the Windows kernel.

Think of a container as a super-powered process: isolated from other processes, carrying its dependencies, and fast to start and stop.

## Images and Dockerfiles

Every running container is an instance of an image. An image is an immutable, read-only snapshot that defines the filesystem, runtime, and the command to run. You can launch many containers from the same image.

Images are usually built from a Dockerfile (or equivalent). A Dockerfile is a small declarative script telling a container engine how to assemble the image. Docker is a widely used tool for building and running images; alternatives include Podman and runtimes like containerd.

Example Dockerfile:

```dockerfile theme={null}
FROM node:14-alpine3.16
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]
```

Once you build an image, you can run one container or thousands; each behaves like a clean, standalone application instance you can start, stop, pause, or remove without altering the host system.

<Frame>
  <img alt="The image shows a graphic of a laptop with containers and a user interface labeled &#x22;Standalone App&#x22; with options: Start, Stop, Pause, and Delete, alongside a person in a KodeKloud shirt." />
</Frame>

Networking: containers communicate with each other and the outside world over virtual networks. Container runtimes like Docker create default networks so containers in the same group can communicate. For multi-service setups, orchestration tools such as Docker Compose and Kubernetes handle launching, scaling, service discovery, and network policies.

<Frame>
  <img alt="The image shows a person standing next to a diagram illustrating Docker containers emerging from a laptop, with the Docker logo prominently displayed." />
</Frame>

## Why containers matter

Containers address several practical needs for modern development and operations:

<Frame>
  <img alt="The image shows a person standing next to a digital illustration of containers, Kubernetes, and Docker Compose, with related functionalities like launching, scaling, and connecting." />
</Frame>

* Fast startup: No guest OS to boot, so apps can start in seconds—useful for development and autoscaling.
* Consistency: Images provide identical runtime environments across machines, reducing "works-on-my-machine" problems.
* Portability: Build an image once and run it wherever the container runtime is supported.
* Isolation: Containers isolate the app and its dependencies from other host applications.

<Frame>
  <img alt="The image shows two laptops with &#x22;Container&#x22; and cog graphics on the screens, connected by the word &#x22;Same.&#x22; A person stands next to them, and words &#x22;Portable,&#x22; &#x22;Anywhere,&#x22; and &#x22;Across Platform&#x22; are displayed at the top." />
</Frame>

If you prefer a quick comparison:

| Feature           | Containers                        | Virtual Machines            |
| ----------------- | --------------------------------- | --------------------------- |
| Boot time         | Seconds                           | Minutes                     |
| Includes guest OS | No                                | Yes                         |
| Resource overhead | Low                               | Higher                      |
| Isolation level   | Kernel-level (namespaces/cgroups) | Hardware-level (hypervisor) |
| Portability       | High (images)                     | High but heavier            |

## Limitations and trade-offs

Containers share the host kernel, so their isolation is not as strong as a VM's hardware-level separation. A kernel-level vulnerability could potentially affect other containers or the host. Containers are commonly used for single services; running large monoliths is possible but may require different patterns and operational controls.

<Callout icon="warning">
  Containers share the host kernel. For multi-tenant or high-security scenarios, harden the host, minimize the attack surface, or consider VMs for stronger isolation.
</Callout>

## Data persistence

By default, containers are ephemeral: files written to a container’s internal filesystem are lost when the container is removed. Treat the container’s writable layer like a temporary workspace.

<Frame>
  <img alt="The image features a graphical container with a crossed-out folder icon and the text &#x22;Data Persistence is a DOWNSIDE.&#x22; A person is standing next to it, wearing a KodeKloud t-shirt." />
</Frame>

To keep data beyond a container’s lifecycle, attach volumes. Volumes are external storage that persist independently of container instances and are the recommended way to store databases, logs, or user uploads.

<Callout icon="lightbulb">
  Use volumes to persist important data. Volumes exist outside the container’s writable layer, so removing a container won’t delete the stored data.
</Callout>

## Quick quiz

Which statement is true?

A. A container includes its own full operating system.\
B. Containers always save their data, even after they're deleted.\
C. A container runs in an isolated environment using the host's operating system kernel.

Answer: C. Containers run in isolated spaces but share the host kernel. A is false (containers don't include a full guest OS). B is false unless you attach persistent storage such as volumes.

## Summary

<Frame>
  <img alt="The image explains that containers do not save data by default when they stop, and emphasizes the need to connect a volume to retain data. A person stands beside the explanation, wearing a &#x22;KodeKloud&#x22; shirt." />
</Frame>

* Containers typically run a single app or service in an isolated environment.
* They share the host OS kernel instead of bundling a full guest OS.
* Containers start quickly, behave consistently across environments, and avoid dependency conflicts.
* Containers communicate over virtual networks and can be orchestrated at scale with tools like Kubernetes.
* Use volumes to persist data long-term.

Next up: we'll compare containers to virtual machines in detail and discuss when to use one or the other.

<Frame>
  <img alt="The image shows a person speaking, with diagrams of containers and a virtual machine (VM) on a black background. The person is wearing a T-shirt with the &#x22;KodeKloud&#x22; logo." />
</Frame>

## Links and references

* Docker — [https://www.docker.com/](https://www.docker.com/)
* Kubernetes Basics — [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Podman — [https://podman.io/](https://podman.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/virtualization-and-containers/module/ebb6203c-5ff0-4060-a548-16114883f996/lesson/91dff0ed-e519-43ed-b60b-6393538512f1" />
</CardGroup>
