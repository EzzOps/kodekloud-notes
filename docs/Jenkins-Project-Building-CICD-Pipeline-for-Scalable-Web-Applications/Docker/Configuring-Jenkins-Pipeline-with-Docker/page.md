# A dictionary to store tasks with an ID
tasks = {}
task_id_counter = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global task_id_counter
    response_text = ""

    if request.method == 'POST':
        if 'add_task' in request.form:
            task_content = request.form.get('task_content')
            if task_content:
                tasks[task_id_counter] = task_content
                task_id_counter += 1

        elif 'delete_task' in request.form:
            task_id_to_delete = int(request.form.get('task_id_to_delete'))
            tasks.pop(task_id_to_delete, None)

    return render_template('index.html', tasks=tasks)
```

## Creating the Dockerfile

To containerize the Flask application, create a Dockerfile that includes instructions for setting the base image, copying your source code, installing dependencies, exposing the necessary port, and starting the application.

Below is an example Dockerfile for our Flask app:

```dockerfile theme={null}
FROM python:3.12.0b3-alpine3.18
COPY /application
WORKDIR /application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

This Dockerfile performs the following actions:

* **Base Image:** Uses a Python image based on Alpine Linux, tagged as version 3.12.0b3‑alpine3.18.
* **Copying Code:** Transfers your application source code into the container.
* **Setting the Working Directory:** Switches context to `/application` for subsequent commands.
* **Installing Dependencies:** Copies `requirements.txt` and installs the necessary Python packages.
* **Exposing Port 5000:** Documents the port on which the container will listen.
* **Running the Application:** Executes the command to start the Flask application.

<Callout icon="lightbulb">
  The `EXPOSE` instruction is for documentation purposes only and does not publish the port. Use the `-p` flag to map container ports to the host, e.g., `docker run -p 5000:5000 my-flask-app:v1`.
</Callout>

## Selecting the Appropriate Base Image

Since this application utilizes Python, we selected an Alpine-based Python image available on [Docker Hub](https://hub.docker.com) for its reduced size and efficiency. Searching for "python" on Docker Hub provides multiple options, including slim and Alpine variants.

<Frame>
  ![The image shows the Docker Hub website, featuring a search bar and sections for trusted content, spotlight articles, and categories related to development and machine learning.](https://kodekloud.com/kk-media/image/upload/v1752879857/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Building-a-Custom-Docker-Image/docker-hub-website-search-development.jpg)
</Frame>

<Frame>
  ![The image shows a search results page on Docker Hub for "python," displaying various Python-related container images with options to filter by products, trusted content, and categories.](https://kodekloud.com/kk-media/image/upload/v1752879858/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Building-a-Custom-Docker-Image/docker-hub-python-search-results.jpg)
</Frame>

## Copying Application Files

The Dockerfile uses the `COPY` command to add your application files and dependency file into the image. Here’s an illustrative snippet:

```dockerfile theme={null}
FROM python:3.12.0b3-alpine3.18
COPY /application 
COPY hello.txt /absolute/path
COPY hello.txt relative/to/workdir
```

This demonstrates the flexibility of the `COPY` command, allowing files to be added either to an absolute path or relative to the current working directory. Following these commands, the Dockerfile sets up the working directory, installs dependencies, exposes the application port, and defines the startup command.

## Building the Docker Image

With your Dockerfile ready, build the image by running the following command from the directory containing your Dockerfile. The `-t` flag tags the image:

```bash theme={null}
docker build -t my-flask-app:v1 .
```

This command processes each instruction in the Dockerfile and generates a Docker image tagged `my-flask-app:v1`.

## Running the Container

After building the image, you can verify it by listing all Docker images:

```bash theme={null}
docker image ls
```

To run the container, use the following command:

```bash theme={null}
docker run my-flask-app:v1
```

The terminal output should confirm that your Flask application is running on port 5000. Press Ctrl+C to stop the container.

## Pushing the Image to Docker Hub

After creating your Docker image, the next step is to push it to a repository like [Docker Hub](https://hub.docker.com) for easy deployment and team access.

### Logging in and Creating a Repository

First, log into [Docker Hub](https://hub.docker.com) using:

```bash theme={null}
docker login
```

After entering your credentials, create a new repository on Docker Hub (for example, "jenkins-flask-app").

### Retagging and Pushing the Image

Docker Hub requires images to be tagged with the format: username/repository:tag. Retag your image using your Docker Hub username:

```bash theme={null}
docker image tag my-flask-app:v1 sanjeevkt720/jenkins-flask-app:v1
```

Verify the new tag by listing your images:

```bash theme={null}
docker image ls
```

Now, push the image to Docker Hub:

```bash theme={null}
docker push sanjeevkt720/jenkins-flask-app:v1
```

The terminal should display confirmation messages indicating that the image layers and digest have been successfully pushed.

## Updating the Application and Creating New Versions

As your application evolves, update the code and, if necessary, adjust the Dockerfile instructions. Build a new version of the image with an updated tag. For example, after updating the application, rebuild the image as version three:

**Dockerfile remains unchanged:**

```dockerfile theme={null}
FROM python:3.12.0b3-alpine3.18
COPY /application
WORKDIR /application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

Rebuild the image:

```bash theme={null}
docker build -t sanjeevkt720/jenkins-flask-app:v3 .
```

Confirm the new image tag:

```bash theme={null}
docker image ls
```

Push the updated image to Docker Hub:

```bash theme={null}
docker push sanjeevkt720/jenkins-flask-app:v3
```

A successful push will indicate that the new image version is available in your Docker Hub repository.

## Additional Considerations

* **Port Mapping:** To publish a container port on the host, use the `-p` flag with `docker run` (e.g., `docker run -p 5000:5000 sanjeevkt720/jenkins-flask-app:v1`).
* **Alternative Registries:** While [Docker Hub](https://hub.docker.com) is widely used, repositories on AWS, Azure, and GCP also support similar tagging and push commands.

By following these steps, you've successfully containerized your Flask application, built custom Docker images, and deployed them to Docker Hub for streamlined delivery and collaboration.

## Resources

| Resource Type | Use Case                                     | Example Command                                 |
| ------------- | -------------------------------------------- | ----------------------------------------------- |
| Docker Build  | Building a Docker image from your Dockerfile | `docker build -t my-flask-app:v1 .`             |
| Docker Run    | Running a container from the image           | `docker run -p 5000:5000 my-flask-app:v1`       |
| Docker Push   | Pushing your image to a repository           | `docker push sanjeevkt720/jenkins-flask-app:v1` |

For more detailed documentation, visit these links:

* [Docker Documentation](https://docs.docker.com/)
* [Deploying Flask Apps with Docker](https://www.docker.com/blog/containerizing-a-flask-application/)

Happy containerizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/9eb65ce1-0aef-4f00-b661-5f8308aef2bd/lesson/f88eb052-fff3-4a78-83b3-3530030f8d7b" />
</CardGroup>


# Configuring Jenkins Pipeline with Docker

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Docker/Configuring-Jenkins-Pipeline-with-Docker/page

This article explains how to set up a CI/CD pipeline in Jenkins using Docker for building and deploying applications.

In this lesson, we will walk through setting up a CI/CD pipeline in Jenkins that leverages Docker for building and deploying applications. The pipeline automates tasks such as checking out code, running tests, building Docker images, and pushing those images to Docker Hub. This guide will help you understand each step of the process, ensuring your builds are traceable and consistent.

## Pipeline Workflow

The CI/CD pipeline is structured with the following stages:

1. **Check out the source code.**
2. **Run tests and verify code quality.**
3. **Build a Docker image.**
4. **Push the Docker image to Docker Hub.**

Before pushing an image, ensure that Jenkins has the appropriate Docker credentials for authentication. Also, verify that Docker is installed on the Jenkins machine so that it can execute Docker CLI commands.

<Frame>
  ![The image shows a pipeline configuration flowchart with four stages: "Checkout Code," "Test," "Build Docker Image," and "Push Image to DockerHub."](https://kodekloud.com/kk-media/image/upload/v1752879859/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Configuring-Jenkins-Pipeline-with-Docker/pipeline-configuration-flowchart-docker.jpg)
</Frame>

## Setting Up Docker Hub

To begin, create a Docker Hub repository. For example, you might name it "jenkins-flask-app" under your Docker Hub username. The repository path should adhere to the following format:\
\<username>/jenkins-flask-app

<Frame>
  ![The image is a guide to creating a DockerHub repository, showing a Docker Hub icon and a sample repository path format: \\\<username>/jenkins-flask-app.](https://kodekloud.com/kk-media/image/upload/v1752879860/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Configuring-Jenkins-Pipeline-with-Docker/dockerhub-repository-guide.jpg)
</Frame>

When building the Docker image, you should use the format `\<username>/<repo-name>` along with a tag. In our example, we append the Git SHA (provided as an environment variable in Jenkins) to the image tag, ensuring each image can be correlated with a specific Git commit for easier troubleshooting.

<Callout icon="lightbulb">
  Remember to add Jenkins credentials for Docker access (username and password) so Jenkins can authenticate and push images to Docker Hub securely.
</Callout>

<Frame>
  ![The image shows a diagram for configuring DockerHub credentials, featuring a character holding a coffee cup above a box labeled with "Username" and "Password."](https://kodekloud.com/kk-media/image/upload/v1752879861/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Configuring-Jenkins-Pipeline-with-Docker/dockerhub-credentials-diagram.jpg)
</Frame>

## Jenkins Pipeline Configuration

Below is an example of a Jenkins pipeline configuration that integrates Docker build and push steps:

```groovy theme={null}
pipeline {
    agent any
    environment {
        // Define the base image name and tag using the Git commit SHA for unique identification
        IMAGE_NAME = 'sanjeevkt720/jenkins-flask-app'
        IMAGE_TAG = "${IMAGE_NAME}:${env.GIT_COMMIT}"
    }
    stages {
        // Setup stage: Install necessary dependencies
        stage('Setup') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        // Test stage: Run tests using Pytest
        stage('Test') {
            steps {
                sh "pytest"
            }
        }
        // Docker Hub Login stage: Authenticate Jenkins with Docker Hub using secure credentials
        stage('Login to docker hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin'
                    echo 'Logged in successfully'
                }
            }
        }
        // Build Docker Image stage: Build the Docker image with the defined tag and verify its creation
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_TAG} .'
                echo "Docker image built successfully"
                sh 'docker image ls'
            }
        }
        // Push Docker Image stage: Push the Docker image to Docker Hub
        stage('Push Docker Image') {
            steps {
                sh 'docker push ${IMAGE_TAG}'
                echo "Docker image pushed successfully"
            }
        }
    }
}
```

### Key Pipeline Components

* **Environment Configuration:**\
  The pipeline sets the `IMAGE_NAME` and `IMAGE_TAG` using the Git commit SHA. This ensures that each Docker image can be traced back to its corresponding commit.

* **Setup Stage:**\
  Installs necessary dependencies as defined in your `requirements.txt`.

* **Test Stage:**\
  Executes tests using Pytest to verify code quality before proceeding with the build.

* **Docker Authentication:**\
  Uses a secure method to log in to Docker Hub. The credentials stored in Jenkins are injected and passed to the Docker CLI, ensuring they are not exposed in logs or command history.

* **Build and Push Stages:**\
  The Docker image is built using the specified tag and subsequently pushed to Docker Hub, making it ready for deployment.

## Summary

This automated pipeline integrates manual Docker build and push steps into your CI/CD process in Jenkins. By associating every build with a specific Git commit, this configuration enhances traceability and simplifies troubleshooting.

For more information on setting up CI/CD with Jenkins and Docker, check out [Jenkins Documentation](https://www.jenkins.io/doc/) and [Docker Documentation](https://docs.docker.com/).

This concludes the configuration for integrating Jenkins with Docker in your CI/CD workflow.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/9eb65ce1-0aef-4f00-b661-5f8308aef2bd/lesson/80fefaac-fdb4-47b5-88a9-7c744b806d10" />
</CardGroup>
