# Match Statements

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Resource-Filters/Match-Statements/page

Explains Kyverno match block filters for precisely targeting Kubernetes resources and API requests using kinds, names, namespaces, label selectors, operations, and identity or role checks.

This article explains Kyverno's primary filtering tool: the `match` block. Every Kyverno rule uses a `match` statement to tell Kyverno which resources and requests the rule should evaluate. The `match` block supports multiple filters (kinds, names, namespaces, selectors, operations, subject/role identity checks, etc.) that you can combine to create precise targeting. Below we walk through the most common filters, show how they combine logically, and provide practical examples.

## Basic kind matching

The most common filter is the resource `kind`. Use a `resources` block with a required `kinds` list inside a `match` entry. Items in the `kinds` list behave like a logical OR: the request matches if its resource kind equals any listed kind.

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Pod
          - Deployment
          - Service
```

## Names and namespaces

You can narrow matching to specific resource names and namespaces. `names` and `namespaces` are sibling filters inside the same `resources` object:

* Items within each list are ORed (e.g., `names: [a, b]` matches name `a` OR `b`).
* Different sibling filters (e.g., `names` and `namespaces`) are combined with an implicit AND (both must be satisfied for that `resources` entry to match).

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Pod
        names:
          - "dev"
          - "test-*"
        namespaces:
          - "testing"
          - "dev"
```

In this example:

* The resource kind must be `Pod`.
* The resource name must be exactly `dev` OR match the glob `test-*`.
* The resource must be in the `testing` OR `dev` namespace.

> **lightbulb** Lists inside a single filter (for example, multiple `names`) are ORed. Different sibling filters (for example, `names` and `namespaces`) are ANDed, so a resource must satisfy both siblings to match.

## Disambiguating with Group/Version/Kind (GVK)

When the same `kind` name exists in multiple APIs (for example, built-in Kubernetes `NetworkPolicy` and CNI-specific `NetworkPolicy` from Antrea or Calico), disambiguate using Group/Version/Kind (GVK). Specifying the full GVK prevents accidental matches across different API groups.

<Frame>
  <img alt="The image explains the concept of specifying GroupVersionKind (GVK) to avoid naming conflicts between different tools with resources like 'NetworkPolicy'. It provides examples using Kubernetes and Antrea CNI." />
</Frame>

## Label-based selection (`selector`)

Use `selector` to match resources by their labels. Combine `selector` with `operations` when you want the rule to run only for specific actions (CREATE, UPDATE, etc.). `operations` is a sibling of `resources` inside the same `any` item.

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Deployment
      operations:
        - CREATE
        - UPDATE
      selector:
        matchLabels:
          app: critical
```

This rule targets Deployments labeled `app: critical` and only triggers on CREATE and UPDATE operations (it will not run for DELETE operations).

## Namespace label selection (`namespaceSelector`)

Use `namespaceSelector` to filter resources by labels on their namespace. This is useful for applying policies across entire environments or namespaces with specific metadata.

Simple `matchLabels` example:

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Pod
      namespaceSelector:
        matchLabels:
          organization: engineering
```

You can also use `matchExpressions` for more expressive rules with operators like `In`, `NotIn`, `Exists`, and `DoesNotExist`:

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Pod
      namespaceSelector:
        matchExpressions:
          - key: purpose
            operator: In
            values:
              - production
              - staging
          - key: sensitive-data
            operator: NotIn
            values:
              - "true"
```

This matches Pods in namespaces whose `purpose` label is `production` or `staging`, and where `sensitive-data` is not `true`.

## Request identity filtering (subjects, roles, clusterRoles)

Kyverno can filter based on who is making the API request. This enables you to create exceptions for admins, service accounts, or CI/CD systems and enforce policies only for certain requesters.

<Frame>
  <img alt="The image explains a process for filtering by request identity, detailing subjects, roles, and clusterRoles in relation to user permissions. It also shows an icon and mentions checking the requester's ID card as a solution." />
</Frame>

## Subjects

The `subjects` block matches specific request identities. Supported kinds include `User`, `Group`, and `ServiceAccount`. The `subjects` list behaves like an OR: the request matches if it matches any subject entry.

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Pod
      subjects:
        - kind: User
          name: "alex@somecorp.com"
        - kind: Group
          name: "platform-admins"
        - kind: ServiceAccount
          name: "argocd-service-account"
```

## Roles and clusterRoles

Alternatively, match by permission level using `roles` (namespaced Roles) and `clusterRoles` (cluster-scoped ClusterRoles). These check the requester's effective permissions.

Namespace-level role example (matches requests where the user has the `edit` role in the target namespace):

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Secret
      roles:
        - "edit"
```

ClusterRole example (matches requests where the user has the `cluster-admin` ClusterRole):

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Pod
      clusterRoles:
        - "cluster-admin"
```

## Combining resource filters with identity filters (AND semantics)

When `resources`, `subjects`, `roles`, and `clusterRoles` are defined at the same level inside the same `any` item, all sibling filters are combined with logical AND. The request must satisfy every sibling condition in that `any` entry to match.

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Deployment
      subjects:
        - kind: Group
          name: admins
      clusterRoles:
        - cluster-admin
```

In this example the request matches only if:

1. The resource is a Deployment, AND
2. The requester is a member of the `admins` group, AND
3. The requester also has the `cluster-admin` ClusterRole.

If any of these conditions is false, the entire `any` item does not match.

> **warning** Be careful when combining identity checks and resource filters: mismatched expectations (for example, matching a subject that cannot have the listed role) will cause the `any` item to fail and the rule to not apply.

## Complex example: combining multiple filters

You can combine the building blocks above to create very specific match criteria. In the `any` item below, all sibling filters must be satisfied for the request to match.

```yaml theme={null}
match:
  any:
    - resources:
        kinds:
          - Deployment
          - StatefulSet
        names:
          - "mongo*"
          - "postgres*"
        namespaces:
          - "dev*"
          - "test"
      selector:
        matchLabels:
          app: mongodb
        matchExpressions:
          - key: tier
            operator: In
            values:
              - database
```

Breakdown:

* Resource kind must be Deployment OR StatefulSet.
* Resource name must match `mongo*` OR `postgres*`.
* Namespace must match `dev*` OR be named `test`.
* Resource must have label `app: mongodb`.
* Resource must have label `tier` with a value in `[database]`.

All of the above must be true for that `any` item to match.

## Quick reference table

| Filter key               | Purpose                                              | Short example                                         |
| ------------------------ | ---------------------------------------------------- | ----------------------------------------------------- |
| `kinds`                  | Match resource kinds (OR across list items)          | `kinds: [Pod, Deployment]`                            |
| `names`                  | Match specific resource names / globs                | `names: ["api-*", "frontend"]`                        |
| `namespaces`             | Match target namespaces / globs                      | `namespaces: ["dev", "staging*"]`                     |
| `selector`               | Match resource labels in the object                  | `selector: matchLabels: {app: critical}`              |
| `namespaceSelector`      | Match by labels on the resource’s namespace          | `namespaceSelector: matchLabels: {team: ops}`         |
| `operations`             | Match API verbs (CREATE/UPDATE/DELETE)               | `operations: [CREATE, UPDATE]`                        |
| `subjects`               | Match request identities (User/Group/ServiceAccount) | `subjects: [{kind: User, name: "alice"}]`             |
| `roles` / `clusterRoles` | Match based on requester's roles/permissions         | `roles: ["edit"]` / `clusterRoles: ["cluster-admin"]` |

## Links and references

* Kyverno match filter docs: [https://kyverno.io/docs/writing-policies/match-conditions/](https://kyverno.io/docs/writing-policies/match-conditions/)
* Kubernetes API concepts: [https://kubernetes.io/docs/concepts/overview/](https://kubernetes.io/docs/concepts/overview/)
* RBAC in Kubernetes: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

## Conclusion

Kyverno's `match` block provides powerful, composable filters to precisely target when policies apply. By combining `kinds`, `names`, `namespaces`, label selectors, operations, and identity checks (subjects/roles/clusterRoles), you gain fine-grained control over policy scope and enforcement.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/592779da-cc67-4cd3-a990-1f0ffd90f6fc)
