# How Do We Set All of this Up

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Vault-Replication/How-Do-We-Set-All-of-this-Up/page

This article explains how to set up Disaster Recovery replication in HashiCorp Vault through a series of configuration steps.

Disaster Recovery (DR) replication in HashiCorp Vault isn’t enabled by default. Follow these four steps to set up a DR replica set:

1. Enable DR replication on the primary cluster
2. Generate a wrapped secondary token
3. *(Optional)* Inspect the token’s contents
4. Activate DR replication on the secondary cluster

***

## 1. Enable DR Replication on the Primary Cluster

On your primary Vault cluster, enable DR replication. Vault will automatically:

* Provision an internal root CA
* Issue a root certificate and a client certificate for mutual TLS
* Prepare to generate secondary tokens

<Callout icon="lightbulb">
  These internal certificates are separate from the TLS certificates you configure for your Vault listener.
</Callout>

<Frame>
  ![The image is a slide about activating DR replication in Vault, detailing the need to enable replication on each cluster, the creation of a root certificate, and the use of mutual TLS connections. It also mentions potential issues with load balancers terminating TLS.](https://kodekloud.com/kk-media/image/upload/v1752878274/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-How-Do-We-Set-All-of-this-Up/dr-replication-vault-activation-slide.jpg)
</Frame>

<Callout icon="triangle-alert">
  If your Vault nodes sit behind a load balancer that terminates TLS, ensure mTLS traffic on port 8201 is passed through end-to-end. Either disable TLS termination or configure a TCP passthrough.
</Callout>

```bash theme={null}
