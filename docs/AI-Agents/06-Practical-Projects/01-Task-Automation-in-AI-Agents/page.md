# Extract keywords from the job description
extracted_keywords = extract_keywords_from_job_description(JOB_DESCRIPTION)
print("\nExtracted Keywords:\n", extracted_keywords)
```

Create the agent and run it. The agent uses the `scan_resumes_for_keywords` tool defined earlier.

```python theme={null}
agent = Agent(
    name="Resume Matcher",
    instructions=(
        "You are a resume scanner. The user will give you a job description. "
        "First extract the keywords, then use the tool `scan_resumes_for_keywords` "
        "to scan the resumes and report which resumes mention which keywords "
        "(include filename, matched keyword, matching line, and page number)."
    ),
    tools=[scan_resumes_for_keywords],
    model="gpt-4",
    model_settings=ModelSettings(truncation="auto"),
)

prompt = (
    f"Scan the resumes for keywords that match this posting:\n\n{JOB_DESCRIPTION}\n\n"
    f"The extracted keywords are: {', '.join(extracted_keywords)}"
)

# Run the agent using Runner. Runner.run is async, so use asyncio.run to execute it.
if __name__ == "__main__":
    result = asyncio.run(Runner.run(agent, prompt))
    print("\nResume Scan Results:\n")
    print(result)
```

Operational notes:

* `Runner.run` is asynchronous; the `asyncio.run(...)` wrapper is appropriate for simple scripts.
* For long-running or production use, integrate into an async event loop or background worker.

## 5) Example output

A sample (cleaned) output might look like:

```plaintext theme={null}
Resume Scan Results:
RunResult:
- Last agent: Agent(name="Resume Matcher", ...)
- Final output (str):
Here are the results of scanning the resumes for the extracted keywords:

### fake_resume_john_doe.pdf
- Python: Programming Languages: Python, Java, C++ (Page 1)
- Python: Implemented scalable Python microservices for data ingestion pipelines (Page 1)
- Machine Learning: Designed and deployed ML models to improve recommendations (Page 1)
- Git: Tools: Git, Docker, Kubernetes (Page 1)

### resume_1.pdf
- Python: Python, JavaScript, React, Node.js, Docker (Page 1)

### resume_2.pdf
- Python: Python, R, Machine Learning, TensorFlow, SQL (Page 1)
- SQL: Experience with SQL for analytics and pipelines (Page 2)

### resume_3.pdf
- AWS: AWS, Docker, Kubernetes, CI/CD (Page 1)

The identified resumes contain keywords related to Python, Machine Learning, Git, SQL, and cloud tooling.
```

## Next steps / improvements

* Rank resumes by the number of matched keywords or weighted importance.
* Export results to CSV, JSON, or store in a database for later analysis.
* Add a web UI or email summary for recruiters.
* Improve keyword extraction with domain-specific prompts, stop-words, or normalization (e.g., treat "ML" and "Machine Learning" as synonyms).
* Add fuzzy matching or synonym expansion using libraries like `fuzzywuzzy`/`rapidfuzz` or embedding similarity.

## Links and references

* OpenAI Chat Completions guide: [https://platform.openai.com/docs/guides/chat](https://platform.openai.com/docs/guides/chat)
* OpenAI API keys: [https://platform.openai.com/docs/api-keys](https://platform.openai.com/docs/api-keys)
* PyMuPDF documentation: [https://pymupdf.readthedocs.io/](https://pymupdf.readthedocs.io/)
* python-dotenv: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
* OpenAI Python client: [https://github.com/openai/openai-python](https://github.com/openai/openai-python)

You now have a working agent-based resume screener that extracts relevant keywords from a job posting and scans PDF resumes for those keywords. Adjust the prompt, keyword limits, and matching logic to fit your organization's hiring criteria.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/995723a2-bfce-4350-b854-d47bf9b03c8b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/295d0d0b-0445-44cc-9fee-549b0c0b3012)


# Task Automation in AI Agents

Source: https://notes.kodekloud.com/docs/AI-Agents/Practical-Projects/Task-Automation-in-AI-Agents/page

Overview of task automation for AI agents covering planning, tool integration, memory, workflows, triggers, and best practices for building reliable autonomous task-executing systems

Welcome back. In this lesson we explore task automation for AI agents: how agents move from conversation to autonomous action. You’ll learn why automation matters, how agents plan and execute tasks, what tools and architectures enable reliable workflows, and practical patterns for production systems.

What we cover

* Task automation fundamentals for AI agents
* Benefits and challenges
* Types of tasks and integrations
* The agent–task loop (Observe → Design/Plan → Act)
* Task decomposition and planning
* Tools, APIs, and environment integration
* Memory and context management
* Automation patterns, triggers, and schedulers
* Real-world use cases
* Best practices for safe, observable automation

Task automation turns agents into autonomous workers that take input, reason, plan, and act — for example: processing files, scheduling actions, calling APIs, or generating reports. Core enabling capabilities include planning, tool use, memory, and reliability mechanisms. When done well, automated agents function as digital collaborators that reliably execute repeatable tasks at scale.

How a modern AI agent functions
This diagram shows a modern AI agent acting as a central intelligence hub. The flow starts with a user prompt; the agent interprets intent, generates a task list, and executes actions. It interacts with data sources, a code executor, specialized models, and LLMs, then returns outputs to the user.

<Frame>
  <img alt="The image is a diagram titled &#x22;Modern AI Agent as a Central Intelligence Hub,&#x22; showing an AI agent that processes prompts and interacts with various components such as data, code executors, ML models, and LLMs to produce outputs." />
</Frame>

Key integratable components

* Data: Query SQL, search indexes, or structured/unstructured sources.
* Code executor: Run generated code in sandboxed environments and return execution results.
* Specialized ML models: Forecasting, optimization, or domain-specific inference.
* LLMs: Planning, summarization, and complex natural language understanding (e.g., GPT-style or LLaMA-family models).

Benefits and trade-offs
Task automation delivers clear advantages:

* Reduced human workload for repetitive tasks
* Consistent, accurate execution of instructions
* Continuous operation and scaling across time zones

But automation also introduces challenges:

* Handling edge cases and ambiguous inputs
* Maintaining traceability, auditability, and reliability
* Managing compute costs and resource usage as systems scale

<Frame>
  <img alt="The image is a comparison chart outlining the benefits and challenges, with benefits including reducing human workload and improving consistency, while challenges involve handling edge cases and managing costs." />
</Frame>

Types of tasks apt for automation
Below are common categories that map to typical agent capabilities.

| Task Category           | Typical Actions                                  | Example integrations                |
| ----------------------- | ------------------------------------------------ | ----------------------------------- |
| Data operations         | Parsing, transform, cleaning, summarization      | `SQL`, Elasticsearch, cloud storage |
| Workflow tasks          | Email, file moves, DB updates, spreadsheet edits | Email APIs, Google Drive, Notion    |
| Scheduling & monitoring | Reminders, threshold alerts, periodic checks     | Cron, cloud schedulers, task queues |
| Advanced autonomy       | Research, code generation, testing               | LLMs + sandboxed executors          |
| API & RPA               | Enterprise workflows and low-code automations    | Slack, Jira, RPA platforms          |

You can automate across tools like [Notion](https://www.notion.so/), [Slack](https://slack.com/), [Google Drive](https://drive.google.com/), and [Jira](https://www.atlassian.com/software/jira).

<Frame>
  <img alt="The image outlines five core aspects of task automation: data transformation, workflow execution, scheduling, autonomous research, and API integrations with robotic process automation (RPA)." />
</Frame>

The agent–task loop
Every automation agent typically follows a closed loop:

1. Observe — receive input or perceive environment events (webhooks, file changes, user prompts).
2. Design / Plan — determine a sequence of steps or a task tree (static or LLM-driven).
3. Act — invoke tools, call APIs, run code, or produce artifacts.
4. (Optional) Reflect / Store — update memory, emit logs, and persist results for future decisions.

This loop supports iterative improvement, recovery from failures, and stateful behavior across steps.

<Frame>
  <img alt="The image is a flowchart titled &#x22;The Agent Task Loop,&#x22; outlining a process that includes steps like input trigger, perception layer, planner/policy module, tool or API execution, output handling, reflection, and optional memory update." />
</Frame>

Task decomposition and planning
Large tasks are decomposed into smaller, testable subtasks. Example: “send a daily summary” decomposes to:

* Fetch the latest data
* Summarize key insights
* Format the message
* Send email or post to a channel

Decomposition enables stepwise execution, clearer tool responsibilities, retry strategies, and easier observability. Planning strategies:

* Static plans — predefined step lists for deterministic flows
* Dynamic plans — LLM or planner-generated task trees that adapt to context

<Frame>
  <img alt="The image illustrates a process for task decomposition and planning, displaying steps like fetching data, summarizing insights, formatting output, and emailing results. It includes icons and text labels for each step, with a footer mentioning decision trees, LLM planning, and graphs." />
</Frame>

Tools, APIs, and environment integration
Agents act through integrable tools and execution environments:

* REST APIs, RPCs, and SDKs
* Python functions and serverless sandboxes
* Shell commands and containerized runtimes
* Cloud services (storage, pub/sub, schedulers)

Frameworks such as [LangChain](https://learn.kodekloud.com/user/courses/langchain) and other agent frameworks abstract tools into callable primitives. Examples:

* Use the `Google Drive API` to fetch a spreadsheet
* Run a summarization model to condense content
* Call an email API to send results

This modular, tool-centric pattern ensures extensibility and safer execution boundaries.

Memory and context for reliable automation
Memory enables continuity and personalization:

* Short-term memory: session state, which step the agent is on
* Long-term memory: persisted preferences, processed documents, or user history

Memory reduces redundant work and supports adaptive behavior. Without memory, flows are stateless and repeat work on each trigger.

Architectural patterns
Choose a pattern depending on complexity, scale, and fault tolerance:

| Pattern                | When to use                                         | Characteristics                                   |
| ---------------------- | --------------------------------------------------- | ------------------------------------------------- |
| Single-agent loop      | Simple tasks (file renames, basic notifications)    | Easier to implement; single point of control      |
| Multi-agent pipeline   | Complex workflows (research → summarize → validate) | Specialized workers, better fault isolation       |
| Event-triggered agents | Real-time reactions (webhooks, file uploads)        | Low latency, reactive                             |
| Scheduled agents       | Periodic reports or maintenance                     | Cron-like cadence using schedulers or task queues |

Triggers and schedulers
Triggers (event-driven) and schedulers (time-driven) start automated flows:

* Triggers: incoming HTTP requests, webhook events, file-system watchers, messages
* Schedulers: cron jobs, cloud schedulers, or libraries like `Celery` for periodic tasks

Use event triggers for real-time workflows and schedulers for routine, time-based tasks.

Common production use cases

* Downloads Folder Organizer: monitor a folder to categorize, rename, and move files.
* Email Responder: classify incoming mail, draft replies, and escalate to humans when needed.
* GitHub PR Triage: review new PRs, assign reviewers, and add labels.
* Slack Daily Summarizer: aggregate unread messages into an end-of-day brief.

These patterns reduce cognitive load and speed up team workflows.

Best practices for safe, observable automation

* Validate inputs before acting; ambiguous or malformed inputs should trigger clarification.
* Apply structured error handling, backoff, and retry logic to tolerate transient failures.
* Modularize components (parsing, summarizing, emailing) to limit blast radius on failures.
* Log actions, errors, and metrics for observability and troubleshooting.
* Use role separation: give each agent a clear, singular responsibility and defined interfaces.
* Enforce access controls and least privilege when calling external services.

> **lightbulb** Validate inputs, isolate tools, and log actions. These steps greatly reduce the risk of unexpected behavior and make debugging simpler.

<Frame>
  <img alt="The image presents best practices for task automation, including validating inputs, structured error handling, tool isolation, performance tracking, and using role-based agents. Each practice is visually represented with icons." />
</Frame>

Conclusion
By combining clear task decomposition, robust tool integration, contextual memory, and strong observability, you can design AI agents that safely automate meaningful work. For production-grade automation, prioritize input validation, modularity, and monitoring before optimizing for cost and scale.

Links and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [LangChain](https://learn.kodekloud.com/user/courses/langchain)
* [Google Drive API](https://developers.google.com/drive/api)
* [Celery documentation](https://docs.celeryq.dev/en/stable/)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/c9e06a14-db75-49ac-8819-8d319894b8b8)
