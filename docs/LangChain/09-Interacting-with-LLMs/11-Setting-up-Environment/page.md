# Populate the placeholder when invoking:
prompt = chat_prompt.format_prompt(text="LangChain connects components to build LLM apps.")
messages = prompt.to_messages()  # messages can be sent to a ChatModel/LLM
```

<Callout icon="lightbulb">
  Use prompt templates to keep prompts consistent, enforce style or constraints, and share reusable patterns across your application or organization.
</Callout>

## Prompt template types and common uses

| Template Type  | Purpose                                                   | Example / Notes                                                                   |
| -------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------- |
| System message | Set assistant role, tone, and constraints                 | Use `SystemMessagePromptTemplate.from_template("You are a helpful assistant...")` |
| Human message  | Contains user-facing prompt text and dynamic placeholders | Use `HumanMessagePromptTemplate.from_template("Summarize:\n\n{text}")`            |
| AI message     | Template or parsing expectations for model outputs        | Use for expected format or to attach output parsing logic                         |

## Best practices

* Keep system templates focused on role, constraints, and safety guardrails.
* Use human templates for dynamic content and user data; validate or sanitize inputs before formatting.
* Create small, composable templates for reuse (e.g., short/concise vs. long/detailed personas).
* Manage organization-wide templates in a central repo or configuration to maintain consistent model behavior.
* Combine templates with output-parsing tools or schema validation when you need structured data from responses.

## Example use cases

* Summarization: system sets tone, human provides target text.
* QA over documents: system enforces source citation, human supplies query and document context.
* Multi-persona assistants: swap system templates to change assistant behavior without editing application logic.

## Links and references

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (general reference)
* [Docker Hub](https://hub.docker.com/) (general reference)

Next, we’ll walk through demos showing how to construct these prompt templates and use them inside chains.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/4c4472e9-fd82-4691-860a-55d9fad2f7f5" />
</CardGroup>


# Setting up Environment

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Setting-up-Environment/page

Guide to setting up LangChain environment, installing specific package versions, configuring OpenAI API key, and learning model calls, prompt engineering, and response parsing

Welcome to this lesson on interacting with large language models using LangChain. In this module we'll focus on the Model I/O component — the part of LangChain responsible for invoking models and handling their inputs and outputs. You'll learn how to call models, design effective prompts, and format or parse model responses for your applications.

<Frame>
  <img alt="The image is a welcome slide outlining three topics: understanding prompt engineering, formatting and transforming responses, and interacting with a large language model. The slide has colorful graphics and a gradient background." />
</Frame>

What this lesson covers:

* How to invoke a model (model calls).
* How to craft prompts that get reliable outputs (prompt engineering).
* How to format, parse, and transform model responses to suit your app.

By the end of this lesson you will be able to make model calls with LangChain, apply foundational prompt engineering techniques, and parse responses to integrate them cleanly into your application workflows.

<Frame>
  <img alt="The image features a section labeled &#x22;Prerequisites&#x22; with a blue gradient background, listing &#x22;Install the Libraries&#x22; and &#x22;Follow the Versions&#x22; with colored dots." />
</Frame>

Prerequisites

Before you begin, install the required Python packages and pin the package versions used in these examples. LangChain and related libraries evolve quickly; using the exact versions below helps avoid API and behavioral differences that can break examples.

| Requirement     | Purpose                                 | Example / Command                              |
| --------------- | --------------------------------------- | ---------------------------------------------- |
| Python packages | Install LangChain and OpenAI client     | `pip install langchain==0.1.10 openai==1.13.3` |
| OpenAI API key  | Authenticate requests to the OpenAI API | `export OPENAI_API_KEY=YOUR_OPENAI_API_KEY`    |

<Callout icon="lightbulb">
  Use the exact package versions listed to match the code and APIs in this lesson. Version mismatches are a common source of errors.
</Callout>

Install and configure

Run these commands to install the packages and set your OpenAI API key as an environment variable:

```bash theme={null}
pip install langchain==0.1.10 openai==1.13.3
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Security best practices

<Callout icon="warning">
  Never commit API keys to source control. Store secrets in environment variables or a secrets manager. If you use a `.env` file during development, load it securely (for example with `python-dotenv`) and ensure the file is excluded from version control.
</Callout>

Verify your environment

Check that the `OPENAI_API_KEY` environment variable is set before running the examples:

```bash theme={null}
