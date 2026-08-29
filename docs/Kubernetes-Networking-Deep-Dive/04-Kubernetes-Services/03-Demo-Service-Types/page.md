# Demo Service Types

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Kubernetes-Services/Demo-Service-Types/page

This guide explains the four primary Kubernetes Service types using a sample NGINX deployment to help expose applications inside and outside the cluster.

In this guide, you’ll learn about the four primary Kubernetes Service types—ClusterIP, NodePort, Headless, and ExternalName—using a sample NGINX deployment. Understanding these service types will help you expose applications both inside and outside your cluster.

## Overview of Service Types

| Service Type | Scope                    | Use Case                               | Example Port |
| ------------ | ------------------------ | -------------------------------------- | ------------ |
| ClusterIP    | Internal cluster traffic | Internal load-balancing                | `80`         |
| NodePort     | Node’s IP + port         | External access via node IP and port   | `30000`      |
| Headless     | Pod IPs directly         | Direct per-pod connectivity (no LB)    | `80`         |
| ExternalName | DNS CNAME mapping        | Map service to external DNS (no proxy) | N/A          |

Before diving in, we’ve deployed three NGINX pods with the label `role=nginx` in the `default` namespace:

```bash theme={null}
kubectl get pods
