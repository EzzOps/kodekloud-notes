# output: password123
```

If these YAML files land in a public or team-wide repository, **anyone** with read permissions can retrieve your database credentials in seconds.

## How Sealed Secrets protect your credentials

Sealed Secrets let you store **encrypted** secrets safely in Git. You generate a SealedSecret that only your Kubernetes cluster can decrypt:

1. Install the Sealed Secrets controller in your cluster.
2. Seal your plain-Secret using the controller’s `kubeseal` CLI.
3. Commit the resulting `SealedSecret` resource to Git.

At runtime, the controller automatically decrypts the sealed payload and creates a native `Secret` inside the cluster—no one else can reverse-engineer it from your repo.

## Key benefits

| Feature                  | Benefit                                          |
| ------------------------ | ------------------------------------------------ |
| End-to-end encryption    | Secrets remain encrypted at rest in Git          |
| GitOps-friendly workflow | Manage sealed resources alongside your manifests |
| Cluster-bound decryption | Only your cluster’s controller can unseal them   |

## References

* [Sealed Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [GitOps with Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets#usage)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes/module/0f3ed562-f151-48f9-bb8c-8d3a4dbb4fc3/lesson/53d78662-3e7a-4fe7-9145-84a6bc0d90b8" />
</CardGroup>


# Conclusion

Source: https://notes.kodekloud.com/docs/Introduction-to-Sealed-Secrets-in-Kubernetes/Conclusion/Conclusion/page

This guide demonstrates managing secrets in Kubernetes using Sealed Secrets, covering installation, secret creation, and secure distribution practices.

In this guide, we demonstrated how to manage secrets in Kubernetes using Sealed Secrets. We walked through installing the Sealed Secrets controller, creating and encrypting secret manifests, and applying best practices for distributing sensitive data safely across clusters.

## Key takeaways

| Step                | Description                                              |
| ------------------- | -------------------------------------------------------- |
| Installation        | Deployed the Sealed Secrets controller via Helm or YAML. |
| Secret generation   | Created and encrypted Kubernetes Secret manifests.       |
| Secure distribution | Applied sealed manifests to multiple clusters reliably.  |

Looking ahead, you can explore other secret-management solutions to fit your organization’s needs:

* [HashiCorp Vault](https://www.vaultproject.io/)
* AWS native services: [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), [AWS KMS](https://aws.amazon.com/kms/)
* [Azure Key Vault](https://azure.microsoft.com/services/key-vault/)
* [Google Cloud KMS](https://cloud.google.com/kms)

<Callout icon="lightbulb">
  Stay tuned for our upcoming articles, where we'll dive deeper into these tools and help you choose the best secret-management solution for your environment.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes/module/98693b4f-e95e-4c07-a237-eaa630149b52/lesson/6a08a5b7-d15d-4c5b-9920-eecf45dd4eeb" />
</CardGroup>
