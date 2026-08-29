# <no output>
```

## Why `readOnlyRootFilesystem` Isn’t Applied

Because the deployment script checks for an existing Deployment and only runs `kubectl set image…`, it never reapplies the manifest changes (securityContext, volumes, etc.).

## Original Deployment Script Analysis

```bash theme={null}
#!/bin/bash
# Replace image placeholder
sed -i "s|replace|${imageName}|g" k8s_deployment_service.yaml
kubectl get deployment ${deploymentName} > /dev/null

if [[ $? -ne 0 ]]; then
    echo "deployment ${deploymentName} doesn't exist"
    kubectl apply -f k8s_deployment_service.yaml
else
    echo "deployment ${deploymentName} exists, updating image to ${imageName}"
    kubectl -n default set image deployment ${deploymentName} \
      ${containerName}=${imageName} --record=true
fi
```

This script never picks up any YAML changes besides the image tag.

## Quick Workaround: Always Apply Manifest

```bash theme={null}
#!/bin/bash
sed -i "s|replace|${imageName}|g" k8s_deployment_service.yaml
# Always apply full manifest to pick up config changes
kubectl -n default apply -f k8s_deployment_service.yaml
```

<Callout icon="triangle-alert">
  Always applying the full manifest will restart pods and may cause brief downtime. Plan for rolling updates.
</Callout>

After pushing this change, pods now crash with:

```bash theme={null}
kubectl logs devsecops-6d547ad96b-67x7n
# org.springframework.context.ApplicationContextException: Unable to start web server;
# nested exception is org.springframework.boot.web.server.WebServerException:
# Unable to create tempDir. java.io.tmpdir is set to /tmp
```

Since `/tmp` is on a read-only root, the Spring Boot app can’t create its temp directory.

## Solution: Mounting an `emptyDir` Volume

To provide a writable `/tmp` while keeping the rest of the filesystem read-only, add an `emptyDir` volume and mount it at `/tmp`.

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
      serviceAccountName: default
      volumes:
        - name: tmp-vol
          emptyDir: {}
      containers:
        - name: devsecops-container
          image: replace
          volumeMounts:
            - name: tmp-vol
              mountPath: /tmp
          securityContext:
            runAsNonRoot: true
            runAsUser: 100
            readOnlyRootFilesystem: true
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

<Callout icon="lightbulb">
  The `emptyDir` volume is ephemeral and only persists for the pod’s lifetime. Use a `PersistentVolume` if you need data durability.
</Callout>

## Applying the Updated Manifest

```bash theme={null}
kubectl -n default apply -f k8s_deployment_service.yaml
```

## Verification Steps

| Step                               | Command                                                               | Expected Output                                          |
| ---------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------- |
| 1. Check pods are running          | `kubectl get pods`                                                    | All pods in `Running` state                              |
| 2. Confirm readOnlyRootFilesystem  | `kubectl get po devsecops-xxx -o yaml \| grep readOnlyRootFilesystem` | `readOnlyRootFilesystem: true`                           |
| 3. Test write to `/etc`            | `kubectl exec -it devsecops-xxx -- touch /etc/deny && echo ok`        | `touch: cannot touch '/etc/deny': Read-only file system` |
| 4. Test write to `/tmp`            | `kubectl exec -it devsecops-xxx -- touch /tmp/allow && echo ok`       | `ok`                                                     |
| 5. Verify application startup logs | `kubectl logs devsecops-xxx`                                          | Tomcat and Spring Boot start messages                    |

## Best Practices

| Resource        | Purpose                                       | Reference                                                                                     |
| --------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------- |
| securityContext | Enforce container security policies           | [Kubernetes Docs](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) |
| emptyDir volume | Provide ephemeral writable storage            | [emptyDir Volume](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)              |
| Rolling Updates | Minimize downtime when applying new manifests | [Deployments](https://kubernetes.[SECRET_REDACTED]/)          |

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Spring Boot Reference Guide](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/)
* [Deployments in Kubernetes](https://kubernetes.[SECRET_REDACTED]/)
* [emptyDir Volume](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/c502eeeb-4e4b-4054-8860-ea5829bcbb29" />
</CardGroup>


# Demo Integration Tests

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-Integration-Tests/page

This guide explains how to add integration testing to a Jenkins Pipeline for a Kubernetes system using curl commands.

Integration tests ensure that individual components in your application communicate correctly when combined. This guide shows how to add an integration testing stage to a Jenkins Pipeline for a Kubernetes-based system using simple `curl` commands.

## What You Will Learn

* How to verify HTTP response codes and payloads with `curl`
* Embedding integration tests in a Jenkinsfile
* Rolling back failed deployments automatically

## Why Integration Testing Matters

Integration testing catches issues that unit tests cannot, such as network connectivity, misconfigured services, or data serialization errors. For a REST API, common checks include:

* HTTP status codes
* Response headers
* Payload validation (JSON, XML, or plain text)

## Architecture Overview

Our demo application consists of two microservices:

1. A **Spring Boot** service listening on a NodePort (e.g., `31933`)
2. A **Node.js** service that processes business logic

The Spring Boot service forwards requests to the Node.js service. We will run two `curl`-based tests:

1. Check that `/increment/99` returns HTTP 200
2. Confirm payload increments 99 to 100

<Frame>
  ![The image is a diagram explaining integration tests for a Kubernetes-based application, showing the interaction between a Spring Boot microservice and a Node.js microservice. It includes details about ports, endpoints, and the testing focus areas like HTTP response codes and payloads.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873625/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Integration-Tests/kubernetes-integration-tests-diagram.jpg)
</Frame>

### Manual Curl Commands

Use these commands for a quick sanity check:

```bash theme={null}
