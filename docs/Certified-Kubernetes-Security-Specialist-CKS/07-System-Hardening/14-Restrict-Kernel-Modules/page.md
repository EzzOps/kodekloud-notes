# Restrict Kernel Modules

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/Restrict-Kernel-Modules/page

This guide explains how to restrict specific Linux kernel modules to enhance system security.

In this guide, you'll learn how to restrict the use of specific Linux kernel modules to improve the security of your system. The Linux kernel follows a modular design, making it easy to extend its capabilities dynamically. For example, when new hardware is connected, the kernel automatically or manually loads the necessary module—using tools such as modprobe or insmod—to enable device support (e.g., video card drivers).

## Loading and Listing Kernel Modules

Kernel modules are loaded as required, either manually by a system administrator or automatically by the kernel. For instance, to load the PC Speaker module manually, execute the following command as the root user:

```bash theme={null}
modprobe pcspkr
```

After loading modules, you can list all active modules using:

```bash theme={null}
lsmod
```

A typical output from the `lsmod` command might resemble:

```bash theme={null}
