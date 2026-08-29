# Sub agents

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Components/Sub-agents/page

Using isolated sub-agents to offload single focused tasks from a main loop, improving speed, safety, and parallelism while keeping workspace clean and enabling maker-and-checker validation.

Some jobs are large enough to pull the main loop off track. The usual fix is to hand that job to a helper — a sub-agent.

A sub-agent is a helper process the main loop starts to handle a single, well-defined task. The main loop does not stop what it is doing: it spawns the sub-agent, gives it one clear instruction, and continues. The key word is one: a sub-agent is most effective when given a single, focused job to finish.

What makes a sub-agent different from the main loop is that it starts fresh. It receives its own clean workspace and instructions and does not inherit the main loop’s long history. The sub-agent works on its one job, and then returns only the final answer. The main loop never sees the messy middle, just the result.

<Frame>
  <img alt="The image depicts a diagram showing &#x22;The Main Loop&#x22; and &#x22;The Subagent&#x22; with their respective features, illustrating a process titled &#x22;It Starts Fresh.&#x22; The Main Loop has an infinity icon and features labeled &#x22;Answer&#x22; and &#x22;Long history,&#x22; while the Subagent, depicted with a robot icon, has features &#x22;Clean workspace&#x22; and &#x22;Own instructions.&#x22;" />
</Frame>

A simple instruction payload you might send to a sub-agent looks like this:

```json theme={null}
{
  "task": "search_codebase",
  "scope": "src/",
  "query": "functionName",
  "max_results": 10,
  "access": "read-only"
}
```

Think of a manager who assigns a task to a specialist. The specialist goes off, does the work, and returns a short, focused summary. The manager gets the result without living through every step. In this analogy, the sub-agent is the specialist and the main loop is the manager.

Here are two common jobs for a sub-agent.

Job one: searching a large codebase. If the loop needs to find every place a function is used across thousands of files, reading them all itself would flood its workspace with text and slow it down. Instead, it sends a search sub-agent to scan the files and report back a concise summary: for example, “the function is used in three places — here they are.” The loop receives the answer, not a dump of all files.

<Frame>
  <img alt="The image illustrates a task titled &#x22;Job One - Search a Big Codebase,&#x22; showing icons labeled &#x22;The Loop,&#x22; &#x22;Search Subagent,&#x22; and &#x22;2,000 files,&#x22; with a note that &#x22;The Loop&#x22; is used in three places." />
</Frame>

Job two: checking work before saving. This pattern is often called the maker-and-checker.

<Frame>
  <img alt="The image illustrates a workflow titled &#x22;Job Two – Check Before Saving,&#x22; showcasing three steps with icons: &#x22;The Change,&#x22; &#x22;Check It,&#x22; and &#x22;Then Save,&#x22; indicating a process of reviewing changes before saving them." />
</Frame>

One agent (the maker) produces the change. A different agent (the checker) reviews it. Why use a different agent? The maker tends to trust its own output and can miss mistakes. A fresh checker, given its own instructions — and sometimes implemented as a stronger model — inspects the change with new eyes and flags problems the original agent might miss. Splitting the roles this way catches errors that a single agent would overlook.

<Callout icon="lightbulb">
  Use a separate checker when correctness matters. A fresh checker reduces confirmation bias and can be given stricter validation rules or a more powerful model.
</Callout>

A major advantage of sub-agents is containment of clutter. Big jobs generate lots of intermediate data: long search results, massive files, and extra context. If all that landed in the main loop, its working memory would fill up and reasoning would degrade. The sub-agent handles the messy work in its own space and returns a short, focused answer. The main loop only receives the distilled result.

<Frame>
  <img alt="The image illustrates a concept labeled &#x22;The Subagent Takes the Clutter,&#x22; with sections for &#x22;The Subagent&#x22; having &#x22;its own space&#x22; and &#x22;The Main Loop&#x22; shown with a &#x22;Short answer&#x22; indication." />
</Frame>

Sub-agents can also be intentionally minimal: they are given only the tools they need for the task. For example, a search helper might be granted read-only access to files but not permission to modify them. Keeping each helper small reduces cost, increases speed, and improves safety.

<Frame>
  <img alt="The image shows a &#x22;Search Subagent&#x22; icon with the text &#x22;Only the Tools It Needs&#x22; above it. Below the icon, it indicates the ability to &#x22;Read files&#x22; and &#x22;Change files.&#x22;" />
</Frame>

Helpers can run in parallel. If multiple independent jobs can proceed at once, the main loop can spawn several sub-agents simultaneously. Each sub-agent works in its own workspace and reports back its own clean answer. Running side by side saves time while preserving the benefits of isolation.

<Frame>
  <img alt="The image depicts a diagram showing &#x22;The Loop&#x22; leading to three branches, each with a robot icon, under the theme &#x22;Run Side by Side.&#x22; It includes a note indicating that this process &#x22;saves time.&#x22;" />
</Frame>

In short, sub-agents provide focus, speed, and safety. Each one starts fresh, performs a single job, and hands back a clean answer. They remove heavy, messy work from the main loop, keep its working memory tidy, allow concurrent progress, and give the system ways to check itself with fresh eyes.

<Frame>
  <img alt="The image illustrates three key concepts: Focus, Speed, and Safety, each represented with an icon and associated actions like &#x22;Fresh start,&#x22; &#x22;Off the plate,&#x22; and &#x22;Clean memory.&#x22;" />
</Frame>

Recap: a sub-agent is a helper started by the main loop to handle one clear job. It begins with its own workspace and instructions, performs the work, and reports back a short answer so the main loop stays focused. Good uses include searching large codebases and implementing a maker-and-checker workflow. Helpers can also be run side by side to save time.

<Frame>
  <img alt="The image lists &#x22;Good Uses&#x22; for three activities: searching a codebase, using a maker and checker approach, and side-by-side comparison, each with corresponding icons and benefits like &#x22;fresh eyes&#x22; and &#x22;saves time.&#x22;" />
</Frame>

Best practices

* Give each sub-agent a single, unambiguous task and a bounded scope.
* Limit access: grant the minimal permissions (e.g., `read-only`) needed for the task.
* Return only the distilled result (summary, list of hits, or a yes/no verdict) rather than raw intermediate data.
* Use separate checkers for high-stakes outputs to reduce confirmation bias.
* Run independent sub-agents in parallel when possible to reduce wall-clock time.

Quick reference table

| When to use               | Example task                                | Benefit                                               |
| ------------------------- | ------------------------------------------- | ----------------------------------------------------- |
| Offload heavy scanning    | `search_codebase` across thousands of files | Keeps main loop memory small; returns concise results |
| Validation / QA           | Maker produces patch, checker reviews it    | Catches errors and reduces bias                       |
| Parallel independent work | Multiple extractors run concurrently        | Faster overall completion with isolated workspaces    |

Links and references

* [Maker–checker pattern (general concept)](https://en.wikipedia.org/wiki/Segregation_of_duties)
* [Designing isolated worker processes (concepts and patterns)](https://martinfowler.com/articles/patterns-of-distributed-systems.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/loop-engineering/module/6371e2a8-2e13-4841-ba89-95dd842b1bdd/lesson/39d03cf4-6d5c-4513-b7c5-086ed207d82c" />
</CardGroup>
