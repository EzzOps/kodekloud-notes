# User prompt for poem generation
input_message = "Write a haiku about autumn leaves."

response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {"role": "system", "content": "You are an AI chatbot specialized in writing poems."},
        {"role": "user", "content": input_message}
    ]
)

poem = response.choices[0].message.content
print(poem)
```

<Callout icon="triangle-alert">
  Ensure your environment variables (`OPENAI_API_KEY`, `LLM_ENDPOINT`, `MODEL`) are correctly set before running the script.
</Callout>

<Callout icon="lightbulb">
  You can switch between your local Ollama server and the hosted OpenAI API simply by updating the `LLM_ENDPOINT` URL.
</Callout>

## Next Steps

Now that you’ve seen how to:

1. Initialize the OpenAI client for local Ollama models
2. Send chat completion requests
3. Extract and display the generated text

You’re ready to build the full poem-generator application step by step.

<Frame>
  ![The image outlines two next steps: leveraging the OpenAI Python library and using the code to build an AI application.](https://kodekloud.com/kk-media/image/upload/v1752883662/notes-assets/images/Running-Local-LLMs-With-Ollama-Leveraging-Ollama-Models-in-Application-Development/openai-python-library-ai-application.jpg)
</Frame>

## References and Further Reading

* [OpenAI Python Library Documentation](https://github.com/openai/openai-python)
* [Ollama Official Guide](https://ollama.com/docs)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/df5bade3-d12b-4584-aae7-c4bdbaae39ff" />
</CardGroup>


# Ollama REST API Endpoints

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Ollama-REST-API-Endpoints/page

Integrate large language models into applications using the Ollama REST API for text generation, chat, and model management over HTTP.

Leverage the Ollama REST API to integrate large language models (LLMs) into your applications over HTTP. Skip the CLI or chatbot UI—simply send requests to interact with models for text generation, conversational chat, and model management.

***

## Generate Endpoint

The **POST** `/api/generate` endpoint returns a model’s completion for your prompt.

```bash theme={null}
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Compose a poem on LLMs",
  "stream": false
}'
```

By default, `"stream": false` delivers the full response at once. Set `"stream": true` to receive incrementally streamed data (word or phrase by phrase), emulating the gradual output of web chat interfaces.

<Callout icon="lightbulb">
  Streaming responses can improve perceived latency for long completions. Be sure your client can handle partial chunks.
</Callout>

### Formatting the JSON Output

You can instruct Ollama to structure its response using a `format` schema:

```bash theme={null}
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Compose a poem on LLMs",
  "stream": false,
  "format": {
    "title": "string",
    "theme": "string",
    "lines": ["string"]
  }
}'
```

#### Sample Response

```json theme={null}
{
  "model": "llama3.2",
  "created_at": "2025-01-09T06:31:38.309573Z",
  "response": {
    "title": "Cosmic Odyssey",
    "theme": "Self-discovery in Language",
    "lines": [
      "In digital realms, I found my home",
      "A tapestry woven from words and codes",
      "Where meaning flows like starlight to the sea",
      "I danced with syntax, a cosmic rhyme"
    ]
  },
  "done": true,
  "done_reason": "stop",
  "context": [123, 232, 123],
  "total_duration": 18387332083,
  "load_duration": 20368125,
  "prompt_eval_count": 44,
  "prompt_eval_duration": 501000000,
  "eval_count": 68,
  "eval_duration": 13140000000
}
```

* `title` and `theme` are strings.
* `lines` is an array of strings—ideal for rendering multiline content.

***

## Chat Endpoint

Use **POST** `/api/chat` to maintain conversational context. Provide an array of `messages` with roles (`user` or `assistant`).

```bash theme={null}
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    {
      "role": "user",
      "content": "Compose a short poem about LLMs."
    },
    {
      "role": "assistant",
      "content": "In circuits vast, they find their spark,\nLanguage learned in the digital dark.\nTransforming text with neural art,\nLLMs ignite a brand-new start."
    },
    {
      "role": "user",
      "content": "Add alliteration to the poem for more impact."
    }
  ],
  "stream": false
}'
```

### Example Response

```json theme={null}
{
  "model": "llama3.2",
  "created_at": "2025-01-09T06:47:26.589285Z",
  "message": {
    "role": "assistant",
    "content": "Here's an updated version of the poem:\n\nIn silicon sanctums,\nsparks take flight,\nLanguage learning lattices shine so bright.\nNeural networks navigate nuanced space,\nTransforming text with sophisticated pace.\n\nLet me know if you'd like any further adjustments!"
  },
  "done": true,
  "done_reason": "stop",
  "total_duration": 3393490083,
  "load_duration": 807877958,
  "prompt_eval_count": 88,
  "prompt_eval_duration": 1319000000,
  "eval_count": 53,
  "eval_duration": 954000000
}
```

Here, repeated initial sounds like **s** in “silicon sanctums, sparks” and **l** in “Language learning lattices” provide alliteration.

***

## Model Management Endpoints

Ollama’s REST API also lets you list, inspect, copy, delete, and pull models without switching to the CLI.

<Frame>
  ![The image shows a list of API endpoints with three options: listing running models, seeing details of a model, and deleting or pulling a new model.](https://kodekloud.com/kk-media/image/upload/v1752883662/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-REST-API-Endpoints/api-endpoints-models-listing-details.jpg)
</Frame>

### Endpoint Summary

| Endpoint      | Method | Description                           |
| ------------- | ------ | ------------------------------------- |
| `/api/list`   | GET    | List all available local models       |
| `/api/copy`   | POST   | Duplicate a model under a new name    |
| `/api/delete` | DELETE | Remove a specified local model        |
| `/api/pull`   | POST   | Download a model from the Ollama repo |

### Usage Examples

```bash theme={null}
