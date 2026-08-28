# Networking in Kubernetes

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Networking-in-Kubernetes/page

This guide covers core concepts of Kubernetes networking, including IP assignment, CNI plugins, and cluster-wide virtual networks.

In this guide, you’ll learn the core concepts of Kubernetes networking—from a single-node setup to a multi-node cluster. We’ll cover how Pods receive IP addresses, why a Container Network Interface (CNI) plugin is required, and how Kubernetes builds a cluster-wide virtual network.

## Single-Node Cluster Networking

On a single-node cluster, the Kubernetes node itself has an IP address (e.g., `192.168.1.2`). You use this address to SSH into the host or connect to the API server. However, each Pod you create is allocated its own IP from a private Pod network—by default, something like `10.244.0.0/16`.

```yaml theme={null}
