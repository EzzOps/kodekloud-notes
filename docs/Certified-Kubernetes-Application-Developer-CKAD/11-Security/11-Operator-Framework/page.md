# Operator Framework

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Operator-Framework/page

This lesson explores the operator framework for managing Kubernetes custom resources through CRDs and custom controllers in a unified deployment.

In this lesson, we'll explore the operator framework, a powerful method for managing Kubernetes custom resources by combining Custom Resource Definitions (CRDs) and custom controllers into a unified deployment.

Traditionally, you would manually create a CRD along with its corresponding controller (deployed as a Pod or Deployment). The operator framework streamlines this process by packaging both components together. For example, when you deploy a flight operator, it automatically creates the necessary CRD, provisions custom resources, and deploys the custom controller as a Deployment.

Below is an example configuration for a flight ticket CRD and its corresponding controller:

```yaml theme={null}
