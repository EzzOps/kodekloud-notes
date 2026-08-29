# Isolation and Segmentation Security Context

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Isolation-and-Segmentation-Security-Context/page

This lesson covers Kubernetes security contexts for controlling permissions and access for Pods and containers, including best practices and configuration levels.

Welcome to this lesson on **Security Contexts in Kubernetes**. Security contexts allow you to control permissions and access for Pods and containers. You will learn:

* How to mirror Docker security options in Kubernetes
* The difference between Pod-level and Container-level configurations
* Best practices for applying user IDs and Linux capabilities

For detailed reference, see the [Kubernetes Security Context Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).

***

## Why Security Contexts Matter

Security contexts help you enforce least-privilege container execution:

* Define which Linux user or group a container runs as
* Grant or restrict Linux capabilities (e.g., `NET_ADMIN`, `SYS_TIME`)
* Enable Pod-level settings that apply to all containers

If you’ve used Docker, you may be familiar with:

```bash theme={null}
