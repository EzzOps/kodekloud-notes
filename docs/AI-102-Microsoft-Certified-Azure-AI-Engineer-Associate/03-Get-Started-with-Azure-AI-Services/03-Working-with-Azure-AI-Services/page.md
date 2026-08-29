# Working with Azure AI Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-AI-Services/Working-with-Azure-AI-Services/page

Guide to creating Azure AI Language services and performing sentiment analysis using Python SDK and REST API, comparing approaches and covering endpoints, keys, security, and best practices.

This guide demonstrates how to create an Azure AI Language service in the Azure portal and call its sentiment analysis capability using both the Python SDK and the REST API. You’ll see that the SDK provides a more concise developer experience, while the REST example shows the underlying HTTP payloads and is useful when SDKs are unavailable.

What you'll learn:

* How to create an Azure AI service (multi-service account vs. single dedicated service)
* Where to find endpoints and keys
* Example code for sentiment analysis using the Python SDK
* Example code for sentiment analysis using the REST API
* When to choose SDK vs. REST

## Create an Azure AI service in the portal

If you already have a multi-service account, it exposes multiple capabilities (OpenAI, Speech, Vision, Language, etc.) under the same account-level keys. The portal lists AI service resources like this:

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Azure AI services&#x22; page, with a left-hand menu of AI service options and a single listed resource named &#x22;aiservicesai900&#x22; in the main pane." />
</Frame>

If you open a multi-service account and look at Keys and Endpoint, you'll see the shared account-level keys and multiple capability endpoints (OpenAI, Speech, Content Safety, Computer Vision, Content Understanding, etc.).

<Frame>
  <img alt="A screenshot of the Azure AI Services &#x22;Keys and Endpoint&#x22; page for the resource &#x22;aiservicesai900.&#x22; It shows masked API keys, the location &#x22;eastus,&#x22; and OpenAI endpoints for Language, Dall‑E, and Whisper." />
</Frame>

If you prefer a single-purpose resource (for example, a dedicated Language resource), create it from the Language service blade. During creation:

* Select a subscription and resource group (e.g., rg-ai102-get-started-sdk)
* Choose a region (e.g., East US)
* Provide a globally unique resource name (this becomes \<service-name>.cognitiveservices.azure.com)
* Pick a pricing tier (for example S1)

Create the resource and then check the resource group/overview to confirm creation.

<Frame>
  <img alt="A screenshot of the Azure portal showing the Project Details form and a pop-up to create a new resource group, with the name field filled as &#x22;rg-ai102-get-star&#x22; and OK/Cancel buttons. The Subscription is set to &#x22;Kodekloud Labs&#x22; and a notice about the free tier/pricing is visible below." />
</Frame>

Once created, open the resource and go to **Keys and Endpoint** to copy the endpoint URL and one of the two keys for use in your client code.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the Overview page for a resource group named &#x22;rg-ai102-get-started-sdk.&#x22; The page displays subscription details, filters and a single listed resource, plus the left-hand navigation menu with settings and monitoring options." />
</Frame>

> **lightbulb** Do NOT embed long-lived keys directly in source code for production. Use Azure Key Vault, managed identities, or environment variables to secure secrets.

## Choose: SDK vs REST

Both approaches return a sentiment label and confidence scores. Use SDKs when available for a cleaner, idiomatic interface and automatic authentication helpers. Use REST when SDKs are not available or you need direct HTTP access.

Comparison at a glance:

| Resource                            | Use case                                          | Pros                                                       |
| ----------------------------------- | ------------------------------------------------- | ---------------------------------------------------------- |
| Python SDK (azure-ai-textanalytics) | Typical development on Python                     | Concise code, structured objects, handles auth and retries |
| REST API (HTTP POST)                | Direct HTTP integrations, non-supported languages | Shows exact payload and headers, no SDK dependency         |

Useful links:

* [Azure AI Language service overview](https://learn.microsoft.com/azure/ai-services/)
* [Azure SDK for Python - Text Analytics docs](https://learn.microsoft.com/azure/cognitive-services/text-analytics/overview)
* [Language REST API reference (analyze-text)](https://learn.microsoft.com/azure/cognitive-services/language-service/rest-api)

## SDK approach (Python)

Install the SDK packages:

pip install azure-core azure-ai-textanalytics

Example Python SDK usage. Replace endpoint and key with your values (do not hard-code in production).

```python theme={null}
