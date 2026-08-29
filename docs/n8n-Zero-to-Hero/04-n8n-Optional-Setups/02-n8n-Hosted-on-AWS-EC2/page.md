# n8n Hosted on AWS EC2

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Optional-Setups/n8n-Hosted-on-AWS-EC2/page

Guide to deploy n8n on an AWS EC2 Ubuntu instance using Docker and Docker Compose v2 for demos, including setup, environment configuration, and accessing the UI

This guide shows how to deploy n8n on an AWS EC2 instance using Docker and Docker Compose v2. Follow the steps to:

* Launch an EC2 instance (Ubuntu).
* Install Docker and Docker Compose v2 (CLI plugin).
* Clone the n8n self-hosted AI starter kit.
* Configure environment variables and run the stack.
* Access n8n via the instance public IP.

Recommended for quick demos and testing. For a production deployment, see the "Closing notes" section below.

Start by launching an AWS sandbox playground (or use your own AWS account). For a quick demo, KodeKloud provides interactive cloud sandboxes.

<Frame>
  <img alt="The image shows a webpage from KodeKloud titled &#x22;Cloud Playgrounds,&#x22; featuring interactive options for AWS, Azure, Google Cloud, and Azure Data services." />
</Frame>

Sign into the AWS Console using the credentials provided by the playground. Copy and paste the username/password into the AWS sign-in page to access the console.

<Frame>
  <img alt="The image shows an AWS Console Home screen with no recently visited services, an &#x22;Access denied&#x22; alert for listing applications, and an option to diagnose with Amazon Q. The region is set to US East (N. Virginia)." />
</Frame>

## 1 — Launch an EC2 instance

1. Console: EC2 → Instances → Launch Instance.
2. Name the instance `n8n-demo` and select an Ubuntu AMI (e.g., Ubuntu 22.04 LTS).
3. Choose an instance type (e.g., `t2.medium`). This demo uses a slightly larger instance to accommodate Ollama and extra repo data.
4. Increase the root volume to 30 GB (or larger as needed).
5. Create a new key pair `n8n-demo-key` in PEM format and download it.
6. Configure the security group to allow:
   * SSH (port 22) — for administration.
   * n8n (port 5678) — to access the UI.
   * Additional ports used by included services (Ollama, Qdrant) if needed.

When configuring the instance, confirm SSH and any other required ports are allowed.

<Frame>
  <img alt="The image shows an AWS EC2 instance launch configuration screen, detailing network settings, key pair setup, security groups, and a summary of the selected instance details. Options for creating or selecting a security group and allowing SSH and HTTP traffic are visible." />
</Frame>

Increase the storage size to ensure enough room for components like Ollama.

<Frame>
  <img alt="The image shows an AWS EC2 dashboard with options to configure and launch an instance, including security group and storage settings." />
</Frame>

Launch the instance. After it starts, open the instance details to confirm and review the security group inbound rules.

<Frame>
  <img alt="The image shows an AWS EC2 Management Console with one instance running, labeled &#x22;n8n-demo,&#x22; providing details such as instance ID, type, state, and IP addresses." />
</Frame>

Edit the security group's inbound rules to allow SSH and the n8n port (5678). In the demo we configured Custom TCP on port 5678 and allowed it from anywhere.

<Frame>
  <img alt="The image shows the AWS EC2 console's &#x22;Edit inbound rules&#x22; page, where a user is configuring security group rules for inbound traffic. Options for protocol types like TCP and UDP are being selected from a dropdown menu." />
</Frame>

Save the rules after editing.

<Frame>
  <img alt="The image shows an AWS console screen where inbound rules for a security group are being edited, allowing SSH and custom TCP traffic from any IP address. There is a warning about allowing access from all IP addresses." />
</Frame>

> **warning** For production, do not leave SSH (22) or n8n (5678) open to the entire internet (`0.0.0.0/0`). Restrict access by IP range, use a VPN or bastion host, and implement least-privilege security. The open rules shown here are only acceptable for a short-lived demo sandbox.

## 2 — SSH into the instance

On your local machine, move to the folder where the PEM key was downloaded and secure the file:

```bash theme={null}
chmod 400 n8n-demo-key.pem
```

SSH into the instance using the `ubuntu` user and the instance public IP (replace `<PUBLIC_IP>`):

```bash theme={null}
ssh -i "n8n-demo-key.pem" ubuntu@<PUBLIC_IP>
```

On first connect you may see a host authenticity prompt; type `yes` to continue. Example:

```text theme={null}
The authenticity of host '<PUBLIC_IP> (<PUBLIC_IP>)' can't be established.
ED25519 key fingerprint is SHA256:oc3mo7aChuiTyieEkiDuCvPTLBliSDNLMrXc9W0c.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

## 3 — Install Docker and Docker Compose v2

Update packages and install Docker using the official convenience script:

```bash theme={null}
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Enable Docker, add the current user to the docker group, and apply the group change:

```bash theme={null}
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

Install Docker Compose v2 as a CLI plugin (adjust the version URL if you prefer another release):

```bash theme={null}
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

Verify the Compose plugin (note: use `docker compose`, not `docker-compose`):

```bash theme={null}
docker compose version
