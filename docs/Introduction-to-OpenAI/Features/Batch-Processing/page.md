# Simplified RLHF flow (conceptual)
import openai

# 1. Generate multiple responses
responses = [
    openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "Tell me a joke"}], max_tokens=50)
    for _ in range(2)
]

# 2. Human evaluators rank the responses
rankings = {"response_1": 1, "response_2": 2}  # Example feedback

# 3. Train reward model and fine-tune
reward_model = train_reward_model(rankings)
fine_tuned_model = reinforce_model(reward_model)
```

***

## External Data Sources

Integrate GPT-4 with external APIs or databases to retrieve up-to-the-minute information—ideal for financial dashboards, weather apps, or dynamic reporting tools.

Use case: build a financial assistant that fetches live stock prices, then generates an expert analysis.

```python theme={null}
import openai, requests

def get_stock_analysis(symbol):
    # Fetch real-time stock quote
    resp = requests.get(f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=YOUR_API_KEY")
    data = resp.json()[0]
    price = data['price']

    # Generate AI analysis
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"The current price of {symbol} is ${price}. Provide a detailed analysis."
        }],
        max_tokens=150,
        temperature=0.6
    )
    return chat.choices[0].message.content.strip()

print(get_stock_analysis("AAPL"))
```

***

## Multi-Turn Conversations

Maintain context across multiple user–AI exchanges to create natural, conversational experiences for virtual assistants, support bots, and educational tools.

<Frame>
  ![The image explains multi-turn conversations in chatbots, highlighting their ability to maintain context, treat inputs as connected, and remember previous exchanges.](https://kodekloud.com/kk-media/image/upload/v1752879004/notes-assets/images/Introduction-to-OpenAI-Advanced-Usage/multi-turn-conversations-chatbots-explained.jpg)
</Frame>

```python theme={null}
import openai

history = []

def chat_with_ai(user_input):
    history.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=history,
        max_tokens=120,
        temperature=0.7
    )
    ai_reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": ai_reply})
    return ai_reply

# Example dialogue
print(chat_with_ai("Hi, I need help with my order."))
print(chat_with_ai("I didn't receive my package."))
print(chat_with_ai("It's been delayed by 2 days."))
```

***

## Multi-Step Function Calling

Enable GPT-4 to orchestrate complex workflows that involve multiple function calls, data validation, and conditional logic—perfect for booking systems, form wizards, or automated pipelines.

<Frame>
  ![The image is a diagram titled "Multi-Step Function Calling," outlining four steps: complex workflows needing multiple function calls, user input triggering dynamic actions, advanced functions guiding multi-step processes, and AI assisting users through workflows.](https://kodekloud.com/kk-media/image/upload/v1752879005/notes-assets/images/Introduction-to-OpenAI-Advanced-Usage/multi-step-function-calling-diagram.jpg)
</Frame>

```python theme={null}
def step_one(user_info):
    # Collect initial details
    return f"Step 1: Received {user_info}. What's next?"

def step_two(user_info, extra):
    # Finalize using additional data
    return f"Step 2: Used {user_info} and {extra}. Workflow complete."

# Simulation
print(step_one("User data"))
print(step_two("User data", "Additional details"))
```

***

## Long-Form Content Generation with Planning

For in-depth articles, reports, or ebooks, start by generating an outline, then expand each section. This two-phase approach keeps your content structured and coherent.

<Frame>
  ![The image outlines a four-step process for long-form content generation with planning, including tasks like blogs and eBooks, generating an outline, expanding sections, and ensuring logical structure.](https://kodekloud.com/kk-media/image/upload/v1752879007/notes-assets/images/Introduction-to-OpenAI-Advanced-Usage/long-form-content-generation-process.jpg)
</Frame>

```python theme={null}
import openai

# 1. Create an outline
outline_resp = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Outline an article on AI applications in healthcare"}],
    max_tokens=80
)
outline = outline_resp.choices[0].message.content.split("\n")

# 2. Expand each point
sections = []
for item in outline:
    exp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Expand on: {item}"}],
        max_tokens=120
    )
    sections.append(exp.choices[0].message.content)

# 3. Combine into final draft
article = "\n\n".join(sections)
print(article)
```

***

## AI-Driven A/B Testing

Generate multiple versions of marketing copy—emails, headlines, ads—and measure engagement metrics (click-through, conversions) to optimize performance.

<Frame>
  ![The image is an infographic titled "AI-Driven A/B Testing," outlining four benefits: generating multiple versions of content, analyzing effectiveness, usefulness in campaigns, and optimizing marketing performance.](https://kodekloud.com/kk-media/image/upload/v1752879008/notes-assets/images/Introduction-to-OpenAI-Advanced-Usage/ai-driven-ab-testing-infographic.jpg)
</Frame>

```python theme={null}
import openai

variants = [
    "Announce our new product in a friendly tone.",
    "Announce our new product in a professional tone."
]

results = []
for idx, prompt in enumerate(variants, 1):
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )
    results.append((f"Variant {idx}", resp.choices[0].message.content))

for title, text in results:
    print(f"{title}:\n{text}\n")
```

***

## Chain of Thought Prompting

Encourage the model to “think aloud” by detailing intermediate reasoning steps. This is invaluable for solving math puzzles, logical challenges, or any task where transparency matters.

<Frame>
  ![The image is a diagram titled "Chain of Thought," outlining three steps: prompting a model to think aloud, explaining its reasoning step by step, and its usefulness for complex problem-solving tasks.](https://kodekloud.com/kk-media/image/upload/v1752879010/notes-assets/images/Introduction-to-OpenAI-Advanced-Usage/chain-of-thought-diagram-steps.jpg)
</Frame>

<Callout icon="triangle-alert">
  Chain of Thought prompts can increase token usage. Monitor your costs when enabling verbose reasoning.
</Callout>

```python theme={null}
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain step by step how to solve 2x + 5 = 15."}],
    max_tokens=150
)
print(response.choices[0].message.content)
```

***

## Hybrid Human–AI Workflows

Combine AI’s speed with human oversight to achieve both efficiency and quality. Automate routine tasks—like filtering or drafting—and have humans review edge cases or critical decisions.

<Frame>
  ![The image outlines a "Hybrid Human-AI Workflows" process, detailing four steps: integrating AI with human expertise, automating routine tasks, humans managing critical decisions, and AI filtering with human decision-making for borderline cases.](https://kodekloud.com/kk-media/image/upload/v1752879011/notes-assets/images/Introduction-to-OpenAI-Advanced-Usage/hybrid-human-ai-workflows-process.jpg)
</Frame>

**Use case:** AI flags potentially inappropriate content; human moderators review and make final decisions.

***

## Links and References

* [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
* [Reinforcement Learning Introduction](https://en.wikipedia.org/wiki/Reinforcement_learning)
* [Chain-of-Thought Prompting Paper](https://arxiv.org/abs/2201.11903)
* [Best Practices for Prompt Engineering](https://platform.openai.com/docs/guides/completions/prompt-design)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/42afe984-cd3e-4b3c-b1e0-8e9093f57a63/lesson/7680a0cf-76f7-40d7-bbb5-02751385607b" />
</CardGroup>


# Batch Processing

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Features/Batch-Processing/page

Learn to send multiple prompts using OpenAI’s Python client, covering setup, code structure, and best practices for efficient batch processing.

Learn how to send multiple prompts in one go using OpenAI’s Python client. This guide covers setup, code structure, and best practices for efficient batch processing.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install & Import](#install--import)
3. [Define Your Prompts](#define-your-prompts)
4. [Helper Function for a Single Prompt](#helper-function-for-a-single-prompt)
5. [Batch Processing Loop](#batch-processing-loop)
6. [Inspecting Results](#inspecting-results)
7. [Run the Script](#run-the-script)
8. [Reference Links](#reference-links)

## Prerequisites

* Python 3.7+
* An OpenAI API key
* `openai` Python package

<Callout icon="lightbulb">
  Store your API key as an environment variable for security:

  ```bash theme={null}
  export OPENAI_API_KEY="sk-your-api-key-here"
  ```

  Alternatively, pass it directly in code (not recommended for production).
</Callout>

## Install & Import

Install the OpenAI Python client:

```shell theme={null}
pip install openai
```

Then import and initialize the client:

```python theme={null}
from openai import OpenAI

client = OpenAI(api_key="sk-your-api-key-here")
```

## Define Your Prompts

Build a list of user prompts to process in batch:

```python theme={null}
prompts = [
    "Tell me a story about a warrior princess",
    "Generate a list of 5 business ideas",
    "Explain the theory of relativity in simpler terms",
    "Write a poem about Michael Jordan"
]
```

Feel free to extend this list to dozens or hundreds of items.

## Helper Function for a Single Prompt

Encapsulate the API call in a reusable function:

```python theme={null}
def process_prompt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.8
    )
    return response.choices[0].message.content
```

### Model Parameters

| Parameter   | Description                           | Example |
| ----------- | ------------------------------------- | ------- |
| model       | The chat model to use                 | `gpt-4` |
| messages    | Conversation history for the model    | `[...]` |
| max\_tokens | Maximum number of tokens in the reply | `250`   |
| temperature | Controls randomness (0.0–1.0)         | `0.8`   |

## Batch Processing Loop

Iterate through all prompts and collect responses:

```python theme={null}
results = []

for prompt in prompts:
    reply = process_prompt(prompt)
    results.append(reply)
```

<Callout icon="triangle-alert">
  Batch requests can incur higher costs and rate limits. Monitor your usage in the [OpenAI Dashboard](https://platform.openai.com/usage).
</Callout>

## Inspecting Results

Print each prompt alongside its generated response:

```python theme={null}
for idx, (prompt, reply) in enumerate(zip(prompts, results), start=1):
    print(f"Prompt {idx}: {prompt}")
    print(f"Response {idx}:\n{reply}\n")
```

Sample output:

```text theme={null}
Prompt 1: Tell me a story about a warrior princess
Response 1:
Once upon a time in the verdant kingdom of Eldoria, a fierce warrior princess...

Prompt 2: Generate a list of 5 business ideas
Response 2:
1. Eco-friendly packaging startup
2. Virtual event planning service
...

Prompt 3: Explain the theory of relativity in simpler terms
Response 3:
The theory of relativity, proposed by Albert Einstein, shows how time and space are linked...

Prompt 4: Write a poem about Michael Jordan
Response 4:
In courts of hardwood, he stood so tall...
```

## Run the Script

Save the code to `batch_processing.py` and execute:

```shell theme={null}
python batch_processing.py
```

Extend or customize the `process_prompt` function to add streaming output, error handling, or alternative model parameters as needed.

## Reference Links

* [OpenAI Python SDK](https://github.com/openai/openai-python)
* [Chat Completions API](https://platform.openai.com/docs/api-reference/chat)
* [Pricing & Rate Limits](https://platform.openai.com/pricing)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/42afe984-cd3e-4b3c-b1e0-8e9093f57a63/lesson/ed59d365-b517-4f70-ac1d-6b3ed61cc88d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/42afe984-cd3e-4b3c-b1e0-8e9093f57a63/lesson/2806fb1b-967e-44b8-ac17-6724eda29c0f" />
</CardGroup>
