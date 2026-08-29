# python
# Example usage pattern for an agent with FileSearchTool
from openai import OpenAI
from openai.agents import Agent, FileSearchTool

client = OpenAI()
agent = Agent(tools=[FileSearchTool()])

# Upload files into the agent's workspace (session-scoped)
agent.tools["file_search"].upload_file("contracts/nda.pdf")
agent.tools["file_search"].upload_file("reports/strategy_2026.pdf")

# Query using natural language; the tool performs retrieval internally
response = agent.run("What are the key deliverables mentioned in the NDA?")
print(response)
```

Common configuration knobs you’ll use include chunk size, overlap, `max_num_results` (limit retrieved chunks), and metadata filters to scope searches.

<Frame>
  <img alt="The image is a flowchart illustrating the use of FileSearchTool in OpenAI Agents SDK, detailing steps for adding the tool, uploading documents, querying via natural language, and retrieving relevant information." />
</Frame>

## Typical use cases

* Contract review agents: identify clauses, deadlines, or penalty terms.
* Compliance bots: cross-reference internal policies with regulations.
* Report assistants: extract key insights from long business or scientific documents.
* Data validation: verify CSV records, flag anomalies, or reconcile entries.
* Q\&A and knowledge assistants: deliver sourced answers from internal files.

## Security, storage, and performance considerations

FileSearchTool processes files inside the agent runtime. By default, the vector index is session-scoped and not persisted across sessions unless you explicitly export or save embeddings to external storage. Because indexing often occurs in-memory, handling many or very large files can increase memory and CPU usage and affect agent responsiveness.

<Callout icon="warning">
  Always treat sensitive files with strict controls: use role-based access, encryption at rest, session timeouts, memory limits, and logging. Monitor how long files persist in the agent workspace and ensure compliance with your organization's data handling policies.
</Callout>

## Comparing FileSearchTool to external vector databases

| Capability             |                                                        FileSearchTool (native) | External Vector DBs                                                                                 |
| ---------------------- | -----------------------------------------------------------------------------: | --------------------------------------------------------------------------------------------------- |
| Setup complexity       |                Very low — built into the Agents SDK with minimal configuration | Medium–high — requires infrastructure, auth, and index management (e.g., Pinecone, FAISS, Weaviate) |
| Persistence            |                                          Session-scoped by default (temporary) | Persistent — suitable for multi-session, multi-user use cases                                       |
| Integration effort     |                                                  Minimal glue code; native API | Client libraries and synchronization logic required                                                 |
| Scale and access       |       Ideal for single-agent or single-session workflows and rapid prototyping | Designed for large-scale, multi-user, production search across millions of documents                |
| Typical recommendation | Fast prototyping, scoped agent workflows, privacy-sensitive temporary sessions | Long-term knowledge bases, multi-user search, high-availability production systems                  |

References:

* Pinecone: [https://www.pinecone.io](https://www.pinecone.io)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Weaviate: [https://weaviate.io](https://weaviate.io)

Recommendation: Use FileSearchTool for rapid prototyping and session-scoped agent tasks. For long-term persistence, high concurrency, or very large corpora, pair an embedding pipeline with a dedicated vector database.

## Best practices

* Preprocess and clean documents before upload — consistent structure and clear section headers improve chunking quality.
* Choose chunk sizes that preserve semantic coherence and respect token limits; small overlaps help avoid content loss at boundaries.
* Limit retrieved chunks (set `max_num_results`) to prevent context bloat and token overrun.
* Attach and index metadata (file titles, authors, timestamps) and use metadata filters to narrow results.
* Tag files for source, team, or domain filtering if you need scoped searches.
* Monitor memory and CPU usage during indexing and retrieval; batch or stream large files when possible.

<Callout icon="lightbulb">
  Tip: Prefer semantic search over raw keyword matches to improve retrieval quality. Combine semantic ranking with metadata filters to return a smaller, highly relevant context set for the LLM.
</Callout>

## Limitations and future directions

Current constraints include session-scoped persistence and memory pressure for very large document collections. Potential future enhancements include:

* Hybrid keyword + semantic search for faster recall and pre-filtering.
* Streaming or incremental indexing for very large files.
* Dynamic re-indexing when files change and real-time triggers.
* Optional connectors to persistent vector backends for long-lived knowledge stores.
* Improved tooling for chunking configuration, overlap control, and metadata management.

## Conclusion

File-based retrieval is a core capability for agent workflows that must reason over large or structured documents. The FileSearchTool provides an easy-to-use, session-scoped semantic search experience optimized for agent contexts — ideal for rapid prototyping and single-session tasks. For production-grade, persistent, multi-user systems or massive scale, augment FileSearchTool with a persistent vector database and a strong data governance model.

This lesson covered FileSearchTool’s design, pipeline, best practices, and tradeoffs to help you decide when to use it and how to integrate it effectively.

## Links and references

* OpenAI Agents SDK docs: [https://platform.openai.com/docs/agents](https://platform.openai.com/docs/agents)
* Pinecone: [https://www.pinecone.io](https://www.pinecone.io)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Weaviate: [https://weaviate.io](https://weaviate.io)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/1cf28913-75cd-4e3d-9f14-a2377207d259" />
</CardGroup>


# AI Agents Introduction

Source: https://notes.kodekloud.com/docs/AI-Agents/Prerequisites/AI-Agents-Introduction/page

Overview of AI agents including definition, architecture, capabilities, differences from traditional AI and applications

In this lesson we introduce AI agents: what they are, how they differ from traditional AI, their internal anatomy, core capabilities, real-world applications, the historical evolution of agentic systems, and why they matter today.

Understanding AI agents is fundamental to building intelligent systems that can reason, plan, and act autonomously. These agents power digital assistants, research companions, scheduling tools, and many other applications. Unlike one-off predictive models or rigid rule-based programs, agents are goal-driven systems that use memory, tools, and multi-step reasoning to solve complex, changing problems.

## What is an AI agent?

An AI agent is a system that perceives its environment, reasons about observations, and takes actions to achieve defined goals — often autonomously. Agents can call APIs, browse the web, manipulate files, trigger other systems, and interact with people to complete multi-step tasks.

<Callout icon="lightbulb">
  An AI agent follows a human-like problem-solving cycle: observe, decide, act. It combines goals, prior knowledge, and capabilities to produce autonomous, goal-directed behavior.
</Callout>

Agents operate in a feedback loop: they sense inputs, plan using their internal knowledge and tools, act on the environment, and update their state (short-term or long-term memory) based on outcomes. Over time, this loop enables adaptation and continual improvement.

## How AI agents differ from traditional AI

Traditional AI systems are typically reactive: provide an input and receive an output (for example, a classification or a computed result). AI agents are proactive: they can initiate work, decompose tasks, track progress, recover from failures, and take independent multi-step actions.

* Traditional AI: stateless, prompt-and-response, one-step outputs.
* AI agents: stateful, goal-driven, multi-step workflows, tool-enabled.

<Frame>
  <img alt="The image compares AI Agents and Traditional AI, highlighting AI Agents as proactive, stateful, and goal-oriented, while Traditional AI is reactive and requires explicit instructions." />
</Frame>

## Core components of an AI agent

A typical agent architecture includes modular components that together enable perception, reasoning, planning, action, and learning.

| Component            | Purpose                                             | Examples                                                |
| -------------------- | --------------------------------------------------- | ------------------------------------------------------- |
| Perception System    | Interpret inputs from users, sensors, or files      | Natural language parsing, OCR, audio transcription      |
| Reasoning & Planning | Generate plans, decompose tasks, and make decisions | LLM prompts, logic engines, search-based planners       |
| Memory               | Store short-term context and long-term knowledge    | Conversation context, user preferences, knowledge bases |
| Effectors / Tools    | Execute actions in the environment                  | Calendars, APIs, code interpreters, web browsers        |

<Frame>
  <img alt="The image illustrates the components of an AI agent, including the Perception System, Reasoning and Planning Unit, Memory, and Effectors or Tools for Action, along with brief descriptions of each part." />
</Frame>

These modules form feedback loops that let the agent re-evaluate results, adjust planning, and iterate until the goal is satisfied or a defined failure state is reached.

<Frame>
  <img alt="The image depicts the anatomy of an AI agent, highlighting a looped architecture that enables the agent to reevaluate outcomes, adjust its plan, and continue working until success or failure." />
</Frame>

## How an agent thinks and acts (anatomy in practice)

At the center of the system is the reasoning engine — often a Large Language Model (LLM) — which interprets goals, generates plans, and issues commands to tools. Planning typically involves sub-goal decomposition, self-reflection, and critique loops; execution involves calling tools and updating memory.

<Frame>
  <img alt="The image depicts a flowchart titled &#x22;Anatomy of an AI Agent&#x22; showing components like memory, tools, planning, and actions, with elements like short-term and long-term memory, and various tools such as a calendar, calculator, and search." />
</Frame>

The diagram below expands this into a broader ecosystem: role definitions, interfaces, tool integrations, logging, audits, and human supervision all interact with the LLM to produce auditable, safe outcomes.

<Frame>
  <img alt="The image is a flowchart illustrating the anatomy of an AI agent system, detailing components like role definition, interaction interfaces, LLM reasoning engine, and processes such as logging, audits, and analytics. It shows connections between prompts, tools, supervision, feedback, and collaboration, creating a comprehensive AI ecosystem." />
</Frame>

<Callout icon="warning">
  AI agents interacting with external systems require robust guardrails: access control, logging, audit trails, and human-in-the-loop review to maintain safety, compliance, and traceability.
</Callout>

## Modern AI agent capabilities

Modern agents go beyond language understanding to interact with tools, maintain goals over time, and connect to live data sources. Key capabilities:

| Capability                        | What it enables                           | Examples                                            |
| --------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| Natural language understanding    | Interpret complex instructions and intent | Conversational reasoning, instruction parsing       |
| Tool use & action-taking          | Perform operations in external systems    | API calls, database queries, code execution         |
| Goal tracking & adaptive planning | Break down tasks and replan on failures   | Subtask decomposition, progress monitoring          |
| External connectivity             | Access live data and documents            | Reading PDFs, querying APIs, browsing web resources |
| Collaboration                     | Work with humans or other agents          | Shared task handoff, multi-agent orchestration      |

<Frame>
  <img alt="The image is a diagram titled &#x22;Modern AI Agents – Core Capabilities,&#x22; showing three linked sections that represent solving real-world problems, automating workflows, and collaborating with agents or people." />
</Frame>

These capabilities enable agents to evolve from chatbots into digital workers that solve real problems and automate workflows.

## Real-world use cases

Agents are already deployed across many industries. Representative use cases:

| Industry / Role         | Agent tasks                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| Executive assistant     | Manage calendars, summarize emails, schedule meetings             |
| Finance advisor         | Monitor markets, analyze news, generate investment insights       |
| Education               | Personalized tutoring, adaptive practice exercises                |
| Task automation         | Automate email responses, workflow orchestration, code deployment |
| Multimodal applications | Combine vision, speech, and sensors in smart devices              |
| Research assistant      | Web search, literature summarization, knowledge synthesis         |

<Frame>
  <img alt="The image illustrates real-world use cases for technology, including executive assistants, finance advisors, tutoring bots, task automation, and multi-modal development. It features a person interacting with a tablet alongside various icons representing these functions." />
</Frame>

Agents often integrate with services like Google Calendar, Notion, Slack, and cloud APIs to perform context-aware automation.

## Evolution of AI agents

Agent architectures have progressed from simple, rule-based systems to sophisticated, learning-enabled agents:

* If-then rule systems: predictable but brittle in dynamic environments.
* Model-based agents: internal world models for better context handling.
* Goal-based & utility-based agents: planning and outcome evaluation.
* Learning agents: adapt via experience and data-driven policies.
* Modern agents: multi-step reasoning, tool use, and autonomous initiation.

<Frame>
  <img alt="The image illustrates the evolution of agents from model-based, using fixed &#x22;if-then&#x22; rules, to traditional agents with context-aware actions." />
</Frame>

This evolution enables agents that can reason across steps, call tools as needed, and improve performance through feedback.

## Why AI agents matter

AI agents unite decision-making, learning, and autonomous action. They reduce human cognitive load, automate complex workflows, and scale intelligent assistance across domains such as business, healthcare, and research. When combined with robust controls and human oversight, agents become indispensable collaborators rather than simple task executors.

<Frame>
  <img alt="The image explains the importance of AI agents in business, highlighting their ability to reduce cognitive load, automate routine workflows, and enable scalable and intelligent assistance." />
</Frame>

As agents continue to integrate with tools, live data, and human workflows, they will play a central role in building autonomous, auditable, and efficient systems that augment human capabilities.

## Links and references

* [Large language model (LLM) — Wikipedia](https://en.wikipedia.org/wiki/Large_language_model)
* [Autonomous agent — Wikipedia](https://en.wikipedia.org/wiki/Autonomous_agent)
* For best practices on safe agent deployment, consult provider documentation and industry guidelines on auditability, access control, and human oversight.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/3027a2f9-9ff6-40c0-8e44-121170fecef0/lesson/e9268daa-e945-46da-8a68-18d5a7e1fdaf" />
</CardGroup>
