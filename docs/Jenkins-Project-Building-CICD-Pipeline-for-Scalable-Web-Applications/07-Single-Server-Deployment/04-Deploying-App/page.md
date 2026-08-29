# Deploying App

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Single-Server-Deployment/Deploying-App/page

Learn to deploy a Flask application on a server, set up a virtual environment, and configure a systemd service for automatic management.

Deploy your Flask application on a server before configuring a CI/CD pipeline. In this guide, you'll learn how to deploy a Flask application to an [AWS EC2 instance](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) (or a similar server). We will walk through setting up the application directory, creating a Python virtual environment, and configuring a systemd service to manage your app.

## Setting Up the Application Directory and Virtual Environment

Begin by connecting to your server and creating a dedicated folder for your application code. In this example, we use the default user `ec2-user` on an AWS EC2 instance:

```bash theme={null}
