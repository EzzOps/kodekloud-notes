# zap-api-scan rule configuration file
# Change WARN to IGNORE to ignore a rule or FAIL to fail if the rule matches.
# Active scan rules set to IGNORE will not run, which speeds up the scan.
# Only the rule identifiers are used—the names are provided for informational purposes.
# You can append your custom messages after a tab on each line.
0       WARN (Directory Browsing - Active/release)
10010   WARN (Cookie No HttpOnly Flag - Passive/release)
10011   WARN (Cookie Without Secure Flag - Passive/release)
10012   WARN (Password Autocomplete in Browser - Passive/release)
10015   WARN (Incomplete or No Cache-control and Pragma HTTP Header Set - Passive/release)
10016   WARN (Web Browser XSS Protection Not Enabled - Passive/release)
10017   WARN (Cross-Domain JavaScript Source File Inclusion - Passive/release)
10020   WARN (Content-Type Header Missing - Passive/release)
10030   WARN (X-Frame-Options Header Scanner - Passive/release)
10031   WARN (X-Content-Type-Options Header Missing - Passive/release)
10032   WARN (Information Disclosure - Debug Error Messages - Passive/beta)
10033   WARN (Information Disclosure - Sensitive Informations in URL - Passive/beta)
10034   WARN (Information Disclosure - Sensitive Information in HTTP Referrer Header - Passive/beta)
10035   WARN (HTTP Parameter Override - Suspicious Comments - Passive/beta)
10036   WARN (Information Disclosure - Passive/beta)
10037   WARN (Viewstate Scanner - Passive/beta)
10038   WARN (Secure Pages Include Mixed Content - Passive/release)
10040   WARN (Source Code Disclosure - /WEB-INF folder - Active/beta)
10041   WARN (Remote Code Execution - Shell Shock - Active/beta)
10042   WARN (Backup File Disclosure - Passive/beta)
10043   WARN (Weak Authentication Method - Passive/beta)
10044   WARN (Presence of Anti-CSRF Tokens - Passive/beta)
```

Each line in the file consists of:

* Rule ID
* Action (`IGNORE`, `WARN`, or `FAIL`)
* Additional informational text (optional)

Save this file (e.g., as `zap_ignore_rules`) and reference it in your Jenkins pipeline.

## Integrating with Jenkins Pipeline

Below is an example snippet from a Jenkinsfile which shows different pipeline stages. Notice the use of the configuration file in the "DAST - OWASP ZAP" stage:

```groovy theme={null}
stage('Integration Testing - [AWS EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)') {
    // Integration testing steps...
}

stage('K8S - Update Image Tag') {
    // Kubernetes image update steps...
}

stage('K8S - Raise PR') {
    // Steps to raise a pull request...
}

stage('App Deployed?') {
    when {
        branch 'PR*'
    }
    steps {
        timeout(time: 1, unit: 'DAYS') {
            input message: 'Is the PR merged and ArgoCD Synced?', ok: 'YES! PR is Merged and ArgoCD Applied'
        }
    }
}

stage('DAST - OWASP ZAP') {
    // DAST steps using ZAP
}

post {
    always {
        // Cleanup actions...
    }
}
```

After creating the configuration file, update the Docker command in your pipeline as shown below:

```bash theme={null}
chmod 777 $(pwd)
docker run -v $(pwd):/zap/wrk/:rw ghcr.io/zaproxy/zaproxy zap-api-scan.py \
-t http://134.209.155.222:30000/api-docs/ \
-f openapi \
-r zap_report.html \
-w zap_report.md \
-J zap_json_report.json \
-x zap_xml_report.xml \
-c zap_ignore_rules
```

This command executes the ZAP scan and generates several reports (HTML, Markdown, JSON, and XML). The HTML report is eventually published in the pipeline, as illustrated below:

```groovy theme={null}
post {
    always {
        script {
            if (fileExists('solar-system-gitops-argocd')) {
                sh 'rm -rf solar-system-gitops-argocd'
            }
        }
    }
    junit allowEmptyResults: true, stdioRetention: '', testResults: 'test-results.xml'
    junit allowEmptyResults: true, stdioRetention: '', testResults: 'dependency-check-junit.xml'
    junit allowEmptyResults: true, stdioRetention: '', testResults: 'trivy-image-CRITICAL-results.xml'
    junit allowEmptyResults: true, stdioRetention: '', testResults: 'trivy-image-MEDIUM-results.xml'
    publishHTML([allowMissing: true,
                 alwaysLinkToLastBuild: true,
                 keepAll: true,
                 reportDir: './',
                 reportFiles: 'zap_report.html',
                 reportName: 'DAST - OWASP ZAP Report',
                 reportTitles: '',
                 useWrapperFileDirectly: true])
    publishHTML([allowMissing: true,
                 alwaysLinkToLastBuild: true,
                 keepAll: true,
                 reportDir: './',
                 reportFiles: 'trivy-image-CRITICAL-results.html',
                 reportName: 'Trivy Image Critical Vul Report',
                 reportTitles: '',
                 useWrapperFileDirectly: true])
    publishHTML([allowMissing: true,
                 alwaysLinkToLastBuild: true,
                 keepAll: true,
                 reportDir: './',
                 reportFiles: 'trivy-image-MEDIUM-results.html',
                 reportName: 'Trivy Image Medium Vul Report',
                 reportTitles: '',
                 useWrapperFileDirectly: true])
}
```

## Front-End Visual Elements

In your front-end application, you can add visual cues to indicate status updates. For instance, the index page includes a button with rocket icons representing the application's status:

```html theme={null}
<body>
  <div>
    <div>
      <a href="index.html">
        <button style="font-size: 40px; background: rgb(50,43,167); background: linear-gradient(90deg, rgba(50,43,167,1) 0%, rgba(82,41,124,1) 0%, rgba(137,37,142,1) 0%); color: white; font-family: 'Orbitron', sans-serif; border-radius: 25px; border: 2px solid rgb(35,34,36); width: 600px; height: 70px; text-align: center; line-height: initial; border-width: 1px 1px 3px;">
          <i class="fa fa-rocket"></i> $OLAR <i class="fa fa-rocket"></i> SY:
        </button>
      </a>
    </div>
    <br>
    <input type="submit" id="submit" value="Search the Planet" style="float: right; background-color: rgb(187,75,243); color: white; font-family: 'Ubuntu';">
  </div>
</body>
```

This design feature visually distinguishes important sections of the solar system application.

## Pipeline Execution and Final Verification

Once the pipeline is triggered, it pauses at the "App Deployed?" stage for manual confirmation. After merging the pull request and synchronizing ArgoCD, the pipeline resumes and deploys the updated application. You should see console messages similar to the following:

```bash theme={null}
chmod 777 $(pwd)
docker run -v $(pwd):/zap/wrk/:rw ghcr.io/zaproxy/zap-api-scan.py -t http://134.209.155.222:30000/api-docs/ -f openapi -r zap_report.html -w zap_report.md -J zap_json_report.json -x zap_xml_report.xml -c zap_ignore_rules
```

If executed correctly, the output confirms that 112 tests passed while ignoring the designated warning. For example:

```bash theme={null}
PASS: Cross Site Scripting (Persistent) [40016]
PASS: SQL Injection [40018]
...
IGNORE-NEW: Unexpected Content-Type was returned [100001] x 83
HTTP/134.209.155.82:8080 (200 OK)
...
FAIL-NEW: @ INFO: 0 | WARN-INPROG: @ INFO: 0 | IGNORE: 1 | PASS: 112
```

<Callout icon="triangle-alert">
  If you encounter an error like:

  Failed to load config file /zap/wrk/zap\_ignore\_rules Unexpected number of tokens on line - there should be at least 3, tab separated: 100001 IGNORE

  it indicates that your ignore file does not follow the proper format. Edit the file with a reliable text editor (e.g., vi) to ensure each line has at least three tab-separated tokens.
</Callout>

For example, use the following commands in your terminal:

```bash theme={null}
cd solar-system/
vi zap_ignore_rules
```

After updating and committing the corrected file, re-run the pipeline build. When successful, the DAST stage generates the expected reports, and the OWASP ZAP scan completes without errors.

## Final Docker Command (Demo)

Below is a reminder of the Docker command used for the demo:

```bash theme={null}
chmod 777 $(pwd) && docker run -v $(pwd):/zap/wrk/:rw ghcr.io/zaproxy/zap-api-scan.py -t http://134.209.155.222:30000/api-docs/ -f openapi -r zap_report.html -w zap_report.json -x zap_xml_report.xml -c zap_ignore_rules
```

By following this configuration, you can integrate OWASP ZAP into your CI/CD pipeline, effectively ignore specific warnings during DAST, and generate comprehensive security scanning reports.

***

<Frame>
  ![The image shows an Argo CD dashboard with two applications listed: "bitnami-sealed-secrets" and "solar-system-argo-app," displaying their status, repository information, and sync details.](https://kodekloud.com/kk-media/image/upload/v1752879706/notes-assets/images/Jenkins-Pipelines-DAST-Ignore-Rules/argo-cd-dashboard-bitnami-solar-system.jpg)
</Frame>

After synchronizing Argo CD, you should see a new replica set and multiple pods being created as the application is updated. The deployment dashboard may resemble the following:

<Frame>
  ![The image shows an Argo CD application dashboard displaying the status and details of a Kubernetes deployment, including health and sync status, with a visual representation of the application's components and their relationships.](https://kodekloud.com/kk-media/image/upload/v1752879708/notes-assets/images/Jenkins-Pipelines-DAST-Ignore-Rules/argo-cd-kubernetes-deployment-dashboard.jpg)
</Frame>

Finally, the Jenkins pipeline interface presents various build stages and includes a prompt to confirm that the pull request has been merged and ArgoCD is synchronized:

<Frame>
  ![The image shows a Jenkins pipeline interface for a project named "solar-system" with various stages like dependency scanning, unit testing, and deployment. It includes a prompt asking if the pull request is merged and ArgoCD is synced, with an option to confirm.](https://kodekloud.com/kk-media/image/upload/v1752879708/notes-assets/images/Jenkins-Pipelines-DAST-Ignore-Rules/jenkins-pipeline-solar-system-stages.jpg)
</Frame>

Upon successful pipeline completion, you can review the OWASP ZAP security scanning report:

<Frame>
  ![The image shows a ZAP Scanning Report detailing security alerts for various websites, with a summary of risk levels and specific alert details.](https://kodekloud.com/kk-media/image/upload/v1752879709/notes-assets/images/Jenkins-Pipelines-DAST-Ignore-Rules/zap-scanning-report-security-alerts.jpg)
</Frame>

This concludes the demonstration on how to configure OWASP ZAP to ignore specific warnings and integrate it into a CI/CD pipeline for Kubernetes deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-pipelines/module/fb6b2c83-178c-4962-b4e6-ca5528721170/lesson/2c26bfe9-bdc1-4932-8c6b-605489ccc3d4" />
</CardGroup>


# DAST and Manual Input

Source: https://notes.kodekloud.com/docs/Jenkins-Pipelines/Kubernetes-and-GitOps/DAST-and-Manual-Input/page

This guide demonstrates configuring CI/CD pipeline stages for manual input and Dynamic Application Security Testing using OWASP ZAP.

In this guide, we will demonstrate how to configure multiple stages in your CI/CD pipeline that accept manual user input and perform Dynamic Application Security Testing (DAST).

## Overview of DAST

Dynamic Application Security Testing (DAST) is an essential method for identifying vulnerabilities before an application goes live. DAST tools automatically scan web interfaces and APIs for common security issues such as SQL injection, cross-site scripting, and more. Unlike static analysis, which reviews source code without execution, DAST requires the application to be running so that it can inject malicious payloads and reveal potential exploits.

There are various tools available for DAST, ranging from open-source solutions to commercial products. In our example, we are utilizing the open-source tool [OWASP ZAP (Zed Attack Proxy)](https://owasp.org/www-project-zap/), one of the most popular options. Commercial alternatives include Netsparker and Burp Suite.

## Using ZAP with Docker

ZAP can be easily integrated into a CI/CD environment using Docker images. Different Docker images are provided for various scanning needs:

1. **Baseline Scan:** A time-limited, passive scan that reports issues.
2. **Full Scan:** Combines both active and passive scanning, using tools like Ajax spider, SpyDdos, and ActiveScan.
3. **API Scan:** Performs a comprehensive scan of an API based on its specification (OpenAPI, GraphQL, or SOAP).

For this demo, we will perform an API scan. The API scan script accepts a target API definition (via a URL or local file) along with a format specification (e.g., openapi) and generates reports in HTML, Markdown, JSON, and XML formats.

<Frame>
  ![The image shows a webpage titled "ZAP Docker Documentation" by Checkmarx, listing various guides and tools related to ZAP's Docker images for automation in CI/CD environments.](https://kodekloud.com/kk-media/image/upload/v1752879710/notes-assets/images/Jenkins-Pipelines-DAST-and-Manual-Input/zap-docker-documentation-guides.jpg)
</Frame>

The usage of the scan script is described below:

```bash theme={null}
Usage: zap-api-scan.py -t <target> -f <format> [options]
  -t target          Target API definition (OpenAPI/Soap) as a local file or URL, e.g., https://www.example.com/openapi.json,
                     or target endpoint URL for GraphQL, e.g., https://www.example.com/graphql.
  -f format          OpenAPI, soap, or graphql
  -h                 Print this help message
  -c config_file     Config file to use to INFO, IGNORE or FAIL warnings
  --config_url       URL of config file to use to INFO, IGNORE or FAIL warnings
  -g gen_file        Generate default config file (all rules set to WARN)
  -r report_html     File to write the full ZAP HTML report
  -r report_md       File to write the full ZAP Markdown report
  -r report_xml      File to write the full ZAP XML report
  -r report_json     File to write the full ZAP JSON report
  -d                 Show debug messages
  -p port            Specify listen port
  -D                 Delay in seconds to wait for passive scanning
  -P                 Do not fail on warning (post 2.9.0)
```

<Callout icon="lightbulb">
  If URLs return unexpected content types, the script raises corresponding alerts. For more information on available options, please refer to the usage message above.
</Callout>

## Configuring DAST in the Jenkins Pipeline

The following snippet from a Jenkinsfile illustrates how to configure the DAST stage using ZAP running in Docker. In this stage, a Docker container is executed to run an API scan against your application's OpenAPI specification, typically served from the `/api-docs` endpoint.

### Jenkinsfile Stage for DAST

```groovy theme={null}
stage('DAST - OWASP ZAP') {
    when {
        branch 'PR*'
    }
    steps {
        sh '''
        ##### REPLACE below with Kubernetes http://IP_Address:30000/api-docs/ #####
        chmod 777 $(pwd)
        docker run -v $(pwd):/zap/wrk/:rw ghcr.io/zaproxy/zap-api-scan.py \
        -t http://134.209.155.222:30000/api-docs/ \
        -f openapi \
        -r zap_report.html \
        -w zap_report.md \
        -J zap_json_report.json \
        -x zap_xml_report.xml
        '''
    }
}
```

<Callout icon="lightbulb">
  The command `chmod 777 $(pwd)` ensures that the generated reports have appropriate permissions, allowing them to be copied from the Docker container to the current working directory. Make sure to replace the target URL with your actual Kubernetes endpoint.
</Callout>

## API Documentation

Before starting the scan, verify that the `/api-docs` endpoint correctly returns your API's OpenAPI specification. Below is a sample JSON output:

```json theme={null}
{
  "openapi": "3.0.0",
  "info": {
    "title": "Solar System API",
    "version": "1.0"
  },
  "paths": {
    "/": {
      "get": {
        "responses": {
          "200": {
            "description": "",
            "content": {
              "text/plain": {
                "schema": {
                  "example": "Example",
                  "type": "string"
                }
              }
            }
          }
        }
      }
    },
    "/live": {
      "get": {
        "responses": {
          "200": {
            "description": "",
            "content": {
              "text/plain": {
                "schema": {
                  "example": "Example",
                  "type": "string"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

This JSON specification is also available in the repository as `OAS.json`.

## Integrating Manual Approval

To ensure that the DAST scan runs against the latest version of the application, we introduce a manual approval stage. This stage pauses the pipeline until a user verifies that the pull request has been merged and the application has been synchronized (typically via Argo CD).

### Jenkins Pipeline Stages Overview

```groovy theme={null}
stage('Integration Testing - [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)') {
    // Integration test steps
}

stage('K8S - Update Image Tag') {
    // Update Docker image tag in Kubernetes deployment
}

stage('K8S - Raise PR') {
    // Raise a pull request for the update
}

stage('App Deployed') {
    when {
        branch 'PR*'
    }
    steps {
        timeout(time: 1, unit: 'DAYS') {
            input message: 'Is the PR merged and is the Argo CD application synced?', ok: 'Yes, PR merged & Argo CD synced'
        }
    }
}

stage('DAST - OWASP ZAP') {
    // DAST stage executed after confirmation
}
```

The "App Deployed" stage employs a Jenkins input step with a timeout to ensure that the DAST scan is only executed after the application has been updated.

### Example of the Input Step in Jenkins

When the pipeline reaches the input step, a prompt is displayed asking for confirmation before proceeding. The screenshots below illustrate examples of the Jenkins interface for input configuration:

<Frame>
  ![The image shows a Jenkins interface with the "Snippet Generator" tool open, allowing users to configure and generate pipeline scripts. The interface includes options for selecting and configuring steps, such as archiving artifacts.](https://kodekloud.com/kk-media/image/upload/v1752879711/notes-assets/images/Jenkins-Pipelines-DAST-and-Manual-Input/jenkins-snippet-generator-interface.jpg)
</Frame>

If there's an error or a required input is missing, Jenkins will display an appropriate error message:

<Frame>
  ![The image shows a Jenkins interface with the "Declarative Directive Generator" open, where a user can generate pipeline code for a declarative pipeline directive. An error message indicates that an input message must be provided.](https://kodekloud.com/kk-media/image/upload/v1752879713/notes-assets/images/Jenkins-Pipelines-DAST-and-Manual-Input/jenkins-declarative-directive-generator-error.jpg)
</Frame>

For more details on configuring the input directive, refer to the [Jenkins documentation](https://www.jenkins.io/doc/).

<Frame>
  ![The image shows a webpage from the Jenkins documentation, specifically detailing the "input" directive in pipeline syntax, with configuration options and descriptions.](https://kodekloud.com/kk-media/image/upload/v1752879714/notes-assets/images/Jenkins-Pipelines-DAST-and-Manual-Input/jenkins-input-directive-pipeline.jpg)
</Frame>

## The Complete Flow

The complete CI/CD flow is as follows:

1. **Application Deployment:** The latest changes are deployed using a GitOps approach. A pull request (PR) is created, manually merged, and synchronized via Argo CD.
2. **Manual Approval:** The pipeline pauses at the "App Deployed" stage, awaiting confirmation that the PR is merged and the deployment is updated.
3. **DAST Execution:** After approval, the "DAST - OWASP ZAP" stage is executed. The Docker container scans the API (served at `/api-docs`) according to the OpenAPI specification.
4. **Results and Reporting:** The scan generates multiple reports (HTML, Markdown, JSON, XML). Note that while tests may pass, warnings such as unexpected content types can trigger a non-zero exit code, causing the stage to fail until resolved.

Here’s an example of the final Docker command that outputs the scan logs:

```bash theme={null}
chmod 777 $(pwd)
docker run -v $(pwd):/zap/wrk ghcr.io/zaproxy/zap-api-scan.py \
-t http://134.209.155.222:30000/api-docs/ \
-f openapi \
-r zap_report.html \
-w zap_report.md \
-J zap_json_report.json \
-x zap_xml_report.xml
```

<Callout icon="triangle-alert">
  If warnings are detected (e.g., unexpected content types), the scan might complete most tests successfully but still return a non-zero exit code. You can either address the warning or configure ZAP to ignore it in subsequent runs.
</Callout>

Thank you for following this guide to integrate DAST with manual approval into your CI/CD pipeline. This configuration not only improves security testing efficiency but also ensures that tests are run against the most recent application deployment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-pipelines/module/fb6b2c83-178c-4962-b4e6-ca5528721170/lesson/4e07c4dc-d403-4d21-8dfe-72f383b111a6" />
</CardGroup>
