# Demo Configure a backend service based external load balancer

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Networking-for-GKE-clusters/Demo-Configure-a-backend-service-based-external-load-balancer/page

This guide explains how to set up a backend service–based external load balancer on Google Kubernetes Engine.

In this guide, you will learn how to set up a backend service–based external (Layer 4) load balancer on Google Kubernetes Engine (GKE). We’ll walk through configuring your gcloud defaults, creating a GKE cluster with HTTP load balancing, deploying an echo server, exposing it via an annotated Service, and verifying traffic distribution across Pods.

## Table of Contents

1. [Set the Default Region and Zone](#1-set-the-default-region-and-zone)
2. [Create the GKE Cluster](#2-create-the-gke-cluster)
3. [Prepare the Deployment Manifest](#3-prepare-the-deployment-manifest)
4. [Prepare the Service Manifest](#4-prepare-the-service-manifest)
5. [Deploy the Application and Service](#5-deploy-the-application-and-service)
6. [Verify the External Load Balancer](#6-verify-the-external-load-balancer)
7. [Inspect the Service Configuration](#7-inspect-the-service-configuration)
8. [Links and References](#8-links-and-references)

***

## 1. Set the Default Region and Zone

Configure your default compute zone so that all subsequent gcloud commands target **us-west1-a**:

```bash theme={null}
gcloud config set compute/zone us-west1-a
```

## 2. Create the GKE Cluster

Create a cluster named `gke-deep-dive` with HTTP load balancing enabled:

```bash theme={null}
gcloud container clusters create gke-deep-dive \
  --num-nodes=1 \
  --disk-type=pd-standard \
  --disk-size=10 \
  --enable-ip-alias \
  --addons=HttpLoadBalancing
```

This step can take several minutes. Once complete, verify the HTTP load balancing add-on:

```bash theme={null}
gcloud container clusters describe gke-deep-dive \
  --format="yaml(addonsConfig.httpLoadBalancing)"
```

Expected output snippet:

```yaml theme={null}
addonsConfig:
  httpLoadBalancing: {}
```

> **triangle-alert** Creating clusters and load balancers may incur charges on your GCP account. Monitor your billing dashboard or delete resources when you’re done.

## 3. Prepare the Deployment Manifest

Save the following Deployment in `gke-deep-dive-app.yaml`. It launches two replicas of an echo server on port 8080 and configures a readiness probe.

```yaml theme={null}
