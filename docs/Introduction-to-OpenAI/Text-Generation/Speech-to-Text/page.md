# Example usage
text = "I love the new design of the product. It’s amazing!"
print("Input:", text)
print("Sentiment:", analyze_sentiment(text))
```

Output:

```text theme={null}
Input: I love the new design of the product. It’s amazing!
Sentiment: Positive
```

If you pass mixed feedback:

```python theme={null}
text = "The product worked well, but the customer service was awful."
print("Sentiment:", analyze_sentiment(text))
```

You’ll get a combined sentiment reflecting both positive and negative aspects.

***

## Advanced Sentiment Analysis

### Fine-Grained Sentiment Categories

For deeper insights, classify text into multiple levels—from **very positive** to **very negative**.

<Frame>
  ![The image is a slide titled "Fine-Grained Sentiment Analysis," explaining the categorization of sentiment into granular levels, with examples ranging from "very positive" to "very negative."](https://kodekloud.com/kk-media/image/upload/v1752879251/notes-assets/images/Introduction-to-OpenAI-Sentiment-Analysis-With-OpenAI/fine-grained-sentiment-analysis-categorization.jpg)
</Frame>

```python theme={null}
def analyze_fine_grained_sentiment(text):
    prompt = (
        f"Classify the sentiment of the following text as 'very positive', 'positive', "
        f"'neutral', 'negative', or 'very negative': '{text}'"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

text = "The product quality is excellent, but the shipping was slow."
print("Fine-Grained Sentiment:", analyze_fine_grained_sentiment(text))
```

### Domain-Specific Fine-Tuning

When dealing with specialized fields—legal, healthcare, finance—you’ll need jargon-aware models. Fine-tuning steps:

<Callout icon="lightbulb">
  OpenAI’s fine-tuning API currently supports GPT-3.5 series models. GPT-4 fine-tuning is not yet generally available.
</Callout>

1. Prepare a labeled dataset with domain-specific texts annotated for sentiment.
2. Use the OpenAI fine-tuning endpoint to train your model.
3. Deploy and call your custom model for improved accuracy.

<Frame>
  ![The image outlines the process of fine-tuning a model for domain-specific sentiment analysis, including preparing the dataset, training the model, and using the fine-tuned model.](https://kodekloud.com/kk-media/image/upload/v1752879253/notes-assets/images/Introduction-to-OpenAI-Sentiment-Analysis-With-OpenAI/fine-tuning-domain-specific-sentiment-analysis.jpg)
</Frame>

### Aspect-Based Sentiment Analysis

Break down sentiment by features or categories—design, performance, service—to pinpoint strengths and weaknesses.

<Frame>
  ![The image is a slide titled "Aspect-Based Sentiment Analysis for Product Review," explaining how feedback can be broken down into different areas to understand which aspects are praised or criticized, and categorized by food, service, and ambiance.](https://kodekloud.com/kk-media/image/upload/v1752879254/notes-assets/images/Introduction-to-OpenAI-Sentiment-Analysis-With-OpenAI/aspect-based-sentiment-analysis-slide.jpg)
</Frame>

```python theme={null}
def aspect_based_sentiment(text, aspects):
    results = {}
    for aspect in aspects:
        prompt = f"Analyze the sentiment for '{aspect}' in: '{text}'"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.0
        )
        results[aspect] = response.choices[0].message.content.strip()
    return results

text = "The phone design is sleek and modern, but the performance is lagging at times."
aspects = ["design", "performance"]
analysis = aspect_based_sentiment(text, aspects)
for aspect, sentiment in analysis.items():
    print(f"{aspect.title()}: {sentiment}")
```

***

## Applications

| Application        | Use Case                                  | Example                                                  |
| ------------------ | ----------------------------------------- | -------------------------------------------------------- |
| Product Reviews    | Identify recurring feedback themes        | Pinpoint “battery life” complaints in customer reviews   |
| Social Media       | Monitor campaign performance and PR risks | Track sentiment spikes on Twitter after a product launch |
| Financial Analysis | Gauge market reaction to earnings calls   | Analyze Twitter chatter around quarterly reports         |

***

## Links and References

* [OpenAI API Documentation](https://platform.openai.com/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/e1a8d4f0-4265-4c2c-8a0c-5e0ff969feda" />
</CardGroup>


# Speech to Text

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Speech-to-Text/page

This tutorial guides Python developers in building a speech-to-text application using OpenAI's Whisper model for accurate audio transcriptions.

In this tutorial, you’ll build a speech-to-text application using OpenAI’s Whisper model. You’ll learn how to record or supply an audio file, send it to the OpenAI API, and receive accurate transcriptions in seconds. This guide is ideal for Python developers looking to integrate speech recognition into their projects.

## Prerequisites

Before you begin, make sure you have the following:

| Requirement    | Description                                 | Example                         |
| -------------- | ------------------------------------------- | ------------------------------- |
| Python         | Version 3.7 or newer                        | `python --version`              |
| OpenAI API Key | Access for Whisper transcriptions           | [Get your key][openai-api]      |
| Audio File     | Local MP3, WAV, or OGG file (10–20 seconds) | `~/recordings/voice_sample.mp3` |

<Callout icon="lightbulb">
  Whisper supports most common audio formats, including `mp3`, `wav`, `ogg`, and `m4a`. Ensure your file is clear and has minimal background noise for best results.
</Callout>

## 1. Install the OpenAI Python Client

First, install the OpenAI SDK using pip:

```bash theme={null}
pip install openai
```

If you’re working in a virtual environment, activate it before running the command.

## 2. Prepare Your Python Script

Create a file named `speech_to_text.py` and add the following code. It initializes the OpenAI client, reads your local audio file in binary mode, and sends it to Whisper for transcription.

```python theme={null}
import os
from openai import OpenAI
