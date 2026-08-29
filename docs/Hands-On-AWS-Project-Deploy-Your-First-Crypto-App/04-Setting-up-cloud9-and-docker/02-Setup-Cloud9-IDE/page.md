# Setup Cloud9 IDE

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Setting-up-cloud9-and-docker/Setup-Cloud9-IDE/page

Guide to provisioning an AWS Cloud9 IDE, cloning a CodeCommit repository, inspecting a Flask app, and preparing to containerize it with Docker

Welcome back. In this lesson you'll provision an AWS Cloud9 IDE and prepare a development workspace for the sample application used throughout this course. Follow the steps below to create the environment, inspect the repository, and run the initial app files.

1. Open the AWS Management Console and search for Cloud9. Select the Cloud9 service. If you use Cloud9 frequently, bookmark it — bookmarked services appear in the left panel.

<Frame>
  <img alt="The image shows the AWS Cloud9 web page, which describes it as a cloud IDE for writing, running, and debugging code, highlighting features, benefits, and how it works. There are sections for getting started and additional resources on the page." />
</Frame>

2. Create a new Cloud9 environment:
   * Click "Create environment".
   * Provide a name (this lesson uses `CodingGround`) and an optional description.
   * Leave other settings at their defaults unless you have specific instance size or networking requirements.

<Frame>
  <img alt="The image shows an AWS Cloud9 environment creation page, where users can name the environment, provide a description, and choose between a new or existing EC2 instance. Different instance types with varying RAM and vCPU specifications are also displayed." />
</Frame>

Cloud9 will provision the required backend resources (it creates and configures an EC2 instance for your IDE). Provisioning typically takes 5–10 minutes. When the environment is ready, click "Open" to launch the Cloud9 editor in a new tab and wait for the IDE to initialize and connect.

> **lightbulb** Cloud9 uses an EC2 instance billed to your account. If you want to avoid ongoing charges, stop or terminate the instance when not in use.

Once connected, the Cloud9 interface provides a complete development workspace: the file tree is on the left, the editor in the center, and an integrated terminal at the bottom.

<Frame>
  <img alt="The image shows an AWS Cloud9 development environment interface with a welcome screen and a terminal at the bottom. The interface includes navigation options and a &#x22;Getting started&#x22; section on the right." />
</Frame>

For example, opening the repository `README.md` displays the file in the editor while leaving the terminal available for commands.

<Frame>
  <img alt="The image shows an AWS Cloud9 development environment with a README.md file open, displaying a welcome message and instructions. A terminal window is visible at the bottom, ready for user input." />
</Frame>

Next: clone the course repository from AWS CodeCommit into your Cloud9 environment.

4. In the AWS Console, open CodeCommit and copy the repository’s HTTPS clone URL.

<Frame>
  <img alt="The image shows a screenshot of the AWS CodeCommit console displaying a list of repositories, including &#x22;aws-microservice-project,&#x22; &#x22;login-page,&#x22; and &#x22;aws-microservice,&#x22; with options for HTTP and SSH clone URLs." />
</Frame>

Important: Your Cloud9 EC2 instance must be able to authenticate to CodeCommit. If you see authentication errors while cloning, ensure either:

* The Cloud9 EC2 instance has an IAM role attached with the necessary CodeCommit permissions, or
* You have configured the AWS CLI credential helper / Git credentials for CodeCommit on the instance.

Now switch to the Cloud9 terminal and run the clone command. Example output:

```bash theme={null}
ec2-user:~/environment $ git clone https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/aws-microservice-project
Cloning into 'aws-microservice-project'...
remote: Counting objects: 24, done.
Unpacking objects: 100% (24/24), 10.94 MiB | 15.82 MiB/s, done.
ec2-user:~/environment $
```

After cloning, a new folder `aws-microservice-project` appears in the Cloud9 file tree. Expand it to inspect project files. Typical top-level files and folders include:

| File / Folder | Purpose                                             |
| ------------- | --------------------------------------------------- |
| `app.py`      | Main Flask application entry point.                 |
| `templates/`  | HTML templates (e.g. `login.html`, `product.html`). |
| `static/`     | Static assets like CSS and images.                  |
| `README.md`   | Project overview and setup instructions.            |

Below is an excerpt from `app.py` to show the basic Flask structure and where the database client will be integrated later:

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for
import psycopg2  # Will be used later for PostgreSQL connections

app = Flask(__name__)
