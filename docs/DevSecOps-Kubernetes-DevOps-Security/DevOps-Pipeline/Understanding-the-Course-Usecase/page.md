# Jenkins
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update && sudo apt-get install -y openjdk-11-jdk jenkins

# Helm, Terraform, Azure CLI extensions
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
sudo apt-get install -y unzip
curl https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip -o tf.zip
unzip tf.zip && sudo mv terraform /usr/local/bin/
az extension add --name aks-preview
```

## 5. Create a Basic Jenkins Pipeline

Here’s a simple `Jenkinsfile` with four stages:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps { git 'https://github.com/your-org/your-repo.git' }
    }
    stage('Build') {
      steps { sh 'mvn clean package' }
    }
    stage('Test') {
      steps { sh 'mvn test' }
    }
    stage('Deploy') {
      steps { sh './scripts/deploy.sh' }
    }
  }
}
```

## References

* [Azure Free Account](https://azure.microsoft.com/free/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/)
* [Helm Charts](https://helm.sh/docs/topics/charts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/c7663f49-9092-43d7-9192-8445b208a4d8" />
</CardGroup>


# Understanding the Course Usecase

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Understanding-the-Course-Usecase/page

This article explains a microservices architecture using Dockerized Node.js and Spring Boot services with REST API communication.

In this lesson, we’ll walk through our example architecture and the HTTP endpoints each service exposes. We have two simple Dockerized microservices:

1. A Node.js service (runs on port 5000)
2. A Spring Boot service (runs on port 8080)

Both services communicate via REST APIs, demonstrating best practices for containerization and orchestration.

***

## Node.js Microservice (Port 5000)

This lightweight Node.js application is packaged in Docker and listens on port 5000. It offers a single endpoint:

**GET /plusone/**

* **Function**: Takes an integer and returns its value plus one.
* **Example Request**:

  ```bash theme={null}
  curl http://localhost:5000/plusone/41
  # 42
  ```

<Callout icon="lightbulb">
  Ensure Docker is running and the container is listening on port 5000 before invoking this endpoint.
</Callout>

***

## Spring Boot Microservice (Port 8080)

The Spring Boot application exposes three REST endpoints on port 8080. It illustrates service-to-service calls and conditional logic.

| Endpoint        | Description                                                                           | Example                                                             |
| --------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET /           | Returns a welcome message                                                             | `curl http://localhost:8080/`                                       |
| GET /increment/ | Forwards `{number}` to Node.js `/plusone` endpoint and returns the incremented result | `curl http://localhost:8080/increment/41` → `42`                    |
| GET /compare/   | Compares `{number}` against 50 and returns a descriptive message                      | `curl http://localhost:8080/compare/77` → `"77 is greater than 50"` |

### 1. GET /

Returns a simple greeting from the Spring Boot service:

```bash theme={null}
curl http://localhost:8080/
