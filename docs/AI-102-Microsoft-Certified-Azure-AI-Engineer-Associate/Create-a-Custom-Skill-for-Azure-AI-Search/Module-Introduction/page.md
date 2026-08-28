# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Create-a-Custom-Skill-for-Azure-AI-Search/Module-Introduction/page

How to design, implement, host, and register custom HTTP JSON skills to extend Azure AI Search enrichment pipelines, covering API contract, hosting, authentication, and deployment best practices.

Creating a custom skill for Azure AI Search

In this lesson you will learn how to design, implement, host, and register a custom skill to extend Azure AI Search's enrichment pipeline. We cover the custom skill contract (HTTP JSON input/output), best practices for hosting as a web API, integration into a skillset and indexer, and deployment considerations such as authentication and latency so your skill runs reliably as part of the indexing workflow.

<Frame>
  <img alt="A dark-themed presentation slide from KodeKloud with their logo at the top. The title reads &#x22;Creating a Custom Skill for Azure AI Search.&#x22;" />
</Frame>

Below are the learning objectives for this module. Each objective maps to practical outcomes and examples to help you implement a production-ready custom skill.

| Learning objective                               |                                                                                      What you'll learn | Example outcome                                                                           |
| ------------------------------------------------ | -----------------------------------------------------------------------------------------------------: | ----------------------------------------------------------------------------------------- |
| Role of custom skills in the enrichment pipeline | How custom skills complement built-in skills to perform specialized content processing during indexing | Enrich documents with domain-specific metadata that built-in skills cannot extract        |
| Custom skill interface design                    |     Input/output JSON contract, required fields, and shape of the request/response for Azure AI Search | Create an HTTP endpoint that accepts Azure enrichment JSON and returns transformed values |
| Develop, host, and register a custom skill       |          Implement skill logic, host as a secure web API, and register the endpoint in Azure AI Search | Deploy a Dockerized API and add it to a skillset using the Azure portal or REST API       |
| Configure and deploy in a skillset               |                  Add the custom skill to a skillset and ensure it runs as part of the indexer pipeline | Index enriched content automatically with the configured skillset and indexer             |

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; with four numbered points. The points cover the role of custom skills in the enrichment pipeline, how custom skill interfaces process and transform data, developing and integrating a custom skill using Azure AI Search, and configuring/deploying a custom skill within an AI Search skillset." />
</Frame>

<Callout icon="lightbulb">
  Custom skills are HTTP endpoints that accept and return JSON payloads following Azure AI Search's enrichment contract. When building a custom skill, pay attention to the API contract (input/output schema), authentication (API key, Azure AD), performance (minimize latency), error handling (graceful failures and retry semantics), and secure hosting. These considerations ensure the custom skill integrates reliably into the enrichment pipeline and scales with your indexing workload.
</Callout>

## Links and references

* [Azure Cognitive Search documentation](https://learn.microsoft.com/azure/search/)
* [Create a custom skill for Azure Cognitive Search — guidance and examples](https://learn.microsoft.com/azure/search/cognitive-search-custom-skill-interface)
* [Designing HTTP APIs: best practices for reliability and performance](https://docs.microsoft.com/azure/architecture/best-practices/api-design)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/1413da7e-948c-4865-8347-5710a35851a4/lesson/cf4db337-2d30-4590-8013-d0ef54b4e0fb" />
</CardGroup>
