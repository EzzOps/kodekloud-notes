# edit README.md
git add README.md
git commit -m "Edited README"
git push origin main
```

The webhook notifies Jenkins, triggering a new build:

<Frame>
  ![The image shows a Jenkins dashboard displaying the status of a pipeline job, with stages like "Checkout SCM," "Build," and "Test" marked as completed. It also includes a test result trend graph and build history.](https://kodekloud.com/kk-media/image/upload/v1752871048/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-Organization-Folder-Project/jenkins-dashboard-pipeline-status-2.jpg)
</Frame>

<Callout icon="triangle-alert">
  Ensure your Gitea API token has permissions to create webhooks and read repositories.
</Callout>

***

## Conclusion

After adding a `Jenkinsfile` to the `solar-system` repository, Jenkins picks it up in the next scan and automatically creates a pipeline:

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of jobs with their statuses, last success, last failure, and duration details.](https://kodekloud.com/kk-media/image/upload/v1752871049/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-Organization-Folder-Project/jenkins-dashboard-job-statuses-2.jpg)
</Frame>

***

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Gitea Documentation](https://docs.gitea.io/)
* [Gitea Plugin for Jenkins](https://plugins.jenkins.io/gitea/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/73d0066f-a01f-4d13-a00c-c9baf9aae603/lesson/bc021ff4-53fe-4109-a393-5da33f5bde18" />
</CardGroup>


# Demo Fixing Vulnerabilities Publish HTML Report

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Setting-up-CI-Pipeline/Demo-Fixing-Vulnerabilities-Publish-HTML-Report/page

Learn to fix vulnerabilities and publish HTML and JUnit reports in Jenkins for improved visibility and compliance tracking.

In this walkthrough, you’ll learn how to address critical vulnerabilities flagged by `npm audit` and OWASP Dependency-Check, then expose the HTML and JUnit reports in your Jenkins pipeline for better visibility and compliance tracking.

## 1. Identify Failing Dependency Scans

First, run an audit locally to pinpoint blocking issues:

```bash theme={null}
npm audit --audit-level=critical
```

Example output:

```bash theme={null}
@babel/traverse <7.23.2
Severity: critical
Babel vulnerable to arbitrary code execution when compiling specifically crafted malicious code - https://github.com/advisories/GHSA-67hx-6x53-jw92
...
8 vulnerabilities (2 moderate, 5 high, 1 critical)
To address all issues, run:
npm audit fix
```

In Jenkins, the **Dependency Scanning** stage may look like this:

```groovy theme={null}
stage('Dependency Scanning') {
  parallel {
    stage('NPM Dependency Audit') {
      steps {
        sh '''
          npm audit --audit-level=critical
          echo $?
        '''
      }
    }
  }
}
```

## 2. Fix the Critical Vulnerability

To resolve the critical issue in `@babel/traverse`, install a version ≥ 7.23.2:

```bash theme={null}
npm install @babel/traverse@^7.23.2
```

Re-run the audit to confirm the fix:

```bash theme={null}
npm audit --audit-level=critical && echo $?
