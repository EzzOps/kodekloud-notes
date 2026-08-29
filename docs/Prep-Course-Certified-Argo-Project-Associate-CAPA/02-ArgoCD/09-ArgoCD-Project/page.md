# ArgoCD Project

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-Project/page

Explains Argo CD AppProjects for enforcing repository and deployment boundaries, role based permissions, and sync windows to enable multi tenancy and least privilege in GitOps.

In this lesson we cover Argo CD AppProjects — the mechanism Argo CD uses to create security boundaries, enable multi-tenancy, and limit what applications can do and where they can be deployed. Every Argo CD Application is assigned to an AppProject. By defining projects you can enforce least privilege and reduce blast radius between teams and environments.

<Frame>
  <img alt="A blue-green gradient slide with the title &#x22;ArgoCD AppProject&#x22; centered. A small &#x22;© Copyright KodeKloud&#x22; notice appears in the bottom-left." />
</Frame>

By default Argo CD creates a permissive `default` project. AppProjects let you narrow that scope using rules such as:

| Field                    | Purpose                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| sourceRepos              | Which Git repositories application manifests may come from (patterns allowed).             |
| destinations             | Which clusters and namespaces applications may be deployed to (server + namespace).        |
| clusterResourceWhitelist | Which cluster-scoped resource kinds (group/kind) the project’s apps are allowed to manage. |
| roles                    | Role-based permissions for users and automation acting on applications in the project.     |
| syncWindows              | Time windows that allow or block automated syncs for applications in the project.          |

<Callout icon="lightbulb">
  Create AppProjects for each team or environment to enforce least privilege and reduce the blast radius of potential mistakes or compromise.
</Callout>

Inspecting the default project with kubectl:

```bash theme={null}
$ kubectl get appprojects -n argocd

NAME      AGE
default   10h
```

View the YAML for the `default` project:

```bash theme={null}
$ kubectl get appproject default -o yaml -n argocd
```

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: default
  namespace: argocd
spec:
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'
  destinations:
  - namespace: '*'
    server: '*'
  sourceRepos:
  - '*'
```

Explanation of the key fields shown above:

* clusterResourceWhitelist: A list of cluster-scoped resource kinds (group/kind) that applications in this project are allowed to manage. The default allows all cluster resources.
* destinations: A list of allowed destinations (server and namespace) where applications may be deployed. The default allows any cluster/namespace.
* sourceRepos: A list of allowed Git repositories (patterns) that can be used as the source for applications in this project. The default allows any repo.

You should tighten these fields to restrict which repos can be used and where apps can be deployed. In addition to the fields above, define fine-grained roles to control user and automation permissions, and configure sync windows to permit or block automated syncs during specific times.

<Callout icon="warning">
  The default AppProject is permissive (allows all repos, namespaces, and cluster resources). Always create scoped AppProjects for teams and production environments to prevent unauthorized access or accidental changes across clusters.
</Callout>

Links and references:

* [Argo CD Projects — Official Documentation](https://argo-cd.readthedocs.io/en/stable/operator-manual/project/)
* [Argo CD Concepts](https://argo-cd.readthedocs.io/en/stable/user-guide/overview/)
* [Kubernetes RBAC and Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

Summary: Use AppProjects to enforce repository and deployment boundaries, restrict cluster-scoped resource management, and apply role-based access and sync policies. Properly scoped projects are a core practice for Argo CD multi-tenancy and secure GitOps workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/8cc0543a-c857-4ebb-b47a-fe1e222078b9" />
</CardGroup>
