# Example output:
# production-canary-77cbf87488-2x5jm   1/1 Running
# production-defd6d64cf-4qgl7          1/1 Running
```

Traffic splits according to ingress weights configured in each rollout step.

<Frame>
  ![The image shows a GitLab pipeline interface for a customized AutoDevOps job, displaying stages like build, test, and incremental rollout with various completion statuses.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877065/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-pipeline-autodevops-job-2.jpg)
</Frame>

## Approving Protected Deployments

Protected environments halt deployments until manual approval:

<Frame>
  ![The image shows a GitLab interface with a job deployment process waiting for approvals. It includes a sidebar with navigation options and a message about deploying to a protected environment.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877066/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-job-deployment-approvals-interface.jpg)
</Frame>

Click **Approve** in the confirmation dialog:

<Frame>
  ![The image shows a GitLab interface with a pop-up window for approving or rejecting a deployment. The user is about to approve deployment #14 with a comment "ok."](../../../../images/kodekloud.com/kk-media/image/upload/v1752877067/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-deployment-approval-popup.jpg)
</Frame>

Then trigger any manual rollout jobs if required:

<Frame>
  ![The image shows a GitLab interface indicating that a job requires manual action to start, with options to input CI/CD variable keys and values. It includes a "Run job" button and a sidebar with navigation options like Issues, Merge requests, and Pipelines.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877068/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-manual-action-job-interface.jpg)
</Frame>

Or use an unscheduled manual action:

<Frame>
  <img alt="The image shows a GitLab interface with a job requiring manual action for deployment. It includes options to input CI/CD variables and a &#x22;Run job&#x22; button." />
</Frame>

## Monitoring Environments

View all deployments and their statuses under **Operations > Environments**:

<Frame>
  ![The image shows a GitLab environment dashboard with details of deployment jobs, including their status, triggers, and branches. The sidebar displays various project management options like "Manage," "Plan," and "Code."](../../../../images/kodekloud.com/kk-media/image/upload/v1752877069/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-dashboard-deployment-jobs.jpg)
</Frame>

***

For more details, see the [Auto DevOps documentation](/help/topics/autodevops) or explore these resources:

* [GitLab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)
* [Kubernetes CLI Overview](https://kubernetes.io/docs/reference/kubectl/overview/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/a6a5540f-e7d1-4820-afc8-2be1d6e3061a/lesson/4dd5f4d8-cfc4-402e-a785-0ced134f1a6b" />
</CardGroup>


# Automatic Deployment to Production Environment

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Auto-DevOps/Automatic-Deployment-to-Production-Environment/page

This article explains how to automate application deployment to a production environment using GitLabs CI/CD pipelines.

In this lesson, we’ll automate the deployment of our application to the `production` environment by merging a feature branch into `main`. Previously, we ran the pipeline in the feature branch and verified deployment to the review stage using Auto DevOps. Now, accepting the merge request will trigger a new pipeline on `main`.

## 1. Merge Feature Branch into Main

First, confirm that all review jobs have passed:

<Frame>
  ![The image shows a GitLab pipeline interface with stages for build, test, review, performance, and cleanup, indicating the status of various jobs. Each stage has a green checkmark, suggesting successful completion.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877069/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-pipeline-interface-stages.jpg)
</Frame>

Open the merge request, uncheck **Delete source branch**, and click **Merge** to push your changes to `main`:

<Frame>
  ![The image shows a GitLab merge request page for updating "app.js" for testing autodevops, with a pipeline that passed with warnings. The request is ready to merge, and approval is optional.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877070/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-merge-request-appjs-autodevops.jpg)
</Frame>

## 2. Monitor the Pipeline on Main

Navigate to **CI/CD > Pipelines** to see the new run:

<Frame>
  ![The image shows a GitLab pipeline dashboard with various pipeline statuses such as running, warning, canceled, and failed, along with details about each pipeline.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877071/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-pipeline-dashboard-statuses.jpg)
</Frame>

The `main` pipeline executes the following stages:

| Stage       | Purpose                            |
| ----------- | ---------------------------------- |
| build       | Compile code and build artifacts   |
| test        | Run unit and integration tests     |
| production  | Deploy to the production namespace |
| performance | Execute browser performance tests  |

<Callout icon="lightbulb">
  To speed up demos, cancel the test jobs manually once they start.
</Callout>

## 3. Validate Production Deployment

Ensure that the `production` namespace is empty before deployment:

```bash theme={null}
kubectl get all -n production
```

When the **production** stage completes, you’ll see logs indicating Helm deployment and artifact uploads:

```bash theme={null}
$ auto-deploy delete canary
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /builds/.../KUBECONFIG
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /builds/.../KUBECONFIG

$ auto-deploy persist_environment_url
Uploading artifacts for successful job
environment_url.txt: found 1 matching artifact files and directories
WARNING: tiller.log: no matching files. Ensure that the artifact path is relative to the working directory (/builds/...)
Uploading artifacts as "archive" to coordinator... 201 Created
Job succeeded
```

<Callout icon="triangle-alert">
  The warnings above show that your `KUBECONFIG` file has overly permissive access. Restrict file permissions to prevent security issues.
</Callout>

Next, verify that 10 replicas are running (the count is driven by a CI/CD variable):

```bash theme={null}
kubectl get all -n production
```

```plaintext theme={null}
NAME                                           READY   STATUS    RESTARTS   AGE
pod/production-df6dd64cf-2p8b6                 1/1     Running   0          2m22s
… (8 more pods) …

NAME                              TYPE        CLUSTER-IP   PORT(S)    AGE
service/production-auto-deploy    ClusterIP   10.104.1.52  3000/TCP   2m22s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/production   10/10   10           10          2m22s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/production-df6dd64cf       10        10        10      2m22s
```

## 4. Test Load Balancing

Confirm traffic distribution across all replicas by curling the `/os` endpoint repeatedly:

```bash theme={null}
while true; do
  curl -sk https://demos-group-solar-system-autodevops.139.84.208.48.nip.io/os \
    | grep --color -E 'production|canary'
done
```

You’ll see different pod names in the responses, verifying round-robin load balancing.

## 5. Performance Testing

After **production**, the pipeline automatically runs browser performance benchmarks and archives the results:

<Frame>
  ![The image shows a GitLab pipeline interface with stages for build, test, production, and performance, displaying the status of various jobs. The sidebar includes options like Pipelines, Jobs, and Pipeline editor.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877073/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-pipeline-interface-stages-2.jpg)
</Frame>

## 6. Reviewing Auto DevOps Settings

In your project, go to **Settings > CI/CD**, then expand **Auto DevOps** to review deployment strategies. We used Continuous Deployment to production in this lesson:

<Frame>
  ![The image shows a GitLab CI/CD settings page with options for configuring Auto DevOps pipelines and deployment strategies. The sidebar includes various menu options like Deploy, Operate, and Monitor.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877074/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-cicd-auto-devops-settings.jpg)
</Frame>

## 7. Exploring Dashboards and Reports

Auto DevOps generates code quality, SAST, and secret detection artifacts. On the free tier, download these from **Job Artifacts**. With [Premium/Ultimate plans](https://about.gitlab.com/pricing/), you can view reports directly:

* **Security Dashboard**: Aggregated vulnerability findings
* **Operations Dashboard**: Live environment and deployment status

### Vulnerability Report

From the top menu, choose **Security & Compliance > Vulnerability report**:

<Frame>
  ![The image shows a GitLab project dashboard with a list of projects and a sidebar menu. A dropdown menu is open, highlighting the "Vulnerability report" option.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877075/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-project-dashboard-vulnerability-report.jpg)
</Frame>

### Environments Dashboard

Add multiple projects to an **Environments Dashboard** (Premium/Ultimate only):

<Frame>
  ![The image shows a GitLab interface where a user is adding projects to an "Environments Dashboard," with several projects related to "Solar System" listed.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877076/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-environments-dashboard-solar-system.jpg)
</Frame>

Attempting to include private projects on the free tier results in an error:

<Frame>
  ![The image shows a GitLab interface displaying a merge request for updating "app.js" to test autodevops. It includes pipeline details, merge information, and user interactions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877077/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Automatic-Deployment-to-Production-Environment/gitlab-merge-request-appjs-autodevops-2.jpg)
</Frame>

We recommend exploring these dashboards with a trial Ultimate account and configuring manual approvals for production deployments.

## Links and References

* [GitLab Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/)
* [GitLab CI/CD Pipelines](https://docs.gitlab.com/ee/ci/pipelines/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/a6a5540f-e7d1-4820-afc8-2be1d6e3061a/lesson/3cea8695-94eb-4224-908d-7519cf739f3e" />
</CardGroup>
