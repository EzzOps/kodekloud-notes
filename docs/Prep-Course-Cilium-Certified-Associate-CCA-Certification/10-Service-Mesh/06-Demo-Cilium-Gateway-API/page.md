# from pod on worker1
app1-75c78488c4-hvh9f:~# ping 10.0.2.200 -s 1300
```

Note: Place the `-s` option before the destination IP.

2. On the router capture encrypted traffic to encrypted.pcap:

```bash theme={null}
user1@router:~$ sudo tcpdump -nnvv -i ens38 -w encrypted.pcap
^C
# capture stopped, file encrypted.pcap saved
```

3. Open encrypted.pcap in Wireshark. With Cilium IPsec enabled you should no longer see ICMP or HTTP payloads in cleartext for inter-node pod flows. Instead, you will typically see:

* Encapsulating Security Payload (ESP) frames (the encrypted inner payload).
* Possibly additional encapsulation like VXLAN + ESP depending on Cilium configuration.
* Large frame sizes due to encapsulation overhead.

Example encrypted-frame excerpt:

```text theme={null}
Frame 9: 1448 bytes on wire (11584 bits)
Internet Protocol Version 4, Src: 192.168.211.128, Dst: 192.168.44.128
User Datagram Protocol, Src Port: 51422, Dst Port: 8472
Virtual eXtensible Local Area Network
Internet Protocol Version 4, Src: 10.0.1.124, Dst: 10.0.2.104
Encapsulating Security Payload
  ESP SPI: 0x00000003 (3)
  ESP Sequence: 15
```

You should see ESP where the inner protocol (ICMP/HTTP) is not visible — the payload is encrypted and Wireshark cannot display inner protocol fields.

Why captures show cilium\_host (node) IPs as outer addresses
When Cilium encrypts node-to-node traffic it encapsulates pod IPs inside an outer packet that uses node-local Cilium host addresses. Each node typically has a cilium\_host interface with a /32 address reserved for encapsulation. For example:

```bash theme={null}
user1@worker1:~$ ip addr
4: cilium_host@cilium_net: <...> mtu 1500 ...
    link/ether ee:c1:7f:8d:6b:fe brd ff:ff:ff:ff:ff:ff
    inet 10.0.1.124/32 scope global cilium_host
```

Worker2 will have its own cilium\_host (e.g., 10.0.2.104/32). On the wire you will therefore see outer source/destination addresses set to these host addresses and ESP as the protocol; the inner (encrypted) packet contains the original pod IPs and payload.

Recap and key takeaways

* Before enabling Cilium encryption, router captures show pod payloads (ICMP, HTTP) in cleartext.
* After enabling Cilium IPsec, inter-node traffic is encapsulated and encrypted — Wireshark shows ESP (and possibly VXLAN) and you cannot read the inner ICMP/HTTP payloads from the router capture.
* Cilium uses node-local host interfaces (cilium\_host) for outer addresses; the receiving node decrypts and forwards the inner pod traffic to the destination pod.
* Use IPsec or WireGuard depending on your operational and performance requirements.

Links and references

* Cilium: [https://cilium.io](https://cilium.io)
* IPsec (ESP): [https://en.wikipedia.org/wiki/Encapsulating\_Security\_Payload](https://en.wikipedia.org/wiki/Encapsulating_Security_Payload)
* WireGuard: [https://www.wireguard.com](https://www.wireguard.com)
* Kubernetes: [https://kubernetes.io](https://kubernetes.io)
* Helm: [https://helm.sh](https://helm.sh)
* tcpdump: [https://www.tcpdump.org](https://www.tcpdump.org)
* Wireshark: [https://www.wireshark.org](https://www.wireshark.org)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/31c5a508-842b-4023-b234-bf6ad7dbc967)


# Demo Cilium Gateway API

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Service-Mesh/Demo-Cilium-Gateway-API/page

Guide to enable and configure Cilium Gateway API, install Gateway API CRDs, create Gateway and HTTPRoute resources, deploy demo services, and test routing for multiple host and path backends

This guide shows how to enable Gateway API support in Cilium, install the required Gateway API CRDs, enable the feature in the Cilium Helm chart, and configure a Gateway + HTTPRoute to expose multiple apps (shopping.com and blogger.com) plus a default backend.

<Frame>
  <img alt="A screenshot of the Cilium documentation page titled &#x22;Gateway API Support,&#x22; showing explanatory text about the Gateway API and a list of supported resources. A left-hand navigation menu with other documentation links is also visible." />
</Frame>

## Overview

High-level steps covered:

* Install Gateway API CRDs (use experimental CRDs for full TCP/TLS/UDP support).
* Enable Gateway API in the Cilium Helm values and restart Cilium pods.
* Deploy demo applications and ClusterIP services.
* Create a Gateway resource (Cilium-provided GatewayClass) and a LoadBalancer service for external access.
* Create HTTPRoute resources to route host/path combinations to different backends.
* Test with curl or browser (use /etc/hosts for testing DNS to the gateway IP).

## Prerequisites

Follow the Cilium Gateway API docs for full details: [Cilium Gateway API docs](https://docs.cilium.io/en/stable/gateway-api/).

<Frame>
  <img alt="A screenshot of a Cilium documentation webpage showing a &#x22;Prerequisites&#x22; section that lists configuration requirements and CRDs for the Gateway API, with a left-hand navigation menu and several links. A teal cursor arrow is visible pointing at one of the bullet points." />
</Frame>

Cilium expects the experimental Gateway API CRDs in many environments because they include TCPRoute/TLSRoute/UDPRoute support. Install the experimental release to avoid missing-CRD errors.

Install the experimental Gateway API CRDs (example):

```bash theme={null}
