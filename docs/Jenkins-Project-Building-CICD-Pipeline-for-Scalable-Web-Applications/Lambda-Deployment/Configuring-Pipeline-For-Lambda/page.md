# kubectl apply -f pod.yaml
```

Below is an illustrative diagram explaining a Kubernetes pod setup:

<Frame>
  ![The image illustrates a Kubernetes pod containing Python and Logging components, with an arrow pointing to a Kubernetes cluster represented by three icons.](https://kodekloud.com/kk-media/image/upload/v1752879938/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Working-with-Kubernetes/kubernetes-pod-python-logging-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Pods are the smallest deployable units in Kubernetes, and understanding them is crucial for designing effective containerized applications.
</Callout>

## Deployments in Kubernetes

While deploying pods directly is possible, Kubernetes provides an abstraction called a "deployment" to simplify the management of pod lifecycles. A deployment not only creates multiple pod replicas but also monitors them, restarts failed pods, handles scaling, and manages rollouts and rollbacks. For example, if your application needs a continuous presence of three instances, a deployment ensures that exactly three pods remain active.

Here is a typical deployment YAML configuration:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      name: myapp
  template:
    metadata:
      labels:
        name: myapp
    spec:
      containers:
        - name: myapp
          image: <Image>
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
          ports:
            - containerPort: 5000
```

This configuration highlights:

* **apiVersion & Kind**: Uses `apps/v1` for deployments.
* **Replicas**: Specifies the desired number of pod instances.
* **Selector & Template**: The selector identifies which pods the deployment should manage and links to the pod template that defines the pod specification.

Deploy the configuration using:

```bash theme={null}
# kubectl apply -f deployment.yaml
```

The diagram below illustrates how a deployment manages multiple pods and maintains application stability:

<Frame>
  ![The image illustrates a Kubernetes deployment with three pods, each containing Python and Logging components. It highlights features like monitoring and restarting failed pods and scaling pod instances.](https://kodekloud.com/kk-media/image/upload/v1752879939/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Working-with-Kubernetes/kubernetes-deployment-pods-monitoring.jpg)
</Frame>

<Callout icon="lightbulb">
  Deployments offer powerful management capabilities that ensure high availability and seamless updates for your applications.
</Callout>

## Managing Multiple Clusters with kubectl

Many organizations operate multiple Kubernetes clusters, such as production, staging, and development, and managing them efficiently is key. The `kubectl` CLI supports connecting to multiple clusters via a kubeconfig file, which stores all the relevant configuration details and credentials.

Below is a sample kubeconfig file:

```yaml theme={null}
apiVersion: v1
kind: Config
preferences: {}
clusters:
- name: cluster2
  cluster:
    server: https://192.168.54.19:8443
- name: cluster1
  cluster:
    server: https://192.168.59.123:8443
contexts:
- name: john@cluster1
  context:
    cluster: cluster1
    user: john
- name: mike@cluster2
  context:
    cluster: cluster2
    user: mike
current-context: cluster1
users:
- name: john
  user:
    client-certificate: <path-to-client-certificate>
    client-key: <path-to-client-key>
- name: mike
  user:
    client-certificate: <path-to-client-certificate>
    client-key: <path-to-client-key>
```

Explanation of the kubeconfig structure:

* **Clusters**: Lists each Kubernetes cluster with its API server endpoint.
* **Users**: Specifies credentials for accessing the clusters.
* **Contexts**: Ties each user to a specific cluster.
* **Current Context**: Determines the default context used by `kubectl`.

By default, `kubectl` searches for this configuration file in the `$HOME/.kube/config` directory. You can also specify the configuration location using:

| Method                | Command/Variable                      |
| --------------------- | ------------------------------------- |
| Directory             | `$HOME/.kube/config`                  |
| Environment Variable  | `KUBECONFIG`                          |
| Command Line Argument | `kubectl --kubeconfig <path-to-file>` |

To switch between contexts (and hence clusters), use the following commands:

```bash theme={null}
> kubectl config use-context john@cluster1
```

And to switch to another context:

```bash theme={null}
> kubectl config use-context mike@cluster2
```

Using multiple contexts is essential in a CI/CD pipeline. For instance, you might deploy to a staging cluster first (e.g., using `mike@cluster2`) before promoting changes to the production cluster.

The following diagram shows how `kubectl` connects to various Kubernetes clusters:

<Frame>
  ![The image is a diagram showing "kubectl" connected to three Kubernetes clusters labeled Cluster1, Cluster2, and Cluster3.](https://kodekloud.com/kk-media/image/upload/v1752879940/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Working-with-Kubernetes/kubectl-kubernetes-clusters-diagram.jpg)
</Frame>

<Callout icon="triangle-alert">
  Always ensure your kubeconfig file is secured, as it contains sensitive credentials to access your Kubernetes clusters. Use RBAC and other security measures to safeguard your infrastructure.
</Callout>

By understanding these core concepts—pods, deployments, and kubeconfig management—you are now well-equipped to configure and manage Kubernetes environments within your CI/CD pipelines using Jenkins. For more detailed Kubernetes information, consider exploring the [Kubernetes Documentation](https://kubernetes.io/docs/) and other helpful resources.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/1d8036bf-2606-4587-beef-925546e0c655/lesson/0c653b80-3075-4e39-b7e1-79f5584f6568" />
</CardGroup>


# Configuring Pipeline For Lambda

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Lambda-Deployment/Configuring-Pipeline-For-Lambda/page

This article explains how to configure a CI/CD pipeline for AWS Lambda applications using Jenkins and the SAM CLI.

In this lesson, we outline how to set up a robust CI/CD pipeline for your AWS Lambda application using Jenkins and the SAM CLI. This guide covers installing the SAM CLI on Jenkins, configuring AWS permissions, and establishing a pipeline that automates code checkout, dependency installation, testing, building, and deployment.

## Preparing Jenkins

Before proceeding, install the SAM CLI on your Jenkins server. This tool is essential for building and deploying your Lambda code to AWS, just as you would on your local machine.

<Frame>
  ![The image shows a diagram illustrating the installation of SAM CLI on Jenkins, featuring a connection between a SAM CLI box and the Jenkins logo.](https://kodekloud.com/kk-media/image/upload/v1752879942/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Configuring-Pipeline-For-Lambda/sam-cli-jenkins-installation-diagram.jpg)
</Frame>

For detailed installation instructions, please refer to the official SAM CLI documentation.

## Setting Up AWS Permissions

Proper AWS permissions are required for Jenkins to deploy Lambda functions. Start by creating an AWS user with the necessary permissions, and generate an access key and secret key. These credentials will be stored securely in Jenkins.

<Frame>
  ![The image illustrates AWS permissions, showing a user with associated permissions and AWS credentials, including an access key and a secret key.](https://kodekloud.com/kk-media/image/upload/v1752879943/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Configuring-Pipeline-For-Lambda/aws-permissions-user-credentials.jpg)
</Frame>

<Callout icon="lightbulb">
  Ensure that the created AWS user has only the permissions needed for deploying Lambda functions to maintain security best practices.
</Callout>

## Pipeline Overview

The CI/CD pipeline is designed to execute the following sequential steps:

1. Checkout the code from the repository.
2. Install dependencies.
3. Run tests.
4. Build the code using the SAM CLI.
5. Deploy the built application to AWS.

<Frame>
  ![The image is a flowchart titled "Configuring Pipeline," showing steps: Checkout Code, Install Dependencies, Test Code, Build (sam build), and Deploy (sam deploy), with a note about needing AWS credentials.](https://kodekloud.com/kk-media/image/upload/v1752879944/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Configuring-Pipeline-For-Lambda/configuring-pipeline-flowchart.jpg)
</Frame>

## Jenkins Pipeline Configuration

Below is an example Jenkins pipeline configuration. Note that this project contains two `requirements.txt` files. In this example, the development dependencies are installed from `lambda-app/tests/requirements.txt` before running tests.

### Setup Stage: Installing Dependencies

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh "pip3 install -r lambda-app/tests/requirements.txt"
            }
        }
        // Run tests here (e.g., using pytest) if needed.
```

### Build Stage: Building the Code

With the dependencies installed and tests (if any) executed, the next step is to build the Lambda application using the SAM CLI. The command uses the `lambda-app/template.yaml` file to define the build parameters.

```groovy theme={null}
        stage('Build') {
            steps {
                sh "sam build -t lambda-app/template.yaml"
            }
        }
```

### Deploy Stage: Deploying to AWS

The deploy stage includes AWS credentials provided as environment variables. These credentials are set for this stage only to enhance security. The `sam deploy` command is executed with flags `--no-confirm-changeset` and `--no-fail-on-empty-changeset` to automate the deployment process without manual input.

```groovy theme={null}
        stage('Deploy') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('aws-access-key')
                AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
            }
            steps {
                sh "sam deploy -t lambda-app/template.yaml --no-confirm-changeset --no-fail-on-empty-changeset"
            }
        }
    }
}
```

<Callout icon="lightbulb">
  Automating your deployment process with Jenkins ensures consistent and reproducible builds, reducing manual errors and accelerating your release cycles.
</Callout>

This configuration completes the setup of your CI/CD pipeline for AWS Lambda. With these automated steps, every aspect from dependency installation to deployment is seamlessly integrated within Jenkins.

Happy automating your deployments!

## Links and References

* [AWS Lambda Documentation](https://aws.amazon.com/documentation/lambda/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/ddd997d7-0eea-4fa7-8265-5feeb01301e8/lesson/f109f29c-e997-451b-a80f-5e4162a495d7" />
</CardGroup>
