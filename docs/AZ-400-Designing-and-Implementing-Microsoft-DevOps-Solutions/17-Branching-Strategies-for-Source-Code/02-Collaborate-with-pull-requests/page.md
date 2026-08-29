# Collaborate with pull requests

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Branching-Strategies-for-Source-Code/Collaborate-with-pull-requests/page

This guide covers the pull request lifecycle, best practices, and workflows for effective collaboration in software development.

Pull requests (PRs) are essential for modern software teams. They enable code review, discussion, and controlled merges—ensuring high quality and transparency in every change. In this guide, we’ll walk through the pull request lifecycle, share best practices, and demonstrate workflows that foster effective collaboration.

## Table of Contents

1. [Branching Strategy](#branching-strategy)
2. [Opening a Pull Request](#opening-a-pull-request)
3. [Collaborating & Reviewing](#collaborating--reviewing)
4. [Merging & Cleanup](#merging--cleanup)
5. [References & Resources](#references--resources)

***

## Branching Strategy

Isolating work on a dedicated branch prevents conflicts and supports parallel development.

| Branch Type | Naming Convention      | Purpose                       |
| ----------- | ---------------------- | ----------------------------- |
| feature     | `feature/your-feature` | New functionality             |
| fix         | `fix/description`      | Bug fixes                     |
| hotfix      | `hotfix/issue-id`      | Urgent production fixes       |
| release     | `release/x.y.z`        | Prep for next version rollout |

```bash theme={null}
