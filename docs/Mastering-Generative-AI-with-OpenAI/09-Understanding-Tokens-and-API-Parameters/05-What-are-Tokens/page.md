# Deterministic output
completion = openai.ChatCompletion.create(
    model=p_model,
    messages=p_messages,
    n=p_n,
    max_tokens=p_max_tokens,
    temperature=0.0,
    top_p=0.0,
    presence_penalty=p_presence_penalty,
    frequency_penalty=p_frequency_penalty,
)
print("Deterministic →", completion.choices[0].message.content)

# Creative output
completion = openai.ChatCompletion.create(
    model=p_model,
    messages=p_messages,
    n=p_n,
    max_tokens=p_max_tokens,
    temperature=1.5,
    top_p=1.0,
    presence_penalty=p_presence_penalty,
    frequency_penalty=p_frequency_penalty,
)
print("Creative →", completion.choices[0].message.content)
```

By comparing these runs, you’ll see the poem’s structure and word choice change dramatically.

## Summary Table of Key Parameters

| Parameter          | Range       | Default | Description                                    |
| ------------------ | ----------- | ------- | ---------------------------------------------- |
| model              | string      | —       | Model to use (`gpt-3.5-turbo`, `gpt-4`, etc.)  |
| messages           | list        | —       | Conversation history as `[{role, content}, …]` |
| temperature        | 0–2         | 1       | Controls randomness                            |
| top\_p             | 0–1         | 1       | Nucleus sampling threshold                     |
| n                  | int         | 1       | Number of completions                          |
| max\_tokens        | int         | (model) | Max tokens in the completion                   |
| presence\_penalty  | –2.0 to 2.0 | 0       | Penalize new tokens based on prior presence    |
| frequency\_penalty | –2.0 to 2.0 | 0       | Penalize tokens based on prior frequency       |

## Links and References

* [OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat)
* [OpenAI Playground](https://platform.openai.com/playground)
* [OpenAI Python Library](https://github.com/openai/openai-python)

Next up: using these parameters to automate full blog-post generation—stay tuned!

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/e983525e-3a5a-4043-9319-4f259e41bc79/lesson/be0b7d28-12de-433c-a012-f206fdc01a71)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/e983525e-3a5a-4043-9319-4f259e41bc79/lesson/b3fccdf8-d6a6-4999-8765-c4ea22fcdd00)


# What are Tokens

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Understanding-Tokens-and-API-Parameters/What-are-Tokens/page

Explains what tokens are in LLMs, how tokenization works, token counts, context limits, costs, and tools like OpenAI Tokenizer and tiktoken.

In this lesson we’ll explain tokens—the atomic units that large language models (LLMs) use to represent text—and show how tokenization, context limits, and token costs affect your applications.

Machine learning models do not operate on characters, words, or sentences directly. Instead, they process numerical representations called tokens. When you send a prompt, it is first converted into tokens. The model processes those tokens and generates output tokens, which are then decoded back to text to form the response (for example, the output you see from ChatGPT).

Put simply: tokens are the fundamental units of text for models like GPT‑3 and ChatGPT.

<Frame>
  <img alt="A colorful flowchart titled &#x22;How Do LLMs Function?&#x22; showing a prompt turned into tokens, processed by an AI model, and then converted back into tokens to generate a response." />
</Frame>

## How tokenization works

Tokenization is the process of splitting text into tokens that the model can process. A token might represent:

* A whole word (rare for many languages)
* A character (common in some languages or tokenizers)
* A subword or byte-pair encoded piece (common for OpenAI models)

Most modern OpenAI tokenizers use a subword (BPE-like) scheme, so many tokens are partial words. Tokenization depends on the encoding used by the specific model.

## Token size: characters, words, and tokens (rough guidelines)

There is no fixed 1:1 mapping between tokens and words, but a useful approximation for English is:

| Measure        | Approximate mapping     |
| -------------- | ----------------------- |
| 1 token        | \~4 characters          |
| 1 token        | \~0.75 words            |
| 100 tokens     | \~75 words              |
| \~2,000 tokens | \~1,500 words (roughly) |

So 100 tokens is approximately 75 words, and a 1,500‑word document often maps to \~2,000 tokens. Exact counts vary by text and encoding.

<Frame>
  <img alt="A slide titled &#x22;Tokenization&#x22; explaining how OpenAI models (e.g., GPT-3) break input into tokens, with examples: 1 token ≈ 4 characters, 100 tokens ≈ 75 words, and ~1,500 words ≈ 2,048 tokens. It also notes that the API breaks prompts into tokens before processing." />
</Frame>

## Tools to inspect tokenization

Two practical ways to explore how text maps to tokens:

* The interactive OpenAI Tokenizer: [https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer) — paste text and see tokens/token IDs and counts.
* The open-source library tiktoken: [https://github.com/openai/tiktoken](https://github.com/openai/tiktoken) — programmatic encoding/decoding in Python.

<Frame>
  <img alt="A slide titled &#x22;Tools to Explore Tokens&#x22; showing two screenshots: OpenAI's online Tokenizer tool on the left (https://platform.openai.com/tokenizer) and the tiktoken GitHub repository on the right (https://github.com/openai/tiktoken). The images highlight tokenized text, token counts, and repository files." />
</Frame>

> **lightbulb** Always use the tokenizer/encoding associated with the model you are calling (for example, use the encoding for "gpt-3.5-turbo" when calling that model). Token counts and token IDs differ across encodings.

## Encoding and decoding with tiktoken (example)

Encoding converts text to token IDs; decoding converts token IDs back to text. tiktoken implements an efficient BPE-style tokenizer used by OpenAI models and lets you inspect tokens programmatically.

Install tiktoken:

```bash theme={null}
pip install tiktoken
```

Example Python usage:

```python theme={null}
import tiktoken
