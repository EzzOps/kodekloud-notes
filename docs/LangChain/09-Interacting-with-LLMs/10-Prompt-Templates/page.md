# ChatPromptTemplate(input_variables=['subject', 'concept'],
#                    messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=['subject'], template='You are a {subject} teacher')),
#                              HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['concept'], template='Tell me about {concept}'))])
```

## 4. Populate the template to create a concrete prompt

Format the template with actual values for `subject` and `concept`. `format_messages` returns a list of message objects that you can send directly to a chat model:

```python theme={null}
prompt_messages = prompt_template.format_messages(subject="Chemistry", concept="Periodic Table")
```

After formatting, `prompt_messages` contains two message objects:

* System message: "You are a Chemistry teacher"
* Human message: "Tell me about the Periodic Table"

These message objects are ready to pass to the model.

## 5. Invoke the chat model and read the response

Create a `ChatOpenAI` instance and call it with the formatted messages. The `generate_messages` API returns a `ChatResult` containing the generated assistant messages.

```python theme={null}
model = ChatOpenAI()  # set parameters like temperature or model name as needed
response = model.generate_messages([prompt_messages])  # note: pass a list of message lists

# Extract the assistant-generated message content
assistant_content = response.generations[0][0].message.content
print(assistant_content)
```

Example output you might receive:

```text theme={null}
The Periodic Table is a tabular arrangement of the chemical elements, organized based on their atomic number, electron configuration, and recurring chemical properties. The table is divided into rows called periods and columns called groups. Elements in the same group have similar chemical properties due to their similar electron configurations.

The Periodic Table was first created by Dmitri Mendeleev in 1869, who organized the elements based on their atomic mass and predicted the properties of missing elements. The modern Periodic Table is based on atomic number, which is the number of protons in an atom's nucleus. The table is a vital tool in chemistry for predicting element behavior and compound formation, and it continues to evolve as new elements are discovered.
```

## 6. How this fits into a chain

Conceptually, this is a simple chain consisting of:

* A prompt: built from templates and populated at runtime.
* A model: the chat model that consumes the prompt and returns a response.

You can extend this chain with:

* Output parsers (to structure model output).
* Post-processing steps (validation, formatting).
* Storage layers (logs, databases).

## 7. Few-shot prompting (brief)

Few-shot prompting supplies examples to demonstrate desired output style or format. In LangChain, include example message turns in your prompt template so the model sees them along with the instruction and the current query. This helps steer tone, structure, and level of detail.

Example approaches:

* Add one or more example conversation turns using `HumanMessagePromptTemplate` and `AIMessagePromptTemplate` (if available).
* Provide formatted output examples illustrating how the model should structure its response.

## Troubleshooting & tips

* If the model response seems off-topic, enrich the system message with clearer constraints or add few-shot examples demonstrating the desired format.
* Use `temperature` and `max_tokens` settings on `ChatOpenAI` to control randomness and length.
* Avoid committing API keys to source control; use environment variables or secrets management.

<Callout icon="warning">
  Never commit your OpenAI API key to version control. Use environment variables or secret managers to keep keys safe. Monitor usage to avoid unexpected costs.
</Callout>

## Links and references

* [LangChain course on KodeKloud](https://learn.kodekloud.com/user/courses/langchain)
* [Introduction to OpenAI on KodeKloud](https://learn.kodekloud.com/user/courses/introduction-to-openai)
* Official LangChain docs: [https://langchain.readthedocs.io](https://langchain.readthedocs.io)
* OpenAI API docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)

***

This concise walkthrough covers building prompt templates, populating them at runtime, and invoking a chat model with LangChain. You can expand this pattern into pipelines for parsing, validation, or integrating with downstream applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/857f3912-4a8e-4594-bb30-479d5f303cc8" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/0c1c660e-6569-4b29-b3da-790d279553ff" />
</CardGroup>


# Prompt Templates

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Prompt-Templates/page

Explains LangChain prompt templates for system human and AI messages, showing usage patterns, Python example, best practices, and use cases for building reusable chat prompts.

Static messages work, but they’re not flexible or reusable across an application. Prompt templates let you parameterize system, human, or AI messages with placeholders that are filled in at runtime. This makes prompts easier to manage, share, and maintain—especially as your LLM-based application grows.

<Frame>
  <img alt="The image shows a diagram labeled &#x22;Prompt Templates and Prompts&#x22; with rounded rectangles representing different prompts and a legend indicating message types: System Message, Human Message, and AI Message. It notes the attributes &#x22;Helpful&#x22; and &#x22;Flexible.&#x22;" />
</Frame>

In practice, you define templates for each role (system, human, AI) and then combine them to build the final messages sent to your model. A common pattern is to use a system template to set behavior and constraints, and a human template to include the dynamic content or user input.

<Frame>
  <img alt="The image shows two sections titled &#x22;System Message Prompt Template&#x22; and &#x22;Human Message Prompt Template,&#x22; each with colored rectangular prompts. The system template is in blue, and the human template is in green." />
</Frame>

The model’s reply is returned as an AI message. While you can’t control the exact content the model generates, using an AI prompt template or output-parsing logic can help standardize expected formatting and extract structured results.

<Frame>
  <img alt="The image illustrates a process flow from an &#x22;Application&#x22; to an &#x22;AI Message&#x22; and finally to a &#x22;Chat Model,&#x22; associated with an &#x22;AI Message Prompt Template&#x22; concept." />
</Frame>

## Quick Python example

Below is a concise example showing how to compose chat-style prompt templates using LangChain. This demonstrates a `SystemMessagePromptTemplate` and a `HumanMessagePromptTemplate` with a placeholder called `text`. When formatted, the placeholder is filled and converted to messages that you can pass to a chat model.

```python theme={null}
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant that summarizes text concisely."
)

human = HumanMessagePromptTemplate.from_template(
    "Summarize the following text in one paragraph:\n\n{text}"
)

chat_prompt = ChatPromptTemplate.from_messages([system, human])
