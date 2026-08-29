# modules/my-wrapper/main.tf
module "eks" {
  source       = "git::https://github.com/terraform-aws-modules/eks/aws"
  cluster_name = var.cluster_name       # mapped from wrapper input
  vpc_id       = var.vpc_id             # mapped from wrapper input
  tags = merge(
    var.organization_tags,              # enforced by your organization
    var.user_tags                       # additional user-provided tags
  )
  # ...other required community inputs
}
```

3. Declare only the variables your team needs in `variables.tf`:

```hcl theme={null}
# modules/my-wrapper/variables.tf
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the EKS cluster"
  type        = string
}

variable "organization_tags" {
  description = "Tags enforced by the organization"
  type        = map(string)
  default     = { Project = "AcmeCorp" }
}

variable "user_tags" {
  description = "Additional tags from the user"
  type        = map(string)
  default     = {}
}
```

> **lightbulb** By exposing only selected inputs, you maintain a clear contract for your internal teams while still benefitting from community-driven improvements.

4. In your root Terraform or Terragrunt configuration, invoke `modules/my-wrapper` instead of the community module directly.

```hcl theme={null}
module "production_eks" {
  source = "../modules/my-wrapper"

  cluster_name       = "prod-cluster"
  vpc_id             = "vpc-0123456789abcdef0"
  organization_tags  = { Environment = "production", Team = "infra" }
  user_tags          = { Owner = "alice" }
}
```

## Choosing Between Community, Custom, and Wrapper Modules

| Criteria               | Community Modules | Custom Modules | Wrapper Modules          |
| ---------------------- | ----------------- | -------------- | ------------------------ |
| Reusability            | High              | Low            | Medium                   |
| Development Speed      | Fast              | Slow           | Moderate                 |
| Maintenance Overhead   | Low               | High           | Medium                   |
| Upstream Compatibility | Direct upgrades   | N/A            | Retained with mapping    |
| Flexibility            | Limited to inputs | Full control   | Control over inputs only |

### When to Use What

* **Community Modules**: Go-to for rapid prototyping or teams with minimal customization needs.
* **Custom Modules**: Best for specialized architectures requiring bespoke resource definitions.
* **Wrapper Modules**: Ideal for enforcing organizational governance on top of community best practices.

> **triangle-alert** Avoid forking community modules unless you require deep structural changes. Wrapping keeps you in sync with upstream fixes and feature releases.

## References

* [Terraform Module Registry](https://registry.terraform.io/)
* [Terraform AWS EKS Module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws)
* [Terraform Best Practices](https://www.terraform.io/docs/language/modules/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/4d4cda50-7d42-4622-b0d4-fa6e6ce0a16d/lesson/5504cd7a-0183-43a0-9b3c-f0a2e65e8f61)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Ultimate-Certified-Kubernetes-Administrator-CKA-Mock-Exam-Series/Certified-Kubernetes-Administrator-Mock-Exam-Series/Course-Introduction/page

Introduction to KodeKloud's Ultimate CKA mock exam series offering realistic multi‑cluster labs, tasks, kubectl guidance, secret decoding examples, exam weightings, and best practices for CKA preparation

Hello everyone — I’m Vijay Palani from KodeKloud. Welcome to the Ultimate CKA Mock Exam Series.

This series is designed to give you realistic, hands‑on practice that mirrors the real Certified Kubernetes Administrator (CKA) exam experience. If your exam is coming up, these mock exams will help refine your skills across the core CKA domains and get you comfortable with multi‑cluster scenarios, SSH into nodes, and time‑boxed problem solving.

> **lightbulb** If you have not yet completed the [Certified Kubernetes Administrator (CKA) preparation course](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator), please complete it first. It contains the foundation, official mock exams, and Lightning Labs that will prepare you for this advanced mock exam series.

## What this mock exam series covers

Each mock exam in this series is:

* Comprehensive and challenging.
* Structured to reflect the real CKA exam weightages.
* Delivered across multiple Kubernetes clusters (four clusters total), with some clusters dedicated to specific knowledge areas.

<Frame>
  <img alt="The image shows a person speaking, with a list of &#x22;Exam Clusters&#x22; that includes details about various Kubernetes cluster configurations." />
</Frame>

By default you will log in to the student node (a client). From the student node you can:

* Switch kubectl contexts to access any of the four clusters.
* SSH into individual nodes for deeper troubleshooting where required.

### CKA domain breakdown (exam weightage)

|                           Knowledge Area | Percentage |
| ---------------------------------------: | ---------: |
| Architecture, Installation & Maintenance |        25% |
|                   Workloads & Scheduling |        15% |
|                    Services & Networking |        20% |
|                                  Storage |        10% |
|                          Troubleshooting |        30% |

Each mock exam respects these weightages to give you a realistic distribution of tasks.

## Getting started with a lab

When you open a lab from this series, it should load within \~30 seconds (occasionally 1–2 minutes). Once the lab is loaded you will see the task list and the terminal / environment for the student node.

<Frame>
  <img alt="The image shows a webpage from KodeKloud offering the &#x22;Ultimate Certified Kubernetes Administrator (CKA) Mock Exam Series&#x22; with course details and a start course button." />
</Frame>

A typical lab contains \~20 questions that span the CKA domains listed above. Each question will indicate which cluster/context you should use. Always set the correct kubectl context before starting a task.

## Common kubectl context and cluster commands

Switch to the required cluster context (example: cluster3):

```bash theme={null}
kubectl config use-context cluster3
```

List all configured clusters:

```bash theme={null}
kubectl config get-clusters
```

If no context is set, you will access `cluster1` by default. Example cluster descriptions you may encounter:

* `cluster1`: two worker nodes (`cluster1-node01`, `cluster1-node02`)
* `cluster3`: single control-plane node (`cluster3-controlplane`, version 1.24 as of recording)

Always confirm the current context before proceeding:

```bash theme={null}
kubectl config current-context
```

## Typical task: decode a Secret and save it on the student node

A common exam task is to decode an existing Secret and save the decoded value to a file on the student node (for example, `/opt/beta-sec-cka14-arch`). A streamlined, reproducible approach:

1. Ensure you are on the correct cluster/context:

```bash theme={null}
kubectl config use-context cluster3
```

2. Confirm the namespace exists and list secrets in that namespace:

```bash theme={null}
kubectl get ns
kubectl get secrets -n beta-ns-cka14-arch
```

3. View the Secret in YAML to see the base64-encoded data:

```bash theme={null}
kubectl get secret beta-sec-cka14-arch -n beta-ns-cka14-arch -o yaml
```

4. Copy the base64 string shown under `data`, then decode and redirect to the required file on the student node:

```bash theme={null}
echo 'VGhpcpyB0aGlgc2VjcmVtV0lQbw==' | base64 -d > /opt/beta-sec-cka14-arch
```

5. Verify the file contents:

```bash theme={null}
cat /opt/beta-sec-cka14-arch
```

Note: the secret must be saved on the student node filesystem (not inside a pod).

### Useful secret inspection variants

* To decode a specific key from the Secret without saving:

```bash theme={null}
kubectl get secret beta-sec-cka14-arch -n beta-ns-cka14-arch -o jsonpath='{.data.<key>}' | base64 -d
```

Replace `<key>` with the secret data key from the YAML output.

## Navigating multiple questions and sections

You can scroll between questions in the lab interface just like any online mock exam. However:

* The exam is time-boxed. If you exceed the allotted time, the exam will end automatically and be validated.
* You may click the "End Exam" button at any time to trigger immediate validation and view your score.

> **warning** Always monitor your remaining time. Unfinished tasks will be marked as incorrect when the exam ends (manually or due to timeout).

<Frame>
  <img alt="The image shows a split screen with a task-based interface on the left, indicating a 0% score and incomplete tasks, and a terminal window on the right displaying Kubernetes commands and outputs." />
</Frame>

## Example walkthrough snippets

A few sample commands you may see or use during the lab:

* Switch context and monitor logs:

```bash theme={null}
kubectl --context cluster1 logs -f color-app-cka13-arch
```

* Create a ServiceAccount, ClusterRole, ClusterRoleBinding, and validate permissions (RBAC practice):

```bash theme={null}
kubectl --context cluster1 create serviceaccount my-service-account
kubectl --context cluster1 create clusterrole my-cluster-role --verb=get,list,watch --resource=pods
kubectl --context cluster1 create clusterrolebinding my-cluster-role-binding --clusterrole=my-cluster-role --serviceaccount=default:my-service-account
kubectl --context cluster1 auth can-i get pods --as=system:serviceaccount:default:my-service-account
