# What are Custom Actions

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Custom-Actions/What-are-Custom-Actions/page

Custom GitHub Actions allow you to customize CI/CD pipelines for specific project needs beyond existing marketplace options.

Custom GitHub Actions empower you to tailor your CI/CD pipelines to meet project-specific requirements. While the GitHub Marketplace offers a wealth of community-maintained Actions—covering tasks like runtime setup, artifact transfer, Docker builds, test report syncing, and Kubernetes deployments—there are scenarios where you need:

* **Project-specific logic** not covered by existing Actions
* **Integration** with internal or legacy services
* **Complex orchestration** with conditional steps or custom dependencies
* **Strict compliance** or security policies requiring in-house solutions

<Callout icon="lightbulb">
  Leverage community Actions whenever possible to reduce maintenance overhead. Create a custom Action only when you need functionality that isn’t already available.
</Callout>

Common use cases include:

* **Publishing an npm package** when a new Git tag is created
* **Sending SMS or Slack alerts** upon critical issue creation
* **Deploying custom security policies** or infrastructure templates

GitHub supports three main Action types. You can compare their features below:

<Frame>
  ![The image is a comparison chart of three types of custom actions: Composite Actions, Docker Actions, and JavaScript Actions, highlighting their features and differences.](https://kodekloud.com/kk-media/image/upload/v1752876097/notes-assets/images/GitHub-Actions-Certification-What-are-Custom-Actions/custom-actions-comparison-chart.jpg)
</Frame>

| Action Type        | Runner Support        | Isolation        | Best For                               |
| ------------------ | --------------------- | ---------------- | -------------------------------------- |
| Composite Actions  | Linux, macOS, Windows | Low (host)       | Bundling repeated workflow steps       |
| Docker Container   | Linux only            | High (container) | Complex environment or OS dependencies |
| JavaScript Actions | Linux, macOS, Windows | Medium           | Fast, lightweight scripting tasks      |

## Composite Actions

Composite Actions let you encapsulate multiple workflow steps into a single reusable unit.

```yaml theme={null}
