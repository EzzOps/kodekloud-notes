# Monitoring Kubernetes Cluster using in Elastic Agent

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Elastic-Cloud/Monitoring-Kubernetes-Cluster-using-in-Elastic-Agent/page

This guide explains how to monitor a Kubernetes cluster using Elastic Agent, including configuration, deployment, and visualization of metrics in Elastic Cloud.

Welcome to this comprehensive guide on monitoring your Kubernetes cluster with Elastic Agent. In this tutorial, you will learn how to configure Elastic Agent on your Kubernetes cluster, forward logs and metrics to Elastic Cloud, and visualize your data on a pre-configured dashboard.

## Step 1: Add the Kubernetes Integration

After logging into your Elastic Cloud console, click on the **Add integration** option. You will be presented with a list of available integrations:

<Frame>
  ![The image shows a webpage from Elastic, displaying a list of integrations for various Amazon Web Services (AWS) and other categories. The left sidebar lists categories, while the main section shows specific AWS services with descriptions.](https://kodekloud.com/kk-media/image/upload/v1752874193/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Monitoring-Kubernetes-Cluster-using-in-Elastic-Agent/elastic-aws-integrations-webpage.jpg)
</Frame>

From the list, choose the **Kubernetes integration** and then click on **Add Kubernetes**. The console provides you with an installation script that will deploy the Elastic Agent on your Kubernetes cluster.

<Frame>
  ![The image is a guide for adding an integration in Elastic, showing three steps: installing the Elastic Agent, adding the integration, and confirming incoming data.](https://kodekloud.com/kk-media/image/upload/v1752874195/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Monitoring-Kubernetes-Cluster-using-in-Elastic-Agent/elastic-integration-setup-guide.jpg)
</Frame>

## Step 2: Deploy the Elastic Agent on Kubernetes

Click the **Install Elastic Agent** option to view the Kubernetes deployment YAML along with the command required for deployment. The top portion of the deployment file appears as follows:

```yaml theme={null}
---
