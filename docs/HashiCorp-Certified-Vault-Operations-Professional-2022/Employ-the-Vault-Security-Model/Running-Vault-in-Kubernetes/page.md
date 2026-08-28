# Enable AppRole
vault auth enable approle

# Create a role that issues batch tokens
vault write auth/approle/role/hcvop \
  policies="engineering" \
  token_type="batch" \
  token_ttl="60s"

# Create a role that issues periodic tokens
vault write auth/approle/role/hcvop \
  policies="hcvop" \
  period="72h"
```

* `token_type="batch"` → batch tokens
* `period="72h"` → periodic tokens

***

## Authenticating with a Token

### UI

1. Choose the **Token** auth method.
2. Paste your token and click **Sign In**.

<Frame>
  ![The image shows a login interface for "Vault" where users can authenticate using a token. It includes instructions to log in directly with a token and features a certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878544/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Tokens-Auth-Method/vault-login-interface-token-authentication.jpg)
</Frame>

After signing in, select **Copy Token** from the user menu:

<Frame>
  ![The image shows a screenshot of a Vault interface with a dropdown menu highlighting the "Copy token" option. It includes instructions to "Copy the Token You are Using" and features a Vault certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878545/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Tokens-Auth-Method/vault-interface-copy-token-screenshot.jpg)
</Frame>

### API

Include the token in the `X-Vault-Token` header or as a Bearer token:

```bash theme={null}
curl --header "X-Vault-Token: [VAULT_TOKEN]" \
     --request POST \
     --data '{"apikey":"3230sc$832d"}' \
     https://vault.example.com:8200/v1/secret/data/apikey/splunk

curl --header "Authorization: Bearer [VAULT_TOKEN]" \
     --request GET \
     https://vault.example.com:8200/v1/secret/data/apikey/splunk
```

### CLI

Interactive login (token entry hidden from history):

```bash theme={null}
vault login
# Token (will be hidden): <enter your token>
```

Or pass the token directly (it will appear in your shell history):

```bash theme={null}
vault login [VAULT_TOKEN]
```

<Callout icon="triangle-alert">
  Avoid embedding long-lived tokens in scripts or logs. Use short-lived, renewable tokens and dynamic secrets where possible.
</Callout>

***

## Revoking Tokens

Revoke any token, including root, with:

```bash theme={null}
vault token revoke [VAULT_TOKEN]
```

***

Tokens are Vault’s fundamental authentication mechanism. You now know how to choose the right token type, create periodic/use-limited/orphan tokens, configure auth backends for specific token issuance, and authenticate or revoke tokens. For further reading, explore the [Vault Authentication Methods](https://www.vaultproject.io/docs/auth) guide.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/6904571f-302d-4646-9e9c-e115b5231dc6" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/e034a521-c13c-44cc-8080-34a85853547e" />
</CardGroup>


# Running Vault in Kubernetes

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Employ-the-Vault-Security-Model/Running-Vault-in-Kubernetes/page

This guide explores security implications and best practices for running HashiCorp Vault on Kubernetes platforms.

In this guide, we explore the security implications and best practices for running HashiCorp Vault on Kubernetes platforms like EKS, AKS, GKE, and OpenShift. While Vault’s default security model targets VMs or bare metal, containerized deployments require extra hardening. The easiest way to get started is with the official Helm chart—just provide your custom values and install.

## Deploying with the Official Helm Chart

To install Vault using Helm:

```bash theme={null}
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --values my-vault-values.yaml
```

This chart supports high availability, integrated storage backends, TLS, and more. Customize `my-vault-values.yaml` to enable mlock, non-root execution, and other hardening options.

## TLS End-to-End Encryption

Ensure that all traffic between clients, load balancers, and Vault pods is encrypted with TLS 1.2 or higher. Do **not** terminate TLS at the load balancer; instead, use TLS passthrough so that Vault pods handle the certificate handshake.

<Callout icon="lightbulb">
  Configure your cloud load balancer for TCP passthrough to maintain end-to-end encryption. This prevents cleartext traffic from ever reaching your Vault pods.
</Callout>

<Frame>
  ![The image is a diagram illustrating TLS end-to-end encryption for a load balancer service with vault servers and persistent volume claims. It includes notes on not offloading TLS at the load balancer, ensuring encryption, using trusted CA-signed certificates, and requiring TLS 1.2 or higher.](https://kodekloud.com/kk-media/image/upload/v1752878550/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Running-Vault-in-Kubernetes/tls-end-to-end-encryption-diagram.jpg)
</Frame>

Use certificates signed by a trusted CA, enforce TLS 1.2+, and mount each Vault pod’s certificate and private key via a Kubernetes `Secret` and a `PersistentVolumeClaim`.

<Frame>
  ![The image illustrates a TLS end-to-end encryption setup with a load balancer service and multiple vault servers, emphasizing not offloading TLS at the load balancer and using trusted CA-signed certificates. It also highlights the requirement for TLS 1.2+ and includes persistent volume claims for each node.](https://kodekloud.com/kk-media/image/upload/v1752878551/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Running-Vault-in-Kubernetes/tls-end-to-end-encryption-setup.jpg)
</Frame>

## Disable Core Dumps

Core dumps can inadvertently capture Vault’s in-memory encryption keys. Disable them at the kernel and container levels:

```bash theme={null}
