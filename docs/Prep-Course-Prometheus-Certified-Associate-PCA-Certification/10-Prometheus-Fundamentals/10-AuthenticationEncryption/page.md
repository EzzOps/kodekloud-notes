# AuthenticationEncryption

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/AuthenticationEncryption/page

How to secure Prometheus scrapes to Node Exporter using TLS encryption and basic authentication, with configuration steps and best practices for testing and production.

In this lesson we cover how to secure Prometheus scrapes of targets (Node Exporter) using authentication and TLS encryption. We'll walk through the end-to-end steps so that:

* only authorized clients (Prometheus) can scrape metrics (authentication), and
* network traffic is protected from packet sniffers (TLS encryption).

By default, Prometheus can scrape a Node Exporter endpoint without any authentication or encryption. That means anyone who can reach the endpoint can read metrics. Adding authentication restricts access, while TLS prevents eavesdroppers from reading the data, and protects against certain active attacks when properly validated.

> **lightbulb** This guide shows a practical self-signed example for testing and the recommended approach for production—use CA-signed certificates (or a public CA like Let's Encrypt) and keep TLS verification enabled.

<Frame>
  <img alt="The image illustrates a network security diagram showing the process of authentication and encryption between nodes, highlighting security elements like firewalls, user authentication, and data encryption." />
</Frame>

Below are the steps and example configurations to enable TLS + basic auth for Node Exporter and to configure Prometheus to scrape it securely.

## 1) Generate TLS certificate and key for the target (Node Exporter)

For testing you can generate a self-signed cert with OpenSSL. In production, use your organization CA or Let's Encrypt. Make sure the certificate's Common Name (CN) and/or subjectAltName (SAN) includes the hostname or IP address Prometheus will use to reach the Node Exporter (for example `node` or `node.example.com`), otherwise TLS name validation will fail.

Example OpenSSL command (run on the target host):

```bash theme={null}
sudo openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
  -keyout node_exporter.key \
  -out node_exporter.crt \
  -subj "/C=US/ST=California/L=Oakland/O=MyOrg/CN=node" \
  -addext "subjectAltName = DNS:node"
```

This produces `node_exporter.key` and `node_exporter.crt`.

Example listing after generation:

```bash theme={null}
$ ls -l
-rw-r--r-- 1 user2 user2  11357 Dec  5  2021 LICENSE
-rwxr-xr-x 1 user2 user2 18228926 Dec  5  2021 node_exporter
-rw-r--r-- 1 root  root    1326 Sep  5 18:04 node_exporter.crt
-r-------- 1 root  root    1700 Sep  5 18:04 node_exporter.key
```

## 2) Create a Node Exporter web config (TLS + optional basic auth users)

Create a YAML web config for Node Exporter and store it next to the certificate and key (or use absolute paths). Minimal TLS configuration:

```yaml theme={null}
