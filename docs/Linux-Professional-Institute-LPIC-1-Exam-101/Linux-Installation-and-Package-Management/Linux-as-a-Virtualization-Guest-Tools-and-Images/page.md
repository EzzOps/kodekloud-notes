# An array of host[:port] registries to try when pulling an unqualified image, in order.
unqualified-search-registries = ["docker.io"]
```

* Suppress the informational docker wrapper message by creating the marker file:

```bash theme={null}
sudo touch /etc/containers/no-docker
```

Working with images and containers (nginx walkthrough)
Below is a practical workflow for finding, pulling, running, testing, and cleaning up an nginx container using the Docker-compatible CLI. Replace `docker` with `podman` if you prefer explicit Podman commands.

Search for nginx images in the registry:

```bash theme={null}
docker search nginx
```

Pull the official nginx image (long and short forms both work):

```bash theme={null}
docker pull docker.io/library/nginx
# or
docker pull nginx
```

Example pull output (truncated):

```text theme={null}
Trying to pull docker.io/library/nginx:latest...
Getting image source signatures
Copying blob c4ffe9532b5f done
Copying blob 2215908dc0a2 done
Copying config 12766a6745 done
Writing manifest to image destination
Storing signatures
[AWS_SECRET_ACCESS_KEY]
[aaron@LFCS-CentOS ~]$
```

List images available locally:

```bash theme={null}
docker images
```

Example:

```text theme={null}
REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
docker.io/library/nginx    latest    12766a6745ee   17 hours ago    146 MB
docker.io/library/nginx    1.20.2    8f34c303855f   17 hours ago    146 MB
```

Remove an older image tag:

```bash theme={null}
docker rmi nginx:1.20.2
```

Example output:

```text theme={null}
Untagged: docker.io/library/nginx:1.20.2
Deleted: [SECRET_REDACTED]
[aaron@LFCS-CentOS ~]$
```

Creating and running containers

* By default, running without -d attaches your terminal to the container's stdout/stderr. Use Ctrl+C to stop.

Run in the foreground (attached):

```bash theme={null}
docker run nginx
```

Run detached (background):

```bash theme={null}
docker run -d nginx
# outputs container ID, e.g.:
# 92a87f978de3...
```

List running containers:

```bash theme={null}
docker ps
```

List all containers (running and stopped):

```bash theme={null}
docker ps --all
```

Stop and remove containers:

```bash theme={null}
docker stop <container-name-or-id>
docker rm <container-name-or-id>
```

Notes on safe image removal:

* docker rmi fails if an image is in use by any container. Preferred safe removal sequence:
  1. Stop containers: docker stop \<container>
  2. Remove containers: docker rm \<container>
  3. Remove image: docker rmi \<image>

Naming containers and exposing ports

* Assign a name and publish ports with --name and -p HOST:CONTAINER. Example: run nginx named mywebserver with host port 8080 mapped to container port 80:

```bash theme={null}
docker run -d -p 8080:80 --name mywebserver nginx
# Example returned container ID:
# 7953475436b9...
```

Testing the web server with netcat

* Use netcat (nc) to query the server. Pass host and port as separate arguments (no colon):

```bash theme={null}
nc localhost 8080
GET /
```

You should receive the nginx default index.html content:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</html>
```

Press Ctrl+C to exit nc.

<Callout icon="warning">
  Ports below 1024 are privileged. To bind host port 80 to a container, run the command with elevated privileges (sudo) or map a non-privileged host port (>=1024).
</Callout>

Binding to privileged port 80 (example):

```bash theme={null}
sudo docker run -d -p 80:80 --name mywebserver nginx
```

Getting help and Podman-specific options

* Get detailed help for any command with --help:

```bash theme={null}
docker run --help
docker rm --help
# or
podman run --help
```

Podman rm options (example excerpt):

```text theme={null}
podman rm [options] CONTAINER [CONTAINER...]

Examples:
  podman rm imageID
  podman rm mywebserver myflaskserver 860a4b23
  podman rm --force --all
  podman rm -f c684f0d469f2

Options:
  -a, --all           Remove all containers
  -f, --force         Force removal of a running or unusable container
  -v, --volumes       Remove anonymous volumes associated with the container
  -t, --time uint     Seconds to wait for stop before killing the container (default 10)
  ...
```

Quick reference: common Docker/Podman commands

| Action                     | Command                                                       |
| -------------------------- | ------------------------------------------------------------- |
| Search registry            | `docker search <term>`                                        |
| Pull image                 | `docker pull \<image>`                                        |
| List local images          | `docker images`                                               |
| Run container (foreground) | `docker run \<image>`                                         |
| Run detached               | `docker run -d -p <host>:\<container> --name <name> \<image>` |
| List running containers    | `docker ps`                                                   |
| List all containers        | `docker ps --all`                                             |
| Stop container             | `docker stop \<container>`                                    |
| Remove container           | `docker rm \<container>`                                      |
| Remove image               | `docker rmi \<image>`                                         |

Links and references

* [Podman documentation](https://podman.io/)
* [Containers configuration (containers.conf / registries.conf)](https://github.[SECRET_REDACTED]-registries.5.md)
* [Docker CLI reference](https://docs.docker.com/engine/reference/commandline/cli/)

This concludes the short hands-on introduction to pulling images, running containers, mapping ports, and cleaning up images. Practice these commands in a lab environment to build confidence and reinforce container lifecycle management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/a44e2a00-f21e-41d2-b33d-4a45ef05d395" />
</CardGroup>


# Linux as a Virtualization Guest Tools and Images

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Linux-as-a-Virtualization-Guest-Tools-and-Images/page

This article discusses virtualization in Linux, covering hypervisors, VM migration strategies, types of virtual machines, IaaS considerations, and automating VM initialization with cloud-init.

Virtualization allows a hypervisor—a software layer—to host multiple fully emulated computer systems (guests) as isolated processes. The hypervisor allocates physical resources (CPU, memory, storage) to each VM, emulating BIOS, disk controllers, and network interfaces using disk image files stored on the host.

<Frame>
  ![The image is an informational slide about virtualization, explaining the roles of hypervisors and virtual machines, including their functions and characteristics.](https://kodekloud.com/kk-media/image/upload/v1752881428/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/virtualization-hypervisors-virtual-machines-slide.jpg)
</Frame>

## Common Linux Hypervisors

Some of the most popular hypervisors for running Linux virtual machines include:

* **Xen**\
  An open-source Type-1 (bare-metal) hypervisor that boots directly on hardware without an underlying OS.
* **KVM (Kernel Virtual Machine)**\
  A Linux kernel module that turns your host into a hypervisor. Though it runs within a Linux OS (Type-2), its in-kernel design delivers near Type-1 performance. Managed via `libvirt` and supporting tools.

<Frame>
  ![The image is a slide describing the Kernel Virtual Machine (KVM) as a Linux kernel module for virtualization, supporting both Type-1 and Type-2 hypervisors, and requiring a generic Linux operating system to function.](https://kodekloud.com/kk-media/image/upload/v1752881429/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/kvm-linux-kernel-virtualization-slide.jpg)
</Frame>

* **Oracle VM VirtualBox**\
  A cross-platform desktop hypervisor (Type-2) for Linux, macOS, and Windows, known for its user-friendly GUI and extensive guest additions.

<Frame>
  ![The image is a slide describing VirtualBox as a popular desktop application for creating and managing virtual machines, highlighting its cross-platform compatibility with Linux, macOS, and Windows.](https://kodekloud.com/kk-media/image/upload/v1752881430/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/virtualbox-desktop-application-overview.jpg)
</Frame>

## VM Migration Strategies

Migrating VMs between hosts is crucial for maintenance, load balancing, and disaster recovery:

* **Cold migration**: Moves a powered-off VM.
* **Live migration**: Transfers a running VM with minimal downtime.

<Frame>
  ![The image is a slide explaining virtual machine migrations, highlighting that some hypervisors allow dynamic relocation, with migration involving moving a virtual machine between hypervisors. It distinguishes between regular migration, which may require shutdown, and live migration, which occurs while the machine is running.](https://kodekloud.com/kk-media/image/upload/v1752881431/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/virtual-machine-migrations-hypervisors-slide.jpg)
</Frame>

## Types of Virtual Machines

Virtual machines are classified by how the guest OS interacts with the hypervisor:

1. **Fully Virtualized Guests**\
   The guest OS is unmodified and unaware of virtualization. All instructions are emulated or passed through hardware virtualization extensions (Intel VT-x or AMD-V).

<Callout icon="lightbulb">
  Ensure Intel VT-x or AMD-V is enabled in your BIOS/UEFI before deploying fully virtualized guests.
</Callout>

<Frame>
  ![The image contains a list of characteristics and requirements for fully virtualized guests, including the need for Intel VT-x or AMD-V CPU extensions on x86 platforms.](https://kodekloud.com/kk-media/image/upload/v1752881433/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/virtualized-guests-requirements-list.jpg)
</Frame>

2. **Paravirtualized Guests (PVMs)**\
   The guest OS runs with hypervisor-aware kernels and special drivers, reducing emulation overhead for improved performance.

<Frame>
  ![The image is a slide about paravirtualized guests, explaining that the guest operating system is aware it's running in a virtual machine and uses a modified kernel and special drivers for better performance.](https://kodekloud.com/kk-media/image/upload/v1752881434/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/paravirtualized-guests-virtual-machine-slide.jpg)
</Frame>

3. **Hybrid Guests**\
   Combines full virtualization for CPU and memory with paravirtualized drivers (e.g., `virtio` on KVM, Guest Additions on VirtualBox) for near-native I/O throughput.

<Frame>
  ![The image is a slide titled "Hybrid Guests" that explains the combination of paravirtualization and full virtualization, mentioning the use of paravirtualized drivers for performance enhancement, and references to KVM and VirtualBox.](https://kodekloud.com/kk-media/image/upload/v1752881435/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/hybrid-guests-paravirtualization-virtualbox-kvm.jpg)
</Frame>

<Frame>
  ![The image illustrates three types of virtual machines: Paravirtualized Guest, Fully Virtualized Guest, and Hybrid Guest, each represented by a cube icon.](https://kodekloud.com/kk-media/image/upload/v1752881437/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/virtual-machines-paravirtualized-fully-hybrid.jpg)
</Frame>

## Infrastructure as a Service (IaaS) Considerations

IaaS providers deliver hypervisor-based VM instances with web consoles and APIs. Administrators should evaluate:

| Resource       | Use Case                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------- |
| Compute        | Virtual CPU and memory billed hourly or by vCPU‐seconds. Automate scaling to reduce waste.  |
| Block Storage  | Persistent volumes for VM disks. Pricing tiers vary by capacity and IOPS.                   |
| Object Storage | Scalable storage for unstructured data; archival tiers for infrequent access at low cost.   |
| Networking     | Virtual networks, subnets, security groups, DNS, and VPN connectivity to on-premises sites. |

### Compute Instances

Plan instance types and counts to optimize CPU and memory usage. Monitor billing dashboards to avoid surprise charges.

<Frame>
  ![The image is a slide discussing computing instances, highlighting that providers charge based on usage rates, and emphasizing the need for careful planning to manage cloud costs. It also notes that computing instances can refer to virtual machines in a cloud environment, with higher usage leading to higher costs.](https://kodekloud.com/kk-media/image/upload/v1752881438/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/computing-instances-cloud-costs-planning.jpg)
</Frame>

### Block Storage

Attach block volumes as virtual disks. Select performance tiers (e.g., SSD vs. HDD) based on throughput requirements.

<Frame>
  ![The image is a slide about block storage, explaining its use for web-based traffic or external storage to host files, with costs varying based on storage amount and speed.](https://kodekloud.com/kk-media/image/upload/v1752881439/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/block-storage-web-traffic-costs-slide.jpg)
</Frame>

### Object & Archival Storage

Use for backups, logs, and large datasets. Archive tiers offer the lowest cost for infrequent retrievals.

### Networking Services

Design virtual networks, subnets, and security policies through the provider’s console or API. Implement VPN or dedicated links for hybrid cloud scenarios.

<Frame>
  ![The image contains text about networking, describing web-based utilities for network design, DNS solutions, and hybrid solutions for connecting on-premise infrastructure to the cloud via VPN.](https://kodekloud.com/kk-media/image/upload/v1752881441/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Linux-as-a-Virtualization-Guest-Tools-and-Images/networking-web-utilities-dns-vpn.jpg)
</Frame>

## Automating VM Initialization with cloud-init

`cloud-init` standardizes first-boot configuration across cloud platforms using a YAML-based cloud-config file. Typical configurations include:

* Hostname and timezone setup
* System updates and package installations
* User account creation and SSH key injection
* Network interface configuration

Example `cloud-config`:

```yaml theme={null}
#cloud-config
timezone: Africa/Dar_es_Salaam
hostname: test-system
