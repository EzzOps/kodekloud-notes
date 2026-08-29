# Revert a bad commit (replace <commit-hash> with the actual hash)
git revert <commit-hash>
```

Example revert output:

```text theme={null}
$ git revert o3u9n
[master s5e79] Revert "Config change"
 1 file changed, 1 deletion(-)
```

Some GitOps tools (for example Argo CD) can be configured to automatically revert to a known-good state when health checks fail or a deployment does not meet success criteria.

<Frame>
  <img alt="The image shows a rollback process flowchart, with steps from &#x22;Commit A&#x22; to &#x22;System back State A,&#x22; including a &#x22;Commit B (Bad)&#x22; and &#x22;Revert&#x22; step." />
</Frame>

Why rollback matters:

* Rapid recovery from bad deployments or configuration mistakes.
* Minimizes downtime and service disruption.
* Encourages frequent deployments by providing a reliable safety net.

## Key terms at a glance

| Term                      | Short definition                                                             |
| ------------------------- | ---------------------------------------------------------------------------- |
| Continuous reconciliation | Ongoing loop that observes, diffs, and acts to keep systems aligned with Git |
| Declarative               | Configuration style that specifies desired end state (YAML manifests)        |
| Desired state             | The canonical configuration stored in the state store (usually Git)          |
| State drift               | When actual cluster state differs from the desired state                     |
| State reconciliation      | Process to detect drift and restore desired state                            |
| State store               | Central repository of manifests (typically Git or OCI registries)            |
| Feedback loop             | Observability-driven cycle that informs changes in Git                       |
| Rollback                  | Reverting to a previous known-good state via Git or tooling                  |

## Summary

* GitOps uses Git as the single source of truth for declarative configuration.
* Continuous reconciliation (Observe → Diff → Act) keeps actual state aligned with desired state.
* Declarative manifests express intent; GitOps operators apply and maintain that intent automatically.
* State drift is detected and corrected through reconciliation.
* The state store (usually Git) enables collaboration, history, and reproducibility.
* Feedback loops and rollbacks provide operational safety and enable rapid, reliable iteration.

## Links and References

* Flux: [https://learn.kodekloud.com/user/courses/gitops-with-fluxcd](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)
* Argo CD: [https://learn.kodekloud.com/user/courses/gitops-with-argocd](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* Helm basics: [https://learn.kodekloud.com/user/courses/helm-for-beginners](https://learn.kodekloud.com/user/courses/helm-for-beginners)
* Prometheus, Grafana, Alertmanager: [https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/c61c911c-ea63-4920-ac9f-047b262566a5/lesson/5f8aa0fd-51b6-462c-bb07-e39b47937c52)


# Course Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Terminology/Course-Overview/page

Describes GitOps using Git as single source of truth and pull based controllers to prevent drift, improve auditability, reduce credential exposure, and simplify disaster recovery.

This lesson introduces common DevOps challenges and shows how GitOps addresses them by making Git the single source of truth and using automated, pull-based controllers to reconcile cluster state.

## Scenario

Dash0, a software vendor, is moving to a multi-cloud, containerized platform managed by a central Platform DevOps team. They adopted an Infrastructure-as-Code approach using tools such as [Kustomize](https://learn.kodekloud.com/user/courses/kustomize), [Terraform](https://learn.kodekloud.com/user/courses/terraform-basics-training-course), and [Ansible](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course) to define infrastructure and application deployments in code. However, their initial processes contained several operational flaws.

At first, team members manually applied Kubernetes manifests from a single Git branch without versioning, peer reviews, or automation. Changes were applied directly to the cluster, which made it impossible to audit reliably or trace who made what change and when.

<Frame>
  <img alt="The image is a flowchart illustrating the DevOps team's processes and challenges, highlighting tools like Terraform, Ansible, Git, and cloud services, along with issues in code reviews and configuration management." />
</Frame>

To speed up delivery, the team introduced a CI/CD pipeline that used a push-based model. In practice this created a dual workflow: the pipeline could push changes, and operators could still make manual, direct edits to the live cluster using kubectl. For example, operators applied different manifest versions directly:

```bash theme={null}
kubectl apply -f app-v2.8.4.yaml
kubectl apply -f app-v2.9.5.yaml
kubectl apply -f app-v3.0.1.yaml
```

This push-plus-manual approach produced three primary issues:

| Problem                      | Explanation                                                                                                                        | Impact                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Security risk                | The pipeline and manual CLI access required exposing credentials (service account tokens, static kubeconfigs) outside the cluster. | Increased attack surface and higher risk of leaked or misused credentials.                            |
| Configuration drift          | Manual, undocumented changes on the cluster meant the Git repository no longer reflected the live state.                           | Harder to debug, audit, and reason about production state.                                            |
| Unreliable disaster recovery | Disaster recovery plans assumed Git contained the complete, correct state. Undocumented cluster changes broke that assumption.     | Restores required manual discovery and reapplication of changes, increasing downtime and human error. |

## What is GitOps?

GitOps is a methodology that treats Git as the single source of truth for the desired system state and uses automated, auditable mechanisms to reconcile the live cluster state with Git. Instead of pushing changes into the cluster from outside, GitOps relies on pull-based agents (controllers) running inside the cluster to continuously compare and apply the declared state from Git.

> **lightbulb** GitOps: Store the desired state in Git, and use automated controllers (pull-based agents) inside the cluster to continuously reconcile the live state with Git. This improves auditability, reduces credential exposure, prevents configuration drift, and simplifies disaster recovery.

## Key benefits of GitOps

* Auditability: Every change is a Git commit, enabling complete history, code review, and traceability.
* Reduced credential exposure: Controllers running inside the cluster fetch manifests; external systems do not need persistent cluster credentials.
* Declarative convergence: Continuous reconciliation brings the cluster to the declared state, preventing drift.
* Faster, reliable rollbacks: Revert a commit in Git to roll back the desired state, and the controller will converge the cluster accordingly.
* Improved DR posture: The Git repo contains the canonical desired state, so restores are more predictable.

## How GitOps works (high level)

1. Developers or operators create commits (changes) in Git to update infrastructure or application manifests.
2. A GitOps controller inside the cluster watches the Git repository for changes.
3. When a change is detected, the controller pulls the desired state and reconciles the live cluster to match it.
4. Any drift is reported or automatically corrected according to policy.

## Links and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* GitOps principles and best practices — see documentation from major GitOps projects (Argo CD, Flux) for implementation details.
* [Kustomize tooling guide](https://learn.kodekloud.com/user/courses/kustomize)
* [Terraform basics training](https://learn.kodekloud.com/user/courses/terraform-basics-training-course)
* [Ansible for automation](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/c61c911c-ea63-4920-ac9f-047b262566a5/lesson/360f7fe6-0850-4369-bef9-b2ea2f5742aa)
