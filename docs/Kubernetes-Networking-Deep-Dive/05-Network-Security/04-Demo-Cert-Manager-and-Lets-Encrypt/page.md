# Forwarding from 0.0.0.0:12000 -> 8081
# Forwarding from [::]:12000 -> 8081
```

Then browse to [http://localhost:12000](http://localhost:12000).

### Hubble CLI

The Hubble CLI offers the same visibility in a terminal-friendly format, ideal for automation and scripts.

Check the status inside a Cilium agent pod:

```bash theme={null}
kubectl exec -it -n kube-system cilium-xxxxxx -c cilium-agent -- hubble status
# Healthcheck (via unix:///var/run/cilium/hubble.sock): Ok
# Current/Max Flows: 4,095/4,095 (100.00%)
# Flows/s: 4.72
```

#### Installing the Hubble CLI on Linux

```bash theme={null}
HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
HUBBLE_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then
  HUBBLE_ARCH=arm64
fi

curl -L --fail --remote-name-all \
  https://github.com/cilium/hubble/releases/download/$HUBBLE_VERSION/hubble-linux-${HUBBLE_ARCH}.tar.gz \
  https://github.com/cilium/hubble/releases/download/$HUBBLE_VERSION/hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum

sudo tar xvzf hubble-linux-${HUBBLE_ARCH}.tar.gz -C /usr/local/bin
rm hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum
```

***

Next, we’ll dive into a hands-on demo to see Hubble in action.

## Links and References

* [Cilium Documentation](https://docs.cilium.io/)
* [Hubble on GitHub](https://github.com/cilium/hubble)
* [Prometheus OpenMetrics](https://prometheus.io/docs/instrumenting/exposition_formats/)
* [Grafana Dashboards](https://grafana.com/grafana/dashboards)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5a70ab6c-2094-4bf2-9f49-e441919fc8c2/lesson/327fddb8-40a4-49ca-9a3c-d7a64c065bd8)


# Demo Cert Manager and Lets Encrypt

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Network-Security/Demo-Cert-Manager-and-Lets-Encrypt/page

This tutorial explains how to install Cert-Manager on Kubernetes and secure a Traefik Ingress with an SSL certificate from Let’s Encrypt.

In this tutorial, you’ll learn how to install Cert-Manager on Kubernetes and obtain an SSL certificate from Let’s Encrypt to secure a Traefik Ingress. We’ll walk through:

1. Installing Cert-Manager with Helm
2. Reviewing the sample “whoami” app and existing Ingress
3. Creating a Let’s Encrypt **staging** Issuer
4. Applying the Issuer and validating resources
5. Updating the Ingress to request TLS
6. Verifying the ACME challenge and certificate issuance
7. Creating a Let’s Encrypt **production** Issuer and switching over

***

## 1. Install Cert-Manager

First, ensure you have Helm installed and a Kubernetes context pointing at your control plane.

```bash theme={null}
