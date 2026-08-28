# e.g. 14f8cea6ad4b0a883997e96d4a6a7
```

<Callout icon="lightbulb">
  Save this initial password—you’ll use it to generate an API token in the installer script.
</Callout>

## 2. Explore the Plugin Installer Script

Assuming you cloned the `devsecops-k8s-demo` repository, navigate to the Jenkins plugins directory:

```bash theme={null}
cd devsecops-k8s-demo/setup/jenkins-plugins/
ls -l
```

| File                  | Purpose                                                        |
| --------------------- | -------------------------------------------------------------- |
| `plugins.txt`         | Lists each plugin and its version                              |
| `plugin-installer.sh` | Bash script to call the Jenkins Remote API for plugin installs |

### 2.1 plugins.txt

Here’s how the file lists desired plugins:

| Plugin                          | Version |
| ------------------------------- | ------- |
| performance                     | 3.18    |
| docker-workflow                 | 1.26    |
| dependency-check-jenkins-plugin | 5.1.1   |
| blueocean                       | 2.24.7  |
| jacoco                          | 2.0.7   |
| slack                           | 2.4.8   |
| sonar                           | 2.13.1  |
| pitmutation                     | 1.0.2   |
| kubernetes-cli                  | 1.10.2  |

### 2.2 plugin-installer.sh

This Bash script automates plugin installation using the Jenkins Remote API and `jq` for JSON parsing:

```bash theme={null}
#!/bin/bash
set -e

JENKINS_URL="http://localhost:8080"
ADMIN_USER="admin"
ADMIN_PASSWORD=$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword)

# Fetch CRSF protection crumb
JENKINS_CRUMB=$(
  curl -s --cookie-jar /tmp/cookies \
       -u ${ADMIN_USER}:${ADMIN_PASSWORD} \
       "${JENKINS_URL}/crumbIssuer/api/json" \
  | jq -r .crumb
)

# Generate a new API token for 'admin'
JENKINS_TOKEN=$(
  curl -s -X POST \
       -H "Jenkins-Crumb:${JENKINS_CRUMB}" \
       --cookie /tmp/cookies \
       -u ${ADMIN_USER}:${ADMIN_PASSWORD} \
       "${JENKINS_URL}/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken?newTokenName=plugin-installer" \
  | jq -r .data.tokenValue
)

echo "Jenkins URL: ${JENKINS_URL}"
echo "API Token: ${JENKINS_TOKEN}"

# Install each plugin from plugins.txt
while read -r plugin; do
  echo "Installing ${plugin}..."
  curl -s --user "${ADMIN_USER}:${JENKINS_TOKEN}" \
       -H "Content-Type: text/xml" \
       --data "<jenkins><install plugin='${plugin}' /></jenkins>" \
       "${JENKINS_URL}/pluginManager/installNecessaryPlugins"
done < plugins.txt

echo "Plugin installation requests sent."
echo "Some plugins may require a safe restart:"
echo "  ${JENKINS_URL}/safeRestart"
```

<Callout icon="triangle-alert">
  Ensure `jq` is installed (`sudo apt-get install -y jq`) and Jenkins is accessible at `localhost:8080` before running the script.
</Callout>

## 3. Run the Installer

Execute the installer script:

```bash theme={null}
bash plugin-installer.sh
```

Sample output:

```text theme={null}
Jenkins URL: http://localhost:8080
API Token: 8f2a...
Installing performance@3.18...
Installing docker-workflow@1.26...
…
Installing kubernetes-cli@1.10.2...
Plugin installation requests sent.
Some plugins may require a safe restart:
  http://localhost:8080/safeRestart
```

## 4. Verify Plugin Installation

1. Open **Manage Jenkins → Manage Plugins → Installed** in the Jenkins UI.
2. If any plugin is missing, switch to **Available**, search for it (e.g., “Kubernetes CLI”), select the version, and click **Install without restart**.

## 5. Next Steps

With your plugins in place, create a Jenkins pipeline that integrates Maven, Docker, and Kubernetes to validate the new capabilities.

***

## Links and References

* [Jenkins Remote API](https://www.jenkins.io/doc/book/using/remote-access-api/)
* [jq Manual](https://stedolan.github.io/jq/manual/)
* [Manage Jenkins Plugins](https://www.jenkins.io/doc/book/managing/plugins/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/a0b190ab-bc14-456a-a160-8c04e292849d" />
</CardGroup>


# Demo Kubernetes Deployment

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Demo-Kubernetes-Deployment/page

This tutorial covers a CI/CD workflow for deploying a Spring Boot application to Kubernetes using Jenkins Pipeline.

In this tutorial, we’ll walk through a complete CI/CD workflow that builds a Spring Boot application, runs tests, publishes a Docker image, and deploys it to a Kubernetes cluster using a Jenkins Pipeline. Our Git repo contains a Kubernetes manifest (`k8s_deployment_service.yaml`) defining both a Deployment and a Service.

***

## Table of Contents

* [Jenkins Pipeline (Jenkinsfile)](#jenkins-pipeline-jenkinsfile)
* [Kubernetes Deployment & Service Manifest](#kubernetes-deployment--service-manifest)
* [Deploying the Node.js Service](#deploying-the-nodejs-service)
* [Numeric Spring Boot Application](#numeric-spring-boot-application)
* [Verifying the Deployment](#verifying-the-deployment)
* [Links & References](#links--references)

***

## Jenkins Pipeline (Jenkinsfile)

<Callout icon="lightbulb">
  This pipeline leverages Maven for build and test, Docker for image creation and pushing, and the Kubernetes CLI (`kubectl`) for deployment.
</Callout>

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('Build Artifact - Maven') {
      steps {
        sh 'mvn clean package -DskipTests=true'
        archiveArtifacts 'target/*.jar'
      }
    }

    stage('Unit Tests - JUnit & JaCoCo') {
      steps {
        sh 'mvn test'
      }
      post {
        always {
          junit 'target/surefire-reports/*.xml'
          jacoco execPattern: 'target/jacoco.exec'
        }
      }
    }

    stage('Docker Build & Push') {
      steps {
        withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
          sh 'docker build -t siddharth67/numeric-app:${GIT_COMMIT} .'
          sh 'docker push siddharth67/numeric-app:${GIT_COMMIT}'
        }
      }
    }

    stage('Kubernetes Deployment - DEV') {
      steps {
        withKubeConfig([credentialsId: 'kubeconfig']) {
          sh 'sed -i "s#replace#siddharth67/numeric-app:${GIT_COMMIT}#g" k8s_deployment_service.yaml'
          sh 'kubectl apply -f k8s_deployment_service.yaml'
        }
      }
    }
  }
}
```

***

## Kubernetes Deployment & Service Manifest

The `k8s_deployment_service.yaml` file defines:

* A **Deployment** named `devsecops` with 2 replicas.
* A **Service** of type `NodePort` exposing port 8080.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devsecops
  labels:
    app: devsecops
spec:
  replicas: 2
  selector:
    matchLabels:
      app: devsecops
  template:
    metadata:
      labels:
        app: devsecops
    spec:
      containers:
        - name: devsecops-container
          image: replace

---

apiVersion: v1
kind: Service
metadata:
  name: devsecops-svc
  labels:
    app: devsecops
spec:
  type: NodePort
  selector:
    app: devsecops
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
```

| Resource Type | Purpose                            | Example Command                                |
| ------------- | ---------------------------------- | ---------------------------------------------- |
| Deployment    | Manages replicated Pods            | `kubectl apply -f k8s_deployment_service.yaml` |
| Service       | Exposes Pods internally/externally | `kubectl expose ...`                           |

<Callout icon="triangle-alert">
  Ensure you replace the placeholder `replace` with your Docker image tag (`siddharth67/numeric-app:${GIT_COMMIT}`) before applying the manifest.
</Callout>

***

## Deploying the Node.js Service

We need a backend service that our Spring Boot app will call. Deploy a pre-built Node.js service (`siddharth67/node-service:v1`) in the `default` namespace:

```bash theme={null}
