# Storage in Docker

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Storage/Storage-in-Docker/page

This guide explores advanced Docker storage concepts, including storage drivers, data management, and layered architecture for efficient image and container handling.

Welcome to this guide on advanced Docker storage concepts. In this article, we explore how Docker handles storage drivers, manages data on the host file system, and implements a layered architecture to build images and run containers efficiently.

When Docker is installed, it creates a folder structure at `/var/lib/docker` containing subdirectories such as `overlay2`, `containers`, `images`, and `volumes`. These directories store Docker images, container runtime data, and volumes. For instance, files associated with running containers reside in the `containers` folder, image files are stored under `images`, and any created volumes are kept in the `volumes` folder.

## Docker Image Layers

Docker images are built using a layered architecture. Each instruction in a Dockerfile generates a new layer, containing only the modifications from the previous layer. Consider this Dockerfile for our first application:

```dockerfile theme={null}
