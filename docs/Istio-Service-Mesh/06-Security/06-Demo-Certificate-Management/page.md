# Demo Certificate Management

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Security/Demo-Certificate-Management/page

This guide demonstrates configuring Istio to use a custom root certificate for enhanced security and trust in your service mesh.

This guide demonstrates how to configure Istio to use a custom root certificate for your cluster. Follow the steps below to generate your own certificate authority (CA) and integrate it with Istio for enhanced security and trust in your service mesh.

***

## Generating the Root Certificate

Begin by creating a directory for your certificates in the Istio root directory. In this example, we use "ca-certs". Then navigate into the new directory:

```bash theme={null}
mkdir ca-certs
cd ca-certs
```

Generate your root certificate by running the following command. This process creates four files:

* **root-ca.conf**: OpenSSL configuration file used for generating the root certificate.
* **root-cert.csr**: Certificate Signing Request (CSR) for the root certificate.
* **root-cert.pem**: The root certificate.
* **root-key.pem**: The private key associated with the root certificate.

```bash theme={null}
make -f ../tools/certs/Makefile.selfsigned.mk root-ca
```

A sample output may look like this:

```bash theme={null}
istiotraining@local ~/istio-1.10.3 $ mkdir ca-certs
istiotraining@local ~/istio-1.10.3 $ cd ca-certs/
istiotraining@local ca-certs $ make -f ../tools/certs/Makefile.selfsigned.mk root-ca
generating root-key.pem
Generating RSA private key, 4096 bit long modulus
..................................................................................................................++
e is 65537 (0x10001)
generating root-cert.csr
generating root-cert.pem
Signature ok
subject=/O=Istio/CN=Root CA
Getting Private key
istiotraining@local ca-certs $ ls
```

Below is an alternative sample that shows all generated files:

```bash theme={null}
mkdir ca-certs
cd ca-certs/
make -f ./tools/certs/Makefile.selfsigned.mk root-ca
generating root-key.pem
Generating RSA private key, 4096 bit long modulus
............................+++
e is 65537 (0x10001)
generating root-cert.csr
generating root-cert.pem
Signature ok
subject=/O=Istio/CN=Root CA
Getting Private key
ls
