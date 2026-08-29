# 1. Install kubectl
gcloud components install kubectl

# 2. Verify the client version
kubectl version --client

# 3. Install GKE auth plugin
gcloud components install gke-gcloud-auth-plugin

# 4. Check plugin version
gke-gcloud-auth-plugin --version

# 5. Fetch cluster credentials
gcloud container clusters get-credentials CLUSTER_NAME \
  --region COMPUTE_REGION
```

> **lightbulb** If you’re using Google Cloud Shell, both `kubectl` and the GKE auth plugin are pre-installed.

## Organizing clusters with GKE labels

GKE labels are user-defined key–value pairs attached to clusters and node pools. Unlike Kubernetes resource labels, these labels serve metadata purposes such as billing, grouping, and cost tracking.

![The image illustrates the use of GKE labels to organize clusters, showing a series of hexagonal icons with a label indicating key-value pairs.](https://kodekloud.com/kk-media/image/upload/v1752875574/notes-assets/images/GKE-Google-Kubernetes-Engine-Prepare-the-cluster-for-accessibility-and-management/gke-labels-cluster-organization-diagram.jpg)

Although cluster labels and Kubernetes pod labels are conceptually similar, they do not inherit from one another. They function independently to help you filter and manage Google Cloud resources.

![The image illustrates how GKE labels can be used to organize clusters, showing examples with GKE and Kubernetes, and highlighting the use of arbitrary metadata for grouping and filtering.](https://kodekloud.com/kk-media/image/upload/v1752875576/notes-assets/images/GKE-Google-Kubernetes-Engine-Prepare-the-cluster-for-accessibility-and-management/gke-labels-clusters-organization-diagram.jpg)

### Common use cases for cluster labels

![The image is a diagram titled "Cluster Labels – Common Use Cases," listing various types of cluster labels such as team/cost center, component, environment or stage, state, and billing breakdown. It includes a section labeled "Guidelines" with icons and a star.](https://kodekloud.com/kk-media/image/upload/v1752875577/notes-assets/images/GKE-Google-Kubernetes-Engine-Prepare-the-cluster-for-accessibility-and-management/cluster-labels-use-cases-diagram.jpg)

| Use Case            | Description                                | Example Label       |
| ------------------- | ------------------------------------------ | ------------------- |
| Team or cost center | Assign ownership for budgeting and billing | `team=research`     |
| Component           | Identify hosted services                   | `component=ingress` |
| Environment/stage   | Differentiate deployment lifecycle         | `environment=prod`  |
| State               | Track resource lifecycle status            | `state=active`      |
| Billing breakdown   | Allocate costs across departments          | `billing=marketing` |

> **triangle-alert** Avoid creating high-cardinality labels (e.g., timestamp-based) to prevent label sprawl and maintain efficient resource filtering.

## Controlling access with GKE tags

Google Cloud tags are another form of key–value metadata that apply across all GCP resources, including GKE clusters. By combining tags with IAM policies, you can enforce conditional access and uniform security configurations.

* Define tags on clusters (for example, `env=prod`, `env=dev`).
* Reference those tags in IAM policies to grant or restrict roles.
* Maintain consistent access controls and simplify policy management.

![The image is a slide titled "Tags in GKE" featuring the Google Cloud logo and icons representing security policy enforcement, access control management, and resource organization.](https://kodekloud.com/kk-media/image/upload/v1752875578/notes-assets/images/GKE-Google-Kubernetes-Engine-Prepare-the-cluster-for-accessibility-and-management/tags-in-gke-google-cloud-icons.jpg)

## Links and References

* [Kubernetes kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
* [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
* [GCP Resource Manager Tags Overview](https://cloud.google.com/resource-manager/docs/tags-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/897349c1-bf57-4c08-82fb-0aa0ce0e0f6b/lesson/6cab061b-9e10-4bf7-8e03-d078ac5859aa)


# Section Introduction

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/GKE-Deployment-and-Administration/Section-Introduction/page

This guide covers deploying and managing Google Kubernetes Engine, including cluster modes, management, scaling, upgrading, and monitoring with hands-on labs.

Welcome to this comprehensive guide on deploying and managing Google Kubernetes Engine (GKE). Whether you’re new to Kubernetes or looking to optimize your existing clusters, this lesson covers:

* GKE cluster modes of operation
* Cluster accessibility and management
* Scaling and upgrading strategies
* Monitoring and logging with Cloud Operations

We’ll also walk through hands-on lab activities so you can apply these concepts in real time.

![The image is a slide titled "GKE Deployment and Administration," listing topics such as GKE modes of operation, cluster preparation, scaling, upgrading, and monitoring.](https://kodekloud.com/kk-media/image/upload/v1752875579/notes-assets/images/GKE-Google-Kubernetes-Engine-Section-Introduction/gke-deployment-administration-topics-slide.jpg)

## What You’ll Learn

| Topic                  | Description                                                                    |
| ---------------------- | ------------------------------------------------------------------------------ |
| GKE Modes of Operation | Compare Autopilot, Standard, and private clusters                              |
| Cluster Preparation    | Configure networking, IAM, and security                                        |
| Scaling & Upgrades     | Implement cluster autoscaling, node auto-provisioning, and version upgrades    |
| Monitoring & Logging   | Leverage Cloud Operations to monitor, alert, and visualize cluster performance |
| Hands-On Labs          | Create clusters, install `kubectl`, and apply labels/tags                      |

> **lightbulb** GKE combines Google’s infrastructure with open-source Kubernetes, enabling you to focus on applications rather than managing control planes.\
  Learn more in the [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs).

### Detailed Topics

1. **GKE Cluster Modes of Operation**\
   Explore the differences between Standard, Autopilot, and Private clusters, and determine which mode aligns with your organizational needs.

2. **Preparing Your Cluster**
   * Configure networking (VPC, firewall rules)
   * Set up IAM roles and policies
   * Enable private endpoint and master authorized networks

3. **Scaling and Upgrading**
   * Cluster Autoscaling
   * Node Auto-Provisioning
   * Rolling and surge upgrades for both clusters and node pools

4. **Monitoring and Logging**\
   Integrate with the [Cloud Operations suite](https://cloud.google.com/products/operations) to track metrics, set alerts, and visualize logs.

![The image is a slide titled "GKE Deployment and Administration" with a list of lab tasks: creating a GKE cluster, installing kubectl, and applying labels and tags to GKE clusters.](https://kodekloud.com/kk-media/image/upload/v1752875580/notes-assets/images/GKE-Google-Kubernetes-Engine-Section-Introduction/gke-deployment-administration-lab-tasks.jpg)

## Hands-On Lab Exercises

1. **Create a GKE Cluster**
   ```bash theme={null}
   gcloud container clusters create my-gke-cluster \
     --zone us-central1-c \
     --machine-type n1-standard-1
   ```
2. **Install kubectl**
   ```bash theme={null}
   gcloud components install kubectl
   ```
3. **Apply Labels and Tags**
   ```bash theme={null}
   kubectl label nodes <NODE_NAME> environment=production
   gcloud compute instances add-tags <INSTANCE_NAME> --tags=k8s-node
   ```

By the end of this lesson, you’ll have a well-architected GKE environment and the skills to maintain it at scale. Let’s get started!

- [Watch Video](https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/897349c1-bf57-4c08-82fb-0aa0ce0e0f6b/lesson/7053d6df-c45e-4373-87d2-67a710a8a387)
