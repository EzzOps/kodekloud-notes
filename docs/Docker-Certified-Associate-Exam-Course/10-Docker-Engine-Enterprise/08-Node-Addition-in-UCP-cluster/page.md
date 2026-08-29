# Pulling from Docker Hub
docker pull ubuntu

# Pushing to Docker Hub (requires permissions)
docker push ubuntu

# Pulling from a Google Container Registry (GCR) namespace
docker pull gcr.io/your-org/ubuntu
```

## Introducing Docker Trusted Registry

Docker Trusted Registry (DTR) is Docker’s on-premises, enterprise-grade image repository. It delivers:

* **Security Scanning**\
  Automated vulnerability checks integrated into your CI/CD pipelines.
* **Image Signing**\
  Enforce image provenance with [Docker Content Trust].
* **Role-Based Access Control (RBAC)**\
  Granular permissions to govern who can view, push, or pull each repository.

![The image shows a Docker Trusted Registry (DTR) interface with a message indicating there are no repositories and a prompt to create a new one.](https://kodekloud.com/kk-media/image/upload/v1752873879/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Trusted-Registry-Setup/docker-trusted-registry-no-repositories.jpg)

## Deploying DTR on a UCP Cluster

DTR runs as a service on a UCP worker node. Follow these steps to install DTR:

### Prerequisites

| Requirement        | Details                                     |
| ------------------ | ------------------------------------------- |
| Worker Node        | New node dedicated to DTR                   |
| Docker Engine – EE | Enterprise Edition installed                |
| UCP Cluster        | UCP 3.x or later, accessible over TLS/HTTPS |

### Installation Steps

1. **Provision a Worker Node**\
   Spin up a new server (VM or bare metal) and install Docker Engine – Enterprise.

2. **Join the UCP Cluster**\
   On the new node, run:
   ```bash theme={null}
   docker swarm join --token <SWARM_TOKEN> <MANAGER_IP>:2377
   ```
   UCP’s agent (`ucp-agent`) will install automatically.

3. **Retrieve the DTR Install Command**\
   In the UCP Web UI, navigate to **Settings > DTR**, and copy the provided `docker run docker/dtr install ...` command.

4. **Execute the Installer**\
   Run the command on your worker node:
   ```bash theme={null}
   docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
     docker/dtr install \
     --ucp-node-address <NODE_IP> \
     --ucp-insecure-tls \
     --dtr-external-url https://dtr.example.com
   ```

> **triangle-alert** For production environments, deploy **at least three** DTR replicas to ensure high availability.

### High Availability and Raft Consensus

DTR leverages the Raft algorithm to synchronize metadata and configuration across replicas—much like Docker Swarm ensures consistent cluster state.

### Overlay Network: `dtr-ol`

Upon installation, UCP creates an overlay network called `dtr-ol`. This network allows DTR replicas to communicate securely and replicate data.

### External Storage for Images

By default, images are stored on each node’s local filesystem, which can risk data loss in multi-instance setups. Instead, configure an external store:

| Storage Type | Description               | URI Example           |
| ------------ | ------------------------- | --------------------- |
| NFS          | Network File System share | `nfs://server/export` |
| Amazon S3    | AWS object storage        | `s3://my-dtr-bucket`  |
| Google GCS   | Google Cloud Storage      | `gs://my-dtr-bucket`  |

> **lightbulb** Ensure the DTR service account has read/write permissions to the external storage.

## DTR Console After Installation

Once installation completes, open your browser at `https://dtr.example.com`. You’ll see an interface similar to below—ready for you to create and manage repositories.

![The image illustrates a Docker Swarm setup with a manager node and two worker nodes, showing components like ucp-agent, ucp-controller, and dtr-ol, along with a connection to S3 storage.](https://kodekloud.com/kk-media/image/upload/v1752873880/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Trusted-Registry-Setup/docker-swarm-setup-manager-worker.jpg)

***

In the next section, we’ll walk through creating repositories, configuring webhooks, and integrating DTR with your CI/CD pipelines.

[Kubernetes Documentation]: https://kubernetes.io/docs/

[Docker Content Trust]: https://docs.docker.com/engine/security/trust/

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/a6a39359-7fb1-4fab-b0c2-6fc58a6ce617/lesson/be90b268-dc2c-4b30-bd07-9960d9a88689)


# Node Addition in UCP cluster

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Enterprise/Node-Addition-in-UCP-cluster/page

This guide explains how to add worker nodes to a Docker UCP cluster for scaling applications and distributing workloads.

Adding worker nodes to your Docker Universal Control Plane (UCP) cluster allows you to scale applications and distribute workloads. In this guide, you’ll learn how to provision a new host, install Docker Engine, join the Swarm cluster, and verify the node in the UCP console.

## Prerequisites

* A running UCP cluster with at least one manager node
* A new host with a supported Linux distribution (e.g., Ubuntu, CentOS)
* SSH access and root or sudo privileges on the new host
* Network connectivity on ports 2376 (Docker daemon) and 2377 (Swarm)

> **lightbulb** Ensure the Docker Engine version on your new worker matches the UCP manager’s version to prevent compatibility issues.

## 1. Provisioning and Installing Docker Engine

On the new worker node, install Docker Engine using Docker’s official convenience script:

```bash theme={null}
