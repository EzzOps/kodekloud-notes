# Bad: storing secrets in source code (do not do this)
API_KEY = "sk-live-REDACTED"
```

> **warning** Never commit real secrets (API keys, passwords) to source control or paste them into prompts. Use secure credential stores, environment variables, or secret managers instead.

Also be sure you know precisely what a connector can do before enabling it. Typical connector privileges vary; understand whether a connector is read-only, can change specific items, or has full access.

<Frame>
  <img alt="The image is a diagram showing a connector symbol at the top, branching into three categories: &#x22;Read,&#x22; &#x22;Change,&#x22; and &#x22;Everything,&#x22; with corresponding icons." />
</Frame>

Connector privileges — typical breakdown

| Privilege Level  |                               Typical Actions | Example / Mitigation                                                       |
| ---------------- | --------------------------------------------: | -------------------------------------------------------------------------- |
| Read-only        |            View issues, comments, or metadata | Use for analytics or triage tools; restrict to minimal scopes              |
| Change (limited) | Post comments, update status, create branches | Grant only to specific repos/projects; use scoped tokens                   |
| Full access      |   Merge PRs, delete repos, manage permissions | Avoid unless absolutely necessary; require approval workflows and auditing |

Best practices checklist

* Add only necessary connectors and plugins.
* Use short-lived or scoped credentials and secret managers.
* Review and limit permissions; apply least privilege.
* Audit connector activity and require approvals for high-risk actions.
* Document which connectors are enabled and why.

Recap

* A connector links the Loop to a single external tool.
* A plugin is a package that can include skills, tools, and connectors, installed in one step.
* Both extend the Loop’s reach beyond local files.
* Trust matters: add only necessary connectors, keep secrets out of code and prompts, and verify connector permissions before enabling them.

Links and references

* [Model Context Protocol (MCP) — Learn more](https://learn.kodekloud.com/user/courses/fundamentals-of-mcp)
* [GitHub Documentation](https://docs.github.com/)
* [Best practices for secret management](https://12factor.net/config)

- [Watch Video](https://learn.kodekloud.com/user/courses/loop-engineering/module/6371e2a8-2e13-4841-ba89-95dd842b1bdd/lesson/31981d32-1b94-4c61-ba95-592883e630db)


# Memory

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Components/Memory/page

Explains using small persistent memory in looped systems with three tiers and five concise notes to resume work across sessions, avoid repeats, and prevent context drift.

A session ends. The loop shuts down. When it starts again the next day, what does it remember?

Without persistent memory: nothing.

It wakes up blank, unsure of the goal and unsure of what it already did. This is why memory matters for any loop-based system: memory provides the persistent notes the loop reads at the start of a session so it can resume work without redoing finished tasks or repeating past mistakes.

> **lightbulb** Keep memory small and focused. A few targeted notes let the loop resume quickly while avoiding information overload.

A memory setup can be simple.

<Frame>
  <img alt="The image depicts a concept of seamlessly resuming a process, represented by a brain icon labeled &#x22;Memory&#x22; linked to an infinity loop labeled &#x22;The Loop.&#x22; It highlights benefits like &#x22;No wasted effort&#x22; and &#x22;No starting over.&#x22;" />
</Frame>

Key ideas

* Memory is the set of notes the loop keeps across sessions so work continues across restarts.
* Without memory the loop may redo finished work or repeat a mistake it already learned from.
* With memory the loop reads its notes first, sees where it left off, and picks up right where it stopped.

What to store: three tiers

* Now — the current state: what the loop is doing right now (current goal and current task).
* Recent — short-term notes: the most recent steps and their outcomes.
* Archive — long-term record: deeper history to consult when needed.

Short-term notes should be up front; long-term archives live in the back. This keeps the important context easy to reach while still preserving full history.

So what should the notes actually hold? Five fields work well:

1. Goal — what “done” looks like, so the aim never drifts.
2. Last score — the most recent evaluation or metric from the scorer.
3. What was tried — recent attempts, especially failures, to avoid repeats.
4. What is next — the very next step to take, so the loop can start fast.
5. Waiting for a human — explicit items that require human intervention or sign-off.

A compact table makes this easy to scan:

| Field               | Purpose                                              | Example                                              |
| ------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| Goal                | Defines success for the current job                  | `Complete data import and validation`                |
| Last score          | Latest evaluation result for progress tracking       | `0.87`                                               |
| What was tried      | Recent actions and their outcomes (include failures) | `attempted schema mapping V2 — failed on edge cases` |
| What is next        | Immediate next action for the loop to take           | `Run validation on batch #42`                        |
| Waiting for a human | Items requiring human review or approval             | `Approve retry policy`                               |

Keep the five fields concise and machine-readable where possible so automated restarts can act immediately.

<Frame>
  <img alt="The image shows a list titled &#x22;Five Notes, Written Down,&#x22; with five labeled items: Goal, Last score, What was tried, What is next, and Waiting for a human." />
</Frame>

Avoid context drift
Memory must be kept current. If the loop trusts old notes after the environment, data schema, or goals have changed, it will act on a stale picture and make wrong calls. This failure mode is called context drift. The fix is simple: refresh or invalidate related notes whenever the system, goals, or external constraints change.

> **warning** Context drift is a practical failure mode: stale memory causes wrong assumptions. Update or invalidate related notes whenever the system, goals, or external constraints change.

Why this pays off
Memory lets a loop pause and pick back up where it left off without starting over. It can stop at the end of the day, persist its notes, and continue the next morning as if no time had passed. For long-running jobs that span many sessions, consistent memory is essential: individual sessions perform work well, but memory makes many sessions add up to continuous, steady progress.

<Frame>
  <img alt="The image is a diagram titled &#x22;Memory Ties It Together,&#x22; illustrating a sequence from &#x22;Memory&#x22; to &#x22;Session 3,&#x22; each represented by colored squares connected by a line, with symbols inside the squares." />
</Frame>

Recap

* Without memory, a loop forgets what it did last time.
* Use three places: now (current), recent (short-term), archive (long-term).
* Record five concise notes: Goal, Last score, What was tried, What is next, Waiting for a human.
* Keep notes current to prevent context drift.

<Frame>
  <img alt="The image is a recap with five sections labeled &#x22;Remembers,&#x22; &#x22;Three places,&#x22; &#x22;Five notes,&#x22; &#x22;Kept current,&#x22; and &#x22;Pause.&#x22; Each section has an accompanying icon." />
</Frame>

This completes the module.

- [Watch Video](https://learn.kodekloud.com/user/courses/loop-engineering/module/6371e2a8-2e13-4841-ba89-95dd842b1bdd/lesson/f7fb211f-8f21-47f1-8f6d-5ddb89a4bd2f)
