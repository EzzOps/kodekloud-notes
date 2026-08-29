# Intro to GitOps

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Extending-Package-Management-with-GitOps/Intro-to-GitOps/page

Explains GitOps principles, Argo CD operator, and push versus pull deployment models for declarative, auditable Kubernetes infrastructure and application management.

In this lesson we’ll clarify what GitOps means and outline the common deployment models you’ll encounter when adopting Git as the single source of truth for infrastructure and applications.

GitOps is a paradigm that treats a Git repository as the authoritative, versioned record of the desired state for infrastructure and apps. Changes are made declaratively in Git (via commits and pull requests), and a GitOps operator continuously reconciles the live environment to match that repository. Extending this pattern to package management lets you manage packages the same way you manage application and cluster configuration—declaratively and audibly.

<Frame>
  <img alt="The image features a &#x22;GitOps&#x22; logo with two buttons below labeled &#x22;What is Gitops?&#x22; and &#x22;What are the different deployment models?&#x22; with a copyright notice from KodeKloud." />
</Frame>

How a GitOps workflow typically works:

* You author declarative manifests, Helm charts, or package definitions in a Git repository.
* A GitOps operator (for example Argo CD) watches the repository for commits and PR merges.
* The operator reconciles the target environment (for example a Kubernetes cluster) to match the Git state, applying changes automatically.
* All changes are auditable (logged in Git), and configuration drift is detected and corrected by the operator.

This approach replaces manual kubectl/app deployments with a reproducible, auditable pipeline.

<Frame>
  <img alt="The image features the text &#x22;gitops&#x22; with an associated logo and includes labeled buttons for &#x22;Package Management,&#x22; &#x22;Code Commits,&#x22; and &#x22;Gitops Operator.&#x22;" />
</Frame>

In this lesson we use Argo CD as the GitOps operator. Argo CD runs in-cluster and continuously compares the live state against the Git repository, then applies any necessary changes to reconcile differences. Using Argo CD (or a similar operator) improves consistency, reduces manual interventions, and makes deployments repeatable and auditable.

<Frame>
  <img alt="The image is a diagram of Argo CD, a GitOps operator, highlighting issues like &#x22;Manual Deployment&#x22; and &#x22;Configuration drift&#x22; in red, and benefits like &#x22;Consistency&#x22; in green." />
</Frame>

Two common deployment models:

* Push model: An external system (CI/CD pipeline) detects commits and pushes changes to the target environment. Simpler to bootstrap, but it relies on external triggers and may make auditing and drift detection harder.
* Pull model: A GitOps operator running inside the target environment continuously monitors Git and pulls/apply changes when new commits arrive. This model provides a declarative reconciliation loop, stronger control, and better observability.

<Frame>
  <img alt="The image illustrates a &#x22;Pull Model&#x22; in a code deployment process, showing a user pushing code to a Git repository and an event-watching component pulling updates from the repository." />
</Frame>

Comparison: Push vs Pull

| Aspect              |                           Push model | Pull model                                                 |
| ------------------- | -----------------------------------: | ---------------------------------------------------------- |
| Who applies changes | External CI/CD system pushes updates | In-cluster GitOps operator pulls and applies               |
| Auditability        |             Depends on pipeline logs | Git + operator logs provide clear audit trail              |
| Drift detection     |       Often manual or pipeline-based | Continuous reconciliation detects drift                    |
| Security            |     Requires CI/CD access to cluster | Reduced blast radius—operator runs with scoped permissions |
| Typical fit         |      Non-Kubernetes or simple setups | Kubernetes-centric, production-grade ops                   |

> **lightbulb** For Kubernetes-focused deployments, the pull model (with a GitOps operator like Argo CD) is generally recommended because it provides continuous reconciliation, better audit trails, and reduced operational complexity.

Key takeaways

* Use Git as the central source of truth and protect repository integrity (branch protections, signed commits, PR reviews).
* GitOps enables declarative management of infrastructure, applications, and package definitions.
* The pull model is preferred for Kubernetes environments because it enforces a continuous reconciliation loop and improves reliability.
* Choose the model that matches your operational constraints—simplicity vs. control—and ensure proper RBAC and observability for any operator you run.

References and further reading

* [GitOps](https://gitops.tech/)
* [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)
* [Kubernetes documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/0ddd5879-550c-4c12-82cd-ac19fb487de5/lesson/6919992f-40a7-4a4b-aafa-7e8cdcb5ba6b)
