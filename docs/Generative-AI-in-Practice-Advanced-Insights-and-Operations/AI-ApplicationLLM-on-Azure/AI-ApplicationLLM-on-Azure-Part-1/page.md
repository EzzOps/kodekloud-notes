# AI ApplicationLLM on Azure Part 1

Source: https://notes.kodekloud.com/docs/Generative-AI-in-Practice-Advanced-Insights-and-Operations/AI-ApplicationLLM-on-Azure/AI-ApplicationLLM-on-Azure-Part-1/page

This article explores building a test application using Retrieval-Augmented Generation on Azure, detailing infrastructure, code integration, and API setup.

In this lesson, we explore the infrastructure and code behind our test application using Retrieval-Augmented Generation (RAG). Our objective is to illustrate how various components—from APIs and application configurations to vector search and runtime parameters—work in tandem to deliver an end-to-end solution on Azure.

## Overall Architecture

We start by reviewing the overall architecture which includes key components such as Azure Container Apps, Machine Learning workspaces, and storage accounts. This mid-size pilot application leverages common Azure services, including Azure-managed identities and Azure AI Studio.

<Frame>
  ![The image shows a Microsoft Azure Resource Visualizer interface displaying a diagram of interconnected cloud services and resources. It includes various Azure components like Container Apps, Machine Learning workspaces, and Storage accounts.](https://kodekloud.com/kk-media/image/upload/v1752875743/notes-assets/images/Generative-AI-in-Practice-Advanced-Insights-and-Operations-AI-ApplicationLLM-on-Azure-Part-1/azure-resource-visualizer-diagram.jpg)
</Frame>

## Deep Dive into Code Integration

Next, we examine the code—with an in-depth look at Promptly integration.

### YAML Model Configuration

The following YAML configuration defines model settings, including the API endpoint, deployment details, and runtime parameters such as max tokens, temperature, top\_p, and logit bias adjustments. It also provides a sample user and context prompt.

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
      Imagine you are a stand-up comedian with a knack for delivering witty, punchy sketches
      about U.S. politics. Your humor is sharp, insightful, and always respectful, though you
      don't shy away from a little satire on political figures, policies, or the latest headlines.
      Each sketch should be brief, relatable, and funny, making your audience laugh while nudging them
      to think.
```

After saving these changes, the application functions as an API. Users send inquiries and receive answers from the backend LLM.

### API Setup with FastAPI

Consider the main API file that sets up routes using FastAPI. The sample snippet demonstrates the inclusion of CORS middleware and two endpoints: one for a health-check (GET) and another for generating responses (POST).

```python theme={null}
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
    return {"message": "Hello and welcome"}

@app.post("/api/create_response")
@trace
def create_response(question: str, customer_id: str, chat_history: str) -> dict:
    # Implementation goes here
    pass
```

A more detailed view of the API call shows that when the "get response" endpoint is triggered, the code extracts inputs and passes them to another module, which uses Promptly to orchestrate backend processes.

```python theme={null}
@app.get("/")
async def root():
    return {"message": "Hello and welcome"}

@app.post("/api/create_response")
@trace
def create_response(question: str, customer_id: str, chat_history: str) -> dict:
    result = get_response(customer_id, question, chat_history)
    return result
