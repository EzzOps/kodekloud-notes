# Demo OPA Conftest Docker

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-OPA-Conftest-Docker/page

This tutorial demonstrates how to enforce Dockerfile security best practices using Open Policy Agents Conftest.

In this tutorial, we’ll show you how to automatically enforce Dockerfile security best practices using Open Policy Agent's Conftest. You’ll learn to:

1. Review key Dockerfile guidelines
2. Understand Kubernetes’ default container user
3. Install and configure Conftest
4. Write and run Rego policies against your Dockerfile
5. Integrate policy checks into a CI/CD pipeline
6. Remediate common security violations

***

## Table of Contents

* [Dockerfile Security Best Practices](#dockerfile-security-best-practices)
* [Default Container User in Kubernetes](#default-container-user-in-kubernetes)
* [Installing OPA Conftest](#installing-opa-conftest)
* [Writing Rego Policies](#writing-rego-policies)
* [Scanning a Dockerfile with Conftest](#scanning-a-dockerfile-with-conftest)
* [CI/CD Integration](#cicd-integration)
* [Fixing Policy Violations](#fixing-policy-violations)
* [Verifying the Fixes](#verifying-the-fixes)
* [References](#references)

***

## Dockerfile Security Best Practices

Follow [Docker’s official guidelines](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) to reduce vulnerabilities:

| Best Practice      | Description                                                 | Example                                                                                      |
| ------------------ | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Minimal base image | Use smaller images (e.g., Alpine) to reduce attack surface. | `FROM alpine:3.15`                                                                           |
| Pin image tags     | Avoid floating `latest` tags.                               | `FROM nginx:1.21.0`                                                                          |
| Use COPY over ADD  | Prevent unintended archive extraction or remote downloads.  | `COPY src/ /app/`                                                                            |
| Non-root user      | Create and switch to a non-root account.                    | `USER appuser`                                                                               |
| Combine RUN steps  | Limit image layers by chaining commands.                    | `RUN apk add --no-cache curl && rm -rf /var/cache/apk/*`                                     |
| Secure ENV vars    | Do not embed secrets in `ENV`.                              | Use runtime [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/). |

Example: building a minimal BusyBox image

```bash theme={null}
mkdir myproject && cd myproject
echo "hello" > hello
cat > Dockerfile <<EOF
FROM busybox
COPY hello /
RUN cat /hello
EOF
docker build -t helloapp:v1 .
```

Good vs. avoid:

```Dockerfile theme={null}
