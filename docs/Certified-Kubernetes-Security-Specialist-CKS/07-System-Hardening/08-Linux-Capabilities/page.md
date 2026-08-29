# Linux Capabilities

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/Linux-Capabilities/page

This article explores adding or removing Linux capabilities on Kubernetes pods and explains restrictions on certain operations even when running as root.

In this lesson, we explore how to add or remove Linux capabilities on Kubernetes pods and understand why certain operations, like changing the system date, can be restricted even when running as root.

Earlier, in our Seccomp lecture, we observed that even when a container runs with Seccomp set to unconfined, modifying the system date is prohibited. This behavior extends to Kubernetes pods as well. By default, Kubernetes pods do not utilize Seccomp, and a container—even running as root (UID 0)—may still be restricted from performing certain operations.

<Callout icon="lightbulb">
  When running containers with Docker, the default security settings include restrictions that prevent operations such as modifying the system clock, unless explicitly permitted by adjusting capabilities.
</Callout>

## Demonstration Using Docker

The example below demonstrates the restricted behavior using Docker:

```bash theme={null}
docker run -it --rm --security-opt seccomp=unconfined docker/whalesay /bin/sh
