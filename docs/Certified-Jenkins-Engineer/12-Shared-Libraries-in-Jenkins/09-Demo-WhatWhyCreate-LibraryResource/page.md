# Demo WhatWhyCreate LibraryResource

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Shared-Libraries-in-Jenkins/Demo-WhatWhyCreate-LibraryResource/page

This guide explains creating a library resource in Jenkins to enhance maintainability by decoupling script logic from Groovy.

Library Resources in a Jenkins [Shared Library](https://www.jenkins.io/doc/book/pipeline/shared-libraries/) let you bundle static assets—shell scripts, YAML, templates—under `resources/`. At runtime, your Pipeline can load and execute these files via `libraryResource`, decoupling script logic from Groovy and boosting maintainability.

In this guide, we’ll replace hardcoded Trivy commands with a parameterized shell script in `resources/scripts/`, a Groovy loader helper, and a high-level wrapper. You’ll learn how to:

* Store and version static assets in your shared library
* Dynamically load and execute scripts at Pipeline runtime
* Pass custom arguments from your `Jenkinsfile` without touching library code

***

## 1. The Problem: Hardcoded Commands

Our initial `vars/TrivyScan.groovy` contained two inline `sh` blocks with fixed severity levels and exit codes:

```groovy theme={null}
def vulnerability(String imageName) {
    sh '''
        echo image = ${imageName}
        trivy image ${imageName} \
            --severity LOW,MEDIUM,HIGH \
            --exit-code 0 \
            --quiet \
            --format json -o trivy-image-MEDIUM-results.json
        trivy image ${imageName} \
            --severity CRITICAL \
            --exit-code 1 \
            --quiet \
            --format json -o trivy-image-CRITICAL-results.json
    '''
}

def reportsConverter() {
    sh '''
        trivy convert \
            --format template --template "@/usr/local/share/trivy/templates/html.tpl"
    '''
}
```

<Callout icon="lightbulb">
  Hardcoding severity levels and exit codes makes updates error-prone and requires editing Groovy logic for every change.
</Callout>

***

## 2. Solution Overview

We’ll break this into four steps:

| Component            | Location                      | Purpose                                          |
| -------------------- | ----------------------------- | ------------------------------------------------ |
| Parameterized Script | `resources/scripts/trivy.sh`  | Run `trivy image` with custom args               |
| High-Level Wrapper   | `vars/TrivyScanScript.groovy` | Invoke the script from Groovy with a simple API  |
| Generic Loader       | `vars/loadScript.groovy`      | Fetch any `resources/scripts/*` asset at runtime |
| Pipeline Usage       | `Jenkinsfile`                 | Call `TrivyScanScript.vulnerability(...)`        |

1. Add a **shell script** under `resources/scripts/`.
2. Create a **Groovy wrapper** (`TrivyScanScript.groovy`) that calls the script with parameters.
3. Build a **generic loader** (`loadScript.groovy`) using `libraryResource`.
4. Invoke your new API from the `Jenkinsfile`.

***

## 3. Add the Shell Script Resource

File: `resources/scripts/trivy.sh`

```bash theme={null}
#!/bin/bash
set -euo pipefail

echo "imageName = $1"
echo "severity  = $2"
echo "exitCode  = $3"

trivy image "$1" \
  --severity "$2" \
  --exit-code "$3" \
  --format json \
  -o "trivy-image-$2-results.json"
```

This script accepts three arguments:

1. `$1` – Docker image (e.g., `my-app:latest`)
2. `$2` – Severity levels (e.g., `LOW,MEDIUM,HIGH`)
3. `$3` – Exit code on vulnerability detection

***

## 4. Define the TrivyScanScript Library

File: `vars/TrivyScanScript.groovy`

```groovy theme={null}
def vulnerability(Map config = [:]) {
    // Load the parameterized script into the workspace
    loadScript(name: 'trivy.sh')
    sh "./trivy.sh ${config.imageName} ${config.severity} ${config.exitCode}"
}

def reportsConverter() {
    sh 'trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl"'
}
```

Usage in `Jenkinsfile`:

```groovy theme={null}
@Library('your-shared-lib') _
pipeline {
  agent any
  stages {
    stage('Security Scan') {
      steps {
        TrivyScanScript.vulnerability(
          imageName: 'my-app:latest',
          severity: 'CRITICAL',
          exitCode: 1
        )
      }
    }
  }
}
```

***

## 5. Create a Generic Loader: `loadScript.groovy`

File: `vars/loadScript.groovy`

```groovy theme={null}
def call(Map config = [:]) {
    // Fetch any script from resources/scripts/
    def scriptData = libraryResource "scripts/${config.name}"
    writeFile file: config.name, text: scriptData
    sh "chmod +x ./${config.name}"
}
```

<Callout icon="lightbulb">
  This helper lets you load *any* file under `resources/scripts` by passing its filename as `config.name`.
</Callout>

***

## 6. How `libraryResource` Works

`libraryResource` reads a file from your shared library’s `resources` directory and returns its content:

```groovy theme={null}
// Example: Load a JSON template from resources/
def jsonData = libraryResource 'com/mycorp/pipeline/config/request.json'
writeFile file: 'request.json', text: jsonData
```

You can then:

* Pass it to an HTTP API
* Write it to disk for local execution

***

## 7. Recap

* **Static Script** (`trivy.sh`): Parameterized Trivy invocation
* **TrivyScanScript**: Groovy API that loads & executes the script
* **loadScript**: Generic loader using `libraryResource`

This pattern cleanly separates static assets from Groovy logic, making it easy to update scripts without changing code and enabling pipeline authors to provide custom configurations.

***

## Links and References

* Jenkins Shared Library: [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
* Trivy Documentation: [https://github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)
* `libraryResource` Step: [https://www.jenkins.io/doc/pipeline/steps/workflow-cps/#libraryresource-read-a-resource-from-a-shared-library](https://www.jenkins.io/doc/pipeline/steps/workflow-cps/#libraryresource-read-a-resource-from-a-shared-library)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/b0fefde6-7fea-44da-9509-27007d27869f/lesson/8e4df933-d626-43d2-bfe6-207bd985b88d" />
</CardGroup>
