# Kubernetes on AWS EKS

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Kubernetes-on-the-Cloud/Kubernetes-on-AWS-EKS/page

This article guides you through creating an Amazon EKS cluster and

In this lesson, we will guide you through creating an Amazon Elastic Kubernetes Service (EKS) cluster—Amazon’s managed Kubernetes solution. Before proceeding, ensure you have met the prerequisites listed below:

<Frame>
  ![The image lists prerequisites for AWS setup, including an AWS account, KubeCtl CLI, EKS roles, IAM roles, VPC, EC2 key pair, and AWS basics.](https://kodekloud.com/kk-media/image/upload/v1752884924/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-AWS-EKS/frame_10.jpg)
</Frame>

<Callout icon="lightbulb">
  • An active AWS account (new users can explore free access via the AWS Free Tier).\
  • Installation of the [kubectl](https://kubernetes.io/docs/tasks/tools/) utility.\
  • Basic AWS knowledge to configure a cluster role for EKS, create an IAM role for the node group, set up a VPC, and generate an EC2 key pair (the key pair is helpful for SSH access if needed).\
  • The AWS CLI installed and configured with your credentials.
</Callout>

***

## Installing and Configuring the AWS CLI

First, verify that the AWS CLI is installed by running:

```bash theme={null}
aws --version
```

If the AWS CLI is missing, install it using one of the following methods:

**On macOS:**

```bash theme={null}
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

**Using pip3:**

```bash theme={null}
pip3 install awscli --upgrade --user
```

After installation, ensure that the AWS CLI is properly configured with your credentials.

***

## Setting Up kubectl

Since kubectl is already installed, you can verify its version and update your PATH if necessary. First, move the binary to a directory in your home and update your PATH:

```bash theme={null}
mkdir -p $HOME/bin && mv ./kubectl $HOME/bin/ && export PATH=$PATH:$HOME/bin
```

(Optional) To permanently add `$HOME/bin` to your PATH, append the following line to your shell initialization file (e.g., `~/.bash_profile`):

```bash theme={null}
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
```

Finally, check the kubectl client version to ensure it is ready:

```bash theme={null}
kubectl version --short --client
```

***

## Creating the EKS Cluster

Before creating your cluster, confirm you have set up the required IAM role for your EKS cluster and prepared a VPC (or you can choose the default VPC). Follow these steps:

1. Log in to your AWS account and navigate to **Services**.
2. Search for **EKS** and select the service.
3. Click **Create cluster** and configure the cluster:
   * **Cluster Configuration:**\
     Provide a name for your cluster (e.g., `example-voting-app`) and keep the default Kubernetes version (e.g., 1.16). Select the appropriate IAM role for your cluster.

<Frame>
  ![The image shows the AWS EKS console interface for configuring a Kubernetes cluster, including options for naming, version selection, and secrets encryption.](https://kodekloud.com/kk-media/image/upload/v1752884925/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-AWS-EKS/frame_120.jpg)
</Frame>

* Click **Next**.

4. **Networking Configuration:**\
   Choose the default VPC in your region (e.g., US West 2 (Oregon 2)) and select all available subnets.

<Frame>
  ![The image shows the "Specify networking" step in creating an Amazon EKS cluster, where VPC and subnets are selected for network configuration.](https://kodekloud.com/kk-media/image/upload/v1752884926/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-AWS-EKS/frame_140.jpg)
</Frame>

5. Continue through the review pages by clicking **Next**, then click **Create**. Creation may take up to 10 minutes.

When the cluster status becomes active (checkmark visible), you can proceed to add a node group.

***

## Adding a Node Group

A node group represents a set of worker nodes that run your application workloads. To add a node group, follow these steps:

1. In your EKS cluster's **Compute** section, click **Add node group**.
2. Name the node group (e.g., `demo-workers`) and select the previously created EKS node IAM role.
3. Choose the default subnets (or select those that correspond with your network setup).

<Frame>
  ![The image shows an AWS EKS console screen for configuring a node group, including fields for naming, IAM role selection, and subnet configuration.](https://kodekloud.com/kk-media/image/upload/v1752884927/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-AWS-EKS/frame_200.jpg)
</Frame>

4. Optionally, select an EC2 key pair if you wish to enable SSH access to the worker nodes.
5. In the **Compute Configuration** section, review settings like AMI type, instance type, and disk size. Default values are generally acceptable.

<Frame>
  ![The image shows an AWS EKS console screen for setting node compute configuration, including AMI type, instance type, and disk size for a cluster.](https://kodekloud.com/kk-media/image/upload/v1752884928/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-AWS-EKS/frame_230.jpg)
</Frame>

6. Set the auto scaling parameters (minimum, maximum, and desired number of nodes), review your configuration, and click **Create**. Provisioning may take several minutes.

When the node group status is active and the worker nodes are visible (as EC2 instances), your cluster is now fully set up.

<Frame>
  ![The image shows an Amazon EKS console with a node group configuration for "demo-workers," indicating an active status and details like Kubernetes version and instance type.](https://kodekloud.com/kk-media/image/upload/v1752884930/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-AWS-EKS/frame_270.jpg)
</Frame>

***

## Configuring kubectl for the EKS Cluster

Your local kubectl might be configured for a different cluster (e.g., Minikube). To switch to your new AWS EKS cluster, update your kubeconfig file using the AWS CLI. Replace the region and cluster name as needed:

```bash theme={null}
aws eks --region us-west-2 update-kubeconfig --name example-voting-app
```

This command adds a new context to your kubeconfig file (typically located at `~/.kube/config`). Test your configuration by listing the nodes:

```bash theme={null}
kubectl get nodes
```

You should see your worker nodes listed. Keep in mind that in managed Kubernetes services like EKS, the master nodes are maintained by AWS and are neither accessible for SSH nor intended for running workloads.

***

## Deploying the Voting Application

With your EKS cluster ready and kubectl configured, it’s time to deploy the sample voting application. Start by cloning the GitHub repository:

```bash theme={null}
