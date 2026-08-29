# Kubelet Security

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Cluster-Setup-and-Hardening/Kubelet-Security/page

This article discusses securing the Kubelet in Kubernetes by configuring authentication, authorization, and managing access to its APIs.

In this lesson, we revisit the Kubelet and examine multiple approaches for its configuration and hardening on Kubernetes nodes. In the [CKA Certification Course - Certified Kubernetes Administrator](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator), the Kubelet is compared to a ship’s captain. Much like a captain, it handles onboard operations, manages paperwork to join the cluster, and communicates regularly with the master control. It also loads or unloads containers as instructed by the scheduler and sends continuous status reports.

However, a significant security risk arises if an impersonator masquerades as the master, potentially exposing sensitive information about cargo such as its quantity, content, and destination. Therefore, protecting all communications between the master (kube-apiserver) and the Kubelet is essential.

The Kubelet registers its node with the Kubernetes cluster and, upon receiving commands to deploy a container or pod, delegates tasks to the container runtime (for example, Docker). It then continuously monitors the pod and container states, reporting their status back to the kube-apiserver.

***

## Installing the Kubelet

Traditionally, installing the Kubelet involved manually downloading its binary and configuring it as a service. When using the `kubeadm` tool for cluster deployment, the necessary binaries are downloaded automatically, and the cluster is bootstrapped for you. However, you must still install the Kubelet on each worker node manually.

Below is an example of installing the Kubelet and setting up its service:

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.20.0/bin/linux/amd64/kubelet
```

```bash theme={null}
