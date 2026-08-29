# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Implementing-an-Intelligent-Search-Solution/Module-Introduction/page

Guide to building end to end Azure AI Search solutions by provisioning services, defining indexes, adding custom enrichment skills, and storing enriched content for advanced queries and analytics

Implementing an intelligent search solution with Azure AI Search (formerly Azure Cognitive Search).

<Frame>
  <img alt="A dark-blue presentation slide from KodeKloud with the logo at the top and the title &#x22;Implementing an Intelligent Search Solution&#x22; centered. A small copyright notice appears in the lower-left corner." />
</Frame>

This module dives into creating an end-to-end intelligent search pipeline using Azure AI Search. You will learn how to provision and configure search services, enrich content with custom skills, and persist enriched results in a knowledge store for advanced querying and analytics.

> **lightbulb** Before you begin, ensure you have an Azure subscription and sufficient permissions to create resource groups, Search services, and storage resources. For development scenarios, consider using a separate resource group to manage costs.

What we'll cover

* Provisioning and configuring an Azure AI Search service
* Defining indexes and connecting data sources for ingestion
* Implementing and integrating custom skills (Azure Functions or web APIs) into enrichment pipelines
* Building a knowledge store to retain and query enriched data

Goals at a glance

| Goal                            | Outcome                                                                     | Key steps / examples                                                                                                      |
| ------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Set up Azure AI Search          | A running Search service with an index ready to ingest data                 | Provision Search in Azure portal or via CLI; create an index and map fields; connect blob, Cosmos DB, or SQL data sources |
| Build & integrate custom skills | Enrich content during indexing (e.g., OCR, entity recognition, translation) | Implement Azure Functions or custom web APIs; register skills in a skillset; add to indexer pipeline                      |
| Create a knowledge store        | Structured repository of enriched content for analytics and querying        | Configure a knowledge store (Azure Storage or Cosmos DB); route enriched documents to the store                           |

Recommended reading and references

* Azure AI Search overview: [https://learn.microsoft.com/azure/search/](https://learn.microsoft.com/azure/search/)
* Create and manage indexes: [https://learn.microsoft.com/azure/search/search-create-index-portal](https://learn.microsoft.com/azure/search/search-create-index-portal)
* Skillsets and cognitive enrichment: [https://learn.microsoft.com/azure/search/cognitive-search-concept-intro](https://learn.microsoft.com/azure/search/cognitive-search-concept-intro)

This module prepares you to design, implement, and operate an intelligent search solution that supports advanced content enrichment and delivers rich query experiences for applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/668a922e-e573-4bcc-8a97-443ae22d225f/lesson/6b07f15a-b31e-4116-b073-c14726d3cf69)
