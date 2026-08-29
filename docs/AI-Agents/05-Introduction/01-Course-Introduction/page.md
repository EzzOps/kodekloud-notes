# Course Introduction

Source: https://notes.kodekloud.com/docs/AI-Agents/Introduction/Course-Introduction/page

A practical course teaching developers how to design, build, and deploy autonomous AI agents using frameworks, tools, and hands-on labs

AI agents are transforming how we build software, automate work, and enhance human productivity. These intelligent systems can reason, act, and collaborate to complete complex tasks — from customer support assistants to autonomous research agents. Leading companies such as Microsoft, OpenAI, Google, and Meta are shipping agent-driven products (Copilot, ChatGPT, Gemini, Meta AI) that showcase how agents improve workflows and create new application categories.

<Frame>
  <img alt="The image displays logos of major tech companies alongside their AI products: Copilot by Microsoft, ChatGPT by OpenAI, Gemini by Google, and Meta AI by Meta." />
</Frame>

Welcome to the AI Agents course from KodeKloud. I’m Gav Ridgeway, and I’ll guide you through designing, building, and deploying autonomous AI agents. This course is practical and hands-on, aimed at developers, data scientists, and anyone curious about agent-based systems.

What you’ll gain:

* A clear definition of AI agents and their main categories.
* Practical knowledge of core technologies (embeddings, vector DBs, evaluation).
* Experience designing agent architectures and multi-agent interactions.
* Hands-on labs using frameworks like LangChain, CrewAI, AutoGen, and MetaGPT.
* Techniques for connecting agents to external APIs and tools (OpenAI, community APIs).
* Best practices for scaling, monitoring, and evaluating agent systems.

<Frame>
  <img alt="The image shows a slide on an AI Agents Curriculum, listing topics such as prerequisites, agent architecture, and practical projects, alongside a person sitting in a chair with a KodeKloud shirt." />
</Frame>

## Course outline (high-level)

| Module          | Topics covered                             | Outcome                                     |
| --------------- | ------------------------------------------ | ------------------------------------------- |
| Foundations     | What is an agent, agent types, ethics      | Understand trade-offs and governance needs  |
| Core tech       | Embeddings, vector DBs, retrieval, eval    | Build retrieval-augmented agents            |
| Architectures   | Single-agent vs multi-agent, orchestration | Design system architecture diagrams         |
| Frameworks      | LangChain, CrewAI, AutoGen, MetaGPT        | Implement agent flows and chains            |
| Tooling & APIs  | Integrating search, APIs, and tools        | Extend agent capabilities via plugins/tools |
| Projects & Labs | Task-driven and multi-role agents          | Deploy a working agent pipeline             |

Useful references:

* OpenAI API docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)
* LangChain: [https://langchain.com](https://langchain.com)
* MetaGPT: [https://github.com/metagpt/metagpt](https://github.com/metagpt/metagpt)

## Prerequisites and setup

Before running agent examples, ensure your environment variables (API keys, base URLs) are configured and never committed to source control.

<Callout icon="lightbulb">
  Store secrets (API keys, tokens) in a `.env` file and load them with `python-dotenv` during development. Use environment variables for CI/CD and secret managers in production.
</Callout>

<Callout icon="warning">
  Never commit secrets to public repositories. Improper handling of API keys can lead to unauthorized usage and unexpected costs.
</Callout>

Example: load environment variables with dotenv

```python theme={null}
from dotenv import load_dotenv
import os
