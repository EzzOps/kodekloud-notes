# Load Azure credentials from environment
load_dotenv()
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Initialize client
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        if text:
            # Example: run language detection
            lang_resp = client.detect_language(documents=[text])
            if not lang_resp[0].is_error:
                result["language"] = {
                    "name": lang_resp[0].primary_language.name,
                    "iso": lang_resp[0].primary_language.iso6391_name,
                    "confidence": lang_resp[0].primary_language.confidence_score
                }

            # Key phrases
            kp_resp = client.extract_key_phrases(documents=[text])
            if not kp_resp[0].is_error:
                result["key_phrases"] = kp_resp[0].key_phrases

            # Sentiment
            s_resp = client.analyze_sentiment(documents=[text])
            if not s_resp[0].is_error:
                cs = s_resp[0].confidence_scores
                result["sentiment"] = {
                    "label": s_resp[0].sentiment,
                    "scores": {"positive": cs.positive, "neutral": cs.neutral, "negative": cs.negative}
                }

            # NER
            ner_resp = client.recognize_entities(documents=[text])
            if not ner_resp[0].is_error:
                result["entities"] = [{"text": e.text, "category": e.category, "confidence": e.confidence_score} for e in ner_resp[0].entities]

            # Entity linking
            link_resp = client.recognize_linked_entities(documents=[text])
            if not link_resp[0].is_error:
                result["linked_entities"] = [
                    {"name": e.name, "url": e.url, "source": e.data_source, "matches": [{"text": m.text, "confidence": m.confidence_score} for m in e.matches]}
                    for e in link_resp[0].entities
                ]

            # PII
            pii_resp = client.recognize_pii_entities(documents=[text])
            if not pii_resp[0].is_error:
                result["pii"] = [{"text": p.text, "category": p.category, "confidence": p.confidence_score} for p in pii_resp[0].entities]

    return render_template("index.html", text=text, result=result)

if __name__ == "__main__":
    app.run(debug=True)
```

The screenshot below shows a simple web demo that runs these analyses and displays results (language, sentiment, key phrases, named/PII entities):

<Frame>
  <img alt="A screenshot of a webpage titled &#x22;Azure AI Language Services Demo&#x22; showing a text input box, a &#x22;Run Analysis&#x22; button, and a Results section. The Results list detected language and sentiment (positive), key phrases, and named/PII entities such as &#x22;Jane&#x22; and a phone number (1234566543)." />
</Frame>

***

## Best practices

* Never embed secrets in code. Use environment variables or a secret store.
* Validate and sanitize inputs (especially if integrating with user-generated content).
* Use batch processing for high-throughput scenarios and handle rate limits.
* For compliance, store and handle redacted data according to your organization’s privacy policies.
* Check model/version and SDK docs as behavior and method names can change over time.

## Links and references

* Azure AI Language Service documentation: [https://learn.microsoft.com/azure/cognitive-services/language-service/](https://learn.microsoft.com/azure/cognitive-services/language-service/)
* Azure SDK for Python (Text Analytics package): [https://pypi.org/project/azure-ai-textanalytics/](https://pypi.org/project/azure-ai-textanalytics/)
* GDPR overview: [https://gdpr.eu](https://gdpr.eu)
* HIPAA information: [https://www.hhs.gov/hipaa/index.html](https://www.hhs.gov/hipaa/index.html)

That completes this overview of Azure AI Language Services text-analysis features. Use these tools to extract structure, meaning, and privacy-aware metadata from unstructured text across languages and domains.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/c9630dfe-8597-4a05-bb2f-de84e8e2a7b7/lesson/5252539c-73e7-4b2e-b9d8-0bf5fbb62cfd)


# Building Insights

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyzing-Videos/Building-Insights/page

Using custom AI models and Video Indexer to extract insights from video and audio including face recognition, domain-aware transcription, brand detection, and API or widget integration.

This lesson shows how to extract AI-driven insights from video and audio using custom models. You will learn how to detect people, improve transcriptions with domain-aware language models, and identify brands—boosting searchability, content understanding, and personalization for video assets.

## What you can build

* Face recognition and tracking across video timelines for people analytics and personalization.
* Domain-customized transcription for industry-specific vocabulary and multilingual audiences.
* Brand detection (logos, product mentions) to enable content classification and rights management.

## Custom model types and use cases

| Model type                                  | Typical use case                                          | Benefit                                    |
| ------------------------------------------- | --------------------------------------------------------- | ------------------------------------------ |
| People (facial recognition)                 | Identify and track individuals across footage             | Personalization, credits, analytics        |
| Language (custom transcription/translation) | Recognize domain-specific terms and translate transcripts | Higher accuracy, multilingual distribution |
| Brand detection                             | Locate logos or named products in video frames            | Rights tracking, advertising analytics     |

You can combine these models to create richer metadata for indexing, search, and downstream automation.

To enable facial recognition, create a Face resource in Azure AI Services and connect it with Video Indexer to let indexed videos use face models:

* Face resource docs: [https://learn.microsoft.com/azure/cognitive-services/face/](https://learn.microsoft.com/azure/cognitive-services/face/)
* Video Indexer: [https://www.videoindexer.ai/](https://www.videoindexer.ai/)

> **warning** Face recognition may require special approval from Microsoft and may be restricted in some regions or for certain accounts. Request and obtain the required access before using face recognition features.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Building Insights&#x22; with three numbered panels: 01 People (facial recognition), 02 Language (domain-specific transcription/terminology), and 03 Brand (detect product/company names). Each panel includes an icon and a brief description of the model use." />
</Frame>

## Indexer options: widgets vs REST API

Video Indexer provides two primary integration patterns:

* Widgets (embed/iframe): Quick, interactive visualization of insights (topics, people, scenes, transcripts) you can drop into web pages. Use this when you want a low-code front-end integration and interactive playback.
* REST API: Programmatic access to metadata, management, and automation. Choose the API for CI/CD, custom dashboards, batch processing, or workflows that integrate with other services.

Reference:

* Video Indexer: [https://www.videoindexer.ai/](https://www.videoindexer.ai/)
* Video Indexer REST API docs: [https://learn.microsoft.com/azure/azure-video-indexer/video-indexer-use-api](https://learn.microsoft.com/azure/azure-video-indexer/video-indexer-use-api)

Use widgets when embedding the full insight UI. If the video is private, ensure viewers are authenticated or have permission before embedding. For automated scenarios or extracting metadata in pipelines, call the REST API to fetch structured data and orchestrate processing.

<Frame>
  <img alt="A slide titled &#x22;Video Indexer Widgets and API&#x22; showing a &#x22;REST API for Automation&#x22; callout and a text bubble that reads &#x22;Retrieve video metadata, including account details, duration, processing status, and language.&#x22; The slide has a dark teal background with a circular icon at left and a small &#x22;© Copyright KodeKloud&#x22; note at the bottom." />
</Frame>

## Sample REST API response (illustrative)

> **lightbulb** The JSON shown below is a simplified example of metadata returned by the Video Indexer APIs. Actual responses may include additional fields depending on the request parameters and enabled features.

```json theme={null}
{
  "results": [
    {
      "accountId": "1234abcd-9876fghi-0156kihb-00123",
      "id": "a12345bc6",
      "name": "Responsible AI",
      "description": "Microsoft Responsible AI video",
      "created": "2021-01-05T15:33:58.918+00:00",
      "lastModified": "2021-01-05T15:50:03.123+00:00",
      "lastIndexed": "2021-01-05T15:34:08.007+00:00",
      "processingProgress": "100%",
      "durationInSeconds": 114,
      "sourceLanguage": "en-US"
    }
  ]
}
```

Key metadata fields to use in automation and analytics:

* accountId, id: identify the account and video resource.
* name, description: human-readable labels for UI and reports.
* created, lastModified, lastIndexed: timeline for processing and audits.
* processingProgress: track indexing status for orchestration.
* durationInSeconds, sourceLanguage: media properties for players and translations.

## Embedding, access, and automation tips

* Embedding: copy the widget iframe from Video Indexer to display the indexed video and its insights on your web pages. Example direct URL pattern:

```text theme={null}
https://www.videoindexer.ai/accounts/0ae29563-3796-4210-b2f0-0590d4a45948/videos/slut1smuc
```

* Access control: private videos require viewer authentication and permission; public videos can be embedded broadly.
* Automation: use the REST API for retrieving metadata, downloading assets (transcripts, thumbnails), and integrating insights into search indexes, CMS platforms, and analytics pipelines.

For full endpoint details, authentication methods, and examples, see the Video Indexer REST API reference:

* [https://learn.microsoft.com/azure/azure-video-indexer/video-indexer-use-api](https://learn.microsoft.com/azure/azure-video-indexer/video-indexer-use-api)

This concludes the lesson on building insights with Video Indexer—use custom models and the API to transform raw media into searchable, actionable intelligence.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/589e73d5-1588-4196-903e-af5a01f4693a/lesson/a3cd0f34-3ef5-4c1e-9479-8e1b9ac34075)
