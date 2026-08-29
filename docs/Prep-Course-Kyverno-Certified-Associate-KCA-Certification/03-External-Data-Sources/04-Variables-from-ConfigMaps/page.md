# Variables from ConfigMaps

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/External-Data-Sources/Variables-from-ConfigMaps/page

Using Kubernetes ConfigMaps as dynamic external data for Kyverno policies to centrally manage values and auto add cost center labels to Deployments

In this lesson we solve Alex's challenge by using one of Kubernetes' most common external data sources: a ConfigMap. ConfigMaps provide a standard, cluster-native way to store configuration data, and Kyverno policies can reference them dynamically at evaluation time.

ConfigMap + Kyverno = dynamic, centralized configuration for policies:

* Platform, security, or finance teams can manage values in a Kubernetes resource without changing Kyverno policies.
* Kyverno performs a live lookup on each policy evaluation, so ConfigMap updates apply immediately—no policy redeploy required.
* Policy logic stays clean and reusable because configuration values are not hard-coded.

Why this matters (at a glance)

| Benefit                | Description                                                                      | Example                                          |
| ---------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------ |
| Centralized management | Teams manage configuration in a Kubernetes resource instead of editing policies. | Use a `ConfigMap` in a `finance` namespace.      |
| Dynamic policies       | Policies pull the current value at evaluation time.                              | Updated `cost-center` value applied immediately. |
| Decoupling             | Policy logic remains reusable and free of hard-coded values.                     | One policy can serve many environments.          |

How it works
Kyverno exposes per-rule external data via a `context` block. Think of `context` as a rule-level variable declaration: you give the data source a name, specify the type (`configMap`) and the ConfigMap's `name` and `namespace`. Kyverno fetches the ConfigMap and exposes its data under the name you provide.

Example context structure:

```yaml theme={null}
rules:
  - name: my-rule-that-needs-data
    # The context is defined here, per-rule
    context:
      # A unique name for the context variable
      - name: <a-unique-name-for-this-data>
        configMap:
          # Name of the ConfigMap which will be looked up
          name: <name-of-the-configmap>
          # Namespace in which this ConfigMap is stored
          namespace: <namespace-of-the-configmap>
    match:
      ...
    mutate:
      ...
```

Problem recap: Alex needs to mutate new Deployments to add a `cost-center` label. The finance team manages the label value in a central ConfigMap outside the policy.

<Frame>
  <img alt="The image illustrates a step in Alex's challenge involving auto-adding a cost-center label to deployments, managed by a finance department using a central ConfigMap." />
</Frame>

Step 1 — create the ConfigMap
Before Kyverno can read configuration from the cluster, the ConfigMap must exist. The finance team manages a ConfigMap named `billingInfo` in the `finance` namespace containing the `cost-center` value:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: billingInfo
  namespace: finance # Managed by the finance team
data:
  # The value they want to apply
  cost-center: "alpha-project"
```

Step 2 — write the Kyverno policy
Objectives:

1. Define a `context` that points to the `billingInfo` ConfigMap.
2. Use the fetched value to add a `cost-center` label to Deployments.

Policy (ClusterPolicy) that performs the mutation:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-cost-center-label
spec:
  validationFailureAction: audit
  rules:
    - name: add-cost-center-label
      match:
        any:
          - resources:
              kinds:
                - Deployment
      context:
        - name: billingData          # Our context variable name
          configMap:
            name: billingInfo        # Name of the ConfigMap
            namespace: finance       # Namespace of the ConfigMap
      mutate:
        patchStrategicMerge:
          spec:
            template:
              metadata:
                labels:
                  cost-center: "{{billingData.data.\"cost-center\"}}"
```

How the policy works

* The `context` block defines a variable called `billingData` that points to the `billingInfo` ConfigMap in the `finance` namespace.
* Reference the ConfigMap value inside the substitution expression using the context name followed by `.data` and the key name. For example: `{{billingData.data."cost-center"}}`.
* The `mutate` rule uses `patchStrategicMerge` to ensure the label is added to the Pod template metadata for matched Deployments.

Important detail — keys with special characters
When a ConfigMap key contains special characters (like a hyphen), quote the key inside the substitution expression so it is treated as a literal field name. In this policy the label value is set as:

```yaml theme={null}
cost-center: "{{billingData.data.\"cost-center\"}}"
```

> **lightbulb** When referencing keys that include characters like `-` (dash) or spaces, quote the key inside the substitution expression so it is treated as a literal field name.

Putting it all together

* The finance team updates `billingInfo` when the cost center changes.
* Kyverno reads the latest value at evaluation time using the per-rule `context`.
* New Deployments are automatically labeled with the current `cost-center` from the ConfigMap—no policy edits required.

This approach centralizes configuration, removes hard-coded values from policies, and enables non-policy teams to manage operational values using standard Kubernetes resources.

Links and references

* [Kubernetes ConfigMap documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [Kyverno documentation: Context](https://kyverno.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/470bb961-febf-41b6-b75b-4c439def6eae/lesson/fe909135-71f6-4e33-85be-5f6a625c793d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/470bb961-febf-41b6-b75b-4c439def6eae/lesson/6a444ab2-ec43-4bb3-8970-6251471fcbdd)
