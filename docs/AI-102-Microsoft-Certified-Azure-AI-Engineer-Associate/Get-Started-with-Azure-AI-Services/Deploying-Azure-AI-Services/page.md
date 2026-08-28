# Deploying Azure AI Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-AI-Services/Deploying-Azure-AI-Services/page

Guide for provisioning and configuring Azure AI Services, selecting resource types, managing endpoints and keys, planning deployments, and connecting applications via REST APIs or language SDKs

This guide shows how to provision and configure Azure AI Services, choose the appropriate resource type, and connect from applications using REST APIs or language SDKs. It covers portal setup, deployment considerations, authentication, and sample requests so you can get a tested endpoint, keys, and region for development or production.

## Create an Azure AI resource

To get started, create an Azure AI resource in the Azure portal. Required information includes:

* Subscription and resource group
* Deployment region — pick a region close to your users to reduce latency and meet data residency requirements
* Instance name
* Pricing tier — some capabilities may offer a free tier for experimentation; otherwise select a plan matching your expected usage

After entering the required fields, click Review + Create to provision the resource.

<Frame>
  <img alt="A presentation slide titled &#x22;Setting Up Azure AI Services&#x22; showing a screenshot of the Azure portal &#x22;Create Azure AI services&#x22; form with fields for subscription, resource group, region, name, and pricing tier. The slide has a dark blue background and a small &#x22;© Copyright KodeKloud&#x22; note in the bottom left." />
</Frame>

<Callout icon="lightbulb">
  Tip: Use a descriptive name and consistent tagging for resources to simplify billing, monitoring, and automation. Free tiers are ideal for testing but verify quotas and limits before using in production.
</Callout>

## Multi-service vs Single-service resources

When creating a resource you can choose between:

* Multi-service resource: exposes multiple AI capabilities (Language, Vision, Speech, etc.) through a single endpoint and shared keys — simplifies management and billing.
* Single-service resource: scoped to one capability (for example, a Language-only or Vision-only resource) with its own endpoint and keys — useful for isolation, fine-grained permissions, or separate team ownership.

Use the table below to decide which fits your scenario.

| Resource Type  | When to use                                                                              | Benefits                                               |
| -------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Multi-service  | Small teams or consolidated billing; want a single endpoint for multiple AI capabilities | Fewer endpoints/keys, simplified management            |
| Single-service | Separate teams, strict access control, or different regions/tiers per capability         | Isolation, granular permissions, independent lifecycle |

<Frame>
  <img alt="A presentation slide titled &#x22;Setting Up Azure AI Services&#x22; that compares resource types. It contrasts a &#x22;Multi-service Resource&#x22; (single key/endpoint for multiple AI services) with a &#x22;Single-service Resource&#x22; (one unique key and endpoint per service), with a central &#x22;Resource Type&#x22; circle." />
</Frame>

Choose single-service resources when you need strict separation (for example, the Vision team should not access Speech). Choose multi-service to simplify management and reduce the number of endpoints and keys.

## Deployment considerations

Plan these factors before provisioning to avoid rework:

* Subscription & region — compliance, data residency, and latency constraints
* Pricing & tiers — costs, quotas, and available features differ by tier
* Security & access — use Azure RBAC, key rotation, and managed identities where possible

<Frame>
  <img alt="A presentation slide titled &#x22;Setting Up Azure AI Services.&#x22; It shows three deployment-consideration cards: &#x22;Subscription and Region,&#x22; &#x22;Pricing and Tiers,&#x22; and &#x22;Security and Access,&#x22; each with a short explanatory note." />
</Frame>

### Endpoints, keys, and locations

After deployment you will obtain:

* Endpoint — base URL your application calls
* Keys — typically two API keys for key rotation; either key can be used
* Location — region hosting the resource (for example, eastus). Some SDKs and REST endpoints require the region value

Example values (format):

```text theme={null}
https://ai102-cog.cognitiveservices.azure.com/
eastus
```

| Artifact | Description                                                     |
| -------: | --------------------------------------------------------------- |
| Endpoint | Base URL for REST and SDK calls                                 |
|     Keys | API keys for authentication (rotate regularly)                  |
| Location | Azure region of the resource; used for some requests or routing |

<Callout icon="lightbulb">
  Best practice: rotate keys regularly and prefer Microsoft Entra ID (OAuth bearer tokens) where supported for stronger identity-based authentication. See Microsoft Entra ID docs: [https://learn.microsoft.com/en-us/azure/active-directory/](https://learn.microsoft.com/en-us/azure/active-directory/)
</Callout>

## Accessing Azure AI Services via REST APIs

REST endpoints provide platform-independent access to Azure AI capabilities. Typical request flow:

1. Client sends an HTTP request to the service endpoint.
2. Request contains authentication (API key header or Microsoft Entra ID bearer token).
3. Request body is JSON following the service schema.
4. Service returns a structured JSON response with analysis results.

Authentication options:

| Method                     | Header example                         | When to use                                                                |
| -------------------------- | -------------------------------------- | -------------------------------------------------------------------------- |
| API key                    | `api-key: <your-api-key>`              | Simple setup, suitable for server-to-server calls or quick testing         |
| Microsoft Entra ID (OAuth) | `Authorization: Bearer <access_token>` | Preferred for production deployments; supports RBAC and managed identities |

Example curl request (replace placeholders):

```bash theme={null}
curl -X POST "https://<your-endpoint>/language/analyze?api-version=2024-01-31" \
  -H "Content-Type: application/json" \
  -H "api-key: <your-api-key>" \
  -d '{
    "kind": "SentimentAnalysis",
    "analysisInput": {
      "documents": [
        { "id": "1", "language": "en", "text": "I love the new product!" }
      ]
    },
    "parameters": {}
  }'
```

Example JSON response structure:

```json theme={null}
{
  "results": {
    "documents": [
      {
        "id": "1",
        "sentiment": "positive",
        "confidenceScores": {
          "positive": 0.99,
          "neutral": 0.01,
          "negative": 0.0
        }
      }
    ],
    "errors": []
  }
}
```

REST usage benefits:

* Full control over HTTP behavior and payloads
* Platform/language agnostic
* Useful for environments without official SDK support

## Using SDKs

Official SDKs reduce boilerplate and provide language-native interfaces, automatic retries, and credential handling. SDKs are available for .NET, Python, Node.js, and Java.

Benefits of SDKs:

* Simplified authentication and request construction
* Native response objects and error types
* Built-in retry logic and telemetry integration

Example Python (Text Analytics) using the azure-ai-textanalytics SDK:

```python theme={null}
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-endpoint>/"
key = "<your-api-key>"

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = ["I had a wonderful day!"]
response = client.analyze_sentiment(documents)

for doc in response:
    print(f"Document sentiment: {doc.sentiment}")
    print(f"Confidence scores: {doc.confidence_scores}")
```

SDKs are wrappers around REST APIs and are recommended for most development scenarios unless you need direct control of raw HTTP requests.

## Summary and next steps

You now know how to:

* Provision an Azure AI resource in the portal
* Choose between multi-service and single-service resources
* Plan deployment with region, pricing, and security in mind
* Retrieve endpoint, keys, and location values
* Call services via REST or use language SDKs for faster integration

Next step: Provision an AI resource in your Azure subscription, record the endpoint, keys, and region, and run the curl or SDK examples above from a development environment.

## Links and references

* [Microsoft Entra ID (Azure AD) documentation](https://learn.microsoft.com/en-us/azure/active-directory/)
* [Azure AI documentation](https://learn.microsoft.com/azure/ai-services)
* [Azure SDKs and tools](https://learn.microsoft.com/azure/developer/python/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/10ea4eb0-486e-4464-a864-dda671e1b308/lesson/ced83dab-0b30-4b1f-92ab-b5af6a453782" />
</CardGroup>
