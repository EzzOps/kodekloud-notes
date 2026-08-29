# Extract base image from the first line of Dockerfile
dockerImageName=$(awk 'NR==1 {print $2}' Dockerfile)
echo "Scanning image: $dockerImageName"

# Scan HIGH severity (no failure)
docker run --rm -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 -q image \
  --exit-code 0 --severity HIGH --light \
  $dockerImageName

# Scan CRITICAL severity (fail on detection)
docker run --rm -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 -q image \
  --exit-code 1 --severity CRITICAL --light \
  $dockerImageName

exit_code=$?
echo "Exit code: $exit_code"

if [ $exit_code -eq 1 ]; then
  echo "Image scanning failed. CRITICAL vulnerabilities found."
  exit 1
else
  echo "Image scanning passed. No CRITICAL vulnerabilities found."
  exit 0
fi
```

Make the script executable:

```bash theme={null}
chmod +x trivy-docker-image-scan.sh
```

***

## Verifying in Jenkins

Commit and push your changes. Trigger a Jenkins build to see two parallel steps under the **Vulnerability Scan – Docker** stage:

![The image shows a GitHub Desktop interface with no local changes and options to push commits, open the repository in an editor, view files in Explorer, or open the repository on GitHub. A profile picture is visible in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752873707/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Image-Scan-Docker-1/github-desktop-interface-no-changes.jpg)

![The image shows a Jenkins dashboard with a list of projects, including "checking-versions" and "devsecops-numeric-application," displaying their last success, last failure, and duration. The interface includes navigation options on the left and a user profile icon on the top right.](https://kodekloud.com/kk-media/image/upload/v1752873708/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Image-Scan-Docker-1/jenkins-dashboard-projects-list.jpg)

![The image shows a Jenkins pipeline dashboard with a stage view of a build process, including stages like SCM checkout, Maven build, unit tests, and vulnerability scans. It also features graphs for coverage and dependency-check trends.](https://kodekloud.com/kk-media/image/upload/v1752873710/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Image-Scan-Docker-1/jenkins-pipeline-dashboard-build-process.jpg)

![The image shows a Jenkins dashboard displaying a list of pipeline builds for a project named "devsecops-numeric-application," with their statuses, run numbers, commit messages, durations, and completion times.](https://kodekloud.com/kk-media/image/upload/v1752873711/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Image-Scan-Docker-1/jenkins-dashboard-devsecops-pipeline-builds.jpg)

![The image shows a Jenkins dashboard with a pipeline stage view, including build history and error logs. It displays various stages of a build process, some of which have failed, indicated by red highlights.](https://kodekloud.com/kk-media/image/upload/v1752873712/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Trivy-Image-Scan-Docker-1/jenkins-dashboard-pipeline-stage-view.jpg)

***

## Links and References

* [Trivy Documentation](https://aquasecurity.github.io/trivy/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/6f377ac0-6ca9-405a-8296-6bb893fda2ac)


# Demo Trivy Image Scan Docker 2

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-Trivy-Image-Scan-Docker-2/page

This guide demonstrates using Trivy to scan Docker base images for vulnerabilities and select the most secure option for a Spring Boot application.

In this guide, we use [Trivy](https://github.com/aquasecurity/trivy) to scan Docker base images for vulnerabilities and select the most secure option for a Spring Boot application. We’ll compare five candidates, update the Dockerfile, adjust our Jenkins Pipeline, and verify the build.

## Prerequisites

* Docker installed locally
* Trivy image cache volume (`$WORKSPACE` mapped to `/root/.cache/`)
* A Spring Boot JAR artifact in `target/*.jar`

***

## 1. Scan the Current Base Image

First, scan `myorg/numeric-app:latest`:

```bash theme={null}
docker run --rm \
  -v $WORKSPACE:/root/.cache/ \
  aquasec/trivy:0.17.2 \
  -q image \
  --exit-code 1 \
  --severity CRITICAL \
  --light myorg/numeric-app:latest
