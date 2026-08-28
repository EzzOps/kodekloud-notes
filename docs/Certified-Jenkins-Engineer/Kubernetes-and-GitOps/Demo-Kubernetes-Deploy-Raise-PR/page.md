# Demo Kubernetes Deploy Raise PR

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Demo-Kubernetes-Deploy-Raise-PR/page

This workflow automates PR creation, image updates, and GitOps-driven deployment using Jenkins and Argo CD.

In this guide, we’ll automate creating a pull request on GitHub/Gitea using a Jenkins pipeline. You’ll learn how to:

* Explore the Pull Request REST API
* Test `curl` calls in Swagger UI
* Integrate the command into a `Jenkinsfile`
* Enforce branch protection and sync with Argo CD

## Exploring the Pull Request REST API

Most Git hosting platforms expose a [REST API](https://docs.gitea.io/en-us/api-usage/) for every UI action. To create a pull request via API:

1. Navigate to your repository in the web UI.
2. Open the embedded API (Swagger) documentation.
3. Locate **Pulls** (GitHub) or **Pull Requests** (Gitea) under **Repository**.

<Frame>
  ![The image shows a list of API endpoints related to repository management, including actions like adding, deleting, and checking collaborators, as well as handling commits and contents. The interface appears to be part of a Swagger API documentation.](https://kodekloud.com/kk-media/image/upload/v1752870913/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/api-endpoints-repository-management.jpg)
</Frame>

## Creating a Pull Request via Swagger UI

Search for `pull` and expand the `POST /repos/{owner}/{repo}/pulls` endpoint to view required parameters: `owner`, `repo`, `head`, `base`, `title`, etc.

<Frame>
  ![The image shows a Gitea API interface for creating a pull request, with fields for the repository owner, name, and options for the pull request.](https://kodekloud.com/kk-media/image/upload/v1752870914/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/gitea-api-pull-request-interface.jpg)
</Frame>

Click **Try it out** and fill in:

* owner: `dasher-org`
* repo: `solar-system-gitops-argocd`
* head: feature branch (e.g., `feature-123`)
* base: `main`
* title, body, assignees, labels

<Frame>
  ![The image shows a web interface for creating a pull request using an API, with fields for specifying the repository owner, repository name, and pull request options.](https://kodekloud.com/kk-media/image/upload/v1752870915/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/pull-request-api-interface.jpg)
</Frame>

### Request Body Schema

```json theme={null}
{
  "assignee": "string",
  "assignees": ["string"],
  "base": "string",
  "body": "string",
  "due_date": "2024-09-24T17:50:33.424Z",
  "head": "string",
  "labels": [0],
  "milestone": 0,
  "title": "string"
}
```

Executing **Try it out** generates this `curl` command:

```bash theme={null}
curl -X POST "http://64.227.187.25:5555/api/v1/repos/dasher-org/solar-system-gitops-argocd/pulls" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "assignee": "string",
    "assignees": ["string"],
    "base": "string",
    "body": "string",
    "due_date": "2024-09-24T17:50:33.424Z",
    "head": "string",
    "labels": [],
    "milestone": 0,
    "title": "string"
  }'
```

<Callout icon="lightbulb">
  * **404 Not Found**: Verify the URL, `owner`, and `repo` names.
  * **401 Unauthorized**: Provide a valid API token prefixed with `token `.
</Callout>

Authorize via Swagger’s **Authorize** lock icon or add:

```bash theme={null}
-H "Authorization: token YOUR_TOKEN_HERE"
```

Example with a real token:

```bash theme={null}
curl -X POST "http://64.227.187.25:5555/api/v1/repos/dasher-org/solar-system-gitops-argocd/pulls" \
  -H "accept: application/json" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assignee": "gitea-admin",
    "assignees": ["gitea-admin"],
    "base": "main",
    "body": "Updated Docker image in deployment manifest",
    "head": "feature-123",
    "title": "Updated Docker Image"
  }'
```

## Integrating into a Jenkins Pipeline

Add the validated `curl` call to your `Jenkinsfile`. Store `GITEA_TOKEN` in [Jenkins Credentials](https://www.jenkins.io/doc/book/administration/credentials/):

```groovy theme={null}
pipeline {
  agent any
  environment {
    GITEA_TOKEN = credentials('gitea-token')
  }
  stages {
    stage('Build Docker Image') {
      steps { /* ... */ }
    }
    stage('Trivy Vulnerability Scan') {
      steps { /* ... */ }
    }
    stage('Push Docker Image') {
      steps { /* ... */ }
    }
    stage('Deploy to AWS EC2') {
      steps { /* ... */ }
    }
    stage('Integration Testing - AWS EC2') {
      steps { /* ... */ }
    }
    stage('K8S - Update Image Tag') {
      steps { /* ... */ }
    }
    stage('K8S - Raise PR') {
      when { branch 'PR*' }
      steps {
        sh """
          curl -X POST \
            "http://64.227.187.25:5555/api/v1/repos/dasher-org/solar-system-gitops-argocd/pulls" \
            -H "accept: application/json" \
            -H "Authorization: token $GITEA_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{
              "assignee": "gitea-admin",
              "assignees": ["gitea-admin"],
              "base": "main",
              "body": "Updated Docker image in deployment manifest",
              "head": "feature-${BUILD_ID}",
              "title": "Updated Docker Image"
            }'
        """
      }
    }
  }
  post {
    always { /* notifications, cleanup */ }
  }
}
```

The `when { branch 'PR*' }` condition runs this stage only on branches matching `PR*`. After you push, Jenkins will auto-create a PR:

<Frame>
  ![The image shows a pull request interface with a list of commits and their statuses, including checks and dependencies. Some checks are pending, and there is an option to create a merge commit.](https://kodekloud.com/kk-media/image/upload/v1752870917/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/pull-request-commits-statuses-checks.jpg)
</Frame>

## Enforcing Branch Protection

To require successful Jenkins builds before merging:

| Step | Action                                                                                 |
| ---- | -------------------------------------------------------------------------------------- |
| 1    | In your repo, go to **Settings > Branches**.                                           |
| 2    | Click **Add rule** for branch pattern `main`.                                          |
| 3    | Enable **Require status checks to pass before merging** and select your Jenkins check. |

<Callout icon="triangle-alert">
  Activating branch protection prevents direct pushes and enforces CI gates before merges.
</Callout>

<Frame>
  ![The image shows a web interface for setting branch protection rules in a repository, with options for protected branch name patterns and file patterns.](https://kodekloud.com/kk-media/image/upload/v1752870918/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/branch-protection-rules-interface.jpg)
</Frame>

## Verifying the Pull Request and Merge

Review and merge your PR into `main`:

<Frame>
  ![The image shows a pull request titled "Updated Docker Image #1" on a code repository platform, with details about commits and options to merge the request.](https://kodekloud.com/kk-media/image/upload/v1752870919/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/updated-docker-image-pull-request.jpg)
</Frame>

Argo CD will detect the updated image tag (within \~3 minutes) and sync:

```diff theme={null}
- image: siddharth67/solar-system:3e906e3be95342b1916f202c034344fb267dca
+ image: siddharth67/solar-system:946c630393e77939c920a6fab782e4c53d27
```

<Frame>
  ![The image shows an Argo CD application dashboard displaying the status and structure of a "solar-system-argo-app" with components like services, deployments, and pods, all marked as healthy and synced.](https://kodekloud.com/kk-media/image/upload/v1752870921/notes-assets/images/Certified-Jenkins-Engineer-Demo-Kubernetes-Deploy-Raise-PR/argo-cd-solar-system-dashboard.jpg)
</Frame>

## Accessing the Application

After sync completes, list Kubernetes resources:

```bash theme={null}
kubectl get all -n solar-system
```

Locate the NodePort service and browse to:

```text theme={null}
http://<NODE_IP>:30000
```

You should see the Solar System app connected to MongoDB.

## Inspecting the Sealed Secret

Bitnami [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) decrypts your sealed YAML into a regular `Secret`:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: mongo-db-creds
  namespace: solar-system
  annotations:
    sealedsecrets.bitnami.com/cluster-wide: 'true'
type: Opaque
data:
  MONGO_USERNAME: "++++++++"
  MONGO_PASSWORD: "++++++++"
  MONGO_URI: "++++++++"
```

Retrieve it with:

```bash theme={null}
kubectl get secret mongo-db-creds -n solar-system -o yaml
```

This workflow automates PR creation, image updates, and GitOps-driven deployment using Jenkins and Argo CD.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/8823deeb-9cbd-476f-a8e9-49780e77d0ff" />
</CardGroup>
