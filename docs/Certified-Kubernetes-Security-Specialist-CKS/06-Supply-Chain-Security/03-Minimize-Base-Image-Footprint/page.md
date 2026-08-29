# Minimize base image footprint

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Supply-Chain-Security/Minimize-Base-Image-Footprint/page

This article provides guidance on minimizing the base image footprint in Docker images for improved efficiency, security, and faster deployments.

Welcome to this comprehensive lesson on minimizing the base image footprint in Docker images. In this guide, you will learn how to structure and optimize your Docker images for efficiency, security, and faster deployments.

## Understanding Base Images

Understanding how images are built is crucial for optimizing them. Consider the following Dockerfile used to build a custom web application image:

```dockerfile theme={null}
