# id_rsa     -> private key (keep secure)
# id_rsa.pub -> public key (place on server)
```

On each target server, append the public key to `~/.ssh/authorized_keys`:

```bash theme={null}
cat ~/.ssh/authorized_keys
# ssh-rsa AAAAB3NzaC...KhtUBfoTzlBqRV1NThvOo4opzEwRQo1mWx user1
```

Connect using your private key:

```bash theme={null}
ssh -i ~/.ssh/id_rsa user1@server1
# Successfully Logged In!
```

To grant access on multiple servers, copy your public key to each server’s `authorized_keys`. To onboard other users, they generate their own key pairs and provide you with their `.pub` file.

> **lightbulb** Keep your private key (`id_rsa`) out of version control and never share it. If compromised, revoke and generate a new key pair.

## HTTPS Key Exchange Process

Web servers combine asymmetric and symmetric encryption to optimize performance:

1. Server generates an RSA key pair.
2. Client (browser) downloads the server’s public key.
3. Browser generates a random symmetric session key.
4. Browser encrypts the session key with the server’s public key.
5. Server decrypts the session key using its private key.
6. Both sides use the symmetric key for bulk data encryption.

Generate the server’s RSA pair with [OpenSSL](https://www.openssl.org/):

```bash theme={null}
openssl genrsa -out my-bank.key 2048
openssl rsa -in my-bank.key -pubout > my-bank.pem
```

The public key (`my-bank.pem`) is served to clients; the private key (`my-bank.key`) remains secure on the server.

## Digital Certificates and Trust

A self-generated public key provides no identity proof. Digital certificates bind your public key to your domain, signed by a trusted Certificate Authority (CA).

```text theme={null}
Certificate:
    Data:
        Serial Number: 420327018966204255
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN=kubernetes
        Validity
            Not After : Feb  9 13:41:28 2020 GMT
        Subject: CN=my-bank.com
        X509v3 Subject Alternative Name:
            DNS:mybank.com, DNS:i-bank.com,
            DNS:we-bank.com
        Subject Public Key Info:
            00:b9:b0:55:24:fb:a4:ef:77:73:7c:9b
```

Generate a Certificate Signing Request (CSR) and submit it to a CA, such as [DigiCert](https://www.digicert.com/) or [GlobalSign](https://www.globalsign.com/):

```bash theme={null}
openssl req -new -key my-bank.key -out my-bank.csr \
  -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=my-bank.com"
# my-bank.csr → send to CA for signing
```

![The image illustrates the process of obtaining a digital certificate from a Certificate Authority (CA), featuring logos of various CAs and a sample certificate for "MY-BANK.COM." It includes steps like Certificate Signing Request (CSR), information validation, and certificate signing.](https://kodekloud.com/kk-media/image/upload/v1752880880/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Connectivity-TLS-Basics/digital-certificate-process-ca-logos.jpg)

## Browser Trust Chain

Browsers ship with a root store of trusted CA public keys. When presented with your signed certificate, the browser:

1. Verifies the CA signature using the trusted root key.
2. Confirms the certificate’s validity period and domain match.
3. Establishes a secure HTTPS session.

![The image shows a concept of online banking security with a browser displaying a secure website and a digital certificate issued to "my-bank.com" by a certificate authority.](https://kodekloud.com/kk-media/image/upload/v1752880881/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Connectivity-TLS-Basics/online-banking-security-digital-certificate.jpg)

> **lightbulb** For internal applications, consider deploying your own private CA and distributing its root certificate to employee devices.

## Summary

* Symmetric encryption is fast but needs a secure key exchange.
* Asymmetric encryption uses public/private key pairs to exchange secrets safely.
* SSH relies on key pairs for authentication.
* HTTPS uses asymmetric encryption to bootstrap a symmetric session key.
* Digital certificates prove ownership of a public key, validated by CAs.
* Browsers trust certificates based on their embedded root CA list.
* Private CAs work well for internal service authentication.

## Mutual TLS (mTLS)

Mutual TLS adds client certificate authentication, requiring both server and client to present valid certificates during the TLS handshake. This strengthens security for APIs and inter-service communication.

## Key–Lock Analogy Clarification

Although we talk about a “lock” (public key) and a “key” (private key), either key can encrypt or decrypt. Encrypt with one; decrypt with the other. Private-key encryption is commonly used for digital signatures and identity verification.

## Naming Conventions

| File Type   | Extension    | Example      |
| ----------- | ------------ | ------------ |
| Public Cert | .crt or .pem | `server.crt` |
| Private Key | .key or .pem | `server.key` |

Always secure private keys and limit their filesystem permissions.

## References

* [OpenSSL Documentation](https://www.openssl.org/docs/)
* [DigiCert](https://www.digicert.com/)
* [GlobalSign](https://www.globalsign.com/)
* [Kubernetes Security](https://kubernetes.io/docs/concepts/security/overview/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/dee32061-d4e1-4fc8-ba3b-c3630f294225)


# Connectivity TLS Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Connectivity-TLS-Introduction/page

This article introduces TLS certificates and their role in securing communication within Kubernetes clusters, covering fundamentals and specific implementations.

Securing communication in a Kubernetes cluster hinges on a solid understanding of TLS certificates and Certificate Authorities (CAs). Without this foundation, configuring and troubleshooting TLS-related issues can be challenging.

In a recent poll, many participants indicated limited experience with TLS certificates. To address this gap, this lesson series covers both general TLS fundamentals and Kubernetes-specific implementations.

> **lightbulb** This section starts with the basics of public key cryptography and certificate lifecycles. If you’re already familiar with these topics, you can skip ahead to the [Kubernetes-Specific Topics](#kubernetes-specific-topics) further below.

## Goals for TLS Certificate Mastery

![The image is a slide titled "Goals!" listing objectives related to TLS certificates, including understanding, generating, configuring, viewing, and troubleshooting them in the context of Kubernetes.](https://kodekloud.com/kk-media/image/upload/v1752880882/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Connectivity-TLS-Introduction/tls-certificates-goals-kubernetes.jpg)

By the end of this module, you will be able to:

| Objective                                 | Description                                                                |
| ----------------------------------------- | -------------------------------------------------------------------------- |
| Understand TLS certs and CAs              | Explain public/private key pairs, trust chains, and the role of CAs        |
| Generate and configure TLS certificates   | Use tools such as `openssl`, `cfssl`, and Kubernetes resources             |
| Inspect certificate contents and validity | Leverage `openssl x509`, `kubectl get csr`, and certificate metadata       |
| Troubleshoot certificate issues           | Diagnose common TLS handshake failures and misconfigurations in Kubernetes |

## Prerequisites: Core TLS Concepts

![The image is an orange slide with the text "TLS Certificates (Pre-Req)" and an icon of a certificate.](https://kodekloud.com/kk-media/image/upload/v1752880883/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Connectivity-TLS-Introduction/tls-certificates-pre-req-slide.jpg)

Before diving into Kubernetes integrations, make sure you understand:

* **Public Key Cryptography**: Asymmetric key pairs, digital signatures, and encryption.
* **Certificate Authorities (CAs)**: Root vs. intermediate CAs, trust stores, and signing processes.
* **Certificate Lifecycle**: Creation (CSR), issuance, renewal, and revocation.

> **triangle-alert** Ensure that `openssl` (version 1.1 or higher) is installed on your system. Certificate operations in this course rely on OpenSSL commands.

## Kubernetes-Specific Topics

Once you’ve reviewed the TLS fundamentals above, the following Kubernetes-focused lectures will explore:

1. **API Server and kubelet certificates** – How Kubernetes generates and rotates its own certs.
2. **Mutual TLS (mTLS)** – Implementing service-to-service authentication within a cluster.
3. **Cert-Manager integration** – Automating certificate issuance and renewal.
4. **Troubleshooting TLS in real clusters** – Common errors, log analysis, and remediation steps.

## References and Further Reading

* [Kubernetes Security Concepts](https://kubernetes.io/docs/concepts/security/)
* [TLS Protocol Overview (IETF)](https://datatracker.ietf.org/wg/tls/about/)
* [OpenSSL Documentation](https://www.openssl.org/docs/)
* [Cert-Manager](https://cert-manager.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/d37ea1ed-8ec2-4c84-8a49-86cabb952cf0)
