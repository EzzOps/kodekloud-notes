# Demo Refactoring Unit Test Stage

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Pipeline-Enhancement-and-Caching/Demo-Refactoring-Unit-Test-Stage/page

This guide refactors a Jenkins pipeline to run unit tests concurrently on multiple Node.js versions for faster feedback and compatibility.

In this guide, we’ll refactor our Jenkins pipeline so that the **Unit Testing** stage runs concurrently on Node.js 18, 19, and 20. This approach speeds up feedback and ensures compatibility across multiple runtime versions.

## Table of Contents

* [Initial Pipeline Configuration](#initial-pipeline-configuration)
* [Adding Parallel Unit Tests](#adding-parallel-unit-tests)
* \[Understanding the Node 20 Failure]\(#understanding-the-node 20-failure)
* \[Fixing Dependencies for Node 20]\(#fixing-dependencies-for-node 20)
* [Complete Refactored Pipeline](#complete-refactored-pipeline)
* [Links and References](#links-and-references)

***

## Initial Pipeline Configuration

We start with a simple declarative pipeline using a Kubernetes agent that defaults to a Node 18 container. By default, all steps in the **Unit Testing** stage will run on Node 18.

```groovy theme={null}
@Library('dasher-trusted-shared-library@featureTrivyScan') _
pipeline {
  agent {
    kubernetes {
      cloud           'dasher-prod-k8s-us-east'
      yamlFile        'k8s-agent.yaml'
      defaultContainer 'node-18'
    }
  }

  tools {
    nodejs 'nodejs-22-6-0'
  }

  environment {
    MONGO_URI         = "mongodb+srv://supercluster.d8jjj.mongodb.net/superData"
    MONGO_DB_CREDS    = credentials('mongo-db-credentials')
    MONGO_DB_USERNAME = credentials('mongo-db-username')
    MONGO_PASSWORD    = credentials('mongo-db-password')
  }

  stages {
    stage('Unit Testing') {
      options { retry(2) }
      steps {
        sh 'node -v'
        sh 'npm test'
      }
    }
  }
}
```

> **lightbulb** All unit tests will execute inside the `node-18` container by default.\
  You can learn more about the [Jenkins Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/) here.

***

## Adding Parallel Unit Tests

To run tests on multiple Node.js versions simultaneously, we replace the single **Unit Testing** stage with parallel sub-stages:

```groovy theme={null}
pipeline {
  agent {
    kubernetes {
      cloud           'dasher-prod-k8s-us-east'
      yamlFile        'k8s-agent.yaml'
      defaultContainer 'node-18'
    }
  }

  tools {
    nodejs 'nodejs-22-6-0'
  }

  environment {
    MONGO_URI          = 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
    MONGO_DB_CREDENTIALS = credentials('mongo-db-credentials')
    MONGO_USERNAME     = credentials('mongo-db-username')
    MONGO_PASSWORD     = credentials('mongo-db-password')
    SONAR_SCANNER_HOME = tool 'sonar-scanner-610'
    GITEA_TOKEN        = credentials('gitea-api-token')
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
        // other scanning stages...
      }
    }

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
              sh 'sleep 10s'     // avoid port conflicts
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
  }
}
```

| Node.js Version | Container / Image       | Configuration Location     |
| --------------- | ----------------------- | -------------------------- |
| 18              | `defaultContainer`      | Kubernetes Pod (`node-18`) |
| 19              | `container('node-19')`  | Kubernetes Pod (`node-19`) |
| 20              | Docker `node:20-alpine` | Standalone Docker agent    |

***

## Understanding the Node 20 Failure

When the Node 20 stage runs as a separate Docker container, you might encounter:

```console theme={null}
> npm test
> Solar System@6.7.6 test
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit

sh: mocha: not found
script returned exit code 127
```

The error occurs because `npm install` was only executed in the Kubernetes Pod (Node 18/19). The separate Node 20 container has no `node_modules` directory.

> **triangle-alert** Docker agents do not share volumes with your Kubernetes Pod. Make sure to install dependencies inside every container or orchestrate a shared volume mount.

***

## Fixing Dependencies for Node 20

### Quick Fix: Inline `npm install`

Add the install step directly to the Node 20 stage:

```groovy theme={null}
stage('NodeJS 20') {
  agent {
    docker {
      image 'node:20-alpine'
    }
  }
  options { retry(2) }
  steps {
    sh 'npm install'
    sh 'node -v'
    sh 'npm test'
  }
}
```

### Cleaner Approach: Separate Install & Test Sub-Stages

Within the parallel group for Node 20, create two sub-stages—one for installing dependencies, one for running tests:

```groovy theme={null}
stage('Unit Testing') {
  parallel {
    // NodeJS 18 & 19 as before...

    stage('NodeJS 20') {
      parallel {
        stage('Install Dependencies') {
          agent {
            docker {
              image 'node:20-alpine'
            }
          }
          steps {
            sh 'npm install'
          }
        }
        stage('Run Tests') {
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
  }
}
```

This structure ensures each Node.js container installs its own dependencies and runs tests in isolation.

***

## Complete Refactored Pipeline

Putting it all together:

```groovy theme={null}
@Library('dasher-trusted-shared-library@featureTrivyScan') _
pipeline {
  agent {
    kubernetes {
      cloud           'dasher-prod-k8s-us-east'
      yamlFile        'k8s-agent.yaml'
      defaultContainer 'node-18'
    }
  }

  tools {
    nodejs 'nodejs-22-6-0'
  }

  environment {
    MONGO_URI           = 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
    MONGO_DB_CREDENTIALS= credentials('mongo-db-credentials')
    MONGO_USERNAME      = credentials('mongo-db-username')
    MONGO_PASSWORD      = credentials('mongo-db-password')
    SONAR_SCANNER_HOME  = tool 'sonar-scanner-610'
    GITEA_TOKEN         = credentials('gitea-api-token')
  }

  options {
    disableResume()
    disableConcurrentBuilds abortPrevious: true
  }

  stages {
    stage('Installing Dependencies') {
      steps {
        sh 'node -v'
        sh 'npm install --no-audit'
      }
    }

    stage('Dependency Scanning') {
      parallel {
        // other scanning stages...
      }
    }

    stage('Unit Testing') {
      parallel {
        stage('NodeJS 18') { /* ... */ }
        stage('NodeJS 19') { /* ... */ }
        stage('NodeJS 20') {
          parallel {
            stage('Install Dependencies') { /* ... */ }
            stage('Run Tests')           { /* ... */ }
          }
        }
      }
    }
  }
}
```

***

## Links and References

* [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
* [Kubernetes Plugin for Jenkins](https://plugins.jenkins.io/kubernetes/)
* [Node.js Official Docker Images](https://hub.docker.com/_/node)
* [Mocha Test Framework](https://mochajs.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/49e48191-1afc-42bf-9ce5-b98f35b6a2fb/lesson/47b38cbc-2cf3-4710-84d4-ddb5e0c0ce0d)
