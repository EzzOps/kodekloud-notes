# Tools needed for EKS

Source: https://notes.kodekloud.com/docs/AWS-EKS/EKS-Fundamentals/Tools-needed-for-EKS/page

This article outlines essential command-line tools for provisioning and managing Amazon EKS clusters.

Before you dive into provisioning and operating Amazon EKS clusters, equip yourself with these essential command-line tools. While our workshop may not invoke every utility directly, you’ll rely on them for automated deployments, secure authentication, and ongoing cluster maintenance.

| Tool                                 | Purpose                                           | Documentation                                   |
| ------------------------------------ | ------------------------------------------------- | ----------------------------------------------- |
| eksctl                               | Official EKS CLI for cluster lifecycle management | [eksctl on GitHub][eksctl-docs]                 |
| eksdemo                              | Demo workloads and add-on deployment using eksctl | [eksdemo on GitHub][eksdemo-docs]               |
| AWS IAM Authenticator for Kubernetes | `kubectl` plugin for AWS IAM–based authentication | [AWS IAM Authenticator][iam-authenticator-docs] |

## eksctl: The Official EKS CLI

`eksctl` streamlines cluster creation, updates, and deletion by generating CloudFormation stacks under the hood. Use it to manage control plane versions, node groups, and scaling policies—all via simple commands or declarative config files.

### Installation

```bash theme={null}
