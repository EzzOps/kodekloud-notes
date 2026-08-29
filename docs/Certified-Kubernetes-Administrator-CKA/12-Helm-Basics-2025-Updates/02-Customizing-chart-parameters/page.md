# Revision 1: Using an older WordPress image
containers:
  - image: wordpress:4.8-apache
```

```yaml theme={null}
# Revision 2: After upgrading to a newer WordPress image
containers:
  - image: wordpress:5.8-apache
```

To roll back to revision 1:

```bash theme={null}
$ helm rollback wordpress
```

With each significant change invoked via Helm commands, a new revision is created. For instance, installation creates revision 1, an upgrade creates revision 2, and a rollback may create revision 3 representing the restored state.

<Callout icon="lightbulb">
  Helm 3's intelligent three-way comparison considers the following:

  * The previous chart revision,
  * The desired chart state,
  * The live state of Kubernetes objects.
    This approach ensures that discrepancies—such as manual changes using kubectl—are correctly reconciled.
</Callout>

## Handling Manual Changes and Upgrades

In Helm 2, if a user manually modified Kubernetes objects (e.g., using `kubectl set image`) after deployment, these changes were not recorded in Helm's revision history, meaning Helm might not detect any differences during a rollback. In contrast, Helm 3 compares the live state against both the current and desired revisions. This ensures:

* Manual modifications outside of Helm are preserved during upgrades.
* Overwritten configurations are avoided unless explicitly intended.

## Conclusion

The transition from Helm 2 to Helm 3 marks a significant improvement in Kubernetes deployment management. By removing Tiller and implementing a more robust rollback mechanism via a three-way strategic merge patch, Helm 3 ensures enhanced security, simplified architecture, and greater reliability during upgrades.

For more detailed information on Helm and Kubernetes, check out the following resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm Documentation](https://helm.sh/docs/)

This guide should help you understand the evolution of Helm and leverage Helm 3's features for a more secure and streamlined deployment experience.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/10d7440b-907c-46da-ac5c-d833e7022375/lesson/0ce360eb-79c9-4e1a-9519-80ff28a8c3fe" />
</CardGroup>


# Customizing chart parameters

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Helm-Basics-2025-Updates/Customizing-chart-parameters/page

Learn to customize chart parameters during a Helm chart installation, including overriding default values for WordPress using command-line options or custom values files.

In this guide, you'll learn how to customize chart parameters during a Helm chart installation. When you deploy WordPress using the Bitnami chart, it uses the default values defined in the chart’s values.yaml file. For example, the default blog name is set as "User's Blog!" in the values file. This article explains how this value is configured and outlines the various methods available for overriding it.

## Understanding the Default Configuration

The WordPress application is deployed using a Kubernetes Deployment resource. Its configuration is partly derived from the values set in `values.yaml`. Below is a snippet from the `values.yaml` file indicating the default settings:

```yaml theme={null}
