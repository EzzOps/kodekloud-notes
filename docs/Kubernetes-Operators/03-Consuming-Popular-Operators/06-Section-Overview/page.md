# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Consuming-Popular-Operators/Section-Overview/page

Guide to consuming cert-manager and Prometheus operators, explaining CRs, workflows, resource ownership, and operational checklist for integrating operators into Kubernetes platforms

You’ve spent most of this course building an operator. In this section you switch roles: instead of authoring controllers, you learn to consume operators that platform or shared teams install and operate.

This shift matters. On real platforms, shared controllers (operators) are frequently installed long before individual teams write their own. Knowing how to consume and integrate these operators is essential for building reliable, maintainable systems on Kubernetes.

Two concrete, widely used examples are covered here:

* cert-manager: exposes Kubernetes APIs such as `Issuer`, `Certificate`, and `CertificateRequest`. Instead of creating TLS Secrets by hand, you declare a `Certificate` and cert-manager reconciles it into a Kubernetes `Secret` that applications consume.
* Prometheus Operator: provides custom resources for running Prometheus and for selecting scrape targets. A `ServiceMonitor` lets teams describe which services Prometheus should scrape without editing Prometheus’ config directly.

This section explains each operator’s resource model and demonstrates the typical workflow from the operator’s custom resources to the Kubernetes primitives your workloads consume. It also includes a lab combining both operators in the same cluster so you can reason about ownership boundaries—who owns certificates, who owns monitoring, and what your application resources should request or consume.

<Frame>
  <img alt="The image is a diagram illustrating how each operator, &#x22;cert-manager&#x22; and &#x22;Prometheus operator,&#x22; manages its respective lifecycle (certificate and monitoring), providing results that are consumed by an application." />
</Frame>

cert-manager in brief:

* Primary CRs: `Issuer` / `ClusterIssuer`, `Certificate`, `CertificateRequest`
* Outcome: Kubernetes `Secret` containing TLS material
* Common issuers: ACME (Let's Encrypt), HashiCorp Vault, Venafi, self-signed

Prometheus Operator in brief:

* Primary CRs: `Prometheus`, `ServiceMonitor`, `PodMonitor`, `Alertmanager`
* Outcome: Managed Prometheus instances with targets discovered via `ServiceMonitor`/`PodMonitor`
* Benefit: Teams describe scrape targets declaratively without changing Prometheus config directly

Table — Key resources and their purpose

|                   Resource | Purpose                                                  | Typical consumer            |
| -------------------------: | -------------------------------------------------------- | --------------------------- |
| `Issuer` / `ClusterIssuer` | Configure a certificate authority for signing            | cert-manager controller     |
|              `Certificate` | Declarative TLS request that becomes a `Secret`          | Applications needing TLS    |
|       `CertificateRequest` | Low-level request used by cert-manager for issuance flow | cert-manager and CAs        |
|               `Prometheus` | Deploys a Prometheus server (managed)                    | Platform operators          |
|           `ServiceMonitor` | Selects services to scrape and configures scraping       | Prometheus Operator         |
|                   `Secret` | Stores TLS key/cert and other secrets                    | Application pods, ingresses |

> **lightbulb** Key learning outcomes: Understand cert-manager’s Issuer → Certificate → Secret flow, learn how ServiceMonitor integrates services with Prometheus, and develop the habit of evaluating operator ownership boundaries before consuming resources.

When consuming operators, ask operational questions up front. These affect security, availability, and upgrade paths:

* What CRDs does the operator install? (names, versions)
* Which namespaces does it watch? (single-namespace, multi-namespace, cluster-scoped)
* What RBAC permissions does it require? (cluster roles, service accounts)
* What happens when a custom resource is deleted? (finalizers, leftover Secrets)
* How are upgrades handled? (CRD versioning, migration rules, operator lifecycle)

Table — Operator checklist: what to check and where to look

| Question                       | Why it matters                          | Where to look                                         |
| ------------------------------ | --------------------------------------- | ----------------------------------------------------- |
| What CRDs are installed?       | Compatibility & API stability           | `kubectl get crds` and operator Helm/manifest         |
| Which namespaces are watched?  | Multi-tenant isolation & scoping        | Operator docs, deployment args (e.g., `--namespace=`) |
| What permissions are required? | Least-privilege & security audits       | RBAC manifests (ClusterRole/RoleBinding)              |
| Deletion behavior              | Resource cleanup and secret ownership   | Look for `finalizers` and docs on resource lifecycle  |
| Upgrade strategy               | Safe operator upgrades & CRD migrations | Release notes, CRD versioning docs, migration guides  |

<Frame>
  <img alt="The image outlines considerations for noticing any operator, including CRDs installation, namespaces watched, required permissions, deletion impact, and upgrade handling. It concludes with a message about consuming operators responsibly." />
</Frame>

> **warning** Before granting an operator broad cluster permissions or creating cluster-scoped CRs, confirm ownership and lifecycle expectations. Operators that own Secrets or Service configurations can impact many teams when misconfigured or upgraded.

What’s next

* The following sections take a closer look at cert-manager (Issuer → Certificate → Secret) and the Prometheus Operator (Prometheus → ServiceMonitor → scrape targets), with examples and a lab that installs both operators in one cluster. That lab emphasizes reasoning about ownership: cert-manager owns certificate lifecycle, Prometheus Operator owns monitoring lifecycle, and your application resources consume their outputs.

Links & References

* [cert-manager documentation](https://cert-manager.io/docs/)
* [Prometheus Operator (kube-prometheus) documentation](https://github.com/prometheus-operator/prometheus-operator)
* [Kubernetes CRD concepts](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/b5e6237b-c98e-4357-b26a-f18c583af395/lesson/a1f2c723-dce0-457a-8aec-de1ecf308af4)
