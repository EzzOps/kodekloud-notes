# find the container id (or use the first few unique characters)
docker exec -it <container_id> sh

# from inside the container shell:
echo "kode kloud" > /usr/share/nginx/html/test.txt
exit
```

Then visit [http://localhost:8888/test.txt](http://localhost:8888/test.txt) to view the file.

Persist data with a host directory mount:

```bash theme={null}
docker run -d -p 8888:80 -v ~/nginx-data:/usr/share/nginx/html nginx
```

* Files written to `~/nginx-data` on the host will persist even if you remove and recreate the container.

> **lightbulb** Containers are designed to be fast, portable, and disposable. Use Docker volumes or host mounts to persist important data across container restarts or recreations.

## Quick comparison: VM vs Container

| Characteristic    |                              Virtual Machine (VM) | Container                                                        |
| ----------------- | ------------------------------------------------: | ---------------------------------------------------------------- |
| Boot time         |        Slow (boots a full OS, seconds to minutes) | Fast (milliseconds to seconds)                                   |
| Isolation         |  Strong (separate kernel instances or hypervisor) | Kernel-level isolation (namespaces, cgroups); shares host kernel |
| Persistence       |              Virtual disk persists across reboots | Ephemeral by default; use volumes for persistence                |
| Resource usage    |             Higher (full OS, dedicated resources) | Lower (shared kernel, lightweight)                               |
| Typical use cases | Legacy systems, full OS testing, secure isolation | App deployment, microservices, CI/CD, scaling                    |
| Examples          |                     `UTM`, `VirtualBox`, `VMware` | `Docker`, `Podman`, `containerd`                                 |

## Real-world use cases

* Home: run risky apps, sandbox new OS versions, or experiment without modifying the host.
* Development teams: use containers to ensure consistent environments across dev, CI, staging, and production.
* Enterprises: run scalable microservices, CI pipelines, and thousands of containers to deploy updates rapidly.
* Cloud: use VMs when you need a full OS or strong isolation; use containers for portable, scalable app workloads.

## Summary

* VMs (e.g., UTM, VirtualBox, VMware) run full operating systems with strong isolation and persistent virtual disks. They're well suited for legacy apps, full OS testing, or scenarios requiring strict isolation.
* Containers (e.g., Docker, Podman, containerd) run lightweight, isolated user-space environments that share the host kernel. They are ideal for fast, portable application deployment and scalable architectures.
* This walkthrough demonstrated differences in boot time, isolation, and persistence, and provided hands-on commands you can try locally or in an online playground.

## Links and references

* [UTM — getutm.app](https://getutm.app)
* [VirtualBox — virtualbox.org](https://www.virtualbox.org)
* [VMware Fusion — vmware.com](https://www.vmware.com/products/fusion.html)
* [Docker Desktop — docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
* [Docker Hub — hub.docker.com](https://hub.docker.com)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [AWS EC2 course on KodeKloud](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

- [Watch Video](https://learn.kodekloud.com/user/courses/virtualization-and-containers/module/742008ab-ddfc-4b6b-bc4b-b7d3f9a0dafb/lesson/490c590a-203d-4ed1-9b58-b9ee3ec93d69)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/virtualization-and-containers/module/742008ab-ddfc-4b6b-bc4b-b7d3f9a0dafb/lesson/5265946b-bbf8-4263-af97-f6a7a0f6edad)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Virtualization-and-Containers/Introduction/Course-Introduction/page

Intro to virtualization and containers, covering hypervisors, VMs, container runtimes, orchestration, deployment workflows, and practical labs for scalable, reliable production systems.

Imagine a global platform — like Amazon — where millions of users search for products, add items to wishlists, make payments, recharge mobiles, and use services such as Amazon Pay simultaneously.

How does a company keep all those different services running reliably and independently, without creating a maintenance nightmare?

Think of Amazon as a massive ship, and each service — product search, payments, user profiles — as a separate shipping container on that ship.

<Frame>
  <img alt="The image features a person standing on the right wearing a &#x22;KodeKloud&#x22; t-shirt, with a digital illustration of a crane, shipping containers, a boat, and a mobile shopping interface on the left." />
</Frame>

Each container keeps its cargo isolated and secure while the ship moves everyone forward together. This is the practical power of virtualization and containers: running many isolated workloads on shared hardware while keeping them manageable and scalable.

<Frame>
  <img alt="The image features a person in front of a graphic with the Amazon logo, alongside illustrations labeled &#x22;VM&#x22; and &#x22;Container.&#x22; The person is wearing a &#x22;KodeKloud&#x22; T-shirt." />
</Frame>

Hi, I'm Alan — your guide through this virtualization and containers course. Below is a clear roadmap of what you'll learn and why these technologies matter in production systems.

What you'll learn

* Fundamentals of virtualization and how a single physical server can behave like many logical machines.
* The role of hypervisors and how they isolate and manage virtual machines (VMs).
* What containers are, their advantages (fast startup, portability, resource efficiency), and how they manage persistent data using volumes and patterns.
* When to choose VMs vs containers — strengths, trade-offs, and common hybrid deployments.
* Hands-on workflows: installing runtimes, building and managing images, running containers, and orchestrating at scale.
* Real-world case studies demonstrating how organizations scale services and deploy updates reliably.

Hypervisors and virtual machines
First, we'll explore virtualization: how a hypervisor enables multiple operating systems to run concurrently on the same physical host. You'll learn the architecture and trade-offs — better utilization and isolation vs. added overhead and complexity.

<Frame>
  <img alt="The image features a person standing beside a diagram illustrating a hypervisor with multiple operating systems. The person is wearing a &#x22;KodeKloud&#x22; T-shirt." />
</Frame>

Containers and container runtimes
Next, we'll zoom in on containers: lightweight, portable environments that package an application and its dependencies. Containers start quickly, use fewer resources than full VMs, and simplify deployments across environments. We'll also cover volumes and stateful patterns to keep application data consistent and portable.

<Frame>
  <img alt="The image features a person standing beside a graphic depicting containers, with labels highlighting benefits like portability, speed, and resource savings. A small rocket icon adds emphasis to the concept being presented." />
</Frame>

VMs vs Containers — a quick comparison

| Topic             | Virtual Machines (VMs)                           | Containers                                       |
| ----------------- | ------------------------------------------------ | ------------------------------------------------ |
| Isolation         | Strong OS-level isolation (separate kernels)     | Process-level isolation (shared kernel)          |
| Resource overhead | Higher: full guest OS per VM                     | Lower: lightweight runtime and shared kernel     |
| Startup time      | Slower (minutes)                                 | Fast (seconds)                                   |
| Portability       | Portable across hypervisors                      | Portable across container runtimes and platforms |
| Use cases         | Legacy apps, strict isolation, multiple OS types | Microservices, CI/CD, cloud-native apps          |

When to use which

* Choose VMs for workloads that require full OS isolation, different OS kernels, or stricter security boundaries.
* Choose containers for microservices, CI/CD pipelines, and when you need rapid scaling and efficient resource use.
* Many organizations combine both: VMs host container orchestrators, and containers run the workloads.

Hands-on: tools and orchestration
After theory, we'll get practical. You’ll install and use container runtimes and learn how orchestration platforms automate deployment, scaling, and recovery.

> **lightbulb** Before running containers locally, ensure Docker (or your chosen container runtime) is installed and running on your machine.

Example: run a quick container locally

```bash theme={null}
docker run rancher/cowsay kode-kow
```

This simple command demonstrates pulling an image and running a containerized process. We’ll expand on image management, build workflows, tagging, and pushing to registries.

Real-world examples and best practices
To make learning concrete, we’ll walk through real-world scenarios showing how companies use virtualization and containers to launch products, roll out updates, and scale globally — the same principles that keep massive platforms running.

Community and resources
You're not alone in this learning journey. KodeKloud’s community forums offer peer support, and the course provides hands-on labs and examples to practice.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Documentation](https://docs.docker.com/)
* [Hypervisor Overview — VMware](https://www.vmware.com/topics/glossary/content/hypervisor.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/virtualization-and-containers/module/0e41196e-1ae3-43fb-a444-1e0b48253594/lesson/915d3157-22d5-464f-bdfd-07dd2134c1a1)
