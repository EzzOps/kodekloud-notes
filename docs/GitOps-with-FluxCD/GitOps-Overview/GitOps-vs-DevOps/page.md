# Pseudocode for a reconciliation loop
while true; do
  actual_state=$(kubectl get all -o yaml)
  desired_state=$(git clone https://repo.git desired && cat desired/apps/nginx-deployment.yaml)
  if [ "$actual_state" != "$desired_state" ]; then
    kubectl apply -f desired/apps/nginx-deployment.yaml
  fi
  sleep 30
done
```

<Frame>
  ![The image outlines the four principles of GitOps: describing the system declaratively, versioning the desired state in a Git repository, automatically applying changes, and using GitOps agents to ensure system correctness and reconciliation.](https://kodekloud.com/kk-media/image/upload/v1752877620/notes-assets/images/GitOps-with-FluxCD-GitOps-Principles/gitops-four-principles-diagram.jpg)
</Frame>

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Argo CD](https://argo-cd.readthedocs.io/)
* [Flux CD](https://fluxcd.io/)
* [GitOps on CNCF](https://www.cncf.io/projects/gitops/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/3b5390cf-dfef-4ace-ab99-1ea5587a2cdb/lesson/66f3c857-d316-4d74-a6da-8c19bbf8ba77" />
</CardGroup>


# GitOps vs DevOps

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/GitOps-Overview/GitOps-vs-DevOps/page

This article compares GitOps and DevOps, highlighting their differences in application delivery, deployment workflows, challenges, and benefits.

GitOps is best understood as an evolution of DevOps that focuses exclusively on application delivery through Git as the single source of truth. While DevOps spans the entire CI/CD lifecycle—including build, test, deployment, monitoring, and governance—GitOps zeroes in on declarative infrastructure and automated cluster reconciliation.

***

## DevOps Deployment Workflow

In a traditional DevOps pipeline, the CI server (e.g., Jenkins, GitLab CI, CircleCI) handles both build and deployment:

1. **Commit & Build**
   * A developer pushes code to a Git repository.
   * The CI server runs unit tests, builds the application, and packages it into a Docker image.
2. **Push Image**
   * The image is tagged (e.g., `repo/app:v1.2.3`) and pushed to a container registry (Docker Hub, ECR, GCR).
3. **Deploy to Kubernetes**

   * The same CI pipeline uses stored Kubernetes credentials to apply manifests directly:

   ```bash theme={null}
   kubectl apply -f k8s/deployment.yaml
   ```

### Challenges in DevOps Deployment

| Challenge                 | Impact                                                                 |
| ------------------------- | ---------------------------------------------------------------------- |
| Cluster credentials in CI | Security risk if credentials are leaked or compromised.                |
| CI tool coupling          | Migrating to another CI/CD system requires rewriting deployment logic. |
| Limited auditability      | Harder to track “who changed what” outside Git history.                |

<Callout icon="triangle-alert">
  Storing Kubernetes credentials in your CI/CD server can expose your cluster if the server is compromised.
</Callout>

***

## GitOps Deployment Workflow

GitOps decouples build from deploy by introducing an in-cluster agent (often called an operator) that continuously reconciles Git state with the live cluster.

### Common CI Steps (Same as DevOps)

1. Developer commits code.
2. CI server builds, tests, and pushes the Docker image to the registry.

### Deployment Options

| Option | Process                                                                                                                  |
| ------ | ------------------------------------------------------------------------------------------------------------------------ |
| **A**  | 1. Install a GitOps agent (e.g., [Argo CD](https://argo-cd.readthedocs.io/), [Flux](https://fluxcd.io/)) in the cluster. |

2. Agent watches registry tags or watches the Git repo directly.
3. On detecting a new tag, agent updates or pulls manifests and applies changes. |
   \| **B**   | 1. Extend CI pipeline to clone the manifests repo.
4. CI updates `deployment.yaml` with the new image tag:

```bash theme={null}
kubectl set image deployment/app app=repo/app:v1.2.3
git commit -am "chore: bump image to v1.2.3"
git push origin main
```

3. CI opens a Pull Request against the manifest repository.
4. After review & merge, the in-cluster agent pulls and applies the updated manifests. |

<Callout icon="lightbulb">
  In both options, the CI server never needs direct access to Kubernetes. All deployment actions are driven by Git operations.
</Callout>

***

## Key Benefits of GitOps

| Feature                  | DevOps                 | GitOps                                                  |
| ------------------------ | ---------------------- | ------------------------------------------------------- |
| Source of Truth          | CI/CD tool + Git       | Git repository only                                     |
| Cluster Credential Scope | Stored in CI server    | Only the in-cluster agent has access                    |
| Audit & Rollback         | Custom scripts & logs  | Git history and simple `git revert`                     |
| Tool Coupling            | CI/CD-specific         | Any Git-compatible workflow                             |
| Security & Compliance    | Broader attack surface | Reduced credentials exposure, easier policy enforcement |

***

## Links and References

* [What is DevOps?](https://aws.amazon.com/devops/what-is-devops/)
* [GitOps Fundamentals](https://www.gitops.tech/)
* [Argo CD Documentation](https://argo-cd.readthedocs.io/)
* [Flux CD Overview](https://fluxcd.io/)
* [Kubernetes GitOps](https://kubernetes.io/docs/concepts/cluster-administration/gitops/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/3b5390cf-dfef-4ace-ab99-1ea5587a2cdb/lesson/78e7dcda-bb40-478f-a13b-5e679458ca11" />
</CardGroup>
