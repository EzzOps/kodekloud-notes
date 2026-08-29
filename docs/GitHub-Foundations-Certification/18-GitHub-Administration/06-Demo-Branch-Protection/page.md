# Demo Branch Protection

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Demo-Branch-Protection/page

Guide demonstrating how to create and enforce GitHub branch protection rules requiring pull requests, code reviews, status checks, and preventing direct commits to critical branches like main

Branch protection rules prevent accidental or unauthorized direct pushes to critical branches (for example, `main`). They enforce workflows such as requiring pull requests, code reviews, and passing automated checks before changes can be merged. This guide walks through creating a branch ruleset, targeting branches, selecting protection settings, and observing how GitHub blocks direct commits and enforces pull-request workflows.

<Frame>
  <img alt="The image is a screenshot of a GitHub profile page showing a list of repositories. The profile belongs to a user with the handle &#x22;sid-gh900,&#x22; highlighting both public and private repositories along with their descriptions and programming languages used." />
</Frame>

## Open the repository and locate branch protection

Open the repository you want to protect — in this demo it’s the Block Buster repository. If the default branch is unprotected, GitHub may show a banner offering a quick “Protect this branch” action. Alternatively, configure comprehensive rulesets by navigating to Settings > Branches in the repository.

<Frame>
  <img alt="The image shows a GitHub repository settings page, specifically for configuring branch rules. It includes options for setting rulesets, enforcement status, bypass lists, and branch targeting criteria." />
</Frame>

## Create a ruleset and configure enforcement

Create a new ruleset (for example, name it `prod-rules`) and enable enforcement. You can optionally add a bypass list to exempt specific users or teams (such as a small set of emergency admins). In this demo, we intentionally leave the bypass list empty so the rules apply to everyone, including repository admins.

> **lightbulb** Leaving the bypass list empty means no one—regardless of permissions—can bypass the rules. This is a strict setting useful for high-stakes repositories.

Target which branches the ruleset should affect. You can use explicit names (e.g., `main`) or wildcard patterns (for example, `release/*` or `feature/*`). Any branch matching the pattern will be subject to the rules; in this demo we target the default branch `main`.

### Common protection options

Below are commonly used protection settings and when to enable them.

| Protection option                     | Purpose                                                   | Example / Notes                                      |
| ------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| Require a pull request before merging | Disallows direct commits to protected branches            | Ensures every change is reviewed and merged via PR   |
| Require approving reviews             | Enforces code review by one or more reviewers             | Example: set minimum approving reviews to `1` or `2` |
| Require CODEOWNERS approval           | Requests review from maintainers listed in `CODEOWNERS`   | See [CODEOWNERS](/) for format and behavior          |
| Restrict merge methods                | Limits allowed merge strategies (merge, squash, rebase)   | Prevents undesirable histories or merges             |
| Require status checks to pass         | Blocks merges until CI, static analysis, or scans succeed | Example: CodeQL or other CI workflows                |
| Block force pushes / deletion         | Prevents destructive changes to branch history            | Recommended for protected release branches           |

<Frame>
  <img alt="The image shows a GitHub repository settings page with options for merging methods, blocking force pushes, and requiring code scanning results and Copilot code review." />
</Frame>

## Code scanning and integrations

GitHub Code Scanning (CodeQL) is a common built-in security scanner. When enabled, CodeQL runs as a GitHub Actions workflow and can be configured to mark PRs with alerts. You can require that these scans succeed (or meet a configured severity threshold) before allowing merges.

Create the ruleset. GitHub may prompt you to re-authenticate or complete two-factor authentication (2FA) if your account policy or organization requires it.

> **warning** If your organization enforces two-factor authentication or SSO, you may be prompted to verify your identity before activating the ruleset.

When the ruleset is saved and activated you’ll see it listed under the repository rulesets.

<Frame>
  <img alt="The image shows a GitHub repository settings page, specifically under &#x22;Rulesets&#x22; for a repository named &#x22;block-buster,&#x22; with an active ruleset named &#x22;prod-rules.&#x22; The bypass list is empty, and the settings indicate it applies to the &#x22;main&#x22; branch." />
</Frame>

## How protection affects everyday workflows

Once the ruleset is active, direct commits to `main` are blocked. For example, editing the README and attempting to commit directly to `main` will not succeed; GitHub will prompt to create a new branch and initiate a pull request instead.

Example README content that might be edited:

```markdown theme={null}
