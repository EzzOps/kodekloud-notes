# Sign in interactively
az login

# (Optional) Set the subscription to use
az account set --subscription "YourSubscriptionID"
```

Create an Azure OpenAI (Cognitive Services) resource using Azure CLI:

```bash theme={null}
az cognitiveservices account create \
  --name YourAIResource \
  --resource-group YourResourceGroup \
  --location eastus \
  --kind OpenAI \
  --sku S0 \
  --subscription YourSubscriptionID
```

Notes:

* Use uppercase `S0` for the `--sku` value in most cases.
* This command provisions a Cognitive Services account with `kind` set to `OpenAI`. After provisioning, retrieve keys and the endpoint from the resource overview.

<Callout icon="lightbulb">
  Before creating an Azure OpenAI resource, ensure your account and subscription have the required permissions and quota. Some tenants require an access request or enrollment for Azure OpenAI—check your organization's policy and request access if needed.
</Callout>

## Post-deployment: keys, endpoints, and Azure AI Foundry

* From the resource overview you can:
  * View and copy your endpoint and keys.
  * Navigate to Azure AI Foundry (Azure AI Studio) for model experimentation and deployment.
* Use the endpoint and keys to authenticate and call the Azure OpenAI APIs:
  * Overview and API reference: [https://learn.microsoft.com/azure/cognitive-services/openai/overview](https://learn.microsoft.com/azure/cognitive-services/openai/overview)
  * Azure AI Studio: [https://learn.microsoft.com/azure/ai-studio/](https://learn.microsoft.com/azure/ai-studio/)

Common use cases for Azure OpenAI models:

* Generate or summarize text
* Answer natural-language questions
* Assist with code generation or translation
* Integrate securely in enterprise Azure architectures

## Troubleshooting tips

* If the portal shows validation errors, verify all required fields (Subscription, Resource Group, Region, Pricing tier).
* If CLI returns permission or quota errors, confirm subscription and role access, and check if Azure OpenAI access must be requested for your tenant.
* Confirm correct region availability for Azure OpenAI in your subscription.

## Links and references

* [Azure Portal](https://portal.azure.com)
* [Azure CLI documentation](https://learn.microsoft.com/cli/azure/)
* [Azure PowerShell](https://learn.microsoft.com/powershell/azure/)
* [Azure OpenAI overview and API docs](https://learn.microsoft.com/azure/cognitive-services/openai/overview)
* [Azure AI Studio (Foundry)](https://learn.microsoft.com/azure/ai-studio/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f28c5dfe-9fe8-486d-bc61-eade55096b1c/lesson/8bc24781-db55-408e-bf85-75aa2f948864" />
</CardGroup>


# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-OpenAI-Service/Module-Introduction/page

Introduction to provisioning Azure OpenAI resources, deploying generative models, and using the Azure AI Foundry portal for experimentation, model management, and governance

Getting Started with Azure OpenAI Service

[Azure OpenAI](https://learn.microsoft.com/azure/cognitive-services/openai/) pairs [OpenAI](https://openai.com/)'s advanced large language models (for example, [GPT](https://openai.com/research/gpt-4)) with Azure’s enterprise-grade security, governance, and compliance. This module introduces how to provision Azure OpenAI resources, deploy generative models, and use the Azure AI Foundry portal to run experiments and manage assets.

Why this matters: organizations use Azure OpenAI to accelerate development of conversational agents, summarization pipelines, and other generative AI solutions while maintaining control over data residency, access, and auditability.

Learning objectives

| Objective                   | What you’ll learn                                                | Where it applies                                                             |
| --------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Understand generative AI    | Distinguish generative AI from traditional ML and when to use it | Evaluating use cases such as chatbots, content generation, and summarization |
| Deploy and configure models | Create Azure OpenAI resources, pick models, and set up endpoints | Production and development deployments, SDK and REST usage                   |
| Use Azure AI Foundry portal | Run experiments, catalog models, and manage AI assets            | Experimentation, governance, and model lifecycle management                  |

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Learning Objectives&#x22; with a dark left panel and a light right area. It lists three numbered items: &#x22;Understanding Generative AI,&#x22; &#x22;Model deployment,&#x22; and &#x22;Azure AI Foundry portal,&#x22; each marked with a teal numbered icon." />
</Frame>

What to expect in this module

* A concise overview of generative AI concepts and how they differ from predictive or classification models.
* Step-by-step guidance for provisioning an Azure OpenAI resource, selecting a model (e.g., GPT family), and creating an API endpoint.
* Introduction to the Azure AI Foundry portal for experimentation, model versioning, and asset management.

Quick prerequisites

* An active Azure subscription and permission to create Cognitive Services/OpenAI resources.
* Basic familiarity with REST APIs or one of the Azure SDKs for your preferred language.
* Understanding of common prompts, token usage, and cost implications for large models.

<Callout icon="lightbulb">
  Before you begin: access to Azure OpenAI may require requesting access or enabling preview features depending on your subscription and region. Check the Azure OpenAI quickstart and subscription requirements before provisioning resources.
</Callout>

Next resources

* Azure OpenAI documentation and quickstarts: [https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?tabs=command-line](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?tabs=command-line)
* Azure AI overview and services: [https://learn.microsoft.com/azure/ai-services/](https://learn.microsoft.com/azure/ai-services/)
* OpenAI research (GPT family): [https://openai.com/research/gpt-4](https://openai.com/research/gpt-4)

By the end of this module you’ll be equipped to create an Azure OpenAI resource, deploy a model endpoint, and begin iterating on experiments using the Azure AI Foundry portal.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f28c5dfe-9fe8-486d-bc61-eade55096b1c/lesson/6645f0f0-f982-4353-b448-bd42b4fe5916" />
</CardGroup>
