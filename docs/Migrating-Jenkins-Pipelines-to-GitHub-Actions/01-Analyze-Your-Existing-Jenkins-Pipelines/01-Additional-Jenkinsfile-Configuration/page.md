# Additional Jenkinsfile Configuration

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Additional-Jenkinsfile-Configuration/page

Guide to Declarative Jenkinsfiles explaining pipeline structure directives stages agents environment variables credentials post actions and examples for building testing and deploying applications

Let's break down and understand the syntaxes and components used within a Jenkinsfile.

<Frame>
  <img alt="A minimalist slide showing the word &#x22;Jenkinsfile&#x22; on the left and a white document icon on a teal gradient shape on the right. The slide includes a small &#x22;© Copyright KodeKloud&#x22; notice at the bottom." />
</Frame>

A Jenkinsfile is the cornerstone of your CI/CD automation. It is a text-based script written in a Groovy-like Declarative syntax that defines the stages, agents, environment, and lifecycle of your pipeline.

This article covers Declarative Pipelines only. If you need more advanced programmatic control, you can use Scripted Pipelines or `script` blocks inside Declarative Pipelines.

At a high level, a Jenkinsfile organizes work into distinct stages such as:

* Checkout: retrieve source code from GitHub, GitLab, Bitbucket, etc.
* Build: compile, build, and package the application.
* Test: run unit, integration, and other tests.
* Deploy: publish artifacts to staging/production environments.

The common Declarative pipeline blocks and directives are described below, with examples.

> **lightbulb** This guide focuses on Declarative Pipelines. Declarative syntax provides clearer structure for CI/CD flows; use `script { ... }` blocks when you need Groovy logic for advanced conditions or iteration.

## Common Declarative blocks and directives

| Directive           | Purpose                                                              | Example / Notes                                                                 |
| ------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `pipeline`          | Root block that defines the pipeline                                 | `pipeline { ... }`                                                              |
| `agent`             | Where to run the pipeline or a stage (e.g. `any`, `label`, `docker`) | `agent any` or `agent { docker { image 'maven:3-alpine' } }`                    |
| `stages` / `stage`  | Group and name work stages                                           | `stages { stage('Build') { steps { ... } } }`                                   |
| `steps`             | Actual commands or plugin steps executed inside a stage              | `steps { sh 'mvn -q package' }`                                                 |
| `environment`       | Define env vars at pipeline or stage scope                           | `environment { VAR = 'value' }`                                                 |
| `parameters`        | Parameterize pipeline runs                                           | `parameters { string(name: 'ENV', defaultValue: 'dev') }`                       |
| `post`              | Actions to run after pipeline/stage completion                       | `post { success { ... } failure { ... } }`                                      |
| `when`              | Conditional execution of a stage                                     | `when { branch 'main' }` or `when { expression { env.BRANCH_NAME == 'main' } }` |
| `tools`             | Declare tool installations (e.g., JDK, Maven)                        | `tools { maven 'M3' }`                                                          |
| `options`           | Pipeline options like timestamps, timeout                            | `options { timeout(time: 1, unit: 'HOURS') }`                                   |
| `stash` / `unstash` | Pass files between stages/nodes                                      | `stash name: 'app', includes: 'target/*.jar'`                                   |
| `parallel`          | Run multiple branches concurrently inside a stage                    | `parallel { stage('A') { ... } stage('B') { ... } }`                            |

For the full list of Declarative directives, see the official Jenkins Pipeline Syntax documentation: [https://www.jenkins.io/doc/book/pipeline/syntax/](https://www.jenkins.io/doc/book/pipeline/syntax/)

## Example: Basic Declarative Pipeline

A compact, practical example illustrating agents, stages, a Docker-based build step, test publishing, branch-based deploy condition, and post actions:

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Build') {
            agent { docker { image 'maven:3-alpine' } }
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Unit Test') {
            steps {
                junit 'target/surefire-reports/*.xml'
            }
        }

        stage('Deploy') {
            when {
                expression { env.BRANCH_NAME == 'main' }
            }
            steps {
                sh './deploy.sh'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
```

Notes on the example above:

* `pipeline {}` marks the start of the Declarative pipeline.
* `agent any` at the root means the pipeline can run on any available Jenkins agent by default.
* The `Build` stage overrides the agent and runs inside a Docker container (`maven:3-alpine`) so Maven is available without configuring the node.
* `junit` collects and publishes test results to Jenkins.
* The `Deploy` stage uses a `when` expression to run only on the `main` branch.
* `post` defines lifecycle hooks executed after the pipeline finishes (e.g., `success`, `failure`, `always`).

## Environment variables

Use the `environment` directive to declare variables available to all stages (or declare them inside individual stages to limit scope):

```groovy theme={null}
pipeline {
  environment {
    VAR1 = 'foo'
    VAR2 = 'bar'
  }

  stages {
    stage('Build') {
      steps {
        sh 'echo $VAR1' // prints: foo
      }
    }

    stage('Test') {
      environment { VAR1 = 'test' } // overrides VAR1 for this stage
      steps {
        sh 'echo $VAR1' // prints: test
      }
    }
  }
}
```

## Post actions and notifications

`post` runs after the pipeline or a stage completes. It’s commonly used for notifications, artifact archiving, and cleanup.

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'mvn -q -DskipTests package'
      }
    }
  }

  post {
    success {
      echo 'Send success notification'
      // e.g. slackSend(channel: '#team', message: "Build succeeded")
    }
    failure {
      echo 'Send failure notification'
    }
    always {
      echo 'Cleanup or archive artifacts'
    }
  }
}
```

Slack notification example using the Pipeline Slack plugin:

```groovy theme={null}
post {
  always {
    slackSend(
      channel: '#your-slack-channel',
      message: "Build ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}"
    )
  }
}
```

## Script blocks for advanced logic

Wrap Groovy code in `script { ... }` to use loops, conditionals, and pipeline APIs:

```groovy theme={null}
stage('Process Files') {
  steps {
    script {
      def files = ['file1.txt', 'file2.txt']
      files.each { f ->
        sh "echo Processing ${f}"
      }
    }
  }
}
```

Script blocks are your gateway to logic that Declarative syntax cannot express natively.

## When conditions

`when` controls whether a stage runs. You can use simple built-in conditions or full expressions:

Branch-based condition:

```groovy theme={null}
stage('Deploy') {
  when {
    branch 'main'
  }
  steps {
    sh './deploy.sh'
  }
}
```

Expression-based condition:

```groovy theme={null}
when {
  expression { env.BRANCH_NAME == 'main' }
}
```

## Credentials (secure secrets handling)

Use `withCredentials` to inject credentials into the build environment without exposing them in logs.

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('Example with credentials') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'myCredentials',
                                          usernameVariable: 'USERNAME',
                                          passwordVariable: 'PASSWORD')]) {
          sh 'echo "Username: $USERNAME"'
          // Avoid printing secrets in real pipelines; use them only where needed.
        }
      }
    }
  }
}
```

> **warning** Never print secrets to logs. Use credentials only in the steps that require them and prefer credential-binding plugins over hard-coding.

## Interactive input (manual approvals)

Use `input` to pause the pipeline and require a human confirmation for sensitive steps such as production deploys:

```groovy theme={null}
stage('Manual Approval') {
  steps {
    input message: 'Are you sure you want to deploy?', ok: 'Yes'
    sh './deploy.sh'
  }
}
```

## Parameters

Define parameters to run pipelines with configurable values. Use `params` to access them at runtime:

```groovy theme={null}
pipeline {
  agent any

  parameters {
    string(name: 'ENV_NAME', defaultValue: 'dev', description: 'Environment to deploy to')
  }

  environment {
    ENV = "${params.ENV_NAME}"
  }

  stages {
    stage('Show Env') {
      steps {
        sh 'echo "Deploying to $ENV"'
      }
    }
  }
}
```

## Stash and unstash (passing files between stages/nodes)

`stash` stores files temporarily so another stage (possibly on a different agent) can `unstash` them:

```groovy theme={null}
stage('Build') {
  steps {
    sh 'mvn -q package'
    stash name: 'build-artifacts', includes: 'target/*.jar'
  }
}

stage('Deploy') {
  steps {
    unstash 'build-artifacts'
    sh './deploy-with-artifacts.sh'
  }
}
```

## Parallel stages

Run independent tasks concurrently with `parallel` to reduce overall pipeline time:

```groovy theme={null}
stage('Tests') {
  parallel {
    stage('Unit Testing') {
      steps {
        sh 'mvn -q test'
      }
    }
    stage('Vulnerability Scanning') {
      steps {
        sh './vuln-scan.sh'
      }
    }
  }
}
```

## Putting it all together

Declarative pipelines support many directives—`agent`, `environment`, `parameters`, `stages`, `post`, `options`, `tools`, `triggers`, and more. The examples above cover the most commonly used features. Use `script {}` for advanced Groovy logic and combine plugins (JUnit, Slack, Docker, Credentials, etc.) to integrate Jenkins with the rest of your toolchain.

This guide gives you a solid foundation to author and maintain Declarative Jenkinsfiles for CI/CD. Explore the official docs and plugin pages to extend pipeline capabilities based on your CI requirements.

## Links and references

* Jenkins Pipeline Syntax: [https://www.jenkins.io/doc/book/pipeline/syntax/](https://www.jenkins.io/doc/book/pipeline/syntax/)
* Jenkins Declarative Pipeline: [https://www.jenkins.io/doc/book/pipeline/development/](https://www.jenkins.io/doc/book/pipeline/development/)
* Credentials Binding Plugin: [https://plugins.jenkins.io/credentials-binding/](https://plugins.jenkins.io/credentials-binding/)
* Jenkins Plugins: [https://plugins.jenkins.io/](https://plugins.jenkins.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/cf81c203-622b-412d-856b-696fc468083b)
