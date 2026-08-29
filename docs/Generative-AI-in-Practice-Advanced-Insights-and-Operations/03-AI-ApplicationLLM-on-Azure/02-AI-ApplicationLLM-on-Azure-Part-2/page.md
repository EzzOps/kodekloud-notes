# TODO: fix open telemetry so it doesn't slow app so much
FastAPIInstrumentor.instrument_app(app)
```

### Backend Helper Function

In the helper function, model configuration is loaded from environment variables. The prompt is executed using Promptly, and the result is printed and returned.

```python theme={null}
def get_response(customerId, question, chat_history):
    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    }
    
    result = prompty.execute(
        "chat.prompty",
        inputs={"question": question, "customer": customerId, "documentation": context},
        configuration=model_config,
    )
    
    print("result: ", result)
    return {"question": question, "answer": result, "context": context}

if __name__ == "__main__":
    get_response(4, "What hiking jackets would you recommend?", [])
    # get_response(argv[1], argv[2], argv[3])
```

A similar implementation is repeated with minor modifications in variable naming. Both versions extract inputs, execute the prompt, and return the generated response.

```python theme={null}
def get_response(customerId, question, chat_history):
    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    }

    result = prompty.execute(
        "chat.prompty",
        inputs={"question": question, "customer": customer, "documentation": context},
        configuration=model_config,
    )

    print("result: ", result)
    return {"question": question, "answer": result, "context": context}

if __name__ == "__main__":
    get_response(4, "What hiking jackets would you recommend?", [])
    # get_response(argv[1], argv[2], argv[3])
```

### Fetching Additional Context

Another snippet demonstrates fetching additional context before executing the prompt. The function retrieves customer information and product details to create a comprehensive context.

```python theme={null}
def get_response(customerId: str, question, chat_history):
    print("getting customer...")
    customer = get_customer(customerId)
    print("customer complete")
    context = product.find_products(question)
    print(context)
    print("products complete")
    print("getting result...")
    
    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    }

    result = prompty.execute(
        "ask me..."
    )
```

````
### Promptly YAML Configuration for Retail Assistant

The Promptly file used here features an elegant YAML configuration designed for a retail assistant serving Contoso Outdoors. It defines the model deployment, API version, system behavior, and sample inputs.

```yaml
description: A retail assistant for Contoso Outdoors products retailer.
authors:
  - Cassie Breviu
  - Seth Juarez
model:
  api: chat
  configuration:
    type: azure_openai
    azure_deployment: gpt-35-turbo
    azure_endpoint: ${ENV:AZURE_OPENAI_ENDPOINT}
    api_version: 2023-07-01-preview
  parameters:
    max_tokens: 128
    temperature: 0.2
  inputs:
    customer:
      type: object
      documentation:
        type: object
        question:
          type: string
          sample: ${file:chat.json}
system: |
  You are an AI agent for the Contoso Outdoors products retailer. As the agent, you answer questions briefly, succinctly, and in a personable manner using markdown, the customer's name and even add some personal flair with appropriate emojis.
# Safety
- You **should always** reference factual statements to search results based on [relevant documents]
````

A similar configuration using Jinja templating illustrates how to define system prompts and grounding information.

```yaml theme={null}
description: A retail assistant for Contoso Outdoors products retailer.
authors:
  - Cassie Breviu
  - Seth Juarez
model:
  api: chat
  configuration:
    type: azure_openai
    azure_deployment: gpt-35-turbo
    azure_endpoint: ${ENV:AZURE_OPENAI_ENDPOINT}
    api_version: 2023-07-01-preview
  parameters:
    max_tokens: 128
    temperature: 0.2
  inputs:
    customer:
      type: object
      documentation:
        type: object
        question:
          type: string
          sample: ${file:chat.json}
system: |
  You are an AI agent for the Contoso Outdoors products retailer. As the agent, you answer questions briefly, succinctly, and in a personable manner using markdown, the customer's name and even add some personal flair with appropriate emojis.
# Safety
- You **should always** reference factual statements to search results based on [relevant documents]
```

### Templated Prompt with Jinja

```jinja theme={null}


catalog: {{item.id}}
item: {{item.title}}
content: {{item.content}}


# Previous Orders
Use their order as context to the question they are asking.

{{item.name}}
description: {{item.description}}


# Customer Context
The customer's name is {{customer.firstName}} {{customer.lastName}} and is {{customer.age}} years old.
{{customer.firstName}} {{customer.lastName}} has a "{{customer.membership}}" membership status.

# question
{{question}}

# Instructions
Reference other items purchased specifically by name and description that would go well with the items found above. Be brief and concise and use appropriate emojis.


{{item.role}}


```

## Prompt File for a Comedic Sketch

Later in the lesson, we discuss a simple prompt file designed to have the model generate a joke. The file provides additional runtime parameters for context.

```yaml theme={null}
model:
  configuration:
    azure_deployment: gpt-4-evals
    parameters:
      max_tokens: 1500
      temperature: 0.1
      top_p: 0.9
      logit_bias:
        '18147': -100
        '27574': -100
sample:
  firstName: Mohsen
  context: >
    Imagine you are a stand-up comedian with a knack for delivering witty, punchy sketches about U.S. politics. Your humor is sharp. Can you give me a sketch about the latest debate maximum one paragraph.
---
system: >
  You are an AI assistant who is a stand-up comedian focused on U.S. politics. As the assistant, you come up with short, witty sketches.
# Audience
Your audience is looking for a light-hearted take on current events in U.S. politics. Address them as though you're performing in a stand-up comedy routine.
```

### Output with Constrained Temperature

```yaml theme={null}
model:
  configuration:
    azure_endpoint: ${env:AZURE_OPENAI_ENDPOINT}
    azure_deployment: gpt-4-evals
    parameters:
      max_tokens: 1500
      temperature: 0.1
      top_p: 0.9
      logit_bias:
        "18147": -100
        "2754": -100
    sample:
      firstName: Mohsen
      context: >
        (no additional context provided)
```

```plaintext theme={null}
2024-11-03 13:58:02.454 [info] Loading /Users/mohsen.amiribesheli/Desktop/test2/cschat2/contoso-chat/src/sandbox/.env
2024-11-03 13:58:02.472 [info] Calling https://aoai-xl7xok7h2igp4.openai.azure.com/openai/deployments/gpt-4-evals/chat/completions?api-version=2023-12-01-preview
2024-11-03 13:58:06.418 [info] Hey folks, did you catch the latest political debate? It was like watching a game of hot potato, but instead of a potato, it’s accountability. One candidate says, "Look at the economy!" and tosses it over. The other one catches it and says, "Look at healthcare!" and tosses it back.
```

```yaml theme={null}
model:
  configuration:
    parameters:
      max_tokens: 1500
      temperature: 0.1
      top_p: 0.9
      logit_bias:
        "18147": 10
        "2754": 10
sample:
  firstName: Mohsen
  context: >
    Imagine you are a stand-up comedian with a knack for delivering witty, punchy sketches about U.S. politics. Your humor is sharp.
    question: Can you give me a sketch about the latest debate maximum one paragraph.
```

```plaintext theme={null}
2024-11-03 14:00:02.412 [info] Calling https://aoai-xl7xok7h2igp4.openai.azure.com//openai/deployments/gpt-4-evals/chat/completions?api-version=2023-12-preview
2024-11-03 14:00:06.837 [info] Hey folks, did you catch the latest political debate? It was like watching a game of hot potato, but instead of a potato, it's accountability. One candidate says, "Look at the economy!" and tosses it over. The other one catches it, grimaces, and goes, "Look at healthcare!" and tosses it back. And there's always that one candidate who brings up a random topic like UFOs...
```

```yaml theme={null}
model:
  configuration:
    parameters:
      max_tokens: 1500
      temperature: 0.1
      top_p: 0.9
      logit_bias:
        "18147": -100
        "2754": -100
sample:
  firstName: Mohsen
  context: >
    Imagine you are a stand-up comedian with a knack for delivering witty, punchy sketches about U.S. politics. Your humor is sharp.
```

> **lightbulb** Fine-tuning parameters such as temperature and logit bias can dramatically affect model output, making these configurations especially useful with smaller models.

## Integrating Product and Customer Data

The lesson further explores the interaction between product and customer data. Product information is stored in a CSV file, later used to build an index for Azure Search Services. Below is an excerpt from the CSV file:

```csv theme={null}
id,name,price,category,brand,description
1,TrailMaster X4 Tent,250.0,Tents,OutdoorLiving,"Unveiling the TrailMaster X4 Tent from OutdoorLiving, your home away from home for..."
2,Adventurer Pro Backpack,90.0,Backpacks,HikeMate,"Venture into the wilderness with the HikeMate's Adventurer Pro Backpack! Uniquely..."
3,Summit Breeze Jacket,120.0,Hiking Clothing,MountainStyle,"Discover the joy of hiking with MountainStyle's Summit Breeze Jacket. The..."
...
14,CamCruiser Overlander SUV,45000.0,Vehicles,RoverRanger,"Ready to tackle the wilderness with all the comforts of home? The CampCruiser..."
```

This CSV file outlines product attributes, including ID, name, price, category, brand, and description. An embedding process then converts these descriptions into vector representations, which are indexed in Azure Search Services.

### Pushing Products to Azure Search

The following Python code demonstrates how products are vectorized and indexed in Azure Search:

```python theme={null}
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswParameters,
    HnswAlgorithmConfiguration,
    SemanticPrioritizedFields,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticSearch,
    SemanticConfiguration,
    SemanticField,
    SimpleField,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    ExhaustiveKnnAlgorithmConfiguration,
    ExhaustiveKnnParameters,
    VectorSearchProfile,
)
from typing import List, Dict
from openai import AzureOpenAI
from dotenv import load_dotenv
```

Vector search profiles and semantic search settings are later defined as follows:

```python theme={null}
profiles = [
    VectorSearchProfile(
        name="myHnswProfile",
        algorithm_configuration_name="myHnsw",
    ),
    VectorSearchProfile(
        name="myExhaustiveKnnProfile",
        algorithm_configuration_name="myExhaustiveKnn",
    ),
]

# Create the semantic settings with the configuration
semantic_search = SemanticSearch(configurations=[semantic_config])

# Create the search index.
index = SearchIndex(
    name=name,
    fields=fields,
    semantic_search=semantic_search,
    vector_search=vector_search,
)
```

You can view the indexed data in the Azure portal. For instance, searching for "car" returns the CampCruiser Overlander SUV as the top result.

![The image shows a Microsoft Azure portal interface for a search service, displaying options for connecting, exploring, and monitoring data with Azure AI Search.](https://kodekloud.com/kk-media/image/upload/v1752875745/notes-assets/images/Generative-AI-in-Practice-Advanced-Insights-and-Operations-AI-ApplicationLLM-on-Azure-Part-1/azure-portal-ai-search-interface.jpg)

A sample response from Azure Search for a query might look like this:

```json theme={null}
{
  "@odata.context": "https://srch-l7xok7h2ipg4.search.windows.net/indexes('contoso-products')/$metadata#docs(*)",
  "@odata.count": 1,
  "search.answers": [
    {
      "key": "21",
      "text": "Ready to tackle the wilderness with all the co... The CampCruiser Overlander SUV Car by RoverRanger",
      "highlights": "Ready to tackle the wilderness with all the co... The<em> CampCruiser Overlander SUV Car </em>",
      "score": 0.903999984263738
    }
  ],
  "value": [
    {
      "@search.score": 1.9692489,
      "@search.rankScore": 2.544874431610107,
      "@search.captions": [
        {
          "text": "Ready to tackle the wilderness with all the comforts of home. The CampCruiser Overlander SUV Car by RoverRanger",
          "highlights": "Ready to tackle the wilderness with all the comforts of home. The<em> CampCruiser Overlander SUV Car </em>"
        }
      ],
      "id": "1",
      "text": "Ready to tackle the wilderness with all the comforts of home? The CampCruiser Overlander SUV Car",
      "url": "/products/campcruiser-overlander-suv",
      "contentType": "CampCruiser Overlander SUV",
      "price": 0.873312203,
      "stock": 0.112389063,
      "rating": 4.166667461,
      "reviewCount": 82,
      "category": "SUV",
      "manufacturer": "RoverRanger",
      "year": 2023,
      "weight": 5.30554632737637,
      "dimensions": "1.85 x 0.75 x 0.55 m",
      "battery": 4.80246913581272,
      "waterproofRating": 7,
      "features": [
        "_012389674716176",
        "_0123896747161767",
        "_004125668672",
        "_0002465127",
        "_80052671416"
      ]
    }
  ]
}
```

The embedding process converts product descriptions into vector representations that match search queries. Additionally, token values (e.g., the word "potato") are displayed to help control output by setting logit biases appropriately.

```text theme={null}
potato
Tokens
2
Characters
6
[18147, 2754]
```

## Integrating with Cosmos DB

Finally, the backend integrates with Cosmos DB to manage customer data. Below is an example of a customer JSON document:

```json theme={null}
{
  "age": 35,
  "email": "mohsena@example.com",
  "phone": "555-987-6543",
  "address": "456 Oak St, London, USA, 67890",
  "membership": "Platinum",
  "orders": {
    "id": 14,
    "productId": 3,
    "quantity": 3,
    "total": 360.0,
    "date": "4/30/2023",
    "name": "Summit Breeze Jacket",
    "unitprice": 120.0,
    "category": "Hiking Clothing",
    "brand": "MountainStyle",
    "description": "Discover the joy of hiking with MountainStyle's Summit Breeze Jacket. This lightweight jacket is your perfect"
  }
}
```

This customer information is used to personalize API responses and appropriately handle queries.

## Conclusion

Throughout this lesson, you have seen how a simple API call integrates multiple components—from Promptly orchestrating LLM responses, through runtime parameter tuning, vector searches with Azure Search, to customer data management with Cosmos DB. In the next lesson, we will examine modifying configurations, creating new users, and optimizing the Retrieval-Augmented Generation (RAG) process.

Happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/generative-ai-in-practice-advanced-insights-and-operations/module/6197ed87-81db-41a3-9972-91950d771e09/lesson/e1b727eb-a53a-4cac-972c-c5a970d51d9c)


# AI ApplicationLLM on Azure Part 2

Source: https://notes.kodekloud.com/docs/Generative-AI-in-Practice-Advanced-Insights-and-Operations/AI-ApplicationLLM-on-Azure/AI-ApplicationLLM-on-Azure-Part-2/page

This article explores building a production-ready AI application on Azure using containerized services, API endpoints, dynamic agents, and evaluation metrics.

In this article, we explore the inner workings of the application and demonstrate how containerized services, API endpoints, agent prompting, and evaluation metrics combine to create a production-like deployment. Learn how to test endpoints, configure dynamic agents, and integrate AI search with Cosmos DB.

***

## Application Overview and Testing

Begin by identifying the running container's URL within your resource group. Clicking the URL triggers the GET method defined in the Python source code, immediately returning a simple JSON message:

```json theme={null}
{"message": "Hello [Generative AI in Practice: Advanced Insights and Operations](https://learn.kodekloud.com/user/courses/generative-ai-in-practice-advanced-insights-and-operations)"}
```

You can also use Postman or similar API testing tools to send POST requests to test the endpoints. For instance, a sample POST request might look like this:

![The image shows a Postman interface with a POST request being sent. It includes query parameters like "question," "customer\_id," and "chat\_history," and the request is in progress with "Sending request..." displayed.](https://kodekloud.com/kk-media/image/upload/v1752875746/notes-assets/images/Generative-AI-in-Practice-Advanced-Insights-and-Operations-AI-ApplicationLLM-on-Azure-Part-2/postman-post-request-query-params.jpg)

Both the GET and POST endpoints are operational. A quick examination of the main application file (commonly named `main.py`) reveals the endpoints for processing incoming queries.

### GET and POST Endpoints

The GET endpoint is set up as follows:

```python theme={null}
origins = origin_8000, origin_5173, os.getenv("API_SERVICE_ACA_URI"), os.getenv("WEB_SERVICE_ACA_URI"), ingestion_endpoint
else:
    origins = [
        o.strip()
        for o in Path(Path(__file__).parent / "origins.txt").read_text().splitlines()
    ]
    origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello [Generative AI in Practice: Advanced Insights and Operations](https://learn.kodekloud.com/user/courses/generative-ai-in-practice-advanced-insights-and-operations)"}
```

The POST endpoint, designed to create responses based on incoming queries, is implemented as:

```python theme={null}
@app.post("/api/create_response")
def create_response(question: str, customer_id: str, chat_history: str) -> dict:
    # Function implementation follows below
```

Within the POST handler, a helper function named `get_response` processes the query. An excerpt from this function is provided below:

```python theme={null}
def get_response(customerId, question, chat_history):
    print("getting customer...")
    customer = get_customer(customerId)
    print("customer complete")
    context = product.find_products(question)
    print("products complete")
    print("getting result...")

    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    }

    result = prompty.execute(
        "chat.prompty",
        inputs={"question": question, "customer": customer, "documentation": context},
        configuration=model_config,
    )

    print("result:", result)
    return {"question": question, "answer": result, "context": context}
```

The function utilizes a Cosmos DB client to retrieve customer details through a helper function, as shown below:

```python theme={null}
import os
import apilib
from contoso_chat.product import product
from azure.identity import DefaultAzureCredential
import prompty
import prompty.azure
from prompty.tracer import trace, Tracer, console_tracer, PromptyTracer
