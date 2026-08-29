# Project Status Meeting 3

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Project-Status-Meeting-3/page

The article discusses the refactoring of a CI/CD pipeline to improve database performance and outlines the next steps for deployment planning.

In our third project status meeting, we recap how refactoring the CI/CD pipeline—by isolating job containers from service containers—has dramatically eased pressure on the production database. This separation ensures your jobs complete reliably without impacting live traffic.

> **lightbulb** Container isolation in CI/CD jobs reduces database locks and prevents resource contention.\
  Consider adopting this pattern early for any large-scale pipeline.

## Pipeline Optimization Overview

![The image is a project status meeting chart showing tasks assigned to Alice, with their statuses ranging from "Completed" to "Not started."](https://kodekloud.com/kk-media/image/upload/v1752877280/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Project-Status-Meeting-3/project-status-meeting-chart-alice.jpg)

Key improvements so far:

* Separated build/test jobs from long-running service containers
* Reduced concurrent connections on production DB by 40%
* Improved average job runtime by 25%

## Deployment Stage Roadmap

With the core optimizations complete, Alice and her team are now focusing on the next steps: defining deployment requirements, selecting orchestration tools, and automating rollout strategies. Below is the current project status, highlighting priorities, assignees, and outstanding issues.

![The image is a project status meeting chart listing tasks, their priorities, assigned person, status, and comments/issues. Tasks range from "Completed" to "Not started," all assigned to Alice.](https://kodekloud.com/kk-media/image/upload/v1752877282/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Project-Status-Meeting-3/project-status-meeting-chart.jpg)

| Task                          | Priority | Assignee | Status      | Comments / Issues                      |
| ----------------------------- | -------- | -------- | ----------- | -------------------------------------- |
| Define k8s deployment specs   | High     | Alice    | In Progress | Waiting on service account permissions |
| CI to CD handoff automation   | Medium   | Alice    | Not Started | Evaluate GitLab release job            |
| Helm chart templating         | Low      | Alice    | Not Started | Research community charts              |
| Canary and blue/green rollout | High     | Alice    | Not Started | Drafting rollback procedures           |

> **triangle-alert** Before scaling up in Kubernetes, double-check resource requests/limits to prevent OOM kills and scheduler evictions.

## Next Sessions & Resources

In upcoming meetings, we’ll cover:

* **Kubernetes Fundamentals**: pods, services, deployments
* **Helm & Chart Management**: templating and versioning
* **Automated Rollbacks & Monitoring**: integrating health checks

For a head start on Kubernetes concepts, see [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/).

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [GitLab CI/CD Overview](https://docs.gitlab.com/ee/ci/)
* [Helm Charts Guide](https://helm.sh/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/289d71ce-3109-4f9d-ba17-4b69a6036c64)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/36fd80b0-a7e9-4608-aa9a-805d6e9862a4)
