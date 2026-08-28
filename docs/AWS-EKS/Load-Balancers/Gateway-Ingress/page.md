# Gateway Ingress

Source: https://notes.kodekloud.com/docs/AWS-EKS/Load-Balancers/Gateway-Ingress/page

This article compares Kubernetes Ingress with the Gateway API, highlighting their features, architectures, and traffic management options.

Ingress Resources in Kubernetes manage L7 traffic, but the new Gateway API delivers more extensibility and team isolation. In this article, we compare classic Ingress (NGINX, AWS ALB) with the emerging Gateway API, service meshes, and AWS Lattice. We preserve the sequence of diagrams to illustrate each architecture.

## Table of Contents

* [What Is Kubernetes Ingress?](#what-is-kubernetes-ingress)
* [NGINX Ingress Controller Architecture](#nginx-ingress-controller-architecture)
* [AWS Load Balancer Controller](#aws-load-balancer-controller)
* [Alternative Ingress Controllers & Service Meshes](#alternative-ingress-controllers--service-meshes)
* [AWS Lattice: Gateway API Implementation](#aws-lattice-gateway-api-implementation)
* [Comparison of Traffic Management Options](#comparison-of-traffic-management-options)
* [References](#references)

## What Is Kubernetes Ingress?

An **Ingress** is a native Kubernetes API object (`networking.k8s.io/v1`) that defines rules for routing external HTTP(S) traffic to Services inside the cluster. While stable since Kubernetes v1.19, Ingress has limitations:

* Limited API extensibility for multi-team environments
* Controller-specific annotations for advanced L7 features
* One-to-one mapping between Ingress and external load balancers (in some providers)

The newer [Gateway API](https://gateway-api.sigs.k8s.io/) addresses these gaps by offering:

* Role-based resource split: Gateways, Listeners, Routes
* Fine-grained control for teams and operators
* Extended protocol support beyond HTTP(S)

## NGINX Ingress Controller Architecture

Here’s how a typical NGINX-based Ingress controller routes external traffic within a two-node cluster:

```yaml theme={null}
