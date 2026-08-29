# Output:
# root-ca.conf  root-cert.csr  root-cert.pem  root-key.pem
```

***

## Creating Intermediate Certificates

> **lightbulb** It is not recommended to use the root certificate directly for workload authentication. Instead, generate intermediate certificates to enhance security and ease certificate revocation.

Generate the intermediate certificates by running the following command. This creates an intermediate Certificate Authority (CA) for your cluster under the "localcluster" directory. The following files are produced:

* **cluster-ca.csr**: CSR for the intermediate CA.
* **ca-cert.pem**: Certificate for the intermediate CA.
* **ca-chain.pem**: The full certificate chain.

Intermediate input and temporary files are stored in the localcluster directory and later cleaned up.

```bash theme={null}
make -f ./tools/certs/Makefile.selfsigned.mk localcluster-cacerts
```

Sample output:

```bash theme={null}
Generating RSA private key, 4096 bit long modulus
..................................................++
e is 65537 (0x10001)
generating localcluster/cluster-ca.csr
generating localcluster/ca-cert.pem
Signature ok
subject=/O=Istio/CN=Intermediate CA/L=localcluster
Getting CA Private Key
generating localcluster/ca-chain.pem
Intermediate inputs stored in localcluster/
done
rm localcluster/cluster-ca.csr localcluster/intermediate.conf
istiotraining@local ca-certs $ cd localcluster
istiotraining@local localcluster $ lsa
-bash: lsa: command not found
```

***

## Preparing the Cluster for Custom Certificates

Before proceeding, remove any pre-installed Istio resources to avoid conflicts. Delete the Istio system namespace if it exists or start with a fresh cluster. For example:

```bash theme={null}
kubectl delete namespace istio-system
# Example output:
# namespace "istio-system" deleted
```

Optionally, clean up the default namespace by navigating to the samples directory as needed:

```bash theme={null}
cd ..
cd ca-certs
cd ..
./samples/
```

Next, recreate the Istio system namespace and create a secret that stores all your generated certificates. For instance:

```bash theme={null}
kubectl delete namespace istio-system
cd ..
./samples/bookinfo/platform/kube/cleanup.sh
```

The cleanup script removes all related Bookinfo resources:

```bash theme={null}
using NAMESPACE=default
destinationrule.networking.istio.io "details" deleted
destinationrule.networking.istio.io "productpage" deleted
destinationrule.networking.istio.io "ratings" deleted
destinationrule.networking.istio.io "reviews" deleted
virtualservice.networking.istio.io "bookinfo-gateway" deleted
...
```

***

## Installing Istio with Custom Certificates

Reinstall Istio so that the certificate authority loads the certificates and keys from the secret-mounted files. Run the following command:

```bash theme={null}
istioctl install --set profile=demo
```

You will see output confirming that Istio installs the core components, including Istiod, Ingress, and Egress gateways:

```bash theme={null}
This will install the Istio 1.10.3 demo profile with ["Istio core" "Istiod" "Ingress gateways" "Egress gateways"] components into the cluster. Proceed? (y/N) y
✔ Istio core installed
✔ Istiod installed
Processing resources for Egress gateways, Ingress gateways. Waiting for Deployment/istio-system/istio-egressgateway, Deployment/istio-...
```

You can also deploy additional add-ons such as Kiali, Grafana, and Prometheus. For example:

```bash theme={null}
istioctl install --set profile=demo
# Follow prompts and installation confirmations.
...
kubectl apply -f samples/addons
```

If the path "samples/addons" does not exist in your current directory, navigate appropriately:

```bash theme={null}
cd
cd ca-certs
cd ..
kubectl apply -f samples/addons
```

Optionally, deploy the Bookinfo application and apply default traffic rules:

```bash theme={null}
kubectl rollout status deployment/kiali -n istio-system
# Waiting for the Kiali deployment to become ready...
```

***

## Deploying a Policy for Mutual TLS

Enforce a policy so that workloads accept only mutual TLS traffic. Ensure the Bookinfo application is running before applying the policy. After about 15 seconds, verify that the workloads are using the specified certificates:

```bash theme={null}
kubectl exec "$(kubectl get pod -l app=details -o jsonpath='{.items[0].metadata.name}')" -c istio-proxy -- curl -s localhost:9080
```

The sample output below might indicate a connection refusal, which is expected until the policies are fully in place:

```bash theme={null}
144010290259468:error:2000206f:system library:connect:Connection refused:../crypto/bio/b_sock2.c:110:
144010290259468:error:2008a0c1:BIO routines:BIO_connect:error:../crypto/bio/b_sock2.c:111:
command terminated with exit code 1
```

You can check the status of all pods with:

```bash theme={null}
kubectl get pods
```

Sample output when all pods are running:

```bash theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
details-v1-79f77b4b9-tdp8v            2/2     Running   0          50s
productpage-v1-67b467c4c-qrzjk        2/2     Running   0          49s
ratings-v1-b6994bb-mbjzr              2/2     Running   0          49s
reviews-v1-653db7799-dpk5m            2/2     Running   0          50s
reviews-v2-7bf8c9648f-hmrwx           2/2     Running   0          50s
reviews-v3-84779c7bbc-w2gx            2/2     Running   0          49s
```

If the command is run too early, you might see some pods still initializing:

```bash theme={null}
kubectl get pods
```

Alternate sample output:

```bash theme={null}
NAME                              READY   STATUS            RESTARTS   AGE
details-v1-79f774bd9-18nrf6      1/2     Running           0          9s
productpage-v1-6b746746dc-psqbt  1/2     Running           0          9s
ratings-v1-b6994bb9-v9976        0/2     PodInitializing   0          8s
reviews-v1-545db77b95-6s7wk      1/2     Running           0          8s
reviews-v2-fb86c9648f-gcz7g      2/2     Running           0          9s
reviews-v3-84779c7bbc-tbmnd      1/2     Running           0          9s
```

***

## Verifying Certificate Chains

To further validate the configuration, retrieve and inspect the certificate chain from one of your applications (for example, the "details" application) by connecting to the "productpage" service. Because the CA certificate in this example is self-signed, you may see a warning indicating a "self-signed certificate in certificate chain"—this is expected.

The certificate output (truncated for brevity) will appear similar to:

```text theme={null}
-----BEGIN CERTIFICATE-----
MIITCCGgAwIBAgIjAPG5720SBugrMAQGCS... (truncated for brevity)
-----END CERTIFICATE-----

Server certificate
subject=
issuer=O = Istio, CN = Intermediate CA, L = localcluster

Acceptable client certificate CA names
O = Istio, CN = Root CA
```

These certificates can be saved as separate files if necessary. Next, verify that the root certificate used by Istio matches your specified certificate. First, dump the certificate information from your generated root certificate:

```bash theme={null}
openssl x509 -in ca-certs/localcluster/ca-cert.pem -text -noout > /tmp/ca-cert.crt.txt
```

Then, extract the certificate information from the workload traffic:

```bash theme={null}
openssl x509 -in ./proxy-cert-2.pem -text -noout > /tmp/pod-cert-chain-ca.crt.txt
```

Compare the two files:

```bash theme={null}
diff -s /tmp/ca-cert.crt.txt /tmp/pod-cert-chain-ca.crt.txt
```

A message confirming identical files will look like:

```text theme={null}
Files /tmp/ca-cert.crt.txt and /tmp/pod-cert-chain-ca.crt.txt are identical
```

Next, verify the entire certificate chain from the root to the workload certificate:

```bash theme={null}
openssl verify -CAfile <(cat ca-certs/localcluster/ca-cert.pem ca-certs/localcluster/root-cert.pem) ./proxy-cert-1.pem
```

Successful verification outputs:

```bash theme={null}
./proxy-cert-1.pem: OK
```

This confirms that Istio is signing workload certificates using your provided root certificate.

***

This guide has shown how to configure a custom certificate authority within Istio and verify its proper use in your service mesh. For more in-depth information, consider exploring additional resources on [Istio Security](https://istio.io/latest/docs/tasks/security/) and [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/).

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-service-mesh/module/e4a2171d-d190-4dc9-873e-a0dad6d3cb62/lesson/57a83d19-0bcd-471b-ac0d-9070420d9e85)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-service-mesh/module/e4a2171d-d190-4dc9-873e-a0dad6d3cb62/lesson/41f39dd4-0f29-4d3f-9f10-8143bb6fc65d)


# Istio Security Architecture

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Security/Istio-Security-Architecture/page

This article explores Istio's security architecture and its components that ensure secure microservices communication and policy enforcement.

In this lesson, we explore the core principles behind Istio's security architecture and discover how Istio meets the security requirements of microservices applications. Below, we break down the critical components that form a robust and secure service mesh.

## Key Security Components

### Istiod: The Certification Authority

Within Istiod, a dedicated certification authority manages keys and certificates across the Istio environment. This component:

* Validates certificates.
* Approves certificate signing requests (CSRs).

### Envoy Proxy and Istio Agent

When a workload starts, the Envoy proxy requests a certificate and key from the Istio agent. This process ensures that all communications between services are securely encrypted and authenticated from the very start.

### Configuration API Server

The Configuration API Server plays a crucial role by distributing authentication, authorization, and secure naming policies across the service mesh. These policies are pushed to:

* Sidecars.
* Ingress and Egress proxies.

Both these proxy types serve as policy enforcement points, continuously receiving certificates, keys, and current security policies, ensuring that every point in the network enforces robust security checks.

> **lightbulb** The layered enforcement of security policies across all proxies in the service mesh exemplifies the defense-in-depth approach. This strategy ensures that even if one security layer is compromised, additional layers remain to protect the overall system.

## Next Steps

In upcoming lessons, we will dive deeper into each component and examine their interactions within the Istio service mesh. This will help you understand how a comprehensive security strategy is effectively implemented in modern microservices architectures.

## Additional Resources

* [Istio Documentation](https://istio.io/latest/docs/)
* [Microservices Security Strategies](https://example.com/microservices-security)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-service-mesh/module/e4a2171d-d190-4dc9-873e-a0dad6d3cb62/lesson/10ca824d-10b4-4e56-b723-d4b30c75f5a9)
