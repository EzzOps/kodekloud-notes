# Update the application with latest change and validating image tags

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Task-definition-Image-tags-in-production-and-Load-Balancer/Update-the-application-with-latest-change-and-validating-image-tags/page

Demonstrates updating an app UI, running CI/CD to build and push Docker images to ECR, updating ECS service, and tracing deployed image back to the Git commit hash

Welcome back. In this lesson you'll make a small UI change, push it through your CI/CD pipeline, confirm a new Docker image has been produced and pushed to Amazon ECR, update the Amazon ECS service to use the new task definition, and finally trace the running container image back to the originating Git commit.

We’ll cover:

* Editing the application source in Cloud9
* Committing and pushing the change to CodeCommit
* Starting a build in CodeBuild that builds and pushes an image to ECR
* Updating the ECS service to use the new task definition revision
* Verifying the running application and tracing the image back to the commit hash

<Callout icon="lightbulb">
  This walkthrough demonstrates why tagging Docker images with the Git commit hash (in addition to or instead of `latest`) is critical for traceability and safe rollbacks.
</Callout>

## 1) Edit the application in Cloud9

* In the Cloud9 editor open `templates/login.html`.
* Replace the existing heading (for example `LOGIN`) with the new heading `LOGIN V2` and save the file.

Example change inside `templates/login.html`:

```html theme={null}
<h2 class="login-title">LOGIN</h2>
<!-- updated to -->
<h2 class="login-title">LOGIN V2</h2>
```

## 2) Commit and push the change from the Cloud9 terminal

From your Cloud9 environment, stage, commit, and push to the CodeCommit repository:

```bash theme={null}
cd ~/environment/aws/aws-microservice-project
