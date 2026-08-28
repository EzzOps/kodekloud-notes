# Additional Pipeline Configuration

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Pipelines/Additional-Pipeline-Configuration/page

This guide explores core declarative directives and components for building robust, maintainable CI/CD pipelines using a Jenkinsfile.

A **Jenkinsfile** is a Groovy-like, text-based script that defines and automates the stages of your CI/CD pipeline. In this guide, we’ll explore the core declarative directives and components you need to build robust, maintainable pipelines.

## Typical Pipeline Structure

A declarative Jenkinsfile usually follows this pattern:

1. **Source:** Checkout code from GitHub, Bitbucket, etc.
2. **Build:** Compile, build, and package your application.
3. **Test:** Execute unit tests, integration tests, and other suites.
4. **Deploy:** Push artifacts to staging or production environments.

Here’s a minimal example illustrating these concepts:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Build') {
      agent { docker { image 'maven:3.6.3-jdk-8' } }
      steps {
        sh 'mvn clean package'
      }
    }
    stage('Unit Testing') {
      steps {
        junit 'target/surefire-reports/*.xml'
      }
    }
    stage('Deploy') {
      when { branch 'main' }
      steps {
        sh './deploy.sh'
      }
    }
  }
}
```

## Key Declarative Directives

| Directive     | Purpose                                           | Example                                        |
| ------------- | ------------------------------------------------- | ---------------------------------------------- |
| `pipeline`    | Root block to define a declarative pipeline       | `pipeline { … }`                               |
| `agent`       | Selects where to execute (node, Docker, label)    | `agent any`<br />`agent { docker { image … }}` |
| `environment` | Defines global or per-stage environment variables | `environment { VAR = 'value' }`                |
| `stages`      | Groups one or more `stage` blocks                 | `stages { stage('Build') { … } }`              |
| `stage`       | A named phase in the pipeline                     | `stage('Test') { … }`                          |
| `steps`       | Sequence of commands or plugin invocations        | `steps { sh 'echo Hello' }`                    |
| `post`        | Post-build actions based on build result          | `post { success { … } failure { … } }`         |
| `when`        | Conditional execution of a stage                  | `when { branch 'main' }`                       |
| `script`      | Embed arbitrary Groovy code                       | `steps { script { … } }`                       |

## environment Directive

Set environment variables globally or override them per-stage:

```groovy theme={null}
pipeline {
  agent any
  environment {
    GLOBAL_VAR = 'foo'
  }
  stages {
    stage('Show Global') {
      steps {
        sh 'echo $GLOBAL_VAR'  // prints foo
      }
    }
    stage('Override Var') {
      environment { GLOBAL_VAR = 'bar' }
      steps {
        sh 'echo $GLOBAL_VAR'  // prints bar
      }
    }
  }
}
```

## post Directive

Define actions to run after the entire pipeline finishes, based on the outcome:

```groovy theme={null}
pipeline {
  agent any
  stages { /* … */ }
  post {
    success { echo 'Pipeline succeeded!' }
    failure { echo 'Pipeline failed!' }
    always  { cleanWs() }
  }
}
```

## script Directive

Use `script` blocks to include complex Groovy logic:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Process Files') {
      steps {
        script {
          def files = ['file1.txt', 'file2.txt']
          files.each { file ->
            sh "echo Processing ${file}"
          }
        }
      }
    }
  }
}
```

<Callout icon="lightbulb">
  Use `script` sparingly. Most tasks can be handled with declarative steps or existing plugins.
</Callout>

## when Directive

Control stage execution based on conditions (branches, environment, tags):

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Deploy to Production') {
      when { branch 'main' }
      steps {
        sh './deploy.sh'
      }
    }
  }
}
```

## credentials Directive

Inject Jenkins-managed credentials securely:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Use Credentials') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'myCredentials',
          usernameVariable: 'USER',
          passwordVariable: 'PASS'
        )]) {
          sh 'echo "Deploying as $USER"'
        }
      }
    }
  }
}
```

<Callout icon="triangle-alert">
  Never print credentials or secrets to the console. Always use the Jenkins credentials store and the appropriate binding methods.
</Callout>

## input Directive

Pause the pipeline for manual approval:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Approval') {
      steps {
        input message: 'Proceed with deployment?', ok: 'Deploy'
      }
    }
  }
}
```

## parameters Directive

Allow customization of pipeline runs:

```groovy theme={null}
pipeline {
  agent any
  parameters {
    string(name: 'ENV', defaultValue: 'dev', description: 'Deployment environment')
    booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Execute unit tests?')
  }
  stages {
    stage('Show Params') {
      steps {
        echo "Environment: ${params.ENV}"
        echo "Run tests: ${params.RUN_TESTS}"
      }
    }
  }
}
```

## stash / unstash Directives

Share files between stages or nodes:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'mvn package'
        stash name: 'app', includes: 'target/*.jar'
      }
    }
    stage('Archive') {
      steps {
        unstash 'app'
        archiveArtifacts artifacts: 'target/*.jar'
      }
    }
  }
}
```

## parallel Directive

Run multiple branches in parallel to speed up the pipeline:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Parallel Tasks') {
      parallel {
        stage('Unit Tests') {
          steps { sh 'mvn test' }
        }
        stage('Security Scan') {
          steps { sh './scan.sh' }
        }
      }
    }
    stage('Finalize') {
      steps { echo 'All parallel tasks complete' }
    }
  }
}
```

***

## Further Reading and References

* [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
* [Declarative Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Shared Library](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/054c2c42-f54a-42a4-ab39-4b432a36aaa1/lesson/c93ac078-4d03-4191-bb8f-7deae5a5e163" />
</CardGroup>
