# Lifecycle Management with Glasskube

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Lifecycle-Management-with-Glasskube/Lifecycle-Management-with-Glasskube/page

Explains Glasskube lifecycle management for Kubernetes packages, including update discovery, auto-updates, manual updates, configuration editing, installation, uninstallation, and full purge.

In this lesson we cover how Glasskube keeps cluster packages healthy and up to date. Installing packages is just the start — upstream releases fix bugs, patch vulnerabilities, and add features. Glasskube provides lifecycle-management features that make it easy to discover, approve, apply, configure, and remove package updates.

What Glasskube provides

* Periodic checks for new package versions in the Glasskube packages repository.
* A Glasskube bot that opens PRs to add discovered new versions to the repository.
* UI notifications and CLI commands to list installed packages and pending updates.
* Optional per-package auto-update that updates installed packages after repository PRs are merged.
* Interactive CLI and UI configuration editors for package values.
* Uninstall and purge commands to remove packages or fully clean a cluster.

Below we walk through the typical lifecycle workflow: checking for updates, enabling auto-updates, applying updates, editing configuration, and uninstalling packages.

How auto-update works (high level)

1. Glasskube periodically checks upstream sources for new package releases.
2. The Glasskube bot opens a PR in the Glasskube packages repository to add the new version.
3. After CI/testing and the PR is merged, Glasskube detects the new repository version.
4. If auto-update is enabled for an installed package, Glasskube updates the installation automatically; otherwise the UI/CLI show that an update is available and you can apply it manually.

Glasskube packages repository and the update bot
All supported package definitions live in the Glasskube packages repository. Each package has a folder containing one or more version directories. A Glasskube bot routinely checks upstream sources for new releases, opens PRs to add them to the repository, and those PRs go through testing before being merged.

<Frame>
  <img alt="This is a screenshot of a GitHub repository page for &#x22;glasskube/packages,&#x22; showing the main branch files and folders, recent commits, and repository details like license and contributors." />
</Frame>

When a PR that adds a new version is merged, Glasskube becomes aware of the new repository version. From there you can either let Glasskube auto-update installed packages (if enabled) or trigger updates manually via the CLI or UI.

<Frame>
  <img alt="The image shows a GitHub page with a list of open pull requests for a project, including details like titles, authors, and timestamps." />
</Frame>

Glasskube UI: discover and act on updates
The Glasskube dashboard lists packages and exposes actions such as Install, Update, and Configure. It highlights available updates and shows whether auto-update is enabled.

<Frame>
  <img alt="The image shows a web interface for a package manager called Glasskube, displaying a list of software packages with options to install or update them. Each package has a brief description and buttons for installation or updating." />
</Frame>

Check installed packages and pending updates (CLI)
Use `glasskube list` to see installed packages, repository versions, and auto-update status. Example output:

```bash theme={null}
$ glasskube list
PACKAGENAME            NAMESPACE     NAME                      VERSION         AUTO-UPDATE   REPOSITORY           STATUS
quickwit               analytics     quickwit                  v0.8.1+5        Enabled       glasskube (used)     Ready

NAME                    VERSION           AUTO-UPDATE   REPOSITORY           STATUS
akri                    N/A               N/A           glasskube            Not installed
argo-cd                 v2.11.7+1         Enabled       glasskube (used)     Ready
caddy-ingress-controller N/A              N/A           glasskube            Not installed
cert-manager            N/A               N/A           glasskube            Not installed
cloudnative-pg          v1.23.2+1         N/A           glasskube (used)     Ready
kube-prometheus-stack   v61.6.0+1         N/A           glasskube            Not installed
kubetail                v0.6.0+1          N/A           glasskube            Not installed
... (other packages follow)
```

The `glasskube list` output shows installed package versions alongside repository availability. In the example above, CloudNativePG is installed at `v1.23.2+1` while a newer repository version exists.

Enable per-package auto-update (CLI)
Enable automatic updates for a package at any time:

```bash theme={null}
$ glasskube auto-update enable kubetail
Enable automatic updates for the following packages:
 * kubetail (ClusterPackage)
Continue? (Y/n) Y
Automatic updates enabled: kubetail
```

Manually updating a package (CLI)
If auto-update is not enabled or you prefer manual control, apply updates using `glasskube update <package-name>`. Example updating cloudnative-pg:

```bash theme={null}
$ glasskube update cloudnative-pg
cloudnative-pg cloudnative-pg: v1.23.2+1 -> v1.23.3+1
Do you want to apply these updates? (y/N) y
Applying updates...
Update applied successfully.
```

Interactive configuration editing
Glasskube allows post-install configuration changes via the CLI or dashboard. The CLI provides an interactive prompt that walks through configurable values and saves a concise configuration summary.

Example interactive CLI configuration (kube-prometheus-stack):

```bash theme={null}
$ glasskube configure kube-prometheus-stack
kube-prometheus-stack has 6 values for configuration.

Enable Alertmanager
Old value: true
Keep? (Y/n) Y
Progress: 1/6

Grafana domain
DNS name for the Grafana Ingress.
Leave this empty to disable the Ingress.
Old value:
Keep? (Y/n) Y
Progress: 2/6

Enable Grafana
Old value: true
Keep? (Y/n) Y
Progress: 3/6

Node Exporter host network
Old value: false
Keep? (Y/n) Y
Progress: 4/6

Prometheus retention
Old value: 30d
Keep? (Y/n) n
Default: 30d
Use default? (Y/n) n
Would you like to specify a reference value (ConfigMap, Secret, Package) or literal value?
Enter the number of one of the following (default: Literal value):
 1) Reference value
 2) Literal value
options> 2
Please enter a value:
text> 20d
Progress: 5/6

Prometheus storage size
Old value: 10Gi
Keep? (Y/n) Y
Progress: 6/6

Configuration summary:
* grafanaEnabled: true
* prometheusNodeExporterHostNetwork: false
* prometheusRetention: 20d
* prometheusStorageSize: 10Gi
* alertmanagerEnabled: true
* grafanaDomain:
Continue? (Y/n) Y
✔ configuration changed
```

Namespace packages also expose a configuration editor in the Glasskube dashboard. For example, open the Quickwit package to view and edit its settings.

<Frame>
  <img alt="The image shows a Glasskube dashboard with information about an installed package called &#x22;quickwit,&#x22; including details like its namespace, repository, version, and status. There are options to install, open, and configure the package." />
</Frame>

Uninstalling packages
To remove a single package and its Kubernetes resources, use `glasskube uninstall <package-name>`:

```bash theme={null}
$ glasskube uninstall kubetail
The following packages will be removed from your cluster (minikube):
  * kubetail (requested by user)
Do you want to continue? (y/N) y
kubetail uninstalled successfully.
```

Purge Glasskube (complete cleanup)
To completely remove Glasskube components, CRDs, controllers, and all installed packages, use `glasskube purge`. This performs a full cleanup of Glasskube-managed resources and should be used with caution.

<Callout icon="warning">
  Using `glasskube purge` removes Glasskube components, CRDs, controllers, and all installed packages from the target cluster. Only run this when you intend to perform a full cleanup.
</Callout>

Example `glasskube purge` confirmation:

```bash theme={null}
$ glasskube purge
⚠️ Glasskube and all related resources will be purged from context minikube. This includes removal of all installed packages!
Continue? (y/N)
```

Quick reference — common Glasskube lifecycle commands

| Command                                  | Purpose                                                        | Example                                     |
| ---------------------------------------- | -------------------------------------------------------------- | ------------------------------------------- |
| `glasskube list`                         | List installed packages, repo versions, and auto-update status | `glasskube list`                            |
| `glasskube auto-update enable <package>` | Enable per-package auto-update                                 | `glasskube auto-update enable kubetail`     |
| `glasskube update <package>`             | Manually apply an available update                             | `glasskube update cloudnative-pg`           |
| `glasskube configure <package>`          | Interactive CLI configuration editor                           | `glasskube configure kube-prometheus-stack` |
| `glasskube uninstall <package>`          | Remove a single installed package                              | `glasskube uninstall kubetail`              |
| `glasskube purge`                        | Remove Glasskube and all managed packages (dangerous!)         | `glasskube purge`                           |

Summary

* Glasskube monitors a central packages repository where a bot adds new package versions.
* Enable per-package auto-updates to automatically update installations after repository PRs are merged.
* Use the CLI (`glasskube list`, `auto-update enable`, `update`, `configure`, `uninstall`, `purge`) or the UI to manage package lifecycle tasks interactively.
* Edit package values post-installation with `glasskube configure` or the dashboard.
* Use `glasskube uninstall` to remove individual packages; use `glasskube purge` only for a full cluster cleanup.

References and further reading

* Glasskube packages repository: [https://github.com/glasskube/packages](https://github.com/glasskube/packages)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/e651aa8d-8cb5-4d5c-ab54-c5e732ff9c21/lesson/69aa6f0f-bb6b-4a93-b694-36693b4d20e3" />
</CardGroup>
