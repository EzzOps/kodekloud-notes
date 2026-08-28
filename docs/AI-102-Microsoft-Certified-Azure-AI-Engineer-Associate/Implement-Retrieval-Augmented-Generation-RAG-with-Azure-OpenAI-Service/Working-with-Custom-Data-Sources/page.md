# Pseudocode for RAG-style request handling
def handle_query(user_query):
    # 1) Create embedding for query
    query_vector = embed(user_query)

    # 2) Retrieve top-k relevant docs from vector store
    docs = vector_store.search(query_vector, top_k=5)

    # 3) Rank or filter retrieved docs (optional)
    ranked_docs = rank_documents(docs, user_query)

    # 4) Build augmented prompt (user query + doc excerpts)
    augmented_prompt = assemble_prompt(user_query, ranked_docs)

    # 5) Call LLM with augmented prompt
    response = llm.generate(augmented_prompt)

    # 6) Return response + citations
    return format_with_citations(response, ranked_docs)
```

Practical considerations

* Embeddings: Use a consistent embedding model for both documents and queries to ensure meaningful similarity search.
* Chunking & context windows: Break long documents into chunks sized for the LLM’s context window; include overlap to preserve continuity.
* Relevance and hallucination mitigation: Rank and filter retrieved passages; include explicit citations so users can verify answers.
* Latency and cost: Retrieval adds a network/compute step — caching and efficient indexing help reduce latency and cost.
* Security & privacy: Be cautious about sensitive data in external knowledge bases; apply appropriate access controls and data redaction.

Further reading and references

* [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
* Vector databases and embeddings: consider providers like Pinecone, Milvus, or open-source options
* RAG pattern overview and research: search for Retrieval-Augmented Generation and hybrid retrieval + LLM systems

This architecture is widely used for search-augmented assistants, enterprise knowledge helpers, and any application that needs current, verifiable answers while still leveraging LLM reasoning and natural language capabilities.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/a4cc50fb-4b34-41eb-845e-d527ee8eb362/lesson/1636a0f7-ac8f-47af-8360-942f85da67ae" />
</CardGroup>


# Working with Custom Data Sources

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Implement-Retrieval-Augmented-Generation-RAG-with-Azure-OpenAI-Service/Working-with-Custom-Data-Sources/page

Guide to grounding Azure OpenAI with custom data sources using RAG, including chat playground, Blob Storage indexing, REST and SDK patterns, and a Python end to end example.

This guide explains how to ground Azure OpenAI responses with your own documents (Retrieval-Augmented Generation — RAG). It covers the Chat playground workflow for quickly testing data grounding, an end-to-end demo indexing a PDF from Azure Blob Storage, REST and SDK integration patterns, and a production-minded Python example.

Why ground models with your data?

* Prevent hallucinations by giving models verifiable context.
* Surface organization-specific knowledge not present in base models.
* Enable citations so answers include traceable sources.

## Quick workflow: Chat playground (no code required)

The Azure OpenAI Studio chat playground provides a central UI for composing prompts, selecting deployments, and adding data sources so the assistant can reference documents you control. Use this for rapid iteration before implementing code.

Steps to connect a data source from the Chat playground:

1. Open Chat playground in Azure OpenAI Studio.
2. Click Add your data.
3. Choose an existing data source (for example, Azure AI Search index) or create one from the dialog.
4. After adding, a new chat session is created and grounded in that data — the model can integrate content from your documents and cite sources.

<Frame>
  <img alt="A slide showing the &#x22;Chat playground&#x22; interface (model selection, prompt area, and an &#x22;Add your data&#x22; option) on the left. On the right is a vertical flowchart explaining steps to connect a data source and start a new chat session so the AI can reference your data." />
</Frame>

This lets you move quickly from prototype to a deployment-ready configuration.

## Demo: Indexing a PDF from Azure Blob Storage

Scenario: You have Project\_Orion\_Confidential.pdf stored in Blob Storage and want the assistant to answer questions using the PDF content.

<Frame>
  <img alt="A screenshot of an Azure Storage container named &#x22;rag&#x22; showing one blob file, &#x22;Project_Orion_Confidential.pdf,&#x22; with a modified date of 4/20/2025 and access tier &#x22;Hot (Inferred).&#x22; The left pane shows container navigation options like Overview, Diagnose and solve problems, Access Control (IAM), and Settings." />
</Frame>

Before ingestion, the assistant will answer from general model knowledge. To enforce that responses only come from the indexed document content, set a system message telling the model not to guess. Example system instruction:
"Answer only if you find relevant content in the data source. Do not guess. If unsure, say: 'I don't have information on that topic.'"

After adding that system message, queries about Project Orion will return "I don't have information..." until you ingest and index the PDF.

<Frame>
  <img alt="A screenshot of the Azure AI Foundry / Azure OpenAI Service &#x22;Chat playground&#x22; interface, showing the setup/deployment panel on the left and a chat history pane on the right with text about &#x22;Project Orion.&#x22; The page includes controls for deployment selection, prompt/instructions, and a text input box for user queries." />
</Frame>

### Add the Blob Storage data source

1. In the Add data dialog choose Azure Blob Storage and point to the container with your file.
2. Select an Azure Cognitive Search resource — this service builds the index and returns semantically ranked documents to Azure OpenAI.
3. Provide an index name (for example, rag) and configure authentication (API key or managed identity).
4. Save and let the platform ingest and index the document. A status indicator shows ingestion progress; once complete, the chat session can return citations from the indexed file.

<Frame>
  <img alt="A screenshot of an &#x22;Add data&#x22; dialog in Azure AI where the user selects an Azure Blob Storage data source, subscription, storage container, Azure AI Search resource, index name, and indexer schedule. The dialog overlays a &#x22;Chat playground&#x22; interface in the background." />
</Frame>

Select your search resource, choose authentication, and save. The platform handles ingestion and indexing; once indexing completes the chat assistant can cite document chunks when answering.

<Frame>
  <img alt="A screenshot of an &#x22;Add data&#x22; dialog in the Azure portal showing the Data connection step with &#x22;Azure resource authentication type&#x22; options, the &#x22;API key&#x22; option selected and a &#x22;Validating&#x22; status. The dialog overlays a &#x22;Chat playground&#x22; setup page in the background." />
</Frame>

Once indexed, asking about Project Orion returns answers that include citations (for example: "Project Orion Confidential — Part One") and specific content such as lead researcher names.

<Frame>
  <img alt="A screenshot of the Azure OpenAI &#x22;Chat playground&#x22; interface with the left navigation menu and a central chat pane. The chat shows a user asking about Project Orion and the assistant replying with a list of three lead researchers." />
</Frame>

## REST integration: key considerations

* Each REST request to the Azure OpenAI endpoint for RAG-enabled interactions should include a data\_sources array. This tells the model where to look for external content (for example an Azure Cognitive Search index).
* Authentication for the data source is managed through the search resource (or other data service), not the Azure OpenAI resource. Ensure the access method you pick (API key or managed identity) is configured correctly and the identity has appropriate permissions.

<Frame>
  <img alt="A presentation slide titled &#x22;Using Azure OpenAI REST API&#x22; with a &#x22;Key Considerations&#x22; header. It lists two points: every API call must include data source values alongside the messages array, and data-source authentication is linked to your search resource, not the Azure OpenAI resource." />
</Frame>

Example RAG-enabled REST request body (replace placeholders with your values):

```json theme={null}
POST https://<your_openai_endpoint>/openai/deployments/<deployment>/chat/completions?api-version=<api_version>
Content-Type: application/json
api-key: <your_api_key>

{
  "data_sources": [
    {
      "type": "azure_search",
      "parameters": {
        "endpoint": "https://<your_search_endpoint>",
        "index_name": "<your_search_index>",
        "authentication": {
          "type": "system_assigned_managed_identity"
        },
        "semantic_configuration": "default",
        "query_type": "simple",
        "top_n_documents": 5,
        "strictness": 3,
        "role_information": "Answer only if you find relevant content in the data source. Do not guess. If unsure, say: \"I don't have information on that topic.\""
      }
    }
  ],
  "messages": [
    {
      "role": "system",
      "content": "Answer only if you find relevant content in the data source. Do not guess. If unsure, say: \"I don't have information on that topic.\""
    },
    {
      "role": "user",
      "content": "Who are the lead researchers for Project Orion?"
    }
  ],
  "past_messages": 10,
  "temperature": 0.0,
  "max_tokens": 800
}
```

## SDK overview and typical flow

Azure OpenAI SDKs (used with Azure OpenAI deployments) simplify integration in languages like Python and C#. Even when using the SDK you still supply a messages array and a data source object to indicate where to find ground-truth content.

Typical steps:

1. Install the Azure OpenAI/OpenAI SDK for your language.
2. Create a client (API key or identity-based auth).
3. Define chat messages (system + user).
4. Attach a data\_sources object (endpoint, index, authentication).
5. Send the request and process the response.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Using Azure OpenAI SDK&#x22; with an &#x22;Overview&#x22; button and two text boxes stating that the SDKs support integration with C# and Python and follow a consistent structure across languages. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

Supported data sources (SDK)

* Azure AI Search — primary index for grounding (GA).
* Azure Cosmos DB for MongoDB vCore — document-level grounding (preview).
* More connectors are being added — check Azure release notes for updates.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Using Azure OpenAI SDK&#x22; listing supported data sources: &#x22;Azure AI Search&#x22; and &#x22;Azure Cosmos DB for MongoDB vCore.&#x22; The slide also shows a small &#x22;© Copyright KodeKloud&#x22; note in the corner." />
</Frame>

Table: Common data-source options

| Resource Type                   | Typical Use Case                                    | Availability                  |
| ------------------------------- | --------------------------------------------------- | ----------------------------- |
| Azure AI Search                 | Semantic indexes for document retrieval and ranking | Generally available           |
| Azure Blob Storage              | Raw documents (PDF, DOCX) used by search indexer    | Works with search indexer     |
| Azure Cosmos DB (MongoDB vCore) | Document-level grounding (preview)                  | Preview — check release notes |

Tip: pick a connector that matches where your documents live and your required retrieval semantics.

## When to let the service retrieve vs. app-side retrieval

Two common patterns:

* Service-side retrieval: include data\_sources in the API call and let Azure OpenAI + Azure Cognitive Search handle retrieval + generation. Simpler; less client code.
* App-side retrieval: query Cognitive Search from your app, select top-K docs, and include the content in messages. Offers more control over retrieval, filtering, and privacy.

<Callout icon="lightbulb">
  When integrating data, choose between (a) letting the OpenAI service call your search index via the data\_sources parameter in the API, or (b) performing retrieval in your application (query search), then sending the retrieved content as context. Both approaches are valid—pick one that meets your latency, cost, and security requirements.
</Callout>

<Callout icon="warning">
  Authentication for data sources is tied to the search/data resource, not the Azure OpenAI resource. Ensure the identity (API key or managed identity) you configure has appropriate permissions to access the search index or storage.
</Callout>

## Example: Python end-to-end (Azure Cognitive Search + Azure OpenAI)

This simplified Python example shows one common pattern:

* Query Azure Cognitive Search to get top-K documents.
* Format these documents into a context.
* Call Azure OpenAI chat completions with messages containing the context.
* Print the assistant response.

Replace placeholders with your environment values and use secure credential management in production.

```python theme={null}
