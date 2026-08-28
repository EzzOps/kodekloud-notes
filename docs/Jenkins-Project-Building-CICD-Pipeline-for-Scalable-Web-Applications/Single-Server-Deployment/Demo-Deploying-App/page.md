# Example output:
# [main cf412ea] single server deployment
# 1 file changed, 27 insertions(+), 21 deletions(-)
git push origin main
```

Once pushed, Jenkins will trigger the build. Check the console output for messages that confirm the checkout, dependency installation, successful tests with Pytest, packaging, and SSH-based deployment.

## Step 5: Verify Deployment

After a successful build, open your production server's IP address in a web browser (typically on port 5000). You should see your deployed application running. This verifies that the Jenkins pipeline successfully deployed your application.

## Step 6: Make a Quick Code Update

To demonstrate the update mechanism, make a small change to your application. For example, update the `index.html` file to indicate a new version:

```html theme={null}
<html>
<head>
<style>
  .task-text {
    margin: 0;
  }
</style>
</head>
<body>
<h1>Todo App: v2</h1>
<!-- Add Task Form -->
<form method="post">
```

Then, commit and push the changes:

```bash theme={null}
git add .
git commit -m "upgrade to version 2"
# Example output:
# [main d1f31ad] upgrade to version 2
# 1 file changed, 1 insertion(+), 1 deletion(-)
git push origin main
```

Jenkins will trigger a new build, and the updated version of the application will be deployed automatically. Review the console output for confirmation of installation logs, test results, packaging, and deployment messages.

<Frame>
  ![The image shows a web page of a "Todo App: v2" with a text input field to enter a new task and a button labeled "Add Task." A task labeled "sdfasdf" is listed below.](https://kodekloud.com/kk-media/image/upload/v1752879987/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Pipeline/todo-app-v2-input-add-task.jpg)
</Frame>

This streamlined process demonstrates how to configure a Jenkins pipeline that automatically runs tests on every Git push, packages your application, and deploys it to a production server—ensuring continuous integration and continuous deployment (CI/CD) for your project.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/5fe5875c-d1e2-4f35-8161-af0830fe0deb/lesson/e342cfff-6f0f-40ed-94da-d0ef07044633" />
</CardGroup>


# Demo Deploying App

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Single-Server-Deployment/Demo-Deploying-App/page

Learn to set up a production server on AWS for deploying your application and configuring a CI/CD pipeline.

In this guide, you'll learn how to set up a production server on AWS to deploy your application. Later, this server will serve as the target when configuring your CI/CD pipeline. Follow these steps to launch an Amazon EC2 instance, configure SSH access, and set up a systemd service for your Flask app.

## Step 1: Launching an EC2 Instance

When you log into the AWS console, you will see the EC2 management console displaying a list of running instances:

<Frame>
  ![The image shows an AWS EC2 management console with a list of running instances, including details like instance ID, state, type, and status checks.](https://kodekloud.com/kk-media/image/upload/v1752879989/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-management-console-instances.jpg)
</Frame>

To create a new instance:

1. Click on the **Launch Instance** button.
2. Choose the desired Amazon Machine Image (AMI) and instance type. For a basic Linux server, the default configuration is sufficient.

<Frame>
  ![The image shows the AWS EC2 console for launching an instance, with options to select the instance name, Amazon Machine Image (AMI), and instance type. The summary panel on the right provides details about the selected configuration.](https://kodekloud.com/kk-media/image/upload/v1752879991/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-launch-instance-console.jpg)
</Frame>

### Important Settings:

* **Instance Type:** Use the default instance type (usually a t2.micro with 1 GB memory and one vCPU).
* **Key Pair:** Select an existing SSH key (e.g., "main") for secure access. This will be crucial later when Jenkins connects to your server.
* **Network Settings:** Ensure you allow both HTTPS and HTTP traffic, as your server will host a web service.

<Frame>
  ![The image shows an AWS EC2 instance launch configuration screen, detailing options for instance type, key pair, and network settings. The selected instance type is "t2.micro," which is free tier eligible.](https://kodekloud.com/kk-media/image/upload/v1752879992/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-instance-launch-configuration.jpg)
</Frame>

<Frame>
  ![The image shows an AWS EC2 instance launch configuration screen, detailing network settings and a summary of the instance specifications.](https://kodekloud.com/kk-media/image/upload/v1752879994/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-instance-launch-configuration-2.jpg)
</Frame>

After confirming your configuration, click **Launch**. Wait for a minute or two for the instance to start up.

<Frame>
  ![The image shows an AWS EC2 instance launch configuration screen, detailing storage options and a summary of the instance settings. The "Launch instance" button is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752879995/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-instance-launch-configuration-3.jpg)
</Frame>

Once the instance is running, return to the instances list to locate your production server and copy its IP address.

<Frame>
  ![The image shows an AWS EC2 console screen indicating a successful instance launch, with options for next steps like connecting to the instance and managing resources.](https://kodekloud.com/kk-media/image/upload/v1752879996/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-console-instance-launch.jpg)
</Frame>

<Frame>
  ![The image shows an AWS EC2 management console with a list of instances, including details for a selected instance named "prod-server." The instance is running, with its type, IP addresses, and other details displayed.](https://kodekloud.com/kk-media/image/upload/v1752879997/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Deploying-App/aws-ec2-management-console-prod-server.jpg)
</Frame>

## Step 2: Connecting to Your Server via SSH

Open your terminal and connect via SSH using your key (e.g., `main.pem`) and the default username `ec2-user`:

```bash theme={null}
ssh -i main.pem ec2-user@<Your_EC2_Instance_IP>
```

Upon connecting, you might see a prompt similar to:

```bash theme={null}
The authenticity of host '3.89.97.104 (3.89.97.104)' can't be established.
ED25519 key fingerprint is SHA256:[SECRET_REDACTED].
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes.
Warning: Permanently added '3.89.97.104' to the list of known hosts.
Amazon Linux 2023
https://aws.amazon.com/linux/amazon-linux-2023
[ec2-user@ip-172-31-16-211 ~]$
```

<Callout icon="lightbulb">
  The `main.pem` file is essential for authentication. Your Jenkins server will also use this key later to automatically copy your code and restart your application.
</Callout>

## Step 3: Setting Up the Application Environment

Once connected, set up your application directory, create a Python virtual environment, and verify your working directory:

```bash theme={null}
mkdir app
cd app
pwd  # Expected output: /home/ec2-user/app
```

Check that Python 3 is installed:

```bash theme={null}
python3 --version
```

If needed, install or upgrade Python 3 before proceeding. Then, create a virtual environment:

```bash theme={null}
python3 -m venv venv
ls  # You should see the "venv" directory.
```

## Step 4: Configuring a systemd Service for the Flask App

Next, configure a systemd service so that your Flask application is automatically managed by the server. Create the service file in the `/etc/systemd/system` directory using `sudo` with your preferred editor (e.g., `vi`):

```bash theme={null}
sudo vi /etc/systemd/system/flask-app.service
```

Paste the following configuration into the file:

```ini theme={null}
[Unit]
Description=Flask Application Service
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/app/
Environment="PATH=/home/ec2-user/app/venv/bin"
ExecStart=/home/ec2-user/app/venv/bin/python3 /home/ec2-user/app/app.py

[Install]
WantedBy=multi-user.target
```

Ensure that the paths in `WorkingDirectory`, `Environment`, and `ExecStart` correctly reflect your server's configuration.

After saving the file, reload systemd to register your new service:

```bash theme={null}
sudo systemctl daemon-reload
```

Enable the service to start automatically on boot:

```bash theme={null}
sudo systemctl enable flask-app.service
```

You should see an output like:

```bash theme={null}
Created symlink /etc/systemd/system/multi-user.target.wants/flask-app.service → /etc/systemd/system/flask-app.service.
```

Start the service:

```bash theme={null}
sudo systemctl start flask-app.service
```

Check its status to ensure it is running:

```bash theme={null}
sudo systemctl status flask-app.service
```

<Callout icon="triangle-alert">
  At this stage, the service may fail because the `app.py` file has not yet been copied to `/home/ec2-user/app`. Once your application code is deployed, restart the service with:

  ```bash theme={null}
  sudo systemctl restart flask-app.service
  ```
</Callout>

## Next Steps

This guide completes the initial setup of your production server. In the next tutorial, you will learn how to configure your CI/CD pipeline so that every time you push code to Git, the updated code is automatically copied to your server and the service is restarted.

Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/5fe5875c-d1e2-4f35-8161-af0830fe0deb/lesson/ccc4043a-0fe0-49fa-b67f-613de5bd3e52" />
</CardGroup>
