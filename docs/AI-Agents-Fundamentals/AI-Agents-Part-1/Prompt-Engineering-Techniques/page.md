# Step 1: Import the OpenAI library
# This library helps us talk to AI models
import openai

# Step 2: Import os for environment variables
# This helps us access API keys safely
import os

print("✅ Step 1 Complete: Libraries imported!")
print("- openai: For making API calls")
print("- os: For accessing environment variables")

# Create marker for the automated lab system
os.makedirs("/root/markers", exist_ok=True)
with open("/root/markers/task1_imports_complete.txt", "w") as f:
    f.write("SUCCESS")
```

Run it like this:

```bash theme={null}
root@controlplane ~/code via v3.12.3 (venv) ❯ python3 /root/code/task_1_import_setup.py
✅ Step 1 Complete: Libraries imported!
- openai: For making API calls
- os: For accessing environment variables
```

## Authentication and client setup

To authenticate you need:

* OPENAI\_API\_KEY — your secret API key
* OPENAI\_API\_BASE — (optional) custom API base URL

Keep these values out of source control. Use environment variables, a secrets manager, or CI secrets.

## Task 2 — Initialize the OpenAI client

Open `task_2_client_initialization.py` and initialize the OpenAI client using environment variables. This example creates a client object you can reuse across requests.

```python theme={null}
#!/usr/bin/env python3
"""
Task 2: Initialize the OpenAI client
Set up the client using environment variables.
"""

import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_API_BASE")
)

print("✅ Step 2 Complete: Connected to OpenAI!")
api_key_preview = os.getenv('OPENAI_API_KEY')[:10] + "..." if os.getenv('OPENAI_API_KEY') else "(not set)"
print(f"- API Key: {api_key_preview}")
print(f"- Base URL: {os.getenv('OPENAI_API_BASE')}")
```

Example run:

```bash theme={null}
root@controlplane ~/code via v3.12.3 (venv) ❯ python3 /root/code/task_2_client_initialization.py
✅ Step 2 Complete: Connected to OpenAI!
- API Key: Sk-kKA1-86...
- Base URL: https://dev.kk-ai-keys.kodekloud.com/v1
```

If client initialization fails, confirm your environment variables are set and that the model you request is available for your account.

## Chat completions — the basics

Chat completions implement conversational interactions. You send an ordered list of messages (with roles) and the model returns assistant messages.

Minimal Python pattern:

```python theme={null}
client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Your question here"}
    ]
)
```

Roles:

* system — high-level instructions that define behavior
* user — user input
* assistant — model replies

## Task 3 — Make an API call

Open `task_3_api_call_explained.py`. Configure the model and messages, then make a call where the AI introduces itself.

```python theme={null}
#!/usr/bin/env python3
"""
Task 3: Make your first API call
Send a simple user message and print the full response.
"""

import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_API_BASE")
)

response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Hello AI, please introduce yourself"}
    ]
)

print("✅ API Call Successful!")
print()
print("🤖 AI said:")
print(response.choices[0].message.content)
print()
print(f"📊 Total tokens used: {response.usage.total_tokens}")
```

Example output:

```bash theme={null}
root@controlplane ~/code via v3.12.3 (venv) ❯ python3 /root/code/task_3_api_call_explained.py
✅ API Call Successful!

🤖 AI said:
Hello! I'm ChatGPT, your AI assistant here to help with a wide range of tasks—from answering questions and providing explanations to creative writing and problem-solving. How can I assist you today?

📊 Total tokens used: 53
```

If you receive PermissionDenied or "model not supported" errors, switch to a model available on your account or check API permissions.

## Task 4 — Extract the AI's response

Responses contain nested structures. The straightforward path to the assistant's reply is:

```text theme={null}
response.choices[0].message.content
```

Open `task_4_extract_response.py` to extract and print that text.

```python theme={null}
#!/usr/bin/env python3
"""
Task 4: Extract the AI's response
Show how to retrieve the assistant's message from the response object.
"""

import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_API_BASE")
)

response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "What is Python in one sentence?"}
    ]
)

ai_text = response.choices[0].message.content

print("🍬 Successfully extracted the AI's response!")
print("\n" + "="*60)
print("Question: What is Python in one sentence?")
print("\nAI's Answer:")
print(ai_text)
print("="*60)

# Show the golden path
print("\n🔑 THE GOLDEN PATH - Memorize this:")
print("response.choices[0].message.content")
```

Example output:

```bash theme={null}
root@controlplane ~/code via v3.12.3 (venv) ❯ python3 /root/code/task_4_extract_response.py
🍬 Successfully extracted the AI's response!
============================================================
Question: What is Python in one sentence?

AI's Answer:
Python is a high-level, interpreted programming language known for its readability, simplicity, and versatility across various applications.
============================================================

🔑 THE GOLDEN PATH - Memorize this:
response.choices[0].message.content

✅ Task 4 completed! You now know how to extract AI responses!
```

## Tokens and costs

Tokens are the billing and processing unit used by models. Every request consumes tokens from your account:

| Token Type               | What it represents                       | Example                      |
| ------------------------ | ---------------------------------------- | ---------------------------- |
| prompt/input tokens      | Tokens consumed by the input you send    | Your question text           |
| completion/output tokens | Tokens generated by the model as a reply | The assistant's answer       |
| total tokens             | Sum of prompt + completion               | Billed total for the request |

Output tokens are often priced higher than input tokens, so being concise helps control costs.

<Callout icon="lightbulb">
  Keep your API key secure. Never hard-code it in scripts or check it into version control. Use environment variables or a secrets manager.
</Callout>

<Frame>
  <img alt="A screenshot of a dark-themed code editor and documentation titled &#x22;Understanding Tokens & AI Economics,&#x22; showing bullet points about token types, costs, and where to find usage. The right side shows a file list with Python scripts (e.g., task_4_extract_response.py)." />
</Frame>

## Task 5 — Extract token usage and compute cost

Open `task_5_tokens_and_costs.py`. The response includes a `usage` object with three fields: `prompt_tokens`, `completion_tokens`, and `total_tokens`. Use these values to compute a simple cost estimate with your per-token pricing.

```python theme={null}
#!/usr/bin/env python3
"""
Task 5: Extract token usage and compute cost
Read usage from the response and print a cost breakdown.
"""

import openai
import os

# Example per-token prices (replace with real prices for accurate cost)
INPUT_TOKEN_PRICE = 0.000000789  # example price per input token in dollars
OUTPUT_TOKEN_PRICE = 0.0000023   # example price per output token in dollars

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_API_BASE")
)

response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Explain what an API is in two sentences."}
    ]
)

input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

input_cost = input_tokens * INPUT_TOKEN_PRICE
output_cost = output_tokens * OUTPUT_TOKEN_PRICE
total_cost = input_cost + output_cost

print("📊 Token Usage Report:")
print("="*50)
print(f"  Your question used: {input_tokens} tokens")
print(f"  AI's response used: {output_tokens} tokens")
print(f"  Total tokens billed: {total_tokens} tokens")
print("="*50)
print("\n🧾 Cost Breakdown for This Call:")
print(f"Input cost: ${input_cost:.6f} ({input_tokens} tokens)")
print(f"Output cost: ${output_cost:.6f} ({output_tokens} tokens)")
print(f"TOTAL COST: ${total_cost:.6f}")
```

Sample output (varies per request and model):

```bash theme={null}
root@controlplane ~/code via v3.12.3 (venv) ❯ python3 /root/code/task_5_tokens_and_costs.py
📊 Token Usage Report:
==================================================
  Your question used: 19 tokens
  AI's response used: 301 tokens
  Total tokens billed: 320 tokens
==================================================

🧾 Cost Breakdown for This Call:
Input cost: $0.000015 (19 tokens)
Output cost: $0.000693 (301 tokens)
TOTAL COST: $0.000708
```

<Callout icon="warning">
  Be careful with long model responses or high-frequency calls — costs can add up quickly. Use concise prompts, set max tokens when needed, and monitor usage.
</Callout>

<Frame>
  <img alt="A screenshot of a “Congratulations!” tutorial screen listing mastered topics (environment setup, chat completions, models/roles, extracting responses, token/costs) and a highlighted key takeaway path. A dark editor sidebar on the right shows Python task filenames for the lab." />
</Frame>

## Wrap-up

Congrats — by completing this lab you:

* Verified your environment and runtime
* Initialized the OpenAI Python client
* Made chat completion requests
* Extracted assistant replies via response.choices\[0].message.content
* Read token usage and estimated costs

Next steps: experiment with system messages to control behavior, try longer multi-turn conversations, and test different models to compare quality and cost.

## Quick reference and links

* OpenAI API docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)
* OpenAI homepage: [https://openai.com](https://openai.com)
* LangChain (multi-provider tooling): [https://learn.kodekloud.com/user/courses/langchain](https://learn.kodekloud.com/user/courses/langchain)

Relevant local files in this lab:

| File                               | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| verify\_environment.py             | Check Python, venv, and environment variables |
| task\_1\_import\_setup.py          | Import libraries and mark completion          |
| task\_2\_client\_initialization.py | Initialize the OpenAI client                  |
| task\_3\_api\_call\_explained.py   | Send a simple chat completion                 |
| task\_4\_extract\_response.py      | Extract the assistant message                 |
| task\_5\_tokens\_and\_costs.py     | Read token usage and compute estimated cost   |

You're ready to build on this foundation and explore richer prompts, system instructions, and multi-turn dialogues. Good luck!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/8b3f0db0-6005-45a1-a3c4-352b450fca3c" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/f4f7ef65-9d60-4cc3-a49b-11c2e4014764" />
</CardGroup>


# Prompt Engineering Techniques

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-1/Prompt-Engineering-Techniques/page

Guide to crafting prompts for TechCorp's AI assistant covering techniques, role and format specification, examples, and best practices to improve output quality and consistency

Prompt engineering is the practice of designing inputs to an AI assistant so the responses are accurate, concise, and formatted for your needs. Here we focus on how to craft prompts for TechCorp’s AI Document Assistant — not how to build LangChain apps — because small prompt changes (scope, role, format) dramatically affect output quality.

<Frame>
  <img alt="A hand-drawn diagram on a black background showing &#x22;Tech Corp's AI Application&#x22; in the center with arrows to surrounding components like a large language model, LangChain, R.A.G., a vector/database, server/stack icons, and a chat UI. The sketch maps how different AI building blocks connect into the central application." />
</Frame>

Why prompt engineering matters

* Vague prompts force the model to guess intent, leading to longer, noisier, or off-topic responses.
* Adding minimal constraints (audience, region, format) narrows results and improves relevance.
* Explicit roles and format instructions help the assistant maintain consistent tone and structure.

Example of a vague prompt:

```text theme={null}
what is the policy?
```

More specific and actionable:

```text theme={null}
what's the company's remote work policy for international employees?
```

<Callout icon="lightbulb">
  Be explicit about scope, audience, and desired output format. Small additions — like region, role, or format — often produce substantially better answers.
</Callout>

Define role and output format
Telling the model “who it is” and “how to present the answer” controls voice and structure. For example:

```text theme={null}
You are a TechCorp customer support expert. When asked about company policy, always respond with bullet points for readability.
```

This simple role + format instruction reduces ambiguity and yields predictable outputs across multiple prompts.

Prompting techniques overview
Choose the appropriate technique based on how much guidance you provide: zero-shot, one-shot, few-shot, or chain-of-thought.

Zero-shot prompting
Zero-shot asks the model to perform a task without examples. It relies on the model’s internal knowledge and generalization.

Example:

```text theme={null}
Write a data privacy policy for our European customers.
```

<Frame>
  <img alt="A hand-drawn diagram titled &#x22;zero-shot prompting&#x22; showing a prompt bubble (example text: &#x22;Write a data privacy policy for our European customers&#x22;) feeding into an &#x22;Agent&#x22; drawn as a neural‑network node cluster. Arrows indicate the agent's existing knowledge and an output direction." />
</Frame>

One-shot and few-shot prompting
One-shot and few-shot prompts include one or several examples in the prompt to demonstrate the desired output format, tone, or structure. This helps the model pattern-match and produce consistent results.

Workflow example:

* Provide a template or single example of the policy structure.
* Ask the model to “Write a data privacy policy following the same structure.”

Few-shot is similar but supplies multiple samples to cover edge cases and formatting variations.

<Frame>
  <img alt="A hand-drawn diagram illustrating one-shot prompting: a prompt template on the left feeds into an &#x22;Agent&#x22; (a neural network) in the center, producing output with a specified format and style. Arrows and labels like &#x22;template&#x22; and &#x22;format/style&#x22; annotate the process." />
</Frame>

Chain-of-thought prompting
Chain-of-thought (CoT) prompts ask the model to show or follow intermediate reasoning steps. Instead of only requesting a final output, you specify the stepwise process the assistant should use.

Example steps:

* Review current GDPR requirements for data retention periods.
* Analyze the existing policy to identify gaps.
* Research industry best practices for similar companies.
* Draft specific, implementable recommendations.

<Callout icon="warning">
  Chain-of-thought prompts can improve analytic depth but may increase verbosity and expose intermediate reasoning. In production, avoid revealing sensitive internal reasoning or use post-processing to extract only final action items.
</Callout>

Comparison table: choosing a technique

| Technique        | When to use                              |                                Strengths | Limitations                            |
| ---------------- | ---------------------------------------- | ---------------------------------------: | -------------------------------------- |
| Zero-shot        | Quick tasks with standard formats        |                       Fast, minimal prep | May be too generic                     |
| One-shot         | You have one clear example/template      |            Low prep, improved formatting | Limited coverage                       |
| Few-shot         | You can provide multiple examples        | Better generalization, covers edge cases | More prompt length                     |
| Chain-of-thought | Complex reasoning or multi-step analysis |                 Higher-quality reasoning | Verbose; may reveal intermediate steps |

Actionable prompt template
Use this scaffold to compose consistent, reusable prompts. Replace each bracketed section with your specifics.

```text theme={null}
Role: You are a [role], e.g., "TechCorp policy expert".
Context: [Provide relevant context or background].
Examples: [Optional — paste 1–3 examples or a single template].
Task: [Clear instruction of what to do].
Constraints: [e.g., length, regulations, audience region].
Format: [e.g., bullet points, numbered steps, markdown, JSON].
```

Example using the template:

```text theme={null}
Role: You are a TechCorp legal analyst.
Context: Our European engineering teams process customer IDs and logs.
Examples: See the provided policy template below.
Task: Draft a GDPR-compliant data retention policy focused on logs and temporary IDs.
Constraints: Max 600 words; include retention periods and deletion processes.
Format: Use numbered sections and a short executive summary.
```

Prompt-engineering best practices

* Start with a clear role and targeted context.
* Specify the desired output format (bullets, sections, JSON).
* Supply examples or templates for consistent formatting.
* Limit scope (audience, region, timeframe) to avoid irrelevant detail.
* Test iteratively — refine prompts based on actual outputs.
* Use chain-of-thought only when you need the model’s intermediate reasoning, and sanitize outputs before exposing them.

Examples: bad vs. improved prompts

* Bad: what is the policy?
* Improved: You are a TechCorp HR expert. Summarize the remote-work policy for international employees in 5 bullet points, highlighting eligibility, timezone expectations, and tax considerations.

References and further reading

* [LangChain — KodeKloud course](https://learn.kodekloud.com/user/courses/langchain)
* [OpenAI Prompting Guide](https://platform.openai.com/docs/guides/completion/prompt-design)
* [Retrieval-Augmented Generation (RAG) overview](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

Putting it together
Prompt engineering is selecting the right method (zero-/one-/few-shot, or chain-of-thought) and composing a prompt with clear role, context, examples, and format. Thoughtful prompts act like precise instructions for the agent, improving relevance, consistency, and usefulness of the assistant’s responses.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/ae14e196-126f-4d3e-8ede-d3b09fca7ce0" />
</CardGroup>
