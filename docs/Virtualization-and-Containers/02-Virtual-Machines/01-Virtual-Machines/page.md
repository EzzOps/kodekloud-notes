# Virtual Machines

Source: https://notes.kodekloud.com/docs/Virtualization-and-Containers/Virtual-Machines/Virtual-Machines/page

Overview of virtual machines, hypervisors, VM types, networking, security, performance tradeoffs, and management for running multiple isolated operating systems on one physical host.

Running separate services on separate machines can waste resources, while packing everything onto a single system increases the risk of outages. Virtualization lets you balance isolation and efficiency by running multiple independent “computers” on one physical host.

<Frame>
  <img alt="The image shows a person presenting next to an illustration of servers with gears, labeled with &#x22;Payroll,&#x22; &#x22;Email,&#x22; and &#x22;Backup.&#x22;" />
</Frame>

Imagine you only have one physical machine but need software that only runs on a different OS. For example, Cody is on a Mac, but her client sent a legacy Microsoft Access database that runs only on Windows. Instead of buying new hardware or switching operating systems, Cody can create a virtual machine (a full Windows system) that runs safely inside macOS. That process is called virtualization.

<Frame>
  <img alt="The image shows a person in a &#x22;KodeKloud&#x22; shirt beside a laptop with a &#x22;VM&#x22; icon and an inset graphic of another laptop screen." />
</Frame>

This article explains how virtualization works, what hypervisors do, the key benefits and limitations of VMs, and practical considerations such as networking, security, and resource management.

A brief history: virtualization dates back to the 1960s when IBM used it on mainframes — the centralized machines still common in finance and government. Later, VMware and Microsoft popularized virtualization on commodity servers, enabling modern data centers and public cloud platforms.

<Frame>
  <img alt="The image features an illustrated depiction of early virtualization technology with the IBM logo, accompanied by a person in the foreground wearing a KodeKloud t-shirt." />
</Frame>

<Frame>
  <img alt="The image features a person in a KodeKloud shirt discussing virtualization technology, with logos for AWS, VMware, and Microsoft, and a graphic of servers in a cloud labeled &#x22;2025&#x22;." />
</Frame>

What is a VM?

At its core, virtualization lets a single physical computer run multiple separate “pretend” computers simultaneously. Each virtual machine (VM) includes its own operating system, applications, and configuration.

<Frame>
  <img alt="The image shows a person standing next to a graphic of a laptop screen, which displays two virtual machines with Apple and Windows operating systems. The person is wearing a &#x22;KodeKloud&#x22; t-shirt." />
</Frame>

The physical machine is the host; the VMs are guests — isolated and independent. VMs are useful for running legacy applications, testing updates, or hosting multiple customers on shared hardware in cloud environments.

<Frame>
  <img alt="The image shows a person standing next to a laptop screen displaying graphics labeled &#x22;Old Software&#x22; and &#x22;Risky Update,&#x22; under the logos of AWS and Google Cloud. The person is wearing a KodeKloud shirt." />
</Frame>

Example: Two people can each host a small website using a single physical AWS server. AWS runs multiple VMs on the same hardware to reduce cost while keeping each customer’s environment isolated.

<Frame>
  <img alt="The image shows a diagram comparing two websites hosted on an AWS server, along with a person speaking beside it wearing a KodeKloud t-shirt." />
</Frame>

How virtualization works

Consider the familiar stack: hardware at the bottom, then the host OS and kernel, and apps on top. Virtualization adds a layer called the hypervisor between hardware and guest systems. The hypervisor partitions and abstracts physical resources, presenting each VM with virtual hardware.

A hypervisor is software or firmware that enables multiple guest operating systems to run concurrently on a single host by mediating access to CPU, memory, storage, and devices.

<Frame>
  <img alt="The image depicts a conceptual illustration of virtualization, featuring a hypervisor managing multiple operating systems, with a speaker from KodeKloud presenting." />
</Frame>

Hypervisor types

<Frame>
  <img alt="The image shows a person speaking next to a graphic describing &#x22;Type 01 Bare-Metal&#x22; and &#x22;Type 02 Hosted&#x22; related to a hypervisor." />
</Frame>

There are two primary hypervisor categories:

* Type 1 (bare-metal): Installed directly on physical hardware, often with only a minimal management layer rather than a full general-purpose host OS. These are common in data centers and server deployments (examples: VMware ESXi, Microsoft Hyper-V).

<Frame>
  <img alt="The image illustrates a Type 1 bare-metal hypervisor setup with labeled operating systems and data centers, featuring VMware ESXi and Microsoft Hyper-V logos, alongside a presenter from KodeKloud." />
</Frame>

* Type 2 (hosted): Runs on top of an existing operating system like any other application. This is what Cody used to run Windows inside macOS (examples: VirtualBox, VMware Workstation).

For both types, the hypervisor gives each VM virtualized CPU, memory, storage, and network interfaces so that each guest OS can run as if on its own physical machine.

<Frame>
  <img alt="The image illustrates a layered virtualization concept with a hypervisor managing multiple operating systems, alongside a person standing to the side wearing a &#x22;KodeKloud&#x22; shirt." />
</Frame>

Key considerations

Networking

VMs are isolated by default but can communicate when configured. Common VM network modes and their best uses:

| Mode                              | Use Case                                               | Notes                                                            |
| --------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- |
| NAT (Network Address Translation) | Simple internet access for guest without exposing it   | VM shares host’s IP externally; good for secure defaults         |
| Bridged                           | Run servers reachable by other devices on the same LAN | VM receives its own IP on the physical network                   |
| Host-only                         | Local testing and development between host and VMs     | No external internet access; isolates traffic for secure testing |

<Frame>
  <img alt="The image illustrates a networking concept with virtual machines (VMs) connected to the internet and each other, alongside a person from KodeKloud presenting the information." />
</Frame>

<Frame>
  <img alt="The image explains &#x22;Host Only&#x22; networking for virtual machines, showing how VMs can only communicate with the host machine and not with the internet or other VMs. A person is standing beside the illustration." />
</Frame>

Security

VMs provide strong isolation: a compromised guest often won’t affect the host if isolation is properly configured. Still, VMs are not invulnerable:

* Shared folders, clipboard sharing, and misconfigured virtual networks can enable cross-VM or host compromise.
* Hypervisor vulnerabilities, though rare, can allow escape from a VM to the host; vendors release patches to mitigate this risk.

If you run risky software, disconnect the VM from networks and disable file sharing.

<Frame>
  <img alt="The image features a person in a &#x22;KodeKloud&#x22; shirt discussing security with a graphic depicting virtual machines (VMs) labeled OS01, OS02, and OS03 on a circuit-like platform." />
</Frame>

> **warning** Always assume network-exposed VMs can be probed or attacked. Isolate and restrict access for risky workloads and keep hypervisors up to date with security patches.

Performance and resource usage

VMs improve hardware utilization by consolidating workloads, but each VM runs a full OS, making them heavier than containers:

* Longer boot times and larger RAM/disk requirements compared to containers.
* Running many VMs concurrently can overcommit the host if resources aren’t managed.
* GPUs are not automatically available to VMs for graphics-heavy or ML workloads; use GPU passthrough, SR-IOV, or vendor vGPU solutions for better performance.

Start with conservative resource allocations, monitor usage, and scale resources as needed.

<Frame>
  <img alt="The image shows a person standing next to a graphic of stacked blocks labeled &#x22;VM,&#x22; with tips about virtual machines such as starting small and not over-allocating resources." />
</Frame>

Flexibility and management

VMs offer flexibility across OS choices and rich management features:

* Run Linux on Windows or Windows on macOS without rebooting — ideal for legacy apps and mixed development environments.
* Snapshots capture a VM’s exact state so you can roll back after risky changes.
* Cloning creates full copies of a VM for labs, testing, or rapid provisioning.

<Frame>
  <img alt="The image features a person next to graphics and logos related to virtual machines, VMware, and VirtualBox, with a message about taking a snapshot to save the VM state." />
</Frame>

> **lightbulb** Snapshots are great for quick rollbacks, but they are not a substitute for backups. Keep separate backups for important data.

Quick quiz

Which statement is true?

A. A VM runs directly on the hardware with no OS.\
B. A hypervisor lets one computer run multiple VMs.\
C. VMs are isolated, so they can't communicate with each other.

<Frame>
  <img alt="The image shows a person standing next to a quiz question about virtual machines, with options labeled A, B, and C. The person is wearing a KodeKloud t-shirt." />
</Frame>

Answer: B is correct. A is false because while a Type 1 hypervisor runs on bare metal, each VM still runs a full OS on top of the hypervisor. C is misleading: VMs are isolated by default, but they can communicate over configured virtual networks.

Summary

A virtual machine is a full, self-contained “computer” running inside a physical host with its own OS and applications.

* One physical machine can host multiple VMs, each acting like a separate system.
* The hypervisor is the layer that creates and manages VMs by dividing hardware resources.
* Type 1 hypervisors run on bare metal; Type 2 hypervisors run on top of a host OS.
* VMs are flexible and isolated, ideal for testing legacy apps or running multiple systems — but they are heavier than containers and consume more resources.

<Frame>
  <img alt="The image shows a person speaking alongside a visual of a laptop displaying a virtual machine (VM) icon, with an inset suggesting Windows is running on it." />
</Frame>

<Frame>
  <img alt="The image features a person standing next to graphics of a virtual machine (VM) represented as a purple cube, with text highlighting features such as &#x22;Flexible,&#x22; &#x22;Isolated,&#x22; and &#x22;Great for Testing.&#x22;" />
</Frame>

Next steps

This overview covers traditional virtualization with VMs. To understand how containers solve some VM limitations (lighter weight, faster startup, denser packing), continue to the article on containers.

<Frame>
  <img alt="The image features a person standing next to an illustrated container labeled &#x22;Container&#x22; with the word &#x22;Containers&#x22; above it, surrounded by gear and question marks." />
</Frame>

Links and references

* VMware ESXi: [https://www.vmware.com/products/esxi-and-esx.html](https://www.vmware.com/products/esxi-and-esx.html)
* Microsoft Hyper-V: [https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/what-is-hyper-v](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/what-is-hyper-v)
* VirtualBox: [https://www.virtualbox.org/](https://www.virtualbox.org/)
* AWS Virtualization & EC2 concepts: [https://aws.amazon.com/ec2/](https://aws.amazon.com/ec2/)
* GPU passthrough and SR-IOV overviews: search vendor docs for "GPU passthrough" and "SR-IOV" for platform-specific guidance.

- [Watch Video](https://learn.kodekloud.com/user/courses/virtualization-and-containers/module/a6fdb4aa-7875-4117-8639-042702d02558/lesson/b1c2abc4-054a-4abc-ba63-7d49abb4848b)
