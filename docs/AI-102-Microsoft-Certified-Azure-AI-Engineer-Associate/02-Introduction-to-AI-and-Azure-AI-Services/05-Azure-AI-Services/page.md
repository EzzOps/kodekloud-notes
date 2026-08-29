# Azure AI Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Introduction-to-AI-and-Azure-AI-Services/Azure-AI-Services/page

Overview of Azure AI Services and how to integrate language, speech, vision, and generative AI capabilities into applications with minimal code and managed APIs

In this lesson we explore Azure AI Services — a set of managed, production-ready AI capabilities you can integrate into applications to add intelligence without training models from scratch. Azure groups these offerings by capability so you can pick the best service for your scenario, whether you need language understanding, speech, vision, or generative AI.

These services speed up development and reduce operational overhead: with a few API calls or a small SDK integration you can add document reading, speech transcription, image understanding, or generative content to your app.

## Capabilities overview

Below is a concise breakdown of the primary capability areas and what they enable:

### Language (Azure AI Language Services)

* Text analysis: extract language, key phrases, entities, and structured information from text.
* Sentiment analysis: classify text as positive, negative, or neutral.
* Translation: convert text between languages in real time.
* QnA / knowledge mining: build question-answering systems from documents and knowledge bases.

### Speech (Azure Speech services / Speech SDK)

* Speech-to-text (recognition): convert spoken audio into transcribed text.
* Text-to-speech (synthesis): generate natural-sounding audio from text.
* Speech translation: translate spoken language in real time and produce synthesized output.

### Vision (Azure AI Vision / Document Intelligence)

* Image & video processing: analyze frames to detect scenes, faces, activities, and visual insights.
* Image classification: label images with objects, scenes, or tags.
* Object detection: locate and label objects with bounding boxes.
* OCR (optical character recognition): extract text from scanned documents and images.

### Generative AI (Azure OpenAI and related services)

* Text generation: create human-like text for emails, summarization, code, or creative writing.
* Image generation: create or transform images from text prompts.
* Assistants & custom conversational experiences: build chat-based or multi-modal assistants powered by large generative models.

<Frame>
  <img alt="A presentation slide titled &#x22;Azure AI Services&#x22; showing four colored panels—Language, Speech, Vision, and Generative AI—listing capabilities like text analysis and translation, speech recognition and synthesis, image/video processing and OCR, and AI-powered content creation." />
</Frame>

Azure packages these capabilities into focused offerings such as:

* Azure AI Language Services
* Azure AI Vision
* Azure AI Document Intelligence
* Azure AI Search
* Azure OpenAI Resource

With minimal SDK setup or a few REST API calls, you can add document reading, speech transcription and translation, image understanding, and generative content directly into your applications.

## Service map: which Azure resource to choose

| Service / Resource             | Primary use case                                        | Quick example                              |
| ------------------------------ | ------------------------------------------------------- | ------------------------------------------ |
| Azure AI Language Services     | Text analytics, entity extraction, translation, QnA     | Sentiment analysis, key phrase extraction  |
| Azure Speech                   | Speech-to-text, text-to-speech, speech translation      | Live transcription and TTS for apps        |
| Azure AI Vision                | Image and video analysis                                | Object detection, image classification     |
| Azure AI Document Intelligence | Document parsing, OCR, structured data extraction       | Invoice parsing, form understanding        |
| Azure AI Search                | Indexing and semantic search over documents             | Search experience with AI-enriched results |
| Azure OpenAI Resource          | Generative text and image models, conversational agents | Summaries, code generation, assistants     |

## Quick-start examples

Text analytics (sentiment) — REST (curl)

```bash theme={null}
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/text/analytics/v3.1/sentiment" \
  -H "Ocp-Apim-Subscription-Key: <your-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      { "id": "1", "language": "en", "text": "Azure AI Services make development faster!" }
    ]
  }'
```

Speech recognition — JavaScript (Speech SDK)

```javascript theme={null}
import { SpeechConfig, AudioConfig, SpeechRecognizer } from "microsoft-cognitiveservices-speech-sdk";

const speechConfig = SpeechConfig.fromSubscription("<your-key>", "<your-region>");
const audioConfig = AudioConfig.fromDefaultMicrophoneInput();
const recognizer = new SpeechRecognizer(speechConfig, audioConfig);

recognizer.recognizeOnceAsync(result => {
  console.log("Recognized text:", result.text);
  recognizer.close();
});
```

These snippets demonstrate how little code is required to start adding AI to your application.

> **lightbulb** Tip: Start with managed services (Language, Speech, Vision) for common scenarios. Use Azure OpenAI for advanced generative tasks and custom assistants. Combine services—for example, use OCR from Document Intelligence + Azure AI Search for semantic search over scanned documents.

> **warning** Warning: When integrating AI features, protect sensitive data and ensure compliance with regional data residency and privacy requirements. Review Azure’s data processing terms and choose the right resource type and region for your workload.

## Next steps and resources

* Azure AI Services overview: [https://learn.microsoft.com/azure/ai-services](https://learn.microsoft.com/azure/ai-services)
* Azure AI Language documentation: [https://learn.microsoft.com/azure/ai-services/language/](https://learn.microsoft.com/azure/ai-services/language/)
* Azure Speech documentation: [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
* Azure AI Vision & Document Intelligence: [https://learn.microsoft.com/azure/ai-services/vision/](https://learn.microsoft.com/azure/ai-services/vision/)
* Azure OpenAI documentation: [https://learn.microsoft.com/azure/cognitive-services/openai/](https://learn.microsoft.com/azure/cognitive-services/openai/)

Detailed coverage of these services — including integration patterns, SDK samples, and best practices for production deployments — is available in the linked docs.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/608629a7-1574-4eb2-95a4-f026fc8888b2/lesson/4a937690-6c6b-47be-ae27-3251b9c0645e)
