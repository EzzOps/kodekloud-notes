# Working with Translator Service

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Translating-Text/Working-with-Translator-Service/page

Guide to using Azure Translator to detect language, translate text into multiple languages, and transliterate scripts with REST examples and a Python SDK sample.

This guide demonstrates how to detect language, perform translations, and transliterate text using Azure's Translator service. You'll see REST examples (detect, translate, transliterate) and a concise Python SDK example using the `azure-ai-translation-text` package.

<Frame>
  <img alt="A dark-themed slide showing the KodeKloud logo at the top and the centered title &#x22;Working with Translator Service.&#x22; Small copyright text &#x22;© Copyright KodeKloud&#x22; appears in the lower-left corner." />
</Frame>

Overview

* Detect: Identify the language of a given piece of text and learn whether translation or transliteration is supported.
* Translate: Convert text between languages (one or more target languages).
* Transliterate: Convert text from one script to another (e.g., Arabic script → Latin script).
* SDK option: Use the Azure Python SDK for integration with fewer manual HTTP calls.

Quick reference links

* [Translator Text API documentation](https://learn.microsoft.com/azure/cognitive-services/translator/)
* [Azure SDK for Python — Translation client](https://learn.microsoft.com/azure/developer/python/)

API endpoint summary

| Operation     | Endpoint (path) | Key query parameters                        |
| ------------- | --------------- | ------------------------------------------- |
| Detect        | /detect         | api-version                                 |
| Translate     | /translate      | api-version, from, to (repeatable)          |
| Transliterate | /transliterate  | api-version, language, fromScript, toScript |

Detect (REST)
Use the detect endpoint to identify the language and whether translation/transliteration is supported for the input text.

Example REST request (detect):

```http theme={null}
POST https://api.cognitive.microsofttranslator.com/detect?api-version=3.0
Content-Type: application/json
Ocp-Apim-Subscription-Key: <your-key>

[
  { "Text": "مرحبا" }
]
```

Example response (detect):

```json theme={null}
[
  {
    "language": "ar",
    "score": 1.0,
    "isTranslationSupported": true,
    "isTransliterationSupported": true
  }
]
```

Use the returned ISO language code (for example, "ar") to decide the next action — translate to other languages or transliterate to another script.

Translate (REST)
Translate the detected source language into one or more target languages by calling the translate endpoint and specifying target languages as query parameters.

Example REST request (translate):

```http theme={null}
POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=ar&to=en&to=fr"
Content-Type: application/json
Ocp-Apim-Subscription-Key: <your-key>

[
  { "Text": "مرحبا" }
]
```

Example response (translate):

```json theme={null}
[
  {
    "translations": [
      { "text": "Hello", "to": "en" },
      { "text": "Bonjour", "to": "fr" }
    ]
  }
]
```

Transliteration (REST)
Transliteration converts text from one writing system (script) into another. Provide the source language and script and the desired target script.

Example REST request (transliterate):

```http theme={null}
POST "https://api.cognitive.microsofttranslator.com/transliterate?api-version=3.0&language=ar&fromScript=Arab&toScript=Latn"
Content-Type: application/json
Ocp-Apim-Subscription-Key: <your-key>

[
  { "Text": "مرحبا" }
]
```

Example response (transliterate):

```json theme={null}
[
  {
    "script": "Latn",
    "text": "Marhaba"
  }
]
```

Translate vs. Transliterate — quick comparison

| Feature | Translate                                   | Transliterate                          |
| ------- | ------------------------------------------- | -------------------------------------- |
| Purpose | Convert meaning across languages            | Convert characters across scripts      |
| Input   | Text in any supported language              | Text and source script                 |
| Output  | Target-language text (semantic translation) | Same-language text in different script |
| Example | "مرحبا" → "Hello"                           | "مرحبا" (Arab) → "Marhaba" (Latn)      |

Python SDK (azure-ai-translation-text)
You can perform detection, translation, and transliteration using the Azure Python SDK. Install and verify the package:

```bash theme={null}
pip3 install azure-ai-translation-text
pip3 show azure-ai-translation-text
```

Example installation output (trimmed):

```text theme={null}
Name: azure-ai-translation-text
Version: 1.0.1
Summary: Microsoft Azure AI Translation Text Client Library for Python
Home-page: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk
Author: Microsoft Corporation
License: MIT
Requires: azure-core, isodate, typing-extensions
```

Complete Python example
This example detects language (if returned by the service), translates a Korean sentence into English and French, and transliterates it into the Latin script.

```python theme={null}
