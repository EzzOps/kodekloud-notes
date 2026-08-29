# Container Sandboxing

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Minimize-Microservice-Vulnerabilities/Container-Sandboxing/page

Hardening containers by applying sandboxing techniques such as namespaces, seccomp, AppArmor, capability drops, and microVM alternatives to reduce kernel attack surface and improve isolation.

In this lesson we examine how to harden containers by applying sandboxing techniques that reduce the kernel attack surface and limit what containerized processes can do. We contrast container isolation with virtual machines, show practical examples (including PID namespaces), and present common sandboxing controls and advanced alternatives that provide stronger isolation.

## Quick refresher: virtual machines vs containers

Virtual machines provide strong isolation because each VM runs a full guest operating system and its own kernel on top of a hypervisor. Containers, by contrast, share the host kernel and isolate processes using kernel mechanisms such as namespaces and cgroups. That architecture difference is critical when evaluating attack surfaces and escape risks.

<Frame>
  <img alt="A diagram titled &#x22;Container Sandboxing&#x22; comparing virtual machines and containers. It shows layered stacks (application, libs, deps, guest OS) with VMs using a hypervisor and separate guest OSes, while containers share Docker and the host OS over the hardware." />
</Frame>

| Isolation Aspect                  | Virtual Machines                | Containers                                |
| --------------------------------- | ------------------------------- | ----------------------------------------- |
| Kernel per workload               | Yes — dedicated guest kernel    | No — shared host kernel                   |
| Isolation mechanism               | Hypervisor-based                | Namespaces, cgroups, LSMs                 |
| Typical use case                  | Strong multi-tenant isolation   | Lightweight microservices, higher density |
| Escape risk if kernel compromised | Lower (guest kernel separation) | Higher (shared kernel)                    |

## PID namespaces: a simple example

Containers map process IDs into a PID namespace. Inside the container, a process can appear as PID 1, while on the host it has a different PID. This demonstrates logical process isolation but also shows that the host can still observe and terminate the underlying host PID.

Example (run a BusyBox container that sleeps for 1000 seconds):

```bash theme={null}
