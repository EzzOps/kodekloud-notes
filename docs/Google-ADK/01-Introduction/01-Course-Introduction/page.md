# Create venv
python3 -m venv .venv

# Activate venv (macOS / Linux)
source .venv/bin/activate

# Your prompt should indicate the venv is active, e.g.:
# (.venv) jeremy@MACSTUDIO hello-world %
```

Install the Google ADK package inside the virtual environment:

```bash theme={null}
(.venv) jeremy@MACSTUDIO hello-world % pip install google-adk
```

The package installs several dependencies; expect to download multiple MBs.

Scaffold a new ADK application from your project root:

```bash theme={null}
(.venv) jeremy@MACSTUDIO hello-world % adk create my_agent
```

Follow the interactive prompts. For this lesson choose the Gemini model and Google AI backend:

```text theme={null}
Choose a model for the root agent:
1. gemini-2.5-flash
2. Other models (fill later)
Choose model (1, 2): 1
1. Google AI
2. Vertex AI
Choose a backend (1, 2): 1

Don't have API Key? Create one in AI Studio: https://aistudio.google.com/apikey

Enter Google API key:
```

After entering your API key the scaffold creates a basic layout (files like `__init__.py` and `agent.py`). The generated `agent.py` is the canonical place to register your agent and tools.

Example agent.py
Below is a minimal `agent.py` that defines two deterministic tools and registers them with the root agent. These are intentionally hard-coded for clarity; replace them with real API calls in production.

```python theme={null}
# agent.py
from google.adk.agents.llm_agent import Agent

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    # Hard-coded for demonstration
    return {"status": "success", "city": city, "time": "10:30 AM"}

def get_current_weather(city: str) -> dict:
    """Returns the current weather in a specified city."""
    # Hard-coded for demonstration
    return {"status": "success", "city": city, "weather": "Sunny, 75°F"}

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Tells the current time or weather in a specific city.",
    instruction=(
        "You are a helpful assistant that can provide the current time and the current weather in cities. "
        "Use the 'get_current_time' tool to get the time and the 'get_current_weather' tool to get the weather."
    ),
    tools=[get_current_time, get_current_weather],
)
```

Why register tools this way?

* instruction: The text given to the LLM that defines the agent's behavior and available tools.
* tools: A list of Python callables the model may invoke. The LLM chooses which tool to call based on the user query.

Run the agent from the project root:

```bash theme={null}
(.venv) jeremy@MACSTUDIO hello-world % adk run my_agent
```

A typical interactive session:

```text theme={null}
Log setup complete: /tmp/agents_log/agent.log
/Users/jeremy/.../.venv/lib/python3.14/site-packages/google/adk/cli/cli.py:155: UserWarning: [EXPERIMENTAL] InMemoryCredentialService: This feature is experimental and may change or be removed in future versions without notice.
  credential_service = InMemoryCredentialService()
Running agent root_agent, type exit to exit.
[user]: What do you do?
[root_agent]: I can tell you the current time or weather in a specific city. Just ask me something like "What time is it in New York?" or "What's the weather like in London?"
[user]: What time is it in New York City?
[root_agent]: The current time in New York is 10:30 AM.
[user]: What is the weather in Tokyo?
[root_agent]: The weather in Tokyo is currently Sunny, 75°F.
[user]:
```

Key concepts and best practices

* The LLM acts as a router: the instruction plus the user query determines which tool (if any) gets invoked.
* Tools are plain Python callables and can wrap HTTP APIs, SDKs, or complex business logic.
* For production, use real services (timezone APIs, weather APIs), robust error handling, timeouts, and non-blocking I/O when appropriate.
* Keep tool signatures simple and well-documented (type hints and short docstrings improve the LLM's ability to choose correctly).

Tooling at a glance

| Component         | Purpose                                                    | Example / Notes                                                   |
| ----------------- | ---------------------------------------------------------- | ----------------------------------------------------------------- |
| Agent instruction | Tells the model what tools are available and how to behave | Use clear, concise language describing tools and when to use them |
| tools parameter   | Registers Python callables the agent may invoke            | Functions, API wrappers, async callables (if supported)           |
| Model selection   | Chooses the LLM that will act as the router and responder  | gemini-2.5-flash used in this tutorial                            |
| Backend           | Underlying runtime for the model                           | Google AI (AI Studio) or Vertex AI                                |

> **lightbulb** Tip: Keep your tool interfaces simple and well-documented (type hints and concise docstrings help the LLM choose the right tool). In production, prefer non-blocking calls and proper error handling in tools.

> **warning** Warning: Some ADK features are experimental and may emit warnings at runtime. Pay attention to those messages and review the ADK changelog when upgrading.

Why this structure matters

* The model performs semantic routing: given the instruction and a user prompt, it decides which tool to call and how to format the call.
* This approach separates decision-making (LLM) from execution (tools/APIs), enabling safer, auditable, and extensible agents.
* It mirrors retrieval-augmented patterns: the LLM identifies the appropriate capability or data source and returns the result in natural language.

Summary

* We created a Python virtual environment, installed google-adk, scaffolded a project, added two deterministic tools, and ran an interactive agent that uses the LLM to choose tools based on natural language.
* To build a production-ready agent, replace the stub tools with real API integrations (timezone, weather, or other services), add robust error handling, and monitor agent behavior.

Links and references

* [Google ADK course](https://learn.kodekloud.com/user/courses/google-adk)
* AI Studio: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
* For more on agent design patterns, consult the ADK documentation included with the package or the provider's model docs.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/f42f0830-1e38-449f-8a50-9bf698eb02ab/lesson/7af92786-6ac1-4639-a9f2-c2f9fd71f849)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Google-ADK/Introduction/Course-Introduction/page

Hands-on course teaching Google ADK to build, deploy, and operate LLM-powered cloud automation agents with tools, structured outputs, observability, and production best practices.

Welcome to the Google ADK course. I'm Jeremy Morgan, and I'm excited to guide you through the Agent Development Kit (ADK) — Google Cloud’s toolset for building intelligent cloud automation agents. This course focuses on practical, production-oriented agent design so you can move quickly from prototype to real-world automation.

<Frame>
  <img alt="A futuristic graphic of a robotic hand touching hexagonal tiles labeled &#x22;AUTOMATION&#x22; with blue icons for robotics, cloud, and connectivity. A small circular inset photo of a man appears in the lower-right corner." />
</Frame>

This course is hands-on. Each module includes labs where you’ll implement, test, and iterate on ADK agents using realistic environments and data.

> **lightbulb** This course emphasizes practical labs that let you build, test, and iterate on ADK agents in realistic scenarios.

Course overview

Below is a concise module breakdown so you can scan learning outcomes and the practical skills you'll acquire.

| Module              | Focus                                | What you'll learn / deliverable                                                                             |
| ------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Introduction        | ADK fundamentals & project structure | What ADK is, how it fits into Google Cloud, and a walkthrough of a typical ADK project.                     |
| Building ADK agents | Agent design, tools, workflows       | Scaffold projects, create agents from scratch, define custom tools and workflows, and connect to APIs/data. |
| Deploy & Operate    | Production hardening & observability | Deploy agents to production, secure them, implement structured outputs, and build evaluation pipelines.     |
| Labs & Evaluation   | Iteration and metrics                | Hands-on labs that reinforce design patterns, error handling, and measuring agent quality and safety.       |

Key learning outcomes

* Understand the role of ADK for cloud automation and how it integrates with Google Cloud services.
* Build LLM-backed agents that can reason, call tools, and produce structured outputs.
* Design workflows and tools so agents can operate safely and reliably in production.
* Implement observability and evaluation to continuously measure and improve agent performance.

Example — instantiating a simple ADK agent

Here’s a typical instantiation of an LLM-backed Agent in ADK. This example shows the common fields you’ll specify: a model, descriptive metadata, initial instruction text, and where tools are attached (tools list is empty for now, and you’ll expand it in later modules).

```python theme={null}
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name="helpdesk_root_agent",
    description="Smart IT Helpdesk assistant that helps troubleshoot basic IT issues.",
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n"
        "\n"
        "Goals:\n"
        "1. Quickly understand the user's problem.\n"
        "2. Ask one or two clarifying questions if needed.\n"
        "3. Give clear, step-by-step instructions they can follow.\n"
        "4. Keep answers concise and practical.\n"
        "\n"
        "Constraints for now:\n"
        "- You do NOT have access to tools yet.\n"
        "- Don't claim to check real systems.\n"
        "- Use phrases like 'Based on common IT practice...' instead of pretending.\n"
    ),
    tools=[],
)
```

What this gives you

* A working ADK agent shell that can be executed in simulated or interactive sessions.
* A foundation to attach tools (APIs, database queries, monitoring hooks) and define structured outputs for downstream automation.

Deploying and operating ADK agents

This course covers how to move agents from development into production with safety and observability in mind:

* Secure and harden agents (authentication, least privilege, and data handling).
* Use structured outputs and agent-level schemas to make responses machine-interpretable.
* Implement resilience patterns, retries, and robust error handling.
* Build evaluation and monitoring pipelines to measure agent correctness, latency, and safety.

<Frame>
  <img alt="A presentation slide titled &#x22;ADK's Structured Output Options&#x22; showing two sections: &#x22;Agent-Level Schemas&#x22; (facilitate structured agent interactions) and &#x22;Tool-Level Structured Results&#x22; (ensure organized and interpretable output) with matching icons. There's also a small circular presenter video thumbnail in the bottom-right." />
</Frame>

> **warning** When moving to production, prioritize secure credentials, strict access controls, and thorough testing of tool integrations. Agents with access to live systems should have monitored fallbacks and clear audit trails.

Community and next steps

We believe a strong community accelerates learning. Connect, ask questions, and share your agent projects with peers and mentors.

Recommended resources

* [Google Cloud Documentation](https://cloud.google.com/docs) — guidance for integrating agents with cloud services.
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — if you deploy agents in containers/orchestrated environments.
* [Gemini models on Google Cloud](https://cloud.google.com/vertex-ai/docs/generative-ai) — details on model capabilities and best practices.

Skills you’ll walk away with

* Designing LLM-powered automation agents for cloud operations.
* Implementing tools, workflows, and structured outputs for reliable automation.
* Deploying and operating agents with observability and safety controls.

Are you ready to harness Google ADK and transform your cloud automation skills? Let’s get started.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/f42f0830-1e38-449f-8a50-9bf698eb02ab/lesson/7f295889-465b-489e-86eb-d451f2816dda)
