# Example webhook response:
# admission webhook "validate.kyverno.svc" denied the request:
# resource Deployment/default/nginx-deployment was blocked due to the following policies
# require-deployment-team-label:
#   require-deployment-team-label: 'validation error: You must have label `team` for all deployments. rule require-deployment-team-label failed at path /metadata/labels/team/'
```

Add `labels: { team: frontend }` to succeed.

### Example 2 — Minimum replicas validation

Require at least 3 replicas for Deployments:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: minimum-replicas
spec:
  validationFailureAction: Enforce
  rules:
    - name: minimum-replicas
      match:
        any:
          - resources:
              kinds:
                - Deployment
      validate:
        message: "Deployment must specify at least 3 replicas"
        pattern:
          spec:
            replicas: ">=3"
```

Kyverno evaluates `spec.replicas` and denies requests with replicas \< 3.

### Mutation example — set imagePullPolicy when image uses :latest

Kyverno can mutate incoming requests. Example: set `imagePullPolicy` when a container uses the `:latest` tag:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: set-image-pull-policy
spec:
  rules:
    - name: set-image-pull-policy
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        patchStrategicMerge:
          spec:
            containers:
              - (image): "*:latest"
                imagePullPolicy: "IfNotPresent"
```

Notes:

* `mutate.patchStrategicMerge` merges values into the incoming object.
* The special key `(image): "*:latest"` matches container entries where `image` ends with `:latest` and sets `imagePullPolicy`.

## Demo workflow (commands)

1. Install Kyverno using the Helm commands above.
2. Create and apply example ClusterPolicy YAML files (labels, replicas, mutation).
3. Attempt to apply Deployments/Pods that violate policies to observe Kyverno denying them.
4. Switch `validationFailureAction` from `Audit` to `Enforce` after validating policy impact.

Kyverno documentation covers validate/mutate rules, wildcard patterns, strategic merge, and more. For pattern matching details see: [https://kyverno.io/docs/writing-policies/validate/](https://kyverno.io/docs/writing-policies/validate/)

<Frame>
  <img alt="The image is a screenshot of a webpage from the Kyverno documentation, specifically the section on validating rules, with detailed explanations and a sidebar menu containing navigation links." />
</Frame>

## Additional policy examples

* Deny `:latest` or require an explicit tag:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: no-latest-tag-policy
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-image-tag
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Container image must include an explicit tag, e.g., image:nginx:1.23.0"
        pattern:
          spec:
            containers:
              - image: "*:*"
    - name: disallow-latest-tag
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Cannot use the `:latest` tag"
        pattern:
          spec:
            containers:
              - image: "!*:latest"
```

* Allow only images from a private registry (example uses `kodekloud.io`):

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: deny-public-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: allow-private-registry
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Unknown image registry. Images must be pulled from kodekloud.io."
        pattern:
          spec:
            containers:
              - image: "kodekloud.io/*"
```

The pattern `kodekloud.io/*` enforces that the image string begins with the private registry prefix — replace with your registry (for example: `myregistry.internal/*`).

## Hands-on tips

* Start with `validationFailureAction: Audit` to measure impact before switching to `Enforce`.
* For lists like `containers`, Kyverno’s wildcard patterns and strategic merge keys (e.g., `(image)`) let you match items by key.
* Consider enabling Kyverno’s pre-configured Pod Security Standard policies to get a baseline. See Kubernetes Pod Security Standards: [https://kubernetes.io/docs/concepts/security/pod-security-standards/](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

<Frame>
  <img alt="The image is a flow diagram depicting an installation process involving a user, Helm, and Kubernetes-related components. It shows an arrow sequence from the user to Helm, and then to a group of puzzle-piece icons and a Kubernetes logo." />
</Frame>

## Summary

Kyverno is a Kubernetes-native policy engine that integrates with the admission webhook pipeline to validate and mutate resources using native Kubernetes CRDs (`ClusterPolicy` and `Policy`). With Kyverno you can automate enforcement of labels, image registries and tags, resource constraints, replica counts, network controls, and more. Installing via Helm is simple, and Kyverno offers pre-built policy bundles for common best practices. Start with `Audit` mode to validate impact, then move to `Enforce` when ready.

Happy experimenting with Kyverno — it’s a practical way to automate policy enforcement across your cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-by-doing-kubernetes-policies-with-kyverno/module/a3370f08-e378-4285-9305-52025206031a/lesson/88f594b7-4413-486b-9d5a-e1c9615efa5d" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/Learn-By-Doing-MariaDB/Introduction/Course-Introduction/page

Hands-on MariaDB course teaching installation, configuration, security, SQL, schema design, backups, performance tuning and Docker deployment for database administrators, developers, and IT professionals.

Hello and welcome to this Learn-By-Doing course on MariaDB.

My name is Jarugu Phanivardhan, and I will be your instructor for this course. This hands-on course is tailored for database administrators, developers, and IT professionals who want to master MariaDB for reliable, high-performance database management across development and production environments.

<Frame>
  <img alt="The image shows a circular diagram with three interconnected sections labeled &#x22;Database Administrators,&#x22; &#x22;IT Professionals,&#x22; and &#x22;Developers,&#x22; each represented by different colored icons." />
</Frame>

What you'll do in this course

* Set up and configure MariaDB for development and production.
* Manage users and privileges securely.
* Write and optimize basic SQL queries (CRUD).
* Design and modify table columns and schemas.
* Implement partitioned tables for large datasets.
* Choose and configure appropriate storage engines.
* Perform backups, enable logging, and monitor activity.
* Deploy and operate MariaDB in containerized environments using Docker.

Learning outcomes

* Confidently install and configure MariaDB in multiple environments.
* Securely manage users and roles and restrict access.
* Optimize queries and tune basic performance parameters.
* Implement scalable table designs and backup strategies.
* Deploy MariaDB containers and integrate with CI/CD workflows.

How to use the hands-on labs

* Open the lab environment and consult the course material and workbook.
* Use the terminal provided by the lab environment to run commands and interact with the database.
* Validate your work using the lab's check/validation feature to confirm task completion.

Common way to start the MariaDB client from the lab terminal:

```bash theme={null}
sudo mariadb -u root -p
```

This will prompt for the root password. If you must provide the password inline (use cautiously and only in non-production, controlled labs), you can run:

```bash theme={null}
sudo mariadb -u root -p'Pe$w0rd'
```

<Callout icon="lightbulb">
  For security, prefer the first form (`sudo mariadb -u root -p`) so the password is not visible in your shell history or process list.
</Callout>

If you get stuck

* Consult hints and solutions available in the lab.
* Use the lab validation feature to verify your answers.
* Revisit the workbook examples and command notes.

Course topics (progressive sequence)

| Topic                   | What you’ll learn                                        | Example / Tools                               |
| ----------------------- | -------------------------------------------------------- | --------------------------------------------- |
| Basic configurations    | Install, initialize, and configure MariaDB server        | `mysqld`, configuration files (`/etc/mysql/`) |
| User management         | Create users, grant and revoke privileges securely       | `CREATE USER`, `GRANT`, `REVOKE`              |
| Basic SQL commands      | CRUD operations and simple query tuning                  | `SELECT`, `INSERT`, `UPDATE`, `DELETE`        |
| Columns & schema design | Define columns, types, and constraints                   | `ALTER TABLE`, `CREATE TABLE`                 |
| Partitioned tables      | Partition strategies for large datasets                  | `PARTITION BY RANGE`                          |
| Storage engines         | InnoDB, MyISAM, Aria — when to use each                  | Engine selection and configuration            |
| Backup and logging      | Logical and physical backups, binary logs, audit logging | `mysqldump`, `mariabackup`, `binary log`      |
| MariaDB on Docker       | Containerize MariaDB and manage persistent data          | `docker run`, `docker-compose`                |

Further reading and references

* MariaDB Documentation: [https://mariadb.com/kb/en/](https://mariadb.com/kb/en/)
* Docker Documentation: [https://docs.docker.com/](https://docs.docker.com/)
* Best practices for backups and restores: [https://mariadb.com/kb/en/backup-and-restore/](https://mariadb.com/kb/en/backup-and-restore/)

Ready to begin?
Each lesson builds on the previous one, moving from initial setup to advanced configuration and performance optimization. Start the first hands-on lab to apply these concepts in a practical environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-by-doing-mariadb/module/115a5ed7-8ec1-46ef-97f7-180305153490/lesson/38929527-a9c8-473b-8a91-8d925956b74a" />
</CardGroup>
