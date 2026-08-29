# Deploying Generative AI Models

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-OpenAI-Service/Deploying-Generative-AI-Models/page

Guide to deploying and integrating generative AI models with Azure AI Foundry covering quota checks, portal and CLI deployments including fine tuning, and SDK-based application integration.

This guide shows a practical, end-to-end approach to deploying generative AI models with Azure AI Foundry (Azure OpenAI). You'll learn how to check quotas, automate deployments with Azure CLI, deploy from the AI Foundry portal (including fine-tuning), and call your deployed model from an application using the official SDK.

Overview

* Use Azure AI Foundry to simplify model hosting, scaling, and operational management.
* Choose between deploying a base model or creating a fine-tuned model using labeled data.
* Automate repeatable deployments via Azure CLI and integrate models into apps via SDKs.

Meet Alex, an AI engineer who needs a production-ready generative model for a customer-facing application. He chooses Azure AI Foundry because it abstracts infrastructure and provides portal, CLI, and SDK tooling for deployment, testing, and integration.

Before you deploy: check quotas and capacity
Quota in Azure determines how many deployments and what VM SKUs/capacity you can run in a region. Deploying GPT-4-class models (for example, GPT-4-32K) typically requires higher quota than lighter models. Check quotas in the Azure Portal and request increases proactively to avoid deployment failures or delays.

<Callout icon="lightbulb">
  Check your subscription and regional quotas (and request increases if needed) before attempting to deploy larger models. Quota affects both the number of concurrent deployments and the capacity/VM sizes available.
</Callout>

Automating deployments with Azure CLI
For repeatable provisioning across environments (dev, staging, prod), use the Azure CLI. Automation is helpful when deploying multiple instances or managing infrastructure-as-code workflows.

Example: create a GPT-4 32K deployment
Modify resource names, model version, capacity, or SKU to match your subscription and quota.

```bash theme={null}
az cognitiveservices account deployment create \
  --resource-group MyResourceGroup \
  --name MyAIResource \
  --deployment-name my-custom-model \
  --model-name gpt-4-32k \
  --model-version "0613" \
  --model-format OpenAI \
  --sku Premium \
  --capacity 5
```

<Frame>
  <img alt="A presentation slide titled &#x22;Deploying a Model in Azure AI Foundry.&#x22; It lists three points: deploy multiple instances based on quota limits, view quota details in the portal, and deploy models via the Azure CLI for automation." />
</Frame>

Deploying from the AI Foundry Portal
The portal supports both direct deployment of base models and creating fine-tuned variants:

* Deploy base model: open the model page, click Deploy, choose deployment options, and confirm. You can edit the deployment name or accept the default.
* Fine-tune: use the portal dialog to upload training and validation datasets, set the tuning method and hyperparameters, and create a fine-tuned model.

The portal also includes quick testing via the Playground and provides SDK code snippets for different languages to reduce context switching.

<Frame>
  <img alt="A dark-themed Azure OpenAI Service web UI screenshot showing a &#x22;Create a fine-tuned model&#x22; dialog for gpt-4o with fields for Method, Base model, training/validation data, suffix, seed and hyperparameters. The background shows the model catalog and model versions on the left and center panels." />
</Frame>

After you click Deploy and the deployment completes, open the model in the Playground to test chat completions, prompt designs, or other interactions. The portal also surfaces client SDK examples for quick integration.

<Frame>
  <img alt="A dark-themed dashboard screenshot showing the &#x22;gpt-4o&#x22; model page with a blue &#x22;Deploy&#x22; button, descriptive text, model versions table, and a &#x22;Quick facts&#x22; panel on the right." />
</Frame>

Calling your deployed model from an application
Once your model is deployed and validated, integrate it into your app. Below is a concise Python example using the official azure-ai-openai package. Replace endpoint, key, and deployment\_id with your values.

Install the package:

```bash theme={null}
pip install azure-ai-openai
```

Python example:

```python theme={null}
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential
import os

endpoint = "https://ai102-aoai-eus.openai.azure.com/"
key = os.environ["AZURE_OPENAI_KEY"]  # set your Azure OpenAI key in env

client = OpenAIClient(endpoint, AzureKeyCredential(key))
