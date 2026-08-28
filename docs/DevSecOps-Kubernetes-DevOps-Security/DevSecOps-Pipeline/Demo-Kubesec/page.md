# Replace placeholder with real image name
sed -i "s|replace|${imageName}|g" k8s_deployment_service.yaml

# Check if deployment exists
if ! kubectl -n default get deployment "${deploymentName}" > /dev/null; then
    echo "Creating deployment ${deploymentName}"
    kubectl -n default apply -f k8s_deployment_service.yaml
else
    echo "Updating image for ${deploymentName} to ${imageName}"
    kubectl -n default set image deploy "${deploymentName}" "${containerName}"="${imageName}" --record=true
fi
```

| Script            | Purpose                                | Key Command                                    |
| ----------------- | -------------------------------------- | ---------------------------------------------- |
| k8s-deployment.sh | Create or update the Deployment object | `kubectl apply` / `kubectl set image --record` |

<Callout icon="triangle-alert">
  Ensure the Jenkins service account has `get`, `create`, `update`, and `rollout` permissions on the target namespace.
</Callout>

## Rollout Status Script: `k8s-deployment-rollout-status.sh`

After a short wait, this script checks the rollout status with a timeout. On failure, it issues a rollback to the previous revision.

```bash theme={null}
#!/bin/bash
# Allow pods to initialize
sleep 60s

# Monitor rollout with a 5-second timeout
if ! kubectl -n default rollout status deploy "${deploymentName}" --timeout=5s | grep -q "successfully rolled out"; then
    echo "Rollout FAILED; rolling back ${deploymentName}"
    kubectl -n default rollout undo deploy "${deploymentName}"
    exit 1
else
    echo "Rollout SUCCESSFUL for ${deploymentName}"
fi
```

| Script                           | Purpose                                | Key Command                                       |
| -------------------------------- | -------------------------------------- | ------------------------------------------------- |
| k8s-deployment-rollout-status.sh | Monitor and rollback on failed rollout | `kubectl rollout status` / `kubectl rollout undo` |

## Jenkinsfile Environment Variables

Define all deployment-specific variables at the top of your `Jenkinsfile` for easy maintenance:

```groovy theme={null}
pipeline {
    agent any

    environment {
        deploymentName = 'devsecops'
        containerName  = 'devsecops-container'
        serviceName    = 'devsecops-svc'
        imageName      = "siddharth67/numeric-app:${GIT_COMMIT}"
        applicationURL = 'http://devsecops-demo.eastus.cloudapp.azure.com/'
        applicationURI = '/increment/99'
    }

    stages {
        stage('Build Artifact - Maven') {
            steps {
                sh 'mvn clean package -DskipTests=true'
                archive 'target/*.jar'
            }
        }
        stage('Unit Tests - JUnit and JaCoCo') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Mutation Tests - PIT') {
            steps {
                sh 'mvn org.pitest:pitest-maven:mutationCoverage'
            }
        }
        stage('SonarQube - SAST') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn sonar:sonar \
                        -Dsonar.projectKey=numeric-application \
                        -Dsonar.host.url=http://devsecops-demo.eastus.cloudapp.azure.com:9000'
                }
            }
        }
        // ... Kubernetes stages go here ...
    }
}
```

## Pushing Changes

Once scripts and `Jenkinsfile` are updated, commit and push:

<Frame>
  ![The image shows a GitHub Desktop interface with a repository named "devsecops-k8s-demo" and a notification indicating that changes are being pushed to the origin. The desktop taskbar is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752873626/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kubernetes-Deployment-Rollout/github-desktop-devsecops-push-notification.jpg)
</Frame>

## Pipeline & Cluster Verification

In the pipeline logs for `k8s-deployment.sh`:

```bash theme={null}
+ bash k8s-deployment.sh
deployment devsecops exists
image name = siddharth67/numeric-app:70a453a78462ec8affbf58f4ab3d566c2283
deployment.apps/devsecops image updated
```

The rollout branch confirms:

```bash theme={null}
sh k8s-deployment-rollout-status.sh
# pods start and transition to RUNNING
```

On the Kubernetes cluster:

```bash theme={null}
root@devsecops-cloud:~$ kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/devsecops-abcdef123        1/1     Running   0          59s
pod/devsecops-ghijkl456        1/1     Running   0          61s
deployment.apps/devsecops      2/2     2         2          5m
...
```

If a pod fails to become `Running`, the rollback script will revert to the previous revision.

## Viewing Rollout History

Inspect recorded change causes for debugging:

```bash theme={null}
kubectl rollout history deploy devsecops
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
...
23        kubectl set image deploy devsecops devsecops-container=siddharth67/numeric-app:70a453a78462ec8affbf58f4ab3d566c2283 --namespace=default --record=true
```

Using `--record=true` captures the exact `kubectl` command and Git commit, making audits and rollbacks straightforward.

## Links and References

* [Kubernetes Rollout Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
* [kubectl rollout](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rollout)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Open Policy Agent Conftest](https://github.com/open-policy-agent/conftest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/78359fa4-45f8-4a3e-acb1-0af55e46a2b2" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/14c813d0-6aba-4cfc-997d-87fb1a921040" />
</CardGroup>


# Demo Kubesec

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-Kubesec/page

This article explains how to scan Kubernetes resource definitions for security best practices using Kubesec.

In this lesson, we’ll walk through scanning Kubernetes resource definitions using [Kubesec](https://kubesec.io/). Kubesec helps you enforce cluster security best practices with a simple CLI, Docker image, or HTTP API.

## Table of Contents

1. [Sample Pod Specification](#sample-pod-specification)
2. [Scanning with Kubesec](#scanning-with-kubesec)
   * CLI
   * Docker Image
   * HTTP API
3. [Bash Wrapper for HTTP API](#bash-wrapper-for-http-api)
4. [Jenkins Pipeline Integration](#jenkins-pipeline-integration)
5. [Improving Your Security Score](#improving-your-security-score)
6. [References](#references)

***

## Sample Pod Specification

Here’s a minimal Pod manifest that enables a read-only root filesystem:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: kubesec-demo
spec:
  containers:
    - name: kubesec-demo
      image: gcr.io/google-samples/node-hello:1.0
      securityContext:
        readOnlyRootFilesystem: true
```

***

## Scanning with Kubesec

You can scan your YAML definitions in three ways:

| Method       | Command Example                                                        |
| ------------ | ---------------------------------------------------------------------- |
| CLI          | `kubesec scan pod.yaml`                                                |
| Docker image | `docker run --rm -i kubesec/kubesec:latest scan /dev/stdin < pod.yaml` |
| HTTP API     | `curl -sSX POST --data-binary @"pod.yaml" https://v2.kubesec.io/scan`  |

### 1. CLI

Install the `kubesec` binary, then run:

```bash theme={null}
$ kubesec scan pod.yaml
```

Sample JSON output:

```json theme={null}
[
  {
    "object": "Pod/kubesec-demo.default",
    "valid": true,
    "message": "Passed with a score of 1 points",
    "score": 1,
    "scoring": [
      {
        "id": "ReadOnlyRootFilesystem",
        "selector": "containers[].securityContext.readOnlyRootFilesystem == true",
        "reason": "Immutable root filesystems increase attack cost",
        "points": 1
      }
    ],
    "advice": [
      {
        "id": "ServiceAccountName",
        "selector": ".spec.serviceAccountName",
        "reason": "Use least-privilege service accounts",
        "points": 1
      },
      {
        "id": "AppArmorAny",
        "selector": "metadata.annotations.\"container.apparmor.security.beta.kubernetes.io/nginx\"",
        "reason": "Define AppArmor policies for stronger isolation",
        "points": 1
      },
      {
        "id": "SeccompAny",
        "selector": "metadata.annotations.\"container.seccomp.security.alpha.kubernetes.io/pod\"",
        "reason": "Apply Seccomp profiles to limit syscalls",
        "points": 1
      },
      {
        "id": "LimitsCPU",
        "selector": "containers[].resources.limits.cpu",
        "reason": "Prevent DoS by enforcing CPU limits",
        "points": 1
      },
      {
        "id": "LimitsMemory",
        "selector": "containers[].resources.limits.memory",
        "reason": "Prevent DoS by enforcing memory limits",
        "points": 1
      }
    ]
  }
]
```

***

## Bash Wrapper for HTTP API

Create a shell function to simplify HTTP scans:

```bash theme={null}
#!/usr/bin/env bash
kubesec_scan() {
  local FILE="${1:?Usage: kubesec_scan <file.yaml>}"
  [[ ! -f "$FILE" ]] && { echo "Error: $FILE not found"; return 1; }

  curl -sSX POST \
    --data-binary @"$FILE" \
    https://v2.kubesec.io/scan
}
```

Call it with:

```bash theme={null}
$ kubesec_scan pod.yaml
```

***

## Jenkins Pipeline Integration

Here’s a sample `Jenkinsfile` that builds a Docker image, pushes it, then runs parallel scans with [Conftest](https://www.conftest.dev/) and Kubesec:

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('Docker Build & Push') {
      steps {
        withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
          sh 'docker build -t youruser/app:$GIT_COMMIT .'
          sh 'docker push youruser/app:$GIT_COMMIT'
        }
      }
    }

    stage('Vulnerability Scan') {
      steps {
        parallel(
          'OPA Scan': {
            sh '''
              docker run --rm -v $(pwd):/project \
                openpolicyagent/conftest test \
                --policy opa-k8s-security.rego \
                k8s_deployment_service.yaml
            '''
          },
          'Kubesec Scan': {
            sh 'bash kubesec-scan.sh'
          }
        )
      }
    }
  }
}
```

### kubesec-scan.sh

```bash theme={null}
#!/usr/bin/env bash
set -euo pipefail

scan_result=$(curl -sSX POST --data-binary @"k8s_deployment_service.yaml" https://v2.kubesec.io/scan)
scan_score=$(jq -r '.[0].score' <<<"$scan_result")
scan_message=$(jq -r '.[0].message' <<<"$scan_result")

echo "Scan Score: $scan_score"
if [[ "$scan_score" -ge 5 ]]; then
  echo "✅ Kubesec Scan Passed: $scan_message"
else
  echo "❌ Kubesec Scan Failed: $scan_message (score $scan_score < 5)"
  exit 1
fi
```

<Callout icon="lightbulb">
  Adjust the threshold (`5` points) to match your team’s security policy.
</Callout>

***

## Improving Your Security Score

Based on the advice from Kubesec, let’s update our Deployment to include:

* A dedicated service account
* AppArmor & Seccomp annotations
* CPU & memory limits
* Immutable root filesystem
* Non-root user execution

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
      annotations:
        container.apparmor.security.beta.kubernetes.io/devsecops-container: runtime/default
        container.seccomp.security.alpha.kubernetes.io/devsecops-container: runtime/default
    spec:
      serviceAccountName: default
      containers:
        - name: devsecops-container
          image: youruser/app:latest
          securityContext:
            runAsNonRoot: true
            runAsUser: 100
            readOnlyRootFilesystem: true
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
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

Re-running the scan:

```bash theme={null}
+ bash kubesec-scan.sh
Scan Score: 5
✅ Kubesec Scan Passed: Passed with a score of 5 points
```

***

## References

* [Kubesec Documentation](https://kubesec.io/)
* [Conftest – Policy Testing](https://www.conftest.dev/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/b3a99bc0-8670-45ea-af08-d34f75ec3267" />
</CardGroup>
