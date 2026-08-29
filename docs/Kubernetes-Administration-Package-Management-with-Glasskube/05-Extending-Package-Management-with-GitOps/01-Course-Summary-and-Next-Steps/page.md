# Course Summary and Next Steps

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Extending-Package-Management-with-GitOps/Course-Summary-and-Next-Steps/page

Summary of a course on Kubernetes package management using Glasskube, covering bottlenecks, features, GitOps integration, migration steps, and how to try or contribute to the project.

We’ve reached the end of the Kubernetes Package Management with Glasskube course. This final chapter summarizes what we covered, highlights the concrete benefits Glasskube delivers, and outlines practical next steps if you want to try or contribute.

## What we covered (recap)

* Fundamentals of package management and a Kubernetes refresher to establish context.
* Current state of package management and common bottlenecks that teams face.
* Evaluation of existing tooling (plain Kubernetes manifests, Helm) and where they fall short for full-featured package management.
* Introduction to Glasskube as an alternative designed to address those shortcomings.
* Hands-on package installation and lifecycle management using Glasskube, including multi-repository workflows.
* Integration with GitOps: installed and demonstrated the Glasskube GitOps template to show streamlined cluster management with Git-driven workflows.

## Key takeaways

* Glasskube simplifies dependency management and reduces configuration complexity by offering GUI, definition files, and CLI options.
* Secret injection is more flexible and secure, with multiple supported approaches.
* Glasskube’s opinionated model reduces complexity while remaining flexible enough to support real-world deployments.
* CRD update support and better handling of umbrella-like scenarios mitigate frequent pain points in Kubernetes package management.
* Strong GitOps integration enables a predictable, auditable workflow for cluster changes.

<Frame>
  <img alt="The image lists common package management bottlenecks, including dependency management, configuration complexity, secret injection, umbrella charts, CRD updates, and lack of GitOps support." />
</Frame>

## Bottlenecks vs. Glasskube: quick comparison

| Bottleneck               | How Glasskube helps                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------- |
| Dependency management    | Built-in dependency handling and clearer package boundaries reduce manual coordination.        |
| Configuration complexity | GUI, declarative definition files, and a CLI lower the risk of errors and speed up onboarding. |
| Secret injection         | Multiple injection strategies make secrets safer and more flexible to manage.                  |
| Umbrella-chart friction  | Glasskube’s model avoids many umbrella-chart pitfalls by providing more explicit composition.  |
| CRD updates              | Supports CRD lifecycle and migration workflows to reduce upgrade pain.                         |
| Lack of GitOps support   | Native GitOps templates and workflows for repository-driven cluster management.                |

Secret injection is also much easier with Glasskube since it provides multiple options for injecting sensitive data. The problems we often see with umbrella charts are alleviated by Glasskube’s model, and CRD updates are supported as well — another important improvement.

<Frame>
  <img alt="The image lists common package management bottlenecks, including dependency management, configuration complexity, secret injection, umbrella charts, CRD updates, and lack of GitOps support." />
</Frame>

## What’s next for Glasskube

One major direction is reducing reliance on raw Kubernetes manifests and Helm’s Go templating in the backend. Glasskube is working toward a new package configuration language that aims to be more expressive and user-friendly than Go templates, simplifying package authorship and reuse.

<Frame>
  <img alt="The image depicts a timeline with a single point labeled &#x22;01&#x22; describing a new package configuration language, alongside a blue box asking &#x22;What's next?&#x22;." />
</Frame>

We’ll update this course when those features land and announce changes publicly.

We also plan to strengthen integrations across the Kubernetes ecosystem to improve interoperability with existing tooling, making it easier to adopt Glasskube incrementally.

## How to get involved

Glasskube is open source and welcomes contributions. Here are practical ways to participate:

* Star the repository on GitHub to show support and increase visibility.
* Browse the issue tracker to find starter tasks or feature requests that match your skills.
* Join community channels to ask questions, offer feedback, or coordinate with maintainers.

<Callout icon="lightbulb">
  If you're interested in contributing: consider starring the project, reviewing open issues to find tasks that match your skills, and participating in community discussion channels to ask questions or coordinate with maintainers.
</Callout>

<Frame>
  <img alt="The image shows a &#x22;Next Steps&#x22; section with two points: one is to contribute to the Glasskube project via a GitHub link, and the other is to join a Discord server via another link." />
</Frame>

## Recommended next steps (practical)

* Try Glasskube in a non-production cluster to evaluate workflows and migration paths.
* Apply the GitOps template from the course to a test repository to validate the end-to-end flow.
* Review the project’s contribution guidelines and open issues to identify a first contribution.
* Follow release notes and announcements so you can adopt new package language features and integrations when available.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm](https://helm.sh/)
* Glasskube: check the project repository and community links in the course materials for the latest source and contribution guidelines.

That's it from my side. I hope this course clearly conveyed the core aspects of Kubernetes package management and demonstrated how Glasskube can simplify cluster operations. I also hope it inspired you to explore Glasskube, try it in your clusters, and contribute to the project.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/0ddd5879-550c-4c12-82cd-ac19fb487de5/lesson/ed1115c5-91e2-42c5-9766-471f4008410f" />
</CardGroup>
