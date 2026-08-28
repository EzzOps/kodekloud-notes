# Define build and modify container images

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/Define-build-and-modify-container-images/page

This guide teaches how to create and modify Docker images for containerizing applications, focusing on a Python Flask web app.

Welcome to this comprehensive guide on Docker images. In this tutorial, you’ll learn how to create your own Docker image by containerizing a simple web application built with the Python Flask framework. Containerizing an application is essential for creating customized components that may not be available on Docker Hub, as well as streamlining deployment processes.

<Callout icon="lightbulb">
  Before containerizing, consider the manual deployment steps: starting with a base operating system (like Ubuntu), updating package repositories using APT, installing required system and Python packages, copying the source code to a designated directory (e.g., `/opt`), and finally running the web server with Flask.
</Callout>

<Frame>
  ![The image provides steps to create an image using Ubuntu, including updating repositories, installing dependencies, copying source code, and running a web server with Flask.](https://kodekloud.com/kk-media/image/upload/v1752871130/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Define-build-and-modify-container-images/frame_80.jpg)
</Frame>

With these steps in mind, you can automate the process using a Dockerfile. Below is an example Dockerfile for our Flask application:

```dockerfile theme={null}
FROM ubuntu

RUN apt-get update && apt-get -y install python python-setuptools python-dev
RUN pip install flask flask-mysql

COPY . /opt/source-code

ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run --host=0.0.0.0
```

## Dockerfile Breakdown

* **FROM**: Sets the base image as Ubuntu. Every Docker image starts with a base layer from either an operating system or a prebuilt image available on Docker Hub.
* **RUN**: Executes commands during image build. The first `RUN` updates the system and installs Python, while the second installs Flask and MySQL support via `pip`.
* **COPY**: Transfers your application's source code from your local repository to the container directory `/opt/source-code`.
* **ENTRYPOINT**: Specifies the command to execute when the container launches, setting the `FLASK_APP` environment variable and starting the Flask server.

Docker processes these instructions sequentially, creating layers that represent the changes made with each step. If you update any instruction, Docker reuses the cached layers for all preceding steps, speeding up the build process significantly.

## Viewing Docker Image Layers

To inspect the image layers and their sizes, run the following command:

```bash theme={null}
docker history <your-image-name>
```

## Building the Docker Image

After finalizing your Dockerfile, build your image with the following command:

```bash theme={null}
docker build -f Dockerfile -t mmumshad/my-custom-app .
```

During the build, Docker outputs details for each step. Here’s an example of what the build output might include:

```bash theme={null}
root@osboxes:/root/simple-webapp-docker # docker build .
Sending build context to Docker daemon  3.072kB
Step 1/5 : FROM ubuntu
 ---> ccc7a11d65b1
Step 2/5 : RUN apt-get update && apt-get install -y python python-setuptools python-dev
 ---> Running in a7840bfad17
Get:1 http://archive.ubuntu.com/ubuntu xenial InRelease [247 kB]
Get:2 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Get:3 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Get:4 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [46.3 kB]
Get:5 http://archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]
Get:6 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [440 kB]
Step 3/5 : RUN pip install flask flask-mysql
 ---> Running in a4a6c9190ba3
Collecting flask
Downloading Flask-0.12.2-py2.py3-none-any.whl (83kB)
Collecting flask-mysql
Downloading Flask-MySQL-1.4.0-py2.py3-none-any.whl
Removing intermediate container a4a6c9190ba3
Step 4/5 : COPY app.py /opt/
 ---> 7cda1b1782
Removing intermediate container faaa63c512
Step 5/5 : ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0
 ---> Running in d452c574a8b8
 ---> 9f27c36920bc
Removing intermediate container d452c574a8b8
Successfully built 9f27c36920bc
```

<Callout icon="lightbulb">
  If a build step fails, Docker caches the successful layers up to the failure point. After correcting the error, re-running the build command leverages the cached layers, drastically reducing rebuild times.
</Callout>

## Containerizing a Diverse Range of Applications

Docker is not limited to web applications. You can containerize databases, development tools, web browsers, and utilities like curl, Spotify, or Skype. The versatility of containerization is reshaping how applications are deployed and managed.

<Frame>
  ![The image suggests containerizing applications like Chrome, Firefox, cURL, and Spotify, with the message "Containerize Everything!!!" against a Docker-themed background.](https://kodekloud.com/kk-media/image/upload/v1752871131/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Define-build-and-modify-container-images/frame_430.jpg)
</Frame>

In the future, instead of installing software directly onto your operating system, you'll run it in a containerized environment. This approach ensures that applications can be removed cleanly without leaving residual files or configurations on your system.

Happy containerizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/18668587-1e59-4be8-9ee2-38ce580e3a8a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/440f105b-69c1-4d65-aa55-870702ef53fb" />
</CardGroup>
