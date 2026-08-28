# Demo 1 Service Entries

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-1-Service-Entries/page

Guide to using Istio ServiceEntry and Egress Gateway to control outbound mesh traffic, configure ServiceEntry, Gateway, VirtualService, and verify egress behavior

This guide shows how to use Istio ServiceEntry to control outbound traffic from the mesh and how to route mesh-originating egress through an Istio Egress Gateway. Follow the steps below to:

* Install Istio with `outboundTrafficPolicy` = `REGISTRY_ONLY`.
* Observe behavior before and after automatic sidecar injection.
* Create a ServiceEntry allowing egress to `www.wikipedia.org`.
* Configure an Egress Gateway + DestinationRule + VirtualService to force mesh traffic through the egress gateway.
* Verify traffic and inspect egress gateway logs.

Prerequisites:

* kubectl configured with a cluster
* Permissions to install Istio and create resources
* istioctl available (instructions below)

***

## 1) Install Istio (set outboundTrafficPolicy to REGISTRY\_ONLY)

Download the desired Istio release and add `istioctl` to your PATH:

```bash theme={null}
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.18.2 sh -
export PATH=$PWD/istio-1.18.2/bin:$PATH
which istioctl
