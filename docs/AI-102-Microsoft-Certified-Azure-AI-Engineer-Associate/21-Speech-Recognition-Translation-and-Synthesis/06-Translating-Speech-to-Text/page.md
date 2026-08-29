# Translating Speech to Text

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Speech-Recognition-Translation-and-Synthesis/Translating-Speech-to-Text/page

Guide to using Azure Speech Service to transcribe spoken audio, translate into multiple languages, and optionally synthesize translated text, with pipeline explanation and Python examples.

Translating speech to text with Azure Speech Service lets you transcribe spoken audio and produce real-time translations into one or more target languages. This guide explains the end-to-end translation pipeline, how results are structured, and sample code to get you started.

## How the translation pipeline works

The typical flow for speech translation is:

1. Configure the Speech Translation Config: set your service region, subscription key, the spoken (recognition) language (for example, `en-US`), and one or more target languages (for example, `es`, `fr`).
2. Define the Audio Config: specify the audio input source — microphone, audio file, or a custom stream.
3. Create the Translation Recognizer: combine the translation configuration and audio input in a `TranslationRecognizer`. This component performs speech recognition and forwards the transcribed text to the translation model.
4. Invoke recognition: call `recognize_once_async()` (or use streaming/event-based handlers) to perform recognition and receive translated output.

Below is a diagram showing the flow from configuration to a translated result.

<Frame>
  <img alt="A diagram of a speech-to-text translation workflow where SpeechTranslationConfig and AudioConfig feed into a TranslationRecognizer, which invokes RecognizeOnceAsync(). The translation process returns structured results such as Text, Translations, Duration, OffsetInTicks, Properties, Reason, and ResultId." />
</Frame>

## Recognition result structure

When a translation operation completes, the recognizer returns a structured result. Key attributes help you interpret, log, and debug outputs.

| Attribute       | Description                                                                   | Example                          |
| --------------- | ----------------------------------------------------------------------------- | -------------------------------- |
| `text`          | Original recognized transcription (source language)                           | `Hello, how are you?`            |
| `translations`  | Mapping of target language codes to translated text                           | `{ "es": "Hola, ¿cómo estás?" }` |
| `duration`      | Length of the recognized audio segment                                        | `00:00:02.500`                   |
| `offsetInTicks` | Timestamp (ticks) when recognition started                                    | `637...`                         |
| `properties`    | Metadata and diagnostic properties                                            | e.g., engine or model info       |
| `reason`        | Why the result was returned (e.g., `TranslatedSpeech`, `NoMatch`, `Canceled`) | `TranslatedSpeech`               |
| `resultId`      | Unique identifier for the recognition result                                  | `3a9f...`                        |

Most importantly, `translations` contains a translated string for each target language you configured. The recognition → translation two-step pipeline lets you obtain both the original transcript and multilingual outputs for downstream workflows (display, storage, or synthesis).

## Benefits of Azure Speech translation

* Multi-language support: real-time recognition and translation across many languages.
* Customizable: adjust recognition or translation settings for domain-specific vocabularies.
* Real-time processing: low-latency translations for interactive scenarios (meetings, support).
* Flexible output: get original transcription and translations (text and optional synthesized audio).

<Frame>
  <img alt="A presentation slide titled &#x22;Translating Speech to Text&#x22; showing four feature cards. The cards list Multi-Language Support, Customizable, Real-Time Processing, and Flexible Output with matching icons and short descriptions." />
</Frame>

## Example JSON response

A typical JSON-like structure returned by translation workflows:

```json theme={null}
{
  "sourceLanguage": "en-US",
  "targetLanguages": ["es", "fr", "de"],
  "recognitionResults": {
    "transcription": "Hello, how are you?",
    "translations": {
      "es": "Hola, ¿cómo estás?",
      "fr": "Bonjour, comment ça va?",
      "de": "Hallo, wie geht es dir?"
    }
  }
}
```

This structure is straightforward to parse and integrate into multilingual applications or downstream systems (subtitles, chat, notification messages, etc.).

## Working in Speech Studio (Azure Portal)

Use Speech Studio at [https://speech.microsoft.com/](https://speech.microsoft.com/) to quickly try speech translation and video translation scenarios without writing code. In Speech Studio you can:

* Select the spoken language (e.g., English (United States)).
* Pick one or more target languages (e.g., French).
* Choose the voice for synthesized translated audio (e.g., `Dennis`).
* Record or upload audio, view the transcription, and listen to or download translated audio.

Speech Studio follows the same pipeline: Speech-to-Text → Translation → Text-to-Speech (if synthesis is requested).

## Calling the Translation service from code (Python)

Install the Speech SDK:

```bash theme={null}
pip install azure-cognitiveservices-speech
```

<Callout icon="lightbulb">
  Ensure your Speech resource key and region are set correctly. For safety, store them as environment variables rather than embedding secrets in code.
</Callout>

Below is a concise Python example that:

1. Configures the translation recognizer,
2. Recognizes and translates speech from a WAV file to Spanish, and
3. Synthesizes the translated Spanish text to the default audio output.

```python theme={null}
import azure.cognitiveservices.speech as speechsdk
