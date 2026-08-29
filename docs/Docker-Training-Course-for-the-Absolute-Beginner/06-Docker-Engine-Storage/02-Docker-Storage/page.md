# Docker Storage

Source: https://notes.kodekloud.com/docs/Docker-Training-Course-for-the-Absolute-Beginner/Docker-Engine-Storage/Docker-Storage/page

This article explores Docker storage drivers and file systems, detailing data management and persistent storage in Docker environments.

Welcome to this lesson on advanced Docker concepts. In this article, we dive into Docker storage drivers and file systems, exploring how Docker manages data storage and container file systems. Learn where Docker stores its files, how it structures data, and how to handle persistent data effectively.

## Docker's File Storage Architecture

When Docker is installed, it establishes a directory structure typically at `/var/lib/docker`. This root directory contains several subdirectories that serve different purposes:

* **containers**: Stores files related to running containers.
* **images**: Contains image-related files.
* **volumes**: Holds data for Docker volumes.
* **overlay2**: Manages the overlay filesystem for layering.

> **lightbulb** Each of these directories plays a crucial role in container management. Understanding their function can help troubleshoot and optimize your Docker environment.

## Docker's Layered Architecture

Docker images are constructed using a layered approach. Each instruction in a Dockerfile creates a distinct layer that only contains changes from the previous layer. For example, consider the following Dockerfile:

```dockerfile theme={null}
FROM ubuntu

RUN apt-get update && apt-get -y install python
RUN pip install flask flask-mysql
COPY . /opt/source-code
ENTRYPOINT ["flask", "run"]
```

Build the image using:

```bash theme={null}
docker build -t mummshad/my-custom-app .
```

In this Dockerfile:

* **Base Image**: The first layer pulls the Ubuntu base image.
* **APT Packages**: The second layer installs necessary APT packages.
* **Python Packages**: The third layer installs Python packages required by the application.
* **Source Code**: The fourth layer copies your application code into the container.
* **Entrypoint**: The final layer sets the container's entry point.

Because each layer contains only the incremental changes, their sizes reflect only the modifications from the previous layer. For instance, even if the base Ubuntu image is large, layers that add extra packages or code remain relatively small.

### Reusing Layers Across Images

Docker optimizes builds by reusing layers that remain unchanged between images. Consider a scenario with two nearly identical applications:

```dockerfile theme={null}
