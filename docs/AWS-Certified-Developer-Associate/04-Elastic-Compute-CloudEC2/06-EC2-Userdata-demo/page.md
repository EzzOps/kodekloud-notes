# EC2 Userdata demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Elastic-Compute-CloudEC2/EC2-Userdata-demo/page

Guide showing how to use EC2 user data with cloud-init to install, start, and enable nginx automatically on an instance's first boot.

This guide demonstrates how to use EC2 user data to run an initialization script automatically when a new Amazon EC2 instance boots. Using user data (via cloud-init) lets you perform first-boot configuration such as installing packages, starting services, or bootstrapping applications without SSHing into the instance.

Goal: Launch an EC2 instance that installs, starts, and enables nginx on first boot so the web server is reachable immediately after initialization.

Prerequisites:

* An AWS account with permissions to launch EC2 instances.
* A key pair to access the instance (optional for this demo since configuration is via user data).
* A security group that allows HTTP (80) and HTTPS (443) inbound access.

Step 1 — Launch a new EC2 instance

* Open the EC2 console and click "Launch instance".
* Give the instance a descriptive Name (for example, userdata-demo).
* Select an Amazon Linux AMI (or another supported Linux AMI that uses yum).

<Frame>
  <img alt="Screenshot of the Amazon Web Services EC2 console dashboard. It shows resource summaries, a &#x22;Launch instance&#x22; button, service health status, and the left-hand navigation for instances, images, and storage." />
</Frame>

Step 2 — Choose instance configuration

* Choose an appropriate instance type (t2.micro is fine for testing and is often within the AWS Free Tier).
* Select your key pair or create one if you plan to SSH later.
* Configure networking and storage as needed.

Step 3 — Configure Security Group
Allow inbound access so nginx can serve traffic. At minimum, allow:

| Protocol | Port | Source                   | Purpose                          |
| -------- | ---- | ------------------------ | -------------------------------- |
| TCP      | 80   | 0.0.0.0/0                | HTTP (nginx default)             |
| TCP      | 443  | 0.0.0.0/0                | HTTPS (if serving TLS)           |
| TCP      | 22   | \<your-ip>/32 (optional) | SSH access — restrict to your IP |

Step 4 — Add your user data script
Open Advanced Details on the launch page and paste the script into the User data field (you can also upload a file). The script below runs as root during the instance's first boot and uses yum to install nginx, then starts and enables it:

```bash theme={null}
#!/bin/bash
sudo yum install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

> **lightbulb** User data scripts run as root on first boot via cloud-init. If you need to troubleshoot, check /var/log/cloud-init-output.log on the instance for the script's output and any error messages.

Step 5 — Launch and verify

* Launch the instance and wait for its status checks to pass.
* From the EC2 Instances page, note the instance's Public IPv4 address or Public DNS.

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch Instance&#x22; console showing AMI options (Amazon Linux, macOS, Ubuntu, Windows, etc.) and details on the right summary panel with a t2.micro instance selected and a &#x22;Launch instance&#x22; button." />
</Frame>

<Frame>
  <img alt="A screenshot of the AWS EC2 Instances dashboard showing two running t2.micro instances (one named &#x22;userdata-demo&#x22;) with status checks passed." />
</Frame>

Open a browser and navigate to http\://\<public-ip> (replace \<public-ip> with the instance address). You should see the default nginx welcome page, confirming the user data script installed and started nginx successfully.

<Frame>
  <img alt="A screenshot of a web browser displaying the default &#x22;Welcome to nginx!&#x22; page (showing the nginx welcome text and links) served from an IP address. Browser tabs and the address bar are visible at the top." />
</Frame>

Troubleshooting tips

* Confirm the instance has a public IP and the security group allows inbound HTTP.
* Verify cloud-init ran by inspecting /var/log/cloud-init.log and /var/log/cloud-init-output.log on the instance.
* If the package manager fails, ensure your chosen AMI supports yum (Amazon Linux / RHEL / CentOS) or adjust the script for apt (Ubuntu/Debian).

> **warning** User data runs only during the instance's initial boot. To re-run initialization you can: bake a new AMI with the changes, use configuration management (Ansible/Chef/Puppet), or manually re-run scripts via SSH or with cloud-init's re-run options.

Links and references

* [Amazon EC2 User Guide — Running Commands on Your Linux Instance at Launch](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
* [cloud-init Documentation](https://cloud-init.io/)
* [nginx Official Site](https://nginx.org/)
* [Amazon Linux AMI](https://aws.amazon.com/amazon-linux-ami/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/538040df-b323-4fd1-ad80-f5c22725c345/lesson/4d194068-131d-4c68-81d7-c6bb83184e48)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/538040df-b323-4fd1-ad80-f5c22725c345/lesson/94dee8ad-43a6-4e6d-8600-6c55be407222)
