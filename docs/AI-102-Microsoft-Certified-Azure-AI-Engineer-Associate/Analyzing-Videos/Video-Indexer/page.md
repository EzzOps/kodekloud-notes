# Video Indexer

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyzing-Videos/Video-Indexer/page

Overview of Azure AI Video Indexer and how to create resources, upload videos, and retrieve searchable insights such as transcripts, speaker labels, topics, sentiment, faces, and OCR

Azure AI Video Indexer helps you find important moments in long meeting recordings and other long-form video content. Manually scanning recordings is time-consuming; Video Indexer automates that work by extracting searchable, time-aligned insights — spoken words, speakers, topics, sentiment, faces, on-screen text, and more — so you can jump straight to the moments that matter. For example, a product manager can instantly locate every segment across multiple meetings where a product launch was discussed.

In this article we review Video Indexer’s core capabilities, show how to create and connect a resource in the Azure Portal, and outline how to upload, inspect, and programmatically retrieve insights.

Key capabilities

* Automatic transcription with timestamps and speaker diarization.
* Topic detection, sentiment analysis, and conversation-level signals (questions, decisions).
* Face detection and optional identification (when you provide reference images).
* OCR for on-screen text, object and scene detection, and keyframes.
* Content moderation to flag sensitive or inappropriate content.

These insights help content creators, educators, marketing teams, and enterprises categorize, search, and analyze video content far more efficiently than manual review.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Create storage account&#x22; form with fields for Name, Account kind, Performance (Standard/Premium), and Replication (Locally‑redundant storage). The Name field is partially filled in and the page header shows &#x22;Azure AI Video Indexer.&#x22;" />
</Frame>

Features at a glance

| Feature                             | What it extracts                           | Typical use case                              |
| ----------------------------------- | ------------------------------------------ | --------------------------------------------- |
| Transcription & speaker diarization | Time-aligned text and who spoke when       | Search meetings by keyword or speaker         |
| Topic detection                     | High-level themes and clusters             | Group videos by subject or summarize content  |
| Sentiment analysis                  | Positive/negative/neutral per segment      | Track audience or speaker sentiment over time |
| Face & celebrity recognition        | Faces and optional known identities        | Tag speakers or highlight mentions of people  |
| OCR                                 | Text appearing on-screen                   | Extract slide content, captions, or overlays  |
| Scene detection & keyframes         | Scene boundaries and representative frames | Generate thumbnails or chapter markers        |
| Content moderation                  | Flags for sensitive content                | Enforce compliance and safety rules           |

Creating a Video Indexer resource in the Azure Portal

1. In the Azure Portal search box, type “Video Indexer” and select Azure AI Video Indexer.
2. Create a new Video Indexer resource. During creation you will:
   * Choose a subscription and resource group.
   * Choose or create a storage account (Video Indexer stores uploaded media and derived artifacts there).
   * Optionally connect other AI resources later for extended capabilities (not required to index videos).
3. Review and create the resource. After deployment, the resource appears in your portal and can be associated with the Video Indexer web app.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal on the &#x22;Create a Video Indexer resource&#x22; review page showing a &#x22;Validation passed&#x22; message and a summary of resource settings (subscription, resource group, resource name, region, storage account). The browser toolbar and user menu are visible at the top." />
</Frame>

Accessing the Video Indexer web app

* Open the Video Indexer portal at [https://videoindexer.ai](https://videoindexer.ai) and sign in with the same account used to create the Azure resource.
* When you first sign in you may use a trial account; after you provision the Azure resource you can associate that resource and its storage account with your Video Indexer account.
* Once associated, you can upload videos from your local machine, from the linked storage account, or via a public URL.

Uploading and indexing a video

* Click Upload and choose a file from your device, select from the connected storage account, or paste a file URL.
* Choose language, privacy settings, and the indexing preset that fits your needs.
* Confirm any required consent and click Upload + Index. The service begins ingesting and processing the video.

<Frame>
  <img alt="A screenshot of the Azure AI Video Indexer web app showing an &#x22;Upload and index&#x22; dialog with a summary overview (video language, indexing preset, privacy) and a checked consent box, with the &#x22;Upload + index&#x22; button highlighted." />
</Frame>

<Callout icon="lightbulb">
  When uploading, be aware that certain advanced insights (for example, custom face recognition or celebrity recognition) may require additional configuration or permissions. Always confirm you have the required rights to process personal data in your region.
</Callout>

Indexing workflow and what runs after upload

Once the upload begins, Video Indexer applies multiple models and pipelines, which may include:

* Audio pre-processing (noise reduction, channel separation)
* Automatic speech recognition and closed captions
* Speaker diarization and speaker labeling
* Object, scene, and keyframe detection
* OCR for on-screen text
* Topic and sentiment detection
* Face detection and optional identification
* Content moderation checks

Indexing time depends on video length, selected features, and queue load; typical processing ranges from a few minutes for short clips to longer for full-length recordings.

Inspecting indexed results

* After indexing completes open the video in the Video Indexer UI to see a timeline, interactive transcript, detected topics, object/scene tags, faces, and sentiment trends.
* Use timeline search to jump to keywords, speaker segments, or flagged moments (questions, decisions).
* Export or download metadata and subtitles, or copy insights into your content workflows.

<Frame>
  <img alt="A man wearing a &#x22;KodeKloud&#x22; t-shirt sits facing the camera with computer monitors behind him. The image is shown inside a browser window displaying the Azure AI Video Indexer interface and video insights on the right." />
</Frame>

Programmatic access and the Video Indexer API

Video Indexer provides REST APIs so you can automate uploads, control indexing, poll progress, and fetch insights as JSON for integration into search, analytics, or custom UI experiences.

Basic flow

1. Acquire an access token for your account.
2. Upload the media or point Video Indexer to a storage URL.
3. Monitor indexing status until complete.
4. Retrieve insights (transcript, faces, OCR, topics, sentiment, keyframes).

Example: fetch an account access token (replace placeholders)

```bash theme={null}
curl -X GET "https://api.videoindexer.ai/Auth/{location}/Accounts/{accountId}/AccessToken?allowEdit=true" \
  -H "Ocp-Apim-Subscription-Key: {SUBSCRIPTION_KEY}"
```

Example: upload a video (basic form upload; use the returned access token)

```bash theme={null}
curl -X POST "https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos?name=my-video.mp4&accessToken={ACCESS_TOKEN}" \
  -F "file=@/path/to/my-video.mp4"
```

Note: The API supports many parameters to control language, indexing presets, speaker diarization, and callback webhooks for asynchronous workflows. Store returned JSON (timestamps, object metadata, face tags, OCR results) in your search index or database to enable fast query and rich application experiences.

Quick troubleshooting tips

* If indexing appears stuck, check the job status in the UI or via the API and review the video length/format.
* Ensure the storage account is correctly linked and that the Video Indexer service has permission to read/write blobs.
* For custom face recognition, pre-register reference images and ensure you comply with privacy and data protection regulations.

Summary

Azure AI Video Indexer converts unstructured video into structured, searchable insights: transcription, speaker identification, face detection, OCR, topics, sentiment, scene segmentation, and content moderation. Use the web app for manual review and exploration, or the REST API to integrate indexing into automated pipelines and build searchable video experiences.

Links and references

* [Azure AI Video Indexer portal](https://videoindexer.ai)
* [Video Indexer documentation (Azure)](https://learn.microsoft.com/azure/media-services/video-indexer/)
* [Kubernetes Documentation](https://kubernetes.io/docs/) (example link)
* [Azure Storage documentation](https://learn.microsoft.com/azure/storage/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/589e73d5-1588-4196-903e-af5a01f4693a/lesson/b061f287-718c-4391-a08f-9f9a82712b2a" />
</CardGroup>
