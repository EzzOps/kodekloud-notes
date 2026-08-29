# Demo Explain How to Create a Branch From an Issue

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Issues/Demo-Explain-How-to-Create-a-Branch-From-an-Issue/page

Explains creating GitHub branches from issues, fetching them locally, and preventing exponential multi-ball duplication bug

Learn how and why to create a branch from a GitHub Issue, then fetch and work on that branch locally. Creating branches from issues helps keep `main` stable while you implement fixes or features, and it links your code changes directly to the issue for clearer traceability.

## Why create a branch from an Issue?

* Keeps the `main` branch stable and deployable.
* Attaches context (the issue) to the work you do, improving traceability.
* Simplifies producing a focused pull request that references the issue.

## Create a branch from the GitHub Issues UI

1. Open the Issue you want to work on.
2. Locate the "Development" section in the issue sidebar.
3. Click "Create branch".
4. Choose the destination repository and the source branch (commonly `main`).
5. Confirm the branch name or edit it before creation.

> **lightbulb** GitHub suggests a branch name by default using the issue number and a slugified title (for example, `1-fix-exponential-growth-bug`). You can rename it to match your repo's branch naming conventions (e.g., `issue/1/multi-ball-fix`).

When GitHub creates the branch it also displays the commands you can run locally to fetch and check it out.

## Fetch and check out the branch locally

Use either `git checkout` or `git switch --track`, depending on your Git version and preference. Example commands provided by GitHub:

```bash theme={null}
git fetch origin
git checkout 1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
```

Or using `git switch`:

```bash theme={null}
git fetch origin
git switch --track origin/1-exponential-ball-growth-with-multiple-multi-ball-power-ups-causes-lag
```

Quick reference of common commands:

|                                        Purpose | Command                                          |
| ---------------------------------------------: | :----------------------------------------------- |
|                          Fetch remote branches | `git fetch origin`                               |
|           Checkout a remote branch (older Git) | `git checkout <remote-branch-name>`              |
| Checkout and track a remote branch (newer Git) | `git switch --track origin/<remote-branch-name>` |
|                    Push local branch to origin | `git push -u origin <local-branch-name>`         |

Once checked out, the new branch will reflect `main` at the moment it was branched.

## Example issue: Multi-ball power-up causing exponential growth

Below is a sample issue describing an in-game bug: activating a multi-ball power-up duplicates balls in a way that leads to exponential growth and performance issues.

Problematic code:

```javascript theme={null}
// Problematic code that causes exponential growth of balls
case 'multiBall':
    if (gameState.balls.length < 5) { // This check is insufficient
        gameState.balls.forEach(ball => {
            gameState.balls.push({ ...ball });
        });
    }
    break;
```

Why this is problematic:

* The `forEach` iterates over `gameState.balls` while the loop body pushes new balls into the same array.
* Adding clones during iteration allows newly pushed balls to be iterated later in the same activation, causing the array to grow exponentially: 1 → 2 → 4 → 8...
* The guard `gameState.balls.length < 5` only gates entering the duplication block; it does not prevent overshooting the intended `MAX_BALLS`.

> **warning** This pattern leads to exponential growth of the array and can quickly exceed intended limits, causing performance degradation or crashes. Always avoid mutating the iterated array in ways that change its length during the loop.

## Safer implementation

Capture a snapshot of the array before duplicating and enforce a maximum cap while adding clones only up to the limit:

```javascript theme={null}
// Safer implementation: duplicate only the original balls, and enforce a cap
case 'multiBall': {
    const MAX_BALLS = 5;
    const originalBalls = [...gameState.balls]; // snapshot of balls before duplication
    for (let i = 0; i < originalBalls.length; i++) {
        if (gameState.balls.length >= MAX_BALLS) break;
        gameState.balls.push({ ...originalBalls[i] });
    }
    break;
}
```

Why this works:

* `originalBalls` is a shallow copy taken before adding any new balls, so newly appended balls are not re-duplicated in the same activation.
* The loop checks `gameState.balls.length` on each iteration and breaks once `MAX_BALLS` is reached, preventing overshoot.

## Complete workflow summary

| Step | Action                                                                                              |
| ---: | :-------------------------------------------------------------------------------------------------- |
|    1 | Create a branch from the Issue using the GitHub Issues UI (or create it manually).                  |
|    2 | Fetch and check out the branch locally (`git fetch origin` + `git switch --track origin/<branch>`). |
|    3 | Implement and test your changes on the branch.                                                      |
|    4 | Commit and push the branch (`git push -u origin <branch>`).                                         |
|    5 | Open a pull request that links to the original issue and add reviewers.                             |
|    6 | Address feedback, update the branch as needed, and merge to `main` once approved.                   |

## Links and References

* [GitHub Issues](https://docs.github.com/en/issues)
* [Git basics — Branching](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
* [Git push documentation](https://git-scm.com/docs/git-push)

By creating branches directly from issues and following a guarded duplication pattern shown above, you keep `main` stable and avoid bugs that can lead to exponential growth and performance problems.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/3105bbb3-1ddf-433d-9b4f-15a905853817/lesson/76b1ab65-3f92-494f-9b1d-e1308478ce04)
