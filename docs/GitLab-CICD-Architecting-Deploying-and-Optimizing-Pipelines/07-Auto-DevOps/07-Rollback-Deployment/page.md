# Secret Detection
[INFO] GitLab secrets analyzer v5.1.19
35 commits scanned. Leaks found: 2
Job succeeded
# Test job
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit
MongoDB Connection Successful
  ✓ should return all items
  ✓ should add a new item
...
4 passing (150ms)
```

With tests green, the pipeline proceeds to **Review**.

## 9. Review Apps Stage

The **Review** stage provisions a temporary environment in your Kubernetes cluster via Helm. Auto DevOps:

1. Validates the base domain.
2. Downloads or uses the embedded Helm chart.
3. Switches to the MR namespace.
4. Creates registry secrets.
5. Deploys the review app.

In **Operations → Environments**, you’ll see your running review app:

![The image shows a GitLab interface displaying the "Environments" section, with a focus on a running job in the "feature/auto-devops" branch. The sidebar includes options like Merge requests, Manage, Plan, Code, and more.](https://kodekloud.com/kk-media/image/upload/v1752877120/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-environments-feature-auto-devops.jpg)

### 9.1. Handling Pod Crash Loops

If the review pod crashes, inspect it:

```bash theme={null}
kubectl get all -n default
kubectl describe pod review-feature-auto-devops-xxxxx -n default
kubectl logs review-feature-auto-devops-xxxxx -n default
```

You may see the same Mongoose error, which means the pod lacks the CI/CD environment variables:

```bash theme={null}
MongooseError: The `uri` parameter to `openUri()` must be a string, got "undefined".
```

Environment variables defined in GitLab CI/CD are not automatically injected into Kubernetes pods. To pass them, configure your Helm chart’s `values.yaml` or use GitLab’s [Review App variables documentation](https://docs.gitlab.com/ee/ci/review_apps/).

![The image shows a GitLab CI/CD settings page with various configuration variables such as KUBE\_CONTEXT, MONGO\_PASSWORD, and PRODUCTION\_REPLICAS. The sidebar includes options like Deploy, Operate, and Monitor.](https://kodekloud.com/kk-media/image/upload/v1752877121/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-ci-cd-settings-variables.jpg)

Because the pod fails to start, the Review job times out and a Cleanup stage is triggered:

![The image shows a GitLab pipeline interface with stages for build, test, review, performance, and cleanup. The review stage has failed, while other stages like build and test have passed.](https://kodekloud.com/kk-media/image/upload/v1752877122/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-pipeline-build-test-review-failed.jpg)

***

Up next, we’ll explore how to inject CI/CD variables into your Helm chart so that Review Apps can connect to external services like MongoDB.

## Links and References

* [GitLab Auto DevOps Documentation](https://docs.gitlab.com/ee/topics/autodevops/)
* [GitLab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)
* [Review Apps Configuration](https://docs.gitlab.com/ee/ci/review_apps/)
* [Helm Official Site](https://helm.sh/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/a6a5540f-e7d1-4820-afc8-2be1d6e3061a/lesson/2cf2a3f3-0b86-487f-ad06-d7877e2102ca)


# Rollback Deployment

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Auto-DevOps/Rollback-Deployment/page

This guide explains how to use GitLabs rollback feature to revert to a previous successful deployment, ensuring minimal downtime and restoring stability.

In this guide, you’ll learn how to use GitLab’s rollback feature to revert your environment to a previously successful release. Rollbacks are essential when a new deployment introduces regressions—such as a frozen UI—allowing you to restore stability with minimal downtime.

## Environment Rollback Overview

GitLab’s **Environment Rollback** creates a new deployment job for a selected, successful commit. Note that only the deploy stage runs; any artifacts from earlier stages (build, test) must be regenerated manually before triggering the rollback.

![The image shows a GitLab documentation page about environment rollback, detailing steps to retry or roll back a deployment. The page includes a sidebar with navigation options and a list of related topics.](https://kodekloud.com/kk-media/image/upload/v1752877124/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Rollback-Deployment/gitlab-environment-rollback-documentation.jpg)

## Step 1: Select the Deployment to Roll Back

1. In GitLab, go to **Operations → Environments**.
2. Click on your target environment (e.g., **production**).
3. Locate the list of past deployments and identify a **successful** one. Only these can be rolled back.

![The image shows a GitLab interface displaying a list of deployment jobs in a production environment, with various statuses such as "Success" and "Waiting." The sidebar includes options for managing environments and other DevOps tools.](https://kodekloud.com/kk-media/image/upload/v1752877126/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Rollback-Deployment/gitlab-deployment-jobs-interface.jpg)

4. Click **Rollback** next to the chosen deployment. You can also click **Redeploy** to reapply the same commit without changes.

## Step 2: Confirm the Rollback

When you select **Rollback**, GitLab displays a confirmation dialog indicating the commit to revert to. Verify the commit details before proceeding.

![The image shows a GitLab interface with a confirmation dialog for rolling back a production environment to a previous deployment. The dialog offers options to cancel or proceed with the rollback.](https://kodekloud.com/kk-media/image/upload/v1752877126/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Rollback-Deployment/gitlab-rollback-confirmation-dialog.jpg)

> **lightbulb** Click the commit hash in the confirmation dialog to review code changes and pipeline status before rolling back.

![The image shows a GitLab interface displaying a commit merge from a feature branch to the main branch, with details about the pipeline status and code changes.](https://kodekloud.com/kk-media/image/upload/v1752877128/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Rollback-Deployment/gitlab-commit-merge-feature-main.jpg)

## Step 3: Approve Deployment & Restore Artifacts

Once confirmed, GitLab launches a new pipeline containing only the deploy job. Other stages (build, test) are skipped, so regenerate any required artifacts first.

> **triangle-alert** Rollback pipelines do **not** rebuild artifacts. If your deployment depends on generated files, re-run those pipeline stages or upload artifacts manually before approving the rollback job.

![The image shows a GitLab interface with a job deployment to a production environment, currently waiting for approvals. It includes a sidebar with navigation options and a visual representation of the deployment process.](https://kodekloud.com/kk-media/image/upload/v1752877129/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Rollback-Deployment/gitlab-job-deployment-approvals.jpg)

Approve and run the deploy job in the GitLab UI:

```bash theme={null}
