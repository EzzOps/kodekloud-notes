# Enabling and Disabling Features

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Enabling-and-Disabling-Features/page

How to enable and disable GitHub repository collaboration features, where to change settings, best practices, and differences from archiving and the GitHub Archive Program

Manage which collaboration features appear in a GitHub repository to streamline your team's workflow and reduce UI clutter. Repository administrators can enable or disable many options—such as Issues, Wiki, Discussions, Projects, and Sponsorships—so the repository surface shows only the tools your contributors use.

This guide explains where to find these settings, which features are toggleable, best practices when disabling features, and how disabling features differs from archiving a repository or participating in the GitHub Archive Program.

## Where to change repository feature settings

1. Open the repository you administer.
2. Click the Settings tab.
3. Under Settings → Options, scroll to the Features section (labeling may vary by account or organization).
4. Use the provided checkboxes or toggles to enable or disable features (for example: Issues, Wiki, Discussions, Projects, Sponsorships). Note: availability can depend on account type and organization policies.
5. Save changes if prompted. Most toggles apply immediately for repository visitors.

> **lightbulb** Tip: If you plan to disable a feature that contains historical content (e.g., Issues or Discussions), export or migrate important conversations first so nothing critical is lost to contributors.

## What you can and cannot toggle

| Feature                           | Where to toggle               | Notes                                                                                                        |
| --------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Issues                            | Settings → Options → Features | Can be turned off to hide issue creation and listing; consider exporting issues before disabling.            |
| Wiki                              | Settings → Options → Features | Turn off if docs are maintained elsewhere.                                                                   |
| Discussions                       | Settings → Options → Features | Disabling hides the Discussions tab and new thread creation.                                                 |
| Projects                          | Settings → Options → Features | Projects (classic) and newer project boards may have separate settings or migration paths.                   |
| Sponsorships                      | Settings → Options → Features | Availability may vary by repository/account.                                                                 |
| Pull Requests                     | N/A (core platform feature)   | Cannot be removed via Features toggles. Use branch protection rules and permissions to control PR workflows. |
| Actions / Environments / Packages | Settings → Actions / Packages | These items are controlled in their respective settings pages rather than the general Features section.      |

If you need to limit pull request activity, use:

* Branch protection rules
* Repository permissions and teams
* Limiting who can push or create branches

## Best practices and considerations

* Disable features that are unused to simplify the repository UI and reduce maintenance.
* Before you disable Issues or Discussions, export or migrate important content. Disabling a feature can make historic conversations harder to discover.
* If you want to stop new activity but keep the existing history untouched and accessible, consider archiving the repository (see next section) instead of turning off individual features.
* For organization-wide control, check any organization policies that may override repository-level settings.

## Distinguishing repository archiving vs. feature toggles

Archiving a repository (Settings → Options → Archive this repository) sets the repo to read-only: pushes are disabled, and issues and pull requests are frozen so they cannot be opened or modified. This is a separate, reversible administrative action and is not the same as toggling individual Features in a repo’s Options.

> **warning** Archiving a repository on GitHub makes it read-only and is distinct from the GitHub Archive Program. Archiving freezes normal activity (pushes, issues, PRs) but does not enact long-term preservation by GitHub.

## About the GitHub Archive Program

The [GitHub Archive Program](https://archiveprogram.github.com/) is a long-term preservation initiative. Selected repositories are preserved in multiple secure, geographically distributed locations (including a deep archive in Svalbard, Norway). Participation is managed by GitHub and is separate from repository-level feature toggles and the read-only archive state.

> **lightbulb** Disabling unused collaboration features and choosing the appropriate archival or preservation path helps maintain a clean repository experience while protecting important project history.

## Quick summary

* Use Settings → Options → Features to toggle collaboration features you do not use.
* You cannot remove pull request functionality via the Features toggles; control PR workflows with permissions and branch protections.
* Archiving a repository on GitHub makes it read-only; the GitHub Archive Program provides separate, long-term preservation.

## Links and references

* [GitHub Archive Program](https://archiveprogram.github.com/)
* [Archiving a repository (GitHub Docs)](https://docs.github.com/en/repositories/archiving-a-repository/archiving-a-repository)
* [Repository settings documentation](https://docs.github.com/en/repositories)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/05139926-c8bd-46a1-a08c-541680eb64c9)
