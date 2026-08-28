# Google Kubernetes Engine A Google Managed Service

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/High-Level-Overview/Google-Kubernetes-Engine-A-Google-Managed-Service/page

Google Kubernetes Engine is a fully managed service for deploying, scaling, and operating containerized applications on Google’s infrastructure.

Google Kubernetes Engine (GKE) is Google’s fully managed implementation of the open-source container orchestration platform [Kubernetes](https://kubernetes.io). It enables you to deploy, scale, and operate containerized applications on Google’s infrastructure, leveraging features that originated from Google’s internal cluster manager, Borg. For deeper insights into Borg, see Google’s [Borg research publication](https://research.google/pubs/pub43438/).

<Frame>
  ![The image features the Google Cloud Platform logo with a search bar displaying a URL, and icons labeled "GKE" and "Borg."](https://kodekloud.com/kk-media/image/upload/v1752875613/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/google-cloud-platform-logo-search-bar.jpg)
</Frame>

***

## The House-Building Analogy

To illustrate how GKE compares to managing Kubernetes yourself, picture building a house. You have two approaches:

1. **Option A: Hire Individual Trades**
2. **Option B: Hire a Builder**

<Frame>
  ![The image illustrates a simplified process of building a house, showing a house icon, building staff, and a builder manager.](https://kodekloud.com/kk-media/image/upload/v1752875615/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/house-building-process-icon-diagram.jpg)
</Frame>

### Option A: Manage Each Trade Yourself

Taking on each specialty—carpenters, electricians, plumbers—means you must:

* Select qualified trades and materials
* Coordinate schedules and handoffs
* Verify certifications and expertise
* Integrate all parts into a single, livable home

<Frame>
  ![The image is a slide titled "Option A: Individual," featuring a blue circle with an icon and text, alongside a list of criteria: Selection Criteria, Coordination, Expertise, and Integration.](https://kodekloud.com/kk-media/image/upload/v1752875616/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/option-a-individual-slide-criteria.jpg)
</Frame>

Managing each piece separately often becomes overwhelming and error-prone.

### Option B: Hire a Builder

A builder handles everything—sourcing, scheduling, quality control—so you only need to oversee the project outcome:

* Centralized selection and procurement
* Single point of contact for updates
* Accountability for trades and results
* Seamless assembly of all components

<Frame>
  ![The image is a presentation slide titled "Option B: Hiring a Builder," featuring a diagram with a circle labeled "Option B" and a list of benefits: Selection Criteria, Simplified Management, Expertise and Accountability, and Seamless Integration.](https://kodekloud.com/kk-media/image/upload/v1752875616/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/option-b-hiring-builder-diagram.jpg)
</Frame>

***

## Kubernetes vs. GKE

Working with upstream Kubernetes is like Option A: you provision the control plane, configure etcd, manage upgrades, scale nodes, and maintain high availability. GKE, on the other hand, is your dedicated builder:

<Frame>
  ![The image is an overview diagram of Google Cloud Platform's GKE (Google Kubernetes Engine), showing its integration with various services like Compute Engine, Load Balancer, Cloud Storage, and more.](https://kodekloud.com/kk-media/image/upload/v1752875619/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/gke-overview-diagram-google-cloud.jpg)
</Frame>

With GKE, Google handles:

* Control plane provisioning, upgrades, and patching
* Node auto-provisioning, autoscaling, and auto-repair
* Regional clusters with built-in high availability
* Security hardening (e.g., Shielded GKE Nodes)
* Native integration with Cloud Monitoring, Load Balancing, IAM, and more

This lets you focus on your workloads while GKE manages the infrastructure.

***

## When to Use GKE

Built on a decade of Borg experience, GKE delivers production-ready defaults and managed services for your applications:

<Frame>
  ![The image is an infographic titled "When to Use GKE?" showing four benefits of using Google Kubernetes Engine: Selection Criteria, Simplified Management, Expertise and Accountability, and Seamless Integration.](https://kodekloud.com/kk-media/image/upload/v1752875621/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/when-to-use-gke-infographic.jpg)
</Frame>

| Use Case                  | Benefit                                                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Production-Hardened Plane | Google maintains your control plane with version upgrades, security patches, and an SLA-backed uptime guarantee. |
| Node Management           | Automatic provisioning, scaling, and self-healing for worker nodes.                                              |
| Reliability & Expertise   | Regional clusters and Google’s global network offer high availability and low latency worldwide.                 |
| Service Integration       | Deep connectivity with Artifact Registry, Cloud Monitoring & Logging, VPC, and IAM.                              |

<Callout icon="lightbulb">
  GKE supports Container-Optimized OS (COS), Ubuntu, and Bottlerocket node images for enhanced security and performance.
</Callout>

***

## Key GKE Features & Benefits

GKE enhances open-source Kubernetes with managed services that accelerate development and simplify operations:

<Frame>
  ![The image is a diagram listing the benefits of a service, including managed Kubernetes clusters, autoscaling, load balancing, logging and monitoring, and integration. It features a GKE icon and stars highlighting certain points.](https://kodekloud.com/kk-media/image/upload/v1752875623/notes-assets/images/GKE-Google-Kubernetes-Engine-Google-Kubernetes-Engine-A-Google-Managed-Service/kubernetes-benefits-diagram-gke-icon.jpg)
</Frame>

| Feature                | Description                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| Fully Managed Clusters | Google manages control plane, nodes, networking, storage, and upgrades                           |
| Autoscaling            | Cluster and Horizontal Pod Autoscaling automatically adjust resources to meet demand             |
| Load Balancing         | Built-in HTTP(S), TCP/SSL, and internal load balancing for high availability                     |
| Observability          | Integrated Cloud Monitoring, Logging, Debugger, and Trace for real-time insights                 |
| Ecosystem Integration  | Seamless connectivity to Cloud SQL, Cloud Storage, BigQuery, and the full Google Cloud portfolio |

GKE is the ideal choice when you want the power of Kubernetes without the overhead of managing control planes, node lifecycles, and production-grade integrations.

***

## Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Google Kubernetes Engine Documentation](https://cloud.google.com/kubernetes-engine/docs)
* [Terraform Registry: Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
* [Google Cloud Platform](https://cloud.google.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/f43dc1c8-e09e-496b-bd15-160434440a1d/lesson/f0fbc2fb-b7a8-40fc-9050-312fa669697b" />
</CardGroup>
