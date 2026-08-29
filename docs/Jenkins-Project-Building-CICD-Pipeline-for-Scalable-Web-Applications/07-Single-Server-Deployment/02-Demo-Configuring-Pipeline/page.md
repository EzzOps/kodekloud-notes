# Demo Configuring Pipeline

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Single-Server-Deployment/Demo-Configuring-Pipeline/page

This guide explains how to configure a Jenkins pipeline for application deployment, covering credential setup, pipeline creation, Jenkinsfile review, and code updates.

In this guide, you'll learn how to configure a Jenkins pipeline for deploying applications. We will start by setting up the required credentials, then create and configure the pipeline job, review and update the Jenkinsfile, and finally commit and push code changes. The pipeline will execute stages to install dependencies, run tests, package code, and deploy the application using SSH.

> **lightbulb** This guide assumes you have basic familiarity with Jenkins and version control (Git). Adjust repository URLs and credentials as needed.

## Step 1: Create Credentials

### Create Secret Text Credential

1. Go to **Manage Jenkins** and select **Credentials**.
2. Expand the **Global** domain and click **Add Credentials**.
3. Choose the **Secret Text** option.
4. In the secret field, paste the production server's IP address as plain text.
5. Set the ID to `prod-dash-server-dash-IP` and provide a meaningful description (e.g., "IP address of prod server").
6. Click **Create**.

![The image shows a Jenkins interface for creating new credentials, with fields for kind, scope, secret, ID, and description.](https://kodekloud.com/kk-media/image/upload/v1752879982/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Pipeline/jenkins-create-credentials-interface.jpg)

### Create SSH Key Credential

1. Click **Add Credentials** again.
2. Choose the **SSH Username with private key** option.
3. Enter the username (for example, `ec2-user`) that will be used to connect to the server. Optionally, treat the username as secret.
4. Paste your private key directly into the provided field. If your private key is stored in a file (e.g., `main.pem`), open the file, copy its contents, and paste them here.
5. If your private key has a passphrase, provide it; otherwise, leave the field blank.
6. Click **Create**.

![The image shows a Jenkins interface for adding new credentials, with a dropdown menu for selecting the type of credential, such as "Username with password."](https://kodekloud.com/kk-media/image/upload/v1752879983/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Pipeline/jenkins-add-credentials-interface.jpg)

![The image shows a Jenkins interface for adding new credentials, with fields for description, username, and a private key. The private key is entered directly, and there's a "Create" button at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752879984/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Pipeline/jenkins-add-credentials-interface-2.jpg)

> **lightbulb** Ensure that all secrets and SSH keys are stored securely and access is limited only to trusted personnel.

Now that the credentials have been created, proceed to configure your pipeline.

## Step 2: Create Pipeline

1. Create a new pipeline job and assign it a descriptive name (e.g., "single server pipeline").
2. In the pipeline configuration, enable the **GitHub hook trigger for GITScm polling**.
3. Set the pipeline definition to **Pipeline script from SCM**:
   * Select **Git** as the SCM.
   * Provide the public repository URL.
   * Specify the branch (for example, `main`).
   * Set the script path to `Jenkinsfile`.
4. Save the configuration.

![The image shows a configuration page for a Jenkins pipeline, with options for build triggers and advanced project settings. A GitHub hook trigger for GITScm polling is selected.](https://kodekloud.com/kk-media/image/upload/v1752879985/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Pipeline/jenkins-pipeline-configuration-github-hook.jpg)

![The image shows a configuration screen for a Jenkins pipeline, where options like branch specifier and script path are being set.](https://kodekloud.com/kk-media/image/upload/v1752879986/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Pipeline/jenkins-pipeline-configuration-screen.jpg)

## Step 3: Review the Jenkinsfile

The Jenkinsfile defines the stages of your CI/CD pipeline. The sample Jenkinsfile provided below includes four stages: **Setup**, **Test**, **Package Code**, and **Deploy to Prod**.

### Initial Jenkinsfile Configuration

```groovy theme={null}
pipeline {
    agent any
    environment {
        SERVER_IP = credentials('prod-dash-server-dash-IP')
    }
    stages {
        stage('Setup') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test') {
            steps {
                sh "pytest"
            }
        }
        stage('Package code') {
            steps {
                sh "zip -r myapp.zip ./* -x '**.git**'"
                sh "ls -lart"
            }
        }
        stage('Deploy to Prod') {
            steps {
                // Deployment steps here
            }
        }
    }
}
```

In this configuration, the production server IP is stored in the `SERVER_IP` environment variable, making it available for all pipeline stages.

### Updated Pipeline with SSH Deployment

The updated Jenkinsfile integrates SSH-based deployment. With this configuration, the pipeline securely copies the packaged application to the production server and performs deployment tasks such as unzipping files, activating the virtual environment, installing dependencies, and restarting the Flask application service.

```groovy theme={null}
pipeline {
    agent any
    environment {
        SERVER_IP = credentials('prod-dash-server-dash-IP')
    }
    stages {
        stage('Setup') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test') {
            steps {
                sh "pytest"
            }
        }
        stage('Package code') {
            steps {
                sh "zip -r myapp.zip ./* -x '**.git**'"
                sh "ls -lart"
            }
        }
        stage('Deploy to Prod') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ssh-key', keyFileVariable: 'MY_SSH_KEY', usernameVariable: 'username')]) {
                    sh '''
                    scp -i $MY_SSH_KEY -o StrictHostKeyChecking=no myapp.zip ${username}@${SERVER_IP}:/home/ec2-user/
                    ssh -i $MY_SSH_KEY -o StrictHostKeyChecking=no ${username}@${SERVER_IP} << EOF
                    unzip -o /home/ec2-user/myapp.zip -d /home/ec2-user/app/
                    source app/venv/bin/activate
                    cd /home/ec2-user/app/
                    pip install -r requirements.txt
                    sudo systemctl restart flaskapp.service
EOF
                    '''
                }
            }
        }
    }
}
```

In the **Deploy to Prod** stage:

* The application code is zipped.
* The zip file is securely copied to the production server using SCP.
* An SSH session is initiated to unzip the code, activate the virtual environment, install required dependencies, and restart the Flask app service.

## Step 4: Commit and Push Code Changes

After configuring the Jenkinsfile, commit your changes and push them to your Git repository. Use the following commands:

```bash theme={null}
git add .
git commit -m "single server deployment"
