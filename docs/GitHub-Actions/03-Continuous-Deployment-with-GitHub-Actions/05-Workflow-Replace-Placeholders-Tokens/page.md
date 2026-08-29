# Workflow Replace Placeholders Tokens

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Deployment-with-GitHub-Actions/Workflow-Replace-Placeholders-Tokens/page

This guide explains automating token replacement in Kubernetes manifests using GitHub Actions.

In this guide, you’ll learn how to automate token replacement in your Kubernetes manifests using GitHub Actions. We will cover:

* Defining repository-level variables for namespace, replicas, and image
* Installing and configuring the `cschleiden/replace-tokens@v1` action
* Dynamically fetching the Ingress controller’s external IP
* Applying placeholder replacement in `kubernetes/development/*.yaml`
* Verifying the transformed manifests before deployment

***

## Placeholder tokens in your manifests

Under `kubernetes/development/`, manifests contain tokens like `{_NAMESPACE_}`, `{_REPLICAS_}`, `{_IMAGE_}`, and `{_INGRESS_IP_}`:

```yaml theme={null}
