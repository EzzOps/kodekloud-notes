# .github/FUNDING.yml — supported funding model platforms (examples)
github:          # Up to 4 GitHub Sponsors usernames, e.g., [user1, user2]
patreon:         # Single Patreon username
open_collective: # Single Open Collective username
ko_fi:           # Single Ko-fi username
tidelift:        # Single Tidelift platform-name/package-name, e.g., npm/babel
community_bridge:# Single Community Bridge project-name, e.g., cloud-foundry
liberapay:       # Single Liberapay username
issuehunt:       # Single IssueHunt username
lfx_crowdfunding:# Single LFX Crowdfunding project-name, e.g., cloud-foundry
polar:           # Single Polar username
buy_me_a_coffee: # Single Buy Me a Coffee username
thanks_dev:      # Single thanks.dev username
custom:          # Up to 4 custom sponsorship URLs, e.g., ['https://...', 'https://...']
```

Quick reference — common FUNDING.yml entries:

| Provider        | Purpose                            | Example                                              |
| --------------- | ---------------------------------- | ---------------------------------------------------- |
| GitHub Sponsors | Direct sponsor usernames (up to 4) | `github: ["sid-gh900","alice-mcberry"]`              |
| Patreon         | Patreon profile username           | `patreon: "your-patreon-name"`                       |
| Open Collective | Open Collective slug               | `open_collective: "acme-org"`                        |
| Ko-fi           | Ko-fi username                     | `ko_fi: "your-kofi"`                                 |
| Custom links    | Any external funding URL (up to 4) | `custom: ["https://fund.me/project", "https://..."]` |

Example: only GitHub Sponsors
If you want the repository to list only GitHub Sponsors accounts, create `.github/FUNDING.yml` with the GitHub entries:

```yaml theme={null}
# .github/FUNDING.yml
github: ["sid-gh900", "alice-mcberry"]
# patreon:
# open_collective:
# ko_fi:
# ... other platforms commented out
```

This makes the Sponsor button present those two GitHub usernames as possible recipients.

Branch protection and committing FUNDING.yml
If your repository enforces branch protection on the default branch (for example, requiring pull requests and reviews), you may not be able to commit `FUNDING.yml` directly to `main`. In that case you have two main options:

* Create a new branch, add `.github/FUNDING.yml`, and open a pull request for the default branch; or
* If you are an admin and your policy allows it, temporarily permit admins to bypass the protection rules and commit directly.

<Frame>
  <img alt="The image shows a GitHub interface where a user is proposing changes to a FUNDING.yml file but cannot commit directly to the main branch because it's protected." />
</Frame>

In my case I adjusted the branch rule to allow repository admins to bypass the protection, then committed the `FUNDING.yml` file directly to `main`.

<Frame>
  <img alt="This image shows the settings page of a GitHub repository titled &#x22;block-buster&#x22; where rulesets are being configured, including enforcement status and bypass lists. The interface also shows options for adding bypass actors such as roles or teams." />
</Frame>

After `.github/FUNDING.yml` is present on the default branch, the Sponsors button will appear on the repository UI. Visitors can click it to view available funding options.

<Frame>
  <img alt="The image shows a GitHub repository interface for a project named &#x22;block-buster&#x22; by &#x22;Pixelcraft-Studio-kk,&#x22; highlighting its directory structure and recent commit activity." />
</Frame>

Receiving payments (GitHub Sponsors onboarding)
Declaring a sponsor destination in `FUNDING.yml` does not by itself enable payouts. Each GitHub Sponsors account must complete onboarding steps (identity verification, banking details, tax info) to accept funds. When configuring a sponsorship account you select your country, enter payout information, and finish verification.

<Frame>
  <img alt="The image shows a GitHub Sponsors page prompting a user to complete steps like confirming identity and filling out bank information to launch a sponsorship profile and start receiving funding." />
</Frame>

Account-level sponsorship vs repository-level FUNDING.yml

* Repository-level `FUNDING.yml` controls which funding options a repository advertises.
* Account-level setup (user or organization) is required to accept payments. GitHub provides an accounts page listing organizations and users eligible for GitHub Sponsors.

When visiting a user or organization profile that has sponsorship enabled, visitors will see a Sponsor button. Clicking it opens a page where they can:

* Read about the author or project,
* Choose between tiers (monthly or one-time),
* Provide billing details and complete payment.

Here is an example of the sponsorship confirmation screen where a user confirms a \$1/month tier and fills billing information:

<Frame>
  <img alt="The image shows a GitHub sponsorship page where a user is confirming a $1 per month tier sponsorship. It includes sections for billing information, payment method, and an achievement notification." />
</Frame>

> **lightbulb** Place your `FUNDING.yml` at `.github/FUNDING.yml` on the repository's default branch (for example, `main`). If branch protection prevents a direct commit, open a pull request or temporarily allow admins to bypass the rule according to your workflow.

Summary

* Enable Sponsorship in repository Settings to show the Sponsor button.
* Use `.github/FUNDING.yml` to declare the providers and accounts to surface.
* Complete account-level GitHub Sponsors onboarding to receive payouts.
* If branch protection blocks direct commits, use a PR workflow or a temporary admin bypass.

Links and references

* GitHub Sponsors: [https://github.com/sponsors](https://github.com/sponsors)
* FUNDING.yml documentation: [https://docs.github.com/en/github/building-a-strong-community/adding-a-sponsor-button-to-your-repository](https://docs.github.com/en/github/building-a-strong-community/adding-a-sponsor-button-to-your-repository)
* GitHub branch protection rules: [https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-protected-branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-protected-branches)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c969426b-f74f-4ca3-8269-a63dff90fbc2/lesson/7fd39446-6e3d-434e-98a9-f45c97227c25)


# Demo Identify How to Follow People

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Benefits-of-Open-Source-Community/Demo-Identify-How-to-Follow-People/page

Guide on following users and organizations on GitHub, explaining what following does, differences from watching and starring repositories, and how to manage notifications.

Following people and organizations on GitHub helps you stay updated on their public activity—commits, public PRs, and issue activity—that appears in your personal news feed. This guide explains how to follow users and organizations, what following actually does, and how it differs from other GitHub features like `Watch` and `Star`.

Why follow?

* Receive a curated view of public activity from people and organizations you care about.
* Discover repositories, contributions, and community activity relevant to your interests.
* Build a list of profiles to quickly revisit.

## How to follow an individual user

1. Navigate to the user's GitHub profile page.
2. Locate the "Follow" button near the top-right of the profile header.
3. Click the "Follow" button.

Once followed, some of that user's public activity (e.g., public commits, public PRs) will appear in your activity feed. Following does not automatically subscribe you to repository-level notifications (issues, PRs, or emails).

<Frame>
  <img alt="The image shows a GitHub profile page with user details, repositories, and contribution stats. The profile features various repositories related to Kubernetes and Ansible." />
</Frame>

## How to follow an organization

1. Search for the organization by name or navigate to its GitHub organization page.
2. Open the organization profile.
3. Click the "Follow" button, usually near the top-right of the organization header.

Following an organization surfaces the organization’s public activity in your feed, similar to following an individual user. It does not grant access to private content or automatically sign you up for repository notifications.

> **lightbulb** Following someone or an organization surfaces their public activity in your feed. To receive issue/PR/email notifications for a specific repository, use that repository’s `Watch` settings.

## Follow vs Watch vs Star — quick comparison

| Action               | What it surfaces                                                               | Typical use case                                       |
| -------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| `Follow` (user/org)  | Public activity from a person or organization in your feed                     | Track people/organizations you want to monitor broadly |
| `Watch` (repository) | Notifications for activity in a specific repository (issues, PRs, discussions) | Get notified about repository-specific activity        |
| `Star` (repository)  | Save/favorite a repository for quick access and to indicate interest           | Bookmark repositories or show appreciation             |

For repository-level notifications:

* Click the `Watch` button on the repository page and choose the notification level you want (e.g., “All Activity”, “Custom”).

## Additional tips and important notes

* Following someone or an organization does not:
  * Subscribe you to issue/PR notifications for their repositories, or
  * Grant access to private repos or organization resources.

> **warning** Following does not change repository permissions or privacy. If you need notifications for a repository, set the repository's `Watch` level or adjust notification settings in your GitHub account.

## Useful links and references

* [GitHub Docs — Following users](https://docs.github.com/en/get-started/exploring-projects-on-github/following-people-on-github)
* [GitHub Docs — Watching repositories](https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/about-notifications)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c969426b-f74f-4ca3-8269-a63dff90fbc2/lesson/3464d99b-4a97-4285-807e-3efc9c2d3ee6)
