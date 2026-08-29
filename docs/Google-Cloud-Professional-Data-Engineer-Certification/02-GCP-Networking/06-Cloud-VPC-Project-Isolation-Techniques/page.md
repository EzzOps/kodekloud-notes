# Example static route for restricted.googleapis.com
Destination: 199.36.153.4/30
Next hop: private gateway (Private Service Connect / Private Google Access)
```

## Quick reference table

| Concept                       |                                           Purpose | Example / Note                                                            |
| ----------------------------- | ------------------------------------------------: | ------------------------------------------------------------------------- |
| Service perimeter             |         Enforce security boundary around projects | See [VPC Service Controls](https://cloud.google.com/vpc-service-controls) |
| Authorized VPC / VM           |                  Workload source inside perimeter | Compute Engine VM in authorized project                                   |
| Restricted endpoint           |          Private API access inside Google network | `restricted.googleapis.com`                                               |
| Static route                  | Route restricted endpoint through private gateway | `199.36.153.4/30`                                                         |
| Private Service Connect (PSC) |          Expose/consume services via internal IPs | Consumer creates PSC endpoint attached to producer service                |
| Service attachment            |   Producer-side resource representing the service | Allows private access without public IPs                                  |

> **lightbulb** Private Service Connect gives workloads a private, controlled path to Google APIs and partner services using internal IPs and service attachments—keeping traffic on Google’s network and off the public internet.

## Links and references

* [Private Service Connect (PSC)](https://cloud.google.com/vpc/docs/private-service-connect)
* [Private Google Access and restricted.googleapis.com](https://cloud.google.com/vpc/docs/private-google-access)
* [VPC Service Controls (service perimeter)](https://cloud.google.com/vpc-service-controls)
* [Compute Engine](https://cloud.google.com/compute)
* [Cloud Storage](https://cloud.google.com/storage)
* [BigQuery](https://cloud.google.com/bigquery)

## Recap

* PSC provides private connectivity to Google-managed and partner services without public IPs.
* It uses a consumer–producer model with service attachments and internal IP endpoints.
* Traffic remains on Google’s backbone and can be restricted by service perimeters for added security.

That’s it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/f353b708-8681-4fc6-851f-6adae7889f8e)


# Cloud VPC Project Isolation Techniques

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-VPC-Project-Isolation-Techniques/page

Guide to GCP project isolation strategies comparing Shared VPC and separate VPCs, and explaining IAM, firewall controls and connectivity options to secure multi-project networks.

Welcome. In this lesson we cover practical VPC project isolation techniques in Google Cloud (GCP) and why they matter for data engineers. If you manage many GCP projects, clear isolation patterns simplify troubleshooting, reduce blast radius, and make it easier to enforce security and compliance at scale.

This article explains the two common isolation approaches, how the GCP project boundary contributes to isolation, and how firewall and IAM policies provide additional, powerful controls. Finally, you’ll find guidance on connectivity options when projects must exchange data.

## Isolation models: Shared VPC vs Separate VPCs

There are two primary approaches organizations adopt for VPC networking in multi-project environments:

* Shared VPC\
  A single centrally managed VPC lives in a host project, and other projects (service projects) attach to subnets in that host. Think of this as an apartment building: projects get their own space but share plumbing, routing, and network policy. Shared VPC is ideal when you want centralized routing, consistent subnet design, and centralized enforcement of firewall/NAT policies.

* Separate VPC per project\
  Each project has its own VPC network and is managed independently—like separate houses. This model gives stronger isolation between teams or environments and is preferred when compliance, auditing, or strict separation of duties is required. Connectivity between separate VPCs must be explicitly established (VPC Peering, Cloud VPN, Cloud Interconnect, or Private Service Connect).

As a practical rule of thumb:

* Choose Shared VPC for centralized control, consistent policy, and simplified network operations.
* Choose separate VPCs when you need strict project-level isolation and a reduced blast radius.

## Quick comparison

|                       Feature |            Shared VPC            |          Separate VPC per Project          |
| ----------------------------: | :------------------------------: | :----------------------------------------: |
|     Centralized routing & NAT |                Yes               |                     No                     |
|       Central firewall policy |                Yes               |              No (per-network)              |
|        Blast radius isolation |               Lower              |                   Higher                   |
| Ease of cross-project routing |               High               | Requires explicit peering/VPN/Interconnect |
|              Typical use case | Central infra & managed services |     Isolated teams, regulated workloads    |

## Project boundary: the first and strongest isolation layer

By default, each GCP project gets its own logical isolation (including resource quotas, billing, IAM scoping, and VPCs—a default network may be created unless auto-create is disabled). Use the project boundary as your primary partitioning mechanism to limit the impact of misconfigurations and to organize costs and permissions.

<Frame>
  <img alt="A presentation slide titled &#x22;Cloud VPC – Project Isolation Techniques&#x22; showing &#x22;Project as a Boundary&#x22; with two key points: each GCP project has its own isolated VPC by default, and projects provide separation of billing, IAM policies, and quotas. The slide is branded © KodeKloud." />
</Frame>

> **lightbulb** Treat the project boundary as your primary isolation mechanism: it separates network, billing, IAM, and quotas. Use folders and organization policies to group and consistently govern projects.

Practical recommendations:

* Use folders and organization policies to enforce naming, labels, and network creation rules (for example, disable auto-create network for new projects).
* Map environments to projects (e.g., prod, staging, dev) and allocate quotas and billing accordingly to reduce accidental cross-impact.
* Apply least-privilege IAM at the project or folder level to reduce administrative risk.

## Firewall and IAM boundaries: enforce segmentation and access control

Two additional, essential layers of isolation are firewall rules (network-level) and IAM (identity-level):

* Firewall rules\
  GCP firewall rules are stateful and applied per VPC. They are evaluated by priority and can be targeted using instance tags or service accounts. In Shared VPC setups, rules in the host network determine allowed traffic for all attached service projects. For strict segmentation, use deny rules, non-overlapping subnet ranges, and carefully ordered priorities.

* IAM boundaries\
  IAM controls who can administer or access resources. Apply IAM at the organization, folder, or project level to prevent unauthorized cross-project access. Shared VPC requires specific roles (for example, `roles/compute.networkAdmin` and `roles/compute.networkUser`) so service projects can attach resources to host project subnets without granting broader network admin privileges. Enforce least privilege and prefer role binding at folder-level when possible to scale securely.

Together, firewall rules and IAM form complementary controls: firewall enforces traffic-level policies, while IAM enforces who can change or consume resources.

<Frame>
  <img alt="A presentation slide titled &#x22;Cloud VPC – Project Isolation Techniques&#x22; about firewall and IAM boundaries in GCP. It lists two recommendations: enforce project-specific firewall rules and apply IAM at the project or folder level to restrict cross-project access." />
</Frame>

## Connectivity options when projects must communicate

When you need controlled connectivity between projects, choose from these explicit options and combine them with firewall + IAM controls:

* Shared VPC — central network with host/project attachment
* VPC Peering — low-latency private connectivity, but no transitive peering
* Cloud VPN — encrypted IPsec tunnels for cross-region or cross-cloud links
* Cloud Interconnect — high-throughput, low-latency private connections for on-prem to GCP
* Private Service Connect — privately access-managed services across projects

> **warning** When connecting VPCs, explicitly plan routing, firewall rules, and IAM. Misconfigured routes or overly permissive firewall rules can inadvertently bypass project isolation.

Practical tips for connectivity:

* Use non-overlapping CIDR blocks to avoid routing conflicts.
* Prefer Shared VPC when many teams need consistent access to central services (DNS, NAT, logging).
* With VPC Peering, remember that it is non-transitive: plan a hub-and-spoke or use Shared VPC for transitive requirements.
* Validate firewall rules at both ingress and egress directions and confirm that service accounts/tags used for scoping are applied consistently.

## Summary / Best practices

* Treat the project as your primary isolation boundary for billing, IAM, quotas, and the default network.
* Use Shared VPC for centralized network management and consistent policies; use separate VPCs for strict isolation and compliance.
* Combine IAM and firewall rules to enforce both administrative and traffic-level separation.
* When you connect projects, choose the right connectivity mechanism (Shared VPC, peering, VPN, interconnect, or Private Service Connect) and harden routing and firewall rules.

Further reading:

* [VPC Network Overview (Google Cloud)](https://cloud.google.com/vpc/docs)
* [Shared VPC (Google Cloud)](https://cloud.google.com/vpc/docs/shared-vpc)
* [VPC Network Peering (Google Cloud)](https://cloud.google.com/vpc/docs/vpc-peering)

That is it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/dea9e6fb-a581-4015-857c-fe2829665b54)
