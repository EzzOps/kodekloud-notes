# Repository Privacy Setting Options

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Repository-Privacy-Setting-Options/page

Guidance on repository governance using branch protection, CODEOWNERS, and required reviewers to enforce reviews, ownership, and CI gating for stable auditable main branches

Move a repository from a personal or generic workflow to a production-ready, team-governed environment by applying three governance pillars that ensure every change is verified before reaching protected branches. These pillars enforce review, ownership, and CI gating so your main or production branches stay stable and auditable.

* Branch protection
* CODEOWNERS
* Required reviewers

## At-a-glance: governance pillars

| Pillar             | Purpose                                              | Key benefit                                                                   |
| ------------------ | ---------------------------------------------------- | ----------------------------------------------------------------------------- |
| Branch protection  | Enforce merge and push policies on critical branches | Prevents direct or force pushes; ensures merges follow team processes         |
| CODEOWNERS         | Map files and paths to responsible users or teams    | Automatically requests reviews from designated owners when those files change |
| Required reviewers | Make code review a blocking requirement for merges   | Ensures peer review, knowledge sharing, and prevents unilateral deployments   |

## 1) Branch protection

Branch protection rules are immutable guardrails you apply to important branches (for example, `main` or `production`). They convert ad-hoc Git operations into policy-driven workflows: merges must follow rules, CI must pass, and direct pushes or force pushes can be blocked. Typical branch protection features include required status checks, required approving reviews, and restrictions on who can push or merge.

Benefits:

* Enforce a pull-request-only workflow
* Prevent accidental overwrites or bypassing CI/CD
* Require specific checks and approvals before merge

## 2) CODEOWNERS

A `CODEOWNERS` file maps file paths to users or teams so that GitHub automatically requests reviews from the right people when code touching those paths is changed. Place it at `.github/CODEOWNERS`, the repository root, or in the `.github` folder in the repository.

<Frame>
  <img alt="The image is a table comparing two features, &#x22;Branch Protections&#x22; and &#x22;CODEOWNERS,&#x22; detailing their technical purposes and key benefits. It highlights how branch protections prevent accidental actions on stable code, and CODEOWNERS automates reviewer assignment based on file modifications." />
</Frame>

A simple `CODEOWNERS` example:

```text theme={null}
