# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

<Callout icon="lightbulb">
  Using a virtual environment is optional but recommended for dependency management.
</Callout>

## 2. Install the OpenAI Python Package

With your environment active, install the official OpenAI library:

```bash theme={null}
pip install --upgrade openai
```

## 3. Configure Your API Key as an Environment Variable

Storing credentials in environment variables keeps them out of your codebase. Use the command for your OS:

| Platform             | Command                                     |
| -------------------- | ------------------------------------------- |
| macOS/Linux          | `export OPENAI_API_KEY="your_api_key_here"` |
| Windows (PowerShell) | `setx OPENAI_API_KEY "your_api_key_here"`   |

If you need an API key, visit:\
[OpenAI Platform → Settings → API Keys](https://platform.openai.com/account/api-keys) → *Create new secret key*.

<Callout icon="triangle-alert">
  Never commit your API key—or any secrets—to version control. Consider adding `.env` or environment-specific files to your `.gitignore`.
</Callout>

## 4. Write Your Python Script

Create a file named `example.py`:

```python theme={null}
from openai import OpenAI

# The client automatically reads OPENAI_API_KEY from your environment
client = OpenAI()

prompt = "Tell me a joke"
response = client.chat.completions.create(
    model="gpt-4o-mini",         # select an available model
    messages=[{"role": "user", "content": prompt}],
    max_tokens=150,              # adjust response length
    temperature=0.7,             # controls creativity
)

print(response.choices[0].message.content)
```

## 5. Run the Script and Verify the Output

With your environment variable set, execute:

```bash theme={null}
python example.py
```

Sample output:

```text theme={null}
Why did the scarecrow win an award?
Because he was outstanding in his field!
```

Running the script this way ensures your API key remains secure and separate from your codebase.

***

## Links and References

* [OpenAI Quickstart Guide](https://platform.openai.com/docs/quickstart)
* [OpenAI Python Library on PyPI](https://pypi.org/project/openai/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/6c8ab32c-658d-4139-ac95-e929de8c6edf" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/f493c45e-434f-48cd-821b-6e4ba818532e" />
</CardGroup>


# Overview of OpenAI Assistant

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Overview-of-OpenAI-Assistant/page

OpenAI Assistants are AI-driven conversational agents that automate tasks and enhance user interactions across various industries.

OpenAI Assistants are AI-driven conversational agents built on GPT models (like GPT-4) that automate tasks, enhance user interactions, and streamline workflows across industries—from customer support to finance and healthcare. In this guide, you’ll learn how they operate, explore core workflow states, discover key benefits, and see examples for customization.

***

## Personal Finance Assistant Example

This scenario showcases a personal finance bot helping with retirement planning. When a user asks, “How much should I contribute to my retirement plan?” the assistant:

1. Receives the user message.
2. Uses a code interpreter to calculate the optimal contribution.
3. Sends back: “You should contribute \$478 a year.”

On the right, the run panel highlights each step from computation to message creation.

<Frame>
  ![The image is a flowchart illustrating a personal finance bot assisting with retirement planning. It shows a user's message asking about retirement contributions and the assistant's response, with steps involving a code interpreter and message creation.](https://kodekloud.com/kk-media/image/upload/v1752879223/notes-assets/images/Introduction-to-OpenAI-Overview-of-OpenAI-Assistant/personal-finance-bot-retirement-flowchart.jpg)
</Frame>

***

## What Are OpenAI Assistants?

OpenAI Assistants leverage large language models to:

* Perform specific tasks and automate repetitive workflows
* Engage in natural language conversations
* Integrate with external tools (APIs, databases, code interpreters)

These agents excel in contexts like customer support, education, financial advising, and medical triage by understanding intent, generating accurate responses, and maintaining conversational context.

<Frame>
  ![The image is a slide titled "What Are OpenAI Assistants?" describing them as tools designed to perform tasks, assist with workflows, and interact with users in natural language (NL).](https://kodekloud.com/kk-media/image/upload/v1752879224/notes-assets/images/Introduction-to-OpenAI-Overview-of-OpenAI-Assistant/what-are-openai-assistants-slide.jpg)
</Frame>

***

## Core Workflow States

OpenAI Assistants track each task through a series of states:

| State            | Description                           |
| ---------------- | ------------------------------------- |
| queued           | Task is waiting to start              |
| in\_progress     | Task is actively running              |
| requires\_action | Task needs user input or intervention |
| cancelling       | Task is being stopped                 |

Final outcomes:

| Final State | Meaning                           |
| ----------- | --------------------------------- |
| completed   | Task finished successfully        |
| failed      | Task encountered an error         |
| cancelled   | Task was intentionally stopped    |
| expired     | Task timed out without completion |
| incomplete  | Task was partially done           |

<Frame>
  ![The image is a flowchart titled "OpenAI Assistants," showing different states such as "queued," "in\_progress," "requires\_action," and their possible outcomes like "completed," "failed," and "cancelled."](https://kodekloud.com/kk-media/image/upload/v1752879226/notes-assets/images/Introduction-to-OpenAI-Overview-of-OpenAI-Assistant/openai-assistants-flowchart-states-outcomes.jpg)
</Frame>

***

## Key Benefits

<Frame>
  ![The image is a split screen with two lists. The left side highlights benefits of automation, such as automating repetitive tasks and increasing efficiency, while the right side lists features like scalability, 24/7 availability, and personalization.](https://kodekloud.com/kk-media/image/upload/v1752879227/notes-assets/images/Introduction-to-OpenAI-Overview-of-OpenAI-Assistant/automation-benefits-features-comparison.jpg)
</Frame>

1. **Automation & Efficiency**\
   Free up teams by automating FAQs, ticket routing, and data processing.

2. **Scalability**\
   Seamlessly handle spikes in demand without hiring additional staff.

3. **24×7 Availability**\
   Provide nonstop support—ideal for global audiences or critical services.

4. **Personalization**\
   Adapt responses based on user history and preferences.

5. **Data Insights & Analytics**\
   Monitor conversations to extract sentiment, trends, and improvement areas.

6. **Continuous Learning**\
   Fine-tune on domain-specific datasets (e.g., legal, medical) to boost accuracy.

***

## Assistant Example: Customer Support

Here’s a Python snippet demonstrating a simple customer support assistant with GPT-4:

```python theme={null}
from openai import OpenAI

client = OpenAI()

def support_response(user_query: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a customer support assistant."},
            {"role": "user", "content": user_query}
        ],
        max_tokens=150,
        temperature=0,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    query = "Help me answer this technical question about my new snowblower."
    print(support_response(query))
```

<Callout icon="lightbulb">
  Adjust `temperature`, `max_tokens`, and `top_p` to control response creativity, length, and diversity.
</Callout>

***

## Building Custom OpenAI Assistants

You can tailor assistants to your business needs by focusing on:

1. **Training Data**\
   Fine-tune on domain-specific records or custom corpora to enhance subject-matter accuracy.

2. **Context Handling**\
   Implement memory by storing conversation history, user preferences, or session variables.

3. **Model Parameters**\
   Configure `temperature`, `max_tokens`, and `top_p` for your desired output style.

<Frame>
  ![The image outlines the process of building custom OpenAI assistants, highlighting three key aspects: creating custom assistants, fine-tuning with industry-specific datasets, and designing for context handling.](https://kodekloud.com/kk-media/image/upload/v1752879227/notes-assets/images/Introduction-to-OpenAI-Overview-of-OpenAI-Assistant/custom-openai-assistants-building-process.jpg)
</Frame>

<Callout icon="triangle-alert">
  When fine-tuning with sensitive or personal data, ensure you comply with privacy regulations (e.g., GDPR, HIPAA). Always anonymize PII and validate data sources.
</Callout>

***

## Links and References

* [OpenAI Official Docs](https://platform.openai.com/docs)
* [GPT-4 Model Card](https://platform.openai.com/docs/models/gpt-4)
* [Fine-tuning Guides](https://platform.openai.com/docs/guides/fine-tuning)
* [Code Interpreter Feature](https://platform.openai.com/docs/guides/code-interpreter)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/33f37ca1-e3cd-403b-817f-3fae60617074" />
</CardGroup>
