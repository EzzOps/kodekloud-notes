# Demo How to Comment on a Posted Link to a Line or Lines of Code From a File

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Demo-How-to-Comment-on-a-Posted-Link-to-a-Line-or-Lines-of-Code-From-a-File/page

Guide to reviewing GitHub pull requests, adding inline and multi line comments, requesting changes, fixing code by avoiding array mutation during iteration, and merging updated commits.

In this lesson you'll learn how to leave inline comments on specific lines (or a contiguous selection of lines) inside a GitHub pull request (PR), review those comments, apply fixes in a follow-up commit, and complete the merge. This walkthrough uses a small game project example where a multi-ball power-up could unintentionally cause exponential growth of the `balls` array.

Open the pull request that needs review. In this example the PR is awaiting review from Alice and Siddharth Barahalikar.

<Frame>
  <img alt="This image shows a GitHub pull request titled &#x22;Fix: Prevent exponential ball growth on multi-ball pickup,&#x22; addressing performance issues with power-ups in a project. The pull request is open and awaiting review." />
</Frame>

Switch to Alice’s account to perform the review. Alice sees a notification for a requested review; clicking it opens the PR where she can read the description, comments, and examine the Files changed tab. She starts by inspecting the changed code.

Example of the buggy implementation under review (this mutates the array during iteration which may lead to exponential growth):

```javascript theme={null}
// Buggy example: mutates the array while iterating and may cause exponential growth
switch (type) {
  case 'multiBall':
    if (gameState.balls.length < 5) {
      gameState.balls.forEach(ball => {
        gameState.balls.push({ ...ball });
      });
    }
    // Add two new balls with slightly different trajectories
    gameState.balls.push({ ...gameState.balls[0], dx: gameState.balls[0].dx });
    gameState.balls.push({ ...gameState.balls[0], dy: Math.abs(gameState.balls[0].dy) });
    gameState.powerups.multiBall.active = true;
    gameState.powerups.multiBall.activationTime = currentTime;
    break;
}
```

How to add inline comments and multi-line comments

* Click the plus icon to the left of a line to open a small comment box tied to that specific line.
* To comment on multiple contiguous lines, click and drag to select them — the resulting comment will reference the selection.
* Comments can be standalone or grouped into a pending review. Starting a review collects comments until you submit them as a single review action.

Sample inline reviewer comment (added to the PR):\
"This block mutates `gameState.balls` while iterating — that can cause exponential growth. Please avoid mutating the array while iterating and also ensure we cap the total number of balls."

Review workflows and submission options
When you start a review, comments are added as pending on the PR. When submitting the review you choose one of three outcomes:

* Comment — general feedback that does not block merging
* Approve — indicates the PR is ready to merge
* Request changes — prevents merging until required changes are made

In this scenario, Alice requests changes and suggests a safe, non-mutative approach that caps the number of balls. One corrected implementation applied in a follow-up commit looks like this:

```javascript theme={null}
function activatePowerUp(type) {
  switch (type) {
    case 'multiBall': {
      // Only add new balls if we have fewer than 4 (prevents excessive growth)
      if (gameState.balls.length < 4) {
        // Use a base ball to create new balls, don't mutate during iteration
        const base = gameState.balls[0];
        gameState.balls.push({ ...base, dx: -base.dx });                // mirrored dx
        gameState.balls.push({ ...base, dy: Math.abs(base.dy) });      // ensure positive dy
        gameState.powerups.multiBall.active = true;
        gameState.powerups.multiBall.activationTime = currentTime;
      }
      break;
    }
    default:
      break;
  }
}
```

> **lightbulb** Avoid mutating an array while iterating over it (for example, pushing into the same array inside a `forEach`). Instead, collect new items separately or push a known small number of items derived from an existing base element.

After Alice submits a "request changes" review with inline comments, the PR UI reflects that a change was requested. The PR page also provides options to dismiss the review, ask the reviewer to re-check, or see who requested changes.

<Frame>
  <img alt="The image shows a GitHub pull request interface where a user named &#x22;sid-gh900&#x22; wants to merge commits into a main branch. There is a requested change, two pending reviews, and no conflicts with the base branch for merging." />
</Frame>

Author applies the suggested fix locally
Switch back to the author’s account (Siddharth). He reads Alice’s comments and updates the code locally. Typical local workflow to stage, commit, and push the fix to the same PR branch:

```bash theme={null}
