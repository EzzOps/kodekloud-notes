# Creating EC2 Instance

Source: https://notes.kodekloud.com/docs/Pulumi-Essentials/Pulumi-Essentials/Creating-EC2-Instance/page

Shows how to create an AWS EC2 instance and S3 bucket using Pulumi Python, export the instance public IP, and configure AMI, key pair, and SSH access.

In this lesson we'll add an Amazon EC2 instance to make the project more practical. Using the Pulumi AWS package and Python, we define an EC2 instance and export its public IP so you can SSH into it after deployment.

Below is a concise, working Pulumi program that creates an Amazon S3 bucket and an EC2 instance. Replace the AMI ID with one appropriate for your AWS region (see the note below).

```python theme={null}
