# Speech Service

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Speech-Recognition-Translation-and-Synthesis/Speech-Service/page

Overview of Azure AI Speech services, including speech to text, text to speech, translation, speaker recognition, intent extraction, SDK and REST usage, examples, and best practices.

Azure AI Speech provides cloud APIs and SDKs for building voice-enabled applications that can listen, understand, and speak. With these services you can add capabilities such as real-time transcription, natural-sounding speech synthesis, multilingual translation, speaker verification, and intent extraction. Typical scenarios include voice-enabled chatbots, call-center assistants that transcribe and synthesize replies, real-time translators for conferencing, and biometric voice verification for authentication.

Below is a concise breakdown of the primary capabilities that enable these scenarios.

* Speech-to-Text (STT)
  * Converts spoken audio into written text.
  * Common uses: transcriptions, live captions, voice commands, and conversational logging.
  * Supports real-time streaming and batch transcription modes.

* Text-to-Speech (TTS)
  * Synthesizes natural-sounding audio from text.
  * Supports customizable voices, speaking styles, and SSML for fine-grained control.
  * Useful for accessibility, IVR systems, and spoken responses in assistants.

* Speech Translation
  * Performs real-time translation of spoken language into another language (text or synthesized audio).
  * Ideal for multilingual conversations in travel, customer support, and meetings.

* Speaker Recognition
  * Identifies or verifies an individual by their voice (speaker identification and verification).
  * Used in biometric authentication, user personalization, and audit trails.

* Intent Recognition
  * Extracts user intent and entities from spoken input.
  * Often combined with language understanding models such as Conversational Language Understanding (CLU) or LUIS to power voice assistants and conversational agents.

|          Capability | Primary Use Cases                       | Quick Link                                                                                                                                                                                                                                   |
| ------------------: | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|      Speech-to-Text | Transcription, captions, voice commands | [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)                                                                                                 |
|      Text-to-Speech | Spoken responses, accessibility, IVR    | [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)                                                                                                 |
|  Speech Translation | Real-time multilingual conversations    | [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)                                                                                                 |
| Speaker Recognition | Biometric verification, personalization | [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)                                                                                                 |
|  Intent Recognition | Voice-driven conversational agents      | [https://learn.microsoft.com/azure/cognitive-services/language-service/conversational-language-understanding/overview](https://learn.microsoft.com/azure/cognitive-services/language-service/conversational-language-understanding/overview) |

Azure Speech is exposed via:

* Speech SDKs for platforms such as Windows, macOS, Linux, iOS, Android, and JavaScript (recommended for low-latency, real-time streaming).
* REST APIs for batch processing, server-side integration, or when SDKs are not available.

> **lightbulb** Use the Speech SDK for low-latency, real-time scenarios (streaming recognition and synthesis). For batch transcription, file-based workflows, or simple server-side integrations, the REST APIs are often the most convenient choice.

## Getting started (high level)

1. Create a Speech resource in the Azure portal or obtain an endpoint and API key from an existing Cognitive Services or Speech resource.
2. Choose SDK vs REST based on your scenario: SDK for streaming, REST for batch or server-to-server.
3. Implement authentication (shared key or Azure AD) and configure region/endpoint.
4. Start with a small integration (transcribe a test audio file or synthesize “Hello world”) and iterate to add custom voices, intent models, or translation.

## Minimal examples

JavaScript (Speech SDK) — Real-time recognition

```javascript theme={null}
import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk";

const speechConfig = SpeechSDK.SpeechConfig.fromSubscription("<YOUR_KEY>", "<YOUR_REGION>");
const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
const recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);

recognizer.recognizeOnceAsync(result => {
  console.log("Recognized text:", result.text);
  recognizer.close();
});
```

REST (Batch transcription) — POST audio file (pseudo-request)

```http theme={null}
POST https://<your-region>.api.cognitive.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US
Ocp-Apim-Subscription-Key: <YOUR_KEY>
Content-Type: audio/wav

[binary audio body]
```

TTS (REST) — Synthesize a short phrase using SSML

```http theme={null}
POST https://<region>.tts.speech.microsoft.com/cognitiveservices/v1
Ocp-Apim-Subscription-Key: <YOUR_KEY>
Content-Type: application/ssml+xml
X-Microsoft-OutputFormat: audio-16khz-32kbitrate-mono-mp3

<speak version="1.0" xml:lang="en-US">
  <voice name="en-US-JennyNeural">Hello, this is Azure Text-to-Speech.</voice>
</speak>
```

## Best practices

* For real-time interactive apps (voice assistants, live captions), prefer the Speech SDK to minimize latency and benefit from built-in audio management.
* Use SSML to control prosody, pronunciation, and voice selection for higher-quality synthesized speech.
* For sensitive use cases (authentication, verification), use secure key management and consider Azure AD authentication and role-based access.
* Evaluate model costs and latency trade-offs when choosing between streaming and batch transcription.

## Links and references

* Speech SDK: [https://learn.microsoft.com/azure/cognitive-services/speech-service/speech-sdk](https://learn.microsoft.com/azure/cognitive-services/speech-service/speech-sdk)
* Speech REST APIs: [https://learn.microsoft.com/azure/cognitive-services/speech-service/rest-apis](https://learn.microsoft.com/azure/cognitive-services/speech-service/rest-apis)
* Conversational Language Understanding (CLU): [https://learn.microsoft.com/azure/cognitive-services/language-service/conversational-language-understanding/overview](https://learn.microsoft.com/azure/cognitive-services/language-service/conversational-language-understanding/overview)
* LUIS overview: [https://learn.microsoft.com/azure/cognitive-services/luis/overview](https://learn.microsoft.com/azure/cognitive-services/luis/overview)

This article provided an overview of Azure AI Speech capabilities, practical guidance for choosing SDK vs REST, minimal examples for common tasks, and best practices to help you integrate speech into your applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/188c2a25-9d63-45b4-b934-33ab2d412470/lesson/2f291ad1-d013-4384-be71-eeba8204ad8b)
