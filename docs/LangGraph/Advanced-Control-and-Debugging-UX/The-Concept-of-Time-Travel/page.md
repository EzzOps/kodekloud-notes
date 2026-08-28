# The Concept of Time Travel

Source: https://notes.kodekloud.com/docs/LangGraph/Advanced-Control-and-Debugging-UX/The-Concept-of-Time-Travel/page

Explains LangGraph's time travel feature using checkpointing to snapshot, restore, and resume graph executions for debugging, rapid iteration, demonstrations, and selective replays.

Why time travel in LangGraph?

Time travel in LangGraph is not science fiction — it’s a practical debugging and iteration capability that lets you rewind a graph to a previous execution state and resume from that point. This makes it easy to re-run failed segments, inspect intermediate data, and test alternative paths without restarting the entire workflow. Time travel is especially valuable for long-running or multi-step graphs where re-executing everything is slow or costly.

<Frame>
  <img alt="The image depicts a flowchart demonstrating &#x22;Time Travel in LangGraph,&#x22; which allows rewinding and resuming at specific checkpoints in an execution history for multi-step workflows." />
</Frame>

How time travel works

At its core, time travel relies on persistence (checkpointing). When enabled, LangGraph stores snapshots of the graph’s state at execution points you mark or at configured intervals. Each snapshot can be restored or forked into a new run. Restoring a snapshot reloads the graph state (variables, node outputs, metadata) and allows you to continue execution from that point as if you had never left.

Example — resuming from a stored checkpoint

```python theme={null}
config = {"configurable": {"thread_id": "abc123"}}
