# application 'sealed-secrets' created
```

3. Install the `kubeseal` client locally (example using a release binary):

```bash theme={null}
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-linux-amd64 -O kubeseal && \
  sudo install -m 755 kubeseal /usr/local/bin/kubeseal
# kubeseal installed to /usr/local/bin/kubeseal
```

4. Create the SealedSecret YAML by running `kubeseal`. If `kubeseal` can reach the Sealed Secrets controller, it will fetch the controller’s public certificate automatically. You can also provide the certificate file using `--cert`:

```bash theme={null}
kubeseal -o yaml --scope cluster-wide --cert sealedSecret.crt < mysql-password_k8s-secret.yaml > mysql-password_sealed-secret.yaml
```

<Callout icon="lightbulb">
  If you omit `--cert`, `kubeseal` will try to fetch the controller's public certificate from the cluster. Use `--cert` when you cannot reach the cluster API from your local environment or when you want to ensure reproducible encryption using a specific certificate.
</Callout>

5. Commit the generated `mysql-password_sealed-secret.yaml` to your Git repository. Any GitOps operator (ArgoCD, Flux, etc.) can sync the manifest to the cluster.

6. At deploy time the Sealed Secrets controller running in the target cluster decrypts the SealedSecret and creates a native Kubernetes Secret in the cluster namespace. From the application pod’s perspective, this is a normal Secret and is consumed in the usual way (environment variables, volumes, etc.).

## Why this is secure

* SealedSecret objects are encrypted using the controller’s public key; only the controller’s private key (stored inside the cluster) can decrypt them.
* Storing SealedSecrets in Git is safe—even in public repositories—because the ciphertext cannot be converted back to plaintext without the controller’s private key.
* Application pods are unaware of the encryption step: they receive native Kubernetes Secrets at runtime exactly as they would with any conventional Secret.

## Best practices

* Keep the Sealed Secrets controller private key secure and limit access to the cluster control plane.
* Use `--cert` for reproducible encryption when working from CI/CD runners that cannot access the cluster API.
* Rotate the controller keys periodically and plan for re-sealing Secrets if keys are rotated or compromised.
* Use RBAC and network policies to limit who can create SealedSecrets and who can access Secrets in the cluster.

## Summary

Bitnami Sealed Secrets offers a simple, Git-friendly method for managing Kubernetes Secrets using asymmetric encryption. Use `kubeseal` to produce SealedSecret manifests, store those manifests in Git, and let your GitOps operator and the Sealed Secrets controller handle decryption and provisioning within the cluster.

## Links and references

* Bitnami Sealed Secrets GitHub: [https://github.com/bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)
* kubeseal releases: [https://github.com/bitnami-labs/sealed-secrets/releases](https://github.com/bitnami-labs/sealed-secrets/releases)
* ArgoCD: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Kubernetes Secrets: [https://kubernetes.io/docs/concepts/configuration/secret/](https://kubernetes.io/docs/concepts/configuration/secret/)
* SOPS: [https://github.com/mozilla/sops](https://github.com/mozilla/sops)
* HashiCorp Vault: [https://www.vaultproject.io/](https://www.vaultproject.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/b5f617f3-f436-4f3d-87a0-e4971d42b0da" />
</CardGroup>


# Blue Green vs Canary vs AB vs Shadow

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Blue-Green-vs-Canary-vs-AB-vs-Shadow/page

Comparison of deployment strategies Blue-Green, Canary, A/B testing, and traffic shadowing to guide risk-aware software releases and validation

This guide compares four common deployment and release strategies—Blue-Green, Canary, A/B testing, and Traffic Shadowing (mirroring)—so you can pick the right approach to release software with minimal risk. Each technique has trade-offs in complexity, resource usage, rollback speed, and the type of feedback you can collect during a rollout. Use the sections below to match a strategy to your risk tolerance, observability maturity, and infrastructure constraints.

## Blue-Green Deployment

Blue-Green deployment maintains two identical production environments: one active (blue) and one idle (green). Deploy the new version to the idle environment, test it, then switch live traffic to it via a load balancer or routing layer. If something fails, the switch can be reversed immediately to restore the previous environment.

<Frame>
  <img alt="The image depicts a schematic of a blue/green deployment strategy, illustrating traffic switching between two versions, v1 and v2, via a load balancer." />
</Frame>

Key benefits:

* Near-zero downtime cutover.
* Fast, reliable rollback by switching back to the previous environment.
* Validation occurs before serving all traffic.

Considerations:

* Requires duplicate infrastructure for both environments.
* Less granular real-time feedback compared to progressive rollouts.

<Frame>
  <img alt="The image is a diagram illustrating a Blue/Green deployment strategy with a rollback mechanism, showing a user and two versions (v1 and v2) connected through a load balancer." />
</Frame>

## Canary Deployment

Canary deployments introduce a new version alongside the stable version and route a small percentage of traffic to it. The percentage increases gradually (for example, 5% → 25% → 50% → 100%) as automated health checks and business metrics validate the release. If problems arise, you reduce the canary weight back to zero or remove it.

<Frame>
  <img alt="The image is a diagram illustrating a canary deployment strategy, where 90% of traffic is directed to version 1 (v1) and 10% to version 2 (v2) of a service." />
</Frame>

Why use Canary:

* Limits blast radius by exposing a subset of users to changes.
* Provides continuous, real-user feedback during rollout.
* Can be automated with monitoring gates, enabling safe promotions or automated rollbacks.

Trade-offs:

* Requires more complex traffic routing and automation.
* Needs strong observability (metrics, logs, traces) and often feature-flag integration.

## Comparing Blue-Green and Canary

Below is a practical comparison to help you decide which approach matches your needs.

<Frame>
  <img alt="The image is a comparison table between Blue/Green Deployment and Canary Deployment, highlighting features such as primary goal, environment, traffic split, rollback, complexity, feedback loop, risk reduction, resource usage, and suitability for different applications." />
</Frame>

Comparison table:

| Characteristic  |                                            Blue-Green |                                                 Canary |
| --------------- | ----------------------------------------------------: | -----------------------------------------------------: |
| Primary goal    |                 Fast, atomic switch for full releases |                    Progressive exposure to reduce risk |
| Environments    |                      Two full, identical environments |  Same environment with mixed versions or separate pods |
| Traffic pattern |                                    All at once switch |          Gradual traffic shift (e.g., 5% → 25% → 100%) |
| Rollback speed  |                             Instant by switching back |         Decrease canary traffic to 0% or remove canary |
| Complexity      |                     Lower (but needs duplicate infra) |                    Higher (routing, automation, gates) |
| Resource usage  |                                High (duplicate infra) |                          More efficient during rollout |
| Feedback type   |                                Pre-cutover validation |                   Real-time user metrics and telemetry |
| Best when       | You can afford duplicate infra and need fast rollback | You want limited blast radius and robust observability |

<Frame>
  <img alt="The image is a comparison chart between Blue/Green Deployment and Canary Deployment, highlighting their differences in features such as primary goal, environment, traffic split, rollback, complexity, feedback loop, risk reduction, resource usage, and best use cases." />
</Frame>

Which to choose:

* Blue-Green: Use when you need a straightforward, reliable full-environment rollback and can allocate duplicate infrastructure.
* Canary: Use when you want to minimize blast radius, capture real-user signals, and have automation to promote/rollback releases.

<Callout icon="lightbulb">
  Choose the strategy that matches your risk tolerance, monitoring maturity, and infrastructure constraints. Canary requires robust automation and observability, while Blue-Green requires duplicate environments.
</Callout>

## Progressive Delivery, Feature Flags, A/B Testing, and Shadowing

Progressive Delivery combines multiple techniques—Canary releases, feature flags, traffic shifting, and automated validation gates—to expose changes gradually and safely. It focuses on continuous delivery with guardrails that minimize production risk.

* Canary releases: Incrementally increase exposure to the new version while checking health and business metrics.
* Feature flags: Toggle features at runtime so you can decouple code deploys from feature releases and instantly disable problematic features.
* A/B testing: Route traffic between variants to measure user behavior, conversion, or engagement and choose the best-performing variant based on data.
* Traffic mirroring / shadowing: Duplicate live production traffic to a shadow environment that processes requests for validation; responses are discarded so users are unaffected. When implementing shadowing, ensure side effects (writes, external calls) are suppressed or mocked so validation does not modify production data.

<Frame>
  <img alt="The image is a diagram titled &#x22;Progressive Delivery&#x22; featuring four concepts: Canary Deployment, Feature Flags, A/B Testing, and Traffic Mirroring. Each concept is represented in separate blue-green gradient rectangles with icons." />
</Frame>

<Callout icon="warning">
  When using traffic mirroring / shadowing, ensure shadow instances do not perform destructive operations or call external systems that modify data. Mock or suppress side effects to prevent impacting production systems.
</Callout>

Practical combos:

* Feature flags + Canary: Use flags to enable new behaviors for the canary cohort before promoting globally.
* A/B testing + Feature flags: Implement variants behind flags and use experimentation platforms to measure outcome metrics.
* Shadowing + Canary: Validate performance and side effects in shadow environments, then run a canary to validate user-facing behavior.

## Summary

* Blue-Green: Fast full-environment switch, simple rollback, higher infrastructure cost.
* Canary: Gradual exposure with a lower blast radius; requires automation and strong observability.
* Feature Flags: Fine-grained control over who sees features; enables instant rollback at feature level.
* A/B Testing: Data-driven decisions by comparing user metrics across variants.
* Traffic Shadowing: Validate under real load without affecting users—careful handling of side effects is essential.

Select one approach or a combination based on your application's acceptable risk, resource availability, and the maturity of your monitoring and automation tooling.

Links and references

* [Kubernetes: What is a Deployment?](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [Progressive Delivery (article)](https://landing.google.com/sre/sre-book/chapters/progressive-delivery/)
* [Feature flagging primer (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)
* [Canary Releases (best practices)](https://cloud.google.com/architecture/canary-deployments)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/c602b9e0-b374-4452-97b8-c3a09c77e527" />
</CardGroup>
