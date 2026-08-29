# Docker EE UCP Client Bundle

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Enterprise/Docker-EE-UCP-Client-Bundle/page

This guide explains how to configure the Universal Control Plane client bundle on your local machine for Docker CLI interaction with a UCP cluster.

In this guide, you'll configure the Universal Control Plane (UCP) client bundle on your local machine to interact with a UCP cluster through the Docker CLI.

## 1. Exploring the UCP Documentation

Start by reviewing the official Docker Engine Enterprise (EE) and UCP docs:

1. Visit the Docker Engine Enterprise documentation.[1]
2. Under **Product Manuals**, select **Docker Enterprise**.
3. Click **Universal Control Plane** → **Access UCP**.
4. Follow the **CLI-Based Access** instructions to obtain the UCP client bundle.

With UCP, you continue using the Docker CLI by downloading a bundle that contains the necessary certificates and environment scripts.

## 2. Downloading the UCP Client Bundle

1. In your UCP console dashboard, locate the **Docker CLI** section and click **Download**.
2. Choose the Linux or macOS binary.
3. Under **My Profile** (your admin user), download the client certificates ZIP.

![The image shows a webpage from Docker documentation, detailing instructions for downloading and using the Docker CLI client. It includes navigation menus and highlighted sections for downloading client binaries.](https://kodekloud.com/kk-media/image/upload/v1752873878/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-EE-UCP-Client-Bundle/docker-cli-client-download-instructions.jpg)

```bash theme={null}
unzip ucp-bundle-{username}.zip
eval "$(env.sh)"
```

> **lightbulb** Keep your client certificates secure. Do not commit them into version control.

Back in the UCP dashboard, click **New Client Bundle** to generate and download your personalized bundle. You should now have:

* `docker` CLI binary
* `ucp-bundle-{username}.zip`

## 3. Setting Up a Remote Client

For this example, we provisioned a CentOS host on AWS named `Yogesh Client Bundle Test`. Transfer both the Docker CLI binary and the UCP client bundle (e.g., via WinSCP), then:

```bash theme={null}
