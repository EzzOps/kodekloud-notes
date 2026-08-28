# Observability Falco Overview and Installation

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Observability-Falco-Overview-and-Installation/page

This guide explains how to install Falco for threat detection in Kubernetes environments using different deployment methods.

In this guide, you’ll learn how to install Falco to enhance threat detection and analysis in your Kubernetes environment. Falco is an open-source runtime security tool that inspects system calls from user-space applications, applying customizable rules to identify suspicious behavior.

## How Falco Works

Falco captures kernel events via two primary methods, then filters them through its policy engine:

| Capture Method | Description                                                                | Pros & Cons                                                                                |
| -------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Kernel Module  | Inserts a module into the Linux kernel to intercept syscalls.              | **Pros:** High performance<br />**Cons:** Intrusive; may be restricted on managed clusters |
| eBPF           | Uses Extended Berkeley Packet Filter to attach probes to kernel functions. | **Pros:** Safer, non-intrusive<br />**Cons:** Slightly higher overhead                     |

Once captured, events flow through Falco’s user-space components—including Sysdig libraries and the Falco policy engine—where they’re evaluated against rules. Alerts can be forwarded to syslog, standard output, Slack, email, and other sinks.

<Frame>
  ![The image is a diagram of Falco's architecture, showing the interaction between applications, syscalls, the Falco kernel module, eBPF, and components like the policy engine, libraries, and Falco rules, leading to output.](https://kodekloud.com/kk-media/image/upload/v1752880892/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Observability-Falco-Overview-and-Installation/falco-architecture-diagram-syscalls.jpg)
</Frame>

## Installation Methods

You have two common ways to deploy Falco, depending on your access level and platform restrictions:

| Method                        | Use Case                                    | Advantages                                        |
| ----------------------------- | ------------------------------------------- | ------------------------------------------------- |
| Native Linux Installation     | Full root access to a Linux node            | Isolated from Kubernetes control plane            |
| Kubernetes DaemonSet via Helm | Managed clusters or restricted environments | Easy upgrades and centralized management via Helm |

### Installing Falco on a Linux Node

Use this approach if you can install packages and kernel modules directly on your host. It ensures Falco remains operational even if your Kubernetes control plane is compromised.

<Callout icon="triangle-alert">
  Ensure you have the correct `linux-headers-$(uname -r)` package. Mismatched headers can prevent the Falco kernel module from building.
</Callout>

```bash theme={null}
