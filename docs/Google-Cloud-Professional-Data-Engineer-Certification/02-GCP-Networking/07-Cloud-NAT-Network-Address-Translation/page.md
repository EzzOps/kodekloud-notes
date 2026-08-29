# Cloud NAT Network Address Translation

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-NAT-Network-Address-Translation/page

Explains Google Cloud NAT, a managed service that enables outbound internet access for private VMs without external IPs, preserving privacy, scalability, and centralized egress control.

Welcome back. In this article we explain Cloud NAT (Cloud Network Address Translation) for Google Cloud: what it is, how it works, and why it matters for engineers who run private workloads that still need outbound internet access.

TL;DR: Cloud NAT lets private GCP resources initiate outbound connections to the internet without assigning public IPs to each instance. It’s a managed, scalable NAT service that preserves private IP address privacy while enabling outbound-only connectivity.

To visualize this, imagine the public internet on the left, a Cloud NAT gateway in the middle acting as the translator, and a group of VM instances with only private IPs on the right. When these private instances need to download updates or call external APIs, Cloud NAT translates their internal IPs to one or more public IPs for outbound traffic. This keeps your machines private while still allowing them to initiate connections to external services.

<Frame>
  <img alt="A slide titled &#x22;Cloud Network Address Translation (NAT)&#x22; with two cartoon user icons and speech bubbles, one asking &#x22;What is the purpose of Cloud NAT?&#x22; The other bubble answers that Cloud NAT &#x22;allows private GCP resources to access the internet securely with outbound-only connectivity.&#x22;" />
</Frame>

Overview

* What is Cloud NAT?\
  Cloud NAT is a managed Network Address Translation service in Google Cloud that provides outbound-only internet access for resources with only private/internal IP addresses. It translates private source IPs and ephemeral ports to one or more public IP addresses for outbound connections.

* How Cloud NAT operates (high level)\
  Private VMs keep internal IP addresses; when they initiate outbound connections, Cloud NAT maps those internal addresses and ports to one or more external IP addresses and ports, maintaining state so return traffic for those established connections is routed back to the correct instance. Cloud NAT is managed and scales automatically — you do not need to maintain NAT VM instances or assign external IPs to every VM.

* Key use cases
  * Private VMs that must download OS/package updates or access external APIs.
  * Batch or pipeline compute that must reach internet services without exposing instances to inbound connections.
  * Controlled egress from private networks in multi-cloud and hybrid deployments.

> **lightbulb** Cloud NAT provides outbound-only access for private resources. It is not a firewall and does not permit unsolicited inbound connections to your VMs.

How Cloud NAT differs from alternatives

| Option                       | Description                                                                    | When to use                                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Cloud NAT                    | Managed NAT service for outbound-only traffic; no external IPs on VMs required | Private VMs that need web access or to call APIs while remaining unaddressable from the internet |
| External IP per VM           | Assigns public IP directly to each VM                                          | Small fleets or cases where inbound connectivity is required                                     |
| NAT instances (self-managed) | You run and maintain NAT VMs or load balancers                                 | Legacy setups or when you need custom NAT behavior not provided by Cloud NAT                     |

Benefits

| Benefit            | Why it matters                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------- |
| Security           | Keeps internal IPs private, reducing attack surface; no inbound connections permitted via NAT |
| Simplicity         | No per-VM external IPs or NAT servers to manage                                               |
| Scalability        | Google-managed scaling for NAT mappings and ephemeral ports                                   |
| Centralized egress | Easier firewall rules, logging, and IP allowlisting for external services                     |

Quick example: Provisioning Cloud NAT with gcloud

Below is a compact example of the typical workflow: create a Cloud Router, reserve an external IP (optional), and create the NAT configuration.

1. Create a Cloud Router (required for Cloud NAT):

```bash theme={null}
gcloud compute routers create nat-router \
  --network=default \
  --region=us-central1
```

2. Optionally reserve a static external IP address:

```bash theme={null}
gcloud compute addresses create nat-ip-1 --region=us-central1
```

3. Create a NAT configuration that uses the router (this example uses all subnet ranges):

```bash theme={null}
gcloud compute routers nats create nat-config \
  --router=nat-router \
  --region=us-central1 \
  --nat-all-subnet-ip-ranges \
  --nat-external-ip-pool=nat-ip-1 \
  --enable-logging
```

Notes about the commands:

* You can provide multiple static IP addresses or let Cloud NAT use ephemeral IPs.
* Use `--nat-custom-subnet-ip-ranges` when you want to target specific subnet ranges only.

Design considerations and best practices

* Port exhaustion: Cloud NAT uses ephemeral ports for translations. For very high connection densities (many simultaneous outbound connections per VM), monitor and provision sufficient external IP addresses or use multiple NAT IPs to increase available port space.
* Logging: Enable Cloud NAT logging for egress flow visibility via Cloud Logging. This helps with troubleshooting and auditing egress traffic.
* Private Google Access vs Cloud NAT: If workloads require access to Google APIs without external IPs, consider enabling Private Google Access where appropriate; Cloud NAT covers general internet egress.
* Firewall rules: Because Cloud NAT is outbound-only, you should still configure VPC firewall rules to control inbound access from other networks and to limit egress where appropriate.

> **warning** Cloud NAT does not permit unsolicited inbound connections. If your application requires inbound connectivity, assign external IPs or use an appropriate load balancer with controlled ingress.

Why data engineers should care

* Package and dependency access: Build agents, pipelines, and data processing jobs often need to pull packages or container images from public repositories. Cloud NAT enables that without exposing the compute nodes.
* Secure integration: When integrating with external APIs, centralizing egress via Cloud NAT simplifies allowlisting and auditing of outbound IPs.
* Hybrid and multi-cloud scenarios: Cloud NAT complements VPN/Interconnect setups by handling internet egress for private subnets in a managed way.

Common FAQ

* Can Cloud NAT handle inbound traffic to private VMs?\
  No — Cloud NAT only provides outbound translation. Inbound connections must be handled via external IPs, load balancers, or VPN/interconnect paths.

* How many public IPs should I allocate?\
  It depends on concurrency and port requirements. If you expect large numbers of simultaneous outbound connections, allocate multiple external IPs to increase available ephemeral ports.

* Is Cloud NAT billed?\
  Cloud NAT has pricing for NAT gateway resources and data processing. Check the official pricing page for up-to-date details.

Links and references

* [Cloud NAT documentation (Google Cloud)](https://cloud.google.com/nat)
* [Cloud Router documentation](https://cloud.google.com/network-connectivity/docs/router)
* [Private Google Access](https://cloud.google.com/vpc/docs/configure-private-google-access)

That covers the essentials of Cloud NAT: why it exists, how it works at a high level, and why it’s useful—especially for data engineers running private pipelines in GCP. Thanks for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/894d0751-ec2c-4ccd-a16e-ede75e6262aa)
