# In [1]
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
def get_word_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Send a chat-style prompt and return the assistant's content string.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response.choices[0].message.content
```

Best practices

* Separate context (source text) from instructions (the prompt). This makes prompts reusable and easier to test.
* Delimit large contexts (e.g., using triple backticks) so the model can clearly distinguish input data from the instruction.
* When requesting structured outputs (JSON, XML, CSV), be explicit about the required schema to minimize parsing errors.

> **lightbulb** When embedding large context into prompts, delimit it (for example with triple
  backticks) so the model can clearly distinguish the source content from the
  instruction.

Summarization

* Keep the source text and the instruction separate. Here’s an excerpt from Steve Jobs' 2005 Stanford commencement address. We ask for a 500-word summary, then show how to request a bullet-point summary for scannability.

```python theme={null}
# In [2]: Context (excerpt)
context = '''
Steve Jobs' 2005 Stanford Commencement Address
I am honored to be with you today at your commencement from one of the finest universities in the world. I never gradu

The first story is about connecting the dots.

I dropped out of Reed College after the first 6 months, but then stayed around as a drop-in for another 18 months or so
'''
```

500-word summary prompt and invocation:

````python theme={null}
# In [3]: Prompt asking for a 500-word summary
prompt = f"""
Create a summary capturing the main points and key details in 500 words based on the content delimited by triple backticks.

```{context}```
"""
response = get_word_completion(prompt)
print(response)
````

Bullet summary (quick, scannable):

````python theme={null}
# In [4]: Bullet summary prompt
prompt_bullets = f"""
Create a summary capturing the main points and key details as bullets based on the content delimited by triple backticks.

```{context}```
"""
response_bullets = get_word_completion(prompt_bullets)
print(response_bullets)
````

Sample bullet-form output (example):

* Steve Jobs delivered a commencement address at Stanford University in 2005 and shared three stories from his life.
* First story: connecting the dots — dropping out led him to learn calligraphy, which later influenced Macintosh design.
* Second story: love and loss — getting fired from Apple enabled him to start anew (NeXT, Pixar) and eventually return.
* Third story: death — facing mortality focused his priorities; follow your intuition and live authentically.
* Closing advice: "Stay Hungry. Stay Foolish." — remain curious and brave in pursuing your work.

Sentiment analysis

* Use the same structure: pass the text as context, then instruct the model how to label each item. This pattern is useful for generating labeled datasets for downstream model training or analysis.

````python theme={null}
# In [5]: Sentiment analysis context
context_reviews = '''
1. If you sometimes like to go to the movies to have fun, Wasabi is a good place to start.
2. An idealistic love story that brings out the latent 15-year-old romantic in everyone.
3. The story loses its bite in a last-minute happy ending that's even less plausible than the rest of the picture.
'''
prompt_sentiment = f"""
Analyze the sentiment of the reviews delimited in triple backticks.

First show the actual review and then add the sentiment - Positive, Negative, or Neutral.

```{context_reviews}```
"""
response_sentiment = get_word_completion(prompt_sentiment)
print(response_sentiment)
````

Expected output example:

1. If you sometimes like to go to the movies to have fun, Wasabi is a good place to start.
   Sentiment: Positive

2. An idealistic love story that brings out the latent 15-year-old romantic in everyone.
   Sentiment: Positive

3. The story loses its bite in a last-minute happy ending that's even less plausible than the rest of the picture.
   Sentiment: Negative

Note: LLMs can be used to generate labeled data (for example, labeling customer reviews or social media posts) which you can then use for downstream analysis or to train supervised models.

Translation (poetic translation)

* LLMs can translate and preserve tone. Provide the poem as context and request a tone-preserving English rendering.

````python theme={null}
# In [6]: Poem translation context
context_poem = """
Demain, dès l'aube, à l'heure où blanchit la campagne,
Je partirai. Vois-tu, je sais que tu m'attends.
J'irai par la forêt, j'irai par la montagne.
Je ne puis demeurer loin de toi plus longtemps.
Je marcherai les yeux fixés sur mes pensées,
Sans rien voir au dehors, sans entendre aucun bruit,
Seul, inconnu, le dos courbé, les mains croisées,
Triste, et le jour pour moi sera comme la nuit.
Je ne regarderai ni l'or du soir qui tombe,
Ni les voiles au loin descendant vers Harfleur,
Et quand j'arriverai, je mettrai sur ta tombe
Un bouquet de houx vert et de bruyère en fleur.
"""
prompt_translate = f"""
Write an English poem based on the French poem delimited in triple backticks.

```{context_poem}```
"""
response_translate = get_word_completion(prompt_translate)
print(response_translate)
````

Sample poetic translation (example):
Tomorrow, at dawn's early light,
I shall depart, for I know you await.
Through forest and mountain, I'll take flight,
For I cannot bear this distance, this weight.

With eyes fixed on my thoughts, I'll tread,
Unseeing of the world, deaf to its sound.
Alone, unknown, stooped with a heavy head,
Gloomy, for me, day will be night unbound.

I'll not gaze upon the evening's golden hue,
Nor watch distant sails descend to Harfleur.
And when I arrive, a bouquet I'll bestrew,
Of green holly and blooming heather pure.

And there, upon your grave, my tribute laid,
I'll feel your presence, though you've been away.

Format conversion (plain text → JSON / XML / JSONL)

* Convert semi-structured plain text into structured formats for ingestion into pipelines and databases. Be explicit about the desired output schema (keys, types) to reduce ambiguity.

````python theme={null}
# In [7]: States and capitals context
context_states = """
1. Alabama - Montgomery
2. California - Sacramento
3. Florida - Tallahassee
4. Georgia - Atlanta
5. Illinois - Springfield
6. Massachusetts - Boston
7. New York - Albany
8. Texas - Austin
9. Pennsylvania - Harrisburg
10. Washington - Olympia
"""
prompt_formats = f"""
From the content delimited in triple backticks, format it in JSON, XML, and JSONL.
```{context_states}```
"""
response_formats = get_word_completion(prompt_formats)
print(response_formats)
````

Example model-converted outputs (examples):

JSON:

```json theme={null}
[
  {
    "state": "Alabama",
    "capital": "Montgomery"
  },
  {
    "state": "California",
    "capital": "Sacramento"
  },
  ...
]
```

XML:

```xml theme={null}
<root>
  <state>
    <name>Alabama</name>
    <capital>Montgomery</capital>
  </state>
  <state>
    <name>California</name>
    <capital>Sacramento</capital>
  </state>
  ...
</root>
```

JSONL (JSON Lines):

```json theme={null}
{"state": "Alabama", "capital": "Montgomery"}
{"state": "California", "capital": "Sacramento"}
{"state": "Florida", "capital": "Tallahassee"}
{"state": "Georgia", "capital": "Atlanta"}
{"state": "Illinois", "capital": "Springfield"}
{"state": "Massachusetts", "capital": "Boston"}
{"state": "New York", "capital": "Albany"}
{"state": "Texas", "capital": "Austin"}
{"state": "Pennsylvania", "capital": "Harrisburg"}
{"state": "Washington", "capital": "Olympia"}
```

Note: JSONL (also called "newline-delimited JSON" or "NDJSON") is not the same as JSON-LD. JSONL means each line is a separate valid JSON object — convenient for streaming and line-by-line processing.

Summary

* What we covered:
  * Summarization: fixed-length summaries and bullet-style output, emphasizing separation of context and prompt.
  * Sentiment analysis: labeling text as Positive / Negative / Neutral for downstream use.
  * Translation: preserving tone (poetic translation example).
  * Format conversion: converting semi-structured text into JSON, XML, and JSONL for pipelines.

Further reading and references

* OpenAI Chat API documentation: [https://platform.openai.com/docs/api-reference/chat](https://platform.openai.com/docs/api-reference/chat)
* JSONL / NDJSON specification and best practices: [https://jsonlines.org/](https://jsonlines.org/)
* Secrets management best practices: consider using environment variables or dedicated secret stores (Vault, AWS Secrets Manager, etc.)

Embeddings and similarity search are core techniques used for retrieval-augmented generation and semantic search — topics for a follow-up lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/0bad671a-6a77-4e3b-b63d-6c771ea3087f/lesson/57e895f5-f8b2-4066-a203-8cd242d01870)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/0bad671a-6a77-4e3b-b63d-6c771ea3087f/lesson/513d39ab-dcb6-4f67-a208-26949181f4a0)


# Performing Text Processing and Analysis

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Performing-Text-Processing-and-Analysis/Performing-Text-Processing-and-Analysis/page

This article discusses advanced NLP techniques using LLMs for tasks like summarization, sentiment analysis, translation, and formatting through a single API endpoint.

Welcome back to our deep dive into advanced Natural Language Processing (NLP) techniques powered by Large Language Models (LLMs). With GPT-3.5, GPT-4, and similar models, you can go well beyond simple text completion to perform a suite of tasks—such as summarization, sentiment analysis, translation, and formatting—using a single API endpoint.

> **lightbulb** You only need one LLM instance to handle multiple text-based tasks, reducing infrastructure complexity and accelerating development.

Before the rise of LLMs, each capability required its own specialized neural network. Today’s generative AI models are trained so broadly that you can prompt the same model to:

![The image illustrates a large language model (LLM) at the center, with arrows pointing to its applications: summarization, translation, sentiment analysis, and formatting and conversion.](https://kodekloud.com/kk-media/image/upload/v1752881540/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Performing-Text-Processing-and-Analysis/large-language-model-applications-diagram.jpg)

| Task               | Description                                | Example Prompt                                           |
| ------------------ | ------------------------------------------ | -------------------------------------------------------- |
| Summarization      | Condense long articles into key takeaways  | “Summarize the following report in three bullet points.” |
| Sentiment Analysis | Detect positive, neutral, or negative tone | “Analyze the sentiment of this customer review.”         |
| Translation        | Convert text between multiple languages    | “Translate this paragraph from English to Spanish.”      |
| Text Formatting    | Reformat or convert markup, code, or prose | “Convert this Markdown list into an HTML table.”         |

## Demo Walkthroughs

In the sections below, we'll explore simple code examples using the [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction). Each demo shows how easily GPT-3.5 or GPT-4 can handle:

1. Summarization
2. Sentiment Analysis
3. Translation
4. Text Conversion

> **triangle-alert** Be mindful of token usage and rate limits when processing large volumes of text. Review the [OpenAI API pricing](https://platform.openai.com/pricing) before running extensive jobs.

## Links and References

* [OpenAI GPT-3.5 Model](https://platform.openai.com/docs/models/gpt-3-5)
* [OpenAI GPT-4 Model](https://platform.openai.com/docs/models/gpt-4?lang=python)
* [OpenAI API Documentation](https://platform.openai.com/docs/)
* [Generative AI Overview (Wikipedia)](https://en.wikipedia.org/wiki/Generative_adversarial_network)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/0bad671a-6a77-4e3b-b63d-6c771ea3087f/lesson/971e03a5-ea68-4a02-9e73-84ea344306c9)
