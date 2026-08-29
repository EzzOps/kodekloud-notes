# Automations

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Components/Automations/page

Explains automation in loop engineering by repeating tasks, evaluating results, applying incremental fixes, saving progress, using timer or run-until-done loops, and enforcing guardrails for safe improvement.

An automation is the engine that powers a loop — it runs tasks repeatedly, evaluates results, and acts on those results until the work is done. Automation turns a one-off try into a reliable loop and is the first of the six parts of loop engineering.

Common loop-triggering commands in AI tooling look like:

```bash theme={null}
/go          run until done
/loop        repeat on a schedule
/ralph-loop  repeat a prompt
```

The core idea is simple: repeat the same prompt (or task), check the result, act on it, and keep repeating until a clear stop signal appears. Repeat, check, repeat — that is automation.

How one pass through the loop works

1. Run the test (or produce an output).
2. Read the score (evaluate the result against a metric).
3. Fix one small failing thing — not everything at once. Focused, incremental fixes are key.

<Frame>
  <img alt="The image shows a three-step process for automation: &#x22;Run the test,&#x22; &#x22;Read the score,&#x22; and &#x22;Fix one thing.&#x22; Each step is visually represented with an icon and numbered sequentially." />
</Frame>

4. Save the good work (commit or persist the improvement). Then start the next pass. Small steps, saved frequently, compound into rapid, reliable progress.

<Frame>
  <img alt="The image illustrates a four-step automation process: Run the test, Read the score, Fix one thing, and Save the work, emphasizing taking small, frequent steps." />
</Frame>

Two common loop styles

* Timer loop: runs on a schedule (every few minutes, hourly, nightly). Acts like a cron job and is best for continuous monitoring (e.g., watching for new issues and acting on them).
* Run-until-done loop: repeats immediately as needed until a finish signal appears, then stops. Requires a precise definition of “done” (for example, “all checks pass”).

> **lightbulb** Choose a timer loop for ongoing monitoring and maintenance. Choose a run-until-done loop when you have a concrete goal and a reliable finish signal (for example, all checks pass).

<Frame>
  <img alt="The image compares two common loop styles: a Timer Loop, which reruns on a schedule, and a Run-until-done Loop, which continues until a goal is met." />
</Frame>

Quick reference: loop styles

| Loop style     | Schedule                        | Best for                                       | Example trigger                     |
| -------------- | ------------------------------- | ---------------------------------------------- | ----------------------------------- |
| Timer loop     | Scheduled intervals (cron-like) | Continuous monitoring, periodic checks         | `every 5 minutes` or cron           |
| Run-until-done | Immediate repeats until finish  | Short-term automation with clear finish signal | `/go` or `run until all tests pass` |

Guardrails for a repeating engine

A repeating engine can be extremely effective — and potentially destructive — so add guardrails. Two rules matter most:

1. The score must only go up, never down. If a change reduces the score, the loop should undo that change automatically. Progress only counts when it holds.
2. Fix breaks before adding more. If something is broken, repair it first; layering new work on a broken base compounds risk.

<Frame>
  <img alt="The image illustrates a concept called &#x22;Loop Guardrails&#x22; showing a graph where the score continually increases and never decreases, emphasizing the idea with labels &#x22;It holds&#x22; and &#x22;Undo it.&#x22;" />
</Frame>

> **warning** If an automated step decreases the score, ensure the loop can roll back that change automatically. Never accept regressions as forward progress.

<Frame>
  <img alt="The image is a guide from KodeKloud titled &#x22;Loop Guardrails,&#x22; which emphasizes fixing breaks before adding more, illustrated with a &#x22;Repair first&#x22; flowchart and a &#x22;Pile it on&#x22; section." />
</Frame>

When these guardrails are enforced, the engine can run autonomously: it makes consistent, incremental improvements, persists each win, and stops when the finish signal appears. That is the purpose of automation — continuous progress without manual supervision.

Recap

* Automation is the engine that repeats work and evaluates outcomes.
* Each pass: run the test, read the score, fix one small break, and save.
* Timer loops repeat on a schedule; run-until-done loops stop when the goal is met.
* Guardrails ensure the score never regresses and that fixes come before new additions.

<Frame>
  <img alt="The image is a recap slide featuring four key concepts: Automation, Each pass, Two styles, and Guardrails, each with a brief description." />
</Frame>

The score should go up, never down, and bugs get fixed first.

Links and references

* Cron (scheduling): [https://en.wikipedia.org/wiki/Cron](https://en.wikipedia.org/wiki/Cron)
* Continuous integration concepts: [https://en.wikipedia.org/wiki/Continuous\_integration](https://en.wikipedia.org/wiki/Continuous_integration)

- [Watch Video](https://learn.kodekloud.com/user/courses/loop-engineering/module/6371e2a8-2e13-4841-ba89-95dd842b1bdd/lesson/0bc57d3f-b47f-4727-966a-4044049ae599)
