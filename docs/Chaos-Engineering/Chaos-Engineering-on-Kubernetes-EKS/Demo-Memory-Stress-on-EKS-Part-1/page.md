# Demo Memory Stress on EKS Part 1

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Chaos-Engineering-on-Kubernetes-EKS/Demo-Memory-Stress-on-EKS-Part-1/page

This guide prepares your environment for running AWS Fault Injection Simulator experiments on Amazon EKS.

In this guide, we’ll prepare your environment for running AWS Fault Injection Simulator (FIS) experiments on Amazon EKS. By the end of this lesson, you will have:

* Logged into an EC2 host and navigated to your working directory
* Created an IAM role dedicated to AWS FIS
* Attached all required IAM policies to the role
* Configured `kubectl` and applied Kubernetes RBAC
* Verified that the metrics-server is operational and checked pod metrics

For more on AWS FIS, visit the [AWS Fault Injection Simulator Documentation](https://docs.aws.amazon.com/fis/latest/userguide/what-is-fis.html).

***

## 1. SSH into EC2 & Navigate to the Experiment Directory

First, connect to your EC2 instance (e.g., via EC2 Instance Connect), switch to root, and change into the workshop folder:

```bash theme={null}
