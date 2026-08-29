# Authenticate with GCP
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Create a GKE cluster in us-central1-a
gcloud container clusters create my-cluster \
  --zone us-central1-a \
  --machine-type e2-medium \
  --num-nodes 3

# Retrieve cluster credentials for kubectl
gcloud container clusters get-credentials my-cluster \
  --zone us-central1-a

# Verify node status
kubectl get nodes
```

> **lightbulb** Always run `gcloud container clusters get-credentials` before executing `kubectl` commands. This ensures your CLI is pointed to the correct cluster endpoint.

***

## Key Takeaways

* Defining sprint tasks is just the starting point; dive into related subtasks (e.g., authentication, IAM) for a deeper understanding.
* Hands-on practice with `gcloud` and `kubectl` cements your GKE workflow.
* Validating cluster connectivity early prevents common deployment headaches.

***

## Next Steps: Sprint 03 Preview

In Sprint 03, we will:

* Deploy a sample application using a Kubernetes Deployment and Service.
* Scale workloads with the Horizontal Pod Autoscaler.
* Perform rolling updates to achieve zero-downtime releases.

***

## Links and References

* [Google Cloud Platform](https://cloud.google.com)
* [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
* [kubectl CLI Reference](https://kubernetes.io/docs/reference/kubectl/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/e0cc2e03-d889-468c-af73-0866856711aa/lesson/c288f12c-b0df-4db6-be57-036549e0b3c8)


# Sprint 02

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-02/Sprint-02/page

This article focuses on setting up Google Cloud infrastructure and launching a Kubernetes cluster in Sprint 02.

In Sprint 02, we'll focus on establishing your Google Cloud infrastructure and launching your first Kubernetes cluster. By the end of this sprint, you’ll be ready to deploy containerized applications on GKE.

## Sprint Objectives

| Objective              | Outcome                                                        |
| ---------------------- | -------------------------------------------------------------- |
| Create a GCP account   | Set up your Google Cloud identity, billing, and permissions.   |
| Learn GKE fundamentals | Explore pods, services, deployments, and cluster components.   |
| Set up a GKE cluster   | Provision a multi-node cluster using Google Kubernetes Engine. |

![The image lists sprint goals, including creating a GCP account, understanding GKE fundamentals in GCP, and setting up a GKE cluster.](https://kodekloud.com/kk-media/image/upload/v1752875451/notes-assets/images/GCP-DevOps-Project-Sprint-02/sprint-goals-gcp-gke-cluster.jpg)

> **lightbulb** Feel free to share any questions or suggest additional tasks now. This helps the team refine the sprint plan and provide targeted guidance.

That’s all for Sprint 02! In the next lesson, we'll dive into creating your GCP account and configuring the Cloud Console.

## Links and References

* [GCP Free Tier Signup](https://cloud.google.com/free)
* [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/e0cc2e03-d889-468c-af73-0866856711aa/lesson/5ae5d112-3915-4970-bd29-ef19bb0951cf)
