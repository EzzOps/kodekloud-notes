# Load your API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request a chat completion
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "Hello, world!"}]
)

print(response.choices[0].message.content)
```

#### Using the CLI

```bash theme={null}
openai api chat_completions.create \
  -m gpt-3.5-turbo \
  -g user "Hello, world!"
```

> **lightbulb** The `openai` CLI supports commands for completions, embeddings, file uploads, and fine-tuning. Run `openai --help` to explore all options.

### Node.js SDK

#### Installation

```bash theme={null}
npm install openai
```

#### Basic Usage (JavaScript)

```javascript theme={null}
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function chat() {
  const response = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{ role: "user", content: "Hello, world!" }]
  });
  console.log(response.choices[0].message.content);
}

chat();
```

For TypeScript examples and advanced configurations, see the [Node.js SDK Guide](https://platform.openai.com/docs/libraries/javascript).

## Community Libraries

OpenAI’s documentation also links to community-maintained libraries across various languages. Use these with caution, as they are not officially supported:

![The image shows a webpage from OpenAI's documentation, listing community libraries for various programming languages like C#, C++, Clojure, and Crystal. It includes links to GitHub repositories and a disclaimer about using these libraries at one's own risk.](https://kodekloud.com/kk-media/image/upload/v1752881513/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-API-and-Libraries/openai-community-libraries-documentation.jpg)

## Next Steps

Now that you have the SDKs installed and the CLI at your fingertips, you’re ready to configure your development environment and build your first Python application that calls the OpenAI API.

## Links and References

* [OpenAI SDKs](https://platform.openai.com/docs/libraries)
* [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
* [Managing API Keys](https://platform.openai.com/docs/api-keys)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/7cf291c5-4705-4a69-965a-b0ba7d2169c6/lesson/6e105a90-147d-4c23-9021-e37885d4b3df)


# OpenAI Foundation Models

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Getting-Started-with-OpenAI/OpenAI-Foundation-Models/page

OpenAI’s foundation models enable generative AI for text, image, and audio applications, featuring GPT, DALL·E, and Whisper.

OpenAI’s foundation models form the backbone of modern generative AI, powering text, image, and audio applications. In this lesson, we explore the three flagship models available via the OpenAI API:

* **GPT**: Large language model for text tasks
* **DALL·E**: Text-to-image synthesis
* **Whisper**: Automatic speech recognition and translation

## Generative Pre-trained Transformer (GPT)

The **Generative Pre-trained Transformer (GPT)** is a transformer-based large language model trained on massive public-domain text corpora. It excels at generating contextually relevant text and supports a wide range of natural-language tasks.

> **lightbulb** GPT-3.5 is the current public release with 175 billion parameters. GPT-4 offers enhanced capabilities but is accessible only to approved users via the OpenAI waitlist.

### Key Capabilities of GPT-3.5

| Task               | Description                                    | Example API Call                                                             |
| ------------------ | ---------------------------------------------- | ---------------------------------------------------------------------------- |
| Text Generation    | Continue or complete text                      | `openai.chat.completions.create({ model: "gpt-3.5-turbo", ... })`            |
| Code Generation    | Produce code snippets in multiple languages    | `openai.chat.completions.create({ prompt: "Write Python sort...", ... })`    |
| Summarization      | Condense long documents                        | `openai.chat.completions.create({ prompt: "Summarize research...", ... })`   |
| Sentiment Analysis | Classify emotional tone                        | `openai.chat.completions.create({ prompt: "Analyze sentiment of...", ... })` |
| Chat & Q\&A        | Interactive conversations                      | `openai.chat.completions.create({ messages: [...], ... })`                   |
| Embeddings         | Vector representations for search & clustering | `openai.embeddings.create({ model: "text-embedding-ada-002", ... })`         |

![The image is a diagram illustrating the process of a Generative Pretrained Transformer (GPT) taking a prompt and producing various outputs such as classification, sentiment analysis, summarization, word completion, chat, code generation, and word embeddings.](https://kodekloud.com/kk-media/image/upload/v1752881514/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-Foundation-Models/gpt-prompt-output-process-diagram.jpg)

## DALL·E: Text-to-Image Generation

**DALL·E 2** is a diffusion-based model that transforms textual descriptions into high-fidelity images. It uses a two-step process: first generating a low-resolution image, then upscaling it.

### Generating an Image with DALL·E 2

```bash theme={null}
openai images.generate \
  --model "dall-e-2" \
  --prompt "A futuristic city skyline at sunset" \
  --n 1 \
  --size "1024x1024"
```

> **lightbulb** DALL·E 2 is currently in beta. Image credits and usage rights vary—review the [OpenAI Image Policy](https://openai.com/policies/images) before deploying.

![The image is a diagram explaining DALL-E 2, showing the process from a text prompt to image generation, with notes on its similarity to GPT and its diffusion model architecture.](https://kodekloud.com/kk-media/image/upload/v1752881515/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-Foundation-Models/dall-e-2-image-generation-diagram.jpg)

## Whisper: Automatic Speech Recognition

**Whisper** is a versatile ASR model trained on diverse languages, accents, and audio qualities. It provides both transcription and translation features out of the box.

### Transcribing Audio with Whisper

```bash theme={null}
openai audio.transcriptions.create \
  --model "whisper-1" \
  --file "meeting_recording.mp3" \
  --language "en"
```

```bash theme={null}
openai audio.translations.create \
  --model "whisper-1" \
  --file "entrevista.mp3"
```

> **triangle-alert** Audio files with background noise or overlapping speakers may reduce transcription accuracy. Preprocess audio with noise reduction when possible.

![The image is a diagram explaining Whisper, an automatic speech-recognition model that supports transcription and translation, trained on diverse languages and accents. It highlights Whisper 1 as the latest version in beta.](https://kodekloud.com/kk-media/image/upload/v1752881516/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-Foundation-Models/whisper-speech-recognition-diagram.jpg)

## Summary of OpenAI Foundation Models

| Model    | Primary Function                   | Release Status | Example Use Cases                    |
| -------- | ---------------------------------- | -------------- | ------------------------------------ |
| GPT-3.5  | Text generation & comprehension    | Production     | Chatbots, content creation, code gen |
| DALL·E 2 | Text-to-image synthesis            | Beta           | Marketing art, concept design        |
| Whisper  | Speech transcription & translation | Beta           | Meeting transcriptions, subtitles    |

## Links and References

* [OpenAI API Documentation](https://platform.openai.com/docs)
* [GPT Models Overview](https://platform.openai.com/docs/models/gpt-3-5)
* [DALL·E Overview](https://platform.openai.com/docs/models/dall-e)
* [Whisper Documentation](https://platform.openai.com/docs/models/whisper)

Explore these foundation models to unlock cutting-edge generative AI in your applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/7cf291c5-4705-4a69-965a-b0ba7d2169c6/lesson/e3354118-e1b7-48c4-8e48-11fc860f4746)
