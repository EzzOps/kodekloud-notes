# Use OpenJDK 8 on Alpine Linux as the base image
FROM openjdk:8-jdk-alpine

# Document the port the application listens on
EXPOSE 9999

# Build-time variable for the JAR file
ARG JAR_FILE=target/*.jar

# Copy the packaged JAR into the container
ADD ${JAR_FILE} app.jar

# Run the JAR file when the container starts
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

Key directives:

* `FROM` sets the base image.
* `EXPOSE` documents which port the app listens on.
* `ARG` defines a build-time variable for your JAR.
* `ADD` copies your artifact into the image.
* `ENTRYPOINT` specifies the startup command.

***

## 2. Building the Docker Image

Run this command from the directory containing your `Dockerfile`. Replace `<docker-hub-username>` and `<image-name>` as needed:

```bash theme={null}
docker build -t <docker-hub-username>/<image-name>:v1 .
```

* `-t` tags your image in the format `repository/name:tag`.

> **lightbulb** Docker caches each layer by default. When you rebuild without changing earlier steps, subsequent builds are faster. To bypass the cache, add `--no-cache`.

***

## 3. Pushing to Docker Hub

First, authenticate using:

```bash theme={null}
docker login
```

Then push your tagged image:

```bash theme={null}
docker push <docker-hub-username>/<image-name>:v1
```

> **triangle-alert** You must be logged in to [Docker Hub](https://hub.docker.com/) before pushing images.\
  Use `docker login` and enter your credentials when prompted.

***

## 4. Running the Container Locally

Map port 9999 on your host to port 9999 in the container:

```bash theme={null}
docker run -d -p 9999:9999 <docker-hub-username>/<image-name>:v1
```

* `-d` runs the container in detached mode.
* `-p host_port:container_port` publishes container ports to the host.

***

## Quick Reference: Docker CLI Commands

| Command       | Purpose                                    | Example                                      |
| ------------- | ------------------------------------------ | -------------------------------------------- |
| docker build  | Build an image from a Dockerfile           | `docker build -t user/app:latest .`          |
| docker push   | Push an image to a registry                | `docker push user/app:latest`                |
| docker login  | Authenticate with a Docker registry        | `docker login`                               |
| docker run    | Create and start a container from an image | `docker run -d -p 8080:8080 user/app:latest` |
| docker images | List all local images                      | `docker images`                              |
| docker ps     | List running containers                    | `docker ps`                                  |

***

## Links and References

* [Docker Documentation](https://docs.docker.com/)
* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Docker Hub | Official Images](https://hub.docker.com/search?q=\&type=image)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/27afe3e0-2262-4663-b351-a527cff536ab)


# Git Repository

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Git-Repository/page

Access a GitHub repository containing a Spring Boot microservice, VM configuration templates for Azure and GCP, and automated setup scripts.

In this guide, you’ll access the GitHub repository that houses:

* A Spring Boot microservice
* VM configuration templates for Azure and GCP
* Automated setup scripts for software installation

Follow these steps to fork or import the repo, then clone it to your local machine or a VM.

## Repository Structure

| Directory/File  | Description                                         | Path           |
| --------------- | --------------------------------------------------- | -------------- |
| Spring Boot app | Java source code and `pom.xml` for Maven build      | `/`            |
| setup/azure     | ARM templates and scripts for provisioning on Azure | `/setup/azure` |
| setup/gcp       | Deployment Manager files for GCP VM configuration   | `/setup/gcp`   |
| scripts         | Shell scripts for software installation and setup   | `/scripts`     |

> **lightbulb** Use the `setup` templates to standardize VM provisioning across Azure and GCP, ensuring consistent security policies.

## 1. Fork or Import the Repository

The upstream repository is named `kubernetes-devops-security`. Forking creates a personal copy under your account:

1. Navigate to the original repo:\
   `https://github.com/<original-username>/kubernetes-devops-security`
2. Click **Fork** (top-right corner) to duplicate under your account.

Alternatively, import it as a new repository:

1. On GitHub, go to **Your repositories > Import repository**.
2. Paste the source URL:
   ```text theme={null}
   https://github.com/<original-username>/kubernetes-devops-security.git
   ```
3. Name your repo, e.g., `devsecops-k8s-demo`.
4. Click **Begin import** and wait for completion.

> **triangle-alert** Ensure you have a GitHub account and proper permissions to fork or import repositories.

## 2. Clone the Repository Locally

After forking or importing, clone to your development environment. First, verify Git is installed:

```bash theme={null}
git --version
```

### 2.1 Using GitHub Desktop

1. Open **GitHub Desktop**.
2. Select **File > Clone Repository**.
3. Under the **URL** tab, enter:
   ```text theme={null}
   https://github.com/<your-username>/devsecops-k8s-demo.git
   ```
4. Choose a local folder and click **Clone**.

### 2.2 Using the Command Line

```bash theme={null}
git clone https://github.com/<your-username>/devsecops-k8s-demo.git
cd devsecops-k8s-demo
```

## 3. Explore VM Templates

Review and customize the VM provisioning templates:

* Azure: `setup/azure/`
* GCP: `setup/gcp/`

Integrate with [Azure Resource Manager](https://docs.microsoft.com/azure/azure-resource-manager/templates/) and [Google Cloud Deployment Manager](https://cloud.google.com/deployment-manager).

## Links and References

* [Spring Boot Documentation](https://spring.io/projects/spring-boot)
* [Azure Quickstart Templates](https://azure.microsoft.com/resources/templates/)
* [GCP Deployment Manager](https://cloud.google.com/deployment-manager/docs)
* [GitHub Fork a Repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)
* [Git CLI Documentation](https://git-scm.com/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/e3585b26-9eae-4a27-8595-9712f56db013)
