# CRITICAL: 4, HIGH: 32
```

This reveals 4 critical and 32 high vulnerabilities—unsuitable for production.

***

## 2. Compare Alternative Base Images

We’ll evaluate these images:

1. `openjdk` (latest)
2. `openjdk:8`
3. `openjdk:8-alpine`
4. `adoptopenjdk/openjdk8:alpine-slim`

Use this scan command template:

```bash theme={null}
docker run --rm \
  -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --exit-code 1 \
  --severity CRITICAL \
  --light $IMAGE
```

### 2.1 Summary of Scan Results

| Base Image                        | CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN | Total | Verdict          |
| --------------------------------- | -------- | ---- | ------ | --- | ------- | ----- | ---------------- |
| myorg/numeric-app:latest          | 4        | 32   | –      | –   | –       | 36    | Discard          |
| openjdk                           | 0        | 0    | 0      | 0   | 0       | 0     | Caution (latest) |
| openjdk:8                         | 9        | 26   | 17     | 151 | 5       | 208   | Discard          |
| openjdk:8-alpine                  | –        | –    | –      | –   | –       | 274   | Discard          |
| adoptopenjdk/openjdk8:alpine-slim | 0        | 0    | 0      | 0   | 0       | 0     | Selected (fixed) |

> **triangle-alert** Using the `latest` tag can introduce unexpected changes. Always pin to a specific version for production.

***

## 3. Detailed Scan Examples

### 3.1 openjdk (latest)

```bash theme={null}
docker run --rm \
  -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --exit-code 1 \
  --severity CRITICAL \
  --light openjdk
```

Result:

```text theme={null}
Total: 0 (CRITICAL: 0)
```

### 3.2 openjdk:8

```bash theme={null}
docker run --rm \
  -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --light openjdk:8
```

Result:

```text theme={null}
Total: 208 (UNKNOWN: 5, LOW: 151, MEDIUM: 17, HIGH: 26, CRITICAL: 9)
```

### 3.3 openjdk:8-alpine

```bash theme={null}
docker run --rm \
  -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --light openjdk:8-alpine
```

Result:

```text theme={null}
Total: 274 vulnerabilities
```

### 3.4 adoptopenjdk/openjdk8:alpine-slim

```bash theme={null}
docker run --rm \
  -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --exit-code 1 \
  --light adoptopenjdk/openjdk8:alpine-slim
```

Result:

```text theme={null}
Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)
```

> We choose `adoptopenjdk/openjdk8:alpine-slim` for its zero vulnerabilities and fixed version on Alpine Slim.

***

## 4. Update the Dockerfile

Switch the base image:

```dockerfile theme={null}
FROM adoptopenjdk/openjdk8:alpine-slim
EXPOSE 8080

ARG JAR_FILE=target/*.jar
ADD ${JAR_FILE} app.jar

ENTRYPOINT ["java", "-jar", "/app.jar"]
```

Commit and push these changes. The next Jenkins run will pick up the new base image.

***

## 5. Jenkins Pipeline Configuration

In your `Jenkinsfile`, ensure you have Trivy and Docker build stages:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Vulnerability Scan - Docker') {
      parallel {
        stage('Dependency Scan') {
          steps {
            sh 'mvn dependency-check:check'
          }
        }
        stage('Trivy Scan') {
          steps {
            sh 'bash trivy-docker-image-scan.sh'
          }
        }
      }
    }
    stage('Docker Build and Push') {
      steps {
        withDockerRegistry(credentialsId: 'docker-hub', url: '') {
          sh 'printenv'
          sh 'sudo docker build -t myorg/numeric-app:"$GIT_COMMIT" .'
          sh 'docker push myorg/numeric-app:"$GIT_COMMIT"'
        }
      }
    }
  }
}
```

> **lightbulb** Using `sudo` resolves permission issues on the Trivy cache directory. Alternatively, add the Trivy cache folder to `.dockerignore`.

***

## 6. Build & Scan Logs

```console theme={null}
> sudo docker build -t myorg/numeric-app:"$GIT_COMMIT" .
Sending build context to Docker daemon  19.84kB
Step 1/5 : FROM adoptopenjdk/openjdk8:alpine-slim
...
Successfully built 213b62066198
Successfully tagged myorg/numeric-app:"$GIT_COMMIT"
```

Trivy in the pipeline reports:

```console theme={null}
adoptopenjdk/openjdk8:alpine-slim (alpine 3.13.5)
Total: 0 (CRITICAL: 0)
Exit Code: 0

Image scanning completed. No CRITICAL vulnerabilities found
```

***

## Next Steps

In subsequent lessons, we’ll integrate [OPA Conftest](https://github.com/open-policy-agent/conftest) to enforce Dockerfile best practices and compliance policies.

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/694c51c2-4887-4bc3-9a5c-051cf2883ed0)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/fe16c95a-55eb-4163-8789-5c6c4f012f36)


# Demo Trivy Kubernetes

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-Trivy-Kubernetes/page

This tutorial demonstrates integrating Trivy security scans into a Kubernetes CI/CD pipeline for vulnerability management and deployment.

In this tutorial, you’ll learn how to:

1. Build a Docker image and push it to [Docker Hub](https://hub.docker.com/).
2. Scan Kubernetes manifests with OPA and Kubescape.
3. Perform image vulnerability scans using Trivy.
4. Upgrade a vulnerable dependency (Tomcat) and verify the fix.
5. Deploy the hardened image to a Kubernetes cluster.

This end-to-end demo uses **Jenkins**, **Docker**, **OPA**, **Kubescape**, and **Trivy** to enforce security gates in your CI/CD pipeline.

***

## 1. Jenkins Pipeline Configuration

Define your pipeline with a reusable `imageName` environment variable:

```groovy theme={null}
pipeline {
  agent any

  environment {
    imageName = "siddharth67/numeric-app:${GIT_COMMIT}"
  }

  stages {
    stage('Build Artifact - Maven')            { /* ... */ }
    stage('Unit Tests - JUnit & JaCoCo')      { /* ... */ }
    stage('Mutation Tests - PIT')             { /* ... */ }
    stage('SonarQube - SAST')                 { /* ... */ }
    stage('Docker Build & Push')              { /* see below */ }
    stage('Vulnerability Scan - Kubernetes')  { /* see below */ }
    stage('Trivy Scan')                       { /* see below */ }
    stage('Kubernetes Deployment')            { /* ... */ }
  }
}
```

| Stage                           | Purpose                                             |
| ------------------------------- | --------------------------------------------------- |
| Build Artifact - Maven          | Compile code & package JAR                          |
| Unit Tests - JUnit & JaCoCo     | Validate functionality & track code coverage        |
| Mutation Tests - PIT            | Assess test suite robustness                        |
| SonarQube - SAST                | Static code analysis                                |
| Docker Build & Push             | Build Docker image & push to registry               |
| Vulnerability Scan - Kubernetes | Lint & security test K8s manifests (OPA, Kubescape) |
| Trivy Scan                      | Container image vulnerability scan                  |
| Kubernetes Deployment           | Deploy to target cluster                            |

***

### 1.1 Docker Build & Push

```groovy theme={null}
stage('Docker Build & Push') {
  steps {
    withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
      sh 'docker build -t ${imageName} .'
      sh 'docker push ${imageName}'
    }
  }
}
```

***

### 1.2 Kubernetes Manifest Scans

```groovy theme={null}
stage('Vulnerability Scan - Kubernetes') {
  steps {
    parallel(
      'OPA Scan': {
        sh '''
          docker run --rm \
            -v $(pwd):/project \
            openpolicyagent/conftest test \
            --policy opa-k8s-security.rego \
            k8s_deployment_service.yaml
        '''
      },
      'Kubescape Scan': {
        sh 'bash kubescape-scan.sh'
      }
    )
  }
}
```

***

### 1.3 Trivy Scan Stage

```groovy theme={null}
stage('Trivy Scan') {
  steps {
    sh 'bash trivy-k8s-scan.sh'
  }
}
```

***

## 2. Trivy Scan Script

Create `trivy-k8s-scan.sh` at the root of your repo:

```bash theme={null}
#!/usr/bin/env bash
set -o errexit
echo "🔍 Scanning image: $imageName"
