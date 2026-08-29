# The Whole Loop in Motion

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Tie-It-All-Together/The-Whole-Loop-in-Motion/page

Explains an automated iterative loop using goals, scorekeepers, memory, worktrees, skills, and helpers to make small validated changes until a goal is achieved, with human review for risky decisions

So far, each part of the system worked independently. Now we’ll run a complete loop from start to finish and show exactly where each of the six parts fits in the cycle.

Every loop requires two things before anything else runs:

* A clear goal — a precise statement of what “done” looks like.
* A scorekeeper — an objective measurement that proves whether the work improved or regressed.

The goal points the work in the right direction; the scorekeeper verifies progress. Nothing else should execute until these two are defined.

Now the cycle begins.

## Step 1 — Read memory

The loop first reads its memory: the current goal, the most recent score, what was already tried, and the next planned step. This allows the loop to resume quickly and avoid repeating work or making contradictory changes.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Step 1 – Read Memory,&#x22; showing a process from &#x22;The Loop&#x22; to &#x22;Memory&#x22; towards &#x22;The goal.&#x22; It features icons representing an infinity loop, a brain, and a target." />
</Frame>

## Step 2 — Move into a worktree

The loop creates a safe, isolated copy of the repository to experiment in. Using a Git worktree isolates changes from the main branch so experiments can be discarded if they fail without contaminating the primary codebase.

* Benefit: fast, disposable experiments
* Risk mitigation: keeps main branch clean
* Reference: [git-worktree documentation](https://git-scm.com/docs/git-worktree)

<Frame>
  <img alt="The image illustrates &#x22;Step 2 – Move Into a Worktree,&#x22; depicting a Git workflow with a branch off the main timeline to a worktree labeled &#x22;A safe copy.&#x22;" />
</Frame>

## Step 3 — Lean on a skill

The task is mapped to a skill description that prescribes reproducible steps. Skills codify the know-how required to complete tasks, ensuring consistent behavior and predictable outcomes each time the loop needs to act.

<Frame>
  <img alt="The image is a flowchart illustrating &#x22;Step 3 – Lean on a Skill,&#x22; showing a task leading to a related skill with numbered steps." />
</Frame>

## Step 4 — Make one small change and check the score

Apply a minimal, focused change that is likely to move the score in the right direction. Immediately evaluate the change against the scorekeeper:

* If the score improves → accept and persist the change.
* If the score worsens → rollback, diagnose, and try a different small change.

Small, incremental changes reduce risk and produce clear feedback.

<Frame>
  <img alt="The image is a diagram illustrating &#x22;Step 4 - One Small Change,&#x22; featuring an orange icon labeled &#x22;The Change&#x22; and a green icon labeled &#x22;The Scorekeeper.&#x22; There is a connection between the two icons, indicating a process or relationship." />
</Frame>

## Helpers: sub-agents and connectors

After a change is validated, helpers can augment the loop:

* A sub-agent provides a second set of eyes for review or focused tasks.
* A connector reaches outside the loop to fetch external context (for example, an issue from a tracker or a [pull request on GitHub](https://docs.github.com/en/pull-requests)).

These helpers integrate seamlessly when the work is ready for broader context or additional checks.

<Frame>
  <img alt="The image illustrates a process with three components: &#x22;A Subagent&#x22; described as &#x22;A second set of eyes,&#x22; &#x22;The Loop,&#x22; and &#x22;A Connector&#x22; described as &#x22;Reach outside,&#x22; all part of a section titled &#x22;The Helpers Join in.&#x22;" />
</Frame>

## Human judgment and safety gates

A robust loop does not run blind. If the loop encounters risky choices or subjective judgments, it stops and hands the state to a human reviewer. The handoff includes the full context so humans can make informed decisions about taste, architecture, or other subjective matters. Automation handles repeatable, checkable work; humans remain responsible for judgment.

Automation runs the cycle repeatedly, persisting each validated improvement until the goal is achieved. At that point all six parts have been involved:

* Memory
* Worktree
* Skill
* Scorekeeper
* Sub-agent / Connector
* Automation

These form a complementary system: the goal and scorekeeper are the foundation; the other elements make the loop safer, more focused, and more capable.

<Frame>
  <img alt="The image titled &#x22;The Base and the Add-Ons&#x22; features three main elements: &#x22;Automation&#x22; with a repeat icon, &#x22;The Goal&#x22; with a target icon, and &#x22;The Scorekeeper&#x22; with a checkmark icon, connected by a horizontal bar and an infinity symbol." />
</Frame>

## Full-cycle recap

Start-to-finish sequence:

1. Define the goal and the scorekeeper (required).
2. Read memory.
3. Create a worktree.
4. Lean on a skill.
5. Make one small change.
6. Check the score.
7. Let a sub-agent review (if needed).
8. Use a connector to reach external systems (if needed).
9. Repeat via automation until the goal is met.
10. Stop and hand over to a human whenever a choice requires real judgment.

<Frame>
  <img alt="The image depicts a diagram labeled &#x22;The Full Cycle,&#x22; illustrating a process flow with components named The Base, Memory, Worktree, Skill, Change, Check, Subagent, and Connector, connected in a loop." />
</Frame>

| Component             |                                 Role | Example                                        |
| --------------------- | -----------------------------------: | ---------------------------------------------- |
| Goal                  |            Directs what “done” means | `Fix failing tests and restore 100% pass rate` |
| Scorekeeper           |                 Measures correctness | `unit test pass/fail, performance metric`      |
| Memory                |            Stores state between runs | `last score, previous attempts, next action`   |
| Worktree              |      Isolated experiment environment | `git worktree add -b try-change`               |
| Skill                 |           Encoded steps for the task | `lint-and-fix-style`, `refactor-function`      |
| Sub-agent / Connector | Reviews and fetches external context | `code review sub-agent`, GitHub issue fetcher  |

<Callout icon="lightbulb">
  The most important two elements are the goal and the scorekeeper — they direct and validate every step in the loop. Build those first, then add the other parts to improve safety, focus, and reach.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/loop-engineering/module/e7187c25-1255-491d-84dd-87fedf03d4c1/lesson/efe6a81c-1939-4dcf-83e2-218bec535207" />
</CardGroup>
