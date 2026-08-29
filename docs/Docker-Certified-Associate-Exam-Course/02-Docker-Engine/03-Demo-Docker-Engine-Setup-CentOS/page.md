# Demo Docker Engine Setup CentOS

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Demo-Docker-Engine-Setup-CentOS/page

Learn to install and configure Docker Engine on a CentOS 7 server, including removing old packages and verifying the installation.

Learn how to quickly install and configure Docker Engine (Community Edition) on a CentOS 7 server. This guide covers uninstalling old packages, setting up the official Docker repository, installing Docker CE, and verifying your installation.

> **lightbulb** Always refer to the [official Docker documentation](https://docs.docker.com/get-docker/) for the most up-to-date installation instructions.

## Prerequisites

| Requirement        | Details                                |
| ------------------ | -------------------------------------- |
| Operating System   | CentOS 7 (x86\_64)                     |
| User Account       | A non-root user with `sudo` privileges |
| Enabled Repository | `CentOS Extras`                        |
| Server Access      | SSH access to your instance or VM      |

Log in to your server:

```bash theme={null}
ssh centos@docker-centos
```

## 1. Remove Older Docker Versions

Before installing Docker CE, remove any legacy packages to prevent conflicts:

```bash theme={null}
sudo yum remove -y docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-logrotate \
                  docker-engine
```

Verify your enabled repos:

```bash theme={null}
sudo yum repolist
```

You should see `base`, `extras`, and `updates` in the list.

> **triangle-alert** Removing old Docker packages will not delete your images or containers stored under `/var/lib/docker`, but it’s a good idea to back up any critical data before proceeding.

## 2. Install Dependencies & Configure the Docker Repository

1. Install `yum-utils`, which provides the `yum-config-manager` utility:

   ```bash theme={null}
   sudo yum install -y yum-utils
   ```

2. Add the official Docker CE repository:

   ```bash theme={null}
   sudo yum-config-manager \
     --add-repo \
     https://download.docker.com/linux/centos/docker-ce.repo
   ```

3. Confirm the new repo is enabled:

   ```bash theme={null}
   sudo yum repolist | grep docker-ce
   ```

You should see an entry similar to `docker-ce-stable/x86_64`.

## 3. Install Docker Engine (Docker CE)

Install Docker Engine and its core components:

```bash theme={null}
sudo yum install -y docker-ce docker-ce-cli containerd.io
```

Verify that the Docker packages are installed:

```bash theme={null}
sudo rpm -qa | grep -i docker
```

Expected packages in the output:

* `docker-ce`
* `docker-ce-cli`
* `containerd.io`

## 4. Start and Enable the Docker Service

1. Check the Docker service status:

   ```bash theme={null}
   systemctl status docker
   ```

2. If it’s not running, start and enable it to launch on boot:

   ```bash theme={null}
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. Re-check to ensure Docker is active:

   ```bash theme={null}
   systemctl status docker
   ```

## 5. Verify Your Docker Installation

* **Check Docker version:**

  ```bash theme={null}
  sudo docker --version
  ```

  Sample output:

  ```text theme={null}
  Docker version 19.03.13, build 4484c46d9d
  ```

* **View detailed client/server info:**

  ```bash theme={null}
  sudo docker version
  ```

* **Display full system information:**

  ```bash theme={null}
  sudo docker system info
  ```

When you see information about the Engine, containerd, runc, and your host environment, Docker is installed and running correctly.

Congratulations! You have successfully installed and configured Docker Engine on CentOS 7.

## Links and References

* [Docker Get Started Guide](https://docs.docker.com/get-docker/)
* [Docker Engine Overview](https://docs.docker.com/engine/)
* [CentOS Linux Documentation](https://wiki.centos.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/871494af-49f8-42e9-95e9-cb0df80c2b21/lesson/0997ace0-1714-4e32-a74b-231dce511f7d)
