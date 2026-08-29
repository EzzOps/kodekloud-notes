# Demo Configuring Jenkins Pipeline with Docker

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Docker/Demo-Configuring-Jenkins-Pipeline-with-Docker/page

Learn to configure a Jenkins pipeline with Docker for continuous integration and deployment of applications.

In this lesson, you'll learn how to configure a Jenkins pipeline integrated with Docker, enabling continuous integration and deployment for your applications. Before you start, ensure Docker is installed on your Jenkins server so that it can access the Docker CLI. For installation instructions, please refer to the [Docker documentation page](https://docs.docker.com/get-docker/).

> **lightbulb** Make sure Docker is installed and properly configured on your Jenkins server before proceeding.

## Setting Up Jenkins Credentials

The first step is to configure Jenkins with your Docker Hub credentials. Create credentials within Jenkins using the "Username with password" type. Enter your Docker Hub account name as the username and your Docker Hub password as the password. In this example, the credentials are named "Docker creds".

![The image shows a Jenkins interface where new credentials are being added, including fields for username, password, and ID. The username is filled in as "sanjeevkr720" and the ID as "docker".](https://kodekloud.com/kk-media/image/upload/v1752879862/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Jenkins-Pipeline-with-Docker/jenkins-add-credentials-sanjeevkr720.jpg)

## Creating a New Pipeline

Next, navigate back to the Jenkins dashboard and create a new pipeline named "Docker pipeline". In the pipeline configuration screen, make the following selections:

* Enable "GitHub hook trigger for GITScm polling".
* Choose "Pipeline script from SCM".
* Select Git as your SCM and provide the URL of your repository.
* Set the branch to "main" and keep the default path to your Jenkinsfile.

![The image shows a configuration screen for setting up a Docker pipeline, with options to define a pipeline script from SCM using Git, and a prompt to enter a Git repository URL.](https://kodekloud.com/kk-media/image/upload/v1752879864/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Jenkins-Pipeline-with-Docker/docker-pipeline-configuration-screen.jpg)

## The Jenkinsfile Pipeline Script

Your repository must contain a Jenkinsfile that defines the pipeline stages. In this example, the pipeline executes the following tasks:

* Installs dependencies using pip.
* Runs tests with pytest.
* Logs into Docker Hub using the credentials configured earlier.
* Builds a Docker image.
* Pushes the Docker image to Docker Hub.

Below is an improved and consolidated version of the Jenkinsfile:

```groovy theme={null}
pipeline {
    agent any
    environment {
        IMAGE_TAG = "sanjeevkt720/jenkins-flask-app:${GIT_COMMIT}"
    }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', 
                                                  usernameVariable: 'USERNAME', 
                                                  passwordVariable: 'PASSWORD')]) {
                    sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
                    echo 'Logged in successfully'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_TAG .'
                echo 'Docker image built successfully'
                sh 'docker image ls'
            }
        }
        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_TAG'
            }
        }
    }
}
```

Once you commit this Jenkinsfile to your repository and push your changes, Jenkins will automatically trigger the pipeline. The pipeline will:

* Check out your code.
* Install required packages.
* Run unit tests using pytest.
* Log into Docker Hub.
* Build a Docker image.
* Push the newly built image to your Docker Hub repository.

## Build Output Examples

During the build process, you may see console outputs such as the following when installing dependencies:

```bash theme={null}
pip install -r requirements.txt
Defaulting to user installation because normal site-packages is not writable
Requirement already satisfied: blinker==1.7.0 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 1)) (1.7.0)
Requirement already satisfied: cachetools==5.2.1 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 2)) (5.2.1)
Requirement already satisfied: certifi==2023.11.17 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 3)) (2023.11.17)
Requirement already satisfied: charset-normalizer==3.3.2 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 4)) (3.3.2)
Requirement already satisfied: click==8.1.7 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 5)) (8.1.7)
Requirement already satisfied: colorama==0.4.6 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 6)) (0.4.6)
Requirement already satisfied: Flask==2.3.3 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 7)) (2.3.3)
Requirement already satisfied: itsdangerous==2.1.2 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 8)) (2.1.2)
Requirement already satisfied: Jinja2==3.1.5 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 9)) (3.1.5)
Requirement already satisfied: MarkupSafe==2.1.3 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 10)) (2.1.3)
Requirement already satisfied: numpy==1.24.4 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 11)) (1.24.4)
Requirement already satisfied: requests==2.28.1 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 12)) (2.28.1)
Requirement already satisfied: Werkzeug==2.3.4 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 13)) (2.3.4)
Requirement already satisfied: urllib3==1.26.15 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 14)) (1.26.15)
Requirement already satisfied: zipp==3.15.0 in /var/lib/jenkins/.local/lib/python3.9/site-packages (from -r requirements.txt (line 15)) (3.15.0)
```

When building the Docker image, you may see output similar to the following:

```bash theme={null}
+ docker build -t sanjaevtkt720/jenkins-flask-app:9e287c436a97b9b2e16822545590dcdc2f0130 .
