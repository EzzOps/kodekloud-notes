# Install Python and pip
RUN apt-get update && apt-get install -y python python-pip

# Install Flask and MySQL connector
RUN pip install flask flask-mysql

# Copy application source into the image
COPY . /opt/source-code

# Set environment variable and entrypoint
ENV FLASK_APP=/opt/source-code/app.py
ENTRYPOINT ["flask", "run"]
```

## Specifying a Different Build Context

You can point Docker to any local directory containing your `Dockerfile`:

```bash theme={null}
docker build /opt/my-custom-app -t my-custom-app
```

Docker will look for `/opt/my-custom-app/Dockerfile` and include all files under `/opt/my-custom-app` in the context.

## Common Context Sources

| Context Source    | Command Example                                                         | Description                                    |
| ----------------- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| Current directory | `docker build . -t my-custom-app`                                       | Sends `.` as the context                       |
| Local path        | `docker build /opt/my-custom-app -t my-custom-app`                      | Uses a specified folder                        |
| Git repository    | `docker build https://github.com/myaccount/myapp.git#feature-branch`    | Clones a repo (or branch) as the build context |
| Custom Dockerfile | `docker build -f Dockerfile.dev https://github.com/myaccount/myapp.git` | Specifies an alternative `Dockerfile` location |

## Managing Context Size with `.dockerignore`

Sending large or unnecessary files (logs, build artifacts) can slow down builds, especially when the daemon is remote. To prevent this, create a `.dockerignore` file in your context root:

```text theme={null}
tmp
logs
build
```

Docker will exclude these paths when packaging the build context.

> **triangle-alert** Be careful: missing important source files in `.dockerignore` can lead to build failures or incomplete images.

## Remote Docker Daemon Output

When using a remote Docker daemon, you’ll see output similar to:

```bash theme={null}
Sending build context to Docker daemon  2.048kB
Step 1/7 : FROM ubuntu
...
```

This confirms the context has been sent over the network before the build steps execute.

## Building from a Git Repository

Docker can directly use Git URLs as the build context:

```bash theme={null}
# Clone the default branch
docker build https://github.com/myaccount/myapp

# Build a specific branch
docker build https://github.com/myaccount/myapp#feature-branch

# Build only a subfolder within the repo
docker build https://github.com/myaccount/myapp.git#docker
```

By default, Docker looks for `Dockerfile` at the root of the checked‐out code. Use `-f` to point to a different file:

```bash theme={null}
docker build -f Dockerfile.dev https://github.com/myaccount/myapp
```

## Summary

* The **build context** defines what files are sent to the Docker daemon.
* Use `.dockerignore` to exclude unnecessary files and speed up builds.
* You can build from local paths or Git repositories.
* The `-f` flag lets you specify a non-default Dockerfile.

***

## Links and References

* [Docker Build Reference](https://docs.docker.com/engine/reference/commandline/build/)
* [Dockerignore Documentation](https://docs.docker.com/engine/reference/builder/#dockerignore-file)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/93eec43c-d23b-45d8-bd7e-79a015047aec)


# Building a custom image

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Building-a-custom-image/page

Creating a custom Docker image for a Flask application ensures consistent deployments and includes necessary dependencies for your app.

Creating a custom Docker image ensures consistent deployments and lets you include exactly the dependencies your Python Flask app needs. Whether you require specialized system libraries or a private base image, building your own container image is straightforward.

## 1. Planning Your Dockerfile

Before writing any code, outline the manual steps you’d perform to deploy your Flask application:

1. Select a base image (e.g., [Ubuntu](https://ubuntu.com/) or `python:3-slim`).
2. Update and install OS packages (`apt-get update && apt-get install`).
3. Install Python dependencies (`pip install`).
4. Copy application source code into the image.
5. Configure environment variables and expose required ports.
6. Define the container’s startup command.

![The image is a guide on creating a Docker image, listing steps such as using Ubuntu, updating the apt repository, installing dependencies, and running a web server with Flask.](https://kodekloud.com/kk-media/image/upload/v1752873912/notes-assets/images/Docker-Certified-Associate-Exam-Course-Building-a-custom-image/docker-image-creation-guide.jpg)

> **lightbulb** Using an official Python base image (for example, `python:3.9-slim`) can reduce image size and simplify dependency installation.

## 2. Writing the Dockerfile

Create a file named `Dockerfile` at your project root and add the following contents:

```dockerfile theme={null}
