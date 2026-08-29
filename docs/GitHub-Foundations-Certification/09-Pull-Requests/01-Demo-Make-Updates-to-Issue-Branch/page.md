# Stage your change
git add path/to/file.js

# Commit with a message that references the issue or describes the change
git commit -m "Ref #1: Prevent exponential ball growth on multi-ball pickup"

# Push the changes to the branch tied to the pull request
git push origin your-branch-name
```

After pushing, the PR automatically includes the new commit(s). Refreshing the PR shows the updated diff and lets reviewers inspect the exact lines that changed.

Review re-check and approval
Once the author pushes the fix, reviewers can reopen the review flow, inspect the new commits, and approve if the changes are satisfactory. In this example Alice inspects the update and submits an approval with a brief message:

```javascript theme={null}
// The updated portion in the PR reflects the new guard and non-mutative additions
switch (type) {
  case 'multiBall': {
    // Guard to prevent excessive balls
    if (gameState.balls.length < 4) {
      const base = gameState.balls[0];
      // Create new balls from a snapshot of an existing ball — don't iterate and mutate
      gameState.balls.push({ ...base, dx: -base.dx });
      gameState.balls.push({ ...base, dy: Math.abs(base.dy) });
      gameState.powerups.multiBall.active = true;
      gameState.powerups.multiBall.activationTime = currentTime;
    }
    break;
  }
  default:
    break;
}
```

Merging the PR and post-merge actions
After approval the author (or an authorized maintainer) can merge the PR. If the PR or commit references an issue (for example, by including `#1`), GitHub will automatically close that linked issue on merge.

<Frame>
  <img alt="The image shows a GitHub pull request (PR) discussing fixes for performance issues due to multiple multi-ball power-ups in a game. The conversation includes comments and review requests with assigned reviewers and assignees." />
</Frame>

Once merged, the PR displays as merged and closed and the UI offers the option to delete the source branch.

<Frame>
  <img alt="The image shows a GitHub pull request page where a pull request titled &#x22;Refer to #1 - Fix: Prevent exponential ball growth on multi-ball pickup&#x22; has been successfully merged and closed. There is an option to delete the branch, and a section to add comments." />
</Frame>

Returning to the linked issue will show it as closed with a reference to the PR that fixed it; the issue timeline includes the PR link and the merge.

<Frame>
  <img alt="The image is a screenshot of a GitHub issue page titled &#x22;Exponential ball growth with multiple Multi-Ball power-ups causes lag,&#x22; showing various comments and actions taken to address the issue, including linking a pull request and marking it as completed." />
</Frame>

> **warning** If your repository enforces branch protection or requires multiple approvals, make sure you understand those rules before merging. Deleting the source branch is optional—only delete it when you no longer need it for additional work.

Quick reference: review outcomes and what they mean

| Review action   | Effect on PR                          | When to use it                           |
| --------------- | ------------------------------------- | ---------------------------------------- |
| Comment         | Does not block merge                  | General feedback or discussion           |
| Approve         | Marks PR as ready to merge            | Changes are verified and acceptable      |
| Request changes | Blocks merging until changes are made | Required fixes or regressions identified |

Helpful links and references

* [GitHub Pull Requests documentation](https://docs.github.com/en/pull-requests) — official docs for reviewing and merging
* [GitHub Code review guides](https://docs.github.com/en/get-started/using-github/about-code-reviews) — tips for reviewers and authors

Summary

* Use the plus icon to comment on a single line; select multiple lines to create a multi-line comment that references a block of code.
* Start a review to collect multiple inline comments before submitting (you can Comment / Approve / Request changes).
* Avoid mutating arrays while iterating — instead, snapshot an element or collect new items separately and cap additions to prevent exponential growth.
* Push fixes to the same branch; the PR will update automatically so reviewers can re-check and approve before merging.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/406788e6-e169-4a38-8163-97da3f8d0295)


# Demo Make Updates to Issue Branch

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Demo-Make-Updates-to-Issue-Branch/page

Guide diagnosing and fixing exponential ball duplication caused by a multiBall power-up, with a safe array-copy fix and Git workflow for applying, committing, and pushing the change

This lesson walks through diagnosing and fixing issue #1 in the BlockBuster repository: exponential growth of balls when the `multiBall` power-up is applied. It includes the root cause analysis, a safe fix, and the Git workflow for fetching, checking out, committing, and pushing the change.

Repository / user context

* Repo: BlockBuster
* User: GH900
* Issue: #1 — exponential ball growth caused by the `multiBall` power-up

Problem summary
The `multiBall` handler duplicates all current balls by iterating `gameState.balls` and pushing clones into the same array. Because the code mutates the array while iterating it, newly pushed balls are also iterated, causing exponential growth on repeated activation.

Reproduction (relevant snippet)

```javascript theme={null}
// script.js:
case 'multiBall':
if (gameState.balls.length < 5) { // This check is insufficient
    gameState.balls.forEach(ball => {
        gameState.balls.push({...ball});
    });
}
```

Root cause

* Mutating (pushing into) an array while iterating it with `forEach` causes the loop to process elements added during iteration.
* The guard `if (gameState.balls.length < 5)` only checks at the start; pushing inside the loop invalidates the assumption and allows the array to grow beyond intended limits.

Best practice note

> **lightbulb** When modifying arrays you are iterating over, iterate over a shallow copy (for example, `arr.slice()`) or use an index-based loop that references the original length. Always enforce an explicit maximum when duplicating entities to prevent runaway growth.

Safe fix

* Iterate over a copy of the original balls so newly added balls are not reprocessed.
* Apply a strict upper bound (MAX\_BALLS) to stop duplication once reached.

Corrected implementation:

```javascript theme={null}
// script.js:
case 'multiBall': {
  const MAX_BALLS = 5;
  // Copy the current balls so we don't iterate newly added ones
  const originals = gameState.balls.slice();

  // Add clones of original balls up to MAX_BALLS total
  for (const ball of originals) {
    if (gameState.balls.length >= MAX_BALLS) break;
    gameState.balls.push({ ...ball });
  }
  break;
}
```

This ensures:

* Only balls that existed at activation are duplicated.
* The total number of balls never exceeds `MAX_BALLS`.

Working with the issue branch (Git workflow)
Fetch the remote branch, inspect it locally, check it out to track the remote, apply the fix, test, then commit and push.

1. Fetch remote branches

```bash theme={null}
git fetch
