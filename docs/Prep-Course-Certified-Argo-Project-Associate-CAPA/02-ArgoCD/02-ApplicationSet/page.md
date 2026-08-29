# ApplicationSet

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ApplicationSet/page

Explains Argo CD ApplicationSet that generates many Applications from parameter generators and a template to automate consistent multi-cluster and multi-environment GitOps deployments.

An Argo CD Application defines what to deploy and where. When you scale across clusters, environments, or teams, creating many similar Application manifests manually quickly becomes repetitive and error-prone. An ApplicationSet acts as a factory for Argo CD Applications: you declare a single ApplicationSet manifest that the ApplicationSet controller uses to generate many Applications from parameter sources (generators) and a template.

What this gives you:

* Declare once, produce many: author a single ApplicationSet and generate multiple Applications.
* Consistency: a template ensures each generated Application follows the same blueprint.
* Scale: support multi-cluster, multi-environment, and preview workflows without manual duplication.

## Example: a single Application

Here is a minimal Application manifest that creates one Application named `color-app`:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: color-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/sid/app-1.git
    targetRevision: HEAD
    path: team-a/color
  destination:
    server: https://kubernetes.default.svc
    namespace: color
  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

Instead of copying and editing this manifest for each cluster or environment, use an ApplicationSet: define generators to produce parameter sets and a template that acts as an Application blueprint with placeholders. The ApplicationSet controller renders the template for each parameter set and creates the corresponding Applications for Argo CD to manage.

## ApplicationSet example (list generator)

The following ApplicationSet uses the `list` generator to create a tools Application per cluster:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: common-tools
spec:
  generators:
    - list:
        elements:
          - cluster: software-dev
            url: https://1.0.3.4
          - cluster: telecom-prod
            url: https://2.0.6.8
          - cluster: acme-preprod
            url: https://9.0.7.6
  template:
    metadata:
      name: '{{.cluster}}-tools'
    spec:
      project: default
      source:
        repoURL: https://github.com/dasher-infra-team/cluster-tools.git
        targetRevision: HEAD
        path: tools/{{.cluster}}
      destination:
        server: '{{.url}}'
        namespace: tools
```

The generator provides parameter values such as `cluster` and `url`. The template uses Go-style templating (for example `{{.cluster}}`) to substitute those values when generating each Application.

<Frame>
  <img alt="A diagram titled &#x22;ArgoCD ApplicationSet&#x22; showing a central user branching out to multiple user+envelope icons (many applications). The left side contrasts a single &#x22;ArgoCD Application&#x22; (hand‑written letter) with the right side &#x22;ApplicationSet&#x22; (mail‑merge system) plus notes about generator (parameter list) and template (letter with placeholders)." />
</Frame>

## Core components

The two core concepts in an ApplicationSet are:

* Generators: produce parameter sets (for example, cluster names and API URLs).
* Template: an Argo CD Application manifest that includes placeholders (for example, `{{.cluster}}` and `{{.url}}`) which are filled in by values from the generators.

This pattern enables scalable GitOps workflows: treat an Application as a single, hand-written letter, and an ApplicationSet as a mail-merge system that generates personalized letters for each recipient.

<Callout icon="lightbulb">
  Argo CD provides multiple generator types so you can produce parameters from static lists, cluster registries, Git repositories, SCM providers, and custom plugins—enabling flexible multi-cluster and preview deployments.
</Callout>

## Built-in generator types

ApplicationSet supports several built-in generators. Use the generator type that matches how you want to source parameters (static lists, cluster registry, Git repo layout, etc.).

|                  Generator Type | Use Case                                                                     | Typical example or output                       |
| ------------------------------: | ---------------------------------------------------------------------------- | ----------------------------------------------- |
|                            List | Static parameter sets included in the manifest                               | A list of cluster names and API URLs            |
|                         Cluster | Create an Application per cluster registered with Argo CD                    | Generate apps for every cluster in Argo CD      |
|                             Git | Discover directories in a repository and generate per-directory Applications | Repo-per-environment or path-per-team layouts   |
|                          Matrix | Combine parameter sets from two or more generators to produce all pairings   | Deploy multiple services to multiple clusters   |
|                           Merge | Merge parameter lists from multiple generators into combined sets            | Combine cluster info with environment metadata  |
|                    SCM Provider | Discover repos or organization metadata from GitHub/GitLab                   | Auto-provision apps for discovered repositories |
|                    Pull Request | Create ephemeral preview Applications for open PRs                           | Preview environments for PRs before merging     |
| Cluster Decision Resource (CDR) | Use an external custom resource to select target clusters dynamically        | Dynamic cluster selection based on policies     |
|                          Plugin | Run an external service or script to generate custom parameters              | Integrate custom discovery logic or APIs        |

<Frame>
  <img alt="A slide titled &#x22;ArgoCD ApplicationSet Generators&#x22; showing nine numbered generator types (List, Cluster, Git, Matrix, Merge, SCM Provider, Pull Request, Cluster Decision Resource, and Plugin) arranged in three columns. The slide includes a KodeKloud copyright." />
</Frame>

## Patterns and best practices

* Prefer templates for shared configuration and keep sensitive values out of the template (use Secrets or external secret management).
* Use `matrix` when you need the Cartesian product of two parameter sets (for example, apps × environments).
* Use `merge` to combine attributes from multiple generators into a single parameter set.
* Use the `Cluster` generator together with labels to target a subset of registered clusters.
* For preview environments, use the `Pull Request` generator to create ephemeral Applications that are automatically cleaned up when PRs are closed.

## Quick reference and links

* For the Argo CD project and full ApplicationSet reference, see the official docs: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/) and [https://argo-cd.readthedocs.io/en/stable/applicationsets/](https://argo-cd.readthedocs.io/en/stable/applicationsets/)
* Learn more about GitOps and multi-cluster patterns: [https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)

By combining generators and templates you automate the creation of consistent, repeatable Applications and enable teams to self-serve multi-cluster deployments from a single declarative manifest.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/c7dc3d8d-66f7-4343-b0ad-fa7c09149fa7" />
</CardGroup>
