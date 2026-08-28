# 1. Report LOW, MEDIUM, HIGH (non-blocking)
docker run --rm \
  -v "$WORKSPACE":/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --exit-code 0 \
  --severity LOW,MEDIUM,HIGH \
  --light "$imageName"

# 2. Fail on CRITICAL
docker run --rm \
  -v "$WORKSPACE":/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --exit-code 1 \
  --severity CRITICAL \
  --light "$imageName"

exit_code=$?
echo "🛑 Exit Code: $exit_code"

if [[ $exit_code -ne 0 ]]; then
  echo '❌ Image scanning failed: Critical vulnerabilities found'
  exit 1
else
  echo '✅ Image scanning passed: No critical issues'
fi
```

<Callout icon="lightbulb">
  * `--light` mode skips non-OS packages for faster scans.
  * Cache volume is mapped to reuse vulnerability data between runs.
</Callout>

***

## 3. Initial Trivy Scan Results

Running the scan for the first time may reveal CVEs in embedded libraries:

```bash theme={null}
bash trivy-k8s-scan.sh
siddharth67/numeric-app:a8830b58fa890c9dba275f843679598a3 (alpine 3.13.5)

Total: 5 (LOW: 0, MEDIUM: 2, HIGH: 3)

+-------------------------------------------+---------------+----------+-------------------+-------------------+
| LIBRARY                                   | VULNERABILITY | SEVERITY | INSTALLED VERSION | FIXED VERSION     |
+-------------------------------------------+---------------+----------+-------------------+-------------------+
| org.apache.tomcat.embed:tomcat-embed-core | CVE-2021-17527| HIGH     | 9.0.39            | 9.0.40            |
|                                           | CVE-2021-25122| HIGH     | 9.0.39            | 9.0.43            |
|                                           | CVE-2021-24112| MEDIUM   | 9.0.39            | 9.0.61            |
+-------------------------------------------+---------------+----------+-------------------+-------------------+

Exit Code: 0
Image scanning passed. No vulnerabilities found
```

<Frame>
  ![The image shows a Jenkins dashboard displaying dependency-check results, listing vulnerabilities in various files with their severity levels and associated weaknesses.](https://kodekloud.com/kk-media/image/upload/v1752873713/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Kubernetes/jenkins-dashboard-dependency-check-results.jpg)
</Frame>

Upon seeing these CVEs, we’ll upgrade Tomcat in our `pom.xml`.

***

## 4. Update Tomcat Version in `pom.xml`

Open your Maven POM in Spring Tool Suite and override the `tomcat.version` property:

<Frame>
  ![The image shows a software development environment with a code editor displaying a Maven POM file and a terminal window open below. The editor is part of the Spring Tool Suite, and the file lists various dependencies and versions.](https://kodekloud.com/kk-media/image/upload/v1752873714/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Kubernetes/spring-tool-suite-maven-pom-editor.jpg)
</Frame>

```xml theme={null}
<properties>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
  <java.version>1.8</java.version>
  <tomcat.version>9.0.43</tomcat.version>
</properties>
```

Commit and push your changes. Jenkins will automatically trigger a new pipeline run.

***

## 5. Post-Upgrade Scan

After the Tomcat upgrade, rerun Trivy to confirm no vulnerabilities remain:

```bash theme={null}
bash trivy-k8s-scan.sh
siddharth67/numeric-app:68e6b5f456a28d3615ea1406c1b959f36c334cf6 (alpine 3.13.5)

==========================================
Total: 0 (LOW: 0, MEDIUM: 0, HIGH: 0)

==========================================
Total: 0 (CRITICAL: 0)

Exit Code: 0
Image scanning passed. No vulnerabilities found
```

With the image verified as clean, it’s now safe to proceed to the **Kubernetes Deployment** stage.

***

That’s it for this lesson—your CI/CD pipeline now enforces both manifest and image security checks before deploying to production.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/c1a018b3-6698-4cd7-a759-35c6a6adb631" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/c95d1486-115f-4d66-aa02-fdbdb26b0578" />
</CardGroup>


# End of Section 3 and Promote to PROD namespace

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/End-of-Section-3-and-Promote-to-PROD-namespace/page

This article discusses the final steps in a DevSecOps pipeline, including security measures and a manual approval stage for production deployments.

Welcome to the wrap-up of our DevSecOps pipeline. We have:

* Secured the developer workstation with [Talisman Git Hooks][talisman]
* Run mutation tests, unit tests, and integration tests
* Performed static analysis (SAST) and dynamic analysis (DAST) using [OWASP ZAP][owasp-zap]
* Scanned dependencies with [Dependency Check][dependency-check] and [Trivy][trivy]
* Validated manifests via [OPA Conftest][opa] and [Kubesec][kubesec]
* Configured automatic rollbacks in Kubernetes deployments
* Sent build notifications to Slack for real-time visibility

<Callout icon="lightbulb">
  Below is a quick overview of the tools and their purposes:
</Callout>

| Security Measure             | Tool                    | Purpose                                        |
| ---------------------------- | ----------------------- | ---------------------------------------------- |
| Git pre-commit Hook          | Talisman                | Prevents accidental secrets or high-risk files |
| Static Application Security  | SAST                    | Detects code vulnerabilities early             |
| Dynamic Application Security | DAST (OWASP ZAP)        | Scans running applications for flaws           |
| Dependency Scanning          | Dependency Check, Trivy | Identifies vulnerable or outdated libraries    |
| Policy as Code               | OPA Conftest            | Ensures infrastructure policies compliance     |
| Manifest Linting             | Kubesec                 | Validates Kubernetes manifest best practices   |

## Adding a Manual Approval Stage

To ensure an architect or manager authorizes production deployments, we introduce a **Promote to PROD** stage with a two-day timeout. The snippet below shows how to integrate this into your `Jenkinsfile`:

```groovy theme={null}
stage('OWASP ZAP - DAST') {
    steps {
        withKubeConfig([credentialsId: 'kubeconfig']) {
            sh 'bash zap.sh'
        }
    }
}

stage('Promote to PROD') {
    steps {
        timeout(time: 2, unit: 'DAYS') {
            input message: 'Approve deployment to Production Environment/Namespace?'
        }
    }
}

stage('Testing Slack') {
    steps {
        // This intentional failure triggers our Slack notification
        sh 'exit 1'
    }
}

post {
    always {
        junit 'target/surefire-reports/*.xml'
        jacoco execPattern: 'target/jacoco.exec'
        mutation mutationStatsFile: '**/target/pit-reports/**/mutations.xml'
        dependencyCheckPublisher pattern: 'target/dependency-check-report.xml'
        publishHTML allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true,
                    reportDir: 'owasp-zap-report', reportFiles: 'zap_report'
        // Send a Slack notification with the current build result
        sendNotification currentBuild.result
    }
}
```

<Callout icon="triangle-alert">
  The pipeline will pause at the **Promote to PROD** stage until an approver selects **Proceed** or **Abort**. Aborting will stop the pipeline and notify the team via Slack.
</Callout>

Once committed and pushed, the pipeline executes all stages and halts at our manual approval gate:

<Frame>
  ![The image shows a Jenkins pipeline for a "devsecops-numeric-application" with various stages like build, tests, scans, and deployment. It includes a prompt asking for approval to deploy to the production environment.](https://kodekloud.com/kk-media/image/upload/v1752873717/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-End-of-Section-3-and-Promote-to-PROD-namespace/jenkins-pipeline-devsecops-application.jpg)
</Frame>

At this point, the designated approver clicks **Proceed** to deploy or **Abort** to cancel. If aborted, the stage turns gray, the pipeline stops, and a Slack alert is sent.

The screenshot below shows the completed pipeline with all checks passing and the approval prompt still active:

<Frame>
  ![The image shows a Jenkins pipeline for a "devsecops-numeric-application," detailing various stages such as build, testing, scanning, deployment, and integration. Each stage is marked with a green check, indicating successful completion, and there's a prompt for production deployment.](https://kodekloud.com/kk-media/image/upload/v1752873719/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-End-of-Section-3-and-Promote-to-PROD-namespace/jenkins-pipeline-devsecops-application-2.jpg)
</Frame>

In the next section, we'll add cluster benchmarking with Kubebench, enforce pod-to-pod security using KubeScan, perform a Kubernetes cluster vulnerability audit, and then finalize the production rollout.

## Links and References

* [Talisman Git Hooks][talisman]
* [OWASP ZAP][owasp-zap]
* [Dependency Check][dependency-check]
* [Trivy][trivy]
* [OPA Conftest][opa]
* [Kubesec][kubesec]
* [Jenkins Pipeline Syntax][jenkins-pipeline]

[talisman]: https://github.com/thoughtworks/talisman

[owasp-zap]: https://www.zaproxy.org/

[dependency-check]: https://owasp.org/www-project-dependency-check/

[trivy]: https://github.com/aquasecurity/trivy

[opa]: https://www.conftest.dev/

[kubesec]: https://kubesec.io/

[jenkins-pipeline]: https://www.jenkins.io/doc/book/pipeline/syntax/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/c8977415-ebda-44d4-bd79-2959fc8bb3e7" />
</CardGroup>
