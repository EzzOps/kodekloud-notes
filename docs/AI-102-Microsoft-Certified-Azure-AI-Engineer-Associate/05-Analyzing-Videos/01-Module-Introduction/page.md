# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyzing-Videos/Module-Introduction/page

Overview of using Azure Video Indexer to extract searchable video metadata including transcripts, speaker diarization, OCR, emotions, topics, and integrate insights via portal or APIs

Welcome to the module on analyzing video content. This lesson covers how to extract searchable, actionable insights from video using Azure Video Indexer — a cloud service that combines speech-to-text, computer vision, and natural language processing to turn video into structured metadata.

We’ll focus on Video Indexer’s analysis capabilities and practical workflows (portal and APIs), so you can ingest video, retrieve rich insights, and integrate results into applications and automation pipelines.

Overview

* Target audience: Developers, data engineers, content managers, and ML practitioners who want to automate video indexing and enhance search, compliance, and content understanding.
* Scope: Analysis and integration patterns using Azure Video Indexer (portal and REST APIs). Account provisioning and subscription setup are out of scope; see References for links.

By the end of this lesson you will be able to:

| Capability                                             | What you’ll achieve                                                                                            | Example outcome                                                                            |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Automated analysis (portal & APIs)                     | Run video analysis jobs using the Video Indexer portal or programmatically via REST APIs/SDKs.                 | Submit a video and retrieve a JSON insights payload with timestamps and confidence scores. |
| Extract transcripts and identify people                | Obtain speaker-attributed transcripts, named people recognition, and detected faces.                           | Search spoken phrases and link them to detected speakers or face thumbnails.               |
| Detect emotions, topics, and faces                     | Surface emotional cues, topics, and facial metadata for content classification and moderation.                 | Tag scenes with detected emotions and generate topic labels for content categorization.    |
| Use OCR, speaker diarization, and scene/shot detection | Extract on-screen text, separate speakers (diarization), and segment content into scenes/shots for navigation. | Enable time-aligned search and create chapter markers for long videos.                     |
| Enrich models with domain-specific vocabulary          | Add custom vocabulary or domain models to improve recognition for specialized terminology.                     | Improve speech-to-text accuracy for industry jargon or product names.                      |
| Integrate outputs into apps & pipelines                | Consume Video Indexer results to power search, analytics dashboards, compliance workflows, or automated clips. | Feed insights into a search index, CMS, or downstream ML pipeline.                         |

> **lightbulb** Before you begin, make sure you have access to an Azure subscription and a Video Indexer account (or appropriate API keys). This module concentrates on analysis workflows, so ensure account provisioning is complete before following the walkthroughs.

How this lesson is organized

* Concepts: Core features of Azure Video Indexer and key terms (transcript, diarization, OCR, shot detection, content moderation).
* Hands-on: Uploading videos (portal & API), retrieving insights JSON, and parsing common output fields.
* Customization: Using custom vocabulary and domain models to improve results.
* Integration patterns: Examples for search, CMS enrichment, analytics, and automation pipelines.

Quick glossary

* Transcript: Time-aligned speech-to-text output, often with speaker attribution.
* Speaker diarization: The process of separating and labeling different speakers in audio.
* OCR: Optical character recognition used to extract text from video frames.
* Scene/shot detection: Automatic segmentation of video into logical scenes and shots.
* Insights JSON: The structured output produced by Video Indexer containing recognized entities, timestamps, and metadata.

References and further reading

* [Azure Video Indexer Overview](https://learn.microsoft.com/en-us/azure/azure-video-indexer/)
* [Video Indexer API documentation](https://learn.microsoft.com/en-us/azure/azure-video-indexer/)
* [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)

Next steps
Proceed to the first hands-on topic to learn how to upload a video to Video Indexer and retrieve the Insights JSON using both the portal and the REST API.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/589e73d5-1588-4196-903e-af5a01f4693a/lesson/25c79b92-6753-49cc-98e2-75555542d619)
