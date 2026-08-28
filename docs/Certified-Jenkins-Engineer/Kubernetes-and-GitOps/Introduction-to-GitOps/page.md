# Fetch environment variables for a given tool via withEnv
#### REPLACE below with Kubernetes http://IP_Address:30000/api-docs/ ####
chmod 777 $(pwd)
docker run -v $(pwd):/zap/wrk:/rw ghcr.io/zaproxy/zap-api-scan.py -t http://134.209....
solar-system-gitops-argocd – Verify if file exists in workspace
rm -rf solar-system-gitops-argocd  – Shell Script
```

<Frame>
  ![The image shows a Jenkins workspace interface displaying a list of files and directories with their sizes and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752870950/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/jenkins-workspace-files-directories.jpg)
</Frame>

**Common reports and locations:**

| Report Type       | Directory / File Pattern             |
| ----------------- | ------------------------------------ |
| Code coverage     | `coverage/`                          |
| Dependency-check  | `dependency-check-report.html`, etc. |
| Unit test results | `test-results.xml`                   |
| Container scans   | `trivy*.*`                           |
| OWASP ZAP scans   | `zap*.*`                             |

***

## Creating the S3 Bucket

In the AWS S3 console, create a new bucket (e.g., `solar-system-jenkins-reports-bucket`) in **US East (Ohio)**. This bucket will house all your Jenkins reports:

<Frame>
  ![The image shows an AWS S3 console with a list of general purpose buckets, including one named "solar-system-jenkins-reports-bucket" in the US East (Ohio) region.](https://kodekloud.com/kk-media/image/upload/v1752870951/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/aws-s3-console-general-purpose-buckets.jpg)
</Frame>

***

## Configuring IAM and Jenkins Credentials

1. In AWS IAM, create or select a user with the `AmazonS3FullAccess` policy.
2. In Jenkins, go to **Credentials** and add a new **AWS Credentials** entry. Set the ID to `aws-s3-ec2-lambda-creds`.

<Frame>
  ![The image shows an AWS Identity and Access Management (IAM) console screen, displaying the permissions policies for a user, including AmazonEC2FullAccess and AmazonS3FullAccess.](https://kodekloud.com/kk-media/image/upload/v1752870952/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/aws-iam-console-user-permissions.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of stored credentials, including IDs and names for various systems and services.](https://kodekloud.com/kk-media/image/upload/v1752870953/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/jenkins-dashboard-credentials-list.jpg)
</Frame>

<Callout icon="triangle-alert">
  Do not hard-code AWS keys in your `Jenkinsfile`. Always use Jenkins Credentials and the `withAWS` wrapper.
</Callout>

***

## Installing the Pipeline: AWS Steps Plugin

Install **Pipeline: AWS Steps** via **Manage Jenkins → Manage Plugins**. This plugin provides the `s3Upload` and `withAWS` steps you’ll need.

<Frame>
  ![The image shows a webpage for the Jenkins "Pipeline: AWS Steps" plugin, detailing its features, version information, and installation statistics. It includes links to documentation, GitHub, and other resources.](https://kodekloud.com/kk-media/image/upload/v1752870954/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/jenkins-pipeline-aws-steps-plugin.jpg)
</Frame>

***

## Generating an S3 Upload Snippet

Use Jenkins’s **Snippet Generator** to preview the `s3Upload` syntax and options:

<Frame>
  ![The image shows a Jenkins interface with a "Snippet Generator" for creating pipeline scripts, displaying various options for script steps.](https://kodekloud.com/kk-media/image/upload/v1752870955/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/jenkins-snippet-generator-pipeline-scripts.jpg)
</Frame>

***

## Adding the Upload Stage to the Jenkinsfile

Add a new stage named **Upload – AWS S3** that runs only on PR branches. It will:

1. Create a `reports-$BUILD_ID` directory
2. Copy all relevant reports into it
3. Upload the folder to your S3 bucket

```groovy theme={null}
stage('Upload - AWS S3') {
  when {
    branch 'PR*'
  }
  steps {
    withAWS(credentials: 'aws-s3-ec2-lambda-creds', region: 'us-east-2') {
      sh '''
        ls -ltr
        mkdir reports-$BUILD_ID
        cp -rf coverage/ reports-$BUILD_ID/
        cp dependency* test-results.xml trivy*.* zap*.* reports-$BUILD_ID/
        ls -ltr reports-$BUILD_ID/
      '''
      s3Upload(
        file: "reports-$BUILD_ID",
        bucket: 'solar-system-jenkins-reports-bucket',
        path: "jenkins-$BUILD_ID/"
      )
    }
  }
}
```

<Callout icon="lightbulb">
  Use double quotes for Groovy string interpolation (`"reports-$BUILD_ID"`).\
  You can adjust `path:` to organize reports by job, branch, or date.
</Callout>

***

## Authenticating with AWS in the Pipeline

The `withAWS` step injects your IAM credentials and region into the build. Generate this snippet in the Snippet Generator by searching for **withAWS**.

<Frame>
  ![The image shows the AWS Identity and Access Management (IAM) console, with a search for "S3" displaying related services and features. The right side of the screen shows user details and permissions settings.](https://kodekloud.com/kk-media/image/upload/v1752870956/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/aws-iam-console-s3-search.jpg)
</Frame>

***

## Running the Pipeline

Commit and push your updated `Jenkinsfile` to trigger a build. The **Upload – AWS S3** stage should appear and complete successfully:

<Frame>
  ![The image shows a Jenkins pipeline interface for a project named "solar-system" under "Gitea-Organization," displaying various stages of a build and deployment process, all marked as completed. The interface includes details about a pull request and deployment status.](https://kodekloud.com/kk-media/image/upload/v1752870957/notes-assets/images/Certified-Jenkins-Engineer-Demo-Publish-Reports-to-AWS-S3/jenkins-pipeline-solar-system-gitea.jpg)
</Frame>

***

## Reviewing the Console Output

Inspect the logs to verify the file listing, directory creation, copy commands, and S3 upload progress:

```bash theme={null}
$ ls -ltr
...
# mkdir reports-6
# cp -rf coverage/ reports-6/
# cp dependency* test-results.xml trivy*.* zap*.* reports-6/
Uploading file:/var/lib/jenkins/workspace/.../reports-6/ to s3://solar-system-jenkins-reports-bucket/jenkins-6/
Finished: Uploading to solar-system-jenkins-reports-bucket/jenkins-6/test-results.xml
Finished: Uploading to solar-system-jenkins-reports-bucket/jenkins-6/trivy-image-CRITICAL-results.html
...
```

***

## Verifying Artifacts in S3

Head back to the S3 console and navigate into your bucket. You should see a `jenkins-<build_id>/` folder with all your copied reports.

That’s it! You’ve successfully configured your Jenkins pipeline to publish test, coverage, and security reports to Amazon S3.

***

## Links and References

* [Jenkins Pipeline: AWS Steps Plugin](https://plugins.jenkins.io/pipeline-aws/)
* [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/3b9254df-756e-4605-9508-e064e897ec5d" />
</CardGroup>


# Introduction to GitOps

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Introduction-to-GitOps/page

GitOps uses Git as the single source of truth for managing delivery lifecycles, ensuring environments match repository declarations through automation and version control.

GitOps leverages Git as the single source of truth to manage your entire delivery lifecycle—spanning infrastructure definitions, application manifests, automated deployments, and rollbacks. Building on the principles of [Infrastructure as Code](https://en.wikipedia.org/wiki/Infrastructure_as_code), GitOps uses Git’s versioning, branching, and pull-request workflows to ensure your production environment always matches what’s declared in your repository.

## Why GitOps?

* **Git-Centric Control**\
  Every change is performed via Git commits and pull requests.
* **Declarative Desired State**\
  Infrastructure and applications are described in code, making the system reproducible.
* **Automated Reconciliation**\
  A GitOps operator constantly syncs the live cluster state with the Git repository.

<Frame>
  ![The image illustrates a GitOps workflow, showing the integration of infrastructure, configuration, and application code into a Git repository, followed by continuous integration (CI) and continuous deployment (CD) processes to a Kubernetes cluster. It also depicts a branching and merging process with version control.](https://kodekloud.com/kk-media/image/upload/v1752870958/notes-assets/images/Certified-Jenkins-Engineer-Introduction-to-GitOps/gitops-workflow-integration-diagram.jpg)
</Frame>

1. **Declarative Configuration**\
   Store all infrastructure, application manifests, and configuration files in Git.
2. **Versioned and Immutable**\
   Every change is tracked. Roll back by reverting to a previous commit.
3. **Automated Delivery Pipeline**\
   A GitOps operator inside your Kubernetes cluster watches Git for updates.
4. **Continuous Reconciliation**\
   Drift detection ensures the live environment matches the desired state.

## Developer Workflow

1. Create a feature branch from `main`.
2. Update application code or Kubernetes manifests.
3. Open a pull request for review.
4. After approval, merge back into the central repository.

## CI/CD Integration

A CI system automatically:

* Runs unit and integration tests.
* Builds a Docker image and pushes it to a container registry.
* Updates the Kubernetes manifests in your Git repository.

<Frame>
  ![The image illustrates a GitOps workflow, showing the process from application code merging to continuous integration, and synchronization of Kubernetes manifests to achieve the desired state in production environments.](https://kodekloud.com/kk-media/image/upload/v1752870959/notes-assets/images/Certified-Jenkins-Engineer-Introduction-to-GitOps/gitops-workflow-ci-kubernetes.jpg)
</Frame>

## GitOps Operator Workflow

1. The operator polls (or listens for webhooks) on your Git repository.
2. Detects changes in manifests or configs.
3. Applies updates to your Kubernetes cluster (or clusters).
4. Continuously monitors live state and reconciles any drift.

<Frame>
  ![The image illustrates a GitOps workflow, showing the process from application code merging and continuous integration to Kubernetes manifest synchronization and deployment, highlighting desired and actual states.](https://kodekloud.com/kk-media/image/upload/v1752870960/notes-assets/images/Certified-Jenkins-Engineer-Introduction-to-GitOps/gitops-workflow-ci-kubernetes-2.jpg)
</Frame>

| Component          | Purpose                                     | Example Tool            |
| ------------------ | ------------------------------------------- | ----------------------- |
| Git Repository     | Single source of truth for code and configs | GitHub, GitLab          |
| GitOps Operator    | Syncs Git state to the cluster              | Argo CD, Flux           |
| CI System          | Builds, tests, and packages applications    | Jenkins, GitHub Actions |
| Container Registry | Stores Docker images                        | Docker Hub, ECR         |
| Kubernetes Cluster | Runs and orchestrates workloads             | EKS, GKE, AKS           |

Since all changes are versioned, reverting is as simple as:

```bash theme={null}
git revert <commit-hash>
```

The GitOps operator will detect the revert, pull the previous desired state, and roll back your cluster.

<Callout icon="lightbulb">
  GitOps operators typically reconcile every few seconds. If you manually change resources in your cluster, the operator will revert them to match the Git state.
</Callout>

* [Infrastructure as Code](https://en.wikipedia.org/wiki/Infrastructure_as_code)
* [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration)
* [Continuous Deployment](https://en.wikipedia.org/wiki/Continuous_deployment)
* [GitOps with Argo CD](https://argo-cd.readthedocs.io/)
* [Flux GitOps](https://fluxcd.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/584239f7-4360-4a86-b401-6a649d9f9cb7" />
</CardGroup>
