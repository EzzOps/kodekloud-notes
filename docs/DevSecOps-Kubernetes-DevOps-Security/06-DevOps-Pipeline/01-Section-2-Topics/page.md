# Section 2 Topics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Section-2-Topics/page

This section covers setting up infrastructure, installing software, and building a Jenkins pipeline with four stages.

In this section, we’ll walk through the essential steps to provision your infrastructure, install necessary software, and build a simple Jenkins pipeline with four stages. By the end, you’ll have:

| Step | Description                             | Script Location                   |
| ---- | --------------------------------------- | --------------------------------- |
| 1    | Set up a free Azure account             | `scripts/create-azure-account.sh` |
| 2    | Create a Linux virtual machine          | `scripts/create-vm.sh`            |
| 3    | Deploy a single-node Kubernetes cluster | `scripts/deploy-k8s-cluster.sh`   |
| 4    | Install software for hands-on labs      | `scripts/install-lab-software.sh` |

> **lightbulb** Make sure you have:

  * A Microsoft account to sign up for [Azure Free Account](https://azure.microsoft.com/free/).
  * `az` CLI installed locally.
  * Basic familiarity with [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) and [Jenkins Pipelines](https://www.jenkins.io/doc/book/pipeline/).

![The image outlines a DevOps pipeline process, including setting up a VM, installing software, understanding use cases, and implementing a basic DevOps pipeline. It also covers DevSecOps and Kubernetes security topics.](https://kodekloud.com/kk-media/image/upload/v1752873604/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Section-2-Topics/devops-pipeline-vm-software-security.jpg)

## 1. Set Up a Free Azure Account

1. Navigate to the Azure free tier page.
2. Complete the sign-up form to obtain \$200 in credits.
3. Verify your email and phone number.

> **triangle-alert** Free credits expire after 30 days. Monitor your usage in the [Azure Portal](https://portal.azure.com/) to avoid unexpected charges.

## 2. Create a Virtual Machine

Use the Azure CLI to spin up a Linux VM:

```bash theme={null}
az login
az group create --name DevOpsRG --location eastus
az vm create \
  --resource-group DevOpsRG \
  --name DevNode \
  --image UbuntuLTS \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys
```

## 3. Deploy a Single-Node Kubernetes Cluster

Install Kubernetes with `kubeadm`:

```bash theme={null}
ssh azureuser@<VM_PUBLIC_IP>
sudo apt-get update && sudo apt-get install -y docker.io kubeadm
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

## 4. Install Software for Hands-On Labs

Install common DevOps tools:

```bash theme={null}
