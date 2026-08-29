# Example: Application.spec.syncPolicy to enable auto-sync, pruning, and self-heal
spec:
  syncPolicy:
    automated:
      prune: true      # delete resources removed from Git
      selfHeal: true   # revert out-of-band changes in the cluster
# To keep sync manual, remove the entire `automated` block above.
```

Assume an Application tracks a Git repo that initially contains `deployment.yaml` and `configmap.yaml`. A webhook is set up so Argo CD learns about Git changes immediately. Below are four common combinations of flags and their effects.

1. Automatic sync only (prune = false, selfHeal = false)

* Adding `service.yaml` to Git: Argo CD applies it automatically to the cluster.
* Deleting `service.yaml` from Git: Argo CD does not remove the service from the cluster (no auto-prune).
* Manually deleting the `configmap` in the cluster via kubectl: Argo CD will not recreate it (self-heal disabled).

2. Automatic sync + Auto-pruning (prune = true, selfHeal = false)

* Adding `service.yaml` to Git: applied automatically.
* Deleting `service.yaml` from Git: Argo CD removes that resource from the cluster on the next sync (auto-prune enabled).
* Manually deleting the `configmap` in the cluster: Argo CD does not restore it (self-heal disabled).

3. Automatic sync + Self-heal (prune = false, selfHeal = true)

* Adding `service.yaml` to Git: applied automatically.
* Deleting `service.yaml` from Git: resource remains in cluster (prune disabled).
* Manually deleting the `configmap` in the cluster: Argo CD detects drift and recreates the resource from Git (self-heal enabled).

4. Automatic sync + Auto-prune + Self-heal (prune = true, selfHeal = true)

* Adding `service.yaml` to Git: applied automatically.
* Deleting `service.yaml` from Git: resource is removed from the cluster (auto-prune enabled).
* Manually deleting the `configmap` in the cluster: Argo CD recreates it from Git (self-heal enabled).

For quick comparison, here is a summary table of these scenarios:

| Scenario                         | prune | selfHeal | New manifest added to Git | Manifest removed from Git    | Manual deletion in cluster |
| -------------------------------- | ----- | -------- | ------------------------- | ---------------------------- | -------------------------- |
| 1. Auto sync only                | false | false    | Applied automatically     | Not removed from cluster     | Not restored               |
| 2. Auto sync + prune             | true  | false    | Applied automatically     | Removed from cluster on sync | Not restored               |
| 3. Auto sync + self-heal         | false | true     | Applied automatically     | Not removed from cluster     | Restored automatically     |
| 4. Auto sync + prune + self-heal | true  | true     | Applied automatically     | Removed from cluster on sync | Restored automatically     |

The following diagram visualizes these GitOps flows (initial Git repo: `deployment.yml`, `configmap.yml`) and shows what happens when `service.yml` or `configmap` resources are deleted under different sync options.

<Frame>
  <img alt="A labeled diagram showing GitOps workflows between a GitHub repo (deployment.yml, configmap.yml), Argo CD, and a Kubernetes cluster illustrating what happens when service.yml or configmap resources are deleted. It highlights three behaviors—manual/automatic sync, auto-pruning of resources, and self-heal of the cluster—using icons and step-by-step flows." />
</Frame>

In summary:

* Use automatic sync to apply Git changes immediately and reduce manual steps.
* Enable prune to ensure the cluster mirrors deletions made in Git.
* Enable self-heal to automatically reconcile manual or out-of-band changes so the cluster continuously matches the Git-defined state.

Links and references:

* Argo CD documentation: [https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
* Git: [https://git-scm.com/](https://git-scm.com/)
* Kubernetes: [https://kubernetes.io/](https://kubernetes.io/)
* GitHub webhooks: [https://docs.github.com/en/developers/webhooks-and-events/about-webhooks](https://docs.github.com/en/developers/webhooks-and-events/about-webhooks)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/16e00975-ac10-4915-9801-a00bc17041c4" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Introduction-and-Basics/Course-Introduction/page

This course provides hands-on training for mastering Jenkins CI/CD from foundational concepts to advanced operational strategies.

Welcome to the **Certified Jenkins Engineer** course! I'm **Siddharth Barahalikar**, your instructor for this in-depth Jenkins CI/CD journey.

Jenkins is the leading open-source automation server, powering over one million active installations worldwide. Industry giants like [AWS](https://aws.amazon.com), [IBM](https://www.ibm.com), and [GitHub](https://github.com) rely on Jenkins to streamline their software delivery pipelines.

In this hands-on course, you'll progress from foundational concepts to advanced operational strategies. Each module combines clear explanations with practical labs—so you can experiment, troubleshoot, and master Jenkins on real-world projects.

## Course Outline

### 1. Introduction to Jenkins

Understand Source Control Management (SCM), Continuous Integration (CI), and Continuous Deployment (CD) as the core principles of Jenkins automation.

### 2. Jenkins Architecture & Installation

Explore the master-agent architecture, install Jenkins on various platforms, perform initial configuration, and navigate the user interface.

<Callout icon="lightbulb">
  Ensure you have Java 8+ and Docker installed before starting the labs. These tools are prerequisites for many of our exercises.
</Callout>

### 3. Plugins Management

Discover, install, and manage Jenkins plugins to extend functionality and tailor Jenkins to your workflow.

<Callout icon="triangle-alert">
  Installing outdated or unverified plugins can pose security risks. Always verify plugin sources and versions.
</Callout>

### 4. Jenkins Pipelines

Master both **Declarative** and **Scripted** pipelines, automate your build-test-deploy workflows, and interact with Jenkins via the CLI and REST API.

### 5. Continuous Integration & Deployment

Build CI pipelines for [Node.js](https://nodejs.org) applications, integrate [SonarQube](https://www.sonarqube.org) for code quality, and deploy containers using [Docker](https://www.docker.com) and [AWS](https://aws.amazon.com).

### 6. Kubernetes & GitOps

Implement GitOps workflows with [Argo CD](https://argo-cd.readthedocs.io) and deploy applications on [Kubernetes](https://kubernetes.io).

### 7. Administration & Monitoring

Monitor and manage Jenkins with [Prometheus](https://prometheus.io) metrics and visualize performance dashboards in [Grafana](https://grafana.com).

### 8. Backup & Configuration Management

Automate Jenkins backup and disaster recovery using the Configuration as Code plugin and orchestrate your configuration pipeline with [GitHub Actions](https://github.com/features/actions).

To ensure you're exam-ready, this course includes mock assessments that mirror the real Jenkins certification test. Practice exams will highlight knowledge gaps and boost your confidence.

Ready to become a **Certified Jenkins Engineer**? Enroll now and elevate your CI/CD expertise!

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2e8ea9bb-e5bb-428e-85d9-89f2eb816adb/lesson/d205f96d-b0e8-4df3-91f6-07bf531a19c9" />
</CardGroup>
