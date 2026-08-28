# Comparing an Issue a Discussion and a Pull Request

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Issues/Comparing-an-Issue-a-Discussion-and-a-Pull-Request/page

Explains differences between GitHub issues, discussions, and pull requests and recommends workflow and best practices

This lesson compares GitHub's three collaboration spaces—issues, discussions, and pull requests—so you can choose the right tool for each stage of development. Each space serves a distinct purpose in the workflow:

* Issues track actionable items like bugs, tasks, and feature requests.
* Discussions host open-ended community conversations, brainstorming, and Q\&A.
* Pull requests propose code changes and provide a structured review and integration process.

Use the sections below to understand purpose, best practices, and expected outcomes for each.

<Callout icon="lightbulb">
  Use Issues to define and track work, Discussions to collect context and community input, and Pull Requests to submit, review, and merge code. Linking these together (discussion → issue → pull request) creates a clear trace of decision-making and implementation.
</Callout>

Issues

* Purpose: Track specific work items—bugs, tasks, or feature requests.
* Best uses: Assigning work, prioritizing via labels/milestones, and tracking progress with project boards.
* Integrations: Assignees, labels, milestones, and references to commits and pull requests.

<Frame>
  <img alt="The image provides a comparison of GitHub features: Issues, Discussions, and Pull Requests, highlighting their primary purposes and best uses for project management, community engagement, and code integration." />
</Frame>

Discussions

* Purpose: Host open-ended conversations such as brainstorming, Q\&A, and polls.
* Best uses: Gathering feedback, developing ideas before formalizing requirements, and maintaining community knowledge.
* Outcome: A persistent knowledge base or community consensus that can inform issues or future development.

Pull requests

* Purpose: Propose concrete code or documentation changes and run them through review and CI processes.
* Best uses: Line-by-line code review, running automated tests, tracking CI/CD status, and merging approved changes into the main branch.
* Outcome: Reviewed and tested code merged into the repository.

How they differ at a glance

* Issues: Action-oriented and integrated with project management.
* Discussions: Community-focused, exploratory, and documentation-friendly.
* Pull requests: Implementation-focused with review, CI, and merge gates.

Table — Feature comparison

| Feature         |                          Issue |                          Discussion |                            Pull Request |
| --------------- | -----------------------------: | ----------------------------------: | --------------------------------------: |
| Primary purpose |           Track tasks and bugs |       Community Q\&A, brainstorming |           Propose & review code changes |
| Typical outcome |       Closed when work is done |        Documented consensus or idea |         Merged changes into main branch |
| Best for        | Assigning work, prioritization |  Collecting feedback, brainstorming |         Code review, CI checks, merging |
| Integrations    |  Labels, milestones, assignees | Pins, categories, community replies | CI/CD, code review tools, status checks |

Key feature differences

* Issues integrate with project-tracking features (milestones, assignees, labels).
* Discussions act as a forum for long-form community engagement (Q\&A, polls, brainstorming).
* Pull requests enforce quality control through peer review, CI statuses, and merge checks.

Successful outcomes

* Issues: The task or bug is resolved and the issue is closed.
* Discussions: The conversation becomes a documented resource or leads to a clear decision.
* Pull requests: The changes pass review and CI, and are merged into the target branch.

Workflow hierarchy (recommended)

1. Discussions — explore the “why” (ideas, goals, feasibility).
2. Issues — define the “what” (tasks, acceptance criteria).
3. Pull requests — deliver the “how” (implementation, review, merge).

References and further reading

* [GitHub Docs — About issues](https://docs.github.com/en/issues)
* [GitHub Docs — About discussions](https://docs.github.com/en/discussions)
* [GitHub Docs — About pull requests](https://docs.github.com/en/pull-requests)

<Frame>
  <img alt="The image is a comparison table of GitHub features: Issues, Discussions, and Pull Requests. It outlines their key features, ideal outcomes, and workflow roles." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/3105bbb3-1ddf-433d-9b4f-15a905853817/lesson/40da7b8d-b07f-4b80-8343-bf728ee4efdb" />
</CardGroup>
