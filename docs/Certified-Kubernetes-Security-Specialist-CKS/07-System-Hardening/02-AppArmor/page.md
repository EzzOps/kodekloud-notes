# AppArmor

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/AppArmor/page

This article explores AppArmor, a Linux security module that limits application access to system resources, enhancing container security beyond Seccomp profiles.

In this lesson, we explore AppArmor, a robust Linux security module designed to limit an application's access to system resources. By enforcing strict restrictions, AppArmor helps reduce the attack surface and enhances container security beyond what Seccomp profiles provide.

Previously, we examined Seccomp profiles in Kubernetes. Although Seccomp is effective at limiting the available syscalls for container operations, it does not manage access to specific resources such as files or directories. For example, a custom Seccomp profile can block the MKDIR syscall to prevent the creation of new directories.

Consider the following custom Seccomp profile that allows only a selected set of syscalls while denying all others (including MKDIR by default):

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
        "close",
        "brk"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

You can run a container with this Seccomp profile as shown below:

```bash theme={null}
docker run -it --security-opt seccomp=/root/custom.json docker/whalesay /bin/sh
```

Inside the container, if you try to create a directory:

```bash theme={null}
