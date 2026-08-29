# What are Actions

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-Core-Concepts/What-are-Actions/page

GitHub Actions are automation components for software development workflows, enabling CI/CD, testing, and deployment through reusable actions from GitHub and the community.

GitHub Actions are pre-built, reusable automation components designed to help you automate software development workflows—such as CI/CD, testing, and deployment. Whether you choose official Actions from GitHub, community-created Actions, or build your own, you can share and reuse automation logic across repositories with ease.

## Discovering Actions in the GitHub Marketplace

The [GitHub Marketplace][marketplace] is the primary hub for finding Actions contributed by GitHub and the wider community. You’ll find hundreds of Actions covering tasks like code analysis, Docker builds, notifications, and more.

* **Verified Actions**: Marked with a ✅ badge to indicate GitHub has vetted the creator as a partner.
* **Community Actions**: Created by individual contributors or organizations without the verification badge.

<Callout icon="triangle-alert">
  Always review the source code of community Actions before adding them to your workflows. Verify they don’t expose secrets, log sensitive data, or perform unexpected network requests.
</Callout>

## Adding an Action to Your Workflow

After selecting an Action, navigate to its documentation page to view usage examples, version compatibility, and required inputs. Then, add it to your workflow under `steps:` using the `uses:` keyword:

```yaml theme={null}
