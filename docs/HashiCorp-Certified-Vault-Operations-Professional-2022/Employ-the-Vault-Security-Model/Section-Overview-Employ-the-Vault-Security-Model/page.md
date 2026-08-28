# Disable core dumps on the host
ulimit -c 0
```

In your Pod spec security context:

```yaml theme={null}
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    add: ["IPC_LOCK"]
  resources:
    limits:
      core: 0
```

<Callout icon="triangle-alert">
  A core dump could expose sensitive encryption keys. Always set `RLIMIT_CORE` to `0` in your containers.
</Callout>

<Frame>
  ![The image provides guidance on disabling core dumps in a Kubernetes cluster, highlighting the importance of setting RLIMIT\_CORE to 0 to prevent core dumps that may contain sensitive encryption keys. It includes a diagram of a Kubernetes cluster with nodes running Vault servers.](https://kodekloud.com/kk-media/image/upload/v1752878552/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Running-Vault-in-Kubernetes/disable-core-dumps-kubernetes-diagram.jpg)
</Frame>

## Enable mlock

Prevent Vault’s memory from being swapped to disk by granting the `IPC_LOCK` capability. This ensures in-memory encryption keys never hit swap:

```yaml theme={null}
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    add: ["IPC_LOCK"]
```

## Run as Non-Root & Read-Only Filesystem

Running Vault as root increases risk if a container escape occurs. Enforce non-root execution and mount the filesystem read-only:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: vault-server
spec:
  containers:
    - name: vault
      image: vault:latest
      securityContext:
        runAsNonRoot: true
        readOnlyRootFilesystem: true
        capabilities:
          add: ["IPC_LOCK"]
```

<Frame>
  ![The image is a slide advising not to run Vault as root, explaining that it should run as an unprivileged user to prevent exposure of process memory and encryption keys. It features a yellow background with a cartoon character in the bottom right corner.](https://kodekloud.com/kk-media/image/upload/v1752878553/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Running-Vault-in-Kubernetes/vault-not-run-as-root-advice.jpg)
</Frame>

## Security Context Cheat Sheet

| Feature                   | Configuration Snippet                   | Purpose                               |
| ------------------------- | --------------------------------------- | ------------------------------------- |
| Disable Core Dumps        | limits.core: 0                          | Prevents writing memory dumps to disk |
| Enable mlock              | capabilities.add: \["IPC\_LOCK"]        | Locks memory to avoid swapping        |
| Non-Root Execution        | runAsNonRoot: true<br />runAsUser: 1000 | Reduces attack surface in container   |
| Read-Only Root Filesystem | readOnlyRootFilesystem: true            | Prevents unwanted file modifications  |

## Additional Best Practices

* Deploy Vault on a dedicated Kubernetes cluster.
* Minimize enabled auth methods and secrets engines.
* Keep token TTLs short and prune unused policies regularly.
* Ensure Vault is the main process (PID 1) in each container, so it receives signals properly.

For a deeper dive, see the\
[HashiCorp Learn tutorial on running Vault in Kubernetes](https://learn.hashicorp.com/tutorials/vault/kubernetes).\
Other useful references:

* [Vault Helm Chart](https://artifacthub.io/packages/helm/hashicorp/vault)
* [Kubernetes Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/e5e1dc8a-e494-400d-8c96-44665ed5981d/lesson/900fe81c-0d64-466a-adc0-75c07d1d27d0" />
</CardGroup>


# Section Overview Employ the Vault Security Model

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Employ-the-Vault-Security-Model/Section-Overview-Employ-the-Vault-Security-Model/page

This section covers the HashiCorp Vault security model focusing on client authentication and security implications in Kubernetes deployments.

In this section, we dive into the HashiCorp Vault security model. This conceptual lesson covers two essential topics without any hands-on labs or demos:

| Topic                                                | What You’ll Learn                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------------- |
| Secure introduction of Vault clients                 | Best practices for authenticating and authorizing applications and users. |
| Security implications of running Vault on Kubernetes | Key considerations when deploying Vault within Kubernetes clusters.       |

<Frame>
  ![The image is an objective overview slide titled "Employ the Vault Security Model," listing two objectives: describing the secure introduction of Vault clients and the security implications of running Vault on Kubernetes. It also features a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878554/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Section-Overview-Employ-the-Vault-Security-Model/employ-vault-security-model-overview.jpg)
</Frame>

<Callout icon="lightbulb">
  This section is purely conceptual. Focus on terminology, security considerations, and Vault architecture rather than practical implementation.
</Callout>

When preparing for the [HashiCorp Certified: Vault Operations Professional](https://www.hashicorp.com/certification/vault) exam, “describe” questions assess your theoretical grasp of these topics, often in a multiple-choice format.

<Callout icon="triangle-alert">
  No demos or labs are provided here. For hands-on practice, consult the [Vault documentation](https://www.vaultproject.io/docs) and [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).
</Callout>

Focus on understanding how Vault handles client authentication, authorization, and the security trade-offs when running Vault in a Kubernetes environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/e5e1dc8a-e494-400d-8c96-44665ed5981d/lesson/32283549-a43a-4b76-9002-73a34c558ccd" />
</CardGroup>
