# OpenAI Libraries

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Pre-Requisites/OpenAI-Libraries/page

OpenAI provides official and community libraries for API interaction, supporting various programming languages and use cases like chatbots and image generation.

OpenAI offers a range of official and community-maintained client libraries for interacting with the OpenAI API. Whether you’re building chatbots, generating images, or computing embeddings, there’s a library for your environment. Below is a quick overview of the most popular options:

| Library        | Language       | Official  | Documentation                                                                                                                |
| -------------- | -------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| OpenAI Python  | Python         | Yes       | [https://github.com/openai/openai-python](https://github.com/openai/openai-python)                                           |
| OpenAI Node.js | JavaScript/TS  | Yes       | [https://github.com/openai/openai-node](https://github.com/openai/openai-node)                                               |
| OpenAI.NET     | C#/.NET        | Community | [https://github.com/OkGoDoIt/OpenAI-API-dotnet](https://github.com/OkGoDoIt/OpenAI-API-dotnet)                               |
| Azure OpenAI   | Azure Service  | Yes       | [https://learn.microsoft.com/azure/cognitive-services/openai/](https://learn.microsoft.com/azure/cognitive-services/openai/) |
| Community SDKs | Ruby, PHP, Go… | Community | [https://platform.openai.com/docs/community](https://platform.openai.com/docs/community)                                     |

<Frame>
  ![The image lists various OpenAI libraries, including Python, .NET, Node.js, Azure OpenAI, and community libraries. It also includes a link to the OpenAI documentation.](https://kodekloud.com/kk-media/image/upload/v1752879188/notes-assets/images/Introduction-to-OpenAI-OpenAI-Libraries/openai-libraries-python-dotnet-nodejs.jpg)
</Frame>

For the full list of clients and SDKs, see the [Libraries section on the OpenAI docs](https://platform.openai.com/docs/libraries).

***

## Python

The official Python SDK is the most widely used OpenAI client. It supports:

* Chat and text completions
* Image generation
* Embeddings
* Utility functions and helpers

Python’s readability and extensive ecosystem make it ideal for developers, data scientists, and researchers. It integrates smoothly into existing projects and benefits from comprehensive docs and community support.

<Callout icon="lightbulb">
  Be sure to set your API key in the environment before running examples:

  ```bash theme={null}
  export OPENAI_API_KEY="your_api_key_here"
  ```
</Callout>

```python theme={null}
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)
```

## Node.js

The official Node.js client offers a promise-based API that works seamlessly with modern JavaScript and TypeScript frameworks:

* Async/await support
* ESM modules
* Works with Express, React, Vue, and more

```javascript theme={null}
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const response = await openai.chat.completions.create({
  model: "gpt-3.5-turbo",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user",   content: "What's the weather like today?" }
  ]
});

console.log(response.choices[0].message.content);
```

## .NET

While OpenAI doesn’t provide an official .NET SDK, community libraries like **OpenAI.NET** and **OpenAI API Client** fill the gap. They enable cross-platform .NET applications with:

* Asynchronous processing
* Microsoft stack integration
* Enterprise-grade features

<Frame>
  ![The image is an infographic about .NET Libraries, highlighting features like community-supported libraries, cross-platform applications, enterprise integration, and asynchronous processing, along with use cases in AI, financial services, and Microsoft Teams.](https://kodekloud.com/kk-media/image/upload/v1752879190/notes-assets/images/Introduction-to-OpenAI-OpenAI-Libraries/dotnet-libraries-infographic-features-usecases.jpg)
</Frame>

```csharp theme={null}
using System;
using System.Threading.Tasks;
using OpenAI.Chat;

namespace OpenAILesson
{
    class Program
    {
        static async Task Main()
        {
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
            var client = new ChatClient(new ChatClientOptions
            {
                ApiKey = apiKey,
                Model  = "gpt-3.5-turbo"
            });

            var result = await client.CompleteChatAsync("Say 'this is a test.'");
            Console.WriteLine(result.Choices[0].Message.Content);
        }
    }
}
```

## Azure OpenAI

Azure OpenAI Service brings OpenAI’s capabilities to the Azure ecosystem, offering:

* Enterprise security & compliance
* Managed, scalable API hosting
* Integration with Azure Cognitive Services, ML, and DevOps
* Access to pre-trained and fine-tuned models

Explore the [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/cognitive-services/openai/).

## Community Libraries

Numerous open-source SDKs and tools extend OpenAI support to languages and frameworks beyond the official clients. Community libraries provide:

* Open collaboration and contributions
* Language-specific enhancements
* Cross-platform development
* Creative integrations

<Frame>
  ![The image is a slide titled "Community Libraries" highlighting four aspects: diverse ecosystem, open-source contribution, platform flexibility and language extensions, and open collaboration.](https://kodekloud.com/kk-media/image/upload/v1752879191/notes-assets/images/Introduction-to-OpenAI-OpenAI-Libraries/community-libraries-diverse-ecosystem-slide.jpg)
</Frame>

***

## Further Reading

* [OpenAI Python SDK GitHub](https://github.com/openai/openai-python)
* [OpenAI Node.js SDK GitHub](https://github.com/openai/openai-node)
* [Azure OpenAI Service overview](https://learn.microsoft.com/azure/cognitive-services/openai/)
* [OpenAI Community Resources](https://platform.openai.com/docs/community)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/192b48b6-ae6c-4126-8784-a84f0d284a41/lesson/53697a92-2324-404e-9495-7539d5572096" />
</CardGroup>
