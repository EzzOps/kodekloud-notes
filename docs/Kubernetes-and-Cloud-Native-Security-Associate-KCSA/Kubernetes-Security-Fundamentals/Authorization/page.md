# Authorization

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Authorization/page

This article explains Kubernetes authorization, its importance, mechanisms, and how to configure them for managing user permissions within a cluster.

Kubernetes authentication verifies who you are, while **authorization** decides what actions authenticated users or services can perform within a cluster. Fine-grained authorization ensures that each role—developer, tester, CI/CD pipeline, or monitoring agent—only has the permissions necessary for its tasks.

## Why Authorization Matters

Cluster administrators have full control by default:

```bash theme={null}
