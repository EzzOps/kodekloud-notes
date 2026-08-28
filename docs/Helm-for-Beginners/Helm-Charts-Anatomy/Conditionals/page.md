# Conditionals

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Conditionals/page

This article explores using conditionals in Helm charts to include or exclude template sections based on values in the values file.

In this article, we explore how to use conditionals in Helm charts to include or exclude sections of your templates based on values specified in the values file. With these techniques, you can add optional configurations such as custom labels, control whitespace, and conditionally render entire objects like service accounts—all of which add flexibility to your deployments.

## Example: Adding Optional Labels

Consider a basic Helm chart with a simple service template. Initially, you might have a `values.yaml` file with minimal configuration and a corresponding `service.yaml` template:

```yaml theme={null}
