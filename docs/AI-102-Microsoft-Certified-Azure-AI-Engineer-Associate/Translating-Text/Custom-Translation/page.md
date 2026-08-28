# Replace with your subscription info and audio file path
speech_key = "YOUR_SPEECH_KEY"
service_region = "YOUR_SERVICE_REGION"
audio_file = "path/to/your/audio.wav"

# Configure translation
translation_config = speechsdk.SpeechTranslationConfig(
    subscription=speech_key,
    region=service_region
)
translation_config.speech_recognition_language = "en-US"
translation_config.add_target_language("es")  # Spanish

# Audio config for input WAV file
audio_input = speechsdk.audio.AudioConfig(filename=audio_file)

# Create the translation recognizer
translator = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config,
    audio_config=audio_input
)

print("Translating speech from file...")
result = translator.recognize_once_async().get()

if result.reason == speechsdk.ResultReason.TranslatedSpeech:
    translated_text_es = result.translations.get("es", "")
    print("Recognized (EN):", result.text)
    print("Translated (ES):", translated_text_es)
else:
    print("Recognition/Translation failed. Reason:", result.reason)

# Synthesize the Spanish translation to the default speaker
if translated_text_es:
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    synthesis_result = synthesizer.speak_text_async(translated_text_es).get()
    if synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Synthesized translated speech to speaker successfully.")
    else:
        print("Speech synthesis failed. Reason:", synthesis_result.reason)
```

This example demonstrates the manual pipeline: Speech-to-Text → Translation → Text-to-Speech.

## Event-based vs Manual speech synthesis

Choose the synthesis approach that matches your scenario:

* Event-based speech synthesis:
  * Translates and synthesizes in a streaming fashion.
  * Returns audio chunks in real time (low latency).
  * Best for live translator apps, calls, or scenarios where a single output language is streamed as audio.

Event-based synthesis steps:

1. Configure translation settings (including voice selection).
2. Register an `onSynthesizing` handler to capture audio as it is produced.
3. Call `getAudioStream()` or handle audio events to retrieve synthesized audio in real-time.

<Frame>
  <img alt="A slide titled &#x22;Event-Based Speech Synthesis Process&#x22; showing three steps: configure TranslationSettings for voice parameters, register an onSynthesizing handler to capture real-time audio output, and call Result.getAudioStream() to extract the synthesized speech." />
</Frame>

* Manual speech synthesis:
  * First translate into one or more target languages.
  * For each translation, call the Text-to-Speech API to generate audio.
  * Ideal for multilingual outputs, batch processing, or when you need per-language synthesis control.

Manual synthesis steps:

1. Translate the spoken input into each target language.
2. For each translation, call the Text-to-Speech API to generate audio.
3. Store or play each generated audio file as required.

<Frame>
  <img alt="A slide titled &#x22;Manual Speech Synthesis Process&#x22; that lists three steps: translate spoken input into multiple target languages, use a Text-to-Speech API to generate speech for each translation, and store or play the generated audio." />
</Frame>

The sample Python script above uses the manual approach (translate then synthesize). For truly live scenarios, prefer the event-based streaming approach to reduce end-to-end latency.

## Links and references

* Speech Studio: [https://speech.microsoft.com/](https://speech.microsoft.com/)
* Azure Speech SDK (Python): [https://pypi.org/project/azure-cognitiveservices-speech/](https://pypi.org/project/azure-cognitiveservices-speech/)
* Azure Speech documentation: [https://learn.microsoft.com/azure/cognitive-services/speech-service/](https://learn.microsoft.com/azure/cognitive-services/speech-service/)

With this overview and the sample code, you can integrate Azure Speech translation into apps to transcribe, translate, and optionally synthesize multilingual speech outputs for real-time and batch workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/188c2a25-9d63-45b4-b934-33ab2d412470/lesson/ecab9126-0f11-4e26-935b-63d806f5b7ef" />
</CardGroup>


# Custom Translation

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Translating-Text/Custom-Translation/page

Explains how to train and deploy Azure Custom Translator models using parallel corpora so translations reflect organization or industry specific terminology

Custom Translation helps when out-of-the-box translation models do not capture your organization- or industry-specific terminology and phrasing.

<Frame>
  <img alt="A presentation slide titled &#x22;Custom Translation&#x22; showing a translation icon and the caption: &#x22;Translate organization- or industry-specific terms not in the default Translator model.&#x22;" />
</Frame>

What is Custom Translation?

* It trains a translation model on parallel text (source/target language pairs) that contain your preferred translations for domain-specific terms.
* The result is consistent translations that reflect company style, legal phrasing, medical terminology, or any other specialized vocabulary.

How it works (high-level)

1. Sign in to the Azure Custom Translator portal — the web UI for creating, training, evaluating, and managing custom translation projects.
2. Create or connect a workspace — a container for projects, models, and associated assets.
3. Start a new project — name it, set source and target languages, and choose a domain (for example, medical, legal, or a custom domain).
4. Upload training data — provide parallel documents (aligned source/target pairs) so the model learns your desired translations for terms and phrases.
5. Train the model — after training, publish or deploy the model so it becomes available as a translation endpoint.

<Frame>
  <img alt="A presentation slide titled &#x22;How to Build a Tailored Translation Model&#x22; showing three connected steps: Step 3 &#x22;Initiate Project&#x22;, Step 4 &#x22;Upload Training Data&#x22;, and Step 5 &#x22;Train & Deploy&#x22; on a dark background." />
</Frame>

Workflow summary

| Step                       | Purpose                             | Notes                                          |
| -------------------------- | ----------------------------------- | ---------------------------------------------- |
| Create workspace & project | Organize assets and settings        | Project ties together language pair and domain |
| Upload parallel corpora    | Teach model preferred translations  | Use high-quality, aligned source/target pairs  |
| Train & evaluate           | Tune model to your data             | Evaluate using held-out test sets              |
| Publish model              | Make model available as an endpoint | Publishing yields a category/project ID        |

Using your custom model in Translator API calls

* When you publish a custom model, Azure assigns a category ID (sometimes called a project category ID). Provide this category ID in your Translator API requests to route translations to your custom model instead of the default system model.

Example curl request using the category parameter (Translator Text API v3.0):

```bash theme={null}
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to=de&category=YOUR_CATEGORY_ID" \
  -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"Text":"Please review the patient consent form."}]'
```

Tips and best practices

* Provide high-quality, representative parallel data covering the phrases and terms you want translated.
* Include multiple examples and contexts for ambiguous terms to improve disambiguation.
* Hold out a test set (not used for training) to measure actual translation improvements.
* Document and version your training datasets so you can reproduce and iterate on model improvements.

<Callout icon="lightbulb">
  Ensure your parallel data is clean, well-aligned, and representative of the terminology and phrasing you expect in production. Data quality and coverage directly affect the performance of your custom translation model.
</Callout>

Additional resources

* Microsoft Docs: Custom Translator — [https://learn.microsoft.com/azure/cognitive-services/translator/custom-translator/](https://learn.microsoft.com/azure/cognitive-services/translator/custom-translator/)
* Sample datasets (English↔German): [https://github.com/MicrosoftTranslator/CustomTranslatorSampleDatasets](https://github.com/MicrosoftTranslator/CustomTranslatorSampleDatasets)

For a hands-on starting point, the sample dataset repository on GitHub contains example parallel corpora you can upload to the Custom Translator portal to experiment with training and evaluation.

<Frame>
  <img alt="A screenshot of a GitHub repository page for &#x22;MicrosoftTranslator/CustomTranslatorSampleDatasets&#x22; showing a list of files in the main branch and an About sidebar with repository details." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/5f79b307-e7de-415a-9d8d-82499e075c20/lesson/148e33c0-cd21-4b98-8720-691fc03567dc" />
</CardGroup>
