# Multi Agent Frameworks and Architecture

Source: https://notes.kodekloud.com/docs/AI-Agents/Agent-Architecture-Multi-Agent-Systems/Multi-Agent-Frameworks-and-Architecture/page

Guide to multi-agent systems covering architectures, interaction patterns, frameworks, coordination strategies, benefits, challenges, use cases, and best practices for building scalable, modular, and observable agent ecosystems.

Welcome back.

In this lesson, we’ll explore multi-agent frameworks and architecture. You’ll learn what multi-agent systems (MAS) are, why they matter, typical interaction and communication patterns, leading tools, strategies for role assignment and team coordination, ideal use cases, and best practices for building scalable MAS.

Multi-agent frameworks are essential for handling complex, multi-step tasks by distributing responsibilities across a network of collaborating agents. This mirrors human teams—planners, specialists, and reviewers working together toward a shared objective. Understanding MAS architecture helps you design systems that are modular, scalable, and capable of dynamic role allocation.

<Frame>
  <img alt="The image displays an agenda with five topics related to multi-agent systems, including their benefits, collaboration patterns, and frameworks." />
</Frame>

Multi-agent frameworks enable agent ecosystems that coordinate, adapt, and solve real-world problems through intelligent collaboration.

<Frame>
  <img alt="The image lists reasons why multi-agent frameworks are essential, highlighting task delegation, team structure mirroring, scalability, and agent specialization." />
</Frame>

## What is a multi-agent system (MAS)?

A multi-agent system (MAS) is a distributed network of autonomous agents that interact to accomplish tasks that are difficult or inefficient for a single agent. Each agent may have distinct goals, memory, tools, or reasoning models; agents communicate and coordinate to complete a mission.

Key characteristics:

* Autonomous actors with private state and capabilities.
* Distributed decision-making and parallel execution.
* Communication via messages, events, or shared stores.
* Role specialization (planners, executors, verifiers, tool handlers).

<Frame>
  <img alt="The image explains the concept of a Multi-Agent System (MAS) with three agents, each having distinct goals, memory, and tools, highlighting the importance of multi-agent frameworks." />
</Frame>

MAS models team dynamics—division of labor, parallel execution, and problem-solving from multiple perspectives. Common application areas include workflow automation, document analysis, research synthesis, and game AI ecosystems.

<Frame>
  <img alt="The image explains why multi-agent frameworks are essential, highlighting their role in division of labor, parallel task execution, and problem-solving. It also mentions applications like workflow automation, document analysis, and research synthesis." />
</Frame>

## Single-agent vs multi-agent

* Single-agent systems: one decision maker; actions executed sequentially; simpler to design and debug; best for constrained or linear tasks.
* Multi-agent systems: multiple interacting agents; distributed decision-making; parallel task execution; more flexible and scalable for dynamic, large-scale, or heterogeneous environments.

<Frame>
  <img alt="The image is a comparison chart between single-agent and multi-agent systems, highlighting their characteristics such as decision-making, problem-solving, execution, and collaboration." />
</Frame>

## Supervisory (Coordinator) Agent Architecture

A common MAS pattern uses a supervisory (or coordinator) agent. Typical workflow:

1. A user request arrives at the supervisor.
2. The supervisor decomposes the task and delegates subtasks to specialized agents.
3. Sub-agents run independently or collaboratively, query tools, or access data sources.
4. Agents return results to the supervisor.
5. The supervisor aggregates, reconciles, and composes a final response.

This hierarchical coordination resembles a project manager model where the supervisor monitors progress, resolves conflicts, and ensures a coherent final output.

<Frame>
  <img alt="The image is a flowchart of a multi-agent system, showing how a supervisor agent coordinates between three other agents and tools to process a user question and generate a final response." />
</Frame>

Example pseudocode (supervisor-delegate loop):

```python theme={null}
