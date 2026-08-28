# sample fetched output
remote: Enumerating objects: 8, done.
remote: Counting objects: 100% (8/8), done.
remote: Compressing objects: 100% (7/7), done.
Total 7 (delta 1), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (7/7), 1.87 KiB | 639.00 KiB/s, done.
From https://github.com/sid-990/block-buster
 * [new branch]      1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag -> origin/1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
```

2. List local and remote branches

```bash theme={null}
git branch --list -a
* feature-1
  main
  remotes/origin/1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature-1
  remotes/origin/main
```

3. Check out the remote issue branch and set it to track origin

```bash theme={null}
git checkout 1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
# sample output:
# Branch '1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag' set up to track remote branch '1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag' from 'origin'.
# Switched to a new branch '1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag'
```

Make the change and test locally

* Open `script.js`, apply the corrected code above (or an equivalent safe approach).
* Run the application locally to confirm the fix and check for regressions.

Example local test command:

```bash theme={null}
# start your local dev server / preview as appropriate for the project
# e.g., npm start
npm start
```

Commit and push the fix

* Reference the issue number in the commit message so GitHub links the commit to the issue (e.g., `refs #1` or `#1`).

```bash theme={null}
git add script.js
git commit -m "fix: avoid exponential ball growth when applying multiBall (refs #1)"
git push origin 1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
```

Sample push output:

```bash theme={null}
# sample output:
Counting objects: 5, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 450 bytes | 450.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To https://github.com/sid-990/block-buster
   abc1234..def5678  1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag -> 1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
```

On GitHub

* After pushing, refresh the repo page. The commit will appear on the remote branch and GitHub will auto-link the commit to issue #1 if the commit message includes the issue reference.
* From there, open a pull request to start code review and CI checks.

Common Git commands used in this workflow

| Command                    | Purpose                                                          |
| -------------------------- | ---------------------------------------------------------------- |
| `git fetch`                | Retrieve updates from the remote without changing local branches |
| `git branch --list -a`     | List local and remote branches                                   |
| `git checkout <branch>`    | Switch to a branch; can set up tracking to origin                |
| `git add <file>`           | Stage changes for commit                                         |
| `git commit -m "msg"`      | Commit staged changes with a message                             |
| `git push origin <branch>` | Push local branch to the specified remote branch                 |

Next steps

* Open a pull request from the branch and continue with code review and CI.
* Consider adding a unit or integration test that validates the `multiBall` behavior to prevent regressions (for example, assert the ball count never exceeds `MAX_BALLS` after activation).

Links and references

* [Git documentation](https://git-scm.com/doc)
* [GitHub docs: Creating a pull request](https://docs.github.com/en/pull-requests)
* [MDN: Array.prototype.slice()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice)
* [MDN: Spread syntax](https://developer.mozilla.org/en-US[AWS_SECRET_ACCESS_KEY]/Spread_syntax)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/cd01762a-d490-4310-b50c-e1b357a7dc03" />
</CardGroup>


# Different Pull Request Statuses

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Different-Pull-Request-Statuses/page

Guide to GitHub pull request lifecycle and statuses Draft Open Closed Merged with actions, CI considerations, review tips, and merge strategies.

In this lesson we explain the common statuses a GitHub pull request (PR) goes through from creation to final resolution. Understanding PR states helps teams manage workflows, coordinate code review, and interpret CI results efficiently. This guide covers the typical lifecycle and practical tips for each status.

Key PR states

* Draft
* Open
* Closed
* Merged

| State  | What it means                                             | Typical actions                                             |
| ------ | --------------------------------------------------------- | ----------------------------------------------------------- |
| Draft  | Work-in-progress PR; not ready for final review or merge. | Run CI, share early feedback, convert to open when ready.   |
| Open   | Active review and CI evaluation.                          | Reviewers comment, request changes, authors push commits.   |
| Closed | PR terminated without integration into the base branch.   | Archive discussion, reopen if needed, or create a new PR.   |
| Merged | Changes have been integrated into the base branch.        | PR conversation remains for history; branch may be deleted. |

## Draft

A draft PR indicates the author intends to share ongoing work but the changes are not yet ready for a formal review or merge. In the Draft state:

* The Merge button is disabled.
* Automated notifications to code owners are often reduced.
* CI can still run, so you can validate tests and integrations early.
* Draft PRs are ideal for seeking informal feedback and iterating without signaling completion.

Example: create a draft PR from the GitHub UI (select **Create pull request** → **Convert to draft**) or with the GitHub CLI:

```bash theme={null}
gh pr create --draft
```

<Callout icon="lightbulb">
  Use draft PRs to run CI and validate integration early. This helps catch build or test regressions before formal review.
</Callout>

## Open

An open PR signifies active collaboration: reviewers evaluate the compare branch against the base branch, leave comments, and may request changes. Authors typically respond by pushing additional commits, updating the branch, or addressing requested changes.

<Frame>
  <img alt="The image shows a pull request status indicating an open request to add 'Test' text to the file index.html, with notes about active collaboration, code review, and commit updates." />
</Frame>

During this state you should expect:

* Continuous integration to validate the branch (status checks, linters, tests).
* Reviewers to use comments, suggestions, and change requests.
* Authors to update their branch; each push updates the PR and re-triggers CI.

Best practices while a PR is open:

* Keep commits focused and use descriptive messages.
* Respond to review comments promptly and push follow-up commits rather than force-pushing when possible.
* If multiple changes are required, consider using draft status until the PR stabilizes.

## Closed

A closed PR means the proposed changes were not integrated into the base branch. Common reasons:

* The feature or fix was abandoned.
* The approach was replaced by a different solution on another branch.
* The PR was superseded or no longer relevant.

Closed PRs retain the conversation and commit history for reference and can often be reopened if required. If a PR is closed and you want to continue the work, consider:

* Reopening the PR (if appropriate).
* Creating a new branch and PR with a refined approach.

## Merged

A merged PR indicates successful integration: the commits from the compare branch were incorporated into the base branch. Merging is performed by users with appropriate write or maintain permissions. After merging:

* The PR becomes part of the base branch history.
* The PR conversation remains accessible for audits and context.
* The source branch may be deleted (depending on repository settings).

Common merge strategies:

| Strategy         | Result                                                                                    |
| ---------------- | ----------------------------------------------------------------------------------------- |
| Merge commit     | Preserves all commits and creates a merge commit on the base branch.                      |
| Squash merge     | Combines all PR commits into a single commit on the base branch.                          |
| Rebase and merge | Reapplies commits onto the base branch, preserving commit history without a merge commit. |

<Frame>
  <img alt="The image shows a pull request status indicating that a change titled &#x22;add japanease&#x22; has been merged, with a few notes about integration and permissions." />
</Frame>

<Callout icon="warning">
  Be mindful of branch protections and required status checks. Repositories may block merging until CI passes, required reviews are completed, or specific approvals are given.
</Callout>

## Quick reference and links

* GitHub Docs: [About pull requests](https://docs.github.com/en/pull-requests)
* GitHub CLI: [gh pr create documentation](https://cli.github.com/manual/gh_pr_create)

This overview should help you interpret PR lifecycle states, streamline reviews, and ensure CI and permissions are handled correctly during each stage.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/c121a210-9c0e-4e54-8868-4a2cd2e85985" />
</CardGroup>
