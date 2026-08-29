# Replace these with your Azure Speech resource key and region
speech_key = "YOUR_SPEECH_KEY"
service_region = "eastus"

if not speech_key:
    raise ValueError("You must set your Azure Speech key.")

# Create speech configuration and set voice & output format
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # neural voice
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
)

# 1) Speak to default speaker
print("Speaking text using default speaker...")
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
text = "Hello! This is a sample neural voice using Azure Speech Service."

result = synthesizer.speak_text_async(text).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized successfully to speaker.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("Speech synthesis canceled:", cancellation.reason)
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error details:", cancellation.error_details)

# 2) Save same synthesized audio to file
output_filename = "output_audio.wav"
print(f"Saving audio to '{output_filename}'...")
audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)
file_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

file_result = file_synthesizer.speak_text_async(text).get()
if file_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Audio saved to '{output_filename}'")
elif file_result.reason == speechsdk.ResultReason.Canceled:
    cancellation = file_result.cancellation_details
    print("Speech synthesis canceled:", cancellation.reason)
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error details:", cancellation.error_details)
```

Sample console output (illustrative)

```text theme={null}
Speaking text using default speaker...
Speech synthesized successfully to speaker.
Saving audio to 'output_audio.wav'...
Audio saved to 'output_audio.wav'
```

STT: recognize speech from an audio file

```python theme={null}
import azure.cognitiveservices.speech as speechsdk

# Reuse or recreate speech_config as needed.
audio_input = speechsdk.audio.AudioConfig(filename="output_audio.wav")
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

print("Recognizing speech from audio file...")
result = speech_recognizer.recognize_once_async().get()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized Text:")
    print(result.text)
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("Speech recognition canceled:", cancellation.reason)
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error details:", cancellation.error_details)
```

Typical recognition output (illustrative)

```text theme={null}
Recognizing speech from audio file...
Recognized Text:
Hello! This is a sample neural voice using Azure Speech Service.
```

## Best practices and tips

* For pipelines that include post-processing (noise reduction, alignment, ASR training), prefer uncompressed WAV (16-bit PCM) at 16 kHz or 24 kHz.
* For streaming and mobile delivery, prefer MP3 or Opus (OGG) to reduce bandwidth.
* Test voice choices with representative text. Neural voices may need different SSML or prosody tuning to get the desired intonation.
* Monitor quotas and region availability for neural voices; consider fallback to standard voices if unavailable.

## Summary

* Select file type, sample rate, and bit depth based on your target use (streaming vs. storage vs. processing).
* Use neural voices when you require natural, expressive TTS for UX-heavy applications.
* Configure output format and voice via SpeechConfig in the Azure Speech SDK; you can synthesize to the speaker, save to a file, and use that audio for Speech-to-Text.

Links and references

* [Azure Speech Services Overview](https://learn.microsoft.com/azure/cognitive-services/speech-service/overview)
* [Speech SDK Documentation](https://learn.microsoft.com/azure/cognitive-services/speech-service/speech-sdk)
* [Speech-to-Text (STT) Documentation](https://learn.microsoft.com/azure/cognitive-services/speech-service/speech-to-text)
* [Speech Pricing and Quotas](https://learn.microsoft.com/azure/cognitive-services/speech-service/quotas)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/188c2a25-9d63-45b4-b934-33ab2d412470/lesson/91bacd3d-054b-47f4-8797-9b6fe5f18876)


# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Speech-Recognition-Translation-and-Synthesis/Module-Introduction/page

Overview of speech recognition, translation, and synthesis, teaching setup, SSML customization, and practical integration for building voice enabled multilingual and accessible applications.

Welcome to the Speech Recognition, Translation, and Synthesis module. In this lesson you'll learn how machines listen to spoken language, convert it to text (speech-to-text), translate that text between languages, and generate natural-sounding voice from text (text-to-speech). These building blocks power voice assistants, real-time translation tools, accessibility features, and conversational AI services.

This module focuses on practical setup and integration of Speech Services, techniques for accurate speech recognition, and approaches to customize synthetic voices using Speech Synthesis Markup Language (SSML). You’ll get hands-on knowledge useful for building voice-enabled apps, multilingual experiences, and accessible interfaces.

Learning objectives

By the end of this module you will be able to:

1. Provision and configure the Speech Service required for recognition and synthesis.
2. Implement speech recognition pipelines to reliably convert spoken language to text.
3. Enable speech synthesis to convert text back into natural-sounding audio.
4. Customize audio output by selecting voice, adjusting style, pitch, and speaking rate.
5. Use Speech Synthesis Markup Language (SSML) to fine-tune prosody, pronunciation, and audio effects.

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; showing five numbered items about speech technology: setting up a speech service, implementing speech recognition, enabling speech synthesis, customizing audio output, and leveraging Speech Synthesis Markup Language (SSML)." />
</Frame>

> **lightbulb** Before you begin: make sure you have access to a Speech Service (or equivalent provider), an API key and endpoint, and sample audio or a microphone for testing. Familiarity with basic REST or SDK usage in your preferred language (Python, C#, or JavaScript) will help you follow the hands-on examples in later lessons.

Core capabilities overview

|                  Capability | Primary use cases                                              | Quick reference                                                                                                              |
| --------------------------: | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
|    Speech Recognition (STT) | Voice commands, meeting transcriptions, accessibility captions | [Speech-to-Text docs](https://learn.microsoft.com/azure/cognitive-services/speech-service/overview)                          |
| Translation (Text & Speech) | Real-time multilingual chat, interpreter apps                  | [Speech Translation docs](https://learn.microsoft.com/azure/cognitive-services/speech-service/how-to-use-speech-translation) |
|      Speech Synthesis (TTS) | Voice assistants, narrated content, accessibility              | [Text-to-Speech docs](https://learn.microsoft.com/azure/cognitive-services/speech-service/overview-text-to-speech)           |
|                        SSML | Control prosody, pronunciation, and audio events in TTS        | [SSML reference](https://learn.microsoft.com/azure/cognitive-services/speech-service/speech-synthesis-markup)                |

Recommended next steps

* Review the Speech Service quickstarts for your language of choice.
* Gather sample audio (or prepare a microphone) and target languages for translation tests.
* Skim the SSML reference to understand tags for voice, rate, pitch, and breaks.

References

* [Azure Speech Service documentation](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
* [SSML for Speech Synthesis](https://learn.microsoft.com/azure/cognitive-services/speech-service/speech-synthesis-markup)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/188c2a25-9d63-45b4-b934-33ab2d412470/lesson/a70a4577-f2be-4808-aa40-899e95032a3a)
