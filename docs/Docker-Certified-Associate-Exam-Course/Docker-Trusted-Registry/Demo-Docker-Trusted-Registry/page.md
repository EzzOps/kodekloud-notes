# Demo Docker Trusted Registry

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Trusted-Registry/Demo-Docker-Trusted-Registry/page

This guide covers essential Docker Trusted Registry tasks including login, repository management, image pushing, scanning, and cleanup operations.

In this guide, we’ll walk through key Docker Trusted Registry (DTR) tasks—logging in via UI and CLI, configuring external URLs, creating repositories, pushing and scanning images, adjusting scan settings, and cleaning up images and repositories.

## Table of Contents

1. [Accessing and Configuring DTR](#1-accessing-and-configuring-dtr)
2. [CLI Login to DTR](#2-cli-login-to-dtr)
3. [Creating a Repository](#3-creating-a-repository)
4. [Pushing Images to DTR](#4-pushing-images-to-dtr)
5. [Scanning Images for Vulnerabilities](#5-scanning-images-for-vulnerabilities)
6. [Scanning an Older Image](#6-scanning-an-older-image)
7. [Adjusting Image Scan Settings](#7-adjusting-image-scan-settings)
8. [Deleting Tags and Repositories](#8-deleting-tags-and-repositories)

## 1. Accessing and Configuring DTR

1. Open your browser and navigate to your DTR’s IP or DNS.
2. Log in with your credentials.

<Callout icon="triangle-alert">
  If your DTR VM doesn’t have a persistent IP or DNS name, any change will break UI access. Always assign a static IP or DNS record.
</Callout>

3. To update the external URL for DTR, use the `dtr reconfigure` command:

<Frame>
  ![The image shows a webpage from Docker documentation, specifically detailing command-line options for configuring Docker Trusted Registry (DTR). It includes descriptions and parameters for various configuration settings.](https://kodekloud.com/kk-media/image/upload/v1752873945/notes-assets/images/Docker-Certified-Associate-Exam-Course-Demo-Docker-Trusted-Registry/docker-dtr-command-line-options.jpg)
</Frame>

```bash theme={null}
docker/dtr reconfigure --dtr-external-url https://<NEW_DTR_IP_OR_URL>
```

## 2. CLI Login to DTR

On a machine with the UCP client bundle:

```bash theme={null}
docker login 54.145.234.153
