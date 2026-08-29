# create a new worktree (creates branch 'try-login' and checks it out)
$ git worktree add ../try-login -b try-login
Preparing worktree (new branch 'try-login')
HEAD is now at 9b8c25e
```

List all worktrees and where they live:

```bash theme={null}
$ git worktree list
/projects/main-project  9b8c25e [main]
/projects/try-login     9b8c25e [try-login]
```

Run multiple worktrees side-by-side (no file clashes because each has its own working directory):

```bash theme={null}
# add independent worktrees for a bugfix and a feature
$ git worktree add ../fix-bug -b fix-bug
Preparing worktree (new branch 'fix-bug')
HEAD is now at 9b8c25e

$ git worktree add ../new-feature -b new-feature
Preparing worktree (new branch 'new-feature')
HEAD is now at 9b8c25e
```

Remove a worktree when it's done:

```bash theme={null}
# remove a worktree when it's finished
$ git worktree remove ../try-login
Removing worktree '../try-login'... done
```

Git protects you from accidental deletion: it will refuse to remove a worktree that contains modified or untracked files.

```bash theme={null}
$ git worktree remove ../try-login
fatal: '../try-login' contains modified or untracked files
```

If you intentionally want to discard a worktree and all its changes, add `--force`:

```bash theme={null}
# force-remove a messy copy on purpose
$ git worktree remove --force ../try-login
Removing worktree '../try-login'... done
```

If you manually delete a worktree folder from disk but Git still lists it, clear stale entries with:

```bash theme={null}
# clear stale worktree entries after a manual delete
$ git worktree prune
Cleaning up worktree entries... done
```

> **lightbulb** Worktrees share the same repository history (the main `.git`) while keeping separate working trees. The small `.git` file inside each worktree points Git back to the shared data, which is why creating a worktree is inexpensive.

The payoff

* If a try fails, the usual cost is simply removing the worktree. The main repository remains clean.
* Worktrees make automated experiments and hands-off loops safe: failed tries are disposable, and multiple experiments can run concurrently without interfering with each other.

<Frame>
  <img alt="The image illustrates the concept of &#x22;Worktrees,&#x22; showing a comparison between a &#x22;Messy copy&#x22; and the &#x22;Main code&#x22; that is &#x22;clean and safe,&#x22; with an arrow labeled &#x22;Remove --force&#x22; suggesting a process to maintain safety." />
</Frame>

Quick recap

* A worktree is a separate working copy that shares the repository history.
* Use `git worktree add` to create one, `git worktree list` to display them, and `git worktree remove` to delete when finished.
* Add `--force` to discard a worktree with local changes, and run `git worktree prune` to clean up stale entries.
* Multiple subagents or experiments can run in parallel without clashing; failed attempts are cheap to throw away.

<Frame>
  <img alt="The image is a recap slide explaining Git worktree commands, including how to add, list, and remove worktrees. It highlights using --force and mentions multiple worktrees can run at once while keeping the main branch clean." />
</Frame>

Links and references

* [Git worktree documentation](https://git-scm.com/docs/git-worktree)
* [Git reference manual](https://git-scm.com/docs)
* For detailed workflows and best practices, search for "git worktree workflows" or consult your CI system's docs for integrating ephemeral worktrees into automated loops.

- [Watch Video](https://learn.kodekloud.com/user/courses/loop-engineering/module/6371e2a8-2e13-4841-ba89-95dd842b1bdd/lesson/9a47e6fc-677b-4583-81f9-3ef4cea9bdea)


# Wrap Up and Conclusion

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Conclusion/Wrap-Up-and-Conclusion/page

Guide to building AI coding agents using a try‑test‑fix‑save loop, prioritizing goal and scorekeeper, adding components only as needed for reliable automation.

That completes the loop — from start to finish.

Step back and take in how the pieces connect. An AI coding agent is built around a compact, repeating cycle: `try`, `test`, `fix`, `save`. This cycle runs continuously until the agent reaches its goal. Two immutable foundations must be defined first in every project:

* A clear goal that specifies what “done” looks like.
* A scorekeeper that measures what “correct” means.

Only after those foundations should you add other components. Each additional part exists to solve a concrete problem; add it only when needed.

Callouts for quick reference:

> **lightbulb** Start with the goal and the scorekeeper in every project. Get one small, saved win (a green state) early — it reduces risk and provides a reliable baseline for iteration.

Core components and their roles

* Automations — repeat the loop’s work reliably and without drift.
* Worktrees — create safe branches or disposable copies for experiments.
* Skills — package reusable procedures, heuristics, or models.
* Connectors and plugins — enable interaction with external tools, APIs, or services.
* Sub-agents — delegate focused responsibilities or subtasks to specialized agents.
* Memory — persist notes, context, checkpoints, and other state across sessions.

For clarity, here’s a compact reference table:

| Component            | Purpose                              | Example                                           |
| -------------------- | ------------------------------------ | ------------------------------------------------- |
| Automations          | Ensure repeatable execution of tasks | `CI pipeline that runs tests and saves artifacts` |
| Worktrees            | Isolate experimental changes         | `branching or sandboxed environments`             |
| Skills               | Reusable actions or knowledge        | `linting skill, API-calling skill`                |
| Connectors & Plugins | External integrations                | `GitHub, Slack, cloud provider APIs`              |
| Sub-agents           | Single-responsibility workers        | `data-cleaning agent, test-generation agent`      |
| Memory               | Persistent context & checkpoints     | `short-term cache, long-term log, artifact store` |

Design order and practical rules

1. Define the goal and the scorekeeper first. Without them, the loop cannot measure progress.
2. Get one small win saved (green) quickly — this becomes your rollback/safety point.
3. Add components in this sequence only as problems demand them: Automations → Worktrees → Skills → Connectors/Plugins → Sub-agents → Memory.
4. Keep each addition minimal and justified by a measurable need.

Engineering habits that keep loops healthy

* Make small, incremental changes and `save` often to ensure rollback points exist.
* Inspect the actual outputs shipped by the loop — don’t rely only on the score flipping green.
* Decide up front when the loop should stop, and define the criteria for human handoff.

> **warning** Automate carefully. Over-automation without clear stop conditions can produce brittle behavior. Define explicit termination or escalation rules to ensure safe handoffs to humans.

A short, practical cycle example

```text theme={null}
try -> test -> fix -> save
```

Aim to make each iteration short and measurable. The loop’s objective is to steer itself toward the goal, not to remove humans from the picture entirely.

Final thought
The purpose of this framework is not to memorize a list of parts. It is to learn to think in loops: design compact cycles that detect, measure, and correct their behavior reliably. That shift — from manual steering to designing dependable cycles — is the key skill.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) — for worktree and environment isolation concepts
* [Continuous Integration (CI) Practices](https://martinfowler.com/articles/continuousIntegration.html) — for automation and frequent saves
* [Designing Reliable Systems](https://en.wikipedia.org/wiki/Resilience_\(engineering\)) — resilience and safe handoffs

- [Watch Video](https://learn.kodekloud.com/user/courses/loop-engineering/module/e9e7e00f-c818-4786-9192-b1ebbae551d6/lesson/13c623bc-c1cf-4d11-8cb1-fc4857757dfc)
