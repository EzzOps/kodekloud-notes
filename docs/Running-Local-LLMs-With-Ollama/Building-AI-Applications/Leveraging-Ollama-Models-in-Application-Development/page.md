# NAME               ID              SIZE     MODIFIED
# llama3-copy:latest a80c4f17acd5  2.0 GB   a few seconds ago
# llama3.2:latest    a80c4f17acd5  2.0 GB   24 hours ago
```

**Delete a Model**

```bash theme={null}
curl -X DELETE http://localhost:11434/api/delete \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3-copy"
  }'
```

<Callout icon="triangle-alert">
  Pulling new models via the REST API is not supported. Use the CLI instead:

  ```bash theme={null}
  ollama pull llama3.2
  ```
</Callout>

***

## 7. API Reference & Further Reading

For the full list of endpoints, request/response specifications, and example payloads, see the [Ollama API Documentation on GitHub](https://github.com/ollama/ollama/tree/main/docs).

<Frame>
  ![The image shows a GitHub repository page with a focus on an API documentation file, listing various endpoints such as "Generate a completion" and "Create a Model."](https://kodekloud.com/kk-media/image/upload/v1752883653/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Using-Ollama-API-and-Interacting-With-It/github-repo-api-docs-endpoints.jpg)
</Frame>

Links and References

* [Ollama GitHub Repository](https://github.com/ollama/ollama)
* [jq — Command-line JSON Processor](https://stedolan.github.io/jq/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/e55ae776-a631-4ccc-9b5d-38dbd1ee64c1" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/8b8dde83-9fd6-42c6-bead-db8664eeb29c" />
</CardGroup>


# Leveraging Ollama Models in Application Development

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Leveraging-Ollama-Models-in-Application-Development/page

Learn to build AI applications by integrating local Ollama models into your code, covering workflows from user input to response processing.

In this lesson, you’ll learn how to build AI-powered applications by integrating local Ollama models directly into your code. We’ll cover the end-to-end workflow—from capturing user input and invoking an LLM to processing and displaying responses. Our examples focus on Python, but the same patterns apply to Go, JavaScript, and more.

## Recap: Interacting with Ollama via REST API

Before diving into code, let’s revisit how we used `curl` to query local models:

<Frame>
  ![The image is a slide titled "Recap" with two points: interacting with the Ollama REST API using "curl" and getting a response from different models.](https://kodekloud.com/kk-media/image/upload/v1752883654/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/recap-ollama-rest-api-curl.jpg)
</Frame>

Key takeaways:

* Use `curl` to POST messages to your Ollama server.
* Retrieve structured JSON responses from any running model.

## Integrating API Calls into Your Application

Instead of shell commands, embed API calls in your code. Whether you write in Python, Go, or JavaScript, you can leverage the OpenAI client libraries to target your local Ollama endpoint:

<Frame>
  ![The image titled "The Story of Jane" features icons for Python, Go, and JavaScript programming languages, along with an illustration labeled "Jane."](https://kodekloud.com/kk-media/image/upload/v1752883655/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/the-story-of-jane-programming-icons.jpg)
</Frame>

### Core AI Application Workflow

1. Collect user input or fetch existing data.
2. Send that input to a large language model (LLM).
3. Process the response through your business logic.
4. Present the final result to the user.

<Frame>
  ![The image is a flowchart illustrating the process of AI applications, showing steps of taking user input and sending it to a large language model (LLM) for a relevant response.](https://kodekloud.com/kk-media/image/upload/v1752883656/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/ai-applications-flowchart-llm-response.jpg)
</Frame>

## Real-World Scenarios

| Use Case                 | Description                                                    |
| ------------------------ | -------------------------------------------------------------- |
| AI-Driven Chatbot        | Jane’s product docs bot answers user questions with context.   |
| Risk Assessment Platform | Growmore’s internal tool analyzes client data for risk scores. |

<Frame>
  ![The image illustrates a flowchart showing interactions between "Jane," an "AI Chatbot," and "Users," with an "AI Platform" and "Growmore" mentioned. It visually represents communication and information flow among these entities.](https://kodekloud.com/kk-media/image/upload/v1752883657/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/flowchart-jane-ai-chatbot-users.jpg)
</Frame>

## Example: Pulumi’s Infrastructure Chatbot

Pulumi’s [AI chatbot](https://pulumi.com/ai) lets you describe infrastructure in natural language and returns code in C#, Go, or Python:

```go theme={null}
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        bucket, err := s3.NewBucket(ctx, "my-bucket", nil)
        if err != nil {
            return err
        }
        ctx.Export("bucketName", bucket.ID())
        return nil
    })
}
```

By using OpenAI libraries, you can replicate this experience in your own app, swapping between a local Ollama host in development and the hosted OpenAI API in production—no code changes required.

## Choosing Your Client Library

Both Ollama and OpenAI support multiple languages. Below is a quick reference:

| Language   | Library                             | Local + Hosted Compatibility |
| ---------- | ----------------------------------- | ---------------------------- |
| Python     | `openai`                            | ✔️                           |
| TypeScript | `openai`                            | ✔️                           |
| Go         | `github.com/sashabaranov/go-openai` | ✔️                           |
| Java       | `com.theokanning.openai`            | ✔️                           |

<Frame>
  ![The image displays logos for Ollama and OpenAI at the top, and logos for Python, TypeScript, Go, and Java at the bottom, all on a dark background.](https://kodekloud.com/kk-media/image/upload/v1752883659/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/ollama-openai-python-typescript-go-java.jpg)
</Frame>

## Hands-On: Poem Generator in Python

Imagine an app where users submit prompts and receive custom poems:

<Frame>
  ![The image illustrates a process for building an application, showing a user interacting with AI, which uses a large language model (LLM) to generate a poem.](https://kodekloud.com/kk-media/image/upload/v1752883660/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/application-building-ai-poem-llm.jpg)
</Frame>

```python theme={null}
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("LLM_ENDPOINT")  # e.g., "http://localhost:11434"
)
