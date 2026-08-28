# View revision history for your application
argocd app history <app-name>

# Roll back to a specific revision
argocd app rollback <app-name> <revision-number>
```

This reapplies the manifest from the chosen revision, restoring your cluster to that state.

<Frame>
  ![The image illustrates a CI/CD pipeline with GitOps, showing the flow from application code repository through continuous integration, updating Kubernetes manifests, and synchronizing with a production cluster using ArgoCD.](https://kodekloud.com/kk-media/image/upload/v1752870881/notes-assets/images/Certified-Jenkins-Engineer-CICD-with-GitOps/ci-cd-pipeline-gitops-argocd.jpg)
</Frame>

## Demo Preview

In the upcoming demos, you will:

* Create a **[Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)** defining all pipeline stages
* Open a pull request to update the Kubernetes manifests repository
* Watch ArgoCD synchronize changes and perform rollbacks if necessary

***

## Links and References

* [Kubernetes Objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
* [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/494c9ccc-8e37-4b46-a891-d4c124a05f6d" />
</CardGroup>


# Demo DAST Ignore Rules

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Demo-DAST-Ignore-Rules/page

This article explains how to configure OWASP ZAP to ignore specific DAST warnings in a Jenkins pipeline.

In this walkthrough, we'll adapt our Dynamic Application Security Testing (DAST) with **OWASP ZAP** to ignore a specific warning—“Unexpected Content-Type”—so that the Jenkins build can proceed uninterrupted.

***

## 1. Identify the Unexpected-Content-Type Warning

Run the standard ZAP API scan:

```bash theme={null}
chmod 777 "$(pwd)"
docker run -v "$(pwd)":/zap/wrk/:rw ghcr.io/zaproxy/zap-api-scan.py \
  -t http://134.209.155.222:30000/api-docs/ \
  -f openapi \
  -r zap_report.html \
  -w zap_report.md \
  -J zap_json_report.json \
  -x zap_xml_report.xml
```

You’ll see:

```text theme={null}
WARN: NEW: Unexpected Content-Type was returned [100001]
```

Normally this requires a code fix, but for demo purposes we’ll instruct ZAP to **ignore** this rule.

***

## 2. Generate and Customize the ZAP Rule Configuration

ZAP supports three levels for each rule:

| Level  | Behavior                              |
| ------ | ------------------------------------- |
| FAIL   | Treat as error and exit non-zero      |
| WARN   | Report warning but continue (default) |
| IGNORE | Skip reporting the rule entirely      |

1. **Generate the default config**:

   ```bash theme={null}
   docker run --rm ghcr.io/zaproxy/zap-api-scan.py -g zap_default.conf
   ```

2. **Open** `zap_default.conf`—you’ll see lines like:

   ```text theme={null}
   0       WARN (Directory Browsing - Active/release)
   10019   WARN (Content-Type Header Missing - Passive/release)
   ...
   ```

3. **Modify** or **add** the entry for rule **100001** with single tabs:

   ```text theme={null}
   100001<TAB>IGNORE<TAB>http://134.209.155.222:30000/api-docs/
   ```

4. **Save** this as `zap_ignore_rules`.

<Callout icon="lightbulb">
  Be sure to use **single tab** separators. Mixing spaces or multiple tabs will cause parsing errors.
</Callout>

***

## 3. Update Your Jenkins Pipeline

In your `Jenkinsfile`, add the `-c zap_ignore_rules` flag to the DAST stage:

```groovy theme={null}
stage('DAST - OWASP ZAP') {
    when { branch 'PR*' }
    steps {
        sh '''
        chmod 777 "$(pwd)"
        docker run -v "$(pwd)":/zap/wrk/:rw ghcr.io/zaproxy/zap-api-scan.py \
          -t http://134.209.155.222:30000/api-docs/ \
          -f openapi \
          -r zap_report.html \
          -w zap_report.md \
          -J zap_json_report.json \
          -x zap_xml_report.xml \
          -c zap_ignore_rules
        '''
    }
    post {
        always {
            publishHTML(
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: './',
                reportFiles: 'zap_report.html',
                reportName: 'DAST - OWASP ZAP Report'
            )
        }
    }
}
```

***

## 4. (Optional) Front-End Cosmetic Change for Demo

Add extra rockets in `index.html` to visualize a change in your application:

```html theme={null}
<body>
  <div>
    <a href="index.html">
      <button style="font-size:40px;">
        <i class="fa fa-rocket"></i> SOLAR <i class="fa fa-rocket"></i> SYSTEM
      </button>
    </a>
  </div>
</body>
```

***

## 5. Commit, Merge, and Sync with Argo CD

1. Commit your changes and open a Pull Request.
2. After merge, confirm in Jenkins:

<Frame>
  ![The image shows a Jenkins pipeline interface for a project named "solar-system" under "Gitea-Organization," displaying various stages of a CI/CD process, including unit testing, code coverage, and deployment steps. It also includes a prompt asking if the pull request is merged and ArgoCD is synced, with options to confirm or abort.](https://kodekloud.com/kk-media/image/upload/v1752870882/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-Ignore-Rules/jenkins-pipeline-solar-system-cicd.jpg)
</Frame>

3. In Argo CD, sync the `solar-system` application:

<Frame>
  ![The image shows the Argo CD dashboard displaying two applications: "bitnami-sealed-secrets" and "solar-system-argo-app," with their respective statuses and details. The interface includes options to sync, refresh, or delete the applications.](https://kodekloud.com/kk-media/image/upload/v1752870883/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-Ignore-Rules/argo-cd-dashboard-bitnami-solar-system.jpg)
</Frame>

4. Once synced, inspect the updated replica set and pods:

<Frame>
  ![The image shows an Argo CD application dashboard with a visual representation of a deployment pipeline, indicating the sync status and health of various components in a Kubernetes environment.](https://kodekloud.com/kk-media/image/upload/v1752870884/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-Ignore-Rules/argo-cd-deployment-pipeline-dashboard.jpg)
</Frame>

***

## 6. Troubleshoot Token-Parsing Errors

If you see:

```text theme={null}
Failed to load config file zap_ignore_rules: Unexpected number of tokens on line - there should be at least 3, tab separated: 100001 IGNORE
```

Then your `zap_ignore_rules` likely has spaces instead of tabs.

<Callout icon="triangle-alert">
  Open the file in an editor and ensure exactly one `<TAB>` between each field:

  ```bash theme={null}
  vi zap_ignore_rules
  # Should read:
  100001<TAB>IGNORE<TAB>http://134.209.155.222:30000/api-docs/
  ```
</Callout>

Recommit and rerun the pipeline.

***

## 7. Verify Final DAST Results

A successful DAST stage shows:

```text theme={null}
PASS: ...
IGNORE-NEW: Unexpected Content-Type was returned [100001] x 83
FAIL-NEW: 0 WARN: 0 INFO: 0 IGNORE: 1 PASS: 112
```

Open the HTML report to confirm the ignored rule no longer blocks your build:

<Frame>
  ![The image shows a ZAP Scanning Report detailing security alerts for various websites, with a summary indicating low and informational risk levels.](https://kodekloud.com/kk-media/image/upload/v1752870885/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-Ignore-Rules/zap-scanning-report-security-alerts.jpg)
</Frame>

***

## Summary & Next Steps

In this lesson, we:

* Ran OWASP ZAP DAST against our API
* Generated and customized an ignore-rules file
* Updated our Jenkins pipeline to use `-c zap_ignore_rules`
* Published the HTML report in Jenkins
* Synced changes via Argo CD
* Troubleshot tab-delimited config errors

Next, we’ll explore integrating serverless deployments with AWS Lambda.

***

## Links and References

* [OWASP ZAP Documentation](https://www.zaproxy.org/docs/desktop/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Argo CD User Guide](https://argo-cd.readthedocs.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/d5f53677-f40c-4fbe-b983-289f3baf2c61" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/ef298b92-e6d9-4b41-810b-d4c67b0c1023" />
</CardGroup>
