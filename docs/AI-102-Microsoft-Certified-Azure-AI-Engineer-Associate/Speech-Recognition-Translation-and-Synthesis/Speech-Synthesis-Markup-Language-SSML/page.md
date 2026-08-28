# Speech Synthesis Markup Language SSML

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Speech-Recognition-Translation-and-Synthesis/Speech-Synthesis-Markup-Language-SSML/page

Explains SSML, an XML markup for controlling text-to-speech voice, prosody, pronunciation, pauses, expressive styles, and using Azure Speech Studio and SDKs to author and synthesize speech.

SSML (Speech Synthesis Markup Language) is an XML-based markup that gives developers precise control over how text is converted to speech. With SSML you can shape tone, pacing, pronunciation, and other delivery aspects so synthesized audio sounds more natural and expressive.

<Frame>
  <img alt="A presentation slide titled &#x22;Speech Synthesis Markup Language (SSML)&#x22; with an icon of a document being converted into a speech bubble. The caption explains SSML is a markup language for fine‑tuned customization of how text is converted to speech." />
</Frame>

Core SSML capabilities

* Speaking styles — set the voice's tone or emotion (for example: cheerful, excited, empathetic).
* Pauses and silence — insert breaks or delays to control pacing and rhythm.
* Phonemes — define custom pronunciations for technical terms, names, or nonstandard words.

<Frame>
  <img alt="An infographic slide titled &#x22;Speech Synthesis Markup Language (SSML)&#x22; showing three panels: 01 Speaking Styles (modify tone and emotion), 02 Pauses and Silence (control timing and pacing), and 03 Phonemes (define custom pronunciations). Each panel includes a simple icon and brief explanatory text." />
</Frame>

Additional expressive features

* Prosody adjustments — change pitch, rate, and volume to create a more dynamic delivery.
* Say-as formatting — control how numbers, dates, times, phone numbers, and other tokens are spoken (for example, as a year, ordinal, or telephone number).
* Embedded audio — insert pre-recorded audio or background music for branding or effects.

<Frame>
  <img alt="A presentation slide titled &#x22;Speech Synthesis Markup Language (SSML)&#x22; showing three numbered feature cards: Prosody Adjustments, &#x22;Say-as&#x22; Formatting, and Embedded Audio with short descriptions. Each card lists what the feature does (modify pitch/rate/volume; specify how numbers/dates/times are spoken; insert background or recorded audio)." />
</Frame>

Common SSML tags and when to use them

| Tag              | Purpose                                 | Example use                                                   |
| ---------------- | --------------------------------------- | ------------------------------------------------------------- |
| speak            | Root element for SSML                   | Wrap all SSML content in `<speak>`                            |
| voice            | Select a voice or locale                | `<voice name="en-US-JennyNeural">`                            |
| prosody          | Adjust rate, pitch, volume              | `<prosody rate="-10%" pitch="+4%">`                           |
| break            | Insert pauses                           | `<break time="300ms"/>`                                       |
| phoneme          | Force pronunciation                     | `<phoneme alphabet="ipa" ph="ælɡəˌrɪðəm">algorithm</phoneme>` |
| say-as           | Control formatting of numbers/dates     | `<say-as interpret-as="date">2026-03-17</say-as>`             |
| mstts:express-as | Apply provider-specific speaking styles | `<mstts:express-as style="cheerful">`                         |

Example SSML — C# string literal

This C# example shows two voices with different behaviors, using expressive styles, phonemes, and a pause:

```csharp theme={null}
string ssmlString = @"
<speak xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' version='1.0' xml:lang='en-US'>
    <voice name='en-US-JaneNeural'>
        <mstts:express-as style='empathetic'>I love programming!</mstts:express-as>
    </voice>
    <voice name='en-US-MarkNeural'>
        I pronounce <phoneme alphabet='ipa' ph='ælɡəˌrɪðəm'>algorithm</phoneme> differently.
        <break time='500ms'/> Let's continue!
    </voice>
</speak>";
```

This snippet demonstrates:

* mstts:express-as — apply emotional/speaking styles (provider-specific).
* phoneme — use IPA to precise pronunciation.
* break — insert a pause for natural pacing.

Authoring and previewing SSML in Speech Studio

You can author and preview SSML directly in the browser with Azure Speech Studio. The UI helps configure voice selection, pronunciation rules, rate, pitch, and volume, then lets you export the resulting SSML for programmatic use.

<Frame>
  <img alt="A screenshot of the Azure AI Speech Studio web page showing feature tiles for speech-to-text and related services (Real-time speech-to-text, Whisper Model, Batch speech-to-text, Custom Speech, Pronunciation Assessment, and Speech Translation). The page includes a top navigation bar and a user profile icon in the upper right." />
</Frame>

<Callout icon="warning">
  Speech Studio’s real-time preview functionality is supported in Edge and Chrome. If you use other browsers (for example, Opera), some preview features may not work as expected.
</Callout>

When you export SSML from Speech Studio you may see metadata comments followed by the SSML itself. Example exported SSML with metadata:

```xml theme={null}
<!--ID=B7267351-473F-409D-9765-754A8EBCDDE05;Version=1|{"VoiceNameToldMapItems":[{"Id":"6c640df5-9977-4a98-b785-6b2f195db0e3c","Name":"Microsoft Server Speech Text to Speech Voice (de-DE, SeraphinaMultilingualNeural)","ShortName":"de-DE-SeraphinaMultilingualNeural","Locale":"de-DE","VoiceType":"StandardVoice"}]}-->
<!--ID=FCB40C2B-1F9F-4C26-B1A1-CF8E67B0E7D1;Version=1|{"Files":[]}-->
<!--ID=5B95B1CC-2C7B-494F-B746-CF22A0E779B7;Version=1|{"Locales":{"de-DE":{"AutoApplyCustomLexiconFiles":[]}}}-->
<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="de-DE">
  <voice name="de-DE-SeraphinaMultilingualNeural"> </voice>
</speak>
```

SSML from code — Python example using the Azure Speech SDK

When synthesizing SSML programmatically with the Azure Speech SDK, call the SSML-specific method (for example, speak\_ssml\_async) instead of plain-text APIs. The Python example below demonstrates creating a SpeechSynthesizer and synthesizing expressive SSML:

```python theme={null}
import azure.cognitiveservices.speech as speechsdk
