# Demo Working with Health Checks

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Register-Services-and-Use-Service-Discovery/Demo-Working-with-Health-Checks/page

This tutorial covers enhancing a Consul service definition by adding a TCP health check and observing its status.

In this tutorial, we’ll walk through enhancing a Consul service definition by adding a TCP health check. You will learn how to:

* Register a basic Consul service
* Add a TCP health check on port 80
* Observe and interpret the service’s health status in the Consul UI

> **Prerequisites**\
> You need a running Consul agent and an Apache HTTP server on your node.

***

## Registering a Basic Consul Service

First, create a minimal service definition and register it with Consul.

```bash theme={null}
