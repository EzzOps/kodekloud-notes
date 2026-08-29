# eBPF Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cilium-Overview/eBPF-Basics/page

Overview of eBPF, kernel versus user space, benefits over kernel modules, use cases in observability, networking and security, and how Cilium and XDP leverage eBPF

In this lesson we’ll take a focused, practical look at eBPF: what it is, why it matters, how it fits into the kernel ↔ user-space model, and why projects like Cilium use it to replace legacy datapaths such as iptables/kube-proxy.

To understand eBPF, we first need a quick refresher on the kernel and the purpose of separating user and kernel spaces.

A computer exposes hardware resources (CPU, memory, disk, GPUs, network interfaces) that applications need to use. Letting untrusted applications access hardware directly is dangerous:

* Applications would need device-specific logic and drivers, increasing complexity.
* A buggy or malicious application could crash the whole system.
* Direct access increases the attack surface and enables abuse of hardware/data.

<Frame>
  <img alt="A presentation slide titled &#x22;Kernel – Introduction&#x22; showing three apps (app1, app2, app3) directly connected with lines to hardware components labeled CPU, Memory, Disks, and Devices. The right side lists issues with direct hardware access: apps must know device communication, faulty apps can crash the system, and there's a risk of unauthorized hardware access." />
</Frame>

To avoid those problems, operating systems provide a privileged intermediary: the kernel. The kernel mediates resource access (CPU scheduling, memory allocation, device control, filesystems) and enforces process isolation and access control.

Key kernel responsibilities

* Allocate CPU time, memory, and I/O devices among processes.
* Enforce memory and execution isolation so one process cannot corrupt another.
* Provide a controlled interface for applications via system calls.
* Load and manage device drivers that implement hardware-specific logic.

Device drivers are kernel components that translate generic kernel operations into device-specific actions for disks, NICs, GPUs, printers, etc.

Applications access hardware indirectly through well-defined system calls (open/read/write, socket, mmap, ioctl, etc.). Modern OSes split execution into two privilege domains:

* Kernel space — privileged code with full access to hardware and CPU features.
* User space — unprivileged applications that must request kernel services via system calls.

This separation provides:

* Security: limit what processes can do.
* Stability: confine crashes to user processes rather than the whole OS.
* Multitasking: kernel arbitrates resource sharing and context switching.

<Frame>
  <img alt="A slide titled &#x22;Why This Separation?&#x22; showing three numbered colored tiles labeled &#x22;Security,&#x22; &#x22;Stability,&#x22; and &#x22;Multi-Tasking&#x22; with corresponding icons. The tiles are orange, pink, and green gradients with large white numbers overlaid." />
</Frame>

Common Linux system calls (examples)

|            Category | Example syscalls                                     | Purpose                                           |
| ------------------: | ---------------------------------------------------- | ------------------------------------------------- |
|     Process control | `fork`, `execve`, `exit`, `wait`                     | Create/terminate processes and manage child state |
|     File management | `open`, `read`, `write`, `close`                     | Filesystem I/O and descriptor operations          |
|    Memory & devices | `mmap`, `brk`, `ioctl`                               | Memory mapping and device-specific controls       |
|          Networking | `socket`, `bind`, `listen`, `accept`, `send`, `recv` | Network socket lifecycle and I/O                  |
| Security & identity | `chmod`, `chown`, `getuid`                           | Permissions and identity checks                   |

Example syscall flow when an application opens a file:

1. User-space application calls a library wrapper (e.g., libc `open()`).
2. The wrapper issues the kernel system call, which transitions execution into kernel space.
3. The kernel performs the operation using drivers and hardware access.
4. Results are returned to user space and the application resumes.

<Frame>
  <img alt="A flowchart titled &#x22;Example of System Call&#x22; showing the interaction between User Space and Kernel Space: user requests a service, a library wrapper issues a system call, control switches to the kernel which identifies and executes the call, then returns the result to user space." />
</Frame>

What is eBPF?

[eBPF](https://ebpf.io/) (extended Berkeley Packet Filter) is a kernel feature that lets you safely run small, verified programs inside the Linux kernel without changing kernel source or loading untrusted kernel modules. The kernel verifier enforces safety (bounded loops, valid memory access, correct registers), and verified programs can be JIT‑compiled for native performance. eBPF programs communicate with user space through shared data structures called BPF maps.

Originally developed for packet filtering, eBPF has evolved into a general mechanism for in-kernel extensibility used for observability, networking, security enforcement, tracing, and other kernel‑level tasks—exposed and controlled from user space.

<Callout icon="lightbulb">
  eBPF programs are verified and sandboxed by the kernel verifier, and communicate with user-space via BPF maps. Once verified, eBPF bytecode can be JIT-compiled for high throughput and low latency. Learn more at the official eBPF site: [https://ebpf.io/](https://ebpf.io/).
</Callout>

<Frame>
  <img alt="A slide titled &#x22;eBPF – Introduction&#x22; showing a three-circle Venn-style diagram of colored circles numbered 01–03 labeled Observability, Networking, and Security. A caption at the bottom reads &#x22;eBPF unlocks kernel features for user-space applications.&#x22;" />
</Frame>

Why eBPF instead of kernel modules?

Traditional kernel modules are powerful but dangerous: they run with full kernel privileges, can crash the system, and often need recompilation for different kernel versions. eBPF provides similar capabilities dynamically, while being safer and easier to deploy from user space.

<Frame>
  <img alt="A presentation slide titled &#x22;eBPF – Introduction&#x22; listing four capabilities: monitor all system calls, intercept and modify network packets, enforce security policies in real time, and trace function execution inside the kernel. A caption at the bottom notes that eBPF lets user‑space apps safely tap into kernel features without modules." />
</Frame>

Advantages of eBPF over kernel modules:

* No kernel-source changes or per-kernel-module builds.
* Dynamic load/unload without reboot.
* Kernel verifier reduces risk of crashes and undefined behavior.

<Frame>
  <img alt="A presentation slide titled &#x22;eBPF – Introduction&#x22; showing two comparison boxes: &#x22;Before eBPF&#x22; (saying it needed a risky kernel module and a reboot) and &#x22;With eBPF&#x22; (saying it can safely extend the kernel from userspace). The slide is branded © KodeKloud." />
</Frame>

What an eBPF program can do once loaded

* Collect and aggregate observability data, exposing it to user space via BPF maps.
* Inspect, filter, modify, or redirect packets at various kernel hook points.
* Attach to syscalls, kprobes/uprobes, tracepoints, or cgroup hooks for runtime tracing or enforcement.
* Be updated or unloaded by user-space controllers without a kernel reboot.

What problems does eBPF solve?

1. Observability overhead:
   Traditional instrumentation often relies on polling or intrusive tracing that increases overhead. eBPF enables event-driven, low-overhead tracing of syscalls, kernel events, and user-space interactions in near real time.

<Frame>
  <img alt="A presentation slide titled &#x22;What Problem Does eBPF Solve?&#x22; showing an illustration of servers, a monitor and a mobile device. The slide states &#x22;1. Performance overhead in observability&#x22; with a note that polling-based tools add overhead." />
</Frame>

2. Visibility into kernel ↔ user interactions:
   Getting safe, fine-grained insight into syscalls, memory allocation, and network traffic was historically intrusive. eBPF makes real-time tracing safe and efficient.

<Frame>
  <img alt="A presentation slide titled &#x22;What Problem Does eBPF Solve?&#x22; highlighting &#x22;Limited visibility into kernel and user-space interactions.&#x22; It notes that traditional debugging is intrusive while eBPF enables real-time tracing across kernel and user space, and includes an illustration of a laptop with an eye, gears, and a padlock." />
</Frame>

3. Network packet processing latency:
   eBPF programs (including XDP) can filter and process packets at kernel hook points far earlier than the traditional network stack. This enables much lower latencies and higher throughput than iptables/nftables in high-scale scenarios.

<Frame>
  <img alt="A presentation slide titled &#x22;What Problem Does eBPF Solve?&#x22; highlighting &#x22;3. Network packet processing latency.&#x22; It states that eBPF enables faster packet processing than iptables and shows an icon of a server and monitor." />
</Frame>

4. Runtime security and enforcement:
   Detecting and stopping malicious behavior (suspicious syscalls, kernel rootkits, anomalous memory access) is hard with classic tools. eBPF enables dynamic policy enforcement and behavioral analysis in real time.

<Frame>
  <img alt="A slide titled &#x22;What Problem Does eBPF Solve?&#x22; showing a folder/lock security icon and the point &#x22;4. Security challenges (runtime threat detection)&#x22; with two bullets: &#x22;Traditional tools struggle with real-time threat detection&#x22; and &#x22;eBPF enables dynamic analysis and policy enforcement.&#x22;" />
</Frame>

Common eBPF use cases

|                Use case | Typical goals                                                     |
| ----------------------: | ----------------------------------------------------------------- |
| Observability & tracing | Low-overhead tracing, syscall capture, performance profiling      |
|              Networking | DDoS mitigation, firewalling, L4/L7 load balancing, NAT/tunneling |
|                Security | Runtime threat detection, policy enforcement, exploit mitigation  |
|      Performance tuning | Scheduling, memory/disk I/O optimization, hot-path profiling      |

One important eBPF-based framework: XDP (eXpress Data Path). XDP allows eBPF programs to attach at the earliest packet receive hook—inside the NIC driver—so packets can be accepted, modified, redirected, or dropped before they go through the kernel network stack. This yields ultra-low-latency packet handling for DDoS mitigation, load balancing, and other high-performance networking tasks.

<Callout icon="lightbulb">
  XDP programs run at the earliest receive hook (NIC/driver level) and are ideal for high-performance packet ops such as drop/redirect/modify. XDP is widely used when ultra-low latency and extreme throughput are required.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;XDP – Introduction&#x22; with a stylized gauge icon and upward arrows. The caption explains XDP is a high‑performance packet processing framework that runs eBPF programs at the NIC driver level." />
</Frame>

How eBPF relates to Cilium

[Cilium](https://cilium.io/) is a Container Network Interface (CNI) that uses eBPF extensively to implement high-performance, secure, and observable networking for Kubernetes. Key points:

* In-node packet forwarding is implemented with eBPF programs (replacing large iptables rule sets).
* Service load balancing can be implemented in-kernel with eBPF instead of kube-proxy + iptables.
* Network policies are enforced at packet hooks via eBPF.
* Observability (flows, metrics, tracing) is integrated into the eBPF datapath.
* Additional features (encryption, multi-cluster connectivity, scalable load balancing) are accelerated by eBPF.

<Frame>
  <img alt="A diagram titled &#x22;Role of eBPF in Cilium&#x22; showing three Kubernetes nodes (node01–node03) with apps (app1–app5), kernel/k-proxy components and a green &#x22;App2 Service&#x22; layer spanning them. Arrows show traffic flows between apps and a padlock icon indicates encrypted communication." />
</Frame>

Why replace iptables / kube-proxy with eBPF?

iptables/nftables builds ordered rule lists that are evaluated sequentially. As the number of services and rules grows, lookup latency and update costs increase—and rule updates can require expensive rebuilds.

eBPF solutions store state in BPF maps and per-CPU data structures (hash tables, arrays, LRU maps) which give near-constant-time lookups and cheap updates. This improves latency and scalability in large clusters and high-throughput environments.

<Frame>
  <img alt="A slide titled &#x22;Why Replace iptables With eBPF?&#x22; showing kube-proxy (iptables) behavior: a vertical arrow with five blue service boxes (Service 1–5) and backend IP addresses listed next to each. A small note reads &#x22;Changes to rules trigger a full rebuild.&#x22;" />
</Frame>

eBPF implementations commonly use per-CPU maps to avoid contention and to keep lookup/update performance stable across CPU cores.

<Frame>
  <img alt="A slide titled &#x22;Why Replace iptables With eBPF?&#x22; showing an eBPF-based per-CPU hash table diagram that maps example names (John Smith, Lisa Smith, Sandra Dee) through hash buckets to stored values. The right side shows bucket indices pointing to phone-number-like entries (e.g., 521-8976, 521-9655)." />
</Frame>

Measured results show that for small numbers of services iptables and eBPF look similar, but as services scale up iptables latency grows while eBPF remains much more stable—delivering lower HTTP/TCP latencies at scale.

<Frame>
  <img alt="A slide with two bar charts comparing eBPF versus traditional kube-proxy/iptables networking latencies as the number of Kubernetes services increases. The charts show eBPF (blue) consistently lower HTTP and TCP latencies while iptables-based approaches (red/yellow) rise noticeably with more services." />
</Frame>

Summary

* Direct hardware access by applications creates complexity, instability, and security issues. The kernel mediates hardware access safely.
* Device drivers let the kernel control hardware devices.
* System calls are the interface user-space programs use to request kernel services.
* Kernel space is privileged; user space runs with restricted privileges and uses syscalls to access features.
* eBPF enables small, verified programs to run within the kernel without adding unsafe modules. eBPF programs use BPF maps to communicate with user space and are verified for safety.
* eBPF use cases include observability, tracing, packet processing, load balancing, runtime security, and performance tuning.
* Cilium leverages eBPF to replace kube-proxy, implement load balancing, enforce policies, and deliver built-in observability and encryption.
* XDP is an eBPF-based framework that operates at the NIC/driver level for ultra-low-latency packet processing.

<Frame>
  <img alt="A presentation conclusion slide listing four numbered points about eBPF and user space. It notes that user space runs with limited privileges, eBPF safely runs programs in the Linux kernel without adding modules, provides a sandbox for small dynamic programs, and unlocks kernel features for user-space applications." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Conclusion&#x22; showing four numbered summary points about eBPF, Cilium, and XDP. It notes eBPF's roles in monitoring, load balancing and security; Cilium using eBPF to replace kube-proxy and provide network features; and XDP running eBPF at the NIC/driver level for ultra-low-latency packet processing." />
</Frame>

Further reading and references

* eBPF official site: [https://ebpf.io/](https://ebpf.io/)
* Cilium: [https://cilium.io/](https://cilium.io/)
* Kubernetes kube-proxy documentation: [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)
* iptables: [https://netfilter.org/projects/iptables/index.html](https://netfilter.org/projects/iptables/index.html)
* nftables: [https://wiki.nftables.org/](https://wiki.nftables.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/9c9fa5ec-2721-4654-9383-5cb9b264e8b6/lesson/58731990-66de-48cf-8c16-025e8ebe7410" />
</CardGroup>
