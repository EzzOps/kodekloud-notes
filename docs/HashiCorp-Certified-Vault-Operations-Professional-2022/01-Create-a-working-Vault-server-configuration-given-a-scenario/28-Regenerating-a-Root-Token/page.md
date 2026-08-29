# Enable at default path "pki/"
vault secrets enable pki

# Or enable at custom path "hcvop_int/"
vault secrets enable -path=hcvop_int pki
```

## Tuning the Maximum TTL

Set the maximum lease TTL to enforce certificate lifetimes:

```bash theme={null}
# Default PKI: max TTL = 30 days
vault secrets tune -max-lease-ttl=720h pki

# Custom PKI at "hcvop_int/": max TTL = 1 year
vault secrets tune -max-lease-ttl=8760h hcvop_int
```

***

## Generating and Signing an Intermediate CSR

1. **Generate CSR in Vault** (outputs JSON, extract CSR):

   ```bash theme={null}
   vault write -format=json \
     hcvop_int/intermediate/generate/internal \
     common_name="hcvop.com Intermediate" \
     | jq -r '.data.csr' > pki_intermediate.csr
   ```

2. **Sign CSR** with your offline root CA and save as `intermediate.cert.pem`.

3. **Import the signed certificate** back into Vault:

   ```bash theme={null}
   vault write hcvop_int/intermediate/set-signed \
     certificate=@intermediate.cert.pem
   ```

***

## Configuring CA and CRL URLs

Clients fetch the issuer certificate and CRL via these URLs embedded in issued certs:

```bash theme={null}
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"
```

***

## Defining PKI Roles

A **role** in Vault maps policies to certificate settings (allowed domains, TTLs, SANs).

![The image is an informational slide about PKI roles, explaining the mapping between a policy and configuration in a secrets engine, with notable configurations listed. It includes a Vault certification badge and a cartoon character illustration.](https://kodekloud.com/kk-media/image/upload/v1752878481/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-PKI-Secrets-Engine/pki-roles-policy-configuration-slide.jpg)

### Example Role Configurations

![The image describes unique PKI roles with configurations for web, internal apps, and Kubernetes apps, detailing allowed domains, subdomain permissions, and maximum TTL. It also includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878482/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-PKI-Secrets-Engine/pki-roles-configurations-web-kubernetes.jpg)

| Role Name          | Allowed Domains | Subdomains | Bare Domains | Max TTL |
| ------------------ | --------------- | ---------- | ------------ | ------- |
| **web\_dmz\_role** | dmz.hcvop.com   | ✓          | ✗            | 720h    |
| **internal\_apps** | app.hcvop.com   | ✓          | —            | 24h     |
| **k8s\_apps**      | k8s.hcvop.com   | ✓          | ✗            | 4h      |

***

## Creating a PKI Role

```bash theme={null}
vault write pki/roles/web_dmz_role \
  allowed_domains=dmz.hcvop.com \
  allow_subdomains=true \
  allow_bare_domains=false \
  allow_glob_domains=false \
  max_ttl=720h \
  allow_localhost=true \
  organization=hcvop \
  country=US
```

![The image illustrates a process for creating roles in a Vault system, showing how different PKI roles request certificates for various applications. It includes icons representing Vault, roles, and applications, with a certification badge in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752878483/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-PKI-Secrets-Engine/vault-pki-roles-certificate-process.jpg)

Applications authenticate to Vault and request certificates based on their assigned role.

***

## Issuing Certificates

Issue a certificate for a given role:

```bash theme={null}
vault write pki/issue/web_dmz_role \
  common_name=dmzhcp01.dmz.hcvop.com \
  alt_names=portal.dmz.hcvop.com \
  max_ttl=720h
```

Response fields:

* `certificate`: TLS certificate (PEM)
* `issuing_ca`: CA certificate chain (Vault intermediate)
* `private_key`: Private key (returned **only once**)
* `private_key_type`: Key algorithm (e.g., rsa)
* `serial_number`: Unique cert serial number

> **lightbulb** Always save the `private_key` immediately; Vault does not retain it for later retrieval.

***

## Revoking Certificates

Revoke by serial number:

```bash theme={null}
vault write pki/revoke \
  serial_number="4d:00:01:30:20:2c:5e:31:ba:a9:7b"
```

The response includes revocation time in Unix and [RFC 3339](https://tools.ietf.org/html/rfc3339) formats.

***

## Cleaning Up the Certificate Store

Periodically tidy expired and revoked certificates:

```bash theme={null}
vault write pki/tidy \
  tidy_cert_store=true \
  tidy_revoked_certs=true
```

Vault logs the tidy operation—monitor server logs for completion status.

***

## References

* [Vault PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki)
* [Vault Authentication Methods](https://www.vaultproject.io/docs/auth)
* [X.509 Certificate Profile](https://tools.ietf.org/html/rfc5280)
* [Managing Certificate Revocation List (CRL)](https://tools.ietf.org/html/rfc5280#section-5.1.2.4)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/d4743df6-33f4-4e60-a234-1c657f4ba2e4)


# Regenerating a Root Token

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Regenerating-a-Root-Token/page

This guide explains how to regenerate a root token in HashiCorp Vault when standard authentication methods fail.

When standard authentication methods fail, regenerating a root token grants temporary superuser access. In this guide, you’ll learn what a root token is, how to revoke the initial token, and step-by-step instructions for generating a new one using unseal (recovery) keys.

## What Is a Root Token?

A **root token** is Vault’s superuser credential. It’s bound to the built-in `root` policy—which cannot be modified or deleted—and grants unrestricted access across your Vault cluster.

![The image is an informational slide about root tokens, explaining their unlimited access to Vault, lack of expiration, and guidelines for their use and revocation. It also includes a Vault certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878484/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Regenerating-a-Root-Token/root-tokens-vault-access-guidelines.jpg)

Key characteristics:

| Characteristic              | Description                                         |
| --------------------------- | --------------------------------------------------- |
| No TTL                      | Never expires; valid indefinitely                   |
| Usage scope                 | Only for initial setup or critical emergencies      |
| Immediate revocation needed | Revoke the root token as soon as tasks are complete |
| Immutable                   | Cannot be altered or deleted                        |

## Initial Root Token and Revocation

Immediately after initializing Vault, your only authentication method is the **initial** root token. Once you enable and configure other auth backends (e.g., LDAP, AppRole, Kubernetes) and create policies, revoke this token to minimize risk:

```bash theme={null}
vault token revoke s.dhtIk8VsE3Mj61PuGP3ZfFrg
