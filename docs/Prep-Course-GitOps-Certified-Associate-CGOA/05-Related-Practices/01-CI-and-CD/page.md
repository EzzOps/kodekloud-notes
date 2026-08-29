# Create a Kubernetes Secret manifest (not applied to the cluster)
kubectl create secret generic mysql-password \
  --from-literal=password='s1Ddh@rttF' \
  --dry-run=client -o yaml > mysql-password_k8s-secret.yaml

# Use kubeseal (installed separately) to encrypt the secret into a SealedSecret
# Apply the sealed secret to the cluster (Sealed Secrets controller will decrypt it)
# kubectl apply -f sealed-secret.yaml
```

Local Kubernetes Secret manifest example:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: mysql-password
type: Opaque
data:
  # Base64-encoded password (example)
  password: czFEZGhAcnQj
```

Once you have a `sealed-secret.yaml`, you can manage it in Git and create an Argo CD application that points to the chart or repository hosting the Sealed Secrets controller:

```bash theme={null}
argocd app create sealed-secrets \
  --repo https://bitnami-labs.github.io/sealed-secrets \
  --helm-chart sealed-secrets \
  --revision 2.2.0 \
  --dest-namespace kube-system \
  --dest-server https://1.2.3.4
```

Recommended references:

* Bitnami Sealed Secrets: [https://github.com/bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)
* `kubeseal` docs: [https://github.com/bitnami-labs/sealed-secrets#kubeseal](https://github.com/bitnami-labs/sealed-secrets#kubeseal)

## Tooling and repository layouts

You will practice operating both manifest-based repos and Helm chart repositories. A typical navigation example:

```bash theme={null}
# Example repository navigation
cd cgoa-demos/manifests/helm/
ls
# Output:
# highway-chart
cd highway-chart/
```

Consider organizing repos with clear boundaries:

* `infrastructure/` for cluster-level manifests (ingress, storage)
* `applications/` for per-app Helm charts or Kustomize overlays
* `ci/` for pipeline definitions that update Git

## CI pipelines that update Git (example pattern)

A common GitOps pattern: CI builds and publishes an image, then updates a manifest in Git (e.g., bumps an image tag). The GitOps controller then reconciles that change to the cluster. Below is a cleaned Jenkins pipeline that demonstrates the pattern.

```groovy theme={null}
pipeline {
  agent any
  environment {
    REPO_URL = "http://localhost:5000/kk-org/cgoa-demos"
    BRANCH = "feature-gitea"
    REMOTE_AUTH = "http://587fcc78b44a416b7497ad5065dad577d722708@localhost:5000/kk-org/cgoa-demos"
  }
  stages {
    stage('Checkout') {
      steps {
        script {
          if (fileExists('cgoa-demos')) {
            echo 'Cloned repo already exists - Pulling latest changes'
            dir('cgoa-demos') {
              sh 'git pull'
            }
          } else {
            echo 'Repo does not exist - Cloning the repo'
            sh "git clone -b ${BRANCH} ${REPO_URL}"
          }
        }
      }
    }

    stage('Update Manifest') {
      steps {
        dir('cgoa-demos/jenkins-demo') {
          // Replace placeholder image with the new image tag in deployment.yaml
          sh 'sed -i "s|${IMAGE_REPO}/${NAME}:${VERSION}|${NEW_IMAGE}|g" deployment.yaml'
          sh 'cat deployment.yaml'
        }
      }
    }

    stage('Commit & Push') {
      steps {
        dir('cgoa-demos/jenkins-demo') {
          sh '''
            git config --global user.email "jenkins@ci.com"
            git remote set-url origin ${REMOTE_AUTH}
            git checkout ${BRANCH}
            git add -A || true
            git commit -m "Update manifest: set image to ${NEW_IMAGE}" || true
            git push origin ${BRANCH} || true
          '''
        }
      }
    }
  }
}
```

This pattern demonstrates the separation of concerns:

* CI: build/publish artifacts and update Git (push change).
* GitOps controller: continuously reconcile the cluster to match Git.

## Infrastructure as Code (IaC) vs Configuration as Code (CaC)

Understanding IaC vs CaC clarifies responsibilities:

| Concern       | IaC                                                       | CaC                                                 |
| ------------- | --------------------------------------------------------- | --------------------------------------------------- |
| Primary focus | Provisioning infrastructure (clusters, VMs, networks)     | Application configuration and runtime manifests     |
| Typical tools | Terraform, Pulumi, CloudFormation                         | Helm, Kustomize, plain Kubernetes manifests         |
| GitOps role   | Often used in provisioning pipelines or as upstream input | Primary driver for reconciliation engines (Argo CD) |

Use IaC to create and manage platform resources; use CaC to manage how workloads run on those platforms.

<Frame>
  <img alt="The image compares Infrastructure as Code (IaC) and Configuration as Code (CaC), highlighting their primary focus, what they manage, common tools, context in GitOps, and analogies." />
</Frame>

## Other topics covered

* Moving from DevOps to DevSecOps: integrating security into GitOps workflows.
* CI/CD best practices and how CI pipelines feed pull-based delivery.
* Observability: Prometheus metrics, Grafana dashboards, and Alertmanager for alerts and incident detection.
* DORA metrics: measuring lead time, deployment frequency, MTTR, and change failure rate.
* Labs, exercises, and mock exams to validate your knowledge and certification readiness.

## Quick links & references

* Argo CD: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Bitnami Sealed Secrets: [https://github.com/bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Helm: [https://helm.sh/](https://helm.sh/)
* Kustomize: [https://kustomize.io/](https://kustomize.io/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Jenkins: [https://www.jenkins.io/](https://www.jenkins.io/)
* DORA metrics primer: [https://cloud.google.com/blog/products/devops-sre/dora-research-accelerate](https://cloud.google.com/blog/products/devops-sre/dora-research-accelerate)

Are you ready to become a GitOps Certified Associate and lead cloud-native operational excellence? This course will prepare you with the practical skills and exam-focused practice to succeed.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/b51e7927-03a2-4bb9-a900-6a55c35e6a0c/lesson/cdf68874-2b28-4011-925b-1025405c736c)


# CI and CD

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Related-Practices/CI-and-CD/page

Explains CI and CD, PR based pipelines, automated testing and deployment strategies that enable faster, safer, and more reliable software delivery.

This guide explains why Continuous Integration (CI) and Continuous Delivery/Deployment (CD) are essential for modern software development. It covers typical workflows, common pitfalls when CI is absent, and how CI/CD pipelines validate and promote changes from feature branches to production.

What you'll learn:

* What CI and CD mean and how they differ
* A typical pull request (PR) based CI workflow
* How pipelines validate integrated code and prevent regressions
* Deployment strategies for staging and production

Why CI/CD matters

* CI/CD automates verification and delivery of code changes, reducing human error and accelerating feedback.
* Using a Git hosting platform (for example, Gitea, GitHub, GitLab, Bitbucket) lets teams trigger automated pipelines on pull requests and merges.
* Primary branches (commonly `main` or `master`) are usually the source of truth for production deployments; feature branches let developers iterate without disrupting production.

In a typical project, developers create feature branches to work independently and open a pull request (or merge request) when ready. The PR triggers automated checks—unit tests, static analysis, license scanning, vulnerability scans, and artifact builds—before reviewers merge the change.

<Frame>
  <img alt="The image is a diagram explaining the CI/CD process, illustrating feature branching, committing changes, making a pull request, deployment, and production flow. It highlights the development workflow from code to deployment." />
</Frame>

Common risks when CI is missing

* Delayed testing: Tests run late and integration issues surface only after multiple merges.
* Inefficient deployments: Manual steps increase the chance of inconsistent environment states.
* Reduced quality assurance: Heavy reliance on manual testing introduces human error and bottlenecks.

> **warning** Deploying untested code directly to production is risky. Automated CI and testing reduce the likelihood of regressions and outages.

<Frame>
  <img alt="The image illustrates the need for continuous integration by showing a workflow of feature branches being committed, reviewed, and merged before manual deployment to production. Below, it highlights challenges such as delayed testing, inefficient deployment, and quality assurance issues in the absence of continuous integration." />
</Frame>

Typical PR-driven CI workflow (step-by-step)

1. Developer A creates a feature branch `feature/A`, implements changes, and opens a pull request against `main`.
2. The CI pipeline runs on the PR. Typical stages:
   * Checkout and prepare environment
   * Run unit tests
   * Static code analysis and linting
   * Dependency and license scanning
   * Build artifacts (binaries, Docker images)
   * Vulnerability scanning and security tests
3. If any check fails, the contributor updates the branch and pushes a new commit—this re-triggers the CI pipeline.
4. When checks pass and reviewers approve, merge the PR into `main`.
5. Developer B independently follows the same process with `feature/B`.

Why run CI on both PRs and `main`?

* Fast feedback: CI on the PR validates the change in isolation (often merged with the latest `main` locally) and gives quick feedback to the author and reviewers.
* Integration safety: CI on `main` after merge validates the combined state, catching race conditions or interactions with other recently merged changes.

This practice—frequent automated verification so many developers can integrate changes safely—is continuous integration.

Continuous Delivery vs Continuous Deployment

* Continuous Delivery: Every change is built, tested, and ready to deploy; a manual approval or release step promotes the change to production.
* Continuous Deployment: Every passing change is automatically deployed to production with no manual gate.

Comparison table

|               Pattern |            Production Deployment           | Typical Use Case                                                     |
| --------------------: | :----------------------------------------: | -------------------------------------------------------------------- |
|   Continuous Delivery | Manual approval required before production | Organizations needing human oversight for compliance or coordination |
| Continuous Deployment |    Automatic deployment on successful CI   | High-velocity teams confident in automated tests and monitoring      |

Deployment and validation after CI

* After `main` passes CI, deploy to a non-production environment that mirrors production (for example, staging) for live validation.
* Pipelines can also deploy feature branches to ephemeral environments for testing.
* Post-deploy tests: integration tests, end-to-end (E2E) tests, performance and load testing.
* Promotion: Once staging checks pass, either merge/tags are created to mark release artifacts, and a pipeline promotes those artifacts to production.

Recommended pipeline stages

| Stage                         | Purpose                                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| Build                         | Compile code and produce artifacts (e.g., Docker images)                                       |
| Test                          | Unit tests, integration tests, and E2E tests                                                   |
| Scan                          | Security, dependency, and license scans                                                        |
| Deploy (staging)              | Validate artifacts in an environment similar to production                                     |
| Promote / Deploy (production) | Release artifacts to customers (manual checkpoint for CD, automatic for Continuous Deployment) |

<Frame>
  <img alt="The image illustrates a continuous deployment/delivery pipeline, showing processes like feature branching, continuous integration, deployment to staging and production, unit testing, and code scanning." />
</Frame>

> **lightbulb** Continuous Delivery keeps your codebase always in a deployable state but uses a manual approval before production. Continuous Deployment automates the last step: code moves to production automatically when all checks succeed.

Further reading and references

* [Gitea](https://gitea.io) — lightweight Git hosting
* [GitHub](https://github.com), [GitLab](https://gitlab.com), [Bitbucket](https://bitbucket.org) — popular Git hosting and CI/CD platforms
* CI/CD best practices and pipeline examples:
  * Branch-per-feature workflows and PR validation
  * Use of ephemeral environments for feature testing
  * Automate as many checks as practical to reduce manual testing burden

Adopting CI/CD transforms code delivery from a risky manual process into a reliable, repeatable pipeline—improving quality, accelerating releases, and increasing team confidence.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/673786b2-bedb-4405-a2c9-835aea1a9dd4/lesson/28ade285-972f-4e49-b304-1b4a59ce29e4)
