# GOOD: simple file copy
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# AVOID if you just need to copy (adds unused tar extraction)
ADD https://example.com/big.tar.xz /usr/src/things/
```

To run as non-root:

```Dockerfile theme={null}
FROM alpine:3.15
RUN addgroup -S appgrp && adduser -S appuser -G appgrp
WORKDIR /home/appuser
COPY app.sh .
USER appuser
CMD ["./app.sh"]
```

![The image shows a webpage from Docker documentation, specifically focusing on Dockerfile best practices, with sections on USER, WORKDIR, and ONBUILD instructions. The browser window also displays multiple open tabs and a taskbar with various applications.](https://kodekloud.com/kk-media/image/upload/v1752873633/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-OPA-Conftest-Docker/dockerfile-best-practices-documentation.jpg)

***

## Default Container User in Kubernetes

By default, containers run as root in Kubernetes pods[^1]. Verify with:

```bash theme={null}
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
app-5d8f7f6c67-abcde              1/1     Running   0          10m

$ kubectl exec -it app-5d8f7f6c67-abcde -- id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),...
```

> **triangle-alert** Running containers as root increases risk of privilege escalation. Always switch to a non-root user in your Dockerfile.

***

## Installing OPA Conftest

[Conftest](https://github.com/open-policy-agent/conftest) evaluates your Dockerfile against custom policies written in Rego.

Linux

```bash theme={null}
wget \
  https://github.com/open-policy-agent/conftest/releases/download/v0.24.0/conftest_0.24.0_Linux_x86_64.tar.gz
tar xzf conftest_0.24.0_Linux_x86_64.tar.gz
sudo mv conftest /usr/local/bin
```

macOS

```bash theme={null}
brew install conftest
```

Windows (Scoop)

```powershell theme={null}
scoop install conftest
```

> **lightbulb** Alternatively, use the official Docker image:\
  `docker pull openpolicyagent/conftest`

***

## Writing Rego Policies

Create a file `opa-docker-security.rego` containing rules like:

```rego theme={null}
package main

# 1. Block secrets in ENV keys
secrets_env = ["passwd", "password", "secret", "key", "token", "apikey"]
deny[msg] {
  input[i].Cmd == "env"
  val = lower(input[i].Value)
  contains(val, secrets_env[_])
  msg = sprintf("Line %d: Potential secret in ENV key: %s", [i, input[i].Value])
}

# 2. Trusted base images only (no slash)
deny[msg] {
  input[i].Cmd == "from"
  count(split(input[i].Value[0], "/")) > 1
  msg = sprintf("Line %d: Use a trusted base image", [i])
}

# 3. No 'latest' tags
deny[msg] {
  input[i].Cmd == "from"
  parts = split(input[i].Value[0], ":")
  contains(lower(parts[1]), "latest")
  msg = sprintf("Line %d: Do not use 'latest' tag for base images", [i])
}

# 4. Avoid curl/wget in RUN
deny[msg] {
  input[i].Cmd == "run"
  val = lower(concat(" ", input[i].Value))
  matches = regex.find_all("(curl|wget)[^ ]*", val, -1)
  count(matches) > 0
  msg = sprintf("Line %d: Avoid curl/wget in RUN", [i])
}

# 5. No system upgrades in RUN
upgrade_cmds = ["apk upgrade", "apt-get upgrade", "dist-upgrade"]
deny[msg] {
  input[i].Cmd == "run"
  val = lower(concat(" ", input[i].Value))
  contains(val, upgrade_cmds[_])
  msg = sprintf("Line %d: Do not upgrade system packages in Dockerfile", [i])
}

# 6. COPY not ADD
deny[msg] {
  input[i].Cmd == "add"
  msg = sprintf("Line %d: Use COPY instead of ADD", [i])
}

# 7. Must switch from root
any_user { input[i].Cmd == "user" }
deny[msg] {
  not any_user
  msg = "Use USER to switch from root"
}
```

***

## Scanning a Dockerfile with Conftest

Given `Dockerfile`:

```Dockerfile theme={null}
FROM adoptopenjdk/openjdk8:alpine-slim
EXPOSE 8080
ARG JAR_FILE=target/*.jar
ADD ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","app.jar"]
```

Run:

```bash theme={null}
docker run --rm -v $(pwd):/project \
  openpolicyagent/conftest test \
  --policy opa-docker-security.rego Dockerfile
```

Output:

```bash theme={null}
FAIL - Dockerfile - main - Line 3: Use COPY instead of ADD
FAIL - Dockerfile - main - Do not run as root, use USER instead
FAIL - Dockerfile - main - Line 1: Use a trusted base image
```

***

## CI/CD Integration

Add a Conftest scan to your Jenkins pipeline:

```groovy theme={null}
stage('Vulnerability Scan - Docker') {
  steps {
    parallel (
      'Dependency Scan': { sh 'mvn dependency-check:check' },
      'Trivy Scan':        { sh 'bash trivy-docker-image-scan.sh' },
      'OPA Conftest': {
        sh """
          docker run --rm -v \$(pwd):/project \
            openpolicyagent/conftest test \
            --policy opa-docker-security.rego Dockerfile
        """
      }
    )
  }
}
```

A Conftest failure will halt the pipeline and highlight policy violations.

***

## Fixing Policy Violations

1. **Trusted base images** – comment or adjust the rule if using a private registry.
2. **Replace `ADD` with `COPY`**.
3. **Create and switch to a non-root user**.

### Adjusted Rego (disable trusted-base-image rule)

```rego theme={null}
package main

# # Block untrusted base images
# deny[msg] {
#   input[i].Cmd == "from"
#   count(split(input[i].Value[0], "/")) > 1
#   msg = sprintf("Line %d: Use a trusted base image", [i])
# ... other rules unchanged ...
```

### Revised Dockerfile

```dockerfile theme={null}
FROM adoptopenjdk/openjdk8:alpine-slim
EXPOSE 8080
ARG JAR_FILE=target/*.jar

# Create non-root user
RUN addgroup -S k8s-pipeline \
 && adduser -S k8s-pipeline -G k8s-pipeline

# Copy artifact & switch user
COPY ${JAR_FILE} /home/k8s-pipeline/app.jar
USER k8s-pipeline

ENTRYPOINT ["java","-jar","/home/k8s-pipeline/app.jar"]
```

Commit and push your changes, then rerun the pipeline.

***

## Verifying the Fixes

```bash theme={null}
docker run --rm -v $(pwd):/project \
  openpolicyagent/conftest test \
  --policy opa-docker-security.rego Dockerfile
# 8 tests, 8 passed, 0 warnings, 0 failures, 0 exceptions
```

Deploy to Kubernetes and confirm non-root:

```bash theme={null}
$ kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
app-7f9c5b4d8d-xyz12                  1/1     Running   0          1m

$ kubectl exec -it app-7f9c5b4d8d-xyz12 -- id
uid=100(k8s-pipeline) gid=101(k8s-pipeline) groups=101(k8s-pipeline)
```

***

## References

* [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [Kubernetes Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
* [Open Policy Agent Conftest](https://github.com/open-policy-agent/conftest)
* [Rego Language Documentation](https://www.openpolicyagent.org/docs/latest/policy-language/)

[^1]: Kubernetes inherit root privileges unless overridden by `securityContext`.

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/d57572e8-95c9-458a-b9f2-a0c5a1da53ad)


# Demo OPA Conftest Kubernetes

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-OPA-Conftest-Kubernetes/page

Integrate OPA Conftest into a Jenkins pipeline to enforce policy-as-code for Kubernetes, preventing misconfigurations and security vulnerabilities.

In this hands-on tutorial, you’ll integrate OPA Conftest into a Jenkins pipeline to enforce custom policy-as-code for Kubernetes Deployments and Services. Scanning your manifests before they reach the cluster helps prevent misconfigurations and potential security vulnerabilities.

![The image is a presentation slide titled "HANDS ON" about Kubernetes vulnerabilities, mentioning OPA Conftest, Kubesc, and Trivy. It includes a meme of a boy excitedly looking at a computer with the text "I CAN'T BELIEVE IT IT'S DEMO TIME."](https://kodekloud.com/kk-media/image/upload/v1752873634/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-OPA-Conftest-Kubernetes/hands-on-kubernetes-vulnerabilities-demo-meme.jpg)

## Prerequisites

* Jenkins server with [Docker](https://docs.docker.com/) installed
* Kubernetes cluster and `kubectl` configured
* OPA Conftest CLI available locally or via Docker

> **lightbulb** Ensure your `kubeconfig` credentials are stored in Jenkins (e.g., under `credentialsId: 'kubeconfig'`) before starting.

## Jenkins Pipeline Stages

Add a vulnerability scan stage between the Docker build and Kubernetes deployment:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Docker Build and Push') {
      steps {
        withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
          sh 'sudo docker build -t siddharth67/numeric-app:${GIT_COMMIT} .'
          sh 'docker push siddharth67/numeric-app:${GIT_COMMIT}'
        }
      }
    }

    stage('Vulnerability Scan - Kubernetes') {
      steps {
        sh '''\
          docker run --rm \
            -v $(pwd):/project \
            openpolicyagent/conftest test \
            --policy opa-k8s-security.rego \
            k8s_deployment_service.yaml
        '''
      }
    }

    stage('Kubernetes Deployment - DEV') {
      steps {
        withKubeConfig([credentialsId: 'kubeconfig']) {
          sh 'sed -i "s|replace|siddharth67/numeric-app:${GIT_COMMIT}|" k8s_deployment_service.yaml'
          sh 'kubectl apply -f k8s_deployment_service.yaml'
        }
      }
    }
  }
}
```

## Defining the OPA Policy

Create `opa-k8s-security.rego` at the root of your project:

```rego theme={null}
package main

deny[msg] {
  input.kind == "Service"
  not input.spec.type == "NodePort"
  msg = "Service type should be NodePort"
}

deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.containers[0].securityContext.runAsNonRoot
  msg = "Containers must not run as root - set runAsNonRoot: true"
}
```

| Resource Kind | Rule Description                                  |
| ------------- | ------------------------------------------------- |
| Service       | `spec.type` must be `NodePort`                    |
| Deployment    | Containers require `securityContext.runAsNonRoot` |

## Running Conftest

From your project directory, run:

```bash theme={null}
docker run --rm \
  -v $(pwd):/project \
  openpolicyagent/conftest test \
  --policy opa-k8s-security.rego \
  k8s_deployment_service.yaml
```

> **triangle-alert** If any policy is violated, Conftest exits with a non-zero code and prints the error. Your Jenkins pipeline will fail until you address the violation.

Example failure output:

```text theme={null}
FAIL: k8s_deployment_service.yaml - main - Containers must not run as root - set runAsNonRoot: true
script returned exit code 1
```

## Fixing Policy Violations

### 1. Enforce `runAsNonRoot`

Update your Deployment spec to include a `securityContext`:

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
        securityContext:
          runAsNonRoot: true
---
apiVersion: v1
kind: Service
metadata:
  name: devsecops
  labels:
    app: devsecops
spec:
  type: NodePort
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
  selector:
    app: devsecops
```

Re-run the Conftest command to confirm that all tests pass.

### 2. Specify Numeric User (Optional)

If you encounter a `CreateContainerConfigError` due to a non-numeric user, add `runAsUser`:

```yaml theme={null}
securityContext:
  runAsNonRoot: true
  runAsUser: 100
```

Commit, push, and trigger a new build.

## Verifying Deployment

After a successful pipeline run, validate your resources:

```bash theme={null}
kubectl get all
```

You should see the Deployment and Service running without errors.

## Links and References

* [OPA Conftest GitHub](https://github.com/open-policy-agent/conftest)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/bc7024d0-ecc8-4b49-b688-7f5f5fcaa67f)
