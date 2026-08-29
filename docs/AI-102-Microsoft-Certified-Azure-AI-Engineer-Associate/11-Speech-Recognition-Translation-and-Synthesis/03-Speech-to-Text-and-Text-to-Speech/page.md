# Replace with your subscription key and service region
speech_key = "YourSubscriptionKey"
service_region = "YourServiceRegion"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

ssml = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" version="1.0" xml:lang="en-US">
  <voice name="en-US-JennyNeural">
    <mstts:express-as style="cheerful">
      <prosody rate="-10%" pitch="+4%">Welcome to the [AI-102: Microsoft Certified Azure AI Engineer Associate](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate) course, your gateway to building smart apps with Azure AI.</prosody>
    </mstts:express-as>

    <break time="300ms"/>

    <prosody rate="-12%">From computer vision... to chatbots... we'll cover it all.</prosody>

    <break time="400ms"/>

    <mstts:express-as style="excited">
      <prosody rate="-10%">Let's get started - and level up your AI skills.</prosody>
    </mstts:express-as>
  </voice>
</speak>"""

# Speak the SSML content
result = speech_synthesizer.speak_ssml_async(ssml).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized and played through speaker.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation.reason}")
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print(f"Error details: {cancellation.error_details}")
```

Sample run

```bash theme={null}
$ python3 app_ssml.py
Speech synthesized and played through speaker.
```

Implementation notes and best practices

* Use express-as (or provider-specific equivalents) to apply emotional or speaking styles (cheerful, excited, empathetic, etc.).
* Use prosody to fine-tune rate, pitch, and volume. Negative rate values slow speech; positive values speed it up.
* Use break to add pauses for natural pacing.
* Use phoneme tags to force correct pronunciations for technical terms and names.
* Export SSML from Speech Studio to iterate quickly in the UI, then integrate the SSML into your application code.
* Always test SSML playback on target platforms and browsers, as preview features and supported styles may vary.

> **lightbulb** Tip: When programmatically synthesizing SSML, prefer SSML-specific synthesis methods (for example, speak\_ssml\_async in the Azure Speech SDK) to ensure the markup is interpreted correctly.

Conclusion

SSML enables precise control over voice, timing, pronunciation, and emotion, helping you craft natural, expressive speech for accessibility, conversational interfaces, voice-enabled apps, and branded audio experiences. You can author SSML in code, export it from Azure Speech Studio, or use the SDKs to synthesize SSML directly in your application.

Links and references

* Azure Speech Studio: [https://speech.microsoft.com/](https://speech.microsoft.com/)
* Azure Speech SDK documentation: [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
* W3C SSML specification: [https://www.w3.org/TR/speech-synthesis/](https://www.w3.org/TR/speech-synthesis/)
* Azure Text-to-Speech voices and styles: [https://learn.microsoft.com/azure/cognitive-services/speech-service/voice-styles](https://learn.microsoft.com/azure/cognitive-services/speech-service/voice-styles)

Now that you know how to convert text to speech and enhance it with SSML, begin applying these techniques to build conversational and accessible experiences in your applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/188c2a25-9d63-45b4-b934-33ab2d412470/lesson/7da3600c-90a8-4d7d-bec5-8dd6aec70f9f)


# Speech to Text and Text to Speech

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Speech-Recognition-Translation-and-Synthesis/Speech-to-Text-and-Text-to-Speech/page

Overview of Azure Speech-to-Text and Text-to-Speech capabilities, pipelines, APIs, SDKs, result fields, and using Azure Portal and Speech Studio for testing and integration.

This article explains Azure Speech-to-Text and Text-to-Speech (TTS) capabilities, their high-level pipelines, common result fields, REST vs SDK options, and a short walkthrough of the Azure Portal and Speech Studio testing experience. It’s aimed at developers and architects integrating speech features into applications using the Azure Speech Service and Speech SDK.

## Overview: How the speech pipelines work

Both recognition (Speech-to-Text) and synthesis (Text-to-Speech) follow a similar pattern:

* Configure a SpeechConfig with your Azure region and key (or use Azure AD authentication).
* Configure an AudioConfig to specify input or output (microphone, file, or stream).
* Create the runtime object (SpeechRecognizer for recognition, SpeechSynthesizer for synthesis).
* Call the appropriate method (recognizeOnceAsync / speakTextAsync or streaming equivalents) and inspect the result object for success/failure and metadata.

This pattern is available across SDKs (.NET, Python, JavaScript) and via REST endpoints when you need direct HTTP integration or batch processing.

## High-level Speech-to-Text pipeline

To perform speech recognition you typically configure two objects:

* SpeechConfig — identifies your Azure region and subscription key (tells the service who you are and where your resources are).
* AudioConfig — specifies the input source (a microphone, an audio file, or a stream).

These feed into a SpeechRecognizer which processes the audio and, for single-shot recognition, invokes recognizeOnceAsync (or the equivalent in other SDKs) to return a recognition result.

<Frame>
  <img alt="A diagram of a Speech-to-Text pipeline. It shows SpeechConfig and AudioConfig feeding a SpeechRecognizer that calls RecognizeOnceAsync() and returns result fields like Text, Duration, OffsetInTicks, Properties, Reason, and ResultId." />
</Frame>

### Common recognition result fields

| Field                      | What it contains                                               | When to use it                           |
| -------------------------- | -------------------------------------------------------------- | ---------------------------------------- |
| Text / DisplayText         | The recognized transcript (primary output)                     | Presenting text to users, downstream NLP |
| Duration                   | Length of the recognized segment                               | Alignment, UI timestamps                 |
| OffsetInTicks / Offset     | Start timestamp for the segment in audio                       | Word/segment alignment                   |
| Properties / NBest         | Metadata, confidence scores, alternative hypotheses            | Confidence-based UI decisions            |
| Reason / RecognitionStatus | High-level outcome (e.g., RecognizedSpeech, NoMatch, Canceled) | Verify success before consuming Text     |
| ResultId / Id              | Unique identifier for the recognition result                   | Logging, tracing, debugging              |

Note: Always check the result Reason before consuming Text. The common result reasons are:

* RecognizedSpeech — recognition succeeded and Text is valid.
* NoMatch — the audio did not contain recognizable speech (e.g., noise or silence).
* Canceled — recognition was interrupted (often due to authentication, quota, or network issues). If canceled, inspect the cancellation details to diagnose the issue.

> **lightbulb** Always validate Result.Reason (and CancellationDetails when available) before using recognized text. Use Confidence or NBest alternatives to improve UX for low-confidence transcripts.

## REST APIs for Speech-to-Text

Azure Speech provides two common REST options for recognition:

* Standard Speech Service API — supports real-time/streaming and batch scenarios for most production needs.
* Short Audio API — optimized for short audio clips (roughly up to 60 seconds), useful for commands and brief interactions.

Choose based on latency, expected audio length, and whether you need streaming JSON or batch results.

<Frame>
  <img alt="A presentation slide titled &#x22;Speech-to-Text&#x22; showing three connected blocks. The left describes a Standard Speech-to-Text API (converts live or recorded speech into text), the center highlights REST APIs for Speech-to-Text, and the right describes a Short Audio API optimized for clips up to 60 seconds." />
</Frame>

## SDK support for Speech-to-Text

The Speech SDKs (.NET, Python, JavaScript) abstract the REST details and provide:

* Synchronous and asynchronous methods for single-shot recognition.
* Event-driven streaming recognition with word-level timestamps.
* Helpers to manage audio devices and format conversions.

Use SDKs to reduce boilerplate and handle streaming scenarios more easily; use REST for custom cloud workflows, serverless functions, or where SDKs aren’t available.

## Text-to-Speech pipeline

Text-to-Speech follows a similar configuration pattern:

* SpeechConfig — your resource location and key.
* AudioConfig — determines the output destination (speaker device, audio file, or stream).

The SpeechSynthesizer performs the conversion. When you call speakTextAsync (or its SDK equivalent), the synthesizer returns a result with:

* AudioData — generated audio bytes or a saved file.
* Properties — metadata about the output.
* Reason — indicates success (SynthesizingAudioCompleted) or failure (Canceled).
* ResultId — unique identifier for the synthesis operation.

<Frame>
  <img alt="A Text-to-Speech flow diagram showing SpeechConfig and AudioConfig feeding a SpeechSynthesizer that invokes SpeakTextAsync(). The synthesizer returns results (AudioData, Properties, Reason, ResultId) with short descriptions of each." />
</Frame>

When synthesis fails, retrieve cancellation details to determine the cause — common causes include missing configuration, authentication failure, or network problems.

<Frame>
  <img alt="A Text-to-Speech flow diagram showing SpeechConfig and AudioConfig feeding into a SpeechSynthesizer. Calling SpeakTextAsync() yields outcomes like SynthesizingAudioCompleted or Cancelled (check CancellationDetails)." />
</Frame>

## Text-to-Speech REST APIs

Two primary REST options for TTS:

* Standard Text-to-Speech API — real-time conversion for short text inputs (chatbots, IVRs, accessibility).
* Batch Synthesis API — generate large volumes of audio for content creation, e-learning, or datasets.

Both can be integrated into server-side pipelines or batch jobs.

<Frame>
  <img alt="A slide titled &#x22;Text-to-Speech&#x22; showing a central &#x22;REST APIs for Text-to-Speech&#x22; node linking two boxes: &#x22;Standard Text-to-Speech API&#x22; (for converting text into natural-sounding, real-time speech) and &#x22;Batch Synthesis API&#x22; (optimized for generating large volumes of speech audio from text)." />
</Frame>

SDK support for TTS mirrors recognition: .NET, Python, and JavaScript SDKs provide convenient APIs to generate audio without writing raw REST calls.

<Frame>
  <img alt="A slide titled &#x22;Text-to-Speech&#x22; showing SDK support with .NET, Python, and JavaScript logos. It also notes &#x22;Allows easy integration into applications.&#x22;" />
</Frame>

## Quick Azure Portal / Speech Studio walkthrough

Create or reuse a Speech resource in the Azure Portal (under AI Services). The resource page displays endpoints and keys you can use for REST or SDK authentication. Example endpoints:

```text theme={null}
Speech to Text (Standard) https://eastus.stt.speech.microsoft.com
Text to Speech (Neural) https://eastus.tts.speech.microsoft.com
Custom Voice https://aiservicesai900.cognitiveservices.azure.com/
```

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Azure AI services&#x22; dashboard, with the left navigation listing various AI services and one AI service resource (&#x22;aiservicesai900&#x22;) displayed in the main pane. The top bar includes search and user account controls." />
</Frame>

Speech Studio gives you sample experiences (captioning, post-call transcription, live chat avatar, language learning). Key features:

* Microphone-based real-time testing.
* Upload audio files to transcribe and inspect JSON output with segment and word-level timestamps.
* Preview voice styles and languages for TTS.

<Frame>
  <img alt="A screenshot of the Azure Speech Studio web interface titled &#x22;Get started with Speech,&#x22; showing a notice about no recent projects and a list of speech capability tiles. The tiles include examples like captioning (speech-to-text), post-call transcription and analytics, live chat avatar, and language learning." />
</Frame>

### Real-time Speech-to-Text demo (Speech Studio)

In Speech Studio’s real-time demo you select a resource, grant microphone permissions, and speak. The service returns streaming JSON with segments and word-level timestamps (offset and duration). Example excerpt (formatted):

<Frame>
  <img alt="A screenshot of Microsoft Azure Speech Studio's real-time speech-to-text interface. It shows options to choose language and upload or record audio on the left, and a test results pane on the right with a transcribed JSON output and an uploaded .wav file." />
</Frame>

```json theme={null}
[
  {
    "Id": "ab6b091b9573453f9fa8ec6292625fbd",
    "RecognitionStatus": 0,
    "Offset": 23200000,
    "Duration": 182000000,
    "Channel": 0,
    "DisplayText": "Conversational Language Understanding is one of the custom features offered by Azure AI Language Services.",
    "NBest": [
      {
        "Confidence": 0.8921081,
        "Lexical": "conversational language understanding is one of the custom features offered by azure ai language services",
        "ITN": "conversational language understanding is one of the custom features offered by azure ai language services",
        "Display": "Conversational Language Understanding is one of the custom features offered by Azure AI Language Services.",
        "Words": [
          {
            "Word": "conversational",
            "Offset": 23200000,
            "Duration": 1820000
          },
          {
            "Word": "language",
            "Offset": 25020000,
            "Duration": 1600000
          },
          {
            "Word": "understanding",
            "Offset": 26640000,
            "Duration": 2200000
          }
        ]
      }
    ]
  }
]
```

You can also download the audio file used for transcription directly from the Speech Studio UI.

## Voice Gallery and Text-to-Speech demo

Speech Studio includes a Voice Gallery to preview built-in voices, switch speaking styles, and test languages. Selecting a voice (for example, "Andrew") plays sample phrases and shows personality and style controls.

Important: changing the voice locale does not translate the input text — it simply uses that voice’s phonetics/locale. For translation, first translate the text (using a translation API) and then synthesize the translated text with an appropriate voice.

<Frame>
  <img alt="A screenshot of a &#x22;Voice Gallery&#x22; web interface showing a voice catalog with search, language and sort controls and multiple voice cards. A right-hand panel displays details for a selected voice (Andrew Multilingual) including personality tags and speaking styles." />
</Frame>

Azure also supports custom/personal voices — you can train a voice on human samples (subject to consent and service constraints) and synthesize audio that resembles the target voice. This is commonly used by content creators to produce large volumes of voice content.

## SDKs, integration notes, and best practices

* SDK availability: Python, .NET, and JavaScript SDKs support both recognition and synthesis.
* REST APIs: use when you need serverless/batch flows or to integrate from environments without the SDKs.
* Error handling: always check Result.Reason (or RecognitionStatus) and CancellationDetails. Implement retries for transient failures.
* Region selection: use the correct regional endpoint and monitor quota limits for production workloads.
* Security: prefer Azure AD tokens for long-lived deployments; manage keys and rotate credentials as needed.

> **lightbulb** For production, ensure correct regional endpoints, robust authentication (Azure AD or subscription keys), and implement Result.Reason / CancellationDetails checks with retries for transient network or quota errors.

## Useful links and references

* Azure Speech Service documentation: [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
* Speech SDK quickstarts: [https://learn.microsoft.com/azure/cognitive-services/speech-service/quickstarts](https://learn.microsoft.com/azure/cognitive-services/speech-service/quickstarts)
* Speech Studio: [https://speech.microsoft.com/](https://speech.microsoft.com/)

This concludes the overview of Speech-to-Text and Text-to-Speech workflows, result structures, REST vs SDK options, and how to test them using the Azure Portal and Speech Studio.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/188c2a25-9d63-45b4-b934-33ab2d412470/lesson/bb0c2211-d20c-499a-9ef4-0722557fd76c)
