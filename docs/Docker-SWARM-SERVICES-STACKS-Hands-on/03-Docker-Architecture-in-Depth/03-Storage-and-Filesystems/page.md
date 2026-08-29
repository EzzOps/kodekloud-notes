# Storage and Filesystems

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Docker-Architecture-in-Depth/Storage-and-Filesystems/page

This article explores Dockers storage architecture, file systems, layered image architecture, and storage drivers for managing data on the host.

Hello and welcome to this technical deep-dive into Docker's storage architecture and file systems. My name is Mumshad Mannambeth, and in this lesson we will explore how Docker manages data on the host and the intricacies of container file systems. We will investigate the folder structure created by Docker, the layered image architecture, the copy-on-write mechanism, and various storage drivers.

When Docker is installed, it sets up a folder structure at `/var/lib/docker` that contains several subdirectories such as `aufs`, `containers`, `images`, and `volumes`. These directories are critical because they store all Docker-related data, including files for images, running containers, and persistent volumes. For example, files related to containers reside in the `containers` folder, while image files are stored in the `images` folder.

![A person stands beside a diagram illustrating a file system structure, including directories like "aufs," "containers," "image," and "volumes," on a blue background.](https://kodekloud.com/kk-media/image/upload/v1752874056/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Storage-and-Filesystems/frame_60.jpg)

## Docker Image Layered Architecture

Docker images use a layered architecture. Every instruction in a Dockerfile results in the creation of a new layer that only contains the changes from the previous one. Consider the following example Dockerfile:

```dockerfile theme={null}
FROM Ubuntu

RUN apt-get update && apt-get -y install python
RUN pip install flask flask-mysql
COPY . /opt/source-code
ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run
```

Build this image with the command:

```bash theme={null}
docker build -t mmumshad/my-custom-app .
```

In this build:

1. The base Ubuntu image (\~120 MB) is established.
2. A subsequent layer installs APT packages (around 300 MB).
3. Additional layers add Python dependencies.
4. The application source code is injected.
5. Lastly, the entry point is configured.

Because Docker caches these layers, a similar Dockerfile—even if only differing in the source code and entry point—can reuse the cached layers for the base image, package installations, and dependencies. For instance, another Dockerfile might look like:

```dockerfile theme={null}
FROM Ubuntu

RUN apt-get update && apt-get -y install python
RUN pip install flask flask-mysql
COPY app2.py /opt/source-code
ENTRYPOINT FLASK_APP=/opt/source-code/app2.py flask run
```

Build this second image using:

```bash theme={null}
docker build -t mmumshad/my-custom-app-2 .
```

Docker reuses the first three layers and only builds the layers that include the new source code and entry point. This efficient caching mechanism accelerates builds and conserves disk space.

The layered structure from bottom up is as follows:

1. Base Ubuntu image
2. Installed packages
3. Python dependencies
4. Application source code
5. Entry point configuration

![The image shows a person explaining a layered architecture with five layers, including Ubuntu base, package changes, source code, and entry point updates.](https://kodekloud.com/kk-media/image/upload/v1752874057/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Storage-and-Filesystems/frame_270.jpg)

Once the build is complete, the image layers are read-only. When you run a container using the `docker run` command, Docker mounts a new writable layer on top of these image layers. This writable layer manages any changes made during runtime—such as log files, temporary files, or user modifications. For instance, if you log into a container and create a file (like `temp.txt`), that file is stored in the writable layer:

```bash theme={null}
docker run -it mmumshad/my-custom-app bash
