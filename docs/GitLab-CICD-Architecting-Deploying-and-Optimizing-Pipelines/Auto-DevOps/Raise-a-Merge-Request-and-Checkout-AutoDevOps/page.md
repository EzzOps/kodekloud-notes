# Key: K8S_SECRET_MONGO_URI
# Value: mongodb://mongo.example.com:27017
# Key: K8S_SECRET_MONGO_USERNAME
# Value: appuser
# Key: K8S_SECRET_MONGO_PASSWORD
# Value: superpassword
```

## 3. Cleaning Up the Default Namespace

Before re-running the review job, remove any leftover review resources:

```bash theme={null}
kubectl get all -n default
kubectl get secret -n default

# Delete old review secret if present
kubectl delete secret review-feature-<ID>-secret -n default

kubectl get secret -n default
# No resources found
```

<Callout icon="triangle-alert">
  Ensure you’re only deleting review-specific secrets. Running deletions in `default` can impact other workloads.
</Callout>

## 4. Rerunning and Monitoring the Review Job

Trigger the review job again in GitLab or via API. Then inspect:

```bash theme={null}
kubectl get all -n default
kubectl logs review-feature-<ID>-xxxxx -n default
```

The app will start and connect to MongoDB successfully:

```plaintext theme={null}
Server successfully running on port - 3000
MongoDB Connection Successful
```

However, the liveness and readiness probes still fail.

## 5. Diagnosing Probe Failures

Describe the pod to view probe errors:

```bash theme={null}
kubectl describe pod review-feature-<ID>-xxxxx -n default
```

<Frame>
  ![The image shows a terminal window displaying Kubernetes pod events and status messages, including scheduling, container creation, and liveness probe failures.](https://kodekloud.com/kk-media/image/upload/v1752877098/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/kubernetes-pod-events-status-terminal.jpg)
</Frame>

By default, Auto DevOps probes port `5000`, but your app listens on `3000`:

```javascript theme={null}
// app.js
app.listen(3000, () => {
  console.log("Server successfully running on port - " + 3000);
});
```

## 6. Troubleshooting Auto DevOps Timeouts

Auto DevOps may report a “timed out waiting for the condition” error due to mismatched probe ports:

<Frame>
  ![The image shows a GitLab documentation page about troubleshooting an error related to Auto DevOps deployment, specifically a "timed out waiting for the condition" error. It includes explanations and steps to resolve the issue.](https://kodekloud.com/kk-media/image/upload/v1752877099/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-auto-devops-troubleshooting-error.jpg)
</Frame>

The Helm chart defaults to port `5000` for readiness and liveness:

<Frame>
  ![The image shows a GitLab documentation page about troubleshooting Auto DevOps, specifically addressing issues with liveness and readiness probes during deployment. It includes instructions on changing port values in a Helm chart.](https://kodekloud.com/kk-media/image/upload/v1752877100/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-auto-devops-troubleshooting.jpg)
</Frame>

## 7. Customizing the Helm Chart Values

Create a `.gitlab/auto-deploy-values.yaml` at the root of your branch to override the probe ports:

<Frame>
  ![The image shows a GitLab documentation page about customizing Helm chart values, with navigation menus on the left and related topics on the right.](https://kodekloud.com/kk-media/image/upload/v1752877102/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-customizing-helm-chart-values.jpg)
</Frame>

You can refer to all available Kubernetes options here:

<Frame>
  ![The image shows a GitLab repository interface with a list of configuration options related to Kubernetes deployment, such as dnsConfig, nodeSelector, and securityContext. The left sidebar includes navigation options like Issues, Merge requests, and Repository.](https://kodekloud.com/kk-media/image/upload/v1752877103/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-repo-kubernetes-config-options.jpg)
</Frame>

Example `auto-deploy-values.yaml`:

```yaml theme={null}
service:
  internalPort: 3000
  externalPort: 3000
```

Commit and push to trigger a new pipeline.

## 8. Verifying the Updated Pipeline

After pushing, your pipeline will rerun with the correct ports:

<Frame>
  ![The image shows a GitLab interface displaying a list of CI/CD pipelines with their statuses, such as "Running," "Failed," and "Canceled." The sidebar includes options like "Issues," "Merge requests," and "Pipelines."](https://kodekloud.com/kk-media/image/upload/v1752877104/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-cicd-pipelines-status-interface.jpg)
</Frame>

You can cancel unneeded jobs (e.g., Code Quality, SAST) to speed up **build**, **test**, and **review**.

## 9. Successful Deployment to Review Environment

Once the review job succeeds, you’ll see the application URL:

```plaintext theme={null}
Using helm values file '.gitlab/auto-deploy-values.yaml'
Release "review-feature-<ID>" does not exist. Installing it now.
…
NOTES:
Application should be accessible at
http://<random>-review-feature-<ID>.<cluster-domain>.nip.io/
```

Verify with Kubernetes:

```bash theme={null}
kubectl get pods -n default
kubectl get ingress -n default
```

## 10. Auto Browser Performance Testing

After deployment, Auto DevOps launches **Auto Browser Performance Testing** using sitespeed.io:

<Frame>
  ![The image shows a GitLab documentation page about "Auto Browser Performance Testing," detailing how it measures browser performance using a specific container and generates a JSON report. The page includes navigation links on the left and a table of contents on the right.](https://kodekloud.com/kk-media/image/upload/v1752877104/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-auto-browser-performance-testing.jpg)
</Frame>

The job runs:

```bash theme={null}
sitespeed.io $CI_ENVIRONMENT_URL --outputFolder sitespeed-results
```

Inspect the artifact files:

<Frame>
  ![The image shows a GitLab interface displaying a list of files and directories within a project called "Solar System AutoDevOps," including HTML files and folders like "css," "data," and "img."](https://kodekloud.com/kk-media/image/upload/v1752877105/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-solarsystem-autodevops-files.jpg)
</Frame>

Open the main HTML report to view asset analysis:

<Frame>
  ![The image shows a webpage analysis report from sitespeed.io, listing various assets with details like type, time since last modified, cache time, size, and count.](https://kodekloud.com/kk-media/image/upload/v1752877106/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/webpage-analysis-report-sitespeedio.jpg)
</Frame>

See detailed performance metrics by domain:

<Frame>
  ![The image shows a performance analysis report from sitespeed.io for a specific webpage, detailing metrics like DNS, connect, send, SSL, wait, receive, total time, and requests for various domains.](https://kodekloud.com/kk-media/image/upload/v1752877107/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/sitespeed-performance-analysis-report.jpg)
</Frame>

## 11. Manual Stop Review and Cleanup

When you’re done, manually trigger the **Stop Review** job to delete all review resources:

<Frame>
  ![The image shows a GitLab pipeline interface with stages for build, test, review, performance, and cleanup. Each stage contains various jobs, some of which are marked as completed.](https://kodekloud.com/kk-media/image/upload/v1752877108/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-pipeline-interface-stages.jpg)
</Frame>

In **Pipelines**, click **Stop Review**:

<Frame>
  ![The image shows a GitLab interface indicating a job that requires manual action, with options to input CI/CD variables and a "Run job" button. The sidebar includes project management options like "Manage," "Plan," "Code," and more.](https://kodekloud.com/kk-media/image/upload/v1752877109/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-manual-action-job-interface.jpg)
</Frame>

This job removes the Helm release, pods, secrets, and ingress:

```bash theme={null}
kubectl get all -n default
# Should show only core resources
kubectl get secret -n default  # No secrets
kubectl get ingress -n default # No ingress
```

## 12. Reviewing Deployment History

Finally, view the stopped environment and its deployment jobs for auditing:

<Frame>
  ![The image shows a GitLab environment page displaying a list of deployment jobs with their statuses, IDs, commit messages, and timestamps. The sidebar includes navigation options like "Merge requests," "Manage," "Plan," and "Environments."](https://kodekloud.com/kk-media/image/upload/v1752877110/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-deployment-jobs-statuses.jpg)
</Frame>

## Links and References

* [GitLab CI/CD Variables Documentation](https://docs.gitlab.com/ee/ci/variables/)
* [Auto DevOps Configuration](https://docs.gitlab.com/ee/topics/autodevops/)
* [Kubernetes Probes](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)
* [Helm Chart Values](https://helm.sh/docs/chart_template_guide/values_files/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/a6a5540f-e7d1-4820-afc8-2be1d6e3061a/lesson/4a4d754b-3246-43be-b452-3e95c5f6557d" />
</CardGroup>


# Raise a Merge Request and Checkout AutoDevOps

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Auto-DevOps/Raise-a-Merge-Request-and-Checkout-AutoDevOps/page

Learn to create a feature branch, submit a Merge Request in GitLab, and observe Auto DevOps pipeline stages for MR workflows.

In this lesson, you’ll learn how to create a feature branch, submit a Merge Request (MR) in GitLab, and observe how Auto DevOps adapts its pipeline stages for MR workflows. By the end, you’ll see Review and Cleanup stages in action and understand how to inject CI/CD variables into review environments.

## 1. Inspect the Initial Auto DevOps Pipeline on `main`

Once Auto DevOps is enabled, the pipeline for `main` runs standard stages—Build, Test, Production, and Performance—though the Build stage may be canceled if it’s already succeeded elsewhere:

<Frame>
  ![The image shows a GitLab pipeline interface with stages for build, test, production, and performance, where the build stage is canceled.](https://kodekloud.com/kk-media/image/upload/v1752877111/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-pipeline-build-canceled.jpg)
</Frame>

## 2. Create a Feature Branch and Update Your Code

1. Open `app.js` in your editor.
2. Uncomment the `console.log` callback in `mongoose.connect`.
3. Extend the Mongoose schema by adding a `description` field:

```javascript theme={null}
const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const path = require('path');

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '/')));
app.use(cors());

mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
}, function(err) {
  if (err) {
    console.log("error!! " + err);
  } else {
    console.log("MongoDB Connection Successful");
  }
});

const Schema = mongoose.Schema;
const dataSchema = new Schema({
  name: String,
  id: Number,
  description: String
});

module.exports = app;
```

Now commit and push your changes on a new feature branch:

```bash theme={null}
git checkout -b feature/auto-devops
git add app.js
git commit -m "Update app.js: add description and enable console.log"
git push -u origin feature/auto-devops
```

## 3. Open a Merge Request in GitLab

1. Go to your project in GitLab.
2. Click **Merge Requests → New Merge Request**.
3. Select `feature/auto-devops` as the source and `main` as the target.
4. Fill in the title, description, assign reviewers, and click **Create Merge Request**.

<Frame>
  ![The image shows a GitLab interface where a new merge request is being created, with fields for the title and description of the request. The sidebar displays project management options like issues and merge requests.](https://kodekloud.com/kk-media/image/upload/v1752877112/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-merge-request-interface.jpg)
</Frame>

After creating the MR, the previous pipeline is canceled. Click **Retry** on canceled jobs to trigger a fresh MR pipeline:

<Frame>
  ![The image shows a GitLab interface with a merge request titled "Update app.js for testing autodevops." The request is open, but the pipeline was canceled, and there is a merge conflict that needs resolution.](https://kodekloud.com/kk-media/image/upload/v1752877114/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-merge-request-autodevops-conflict.jpg)
</Frame>

## 4. Observe the Auto DevOps Pipeline for the MR

A new pipeline runs on your feature branch. In addition to Build, Test, Production (swapped for Review), and Performance, you’ll see **Review** and **Cleanup** stages:

| Stage       | Purpose                                          | Trigger   |
| ----------- | ------------------------------------------------ | --------- |
| Build       | Package the application into a container         | commit/MR |
| Test        | Run code quality, security scans, and unit tests | commit/MR |
| Review      | Deploy a temporary review app                    | MR        |
| Performance | Execute browser and load tests                   | commit/MR |
| Cleanup     | Tear down review app                             | after MR  |

<Frame>
  ![The image shows a GitLab pipeline interface with stages for building, testing, reviewing, performance, and cleanup. It includes various jobs like code quality, container scanning, and browser performance.](https://kodekloud.com/kk-media/image/upload/v1752877114/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-pipeline-interface-stages.jpg)
</Frame>

## 5. Build Stage (`Auto Build`)

Auto DevOps uses your Dockerfile if present, otherwise it falls back to Cloud Native Buildpacks:

<Frame>
  ![The image shows a GitLab documentation page about the stages of Auto DevOps, specifically focusing on the "Auto Build" section. It includes navigation menus on the left and right sides.](https://kodekloud.com/kk-media/image/upload/v1752877116/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-autodevops-auto-build-docs.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab documentation page about "Auto Build using Cloud Native Buildpacks," detailing how to build applications using Dockerfiles and Cloud Native Buildpacks. The page includes navigation menus on the left and right sides.](https://kodekloud.com/kk-media/image/upload/v1752877117/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-auto-build-cloud-native-buildpacks.jpg)
</Frame>

Trimmed logs from the build job:

```bash theme={null}
Running with gitlab-runner 16.6.0 on docker+machine executor
Starting service docker:20.10.12-dind ...
Logging in to GitLab Container Registry...
Login Succeeded
Building Cloud Native Buildpack-based application:
  DETECTING heroku/nodejs-engine 2.5, nodejs-npm-install 2.6
  BUILDING Node.js@20.11.0, npm ci --production=false
  EXPORTING image 'tmp-cnb-image-6136662405'
Pushing image to registry.gitlab.com/demos-group/solar-system-autodevops:feature-auto-devops
Job succeeded
```

## 6. Test Stage and Template Jobs

Auto DevOps runs several parallel test jobs:

* Code Quality
* Container Scanning
* Dependency Scanning
* SAST
* Secret Detection
* Semgrep
* Test (your Mocha suite)

All templates pass except **Test**, which fails due to missing MongoDB environment variables:

<Frame>
  ![The image shows a GitLab pipeline interface with a failed job in the "test" stage, specifically the "test" task, due to a script failure. The pipeline includes stages for build, test, review, performance, and cleanup.](https://kodekloud.com/kk-media/image/upload/v1752877118/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-pipeline-failed-test-job.jpg)
</Frame>

### 6.1. Understanding the Test Failure

```bash theme={null}
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit

MongooseError: The uri parameter to `openUri()` must be a string, got "undefined".
Make sure the first parameter to mongoose.connect() or mongoose.createConnection() is a string.
```

<Callout icon="lightbulb">
  The error indicates that `MONGO_URI` (and related credentials) are not defined in CI.
</Callout>

## 7. Define CI/CD Variables in GitLab

Add your MongoDB credentials (and enable historic secret scanning) under **Settings → CI/CD → Variables**:

| Variable Name                     | Value                    |
| --------------------------------- | ------------------------ |
| MONGO\_URI                        | `mongodb://<host>:27017` |
| MONGO\_USERNAME                   | `superuser`              |
| MONGO\_PASSWORD                   | `superpassword`          |
| SECRET\_DETECTION\_HISTORIC\_SCAN | `true`                   |

<Frame>
  ![The image shows a GitLab CI/CD settings page with various environment variables listed, such as KUBE\_INGRESS\_BASE\_DOMAIN and MONGO\_PASSWORD. A notification at the bottom indicates a variable has been successfully added.](https://kodekloud.com/kk-media/image/upload/v1752877119/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Raise-a-Merge-Request-and-Checkout-AutoDevOps/gitlab-ci-cd-settings-environment-variables.jpg)
</Frame>

<Callout icon="triangle-alert">
  Ensure sensitive values like `MONGO_PASSWORD` are **protected** and **masked** in GitLab to prevent exposure.
</Callout>

## 8. Rerun Jobs and Verify Test Success

Rather than rerunning the whole pipeline, retry the **Secret Detection** and **Test** jobs:

```bash theme={null}
