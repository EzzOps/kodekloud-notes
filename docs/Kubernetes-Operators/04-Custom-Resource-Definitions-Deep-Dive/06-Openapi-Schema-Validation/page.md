# Openapi Schema Validation

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Custom-Resource-Definitions-Deep-Dive/Openapi-Schema-Validation/page

Guide to using OpenAPI v3 schemas to validate Kubernetes CRDs, enforce constraints, pruning, defaults, and CEL based validations

A CRD without an OpenAPI schema will accept any YAML you send it. Typos in field names, a string where you expected an integer, or replicas set to negative seven — all of these will be accepted unless you validate the shape.

Example of a malformed spec that a controller might receive:

```yaml theme={null}
spec:
  relicas: 3                  # typo in the field name
  image: 123                  # wanted a string
```

The OpenAPI v3 schema (see: [https://spec.openapis.org/oas/v3.0.3](https://spec.openapis.org/oas/v3.0.3)) is your first line of defense: the Kubernetes API server enforces it before your controller ever sees the object. Think of the OpenAPI schema as the printed rules on a form — it defines which boxes are required, which values are allowed, and which entries the API server should reject before persistence.

On a CRD, the schema lives under `spec.versions.schema.openAPIV3Schema` and follows the standard OpenAPI v3 structural schema. At the top level you describe a tree of `type`, `properties`, and `required` fields. For example:

```yaml theme={null}
versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              image:
                type: string
              replicas:
                type: integer
            required: ["image"]
          status:
            type: object
```

Set `type: object` at the root, then walk down into `spec` and `status` the same way. Each field in the schema supports constraints; these common constraints let you validate names, sizes, ranges, and structural rules before your controller needs to handle invalid input.

Callouts

> **lightbulb** Use an OpenAPI structural schema to reject invalid CRs early — this simplifies controller logic and prevents reconciliation loops caused by malformed objects.

Common constraints by data type

| Data Type        | Common Constraints                               | Example                                         |
| ---------------- | ------------------------------------------------ | ----------------------------------------------- |
| String           | `minLength`, `maxLength`, `pattern`, `enum`      | See "Strings" example below                     |
| Number / Integer | `minimum`, `maximum`, `exclusiveMinimum`         | See "Numbers" example below                     |
| Array            | `minItems`, `maxItems`, `uniqueItems`            | See "Arrays" example below                      |
| Object           | `properties`, `required`, `additionalProperties` | Use object-level `required` to enforce presence |

Strings

* `minLength`, `maxLength`
* `pattern` (regular expression)
* `enum` for closed sets

Example:

```yaml theme={null}
spec:
  type: object
  properties:
    name:
      type: string
      minLength: 3
      maxLength: 40
      pattern: "^[a-zA-Z][a-z0-9-]*$"
    environment:
      type: string
      enum: ["dev", "staging", "prod"]
```

Numbers

* `minimum`, `maximum`, `exclusiveMinimum` (boolean)

Arrays

* `minItems`, `maxItems`, `uniqueItems`

Required

* The `required` list on any object enumerates which child properties must be present. If a required field is missing, writes will be rejected.

```yaml theme={null}
properties:
  replicas:
    type: integer
    minimum: 1
    maximum: 10
    exclusiveMinimum: false
  ports:
    type: array
    minItems: 1
    maxItems: 5
    uniqueItems: true
required: ["image", "replicas"]
```

Defaults

* You can set `default` in the schema. When a user omits that field, the API server fills it on write so your controller doesn't have to handle the empty case.

Example:

```yaml theme={null}
spec:
  type: object
  properties:
    replicas:
      type: integer
      default: 3
```

Pruning (automatic removal of undeclared fields)

* Structural schemas cause automatic pruning. In Kubernetes, a structural schema is a fully typed template: anything not declared on that template is stripped before storage. Pruning prevents users from stashing arbitrary data inside your CR.

Example interaction:

```bash theme={null}
$ kubectl apply -f webapp.yaml
$ kubectl get webapp hello -o yaml
spec:
  image: nginx
  replicas: 3
  # color: blue → pruned before storage
```

If you need a free-form blob in a subtree, opt out of pruning with the `x-kubernetes-preserve-unknown-fields` extension:

```yaml theme={null}
config:
  type: object
  x-kubernetes-preserve-unknown-fields: true
```

Useful Kubernetes schema extensions

* `x-kubernetes-int-or-string` — accepts either integer or string (used by core Kubernetes APIs for ports and quantities).

```yaml theme={null}
port:
  x-kubernetes-int-or-string: true
```

* `x-kubernetes-validations` — where expression-based validation rules live. These use CEL (Common Expression Language, [https://github.com/google/cel-spec](https://github.com/google/cel-spec)) and run in the API server (no admission webhook required). CEL is ideal for cross-field checks that OpenAPI cannot express.

Examples:

```yaml theme={null}
x-kubernetes-validations:
  - rule: "self.replicas <= 100"
    message: "replicas must be 100 or fewer"
  - rule: "self.minReplicas <= self.maxReplicas"
    message: "minReplicas cannot exceed maxReplicas"
```

If a user submits an object violating a CEL rule, the API server returns a descriptive error:

```bash theme={null}
$ kubectl apply -f webapp.yaml  # webapp.yaml sets replicas: 200
The WebApp "hello" is invalid:
replicas must be 100 or fewer
```

Operational notes and versioning

* When you change a schema on an existing CRD, already stored objects are not revalidated; only new writes are checked. Tightening constraints can fail new writes even though old objects remain stored. Version your API and plan schema migrations carefully.

> **warning** When you tighten a schema, existing stored objects are not automatically revalidated. Plan schema migrations and API versioning carefully.

Next steps

* You will write a CRD by hand for the webapp resource and observe these validators rejecting bad input before it reaches your controller.

<Frame>
  <img alt="The image is a slide introducing a topic about writing a Custom Resource Definition (CRD) by hand, highlighting the role of validators in rejecting bad input before it reaches the controller. It includes a blue-green gradient design with a gear icon." />
</Frame>

References and further reading

* OpenAPI Specification v3: [https://spec.openapis.org/oas/v3.0.3](https://spec.openapis.org/oas/v3.0.3)
* Kubernetes CRD validation and structural schemas: [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* CEL for Kubernetes validation: [https://github.com/google/cel-spec](https://github.com/google/cel-spec)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/0355fbee-32d4-44f3-b84e-60fbb1a269da)
