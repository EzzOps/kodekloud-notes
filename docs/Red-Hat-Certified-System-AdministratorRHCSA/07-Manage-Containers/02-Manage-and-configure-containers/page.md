# Manage and configure containers

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Containers/Manage-and-configure-containers/page

This guide covers managing and configuring containers using Docker and Podman, including installation, image handling, and container operations.

Welcome to this comprehensive guide on container management and configuration. In this article, we explore how containers simplify application deployment and migration by encapsulating everything—daemons, configuration files, logs, and databases—in a single, portable unit. Unlike traditional setups (e.g., a conventional MariaDB installation where components are scattered in various directories), containerized applications streamline the process of moving applications between different systems.

***

## Installing Podman to Emulate Docker

In some environments, such as CentOS Stream 8, Docker might not have official support. In these cases, you can install Podman, which offers a Docker-compatible command-line interface. To install Podman using the dnf package manager, execute the following command:

```bash theme={null}
sudo dnf install podman
```

After installation, Podman allows you to use familiar Docker commands as it seamlessly translates them under the hood. The installation output might resemble the following:

```bash theme={null}
