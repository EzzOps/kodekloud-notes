# Get model metadata
model_info = client.get_model("gpt-4o")
print(model_info)

# Create a chat completion using a deployed model
response = client.chat.completions.create(
    deployment_id="my-custom-model",  # the deployment name you created
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short welcome message for new users."}
    ],
)

print(response.choices[0].message.content)
```

Tips for integration

* Use the Playground to iterate on prompts and system messages before embedding them in production code.
* Respect rate limits and scale your deployment capacity based on expected traffic.
* Store and rotate keys securely (e.g., Azure Key Vault or environment variables).

Quick reference: deployment methods and use cases

|         Deployment method | Use case                                                | Example / Note                                   |
| ------------------------: | ------------------------------------------------------- | ------------------------------------------------ |
| Azure Portal (AI Foundry) | Interactive deployments, fine-tuning, and quick testing | Use for experimentation and Playground testing   |
|                 Azure CLI | Automated, repeatable deployments across environments   | Scripted provisioning and CI/CD integration      |
|   SDKs (Python, JS, etc.) | Application integration and runtime calls               | Use azure-ai-openai package for managed clients  |
|    Fine-tuning via portal | Custom behavior for domain-specific tasks               | Provide labeled training and validation datasets |

Recap and next steps

* Verify subscription and regional quotas before deploying larger models to avoid interruptions.
* Use the Azure Portal for interactive deployment, fine-tuning, and Playground testing.
* Automate deployments with Azure CLI to make provisioning repeatable across environments.
* Integrate deployed models into applications using SDKs like azure-ai-openai and follow best practices for prompt design and security.

Links and references

* [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
* [azure-ai-openai (PyPI)](https://pypi.org/project/azure-ai-openai/)
* [Azure CLI documentation](https://learn.microsoft.com/cli/azure/)
* [Azure quotas and limits](https://learn.microsoft.com/azure/azure-subscriptions/manage-subscription-services-resources)

Now that you know how to deploy models with Azure AI Foundry, continue by exploring prompt engineering strategies and experiment in the Playground to optimize responses for your application.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f28c5dfe-9fe8-486d-bc61-eade55096b1c/lesson/e0620085-ae74-4bd1-b96c-3a9d220bc5d3)


# Deploying an Azure OpenAI Resource

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-OpenAI-Service/Deploying-an-Azure-OpenAI-Resource/page

Guide for creating and managing an Azure OpenAI resource via the Azure portal or CLI, including post deployment keys, endpoints, and troubleshooting

This guide shows two common ways to create an Azure OpenAI resource:

* Portal deployment — a guided, beginner-friendly UI flow.
* CLI deployment — scriptable and repeatable for automation and CI/CD.

Both approaches provision an Azure Cognitive Services account of kind `OpenAI` (often referred to as an Azure OpenAI resource). After provisioning you’ll obtain the resource endpoint and keys to call the Azure OpenAI APIs or connect the resource to Azure AI Foundry (Azure AI Studio).

## Quick comparison

| Deployment method | Best for                              | Pros                                                                    | Cons                                                |
| ----------------- | ------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------- |
| Portal (UI)       | Beginners, one-off setups             | Guided validation, visual configuration, easy access to AI Studio links | Manual steps, less repeatable                       |
| CLI / PowerShell  | Automation, CI/CD, reproducible infra | Scriptable, repeatable, integrates with pipelines                       | Requires CLI authentication and scripting knowledge |

## Portal deployment (guided)

Steps — high level:

1. Open the Azure portal: [https://portal.azure.com](https://portal.azure.com)
2. Select your Subscription.
3. Choose or create a Resource Group.
4. Provide instance details: Resource name, Region, and Pricing tier.
5. Complete validation and create the resource.

This guided workflow validates required fields as you fill them, making it ideal for first-time users.

<Frame>
  <img alt="A slide titled &#x22;Deploying an Azure OpenAI Resource&#x22; that outlines portal deployment steps. It shows Step 1: &#x22;Open Azure Portal&#x22; and Step 2: &#x22;Select Subscription,&#x22; &#x22;Select Resource Group,&#x22; and &#x22;Select Instance Details,&#x22; with a &#x22;Portal Deployment&#x22; panel and an icon." />
</Frame>

### Creating a resource in the portal — example flow

When you create a resource you’ll typically:

* Choose (or create) a resource group, e.g., `rg-ai102-oai-eus`.
* Provide a resource name, e.g., `ai102-aoai-eus`.
* Select a region (for example, `East US`) and choose the Pricing tier (commonly `S0`).

If required fields are missing, the portal surfaces validation errors that you must resolve before creating the resource.

<Frame>
  <img alt="A screenshot of an Azure service creation form showing Project Details and Instance Details — Subscription &#x22;Kodekloud Labs&#x22;, Resource group &#x22;(New) rg-ai102-oai-eus&#x22;, Region set to &#x22;East US&#x22; and a partially entered Name. The Pricing tier field is empty and highlighted with a validation error reading &#x22;The value must not be empty.&#x22;" />
</Frame>

After clicking Create:

* Deployment may take several minutes.
* When complete, click Go to resource.
* From the resource overview you can copy the keys and endpoint, and open Azure AI Foundry / AI Studio for model experiments and deployments.

Example resource endpoint (found on the resource overview):

```text theme={null}
https://ai102-aoai-eus.openai.azure.com/
```

## CLI deployment (automated)

Use Azure CLI or Azure PowerShell when you need automation or pipeline integration. Before creating resources, sign in and ensure the correct subscription is selected:

```bash theme={null}
