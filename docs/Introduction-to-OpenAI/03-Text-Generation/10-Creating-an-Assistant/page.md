# Legacy OpenAI Python SDK (no longer recommended)
from openai import OpenAI
client = OpenAI()

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Write a tagline for an ice cream shop."
)
```

```python theme={null}
# Legacy openai-python (also deprecated)
import openai
response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Write a tagline for an ice cream shop."
)
```

***

## Modern Chat Completions

Switch to the chat API for richer, role-based interactions:

```python theme={null}
from openai import OpenAI

openai = OpenAI(api_key="sk-...")

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a tagline for an ice cream shop."}]
)

print(response.choices[0].message.content)
```

***

## Naming Your OpenAI Client

Feel free to name your client object whatever you like. Here’s a standard pattern:

```python theme={null}
from openai import OpenAI

openai = OpenAI(api_key="sk-...")

def chat_comp(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content

print(chat_comp("How can I make more money?"))
```

Or with a custom client name:

```python theme={null}
from openai import OpenAI

RobotBestFriend = OpenAI(api_key="sk-...")

def chat_comp(prompt):
    response = RobotBestFriend.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content

print(chat_comp("How can I make more money?"))
```

Console output:

```plaintext theme={null}
There are several strategies you can consider to increase your income. Here are some ideas:
1. **Negotiate Your Salary:** ...
2. **Acquire New Skills:** ...
3. **Side Gigs:** ...
4. **Investing:** ...
5. **Start a Business:** ...
6. **Monetize Hobbies:** ...
```

> **lightbulb** Never commit your `api_key` to public repositories. Use environment variables or secret management tools.

***

## Roles in Chat Messages

The `messages` array defines each turn in a conversation. Supported roles:

| Role      | Purpose                                                   | Example                                                        |
| --------- | --------------------------------------------------------- | -------------------------------------------------------------- |
| system    | Sets global context, tone, or behavior for the assistant. | `"You are a helpful assistant."`                               |
| user      | End user’s input or question.                             | `"What's the weather today?"`                                  |
| assistant | Model’s prior responses in a multi-turn conversation.     | `"The weather is sunny and 75°F."`                             |
| function  | Allows the model to call a custom function you define.    | `"function_call": {"name": "get_weather", "arguments": {...}}` |

### JavaScript Example

```javascript theme={null}
const openai = new OpenAI({ apiKey: "sk-..." });

const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    {
      role: "system",
      content: [
        {
          type: "text",
          text: "You are a friendly coding tutor who uses southern idioms."
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Are semicolons optional in JavaScript?"
        }
      ]
    }
  ]
});
console.log(response.choices[0].message.content);
```

***

## Adding a System Prompt in Python

Include both `system` and `user` messages to guide the model’s tone:

```python theme={null}
from openai import OpenAI

RobotBestFriend = OpenAI(api_key="sk-...")

def chat_comp(prompt):
    response = RobotBestFriend.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a southern belle."},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=250
    )
    return response.choices[0].message.content

print(chat_comp("What are some side hustles I can try?"))
```

Console output:

```bash theme={null}
There are several ways to bring a little more income if you set your mind to it, sugar...
```

> **lightbulb** Place the `system` message before the `user` message to ensure the context is applied first.

***

## Exploring the `create` Signature

The `chat.completions.create` method supports numerous parameters for fine-tuning:

```python theme={null}
def create(
    *,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int | None = None,
    n: int | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    presence_penalty: float | None = None,
    frequency_penalty: float | None = None,
    logit_bias: dict[str, int] | None = None,
    functions: Iterable[Function] | None = None,
    function_call: FunctionCall | None = None,
    stream: bool | None = None,
    ...
):
    ...
```

Experiment with these options for customized responses:

* **temperature**: Controls randomness.
* **top\_p**: Nucleus sampling probability.
* **presence\_penalty** & **frequency\_penalty**: Encourage topic variety.
* **functions** & **function\_call**: Invoke your own code.

***

## Links and References

* [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/008e902f-5b14-4a71-8d0c-f0f42691e659)


# Creating an Assistant

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Creating-an-Assistant/page

This tutorial guides building, configuring, and testing a custom AI assistant using the OpenAI Assistants API and Assistant Playground.

Welcome to the OpenAI Assistants API guide. In this tutorial, we’ll walk through how to build, configure, and test a custom AI assistant using both the Assistant Playground and the OpenAI API.

## Overview of the Assistants API

The Assistants API (currently in beta) provides a simple way to register and interact with AI assistants. Before you begin, review the official [Assistants API documentation][docs] and explore the [Assistant Playground][playground] for a no-code experience.

![The image shows a webpage from OpenAI's platform documentation, specifically detailing the Assistants API overview and how it works, with a sidebar menu for navigation.](https://kodekloud.com/kk-media/image/upload/v1752879207/notes-assets/images/Introduction-to-OpenAI-Creating-an-Assistant/openai-assistants-api-overview-docs.jpg)

> **triangle-alert** The Assistants API is in **beta**. Endpoints and parameters may change as we improve functionality. Keep your integration up to date by regularly checking the [documentation][docs].

## Using the Assistant Playground

The [Assistant Playground][playground] offers an interactive UI to:

* Configure models and tools
* Set system instructions
* Name your assistant
* Run quick tests

You can instantly see how requests and responses are structured, making it ideal for prototyping before coding.

## Creating an Assistant with Python

To get started programmatically, install the OpenAI Python package and initialize the client:

```bash theme={null}
pip install openai
```

```python theme={null}
from openai import OpenAI

client = OpenAI()
```

Next, register a new assistant:

```python theme={null}
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run Python code to solve math problems step by step.",
    tools={"type": "code_interpreter"},
    model="gpt-4"
)
```

| Parameter    | Description                               | Example                              |
| ------------ | ----------------------------------------- | ------------------------------------ |
| name         | Friendly assistant name                   | `"Math Tutor"`                       |
| instructions | System-level prompt guiding the assistant | `"You are a personal math tutor..."` |
| model        | OpenAI model to power the assistant       | `"gpt-4"`                            |
| tools        | Enabled integrations or plugins           | `{"type": "code_interpreter"}`       |

## Handling Streaming Responses

For real-time output, subclass `AssistantEventHandler` and override event methods:

```python theme={null}
from typing_extensions import override
from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(text, end="", flush=True)

    @override
    def on_text_del(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"Tool call: {tool_call.type}", flush=True)

    @override
    def on_tool_call_del(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print("\n\noutput>", end=" ")
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\noutput.logs = {True}")
```

> **lightbulb** You can run this handler in any IDE (e.g., [Visual Studio Code][vscode]). Streaming makes the assistant feel more interactive by printing results as they arrive.

## Testing Your Assistant

Let’s test the “Math Tutor” with a sample expression in the Playground or via API calls:

> What is 13 times 5 divided by 6, times 5, plus 100 times 4 to the power of 2?

![The image shows a user interface for a math tutor assistant using a GPT-4 model, with a math expression input for evaluation.](https://kodekloud.com/kk-media/image/upload/v1752879207/notes-assets/images/Introduction-to-OpenAI-Creating-an-Assistant/math-tutor-assistant-gpt4-interface.jpg)

The assistant uses the code interpreter to compute and returns the result (approximately **1654.17**).

## Links and References

* [Assistants API Guide][docs]
* [Assistant Playground][playground]
* [API Quickstart Guide][quickstart]
* [Visual Studio Code][vscode]

[docs]: https://platform.openai.com/docs/guides/assistants-api

[playground]: https://platform.openai.com/playground

[quickstart]: https://platform.openai.com/docs/quickstart

[vscode]: https://code.visualstudio.com/

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/726bc20c-5d5a-4825-943e-05bbe12318b5)
