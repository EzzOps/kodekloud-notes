# The Scorekeeper

Source: https://notes.kodekloud.com/docs/Loop-Engineering/What-Is-a-Loop/The-Scorekeeper/page

Explains the importance of an objective, automated, fast, and tamperproof scorekeeper to measure and guide iterative loops and prevent gaming

Imagine a game with no scoreboard.

Both teams play hard, but no one can tell who is winning. That is what a loop without a scorekeeper feels like: it can run forever, but it never truly knows whether it’s making progress or doing the right thing. The scorekeeper defines what “correct” means.

<Frame>
  <img alt="The image depicts a soccer game without a scoreboard, illustrating the concept that although both teams play hard, no one can tell who is winning. Accompanying text explains that a loop without a scorekeeper runs continuously without knowing if it's winning." />
</Frame>

What is a scorekeeper?

The scorekeeper is the mechanism that converts work into a measurable result the loop can read. It might be a test suite, a build that must pass, a checklist, or a rubric another agent uses to grade work. By returning a score each cycle, the scorekeeper tells the loop whether it is improving or regressing.

<Frame>
  <img alt="The image explains the concept of a &#x22;Scorekeeper,&#x22; defining what &#x22;correct&#x22; means using three elements: Test Suite, A Build That Passes, and Checklist or Rubric." />
</Frame>

Why the score matters

On every loop iteration the system runs the scorekeeper and reads the result. A higher score means real progress; a lower score signals a regression. Without this signal the loop is blind—it cannot distinguish true progress from noise and cannot operate reliably on its own.

<Frame>
  <img alt="The image highlights the importance of a scorekeeper by illustrating that without one, a loop becomes blind and unable to differentiate real progress from noise." />
</Frame>

Traits of a trustworthy scorekeeper

A scorekeeper is only useful if it’s reliable. The four essential traits are:

| Trait     | Why it matters                                                                      |
| --------- | ----------------------------------------------------------------------------------- |
| Objective | The same work yields the same result every time; avoid nondeterminism or guesswork. |
| Automatic | Runs with a single command or CI trigger; no manual steps required.                 |
| Fast      | Quick checks enable frequent scoring and rapid detection of failures.               |
| Clear     | Produces a simple, unambiguous score so the loop knows exactly how it’s doing.      |

Objective, automatic, fast, and clear — these traits turn a plain test into a trustworthy judge.

<Frame>
  <img alt="The image outlines four traits of a good scorekeeper: objective, automatic, fast, and clear. Each trait is accompanied by a brief description and an icon." />
</Frame>

Make the score hard to fake

If the loop can pass the score by cheating—faking outputs, changing the tests, or skipping essential work—the score becomes a lie. A gamable score leads to false confidence: the loop believes it succeeded while the system remains broken.

<Frame>
  <img alt="The image describes a flawed system where cheating to pass a score leads to false success, resulting in a broken tool and unreliable outcomes." />
</Frame>

Simple mitigations

* Keep some checks held out (hidden) from the loop during normal iterations to prevent overfitting to visible tests. Use held-out checks as final verification.
* Make critical checks tamper-proof—store them where the loop cannot modify them (e.g., in a separate repository or protected CI job).
* Ensure logs and artifacts needed for verification are immutable or auditable.

<Frame>
  <img alt="The image illustrates a concept titled &#x22;Simple Tricks&#x22; about keeping some checks held out to avoid overfitting, featuring graphics of a loop and checkmarks." />
</Frame>

<Callout icon="warning">
  Never allow the loop to weaken or edit the scorekeeper. If the system can lower the bar, it will choose the easiest path to pass rather than actually fix the work.
</Callout>

Protecting the scorekeeper

Treat the scorekeeper as an oracle: keep its definition and implementation separate from the loop itself. Use access controls, read-only storage, and guarded CI jobs so the loop cannot tamper with tests, rubrics, or scoring logic.

<Frame>
  <img alt="The image illustrates a concept called &#x22;Simple Tricks&#x22; where a bar is lowered to allow something to pass by cheating, rather than fixing the work, with a note about respecting the oracle skill covered in Module 2." />
</Frame>

Rule of thumb

Write the scorekeeper before you start the loop. Defining the score up front makes “done” explicit and lets you verify progress objectively as you iterate.

<Frame>
  <img alt="The image provides a &#x22;Rule of Thumb&#x22; with two steps: first, &#x22;Write the scorekeeper,&#x22; accompanied by a checklist icon, and second, &#x22;The goal says what 'done' looks like,&#x22; illustrated by a target icon." />
</Frame>

<Callout icon="lightbulb">
  Write the scorekeeper first. Define the goal clearly, then use automated, objective checks to measure progress. Protect those checks from being modified by the loop.
</Callout>

Recap

* The scorekeeper decides what is correct and is the heart of any reliable loop.
* A good scorekeeper is objective, automatic, fast, and clear.
* Make the score hard to fake: hold out checks, protect scoring logic, and prevent the loop from editing tests.

<Frame>
  <img alt="The image features a &#x22;Scorekeeper&#x22; graphic displaying a score of 72, with related attributes like &#x22;Objective,&#x22; &#x22;Automatic,&#x22; &#x22;Fast,&#x22; &#x22;Clear,&#x22; and &#x22;Hard to fake&#x22; highlighted around it." />
</Frame>

Quick checklist

* Write tests/rubrics before development.
* Automate scoring in CI.
* Keep some tests secret (held-out).
* Store scoring logic read-only and audit changes.
* Monitor score trends, not just single-pass results.

Further reading and references

* [Test-Driven Development (TDD) overview](https://en.wikipedia.org/wiki/Test-driven_development)
* [Continuous Integration best practices](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration)
* [Designing reliable test suites](https://martinfowler.com/articles/practical-automation.html)

The loop can only run well when it has a trustworthy judge.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/loop-engineering/module/63fbab29-f6e1-497c-ba71-cff4793c2731/lesson/60e19746-b666-45b4-be5b-a7eb52de95b1" />
</CardGroup>
