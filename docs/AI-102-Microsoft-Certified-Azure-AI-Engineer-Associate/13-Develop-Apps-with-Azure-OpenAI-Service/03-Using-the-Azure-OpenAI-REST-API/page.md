# app.py
from flask import Flask, request, render_template, jsonify
import os

from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Read credentials from environment variables for safety
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

if not (AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT):
    raise ValueError("Set AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT environment variables.")

# Initialize the Azure OpenAI client
credential = AzureKeyCredential(AZURE_OPENAI_KEY)
client = OpenAIClient(endpoint=AZURE_OPENAI_ENDPOINT, credential=credential)

@app.route('/')
def index():
    # Serve a simple UI (index.html) that posts JSON to /chat
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "Please send a non-empty message."}), 400

    # Prepare messages and parameters for the chat completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]

    # Call the Azure OpenAI chat completions API (synchronous)
    response = client.get_chat_completions(
        deployment_id=DEPLOYMENT_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    # Extract the assistant reply
    reply = response.choices[0].message.content.strip()
    return jsonify({"reply": reply})

if __name__ == '__main__':
    # For local development only. In production use a WSGI server like Gunicorn or uWSGI.
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Explanation of the key parts

* Initialization: create an OpenAIClient using your Azure endpoint and AzureKeyCredential.
* Messages: construct a list of chat messages with roles ("system", "user", optionally "assistant").
* Request: call client.get\_chat\_completions with your deployment\_id and generation parameters (temperature, max\_tokens).
* Response: extract the assistant text from response.choices\[0].message.content (strip whitespace).

Example response JSON

```json theme={null}
{
  "reply": "Hello! I'm a virtual assistant ready to help. What would you like to do today?"
}
```

Local DevTools / network details (example)

| Property                | Example                                                  |
| ----------------------- | -------------------------------------------------------- |
| Request URL             | [http://127.0.0.1:5000/chat](http://127.0.0.1:5000/chat) |
| Request Method          | POST                                                     |
| Status Code             | 200 OK                                                   |
| Content-Type (response) | application/json                                         |
| Server                  | Werkzeug/3.1.3 Python/3.9.13                             |

Response headers (example)

| Header         | Value                        |
| -------------- | ---------------------------- |
| Connection     | close                        |
| Content-Length | 171                          |
| Content-Type   | application/json             |
| Server         | Werkzeug/3.1.3 Python/3.9.13 |

Request headers (example)

| Header       | Value                                          |
| ------------ | ---------------------------------------------- |
| Accept       | */*                                            |
| Content-Type | application/json                               |
| Host         | 127.0.0.1:5000                                 |
| Origin       | [http://127.0.0.1:5000](http://127.0.0.1:5000) |

Next steps / integrations

* Add authentication and authorization for your Flask endpoints to protect access.
* Integrate with internal knowledge sources or a vector database to implement retrieval-augmented generation (RAG) for context-aware answers. See an intro to RAG here: [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag).
* If your app needs high concurrency, switch to the async client or run the Flask app behind an async-friendly server.
* Consult Azure OpenAI docs for deployment, scaling, and best practices: [https://learn.microsoft.com/azure/cognitive-services/openai/](https://learn.microsoft.com/azure/cognitive-services/openai/)

Summary
Using a language-specific SDK (like the Azure OpenAI Python SDK) keeps your integration concise and consistent. The SDK handles authentication, request/response serialization, and exposes parameters to tune generation behavior—letting you focus on building features like a Flask-based chatbot rather than the underlying REST plumbing.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/555c7620-8f25-4f2d-b1e8-1aa3cca1a55b/lesson/6431bef8-14c5-42e1-8a06-b74d7b5e4251)


# Using the Azure OpenAI REST API

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-Apps-with-Azure-OpenAI-Service/Using-the-Azure-OpenAI-REST-API/page

Guide to using Azure OpenAI REST API endpoints—completions, embeddings, chat completions—with example request and response payloads, deployment details, and curl and Postman tips.

This lesson walks through the three primary Azure OpenAI REST API endpoints — completions, embeddings, and chat completions — showing typical request/response formats, key parameters, and practical tips for calling the APIs from curl or Postman.

Quick overview:

* Completion endpoint: generate text continuations from a prompt.
* Embeddings endpoint: convert text into numeric vectors for semantic tasks (search, clustering, similarity).
* Chat completion endpoint: structured multi-turn conversational interface using role-based messages.

Endpoint summary

|         Endpoint | Purpose                                            | Typical Request URL                                                                               |
| ---------------: | -------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
|      Completions | Generate single-turn text continuations            | https\://\<your-endpoint>.openai.azure.com/openai/deployments/\<deployment-name>/completions      |
|       Embeddings | Produce vector embeddings for semantic tasks       | https\://\<your-endpoint>.openai.azure.com/openai/deployments/\<deployment-name>/embeddings       |
| Chat completions | Multi-turn conversational responses using messages | https\://\<your-endpoint>.openai.azure.com/openai/deployments/\<deployment-name>/chat/completions |

***

## Completion endpoint

Use the completions endpoint to generate text continuations from a prompt. Replace \<your-endpoint> and \<deployment-name> with values from your Azure AI Foundry deployment.

URL:

```text theme={null}
https://<your-endpoint>.openai.azure.com/openai/deployments/<deployment-name>/completions
```

Request body example:

```json theme={null}
{
  "prompt": "Suggest a creative title for a blog about cloud security.",
  "max_tokens": 10
}
```

Response example:

```json theme={null}
{
  "id": "5678...",
  "object": "text_completion",
  "created": 1679001781,
  "model": "gpt-4",
  "choices": [
    {
      "text": "Shielding the Cloud: Security in the Digital Era",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ]
}
```

Key notes:

* The generated text is in `choices[0].text`.
* `max_tokens` caps the response length. Tokens are the billing and length units used by the models.
* You can control generation randomness and style with parameters like `temperature` and `top_p`.

***

## Embeddings endpoint

Use embeddings to convert text into numeric vectors. Store and compare these vectors (e.g., cosine similarity) for semantic search, recommendation, or clustering.

URL:

```text theme={null}
https://<your-endpoint>.openai.azure.com/openai/deployments/<deployment-name>/embeddings
```

Request body example:

```json theme={null}
{
  "input": "Cybersecurity is essential for protecting sensitive business data."
}
```

Response example:

```json theme={null}
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.02837654923,
        -0.0146752345,
        0.0456789345
      ],
      "index": 0
    }
  ],
  "model": "text-embedding-ada-002"
}
```

Key notes:

* `data[0].embedding` is the numeric vector representation.
* Embeddings are commonly stored in vector databases (e.g., Pinecone, FAISS, Azure Cognitive Search) for fast similarity search.

***

## Chat completion endpoint

Chat completions support multi-turn conversational flows using role-based messages (`system`, `user`, `assistant`).

URL:

```text theme={null}
https://<your-endpoint>.openai.azure.com/openai/deployments/<deployment-name>/chat/completions
```

Request body example:

```json theme={null}
{
  "messages": [
    { "role": "system", "content": "You are a helpful assistant for IT professionals." },
    { "role": "user", "content": "What are the key benefits of zero-trust security?" }
  ]
}
```

Response example:

```json theme={null}
{
  "id": "unique_id",
  "object": "chat.completion",
  "created": 1679001781,
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 80,
    "completion_tokens": 120,
    "total_tokens": 200
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Zero-trust security ensures continuous verification, limits access to only authorized users, and minimizes risk by enforcing strict identity authentication and least-privilege access."
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

Key notes:

* Assistant replies appear in `choices[0].message.content`.
* The `usage` object shows token counts for prompt, completion, and total (useful for cost tracking).
* Chat completions are optimized for multi-turn interactions; maintain the `messages` array to preserve conversation context.

> **lightbulb** Not all models support every API type (completions, embeddings, chat). Check the model catalog in your Azure AI Foundry portal to confirm which models support which inference tasks before calling an endpoint.

***

## Inspecting models and deployments in Azure AI Foundry

Review the model catalog in Azure AI Foundry to pick the right model for your task (for example, embeddings vs chat). Filter by inference task to narrow the available models.

<Frame>
  <img alt="A web dashboard for choosing AI models, showing announcement cards at the top and a grid of model tiles (e.g., o4-mini, gpt-4.1, gpt-4o-mini). A filter menu for inference tasks is open on the left with &#x22;Audio generation&#x22; checked." />
</Frame>

After deploying a model, open the deployment to view its REST target URI and configuration details (deployment name, model version, and state).

<Frame>
  <img alt="A screenshot of a &#x22;Model deployments&#x22; admin page showing a single deployed model entry for &#x22;gpt-4o&#x22; (model version 2024-11-20) with state &#x22;Succeeded&#x22; and a retirement date of Dec 20, 2025. A cursor hand is hovering over the model name and the UI shows options like &#x22;Deploy model&#x22;, &#x22;Refresh&#x22; and &#x22;Reset view.&#x22;" />
</Frame>

Notes:

* The deployment page displays the REST endpoint you will call from applications or tools like Postman and curl.
* Use a clear, consistent deployment name — this name appears in the request URL path.

***

## Example: calling the chat completion endpoint with curl / Postman

Set your API key in your shell or PowerShell environment.

Bash (Linux/macOS):

```bash theme={null}
export AZURE_API_KEY="<your-api-key>"
```

PowerShell (Windows):

```powershell theme={null}
$Env:AZURE_API_KEY = "<your-api-key>"
```

Example curl request (replace \<your-endpoint>, \<deployment-name>, and choose the correct api-version):

```bash theme={null}
curl -X POST "https://<your-endpoint>.openai.azure.com/openai/deployments/<deployment-name>/chat/completions?api-version=2024-12-01" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "I am going to Paris, what should I see?"
      }
    ],
    "max_tokens": 512,
    "temperature": 1,
    "top_p": 1
  }'
```

Tips for Postman:

* Add the `Content-Type: application/json` header (Postman will do this automatically for JSON bodies).
* Add an `api-key` header with your Azure API key.
* All inference requests (completions, embeddings, chat/completions) require POST.

Sample (abridged) response for the Paris query:

```json theme={null}
{
  "id": "chatcmpl-BO3j0mAR7oiozlyVFlatZQRB9NsF",
  "object": "chat.completion",
  "created": 1745073890,
  "model": "gpt-4o-2024-11-20",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Paris is often referred to as the City of Light. Highlights include the Eiffel Tower, the Louvre, Notre-Dame, Montmartre, and the Seine riverbanks. Consider strolling the Champs-Élysées, visiting the Musée d'Orsay, and sampling pastries at local pâtisseries. For a unique view, take an evening Seine river cruise to see the city illuminated."
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

> **warning** Keep your API key secure. Never commit keys to source control or expose them in client-side code. Rotate keys regularly and restrict usage with appropriate IAM policies.

***

## Final notes and best practices

* Confirm the model you plan to use supports the required API type (completion, embedding, or chat).
* Use `max_tokens`, `temperature`, and `top_p` to control response length and randomness.
* Track token usage via the response `usage` object to monitor costs.
* For streaming responses, advanced control, or SDK usage, consult the official docs and your Foundry deployment settings.

Links and references

* Azure OpenAI REST API reference: [https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference)
* Azure AI Fundamentals / Foundry docs: [https://learn.microsoft.com/azure/ai-services/](https://learn.microsoft.com/azure/ai-services/)
* Kubernetes and containers (context for deployments & infra): [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

This lesson covered REST endpoints, example request/response payloads, deployment inspection, and practical tips for invoking Azure OpenAI with curl and Postman.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/555c7620-8f25-4f2d-b1e8-1aa3cca1a55b/lesson/f1ca7400-a3a5-48da-908b-6bfeb44af844)
