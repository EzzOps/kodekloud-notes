# Run a container that sleeps
$ docker run -d --name sleeping-container busybox sleep 1000
e2fd5090c9a51eb7cc91a466cf2e18c5468871f84adbb55c2e6c1cf4ea0028a8

# Inside the container: PID 1 is the sleep process
$ docker exec -ti sleeping-container ps -ef
PID   USER     TIME  COMMAND
1     root     0:00  sleep 1000
11    root     0:00  ps -ef

# On the host you can also see the sleep process with a different PID
$ ps -ef | grep sleep | grep -vi grep
root     7902  7871  0 21:39 ?        00:00:00 sleep 1000
```

Because the host-level process exists, killing that host PID terminates the container process. This shows that namespaces provide isolation at the user-space level, but the shared kernel remains the ultimate control plane.

<Callout icon="warning">
  Containers share the host kernel. If the kernel has a vulnerability (for example, a local privilege escalation like Dirty COW), a compromised container process can potentially exploit the kernel and affect the host and other containers.
</Callout>

## How containerized processes interact with the kernel

Applications (in containers or on bare OS) run in user space and make system calls to access hardware and privileged services. Since containers use the host kernel, restricting system call access and other kernel-visible actions is a key hardening strategy. Two widely used kernel-level sandboxing controls are seccomp and AppArmor (or SELinux).

* Seccomp: restricts the set of system calls a process may invoke.
* AppArmor: enforces path- and capability-based access controls for files and other resources.

Both tools reduce the risk of a kernel exploit being used from within a container by reducing what code inside the container can ask the kernel to do.

## Example sandboxing configurations

Example seccomp profile (whitelist-style — deny by default, allow a small syscall set):

```json theme={null}
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "execve",
        "brk",
        "access",
        "capset",
        "clone"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

Example AppArmor profile snippet (blacklist-style rule denying writes to /proc):

```text theme={null}
profile apparmor-deny-write flags=(attach_disconnected) {
    #include <abstractions/base>

    # Allow typical reads and library access (adjust paths for your program)
    /usr/bin/your-binary ixr,
    /lib/** r,
    /usr/lib/** r,
    /etc/** r,

    # Deny all write access to /proc
    deny /proc/** w,
}
```

### Whitelist vs blacklist approaches

| Pattern                      | Description                                      | Strengths                               | Trade-offs                               |
| ---------------------------- | ------------------------------------------------ | --------------------------------------- | ---------------------------------------- |
| Whitelist (seccomp)          | Default deny; explicitly allow required syscalls | Minimal kernel surface, strong security | Requires profiling/application knowledge |
| Blacklist (AppArmor snippet) | Default allow; block specific actions or paths   | Easier to implement for diverse apps    | May miss attack vectors; less strict     |

<Callout icon="lightbulb">
  When feasible, prefer whitelist-based restrictions (e.g., seccomp profiles) to minimize the kernel functionality exposed to containerized applications. Use blacklists when you need broader compatibility and then complement them with other controls.
</Callout>

## Practical guidance for production workloads

* Small, homogeneous fleets: Create strict, minimal seccomp and AppArmor/SELinux profiles for each service (for example, many Nginx or MySQL instances). This gives strong protection with manageable maintenance.
* Large, heterogeneous fleets: Use a layered approach — namespaces + cgroups + capability drops + seccomp + LSMs (AppArmor/SELinux) — and focus on automation to generate and roll out profiles.
* Follow the principle of least privilege: drop Linux capabilities your process does not need and restrict filesystem and network access.
* Monitor and iterate: use runtime observability and profiling to generate accurate whitelists and to find false positives/negatives before enforcing strict policies.

## Advanced sandboxing / microVM alternatives

If the shared-kernel model is unacceptable for your threat model, consider technologies that provide stronger kernel isolation by running containers inside lightweight VMs or alternative kernels:

| Technology      | Description                                                             | Use case                                          |
| --------------- | ----------------------------------------------------------------------- | ------------------------------------------------- |
| gVisor          | User-space kernel that intercepts syscalls and emulates kernel behavior | Improve isolation without heavy VMs               |
| Kata Containers | Runs container workloads inside lightweight VMs managed by a runtime    | Stronger isolation with VM-level boundaries       |
| Firecracker     | MicroVMs designed for minimal overhead and fast startup                 | Serverless and multi-tenant isolation at VM level |

These projects trade some density and complexity for stronger separations between workloads and the host kernel.

## Further reading and references

* Seccomp man page: [https://man7.org/linux/man-pages/man2/seccomp.2.html](https://man7.org/linux/man-pages/man2/seccomp.2.html)
* AppArmor project: [https://apparmor.net/](https://apparmor.net/)
* Dirty COW vulnerability: [https://en.wikipedia.org/wiki/Dirty\_COW](https://en.wikipedia.org/wiki/Dirty_COW)
* gVisor: [https://gvisor.dev/](https://gvisor.dev/)
* Kata Containers: [https://katacontainers.io/](https://katacontainers.io/)
* Firecracker: [https://firecracker-microvm.github.io/](https://firecracker-microvm.github.io/)

Choose the combination of sandboxing techniques that best fits your operational constraints and threat model. No single control is sufficient on its own — layering defenses increases resilience while balancing manageability.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/7431dd03-f5c2-4ebb-b94a-2d35615bbd8c/lesson/cb62e103-2544-447d-98cd-d669d79bd382" />
</CardGroup>


# Control Plane Isolation

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Minimize-Microservice-Vulnerabilities/Control-Plane-Isolation/page

This article explores control plane isolation in Kubernetes to ensure secure, multi-tenant environments through namespaces, access control mechanisms, and resource quotas.

In this article, we will explore control plane isolation in Kubernetes—a critical mechanism for ensuring secure, multi-tenant environments. By isolating the control plane, different teams can operate without interfering with each other’s operations. This isolation is achieved through namespaces, access control mechanisms, and resource quotas.

## Namespaces Overview

Namespaces offer a way to partition cluster resources among multiple users, ensuring that resources in one namespace remain isolated from those in another. This strategy yields two primary benefits:

* Resource names within one namespace can overlap with those in another, allowing teams to use familiar names without conflicts.
* Many Kubernetes security policies, including role-based access control (RBAC), roles, and network policies, are scoped to individual namespaces.

The diagram below illustrates Kubernetes cluster control plane isolation using namespaces across three nodes. Each node manages different namespaces for effective resource management.

<Frame>
  ![The image illustrates Kubernetes cluster control plane isolation using namespaces across three nodes, each containing different namespaces for resource management.](https://kodekloud.com/kk-media/image/upload/v1752871635/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Control-Plane-Isolation/frame_30.jpg)
</Frame>

You can create namespaces easily with the following commands:

```bash theme={null}
kubectl create namespace namespaceA
kubectl create namespace namespaceB
```

Within each namespace, you can deploy pods or services—allowing the same name to be used across namespaces without conflict.

## Authorization and Access Control

Proper authorization is the cornerstone of control plane isolation. Without adequate restrictions, teams or workloads might improperly access or modify API resources, undermining security policies. Implementing the principle of least privilege is essential: each team should only access the namespaces and resources they require.

The next diagram emphasizes Kubernetes control plane isolation through access controls. It showcases how namespaces, pods, services, persistent volumes, and RBAC policies work together to enforce the principle of least privilege.

<Frame>
  ![The image illustrates Kubernetes control plane isolation using access controls, featuring namespaces with pods, services, persistent volumes, and RBAC policies, emphasizing the principle of least privilege.](https://kodekloud.com/kk-media/image/upload/v1752871636/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Control-Plane-Isolation/frame_110.jpg)
</Frame>

RBAC configurations within each namespace dictate which users or service accounts can perform specific actions, ensuring that permissions are strictly confined to their appropriate scope even when teams share the same cluster.

### Example: Role and RoleBinding in the Development Namespace

The following example demonstrates how to create a Role and a corresponding RoleBinding in the "development" namespace. The Role, "developer-role," grants permissions (get, list, watch, create, update, delete) on pods and services. The RoleBinding, "developer-rolebinding," then ties this role to the user "pranjal."

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: developer-role
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch", "create", "update", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-rolebinding
  namespace: development
subjects:
  - kind: User
    name: pranjal
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
```

<Callout icon="lightbulb">
  This configuration enforces strict access control, ensuring that user "pranjal" can only perform the defined actions on pods and services within the "development" namespace.
</Callout>

## Summary

Control plane isolation in Kubernetes is essential for maintaining a secure and efficient multi-tenant cluster environment. By effectively using namespaces along with tightly scoped RBAC policies and access controls, organizations can ensure that each team operates within its designated boundaries without affecting others.

For more information, explore our additional resources on [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) and [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/7431dd03-f5c2-4ebb-b94a-2d35615bbd8c/lesson/4b127100-e6b3-42a9-af50-4bcf5966ef76" />
</CardGroup>
