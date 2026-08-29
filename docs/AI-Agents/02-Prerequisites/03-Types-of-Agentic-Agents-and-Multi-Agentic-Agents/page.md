# Types of Agentic Agents and Multi Agentic Agents

Source: https://notes.kodekloud.com/docs/AI-Agents/Prerequisites/Types-of-Agentic-Agents-and-Multi-Agentic-Agents/page

Overview of autonomous, goal-driven AI agents, their architectures, behaviors, distinctions from standard AI, components, workflows, and real-world use cases for multi-agent systems

In this lesson we examine agentic agents — autonomous, goal-driven AI systems — and how they differ from traditional AI. You'll learn:

* What agentic agents are
* How they compare to standard AI systems
* Core architecture and modular components
* Types of agentic behavior (goal-oriented, tool-using, self-improving)
* Practical, real-world use cases and a working agent loop example

<Frame>
  <img alt="The image is an agenda slide listing five points related to agentic agents, including their understanding, comparison with other AI agents, features, behaviors, and real-world use cases." />
</Frame>

Why agentic agents matter

Agentic agents represent a shift from reactive models to proactive, autonomous systems. Instead of answering one-off prompts, these agents accept goals, plan multi-step actions, use external tools, maintain memory, and adapt over time. That makes them suited for AI copilots, orchestration across services, and multi-agent ecosystems where long-running objectives and coordination are required.

<Frame>
  <img alt="The image discusses why agentic agents are the future, showing a person interacting with a digital interface and tools for building systems. It includes the phrase &#x22;Equips to build systems&#x22; and an &#x22;Initiate&#x22; button with a paper airplane icon." />
</Frame>

As organizations build AI copilots and multi-agent workflows, mastering agentic design is essential for innovation, reliability, and scalability.

<Frame>
  <img alt="The image highlights the future importance of agentic agents, focusing on AI copilots and multi-agent ecosystems, suggesting that understanding agentic design is key to innovation." />
</Frame>

What are agentic agents?

Agentic agents are AI systems that operate with autonomy, intentionality, and goal orientation. They:

* Initiate actions without explicit prompt for each step
* Formulate and adapt plans
* Sense and reason about their environment
* Execute tasks using available tools and services
* Learn and refine strategies over time

Their behavior emerges from integrating memory, reasoning, tool invocation, and execution in a continuous control loop.

<Frame>
  <img alt="The image describes the capabilities of agentic AI agents, highlighting their ability to initiate action, formulate plans, and execute tasks." />
</Frame>

Core architecture of agentic systems

Agentic workflows are typically pipeline-driven and modular to support scaling, observability, and safe tool access:

* Data pipelines ingest and clean structured and unstructured sources.
* A Feature Store provides reusable, versioned features.
* Model experimentation and a model store support reproducibility.
* The Agentic AI Core handles language understanding, planning, and decision-making.
* Microservices and serverless functions enable event-driven, modular execution.
* Hybrid cloud infrastructure supports scale, locality, and compliance.
* Logging, auditing, monitoring, and front-end applications provide observability and human-in-the-loop controls.

Key architecture components and their roles:

| Component                | Purpose                                | Example                      |
| ------------------------ | -------------------------------------- | ---------------------------- |
| Data pipelines           | Ingest and clean inputs (batch/stream) | ETL jobs, Kafka streams      |
| Feature store            | Shareable features for models          | Time-series feature store    |
| Model store & deployment | Versioned models and serving           | Model registry, model server |
| Agentic AI Core          | Planning, reasoning, decision logic    | LLM + orchestration engine   |
| Tooling & microservices  | External API access and execution      | Search, DB, code runner      |
| Observability            | Audit trails, monitoring, alerts       | Logging, APM, dashboards     |

<Frame>
  <img alt="The image is a diagram depicting a comprehensive AI system architecture, including components like front-end applications, serverless functions, modularity, microservices, feature store, data pipelines, and hybrid cloud infrastructure. It illustrates the flow and interaction between these elements for AI model deployment and management." />
</Frame>

Agentic vs. standard AI systems

Agentic agents differ from traditional reactive systems along three core dimensions:

| Trait       | Agentic agents                                        | Standard AI systems                        |
| ----------- | ----------------------------------------------------- | ------------------------------------------ |
| Autonomy    | Self-directed; continue work without repeated prompts | Reactive; perform a single task per prompt |
| Tool usage  | Dynamically invoke APIs, search, code execution       | Limited or no tool invocation              |
| Persistence | Memory across sessions; long-term goals               | Stateless or short-lived context           |

Because of these traits, agentic agents act more like collaborators: they can decompose open-ended tasks, iterate on feedback, and coordinate with other systems or agents.

<Frame>
  <img alt="The image compares agentic AI agents to other AI agents, highlighting their traits: self-directed, tool-usage, and persistent." />
</Frame>

Real-world distinction

* Standard chatbot: answers a given question and stops.
* Agentic system: given "produce a market research report," it decomposes the task, collects data, synthesizes findings, and outputs a formatted report—adapting along the way as new information appears.

Core components of an agentic agent

Agentic solutions are modular. Typical components include:

| Component             | Responsibility                        | Typical implementation                       |
| --------------------- | ------------------------------------- | -------------------------------------------- |
| Goal Management       | Accepts, generates, prioritizes goals | Goal queue, scheduler                        |
| Planning Engine       | Evaluates paths and decomposes tasks  | LLM planning + rule engine                   |
| Action Execution      | Runs tools and external calls         | API clients, serverless functions            |
| Memory Systems        | Store context and outcomes            | Short-term cache, long-term DB               |
| Tool Invocation       | Dynamically select and call tools     | Search, DB, code runner, connectors          |
| Learning & Adaptation | Improve from feedback & data          | Reinforcement learning, retraining pipelines |

<Frame>
  <img alt="The image outlines the key features and architecture of agentic agents, highlighting components like goal management, planning engine, memory systems, and action execution module." />
</Frame>

These components together enable persistence, flexibility, and robust decision-making in dynamic environments.

Types of agentic behavior

Agentic behavior typically spans three overlapping dimensions:

* Goal-oriented: set objectives, plan steps, re-evaluate strategies.
* Tool-using: select and operate tools such as web search, databases, or code execution.
* Self-improving: learn from outcomes, monitor metrics, and refine strategies over time.

High-performing agents combine these behaviors to handle complex, multi-step objectives efficiently.

<Frame>
  <img alt="The image illustrates three types of agentic behavior in AI: goal-oriented, tool-using, and self-improving, each defined by specific capabilities and functions." />
</Frame>

Capability breakdown

An agent integrates multiple capabilities to perceive, reason, and act:

* Autonomy: self-organization and independent operation.
* Memory: short-term and long-term contextual storage.
* Action: execute tasks, call functions, and reflect on outcomes.
* Goal focus: maintain objectives and respect constraints.
* Planning: chain-of-thought reasoning, task decomposition, sequencing.
* Skills: access tools such as web search, code execution, summarizers, and data retrieval.

<Frame>
  <img alt="The image is a diagram of an &#x22;Agent&#x22; with connected elements like Autonomy, Skills, Memory, Planning, Action, and Goal, and includes related concepts like Self-Organizing and Goal Oriented. Various behaviors related to each element are also listed, such as Environment Sensing and Task Execution." />
</Frame>

Use cases

Agentic agents add value where ongoing autonomy, orchestration, or long-horizon planning matters:

* Business automation: schedule coordination, meeting summaries, automatic follow-ups.
* AI research assistants: plan experiments, search literature, debug code, produce reports.
* Customer service orchestration: detect trends, escalate issues, draft stakeholder communications.
* Productivity bots: personal assistants that plan calendars, book appointments, summarize emails.
* Autonomous operations: monitor infrastructure, restart services, report anomalies.

Industries benefiting from agentic AI include customer service, healthcare, retail, manufacturing, marketing, HR, finance, insurance, and logistics.

<Frame>
  <img alt="The image is a diagram illustrating real-world use cases of agentic agents, including AI research assistants, customer service orchestration, productivity bots, business automation, and autonomous operations. Each segment briefly describes how these agents enhance tasks like research, customer service, personal productivity, and infrastructure management." />
</Frame>

Agentic workflow example (agent loop)

A typical agent loop:

1. Goal Initialization — Agent receives or generates a goal (e.g., "Summarize the top five AI news articles").
2. Environment Sensing — Collect data from APIs, web, or files.
3. Planning & Reasoning — Decompose the goal into subtasks (LLM + logic engine).
4. Tool Selection & Action Execution — Run searches, call APIs, execute code, summarize results.
5. Memory Update — Log context, actions, and outcomes.
6. Evaluation & Feedback — Measure success, adjust approach, iterate.

This loop repeats until the goal is satisfied or re-prioritized. Example flowchart:

```mermaid theme={null}
flowchart TD
    A[Goal Initialization<br/>(User-defined or self-generated)] --> B[Environment Sensing<br/>(Text, APIs, Files, Web)]
    B --> C[Planning & Reasoning<br/>(LLM + logic engine)]
    C --> D[Tool Selection & Action Execution<br/>(APIs, code, search, write)]
    D --> E[Memory Update<br/>(Log context, results, failures)]
    E --> F[Evaluation & Feedback<br/>(Was the goal met? Adjust?)]
    F --> A
```

In production, agents select tools dynamically (search engines, databases, code runners), persist context to memory stores, and use evaluation metrics to determine next steps.

> **lightbulb** Agentic systems are most effective when goals, constraints, and evaluation metrics are well defined. Observability (logging, monitoring) and safe tool access controls are critical for reliable deployments.

Links and references

* [Multi-agent systems (overview)](https://en.wikipedia.org/wiki/Multi-agent_system)
* [Designing autonomous agents](https://www.acm.org/) (research & best practices)
* [LLM-based agents and tool use](https://platform.openai.com/docs/guides/agents)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/3027a2f9-9ff6-40c0-8e44-121170fecef0/lesson/4c95c93c-468d-4836-8561-a1accae980b5)
