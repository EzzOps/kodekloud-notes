# Demo DAST and Manual Input

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Demo-DAST-and-Manual-Input/page

This guide extends a Jenkins pipeline with manual approval and Dynamic Application Security Testing using OWASP ZAP.

In this guide, we’ll extend our Jenkins pipeline with two new stages:

1. A **manual approval** checkpoint after deploying the app via GitOps (Argo CD sync).
2. A **Dynamic Application Security Testing (DAST)** step using OWASP ZAP.

## What Is DAST?

Dynamic Application Security Testing (DAST) probes a live application for vulnerabilities like SQL injection and XSS. Instead of scanning source code (SAST), DAST injects malicious payloads at runtime to uncover weaknesses in a running service.

![The image shows a webpage from OWASP discussing dynamic application security testing tools, listing both open-source and commercial options, along with upcoming OWASP global events.](https://kodekloud.com/kk-media/image/upload/v1752870887/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/owasp-dynamic-application-security-testing-tools.jpg)

## OWASP Zed Attack Proxy (ZAP)

OWASP ZAP is an open-source, community-driven web application scanner. It supports passive, active, and API scans.

![The image is a webpage for Zed Attack Proxy (ZAP) by Checkmarx, describing it as a widely used, free, and open-source web app scanner. It includes options to download the software and links to guides and documentation.](https://kodekloud.com/kk-media/image/upload/v1752870889/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/zed-attack-proxy-webpage-scan.jpg)

### ZAP Scan Modes

| Mode     | Description                                       |
| -------- | ------------------------------------------------- |
| Baseline | Time-boxed passive scan                           |
| Full     | AJAX Spider + active + passive scans              |
| API      | Scans OpenAPI/GraphQL/SOAP endpoints (our choice) |

![The image shows a webpage titled "ZAP Docker Documentation" with links to various guides and scans related to automating ZAP in a CI/CD environment. It includes sections like "Baseline Scan," "Full Scan," and "API Scan."](https://kodekloud.com/kk-media/image/upload/v1752870890/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/zap-docker-documentation-guides.jpg)

We’ll run the **API scan** against our service’s OpenAPI definition.

## zap-api-scan.py Usage

Install or use the Docker image `ghcr.io/zaproxy/zaproxy` to invoke `zap-api-scan.py`:

```bash theme={null}
zap-api-scan.py -t <target> -f <format> [options]
```

Key options:

```text theme={null}
-t <target>       API spec URL/file (OpenAPI, SOAP) or GraphQL endpoint
-f <format>       openapi | soap | graphql
-r <report_html>  Full HTML report
-w <report_md>    Markdown report
-J <report_json>  JSON report
-x <report_xml>   XML report
-c <config_file>  Custom INFO/IGNORE/FAIL rules
-g <gen_file>     Generate default config (WARN by default)
-a                Include alpha passive scan rules
-d                Debug output
-P <port>         Proxy listen port
-D <delay>        Delay (s) before passive scan
-I                Treat default rules as INFO
-l                Ignore warnings (post 2.9.0)
```

For full details, see the [OWASP ZAP documentation](https://www.zaproxy.org/docs/).

## Integrating with Jenkins

Add the following stages to your `Jenkinsfile`:

| Stage            | Purpose                              | Trigger        |
| ---------------- | ------------------------------------ | -------------- |
| App Deployed?    | Manual approval after Argo CD sync   | PR branch      |
| DAST – OWASP ZAP | Run ZAP API scan on deployed service | After approval |

### 1. App Deployed? (Manual Approval)

This stage pauses the pipeline until an operator merges your PR and syncs Argo CD.

```groovy theme={null}
stage('App Deployed?') {
  when {
    branch 'PR*'
  }
  steps {
    timeout(time: 1, unit: 'DAYS') {
      input message: 'Has the PR been merged and Argo CD synced?',
            ok: 'Yes, proceed with DAST'
    }
  }
}
```

![The image shows a webpage from the Jenkins documentation, specifically detailing the "input" directive in pipeline syntax. It includes configuration options and descriptions for using the input step in Jenkins pipelines.](https://kodekloud.com/kk-media/image/upload/v1752870891/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/jenkins-input-directive-pipeline.jpg)

> **lightbulb** The `input` step blocks the pipeline until a user clicks **Proceed** or the timeout expires.

### 2. DAST – OWASP ZAP

Once approved, execute ZAP against your live API:

```groovy theme={null}
stage('DAST - OWASP ZAP') {
  when {
    branch 'PR*'
  }
  steps {
    sh '''
      chmod 777 $(pwd)
      docker run -v $(pwd):/zap/wrk/:rw \
        ghcr.io/zaproxy/zaproxy zap-api-scan.py \
        -t http://<K8S_IP>:30000/api/docs/ \
        -f openapi \
        -r zap_report.html \
        -w zap_report.md \
        -J zap_report.json \
        -x zap_report.xml
    '''
  }
}
```

#### Sample OpenAPI Definition

Our service exposes `/api/docs/` with this minimal spec:

```json theme={null}
{
  "openapi": "3.0.0",
  "info": { "title": "Solar System API", "version": "1.0" },
  "paths": {
    "/": {
      "get": {
        "responses": { "200": { "description": "", "content": { "text/plain": { "schema": { "type": "string", "example": "Example" } } } } }
      }
    },
    "/live": {
      "get": {
        "responses": { "200": { "description": "", "content": { "text/plain": { "schema": { "type": "string", "example": "Example" } } } } }
      }
    }
  }
}
```

![The image shows a pull request on a code repository platform, where a user is attempting to merge changes related to a Jenkins pipeline. It includes details about commits, files changed, and review status.](https://kodekloud.com/kk-media/image/upload/v1752870892/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/pull-request-jenkins-pipeline.jpg)

## Running the Pipeline

1. Commit your `Jenkinsfile` changes and open a PR.
2. Jenkins triggers a new build:

![The image shows a Jenkins pipeline interface with various stages of a build process, including installing dependencies, unit testing, and deploying, with some stages marked as completed.](https://kodekloud.com/kk-media/image/upload/v1752870894/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/jenkins-pipeline-build-process-diagram.jpg)

3. **App Deployed?** waits for merge and Argo CD sync.
4. Merge the PR:

![The image shows a GitHub pull request page where a Docker image update has been merged into the main branch. The pull request is titled "Updated Docker Image #2" and has been successfully merged and closed.](https://kodekloud.com/kk-media/image/upload/v1752870895/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/github-pull-request-docker-update.jpg)

5. Sync your app in Argo CD:

![The image shows a dashboard from Argo CD, displaying the status and details of an application deployment named "solar-system-argo-app," with a visual representation of its components and their sync status.](https://kodekloud.com/kk-media/image/upload/v1752870896/notes-assets/images/Certified-Jenkins-Engineer-Demo-DAST-and-Manual-Input/argo-cd-solar-system-deployment.jpg)

```bash theme={null}
kubectl -n solar-system get pods
