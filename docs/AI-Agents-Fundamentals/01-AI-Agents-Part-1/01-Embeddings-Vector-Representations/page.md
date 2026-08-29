# DefaultAzureCredential uses Managed Identity when running in Azure
credential = DefaultAzureCredential()

# Replace with your Key Vault URL
vault_url = "https://<your-key-vault-name>.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve the secret (API key) by name (returns latest version if version not specified)
secret = client.get_secret("azure-ai-api-key")
api_key = secret.value

# Call the Azure AI endpoint using the retrieved key
endpoint = "https://<your-endpoint>/openai/deployments/<deployment>/completions?api-version=2023-05-15"
headers = {"api-key": api_key, "Content-Type": "application/json"}
payload = {"prompt": "Hello from managed identity!", "max_tokens": 16}

response = requests.post(endpoint, headers=headers, json=payload)
print(response.status_code, response.text)
```

Notes on implementation

* Grant the Managed Identity the least privilege necessary: use Azure RBAC or Key Vault access policies to grant the "get" permission for secrets.
* Use Key Vault secret versioning to track rotations; unless you specify a version, retrieving by name returns the current secret.
* Test rotation workflows: after rotating a secret, verify the app can read the updated secret before disabling or deleting older credentials.

<Frame>
  <img alt="The image is a diagram titled &#x22;Securing Azure AI Services.&#x22; It shows an app using a Service Principal to retrieve a key from a key vault and then using that key to access Azure AI services in the cloud." />
</Frame>

Because the application fetches the current secret from Key Vault at runtime, you can rotate keys centrally without changing application code. This reduces downtime risk and limits the window in which an exposed credential is valid.

<Callout icon="warning">
  Never paste production keys or secrets in public repositories or documentation. Avoid logging secrets in plaintext. Use Key Vault and Managed Identity to minimize secret exposure.
</Callout>

Further reading and references

* [Azure Key Vault documentation](https://learn.microsoft.com/azure/key-vault/)
* [Managed identities for Azure resources](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)
* [Azure security documentation](https://learn.microsoft.com/security/azure-security)
* Microsoft Azure Security Technologies (AZ-500) course (example): [https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500](https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500)

Implementing these practices will help secure your Azure AI deployments by minimizing secret exposure, simplifying rotation, and enforcing least privilege access.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/981568f6-848e-45c2-ae00-083b3975ecb5/lesson/a27b7614-1d4c-483c-b876-287e77bb3bf1" />
</CardGroup>


# Embeddings Vector Representations

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-1/Embeddings-Vector-Representations/page

How text embeddings map meaning to vectors enabling semantic search, document retrieval, and LLM grounding for robust paraphrase-insensitive search and recommendations

Embeddings convert text meaning into numeric vectors so machines can compare semantics rather than surface words. Instead of indexing raw keywords, embedding-based systems map words, phrases, and documents into a high-dimensional space where semantically similar items lie close together. This makes tasks like semantic search, clustering, and recommendation far more robust to paraphrase and synonyms.

For example, the phrases "employee vacation policy" and "staff time-off guidelines" use different wording but convey the same concept. An embedding model encodes both into vectors that occupy nearby positions in the embedding space, reflecting their semantic similarity.

An embedding model accepts text and returns a numeric vector (often with hundreds or thousands of dimensions — e.g., 1,536). Similar meaning produces similar numeric patterns; distance or similarity measures such as cosine similarity or dot product are used to identify related items. Words like "vacation" and "holiday" typically produce embeddings that are mathematically close.

When an employee asks, "Can I wear jeans to work?"

<Frame>
  <img alt="A hand-drawn schematic showing an LLM (labeled &#x22;Gemini 2.5 Pro&#x22;) using a large context window to retrieve relevant files from a tech company's 500 GB document store. Below that is a depiction of embeddings — text mapped to numerical vectors in a semantic similarity space (noted as 1,536 dimensions)." />
</Frame>

The typical retrieval pipeline works like this:

1. User query -> embed: Convert the user's question into an embedding vector.
2. Vector search: Compare the query embedding against stored document embeddings in a vector database (vector store) to find nearest neighbors.
3. Context assembly: Retrieve the top matching documents (e.g., HR policies, dress-code documents).
4. LLM grounding: Provide those retrieved documents as context to a large language model so it can generate a grounded answer — returning responses based on meaning and relevant documents rather than only keyword matches.

Practical benefits for an organization (e.g., TechCorp):

* Semantic search across a large document corpus (e.g., 500 GB) to find intent-matching documents.
* Robustness to paraphrase and synonyms: employees get correct answers even if they ask questions differently.
* Better relevance ranking by combining vector similarity with metadata and filters (date, author, department).

Similarity metrics and when to use them:

| Metric             | Use Case                                      | Notes                                                             |
| ------------------ | --------------------------------------------- | ----------------------------------------------------------------- |
| Cosine similarity  | General semantic similarity                   | Robust to vector magnitude; widely used for embeddings            |
| Dot product        | When using models that use attention scores   | Scales with vector norms; useful when magnitude encodes relevance |
| Euclidean distance | Clustering and nearest neighbor visualization | Sensitive to scaling; less common for normalized embeddings       |

<Callout icon="lightbulb">
  Normalize embeddings (L2 normalization) if you plan to use cosine similarity — this simplifies comparisons and often improves search quality. Combine vector similarity with metadata filters (time, department) to reduce false positives.
</Callout>

A concise example flow for the question "Can I wear jeans to work?":

* Convert the question to an embedding.
* Query the vector store to retrieve top N documents about attire, dress code, and HR policies.
* Provide those documents as context (prompting context window) to the LLM so it can answer with citations or specific policy language.
* Optionally, re-rank or filter results by document freshness or source trustworthiness.

Links and references

* [Introduction to Embeddings — Google Developers](https://developers.google.com/machine-learning/glossary/embedding)
* [OpenAI — Embeddings](https://platform.openai.com/docs/guides/embeddings)
* [Vector databases and nearest-neighbor search — Faiss](https://github.com/facebookresearch/faiss)

Further reading

* Semantic search: architectures that combine embeddings + vector DB + LLMs.
* Vector database options: Pinecone, Milvus, Weaviate, and Faiss.
* Prompting strategies: how to assemble retrieved documents into LLM prompts for grounded answers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/2868c859-8bc4-4b36-be80-9482628d94fb" />
</CardGroup>
