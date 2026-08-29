# 1. Clone the repo
git clone https://github.com/your-org/your-repo.git
cd your-repo

# 2. Create and switch to a feature branch
git checkout -b feature/your-feature-name

# 3. Stage and commit your changes
git add .
git commit -m "Add description of your feature or fix"

# 4. Push and publish the branch
git push -u origin feature/your-feature-name
```

After pushing, navigate to the GitHub UI to open a pull request and assign reviewers.

![The image is a flowchart illustrating a GitHub workflow, showing steps from the main branch to cloning, creating a feature branch, and making a pull request, which is then reviewed by an engineer.](https://kodekloud.com/kk-media/image/upload/v1752875416/notes-assets/images/GCP-DevOps-Project-Task-3Setup-Github-repo-according-to-DevOps-best-practice/github-workflow-flowchart-pull-request.jpg)

> **triangle-alert** Avoid emergency fixes directly on `main`. Even urgent patches should follow the pull request process to maintain auditability.

## What’s Next?

In the next article, we’ll demonstrate how to apply branch protection rules in the GitHub settings and manage pull requests step by step.

![The image shows a search bar with the query "How to enable Branch Protection?" and a copyright notice for KodeKloud.](https://kodekloud.com/kk-media/image/upload/v1752875417/notes-assets/images/GCP-DevOps-Project-Task-3Setup-Github-repo-according-to-DevOps-best-practice/search-bar-branch-protection-kodekloud.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/a334971a-4fa2-4c61-8891-9c189e2aab64/lesson/3c497c3c-5e90-43a7-977b-f470047c7b1d)


# Task 4 Coding our application locally

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-01/Task-4-Coding-our-application-locally/page

Set up and test a Flask application locally using VS Code, Docker, and Git before deployment on Google Kubernetes Engine.

Welcome back! In this task, we’ll set up and test our Flask application on your local machine before pushing it to our [GitHub repository](https://github.com). We’ll use VS Code for development, write the application code, declare dependencies, and containerize with Docker.

## Prerequisites

* VS Code: [https://code.visualstudio.com](https://code.visualstudio.com)
* Python 3.8+
* Docker installed locally
* Git configured for your project

***

## 1. Update the README

Open `README.md` in VS Code and add a clear project title and description:

```markdown theme={null}
A simple Python Flask application containerized with Docker.  
This app will later be deployed on Google Kubernetes Engine (GKE).
```

Use VS Code’s Markdown Preview (⌘+Shift+V / Ctrl+Shift+V) to verify formatting.

![The image shows a Visual Studio Code interface with a README.md file open, describing a Docker Flask application written in Python to be deployed on GKE. The file is displayed in both markdown and preview modes.](https://kodekloud.com/kk-media/image/upload/v1752875418/notes-assets/images/GCP-DevOps-Project-Task-4-Coding-our-application-locally/vscode-readme-docker-flask-gke.jpg)

***

## 2. Project File Structure

| File             | Purpose                             |
| ---------------- | ----------------------------------- |
| README.md        | Overview and setup instructions     |
| app.py           | Flask application entrypoint        |
| requirements.txt | Python dependencies                 |
| Dockerfile       | Docker container build instructions |

***

## 3. Create the Flask Application

Create `app.py` at the project root with the following code:

```python theme={null}
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Simple Flask application'
```

This defines a basic web server with one route (`/`) that returns a greeting.

***

## 4. Specify Dependencies

In `requirements.txt`, list your Python packages:

```text theme={null}
Flask
```

This tells `pip` which libraries to install inside the container.

***

## 5. Write the Dockerfile

Create `Dockerfile` and add:

```dockerfile theme={null}
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
```

Key steps:

* Use a lightweight Python base image
* Copy and install dependencies
* Copy application code
* Expose Flask on all network interfaces

> **lightbulb** If Flask does not auto-detect `app.py`, you can set the environment variable:

  ```dockerfile theme={null}
  ENV FLASK_APP=app.py
  ```

  or change the `CMD` to:

  ```dockerfile theme={null}
  CMD ["python3", "app.py"]
  ```

***

## Next Steps

With your files in place (`README.md`, `app.py`, `requirements.txt`, `Dockerfile`), you’re ready to build and run the Docker image locally:

```bash theme={null}
docker build -t flask-app:local .
docker run -p 5000:5000 flask-app:local
```

Visit [http://localhost:5000](http://localhost:5000) to verify the “Hello, Simple Flask application” message.

***

## Links and References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Docker Documentation](https://docs.docker.com/)
* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/a334971a-4fa2-4c61-8891-9c189e2aab64/lesson/70cc5e29-39a6-4dcf-b368-98ecb1c842b0)
