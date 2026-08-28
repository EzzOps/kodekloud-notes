# Cilium Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Container-Network-InterfaceCNI/Cilium-Overview/page

This article provides an overview of Cilium, a Container Network Interface solution for Kubernetes, focusing on its features, architecture, and use cases.

In this lesson, we’ll dive into **Cilium**, the Container Network Interface (CNI) solution used throughout this course. Developed by Isovalent, Cilium is available as an open source edition and a paid subscription. We’ll focus on the open source version.

<Frame>
  ![The image explains Cilium as a CNI solution for Kubernetes, developed by Isovalent, with options for open-source and paid subscription versions.](https://kodekloud.com/kk-media/image/upload/v1752880252/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Overview/cilium-cni-solution-kubernetes-isovalent.jpg)
</Frame>

## CNCF Project and Adoption

Cilium is part of the Cloud Native Computing Foundation landscape. Originally released in 2015, it has seen rapid adoption—boasting nearly 20,000 stars on GitHub as of this recording.

<Frame>
  ![The image is a slide titled "Understanding Cilium" featuring the Cloud Native Computing Foundation logo, with icons representing a timeline from 2015 and a GitHub milestone of 20K.](https://kodekloud.com/kk-media/image/upload/v1752880253/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Overview/understanding-cilium-timeline-github-milestone.jpg)
</Frame>

## Unified Networking, Observability & Security

Cilium delivers a single platform for:

* Networking
* Observability
* Security

<Frame>
  ![The image is a slide titled "Understanding Cilium," featuring two sections labeled "Networking" and "Observability" under the category "Solution."](https://kodekloud.com/kk-media/image/upload/v1752880254/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Overview/understanding-cilium-networking-observability.jpg)
</Frame>

Additionally, Cilium can function as:

* A service mesh
* A load balancer between services
* An encryption provider

Its flexibility and advanced capabilities make it ideal for modern cloud-native deployments.

## How Cilium Works

At its core, Cilium leverages eBPF to implement a high-performance, Layer 3 network that is protocol-aware at Layer 7. It can replace kube-proxy and enforce network policies at Layers 3, 4, and 7.

<Frame>
  ![The image is a diagram explaining how Cilium works, highlighting its components like service mesh, observability, networking, and runtime security, along with integrations with platforms like Kubernetes, AWS, and Google Cloud.](https://kodekloud.com/kk-media/image/upload/v1752880255/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Overview/cilium-architecture-diagram-service-mesh.jpg)
</Frame>

<Callout icon="lightbulb">
  By using eBPF, Cilium achieves features like bandwidth management and fine-grained policy enforcement without kernel modifications.
</Callout>

## eBPF Overview

[eBPF][ebpf-io] (Extended Berkeley Packet Filter) is a Linux kernel technology that allows sandboxed programs to run safely in kernel space. Developers can inject custom logic at runtime—without adding kernel modules or changing kernel source code.

| Use Case                    | Description                                      |
| --------------------------- | ------------------------------------------------ |
| High-performance networking | Packet processing directly in the kernel         |
| Load balancing              | Efficient traffic distribution                   |
| Security enforcement        | Stateful firewalls and IDS                       |
| Packet filtering            | Fine-grained packet selection                    |
| Profiling & tracing         | In-kernel observability and performance insights |

<Frame>
  ![The image is a diagram illustrating the eBPF ecosystem, showing its use cases in networking, security, and observability, with components in user space and kernel space. It includes projects, SDKs, and kernel runtime elements, highlighting applications like tracing, profiling, and monitoring.](https://kodekloud.com/kk-media/image/upload/v1752880257/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Overview/ebpf-ecosystem-diagram-use-cases.jpg)
</Frame>

## Cilium Agent

On every Kubernetes node, a **Cilium agent** manages the eBPF programs that handle container networking, security policies, and observability hooks.

## Hubble: Observability & Security

Hubble is a distributed networking and security observability platform built on Cilium and eBPF. It provides visibility into:

* Pod-to-pod communications
* Service dependency maps
* Security events
* Multi-cluster traffic flows

<Frame>
  ![The image features a colorful illustration of a satellite and text that reads "Hubble" with a description stating it facilitates distributed networking and security observability.](https://kodekloud.com/kk-media/image/upload/v1752880258/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Overview/hubble-satellite-distributed-networking-illustration.jpg)
</Frame>

<Callout icon="triangle-alert">
  Enabling Hubble in production requires careful consideration of resource usage and data retention policies.
</Callout>

## Advanced Network Policies

Cilium supports both Layer 3/4 and Layer 7 policies, using workload identities derived from Kubernetes labels instead of IP addresses:

| Layer | Controls                        | Protocols         |
| ----- | ------------------------------- | ----------------- |
| 3 & 4 | IP, CIDR, port-based allow/deny | TCP, UDP, ICMP    |
| 7     | API-aware filtering and routing | HTTP, gRPC, Kafka |

## Next Steps

Having covered Cilium’s architecture and components, the next step is to install and configure it in your Kubernetes cluster. Follow the [Cilium Documentation][cilium-docs] for setup instructions and best practices.

***

## Links and References

* [Cilium Documentation][cilium-docs]
* [eBPF][ebpf-io]
* [Cloud Native Computing Foundation (CNCF)][cncf]
* [Hubble Overview][hubble-docs]

[ebpf-io]: https://ebpf.io/

[cilium-docs]: https://docs.cilium.io/

[cncf]: https://www.cncf.io/

[hubble-docs]: https://docs.cilium.io/projects/hubble/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5eea49e6-caea-4e84-88a0-268ea6f263af/lesson/16d13766-3dd4-4322-87d5-ec9303a4583f" />
</CardGroup>
