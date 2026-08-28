# Unit testing with pytest

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Jenkins/Unit-testing-with-pytest/page

This guide explains setting up a Jenkins Pipeline to automate tests for a Flask application using Pytest.

In this guide, we demonstrate how to set up a Jenkins Pipeline to run automated tests on a Flask application using Pytest. Follow the step-by-step instructions below to integrate your Flask project with Jenkins and ensure your code remains robust with continuous testing.

## Setting Up the Jenkins Pipeline

Begin by creating a new pipeline in Jenkins for your Flask project:

1. In Jenkins, create a new item, name it "Flask Pipeline," and select **Pipeline** as the project type.

<Frame>
  ![The image shows a Jenkins dashboard with two pipeline projects listed: "Flask-pipeline" and "HelloWorldPipeline," displaying their last success times and durations. The build queue and executor status are also visible, indicating no builds in the queue and two idle executors.](https://kodekloud.com/kk-media/image/upload/v1752879910/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Unit-testing-with-pytest/jenkins-dashboard-pipeline-projects.jpg)
</Frame>

2. Configure the build trigger to use the GitHub hook trigger for Git SCM polling.

<Frame>
  ![The image shows a Jenkins interface where a user is creating a new item named "flaskpipeline." Various project types like Freestyle project, Pipeline, and Multi-configuration project are listed as options.](https://kodekloud.com/kk-media/image/upload/v1752879912/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Unit-testing-with-pytest/jenkins-create-flaskpipeline-item.jpg)
</Frame>

3. For the pipeline configuration, use a Jenkinsfile stored in the application's Git repository instead of defining the script directly in Jenkins. This way, Jenkins fetches its instructions from your GitHub repo.

<Frame>
  ![The image shows a Jenkins configuration page for a project named "flaskpipeline," with options for build triggers and pipeline script settings.](https://kodekloud.com/kk-media/image/upload/v1752879913/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Unit-testing-with-pytest/jenkins-flaskpipeline-configuration.jpg)
</Frame>

4. Select **Pipeline script from SCM**, choose **Git**, and enter the URL of your Git repository. If your repository is private, be sure to provide the appropriate credentials.

<Frame>
  ![The image shows a Jenkins configuration page for setting up a pipeline with a Git repository URL and credential options. The interface includes options to save or apply the configuration.](https://kodekloud.com/kk-media/image/upload/v1752879914/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Unit-testing-with-pytest/jenkins-pipeline-configuration-git.jpg)
</Frame>

5. Specify the branch to build as "main" (or your designated branch) if your repository contains only that branch.

<Frame>
  ![The image shows a GitHub repository page for a project named "jenkins-project" by "kodekloudhub," displaying a list of files and a branch selection dropdown. The repository has one branch, several commits, and contributors listed on the right.](https://kodekloud.com/kk-media/image/upload/v1752879915/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Unit-testing-with-pytest/github-repo-jenkins-project-kodekloudhub.jpg)
</Frame>

6. By default, Jenkins will look for a file named **Jenkinsfile** in the repository's root directory. If your file is located elsewhere or under a different name, provide the full path accordingly. In our case, the Jenkinsfile is in the root directory.

## Exploring the Application Files

Our project is a straightforward Python Flask application. Below is an overview of the key files:

### Main Application Code: app.py

```python theme={null}
from flask import Flask, render_template, request

app = Flask(__name__)
