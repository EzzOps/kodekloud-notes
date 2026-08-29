# Activate the venv and run the verification script
source /root/venv/bin/activate
python /root/code/verify_environment.py
```

Expected (cleaned-up) output example:

```text theme={null}
🔍 Verifying LangChain Lab Environment
=========================================================
✅ Python version: 3.12.3

📦 Virtual Environment Check:
✅ Running in virtual environment

📚 Required Packages:
✅ langchain
✅ openai
✅ other dependencies...
```

Once this check passes, continue to the tasks below.

***

## Quick comparison: Native SDK vs. LangChain

Use this table to get a high-level view of the differences when calling chat models directly vs. using LangChain:

| Resource Type       | Native SDK (example)                          | LangChain (wrapper)                          |
| ------------------- | --------------------------------------------- | -------------------------------------------- |
| Setup lines         | Several lines to configure client & messages  | Few lines to initialize ChatModel wrapper    |
| Message handling    | Provider-specific message objects / responses | Standardized call pattern (list of messages) |
| Provider swaps      | Often change code and response parsing        | Usually change model class or model\_name    |
| Reuse & composition | Manual orchestration                          | Built-in PromptTemplate, Chains, Parsers     |

***

## Task 1 — Boilerplate: Native SDK vs. LangChain

Native SDKs often require explicit client setup and manual message handling. Example (OpenAI SDK pseudocode):

```python theme={null}
# Example using OpenAI SDK (simplified)
import os
from openai import OpenAI  # pseudocode; actual import may differ

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")

client = OpenAI(api_key=api_key, base_url=base_url)

prompt = "Explain cloud computing in one sentence"
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
result = response.choices[0].message.content
print(result)
```

With LangChain you typically reduce that to a few lines by using a chat model wrapper and the standardized message schema:

```python theme={null}
# Using LangChain's chat model wrapper
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)

prompt = "Explain cloud computing in one sentence"
response = llm([HumanMessage(content=prompt)])  # call with a list of messages
print(response.content)
```

> **lightbulb** LangChain provides a consistent high-level API for chat and LLM calls. You still need provider-specific credentials and sometimes provider-specific classes, but swapping providers usually requires only a small change (model\_name or class).

***

## Task 2 — Multi-Model Support (A/B testing)

LangChain makes it easy to initialize multiple providers and run the same prompt against each to compare outputs for A/B testing, quality vs. cost analysis, or feature testing. Below is a compact pattern to initialize multiple model objects and iterate over them.

<Frame>
  <img alt="A screenshot of a tutorial slide titled &#x22;Task 2: Multi-Model A/B Testing (2 minutes)&#x22; explaining multi-model support and listing models to test (OpenAI GPT-4, Google Gemini, X.AI Grok). The slide shows a real-world problem example, a testing checklist and a pro tip about cost savings, with a file/code sidebar visible on the right." />
</Frame>

```python theme={null}
# task_2_multi_model.py
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

print("\n🚀 Task 2: Multi-Model Support with LangChain")
print("=" * 50)

test_prompt = "Explain cloud computing in one sentence"

# Example initializations (replace with provider-specific wrappers and creds in real use)
openai_llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)

# NOTE: The following examples illustrate a unified call pattern.
# In production, use provider-specific wrappers (e.g., Vertex AI client for Gemini)
google_llm = ChatOpenAI(
    model_name="google/gemini-2.5-flash",  # illustrative placeholder
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)

xai_llm = ChatOpenAI(
    model_name="xai/grok-medium",  # illustrative placeholder
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)

for name, llm in [("OpenAI", openai_llm), ("Google", google_llm), ("X.AI", xai_llm)]:
    try:
        response = llm([HumanMessage(content=test_prompt)])
        snippet = response.content[:200]  # show a short snippet
        print(f"{name}: {snippet}...\n")
    except Exception as e:
        print(f"{name}: Error invoking model: {e}\n")

# create marker for completion
import os
os.makedirs("/root/markers", exist_ok=True)
with open("/root/markers/task2_complete.txt", "w") as f:
    f.write("COMPLETED")
```

Sample comparison output:

```text theme={null}
Model Comparison - Same Prompt, Different Models

Prompt: 'Explain cloud computing in one sentence'

OpenAI: Cloud computing is the delivery of computing resources and services, such as storage, processing,...
Google: Cloud computing delivers on-demand computing services—including servers, storage, databases, and networks...
X.AI: Cloud computing is the delivery of on-demand computing resources, such as servers, storage, and databases...
```

This pattern simplifies A/B experiments: same code, different model instances.

> **warning** Model identifiers and client initialization vary across providers. The examples above use placeholders for non-OpenAI providers—swap to provider-specific wrappers (e.g., Vertex AI for Google Gemini) and ensure correct credentials and regional endpoints before running in production.

***

## Task 3 — Prompt templates

Avoid duplicating prompt strings across your codebase by using reusable PromptTemplate objects. Templates let you format input dynamically while keeping a consistent prompt structure.

```python theme={null}
# task_3_prompt_templates.py
import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

print("🧑‍💻 Task 3: Dynamic Prompt Templates")
print("=" * 50)

# Define a reusable template with placeholders
template = PromptTemplate(
    input_variables=["topic", "style"],
    template="Explain {topic} in {style}"
)

# Initialize the LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.7
)

# Format the template with specific values
test_prompt = template.format(topic="artificial intelligence", style="exactly 5 words")
print(f"🛰️ Sending to AI: {test_prompt}\n")

# Send to the model
response = llm([HumanMessage(content=test_prompt)])
print("AI Response:", response.content)
```

Template benefits:

* Single source of truth for prompt patterns
* Easy to update structure or wording in one place
* Clean separation of prompt logic and application data
* Works well with LLMChain for reuse across pipelines

***

## Task 4 — Output parsers (structured outputs)

For production systems you usually need structured outputs (JSON, typed objects). LangChain supports output parsers such as PydanticOutputParser to ensure responses match expected schemas.

```python theme={null}
# task_4_output_parsers.py
import os
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import HumanMessage

# Define the expected structure with Pydantic
class SummaryModel(BaseModel):
    summary: str
    keywords: list[str]

parser = PydanticOutputParser(pydantic_object=SummaryModel)

template = PromptTemplate(
    input_variables=["topic"],
    template=(
        "Provide a short summary and a list of 3 keywords for the topic: {topic}.\n"
        "Respond as JSON that matches the SummaryModel schema."
    ),
)

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.2
)

prompt = template.format(topic="artificial intelligence")
response = llm([HumanMessage(content=prompt)])
raw_text = response.content
print("Raw AI Response:", raw_text)

# Parse into structured data
parsed = parser.parse(raw_text)
print("Parsed object:", parsed)
print("Parsed type:", type(parsed))
```

Using parsers avoids fragile ad-hoc string parsing and gives you typed Python objects ready for downstream usage (databases, APIs, UIs).

***

## Task 5 — Chain composition (building pipelines)

LangChain makes composition straightforward. Use LLMChain to bind prompts and models, then post-process with parsers or helper functions to create readable, reusable pipelines.

```python theme={null}
# task_5_chain_composition.py
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

print("\n🧠 Chain 1: Simple Analysis")
print("=" * 50)

analysis_prompt = PromptTemplate(
    input_variables=["technology"],
    template="Analyze {technology} and provide pros and cons in 2-3 sentences."
)

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.3
)

analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt)

# Invoke the chain with one call
result = analysis_chain.run({"technology": "blockchain"})
print("📥 Input: 'Analyze blockchain'")
print("✅ Output:", result)
```

For more complex pipelines you can chain or sequence multiple components:

* PromptTemplate -> LLM (LLMChain) -> Output parser -> Database save -> Notification

Conceptual example:

```Python theme={null}
prompt = template.format(...)
response = llm([HumanMessage(content=prompt)])
parsed = parser.parse(response.content)
save_to_db(parsed)
send_email_notification(parsed)
```

LLMChain plus parsers and helper functions keep this pattern concise and testable.

***

## Summary

By following the exercises above you should now understand how LangChain helps you:

* Reduce boilerplate versus native SDK code paths
* Experiment with multiple models for A/B testing
* Create reusable prompt templates to avoid duplication
* Produce structured outputs using parsers like PydanticOutputParser
* Compose chains for readable, maintainable pipelines

Keep experimenting with more complex parser schemas, multi-step chains, and provider-specific integrations to adapt this pattern for production workloads.

***

## Links and References

* LangChain Documentation: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* OpenAI API: [https://platform.openai.com/docs](https://platform.openai.com/docs)
* Google Vertex AI (Gemini): [https://cloud.google.com/vertex-ai](https://cloud.google.com/vertex-ai)
* Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
* xAI / Grok (vendor): check vendor docs for model identifiers and APIs

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/d8fdf85b-c8c8-46f0-aca2-9efeb4967164)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/74c5ebbf-cdc6-4fa9-94e4-d4de72be2205)


# Practice Labs Master Prompt Engineering

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-1/Practice-Labs-Master-Prompt-Engineering/page

Guide to mastering prompt engineering with LangChain using zero-shot, one-shot, few-shot, and chain-of-thought techniques with practical examples and best practices

Master prompt engineering using LangChain to get consistent, useful, and controllable outputs from LLMs. This guide demonstrates practical prompting techniques — Zero-Shot, One-Shot, Few-Shot, and Chain-of-Thought — with runnable examples and recommended best practices.

Why this matters: LLMs often produce vague, inconsistent, or incomplete responses when prompts lack structure. The techniques below help you control format, tone, length, and reasoning so outputs match your requirements.

<Frame>
  <img alt="A screenshot of a tutorial titled &#x22;Master Prompt Engineering with LangChain&#x22; that outlines prompting techniques like zero-shot, one-shot, few-shot, and chain-of-thought. The right sidebar shows a file list of Python task scripts." />
</Frame>

> **lightbulb** High-level tip: choose the prompting technique that matches your goal — speed, format consistency, tone, or complex reasoning — and provide explicit constraints (format, length, audience) to get predictable outputs.

Environment verification

Before starting the exercises, confirm your development environment is ready (virtualenv activated, LangChain installed, OpenAI credentials configured, and an LLM connection working). This prevents runtime errors and allows you to focus on prompt quality during experiments.

Run this one-line environment check:

```bash theme={null}
source /root/venv/bin/activate && python /root/code/verify_environment.py
```

Expected verification output (example):

```text theme={null}
🔧 Verifying Prompt Engineering Lab Environment...
========================================
✅ Virtual environment is active

✅ LangChain available (version: 0.3.27)

✅ OpenAI configuration found
API Base: https://dev.kk-ai-keys.kodekloud.com/v1

✅ LLM connection test passed

🎉 All environment checks passed!
Your prompt engineering lab environment is ready.
```

> **warning** Do not commit API keys or secret files to version control. Keep credentials in environment variables or a secure secret store and verify access only from trusted machines.

Once verification passes and prompt utilities are available, proceed to the tasks below. Each task includes the concept, an example prompt or script, expected behavior, and best practices to help you reproduce consistent results.

***

## Task 1 — Zero-Shot Prompting

Zero-shot prompting asks the model to perform a task with no examples. The quality of the output depends heavily on how explicit and constrained the instruction is.

<Frame>
  <img alt="A screenshot of a presentation slide titled &#x22;Task 1: Zero-Shot Prompting (2 minutes)&#x22; that defines zero-shot prompting, contrasts vague vs. specific prompts, and gives example prompts. A dark sidebar on the right lists code filenames (e.g., task_1_zero_shot.py)." />
</Frame>

Key idea: prefer a specific instruction that includes audience, jurisdiction, required sections, and constraints (word count, tone, or format).

Illustrative Python comparison (vague vs. specific zero-shot prompts):

```python theme={null}
