# Homebrew (macOS)
brew install glasskube/tap/glasskube

# Debian/Ubuntu .deb
curl -LO https://releases.d1.glasskube.dev/glasskube_v0.14.0_amd64.deb
sudo dpkg -i glasskube_v0.14.0_amd64.deb

# Fedora/RHEL .rpm
sudo dnf install https://releases.d1.glasskube.dev/glasskube_v0.14.0.rpm

# Nix
nix-shell -p glasskube
```

<Callout icon="lightbulb">
  Before running `glasskube bootstrap`, ensure your `kubeconfig` is pointed to the correct cluster context. Glasskube will install server-side components (the package operator) into the selected context.
</Callout>

Explore the CLI commands:

```bash theme={null}
glasskube help
📦 The next generation Package Manager for Kubernetes 📦
Usage:
  glasskube [command]

Available Commands:
  auto-update    Update autopilot for packages where automatic updates are enabled
  bootstrap      Bootstrap Glasskube in a Kubernetes cluster
  completion     Generate the autocompletion script
  help           Help about any command
  install        Install a package
  version        Show Glasskube and package-operator versions
  # ...additional commands omitted for brevity
```

Bootstrap deploys the server-side package operator and controllers into your cluster:

```bash theme={null}
glasskube bootstrap
```

### Example: checking version before and after bootstrap

Before bootstrapping you may see the package operator is not installed:

```bash theme={null}
glasskube version
Error checking PackageOperator version:
deployments.apps "glasskube-controller-manager" not found

GLASSKUBE
glasskube: v0.17.0
package-operator: not installed
```

After running `glasskube bootstrap` (and allowing installation to complete), re-run:

```bash theme={null}
glasskube version
GLASSKUBE
glasskube: v0.17.0
package-operator: v0.17.0
```

Once bootstrapped, Glasskube is ready to manage packages in the cluster.

## Pros and cons (summary)

Use this quick comparison to evaluate Glasskube for your team:

| Pros                                                                       | Cons                                                                                                |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Multiple client interfaces: CLI, UI, and declarative manifests             | Relies on Helm charts and Kubernetes manifests today; a native config language is still in progress |
| Backend flexibility: public Glasskube repo plus private repositories       | Opinionated configuration may not suit every workflow                                               |
| Simplified package configuration vs. raw Helm charts                       | Newer project: smaller ecosystem and community compared to Helm                                     |
| Good GitOps integration for version control and rollbacks                  | —                                                                                                   |
| Support for automatic updates and package scopes                           | —                                                                                                   |
| Built-in access methods to package frontends reduce ad-hoc port-forwarding | —                                                                                                   |

<Frame>
  <img alt="The image is a comparison chart with a list of pros and cons. The pros include multiple clients and backend flexibility, while the cons mention a lack of native configuration language and a smaller user base." />
</Frame>

## Next steps

* Install the CLI and run `glasskube bootstrap` in a test cluster.
* Try installing a package via the CLI: `glasskube install <package>` and observe the `Package` / `PackageInfo` CRs.
* Experiment with private repositories and a GitOps workflow (store `ClusterPackage` CRs in Git).
* Explore automatic updates and package scopes for multi-tenant scenarios.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm Documentation](https://helm.sh/docs/)
* Glasskube releases and downloads: [https://releases.d1.glasskube.dev/](https://releases.d1.glasskube.dev/)
* General GitOps resources: [https://www.gitops.tech/](https://www.gitops.tech/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/140a6ea0-1539-4d23-9aa6-0d07654a4526/lesson/d3a7578d-b239-48af-bded-d4fe039d4502" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/140a6ea0-1539-4d23-9aa6-0d07654a4526/lesson/4b52c5b3-817b-48d1-8e30-3103a4da690e" />
</CardGroup>


# Helm

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Tooling/Helm/page

Helm packaging and templating for Kubernetes applications, using charts and Go templates to render manifests, manage installs, upgrades and rollbacks, with benefits, limitations and Glasskube integration.

Helm is a popular CLI tool for packaging, templating, and deploying applications on Kubernetes. It packages Kubernetes manifests into charts (reusable bundles of resources) and lets you inject environment-specific values to generate the YAML manifests required for cluster deployment. This abstraction simplifies complex application lifecycle tasks such as install, upgrade, rollback, and dependency management. Many community-maintained charts are discoverable on [Artifact Hub](https://artifacthub.io).

<Frame>
  <img alt="The image is a flowchart showing the process of using the Helm CLI tool to incorporate custom variables and charts, creating Kubernetes manifests, which then lead to version updates." />
</Frame>

## How Helm templating works

Helm’s templating engine uses the Go templating language to produce Kubernetes manifests from templates plus a set of values. Templates contain placeholders (e.g., `{{ .Values.name }}`) that are populated from a `values.yaml` file, additional files passed with `-f`, or inline overrides via `--set`. Template rendering is typically performed client-side by the Helm CLI, producing the YAML that is either displayed (with `helm template`) or submitted to the API server (with `helm install` / `helm upgrade`).

<Frame>
  <img alt="The image is a diagram showing the &#x22;Templating Capabilities&#x22; of the &#x22;Go Templating Language,&#x22; highlighting its attributes such as &#x22;Reusable,&#x22; &#x22;Dynamic values,&#x22; along with challenges like &#x22;Troubleshooting&#x22; and &#x22;Awkward.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Helm templates are evaluated client-side by the Helm CLI (unless using a server-side rendering plugin). Values come from `values.yaml`, from `-f` files, or from `--set` on the command line.
</Callout>

If you are new to Helm and want a structured walkthrough, Mumshad Mannambeth’s course "Helm for Beginners" is a commonly recommended resource.

## Quick example — templating in Helm

Below is a minimal example showing:

* a template file in `templates/deployment.yaml`
* a `values.yaml` file
* commands to render and install the chart

This demonstrates how placeholders are resolved to create a Kubernetes Deployment.

```yaml theme={null}
