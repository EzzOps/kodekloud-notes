# Demo Fixing Script and Read Only Root File System

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-Fixing-Script-and-Read-Only-Root-File-System/page

This tutorial covers troubleshooting a Deployment script in Kubernetes and enabling a read-only root filesystem without disrupting writable paths.

In this tutorial, you’ll learn how to troubleshoot a Deployment script that skips full manifest updates and how to enable a read-only root filesystem in your container without breaking writable paths like `/tmp`.

## Table of Contents

* [Problem Overview](#problem-overview)
* [Initial Deployment Configuration](#initial-deployment-configuration)
* [Why `readOnlyRootFilesystem` Isn’t Applied](#why-readonlyrootfilesystem-isnt-applied)
* [Original Deployment Script Analysis](#original-deployment-script-analysis)
* [Quick Workaround: Always Apply Manifest](#quick-workaround-always-apply-manifest)
* [Solution: Mounting an `emptyDir` Volume](#solution-mounting-an-emptydir-volume)
* [Applying the Updated Manifest](#applying-the-updated-manifest)
* [Verification Steps](#verification-steps)
* [Best Practices](#best-practices)
* [References](#references)

***

## Problem Overview

You’ve added `readOnlyRootFilesystem: true` to your container’s `securityContext`, but after deployment, the pod spec doesn’t reflect this change. The Deployment script only updates the image, never reapplies the full YAML, so new securityContext settings are ignored.

## Initial Deployment Configuration

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
      containers:
        - name: devsecops-container
          image: replace
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

After applying:

```bash theme={null}
kubectl get po devsecops-66cd4b7475-8fn5d -o yaml | grep readOnlyRootFilesystem
