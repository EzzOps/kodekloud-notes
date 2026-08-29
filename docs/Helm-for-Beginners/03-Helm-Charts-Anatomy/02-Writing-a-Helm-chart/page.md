# Writing a Helm chart

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Writing-a-Helm-chart/page

Learn to build a simple Helm chart from scratch, utilizing templates for configurable Kubernetes resource names and automating package installations.

In this guide, you'll learn how to build a simple Helm chart from scratch. We will demonstrate how Helm templates work to create unique and configurable Kubernetes resource names. Helm charts are extremely versatile—they not only automate the installation of Kubernetes packages but also perform additional tasks (like backing up a database before upgrades) much like installation wizards on traditional operating systems.

For example, consider an upgrade command such as:

```bash theme={null}
$ helm upgrade wordpress-release bitnami/wordpress
```

While this may seem complex at first, we will begin with a basic example and progressively introduce more advanced concepts.

## Creating a Simple "Hello World" Chart

In this section, we will create a Helm chart for a simple "Hello World" application. The application will use an Nginx deployment with two replicas and expose the service through a NodePort.

Below are the Kubernetes manifest files for our Hello World application:

```yaml theme={null}
