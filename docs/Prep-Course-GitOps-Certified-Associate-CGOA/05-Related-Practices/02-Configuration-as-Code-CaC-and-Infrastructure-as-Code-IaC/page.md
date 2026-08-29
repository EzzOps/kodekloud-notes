# Configuration as Code CaC and Infrastructure as Code IaC

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Related-Practices/Configuration-as-Code-CaC-and-Infrastructure-as-Code-IaC/page

Explains how Infrastructure as Code and Configuration as Code complement each other in a GitOps workflow, covering definitions, differences, tools, and deployment patterns using Git.

This lesson explains how Infrastructure-as-Code (IaC) and Configuration-as-Code (CaC) relate and how they cooperate in a GitOps workflow. We'll cover definitions, differences, recommended tools, and a practical GitOps pattern for deploying infrastructure and application configurations from Git.

```bash theme={null}
./k8s/manifests
├── deployment.yaml
├── service.yaml
├── ingress.yaml
└── configmap.yaml
```

> **lightbulb** GitOps treats Git as the single source of truth: make changes by updating Git and let automation (CI/CD or a GitOps controller) reconcile those changes against your environments.

## At a glance

IaC and CaC are complementary:

* IaC provisions and maintains infrastructure resources (cloud services, clusters, networks).
* CaC configures operating systems, runtime services, and application settings on that infrastructure.
* In GitOps you typically use IaC to create the platform (clusters, VPCs, storage) and CaC to deploy and configure applications inside that platform (Kubernetes manifests, Helm charts, or configuration management scripts).

## Key differences (quick reference)

| Area                  | IaC (Infrastructure-as-Code)                                        | CaC (Configuration-as-Code)                                                       |
| --------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Primary focus         | Provisioning infrastructure: compute, networking, storage, clusters | Configuring systems and applications: OS settings, packages, services, app config |
| Typical managed items | VMs, VPCs, load balancers, Kubernetes clusters                      | `configmaps`, secrets, packages, users, service settings                          |
| When to use           | When you need durable, reproducible cloud/platform resources        | When you need consistent runtime and app-level configuration                      |
| Example outcome       | A running Kubernetes cluster or cloud network                       | Deployed pods, configured services, application environment variables             |

## Common tools and examples

| Category           | Examples                                                       |
| ------------------ | -------------------------------------------------------------- |
| IaC tools          | Terraform, Pulumi, AWS CloudFormation                          |
| CaC tools          | Ansible, Puppet, Chef, Kubernetes manifests, Helm charts       |
| GitOps controllers | Argo CD, Flux CD                                               |
| CI/CD & automation | GitHub Actions, GitLab CI, Jenkins, Terraform Cloud/Enterprise |

Useful references:

* [Terraform Basics Training Course](https://learn.kodekloud.com/user/courses/terraform-basics-training-course)
* [Helm for Beginners](https://learn.kodekloud.com/user/courses/helm-for-beginners)
* [GitOps with ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [GitOps with FluxCD](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)
* [Learn Ansible Basics - Beginners Course](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)

## How IaC and CaC fit together in a GitOps workflow

A typical GitOps deployment separates concerns while keeping everything declarative in Git:

1. Author IaC to provision and update foundational resources:
   * Create/modify Terraform or Pulumi modules to provision clusters, VPCs, and storage.
   * Apply via CI/CD pipelines or an IaC operator.
2. Store application configuration (CaC) in a Git repo watched by a GitOps controller:
   * Kubernetes manifests, `ConfigMap`/`Secret` YAMLs, or Helm charts live in a Git repository.
   * A GitOps controller (Argo CD, Flux) continuously reconciles cluster state with repo state.
3. Reconcile and observe:
   * CI/CD and GitOps controllers ensure the environment matches the desired state in Git.
   * Rollbacks are performed by reverting commits in Git; automated reconciliation enforces the change.

## Practical example (end-to-end)

* Provision infrastructure with IaC:
  * Use Terraform to create an AWS EKS cluster, VPC, subnets, and IAM roles.
* Deploy and configure applications with CaC:
  * Commit Helm charts or Kubernetes manifests to a `gitops-apps` repo.
  * The GitOps controller (Argo CD / Flux) watches `gitops-apps` and applies manifests to the EKS cluster.
* Manage non-Kubernetes hosts:
  * Use Ansible to provision OS settings, install monitoring agents, and configure bastion hosts; store playbooks in Git and run via CI/CD.

This separation allows platform teams to own and version IaC while application teams manage CaC for their services, with Git enabling auditability and safe rollbacks.

## Workflow checklist

* Use Git as the source of truth for both infrastructure and configuration.
* Separate IaC and CaC repositories or directories to isolate responsibilities.
* Automate applying IaC changes (CI/CD, Terraform Cloud) and CaC reconciliation (Argo CD, Flux).
* Add CI checks (linting, tests) to prevent bad manifests from being applied.
* Tag or version releases so rollbacks are simple and auditable.

## Analogy

* IaC is building the house: foundation, framing, wiring.
* CaC is furnishing and operating the house: appliances, thermostat settings, installed software.

By keeping both infrastructure and configuration declarative in Git and automating their application, GitOps delivers reproducibility, observability, and safer rollbacks across both IaC and CaC changes.

## Links and further reading

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Terraform Documentation](https://www.terraform.io/docs)
* [Argo CD Documentation](https://argo-cd.readthedocs.io/)
* [Flux CD Documentation](https://fluxcd.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/673786b2-bedb-4405-a2c9-835aea1a9dd4/lesson/e5dccd05-0be3-4141-b6aa-27d4245f89f7)
