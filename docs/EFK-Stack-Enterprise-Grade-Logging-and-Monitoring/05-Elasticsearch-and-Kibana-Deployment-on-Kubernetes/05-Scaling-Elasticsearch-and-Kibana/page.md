# Scaling Elasticsearch and Kibana

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Elasticsearch-and-Kibana-Deployment-on-Kubernetes/Scaling-Elasticsearch-and-Kibana/page

This article provides a guide on deploying and scaling Elasticsearch and Kibana in a Kubernetes environment using YAML manifests.

Welcome to this detailed guide on scaling Elasticsearch and Kibana within a Kubernetes environment. In this tutorial, you will learn how to deploy a highly scalable Elasticsearch and Kibana stack using YAML manifests obtained from a GitHub repository.

## Repository Setup and Cluster Configuration

First, clone the repository containing the required YAML manifests and configure your Kubernetes context by removing the control-plane taint, creating the "efk" namespace, and setting the current context to use that namespace. Execute the following commands:

```bash theme={null}
git clone https://github.com/kodekloudhub/efk-stack.git
