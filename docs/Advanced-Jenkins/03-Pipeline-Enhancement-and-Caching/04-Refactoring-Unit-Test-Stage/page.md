# Refactoring Unit Test Stage

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Pipeline-Enhancement-and-Caching/Refactoring-Unit-Test-Stage/page

Explains running parallel Node.js version unit tests in Jenkins, diagnosing missing dependencies across different agents and fixing by installing per stage or using stash/unstash.

In this lesson we update a Jenkins pipeline to run unit tests across multiple Node.js versions using parallel stages. You’ll learn why a parallel stage may fail with "mocha: not found" and how to fix it by ensuring dependencies are available to each runtime.

## Pipeline context

The pipeline runs on a Kubernetes pod whose default container is `node-18`. The `tools` stanza references a named NodeJS tool configured in Jenkins global tools.

```groovy theme={null}
@Library('dasher-trusted-shared-library@featureTrivyScan') _
pipeline {
    agent {
        kubernetes {
            cloud 'dasher-prod-k8s-us-east'
            yamlFile 'k8s-agent.yaml'
            defaultContainer 'node-18'
        }
    }
    tools {
        nodejs 'nodejs-22-6-0'
    }
    environment {
        MONGO_URI = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"
        MONGO_DB_CREDS = credentials('mongo-db-credentials')
        MONGO_USERNAME = credentials('mongo-db-username')
        MONGO_PASSWORD = credentials('mongo-db-password')
    }
    // ...
}
```

## Where dependencies are installed

Below is a fuller pipeline excerpt showing an `Installing Dependencies` stage and a placeholder for dependency scanning. This illustrates the typical place to run `npm install` before tests.

```groovy theme={null}
pipeline {
    agent {
        kubernetes {
            cloud 'dasher-prod-k8s-us-east'
            yamlFile 'k8s-agent.yaml'
            defaultContainer 'node-18'
        }
    }

    tools {
        nodejs 'nodejs-22-6-0'
    }

    environment {
        MONGO_URI = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"
        MONGO_DB_CREDS = credentials('mongo-db-credentials')
        MONGO_USERNAME = credentials('mongo-db-username')
        MONGO_PASSWORD = credentials('mongo-db-password')
        SONAR_SCANNER_HOME = tool 'sonarqube-scanner-610'
        GITEA_TOKEN = credentials('gitea-api-token')
    }

    options {
        disableResume()
        disableConcurrentBuilds abortPrevious: true
    }

    stages {
        stage('Installing Dependencies') {
            options { timestamps() }
            steps {
                sh 'node -v'
                sh 'npm install --no-audit'
            }
        }

        stage('Dependency Scanning') {
            parallel {
                // dependency scanning stages...
            }
        }

        // Unit testing stages follow...
    }
}
```

## Parallelizing unit tests across Node.js versions

You can run tests in parallel for multiple Node.js versions. The example below runs Node.js 18 and 19 as containers inside the same Kubernetes pod, and Node.js 20 using a Docker agent on the Jenkins agent host.

```groovy theme={null}
stage('Unit Testing') {
    parallel {
        stage('NodeJS 18') {
            options { retry(2) }
            steps {
                sh 'node -v'
                sh 'npm test'
            }
        }

        stage('NodeJS 19') {
            options { retry(2) }
            steps {
                container('node-19') {
                    // small delay to reduce transient port/contention issues when multiple containers start at once
                    sh 'sleep 10s'
                    sh 'node -v'
                    sh 'npm test'
                }
            }
        }

        stage('NodeJS 20') {
            agent {
                docker {
                    image 'node:20-alpine'
                }
            }
            options { retry(2) }
            steps {
                sh 'node -v'
                sh 'npm test'
            }
        }
    }
}
```

Important distinctions:

* `NodeJS 18` and `NodeJS 19` run in containers that are part of the same Kubernetes pod. They may share the same underlying workspace depending on how the pod/agent is configured.
* `NodeJS 20` runs in a separate Docker agent. It typically does not share the same workspace or filesystem with the Kubernetes pod containers.

<Callout icon="lightbulb">
  When parallel stages use different agent types (Kubernetes containers vs Docker agent), they generally do not share the same filesystem or installed dependencies. Ensure each runtime has access to dependencies by running `npm install` inside that stage, or by using `stash`/`unstash` when the agent/workspace mechanisms permit it.
</Callout>

## Example failure: "mocha: not found"

When Node 20 runs in its Docker agent, you might see this console output:

```text theme={null}
+ node -v
v20.18.0

+ npm test

> Solar System@6.7.6 test
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit

sh: mocha: not found
script returned exit code 127
```

Why this happens:

* `npm install` was executed inside the Kubernetes pod during `Installing Dependencies`, so `node_modules` were installed in that pod’s workspace.
* The `NodeJS 20` stage runs in a separate Docker agent (`node:20-alpine`) which does not have access to the same `node_modules` and therefore cannot find `mocha`.

## Solutions

You have two common, reliable options:

1. Install dependencies inside each parallel stage that needs them (recommended for portability).
2. Use `stash`/`unstash` to transfer a prepared `node_modules` or workspace between stages — only works when the Jenkins stash/un-stash mechanism and agent types allow it.

Below are code examples for both approaches.

### A — Install dependencies inside the NodeJS 20 stage

Add `npm install` to the stage running under the Docker agent:

```groovy theme={null}
stage('NodeJS 20') {
    agent {
        docker {
            image 'node:20-alpine'
        }
    }
    options { retry(2) }
    steps {
        // Ensure dependencies are available in this Docker agent
        sh 'npm install --no-audit'
        sh 'node -v'
        sh 'npm test'
    }
}
```

This is straightforward and avoids cross-platform binary issues.

### B — Stash/Unstash dependencies (when appropriate)

If both the producer and consumer stages can use Jenkins' stash/unstash workspace mechanism, you can prepare dependencies once and then unstash in the Docker agent:

```groovy theme={null}
stage('Install and Stash Dependencies') {
    steps {
        sh 'npm install --no-audit'
        stash includes: 'node_modules/**', name: 'node-modules'
    }
}

stage('NodeJS 20') {
    agent {
        docker {
            image 'node:20-alpine'
        }
    }
    steps {
        unstash 'node-modules'
        sh 'node -v'
        sh 'npm test'
    }
}
```

<Callout icon="warning">
  Stashing `node_modules` can transfer platform-specific binaries that may be incompatible with the target runtime (for example, Debian/glibc binaries vs Alpine/musl). If native addons or compiled binaries are present, prefer running `npm install` in the target runtime or building artifacts in a consistent environment.
</Callout>

## Comparison: approaches at a glance

| Approach                                    | Pros                                                       | Cons                                                              | When to use                                                                       |
| ------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Install inside each stage (`npm install`)   | Simple, reliable, ensures correct binaries for the runtime | Slower (repeats install per runtime)                              | When runtimes differ (e.g., Alpine vs Debian) or fast iteration isn't critical    |
| `stash` / `unstash` prepared `node_modules` | Avoids repeated installs, faster overall                   | May transfer incompatible native binaries; requires stash support | When agent runtimes are compatible and stash mechanism is supported               |
| Prebuilt Docker image with dependencies     | Fastest for tests, fully reproducible                      | Needs image build and registry updates                            | When you control the image build pipeline and maintain images per Node.js version |

## Summary

* Use parallel stages to test across multiple Node.js versions.
* Always be aware where `npm install` runs — different agents/containers do not necessarily share the same filesystem.
* To fix errors like `mocha: not found`, either install dependencies inside the failing stage or use stash/unstash when agent/workspace compatibility permits.
* Prefer installing in the target runtime when native modules or platform-specific binaries exist.

## Links and references

* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
* [Node.js Docker images](https://hub.docker.com/_/node)
* [Jenkins Stash/Unstash documentation (Pipeline)](https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/#stash-stash-files-for-later-use)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/5352396d-b54f-4910-a874-f2aa70e88823/lesson/bf5c477b-b0e2-4cd6-9380-afed8ed82060" />
</CardGroup>
