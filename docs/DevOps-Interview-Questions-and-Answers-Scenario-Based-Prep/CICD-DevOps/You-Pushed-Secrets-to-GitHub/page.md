# You Pushed Secrets to GitHub

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/CICD-DevOps/You-Pushed-Secrets-to-GitHub/page

Guide for handling accidentally committed secrets to GitHub, rotate credentials immediately, purge them from git history, and enable pre-commit and CI secret scanning.

Scenario: You’re working late and accidentally commit AWS secret keys to a public GitHub repository. You immediately run `git revert` and push again. Does that solve the problem?

Short answer: No.

`git revert` creates a new commit that undoes the change, but the original commit containing the secret still exists in the repository history. Anyone (or any bot) can view older commits or run `git log` to recover the secret.

<Frame>
  <img alt="The image illustrates the concept of using &#x22;git revert,&#x22; showing it creates a new commit, with a diagram and the word &#x22;WRONG&#x22; in bold." />
</Frame>

Automated scanners and harvesting bots are constantly monitoring public pushes. Within seconds or minutes of the push, the exposed keys can be grabbed and used. Cloud providers (like AWS) may detect and notify you, but that notification often arrives after the key has already been exploited.

<Frame>
  <img alt="The image discusses how automated bots scan every push for harvesting, warning about potential security issues related to AWS." />
</Frame>

Immediate action: follow these three steps in this exact order

1. Rotate the secret immediately (revoke it).
2. Purge the secret from Git history (rewrite history).
3. Prevent future leaks by adding local scans / pre-commit hooks.

<Frame>
  <img alt="The image outlines three steps for managing secrets in Git: rotating secrets, purging them from history, and preventing future issues, using tools like BFG Repo Cleaner, git filter-repo, gitleaks, and detect-secrets." />
</Frame>

***

## Detailed steps

### Step 1 — Rotate the secret (do this immediately)

Assume the key is compromised as soon as it was exposed. Do not spend time trying to remove the commit before rotating credentials.

* Revoke or delete the compromised key in the cloud provider console or via CLI.
* Create a new key and update any services that used the old one.
* Notify affected developers or systems so they can update their configurations.

Example AWS CLI commands:

```shell theme={null}
