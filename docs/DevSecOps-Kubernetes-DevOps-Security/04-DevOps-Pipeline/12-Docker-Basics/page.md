# Docker Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Docker-Basics/page

Learn to containerize applications using Docker by defining environments, building images, pushing to registries, and running containers locally.

Docker containers bundle everything an application needs to run—and nothing more—making it simple to move workloads across environments. In this guide, you’ll learn how to:

1. Define your app environment with a **Dockerfile**
2. **Build** a container image
3. **Push** the image to a registry (e.g., Docker Hub)
4. **Run** the image locally

***

## 1. Writing a Dockerfile

Start by creating a `Dockerfile` in your project root. This example shows a Spring Boot application running on OpenJDK 8 (Alpine):

```dockerfile theme={null}
