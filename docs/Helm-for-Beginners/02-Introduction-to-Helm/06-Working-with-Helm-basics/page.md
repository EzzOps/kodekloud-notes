# Application password
# Defaults to a random 10-character alphanumeric string if not set
# wordpressPassword:
# Admin email
wordpressEmail: user@example.com
# First name
# wordpressFirstName: FirstName
# Last name
# wordpressLastName: LastName
# Blog name
# wordpressBlogName: User's Blog!
```

Helm also simplifies application upgrades, rollbacks, and uninstallation. With just one command, Helm determines the necessary adjustments for an upgrade or rollback:

```bash theme={null}
$ helm upgrade wordpress
$ helm rollback wordpress
```

Similarly, to uninstall your application and remove all associated objects, you use:

```bash theme={null}
$ helm uninstall wordpress
```

***

In summary, Helm acts as both a package manager and a release manager for Kubernetes applications. It abstracts the management of individual objects, allowing you to deploy, upgrade, and uninstall your application as a single unit. This abstraction significantly reduces deployment complexity and minimizes human error when managing Kubernetes clusters.

For additional information, visit the [Helm Documentation](https://helm.sh/docs/) and the [Kubernetes Documentation](https://kubernetes.io/docs/).

This concludes our brief introduction to Helm. In the upcoming sections, we will dive deeper into Helm commands and explore advanced usage techniques. Happy Helming!

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/15e220ca-1229-4779-81f0-3bc9f804aa6b/lesson/b13ab55d-4db6-4ea0-99fa-de8e6c600a88)


# Working with Helm basics

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Introduction-to-Helm/Working-with-Helm-basics/page

This guide covers the basics of using Helm, the Kubernetes package manager, and its command-line interface for deploying applications.

In this guide, you will explore the fundamentals of Helm—the Kubernetes package manager—and learn how to use its command-line interface (CLI) for various tasks. Every operation demonstrated here is executed through the Helm CLI.

***

## Viewing General Help

Running the `helm` command without arguments, or with the `--help` flag, displays useful information about available commands and their usage. For example:

```bash theme={null}
$ helm --help

The Kubernetes package manager

Common actions for Helm:
- helm search: search for charts
- helm pull: download a chart to your local directory for inspection
- helm install: deploy a chart onto Kubernetes
- helm list: list chart releases

Usage:
  helm [command]

Available Commands:
  completion  generate autocompletion scripts for the specified shell
  create      create a new chart with the given name
  dependency  manage a chart's dependencies
  env         helm client environment information
  get         download extended information of a named release
  help        Help about any command
  history     fetch release history
```

This output serves as a quick reference for determining the proper command for a specific task. For example, if you're trying to recover from a failed upgrade, this help message reminds you that the correct command is `helm rollback` rather than a non-existent `helm restore`.

***

## Exploring Subcommands: Repository Management

Helm offers detailed assistance for managing chart repositories through subcommands. To view all available commands for repository management, execute:

```bash theme={null}
$ helm repo --help

This command consists of multiple subcommands to interact with chart repositories.
It can be used to add, remove, list, and index chart repositories.

Usage:
    helm repo [command]

Available Commands:
    add     add a chart repository
    index   generate an index file given a directory containing packaged charts
    list    list chart repositories
    remove  remove one or more chart repositories
    update  update information of available charts locally from chart repositories
```

For example, if you want to update your local chart cache, you can review the detailed help for that subcommand:

```bash theme={null}
$ helm repo update --help
Update gets the latest information about charts from the respective chart repositories.
Information is cached locally, where it is used by commands like 'helm search'.

Usage:
    helm repo update [flags]

Aliases:
    update, up
```

***

## Deploying a WordPress Website on Kubernetes

Helm significantly simplifies the deployment of applications in Kubernetes. In this section, you will deploy a WordPress website using a prepackaged Helm chart available on online repositories like Artifact Hub. Look for official or verified publisher badges to identify high-quality charts.

### Steps to Deploy

1. Begin by adding the Bitnami chart repository to your local Helm configuration

> **lightbulb** Begin by adding the Bitnami chart repository to your local Helm configuration.

```bash theme={null}
$ helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories
```

2. With the repository added, deploy the WordPress chart to your Kubernetes cluster

> **lightbulb** With the repository added, deploy the WordPress chart to your Kubernetes cluster.

```bash theme={null}
$ helm install my-release bitnami/wordpress
NAME: my-release
LAST DEPLOYED: Wed Nov 10 18:03:50 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: wordpress
CHART VERSION: 12.1.27
APP VERSION: 5.8.1

** Please be patient while the chart is being deployed **
Your WordPress site can be accessed through the following DNS name from within your cluster:
my-release-wordpress.default.svc.cluster.local (port 80)
```

This output confirms that your WordPress application has been successfully deployed as a release named `my-release`.

3. To view all installed releases, use the `helm list` command

> **lightbulb** To view all installed releases, use the `helm list` command.

```bash theme={null}
$ helm list
NAME        NAMESPACE   REVISION    UPDATED                                  STATUS    CHART                APP VERSION
my-release  default     1           2021-11-10 18:03:50.414174217 +0000 UTC    deployed  wordpress-12.1.27   5.8.1
```

4. When you need to remove the WordPress deployment, Helm allows you to easily c...

> **triangle-alert** When you need to remove the WordPress deployment, Helm allows you to easily clean up all associated Kubernetes objects.

```bash theme={null}
$ helm uninstall my-release
release "my-release" uninstalled
```

***

## Managing Helm Repositories

Helm repositories store charts and their associated metadata. In addition to adding repositories with `helm repo add`, you can list and update your chart repositories as needed.

* **List Current Repositories:**

  ```bash theme={null}
  $ helm repo list
  NAME    	URL
  bitnami  https://charts.bitnami.com/bitnami
  ```

* **Update Repositories:**\
  Similar to a system package manager, refresh the local cache of repository information with:

  ```bash theme={null}
  $ helm repo update
  Hang tight while we grab the latest from your chart repositories...
  ...Successfully got an update from the "bitnami" chart repository
  Update Complete. Happy Helming!
  ```

This ensures you have the most up-to-date chart information from each repository.

***

## Advanced Chart Searches

Helm supports powerful search capabilities to help you find the right chart. You can search for charts hosted on the Artifact Hub or within your local repositories.

* **Search in Artifact Hub:**

  ```bash theme={null}
  $ helm search hub wordpress
  URL
  https://artifacthub.io/packages/helm/riftbit/wordpress
  https://artifacthub.io/packages/helm/bitnami-ak... 
  https://artifacthub.io/packages/helm/bitnami/wordpress
  ```

* **Search Across All Locations:**

  ```bash theme={null}
  $ helm search wordpress
  Search enables you to look for Helm charts in multiple locations, including the Artifact Hub and locally added repositories.

  Usage:
      helm search [command]

  Available Commands:
      hub     search for charts in the Artifact Hub or your own hub instance
      repo    search repositories for a keyword in charts
  ```

Using these search options, you can review important chart details such as version numbers and descriptions before installation.

***

## Conclusion

Helm streamlines the deployment and management of applications on Kubernetes. Whether you're deploying a WordPress website or another application, the Helm CLI offers a powerful and user-friendly set of commands to add repositories, install charts, monitor releases, and remove deployments—all from the command line.

Now that you understand these fundamental operations, try them out in your own environment. Happy Helming!

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/15e220ca-1229-4779-81f0-3bc9f804aa6b/lesson/42552883-ea17-4a2d-8ab5-92d1ed7074ad)
