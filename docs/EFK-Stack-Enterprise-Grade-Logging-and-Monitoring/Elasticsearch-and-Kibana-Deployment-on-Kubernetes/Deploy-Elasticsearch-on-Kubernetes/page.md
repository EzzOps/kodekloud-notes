# Deploy Elasticsearch on Kubernetes

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Elasticsearch-and-Kibana-Deployment-on-Kubernetes/Deploy-Elasticsearch-on-Kubernetes/page

This article provides a guide for deploying Elasticsearch on a Kubernetes cluster, including setup, configuration, and persistent storage.

Welcome to this comprehensive lesson on deploying Elasticsearch on a Kubernetes cluster. In this guide, you'll learn how to set up the cluster, inspect configuration files, and deploy Elasticsearch with persistent storage.

Let’s get started!

## Pre-deployment Setup

Before deploying the Elasticsearch cluster, execute a few preparatory commands. Start by tainting the control plane, creating a dedicated namespace called "efk", and setting the current context to that namespace. Then, clone the repository and navigate to the Elasticsearch/Kibana folder.

```bash theme={null}
kubectl taint node controlplane node-role.kubernetes.io/control-plane-:NoSchedule
kubectl create namespace efk
kubectl config set-context --current --namespace=efk
