# Demo SonarQube Authentication Clarification

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-SonarQube-Authentication-Clarification/page

This guide explains how to streamline SonarQube authentication in Jenkins pipelines using two methods for improved security.

In this guide, we’ll explain how to streamline SonarQube authentication in your Jenkins pipelines. You have two options:

* Supply a login token directly in the Maven CLI using `-Dsonar.login`.
* Let Jenkins inject the token via the `withSonarQubeEnv` wrapper.

Both methods work—choose one to avoid redundancy and improve security.

***

## Authentication Methods Compared

| Method             | Configuration Location | Example                                          | Pros & Cons                               |
| ------------------ | ---------------------- | ------------------------------------------------ | ----------------------------------------- |
| Maven CLI property | `sh "mvn ..."`         | `-Dsonar.login=YOUR_TOKEN`                       | Simple but exposes token in logs          |
| Plugin wrapper     | Jenkinsfile            | `withSonarQubeEnv('SonarQube') { sh "mvn ..." }` | Secure, centralized credential management |

***

## Original Pipeline (with `-Dsonar.login`)

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Mutation Tests - PIT') {
      steps {
        sh "mvn org.pitest:pitest-maven:mutationCoverage"
      }
      post {
        always {
          pitmutation mutationStatsFile: '**/target/pit-reports/**/mutations.xml'
        }
      }
    }

    stage('SonarQube - SAST') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh "mvn sonar:sonar \
            -Dsonar.projectKey=numeric-application \
            -Dsonar.host.url=http://devsecops-demo.eastus.cloudapp.azure.com:9000 \
            -Dsonar.login[AWS_SECRET_ACCESS_KEY]"
        }
        timeout(time: 2, unit: 'MINUTES') {
          script {
            waitForQualityGate abortPipeline: true
          }
        }
      }
    }

    stage('Docker Build and Push') {
      steps {
        withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
          sh 'docker build -t sidhdhart67/numeric-app:"$GIT_COMMIT" .'
          sh 'docker push sidhdhart67/numeric-app:"$GIT_COMMIT"'
        }
      }
    }
  }
}
```

<Callout icon="triangle-alert">
  Using both `withSonarQubeEnv` and `-Dsonar.login` is redundant. Pick one to keep your pipeline clean and secure.
</Callout>

***

## Updated Pipeline (plugin-only authentication)

By removing the `-Dsonar.login` property, Jenkins uses the credentials defined in **Manage Jenkins → Configure System → SonarQube Servers**:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Mutation Tests - PIT') {
      steps {
        sh "mvn org.pitest:pitest-maven:mutationCoverage"
      }
      post {
        always {
          pitmutation mutationStatsFile: '**/target/pit-reports/**/mutations.xml'
        }
      }
    }

    stage('SonarQube - SAST') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh "mvn sonar:sonar \
            -Dsonar.projectKey=numeric-application \
            -Dsonar.host.url=http://devsecops-demo.eastus.cloudapp.azure.com:9000"
        }
        timeout(time: 2, unit: 'MINUTES') {
          script {
            waitForQualityGate abortPipeline: true
          }
        }
      }
    }

    stage('Docker Build and Push') {
      steps {
        withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
          sh 'docker build -t sidhdhart67/numeric-app:"$GIT_COMMIT" .'
          sh 'docker push sidhdhart67/numeric-app:"$GIT_COMMIT"'
        }
      }
    }
  }
}
```

When this pipeline runs, the SonarQube stage completes successfully without exposing the token in the Maven command.

***

## Minimal Jenkinsfile Example

For small projects, you can simplify your Jenkinsfile to just the SonarQube stage:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('SonarQube - SAST') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh """
            mvn sonar:sonar \
              -Dsonar.projectKey=numeric-application \
              -Dsonar.host.url=http://devsecops-demo.eastus.cloudapp.azure.com:9000
          """
        }
      }
    }
  }
  post {
    always {
      timeout(time: 2, unit: 'MINUTES') {
        script {
          waitForQualityGate abortPipeline: true
        }
      }
    }
  }
}
```

<Callout icon="lightbulb">
  The `withSonarQubeEnv` step injects the authentication token automatically. No need for `-Dsonar.login`.
</Callout>

***

## Further Reading

* [Jenkins SonarQube Plugin](https://plugins.jenkins.io/sonar)
* [SonarQube Scanner for Maven](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner-for-maven/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/a3d2a951-7232-4470-b672-f11ac772316a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/812d5090-a3a5-45eb-9d0e-1536216c922f" />
</CardGroup>
