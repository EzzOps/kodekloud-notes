# Demo SonarQube

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-SonarQube/page

This guide explains integrating SonarQube static analysis into a Jenkins pipeline for a Spring Boot application.

In this guide, you’ll learn how to integrate SonarQube static analysis into a Jenkins pipeline for a Spring Boot application. We’ll cover:

* Starting SonarQube in Docker
* Creating and configuring a SonarQube project
* Running analysis locally with Maven
* Embedding SonarQube in your Jenkinsfile
* Enforcing custom quality gates

## Prerequisites

* Docker installed and running
* Jenkins server with Docker and Pipeline plugins
* Maven project for your Spring Boot application

> **lightbulb** Ensure your SonarQube Docker container always listens on port **9000** after VM restarts.

## 1. Start and Verify SonarQube Container

Run SonarQube in Docker:

```bash theme={null}
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
```

Confirm the container is up:

```bash theme={null}
docker ps -a | grep -i sonar
