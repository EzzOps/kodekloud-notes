# Demo Service Mesh

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Register-a-Service-Proxy/Demo-Service-Mesh/page

This guide details deploying a sample application on a HashiCorp Consul Service Mesh, securing communication between microservices with sidecar proxies and managing traffic.

In this guide, we’ll deploy a sample application on a HashiCorp Consul Service Mesh. You’ll use Consul Connect to secure communication between two microservices—**dashboard** and **counting**—each with its own sidecar proxy. Finally, you’ll control traffic using Consul **intentions**.

Based on the [HashiCorp Learn tutorial on Consul Service Mesh](https://learn.hashicorp.com/tutorials/consul/service-mesh), we assume you have a Consul cluster with two server nodes and two web servers. We’ll:

1. Enable Consul Connect for TLS encryption
2. Register counting and dashboard services
3. Launch services with sidecar proxies
4. Verify mutual TLS traffic
5. Manage service intentions

![The image shows a diagram of a service communication flow between a "Dashboard Service" and a "Counting Service," with ports and proxy symbols. It is part of a tutorial on the HashiCorp Learn website.](https://kodekloud.com/kk-media/image/upload/v1752877906/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/service-communication-flow-dashboard-counting.jpg)

## 1. Enable Consul Connect

First, activate Consul Connect on each server node so sidecar proxies can establish mutual TLS.

> **lightbulb** – Consul 1.7+ installed\
  – Systemd or another init system\
  – Network connectivity between nodes

Edit `/etc/consul.d/config.hcl` on **consul-node-a**:

```hcl theme={null}
