# Demo Scripted Pipeline Initialize

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Pipeline-Structure-and-Scripted-vs-Declarative/Demo-Scripted-Pipeline-Initialize/page

This guide explains converting a Declarative Pipeline to a Scripted Pipeline in Jenkins for the solar-system repository.

In this guide, you’ll learn how to convert a Declarative Pipeline into a fully Scripted Pipeline for the **solar-system** repository on the `features/advanced-demo` branch. We’ll cover tool setup, environment configuration, caching, timestamps, and concurrency control.

## 1. Review the Existing Declarative Pipeline

The current pipeline installs Node.js, sets environment variables, and caches npm dependencies:

```groovy theme={null}
pipeline {
    agent {
        tools {
            nodejs 'nodejs-22-6-0'
        }
    }
    environment {
        SONAR_SCANNER_HOME = tool 'sonarqube-scanner-610'
        GITEA_TOKEN        = credentials('gitea-api-token')
    }
    options {
        disableResume()
        disableConcurrentBuilds(abortPrevious: true)
    }
    stages {
        stage('Installing Dependencies') {
            agent any
            options { timestamps() }
            steps {
                cache(maxCacheSize: 550, caches: [
                    arbitraryFileCache(
                        cacheName: 'npm-dependency-cache',
                        cacheValidityDecidingFile: 'package-lock.json'
                    )
                ]) {
                    sh 'node -v'
                    sh 'npm install --no-audit'
                    stash(includes: 'node_modules')
                }
            }
        }
    }
}
```

## 2. Create and Push the Scripted Branch

```bash theme={null}
git checkout -b pipeline/scripted
git push -u origin pipeline/scripted
```

Pushing this branch triggers a new build in Jenkins.

<Frame>
  ![The image shows a Jenkins dashboard for a project named "solar-system," displaying the status of various branches with details on their last success, last failure, and duration.](https://kodekloud.com/kk-media/image/upload/v1752871000/notes-assets/images/Certified-Jenkins-Engineer-Demo-Scripted-Pipeline-Initialize/jenkins-dashboard-solar-system-status.jpg)
</Frame>

## 3. Define the Scripted Pipeline

Wrap all steps inside a `node` block and configure tools, environment, and build properties:

```groovy theme={null}
node {
    // 1. Tool setup: install Node.js and update PATH
    env.NODEJS_HOME = tool 'nodejs-22-6-0'
    env.PATH        = "${env.NODEJS_HOME}/bin:${env.PATH}"

    // 2. Prevent concurrent builds and resume
    properties([
        disableConcurrentBuilds(abortPrevious: true),
        disableResume()
    ])

    stage('Checkout') {
        checkout scm
    }

    // 3. Timestamp wrapper for better logs
    wrap([$class: 'TimestamperBuildWrapper']) {
        stage('Installing Dependencies') {
            // 4. Cache npm modules across builds
            cache(maxCacheSize: 550, caches: [
                arbitraryFileCache(
                    cacheName: 'npm-dependency-cache',
                    cacheValidityDecidingFile: 'package-lock.json'
                )
            ]) {
                sh 'node -v'
                sh 'npm install --no-audit'
                stash(includes: 'node_modules')
            }
        }
    }
}
```

<Callout icon="lightbulb">
  Caching `node_modules` speeds up CI by restoring dependencies from the cache on subsequent runs, reducing network overhead.
</Callout>

## 4. Check Pipeline Syntax Reference

If you need to explore other Scripted Pipeline constructs, consult the official syntax guide.

<Frame>
  ![The image shows a webpage from the Jenkins documentation, specifically detailing pipeline syntax options. It includes a sidebar with navigation links and a main section describing various options like disableConcurrentBuilds and disableResume.](https://kodekloud.com/kk-media/image/upload/v1752871001/notes-assets/images/Certified-Jenkins-Engineer-Demo-Scripted-Pipeline-Initialize/jenkins-pipeline-syntax-options.jpg)
</Frame>

```groovy theme={null}
// Example: wrap([$class: 'TimestamperBuildWrapper']) { ... }
// Visit: https://www.jenkins.io/doc/book/pipeline/syntax/
```

## 5. Validate First and Subsequent Runs

On the **first run**, the cache is empty:

```bash theme={null}
> node -v
v22.6.0
> npm install --no-audit
added 365 packages in 3s
```

On **subsequent runs**, the cache is restored for faster installs:

```bash theme={null}
[Cache ...] Restoring cache...
> node -v
v22.6.0
> npm install --no-audit
up to date in 1s
```

## 6. Ensure Concurrency Control

Start two builds in quick succession; the earlier build will be aborted to honor `abortPrevious: true`.

<Frame>
  ![The image shows a Jenkins pipeline interface with build history and stages for a project named "solar-system." It displays the status of three builds, including their start, checkout, and end stages.](https://kodekloud.com/kk-media/image/upload/v1752871003/notes-assets/images/Certified-Jenkins-Engineer-Demo-Scripted-Pipeline-Initialize/jenkins-pipeline-solar-system-builds.jpg)
</Frame>

<Callout icon="triangle-alert">
  Aborting previous builds can interrupt cleanup tasks. Ensure your pipeline handles partial states and rollbacks correctly.
</Callout>

## Table: Key Pipeline Options

| Option                                         | Purpose                                                              |
| ---------------------------------------------- | -------------------------------------------------------------------- |
| `disableConcurrentBuilds(abortPrevious: true)` | Prevents parallel runs by aborting earlier builds on the same branch |
| `disableResume()`                              | Disables resume from checkpoints to simplify workflow                |
| `wrap([$class: 'TimestamperBuildWrapper'])`    | Adds timestamps to console output                                    |
| `cache(...)`                                   | Reuses files between builds to speed up dependency installation      |

## Links and References

* [Jenkins Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [NodeJS Plugin for Jenkins](https://plugins.jenkins.io/nodejs/)
* [Jenkins Pipeline Caching](https://plugins.jenkins.io/pipeline-build-step/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/956fce34-baa6-4655-a3cf-7b12d2364544/lesson/ce1ca1ea-c63c-48d3-a664-9aeac360b80c" />
</CardGroup>
