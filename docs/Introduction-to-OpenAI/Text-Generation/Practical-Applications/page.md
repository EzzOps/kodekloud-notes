# Temperature = 0.0 (Deterministic)
completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": "Explain how a solar panel works."}],
    max_tokens=100,
    temperature=0.0
)
print(completion.choices[0].message.content)
```

```python theme={null}
# Temperature = 0.5 (Balanced)
completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": "Explain how a solar panel works."}],
    max_tokens=100,
    temperature=0.5
)
print(completion.choices[0].message.content)
```

```python theme={null}
# Temperature = 1.0 (Creative)
completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": "Explain how a solar panel works."}],
    max_tokens=100,
    temperature=1.0
)
print(completion.choices[0].message.content)
```

### Top-P Sampling

Restricts choices to tokens whose cumulative probability ≤ p.

<Frame>
  ![The image is a comparison of different Top-P sampling values (1.0, 0.9, 0.3) and their effects on model behavior, such as diversity, coherence, and determinism.](https://kodekloud.com/kk-media/image/upload/v1752879238/notes-assets/images/Introduction-to-OpenAI-Overview-of-Text-Generation/top-p-sampling-comparison-model-behavior.jpg)
</Frame>

```python theme={null}
# top_p = 1.0 (All tokens)
completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": "Explain how a solar panel works."}],
    max_tokens=100,
    temperature=0.5,
    top_p=1.0
)
print(completion.choices[0].message.content)
```

```python theme={null}
# top_p = 0.9 (Top 90%)
completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": "Explain how a solar panel works."}],
    max_tokens=100,
    temperature=0.5,
    top_p=0.9
)
print(completion.choices[0].message.content)
```

```python theme={null}
# top_p = 0.3 (Highly deterministic)
completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": "Explain how a solar panel works."}],
    max_tokens=100,
    temperature=0.5,
    top_p=0.3
)
print(completion.choices[0].message.content)
```

***

## Fine-Tuning Custom Models

Fine-tuning adapts a GPT model to domain-specific tasks:

1. Prepare a JSONL dataset with input-output pairs.
2. Upload via the OpenAI API.
3. Initiate the fine-tuning job.
4. Call your specialized model just like any other.

<Frame>
  ![The image is a slide titled "Prepare Dataset" with steps "Gather the data" and "Input-Output pairs," alongside an icon depicting data analysis elements like charts and a magnifying glass.](https://kodekloud.com/kk-media/image/upload/v1752879239/notes-assets/images/Introduction-to-OpenAI-Overview-of-Text-Generation/prepare-dataset-gather-data-analysis.jpg)
</Frame>

```json theme={null}
[
  {"prompt": "Generate a confidentiality clause:", "completion": "This Confidentiality Clause ..."},
  {"prompt": "Generate a non-compete clause:", "completion": "This Non-Compete Clause ..."},
  {"prompt": "Generate a termination clause:", "completion": "This Termination Clause ..."}
]
```

***

## Tokenization Details

GPT uses byte-pair encoding (BPE) to efficiently split text into subword tokens.

```python theme={null}
prompt = "Is LeBron better than Jordan?"
response = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=100,
    temperature=0.5,
    top_p=0.3,
)

# Print each token in the response
for token in response.choices[0].message.content:
    print(f"Token: {token}")
```

***

## Transformer and Decoder Stack

After tokenization, text passes through:

1. Embedding Layer
2. Positional Encoding
3. Self-Attention Mechanism
4. Feedforward & Decoder Blocks

<Frame>
  ![The image is a diagram titled "Decoder Stack," describing the process of tokens moving through multiple layers, refining output through attention, and using feedforward layers for final token prediction.](https://kodekloud.com/kk-media/image/upload/v1752879240/notes-assets/images/Introduction-to-OpenAI-Overview-of-Text-Generation/decoder-stack-token-process-diagram.jpg)
</Frame>

***

## Best Practices

* Prompt Engineering: Craft clear, specific instructions.
* Review Outputs: Check for bias, factual accuracy, and coherence.
* Iterate Parameters: Experiment with `temperature`, `max_tokens`, and `top_p`.
* Responsible Usage: Always combine AI-generated content with human oversight, especially in sensitive domains.

***

## Links and References

* OpenAI API Documentation: [https://platform.openai.com/docs](https://platform.openai.com/docs)
* OpenAI Python SDK on PyPI: [https://pypi.org/project/openai](https://pypi.org/project/openai)
* Nucleus Sampling (Top-P) Paper: [https://arxiv.org/abs/1904.09751](https://arxiv.org/abs/1904.09751)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/428405c7-d156-47ee-9f54-a8ff04ce8542" />
</CardGroup>


# Practical Applications

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Practical-Applications/page

Explore real-world use cases for text generation with OpenAI’s GPT-4, demonstrating prompt engineering and model parameters' influence on output.

Explore real-world use cases for text generation with OpenAI’s GPT-4. Each example demonstrates how prompt engineering and model parameters influence the output. We cover:

* Blog post creation
* Summarization
* Conversational agents for customer support
* Code explanations and comments
* Creative writing
* Language translation

All snippets use the [Chat Completion API](https://platform.openai.com/docs/guides/chat) for clarity and reproducibility.

<Callout icon="lightbulb">
  Adjust `temperature` (creativity) and `max_tokens` (length) to fine-tune your results. Lower `temperature` yields deterministic output, while higher values increase randomness.
</Callout>

***

## Overview Table

| Use Case                     | Description                                    | Example Parameter Highlights           |
| ---------------------------- | ---------------------------------------------- | -------------------------------------- |
| Blog Post Generation         | Drafts articles or sections                    | `temperature=0.7`, `max_tokens=150`    |
| Summarization                | Condenses long text into concise summaries     | `temperature=0.3`, `max_tokens=100`    |
| Customer Support Agent       | Automated, professional responses to inquiries | `temperature=0.3`, system prompt setup |
| Code Explanations & Comments | Generates detailed code walkthroughs           | `temperature=0.3`, `max_tokens=150`    |
| Creative Writing             | Short stories, poems, or dialogue              | `temperature=0.9`, `max_tokens=200`    |
| Language Translation         | Translates between specified languages         | default temperature, `max_tokens=60`   |

***

## 1. Blog Post Generation

Generate full articles or individual sections by providing a clear prompt.

```python theme={null}
import openai

def generate_blog_intro():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": "Write a blog post introduction about the benefits of remote work for companies and employees."
        }],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content

print(generate_blog_intro())
```

***

## 2. Text Summarization

Condense research papers, articles, or reports into concise summaries:

```python theme={null}
import openai

def summarize_article(article_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Summarize this article on blockchain technology:\n\n{article_text}"
        }],
        max_tokens=100,
        temperature=0.3
    )
    return response.choices[0].message.content

article_text = (
    "Blockchain technology is a decentralized digital ledger that records "
    "transactions across many computers to ensure security and transparency."
)

print(summarize_article(article_text))
```

***

## 3. Conversational Agent for Customer Support

Build a polite, professional support agent that handles common inquiries:

```python theme={null}
import openai

def customer_support_response():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",  "content": "You are a helpful customer support agent."},
            {"role": "user",    "content": "A customer requests a refund for a defective product. Draft a professional response."}
        ],
        max_tokens=100,
        temperature=0.3
    )
    return response.choices[0].message.content

print(customer_support_response())
```

<Callout icon="triangle-alert">
  Never expose your API key in public repositories or client-side code. Use environment variables or a secrets manager.
</Callout>

***

## 4. Code Explanations and Comments

Automatically generate inline comments or detailed explanations for any code snippet:

```python theme={null}
import openai

def explain_code(code_snippet):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Explain the following Python function:\n\n{code_snippet}"
        }],
        max_tokens=150,
        temperature=0.3
    )
    return response.choices[0].message.content

code_snippet = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

print(explain_code(code_snippet))
```

***

## 5. Creative Writing

Use GPT-4 to craft short stories, poems, or dialogues. Increase `temperature` for more imaginative output:

```python theme={null}
import openai

def short_story():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": "Write a short story about a robot learning to love music."
        }],
        max_tokens=200,
        temperature=0.9
    )
    return response.choices[0].message.content

print(short_story())
```

***

## 6. Language Translation

Translate text between languages by specifying the source and target:

```python theme={null}
import openai

def translate_text():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": "Translate this sentence from English to French: 'I hope you have a wonderful day.'"
        }],
        max_tokens=60
    )
    return response.choices[0].message.content

print(translate_text())
```

***

## References

* [OpenAI Chat Completion API](https://platform.openai.com/docs/guides/chat)
* [OpenAI Models](https://platform.openai.com/docs/models)
* [API Best Practices](https://platform.openai.com/docs/guides/rate-limits)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/04f1a674-6fc4-47a3-a431-2ccfe3bf41ef" />
</CardGroup>
