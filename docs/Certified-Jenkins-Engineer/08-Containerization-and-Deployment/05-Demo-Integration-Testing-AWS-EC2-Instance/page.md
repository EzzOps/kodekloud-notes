# Demo Integration Testing AWS EC2 Instance

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Containerization-and-Deployment/Demo-Integration-Testing-AWS-EC2-Instance/page

This article enhances a Jenkins pipeline with an integration testing stage for a Docker application on an AWS EC2 instance.

In our previous guide, we deployed a Docker image to an AWS EC2 instance. Now, we’ll enhance our **Jenkins** pipeline with an **Integration Testing** stage that dynamically discovers the EC2 instance’s public endpoint and performs HTTP checks against our service.

## Prerequisites

* Docker container running on EC2 (port 3000)
* AWS CLI configured with permissions to `ec2:DescribeInstances`
* `jq` and `curl` installed on the Jenkins agent
* Jenkins credentials (AWS Access Key & Secret) stored (e.g., ID `aws-s3-ec2-lambda-creds`)

> **lightbulb** Ensure your EC2 instance is tagged with `Name=dev-deploy`. This tag is used to filter and locate the instance dynamically.

## 1. Verify the Running Container

Log into your EC2 instance and confirm the application is up:

```bash theme={null}
ubuntu@ip-172-31-25-250:~$ sudo docker ps
CONTAINER ID   IMAGE                                        COMMAND                  CREATED           STATUS          PORTS                    NAMES
cab88363d990   siddharth67/solar-system:5376ef094c479356f…   "docker-entrypoint.s…"   53 minutes ago    Up 53 minutes   0.0.0.0:3000->3000/tcp   solar-system
```

## 2. Create the Integration Test Script

At the root of your Git repo, add `integration-testing-ec2.sh`:

```bash theme={null}
#!/usr/bin/env bash
set -euo pipefail

echo "Integration test starting..."
aws --version
