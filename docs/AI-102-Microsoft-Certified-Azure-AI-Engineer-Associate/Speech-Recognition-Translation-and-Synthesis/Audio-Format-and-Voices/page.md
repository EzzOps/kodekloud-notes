# Audio Format and Voices

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Speech-Recognition-Translation-and-Synthesis/Audio-Format-and-Voices/page

Guidance on choosing audio formats, sample rates, and voice types and configuring Azure Speech SDK for neural and standard text to speech with code examples

In this lesson we'll cover how audio output settings affect speech synthesis quality and efficiency, and how to choose and configure voices in [Azure Speech Services](https://learn.microsoft.com/azure/cognitive-services/speech-service/overview). Topics include audio file types, sample rates, bit depth, and the difference between standard and neural TTS voices — plus concise code examples (C# and Python) showing how to set output formats and voice names with the Azure Speech SDK.

## Audio formats: file type, sample rate, and bit depth

Azure Speech Services supports common audio containers and codecs (WAV, MP3, OGG, and others). Choosing the right format depends on whether you will stream audio, store it for download, or post-process it.

* File type: Pick a container/codec for compatibility and filesize. WAV/PCM is uncompressed and ideal for high-quality processing; MP3 and OGG are compressed and save bandwidth/storage.
* Sample rate: Defines how many samples per second are captured. Higher rates (e.g., 24 kHz) improve clarity for wideband content but increase file size. 16 kHz is a common compromise for speech.
* Bit depth: The number of bits per sample (e.g., 16-bit). Higher bit depth increases fidelity and file size. For speech, 16-bit PCM is typical.

<Frame>
  <img alt="A presentation slide titled &#x22;Audio Format and Voices&#x22; with a waveform icon and the heading &#x22;Audio Format&#x22; on the left. On the right are three colored boxes describing File Type, Sample Rate, and Bit Depth with short explanations." />
</Frame>

<Callout icon="lightbulb">
  Choose audio format and sample rate to match your downstream needs: use higher sample rates and uncompressed formats for post-processing or human listeners, and compressed formats for streaming, mobile, or bandwidth-constrained scenarios.
</Callout>

Audio format quick reference

| File type  | Use case                                        | Pros                         | Cons                        |
| ---------- | ----------------------------------------------- | ---------------------------- | --------------------------- |
| WAV (PCM)  | Post-processing, archival, audio analysis       | Lossless, high fidelity      | Large filesize              |
| MP3        | Streaming, downloads where smaller size matters | Smaller filesize, ubiquitous | Lossy compression artifacts |
| OGG (Opus) | Low-latency streaming, web apps                 | Efficient at low bitrates    | Less universal than MP3     |
| Raw PCM    | DSP and research workflows                      | Simple and predictable       | No container metadata       |

Sample rates and recommended uses

| Sample rate      | Best for                                     |
| ---------------- | -------------------------------------------- |
| 8 kHz            | Narrowband telephony                         |
| 16 kHz           | Typical speech (voicemail, simple TTS)       |
| 24 kHz and above | High-fidelity voice apps, music/voice mixing |

## Voice options: Standard vs Neural

Azure Speech Services provides two primary types of text-to-speech voices:

* Standard voices: Pre-built synthetic voices suitable for basic announcements and simple automation. Often faster and lower-cost but may sound slightly robotic.
* Neural voices: Deep learning–based voices that deliver more natural prosody and expressiveness. Ideal for virtual assistants, audiobooks, and UX-focused experiences.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Audio Format and Voices&#x22; showing two panels describing voice options. The left panel explains &#x22;Standard Voices&#x22; (pre-recorded synthetic voices) and the right panel explains &#x22;Neural Voices&#x22; (AI-powered, more natural-sounding voices using deep learning)." />
</Frame>

Neural voices typically deliver higher naturalness and expressiveness, but review quotas, regional availability, and pricing before production rollout.

<Callout icon="warning">
  Neural voices may have regional availability, quota limits, and different pricing tiers. Verify your subscription limits and regional support in the Azure portal and the Speech Services pricing and quotas documentation.
</Callout>

## Configuring output format and voice in code

Below are concise examples showing how to set output formats and voice names in the Azure Speech SDK. Each example demonstrates setting a neural voice and a common RIFF (WAV) output format.

C# (set RIFF 16 kHz 16-bit mono PCM and a neural voice)

```csharp theme={null}
// Configure Speech SDK (C#)
speechConfig.SetSpeechSynthesisOutputFormat(SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm);
speechConfig.SpeechSynthesisVoiceName = "en-US-JennyNeural";
```

Python examples (Azure Speech SDK)

* What the examples show:
  1. Create a SpeechConfig and set voice and output format.
  2. Synthesize to the default speaker.
  3. Save synthesized audio to a WAV file.
  4. Use that saved file for Speech-to-Text (STT) recognition.

TTS: synthesize to speaker and save to a file

```python theme={null}
import azure.cognitiveservices.speech as speechsdk
