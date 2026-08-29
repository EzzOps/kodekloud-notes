# (enter token at the prompt)
✔ package repository kodekloud-packages added
```

Creating a GitHub personal access token

1. In GitHub, go to Settings → Developer settings → `Personal access tokens`.
2. Create a token with the minimum scope required (prefer repository-read access or fine-grained tokens scoped to the packages repository).
3. Use that token with `--token` or enter it interactively when prompted.

<Frame>
  <img alt="The image shows a GitHub page for creating a new personal access token, with options to set a note, expiration date, and select access scopes." />
</Frame>

After adding a private repository with valid credentials, `glasskube repo list` will include the `AUTH` column and show the detected package count:

```bash theme={null}
~ glasskube repo list
NAME                 URL                                                           AUTH    STATUS  MESSAGE
glasskube            https://packages.d1.glasskube.dev/packages                      none    Ready   repo has 20 packages
kodekloud-packages   https://raw.githubusercontent.com/jakepage91/kodekloud-packages/main/packages/index.yaml  bearer  Ready   repo has 6 packages
```

Installation selection and workflows
Once multiple repositories are configured, you can explicitly choose which repository to install a package from in the Glasskube UI or specify it via CLI. This supports workflows such as installing a package from a staging repository for testing before promoting it to the production registry.

Summary
Glasskube's multi-repository support gives you the flexibility to:

* Aggregate public and private package sources,
* Segregate dev/test/staging registries,
* Implement team or org-level package governance,
* Promote packages between repositories as part of your release workflows.

Try adding a public and a private repository to see package discovery, authorization behavior, and the UI repository selector in action.

<Callout icon="warning">
  Always protect access tokens and follow least-privilege principles. Prefer fine-grained tokens or repository-scoped access when possible, and avoid embedding tokens in shared scripts or version control.
</Callout>

Links and references

* Glasskube documentation: [https://docs.glasskube.dev/](https://docs.glasskube.dev/) (if available)
* GitHub: Creating a personal access token — [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/e651aa8d-8cb5-4d5c-ab54-c5e732ff9c21/lesson/8e389855-3f6b-49aa-80e9-f9490b659855" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/e651aa8d-8cb5-4d5c-ab54-c5e732ff9c21/lesson/93b42842-ad9c-424e-957d-8ae252726d58" />
</CardGroup>


# Section Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Lifecycle-Management-with-Glasskube/Section-Introduction/page

Describes Glasskube's lifecycle management for Kubernetes packages using continuous reconciliation, status reporting, testing, multi-repo workflows, and safe update and rollback processes

This article introduces lifecycle management in Glasskube and how it modernizes package management for Kubernetes. Glasskube shifts package management from a one-time install model to a continuous, observable, and testable lifecycle. That means installing a package is only the beginning — Glasskube enforces desired state, reports health, and helps you safely evolve workloads over time.

Before Glasskube, most Kubernetes package managers emphasized initial installation and provided limited post-install management. Communication was largely one-way: you applied a package and, if something degraded, recovery usually required manual steps, scripts, or operator intervention. This model made it difficult to maintain consistent cluster state, detect drift, or validate changes before promoting them to production.

Glasskube uses continuous reconciliation and status reporting to create a two-way management channel between server and client components. That architecture enables:

* Ongoing enforcement of a package’s desired state (so declared intent matches cluster reality).
* Clear visibility into package health and degradation.
* Safe promotion workflows with built-in testing hooks to reduce risk.
* Multi-repo workflows to organize packages across environments and teams.

<Callout icon="lightbulb">
  Glasskube provides continuous reconciliation and status reporting to ensure packages remain in their intended state. This enables automated healing, clear status visibility, and safer promotion paths from testing to production.
</Callout>

<Frame>
  <img alt="The image is a section overview with points about &#x22;Lifecycle Management&#x22; and &#x22;Multi-Repo Feature,&#x22; including tasks like updating, configuration changes, deleting, and testing." />
</Frame>

Key Glasskube capabilities at a glance:

| Capability                | What it does                                                                                    | Why it matters                                             |
| ------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Continuous reconciliation | Monitors declared package manifests and reconciles cluster state to match desired configuration | Prevents drift and automates remediation                   |
| Status reporting          | Surfaces package health, degraded conditions, and lifecycle events                              | Makes troubleshooting faster and more transparent          |
| Testing & validation      | Provides pre-promotion tests and checks before changes go to production                         | Reduces risk from configuration or version changes         |
| Multi-repo support        | Enables separation of packages across repos for environments, teams, or stages                  | Improves organization, access control, and CI/CD workflows |
| Update & rollback         | Supports controlled upgrades and rollbacks based on observed state                              | Facilitates safe change management                         |

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [GitOps principles and practices](https://www.gitops.tech/)
* [Kubernetes Operators (concepts)](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/e651aa8d-8cb5-4d5c-ab54-c5e732ff9c21/lesson/128115d4-ceed-424a-819e-620f9a63cbca" />
</CardGroup>
