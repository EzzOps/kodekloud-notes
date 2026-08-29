# Build and test dockerfile locally inside Cloud9

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Setting-up-cloud9-and-docker/Build-and-test-dockerfile-locally-inside-Cloud9/page

Guide to building, running, and testing a Flask Docker image in AWS Cloud9, exposing port, adjusting EC2 security group, and committing Dockerfile to Git.

In this lesson you'll build and run a Docker image for a Python (Flask) app inside an AWS Cloud9 environment. We will:

* Build a Docker image locally inside the Cloud9 EC2 instance.
* Run the container and map its port to the EC2 instance.
* Open the EC2 security group so you can access the app from your browser.
* Commit the Dockerfile and related changes back to your Git repository.

Docker CLI is already available in the Cloud9 environment. Follow the steps below.

## Dockerfile for the Flask app

This Dockerfile uses the official Python 3.10 slim image, installs dependencies from `requirements.txt`, exposes port 5000, and runs the Flask development server.

```dockerfile theme={null}
