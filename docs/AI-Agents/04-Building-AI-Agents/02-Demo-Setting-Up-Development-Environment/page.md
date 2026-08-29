# chatbot_agent.py
from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner

# Load environment variables from .env
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in environment. Add it to your .env file.")

# Define the chatbot agent
agent = Agent(
    name="Police Sketch Artist",
    instructions=(
        "You are a police sketch artist. Collect specific details about the individual being sketched. "
        "Ask follow-up questions to clarify features (hair, eyes, nose, mouth, clothing, build, distinctive marks)."
    ),
)

async def main():
    chat_history: list[tuple[str, str]] = []

    print("Police Sketch Artist chatbot. Type 'history' to view conversation, 'exit' or 'quit' to end.\n")

    while True:
        user_input = input("Provide specific details about the individual: ").strip()
        if not user_input:
            continue

        # Exit commands
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        # Show chat history
        if user_input.lower() == "history":
            print("\n--- Chat History ---")
            if not chat_history:
                print("(no messages yet)")
            for i, (u, b) in enumerate(chat_history, start=1):
                print(f"{i}. You: {u}\n   ChatBot: {b}\n")
            print("---------------\n")
            continue

        # Run the agent and collect the response
        result = await Runner.run(agent, user_input)

        # The agent's response may be in result.final_output or result.output depending on SDK behavior
        response = getattr(result, "final_output", None)
        if response is None:
            response = getattr(result, "output", str(result))

        # Save to history and display
        chat_history.append((user_input, response))
        print("\nChatBot:", response)
        print("To end chat, type 'exit' or 'quit'. Type 'history' to view past conversations.\n")

if __name__ == "__main__":
    asyncio.run(main())
```

What this script does

* Loads environment variables safely via `python-dotenv`.
* Defines an Agent with a role-based instruction set so the model acts like a police sketch artist.
* Runs an asynchronous loop that:
  * Accepts and validates user input.
  * Handles `history`, `exit`, and `quit` commands.
  * Invokes the agent using `await Runner.run(agent, user_input)`.
  * Extracts the agent’s output (`final_output` or `output`) and appends each turn to `chat_history`.
  * Prints the agent response and usage reminders.

Quick command reference

| Command         | Description                                                   |
| --------------- | ------------------------------------------------------------- |
| `history`       | Prints the conversation history collected during this session |
| `exit` / `quit` | Ends the chat session and exits the program                   |

Testing and extending the bot
Try providing details like hair color, facial features, build, clothing, or distinctive marks. The agent should ask clarifying questions to gather a structured description. Once you collect attributes, you can extend the pipeline to call an image generation API (for example, DALL·E) to create sketches from the description.

Example interaction (screenshot)

<Frame>
  <img alt="The image shows a chat interface where a user is describing a person who looks like a Viking to a chatbot. The chatbot prompts for details such as facial features, eyes, nose, mouth, clothing, build, and distinctive marks." />
</Frame>

References and next steps

* OpenAI Agents guide: [https://platform.openai.com/docs/guides/agents](https://platform.openai.com/docs/guides/agents)
* OpenAI Agents SDK (examples & Quickstart): [https://github.com/openai/agents](https://github.com/openai/agents)
* python-dotenv: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
* Pydantic docs: [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)
* Images guide (DALL·E): [https://platform.openai.com/docs/guides/images](https://platform.openai.com/docs/guides/images)

Thank you for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/145dc5be-8a43-4ff3-ba90-7d93e142a799/lesson/cbe95d6e-1e59-4beb-9638-bbc5621f4651" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents/module/145dc5be-8a43-4ff3-ba90-7d93e142a799/lesson/51ff8331-399a-48c4-a89d-76d59bd8ee67" />
</CardGroup>


# Demo Setting Up Development Environment

Source: https://notes.kodekloud.com/docs/AI-Agents/Building-AI-Agents/Demo-Setting-Up-Development-Environment/page

Guide to setting up a local Jupyter development environment, securing an OpenAI API key with a .env, and using GitHub for version control and safe commits

Welcome to the first demo lesson.

In this guide you'll set up a local development environment for working with Jupyter Notebook and GitHub, then securely store an OpenAI API key for use in your notebooks. Jupyter Notebook is ideal for step-by-step prototyping, visualization, and interactive documentation — particularly useful for data science, machine learning, and teaching. Pairing Jupyter with GitHub gives you version control, collaboration, and cloud backup so your notebooks remain reproducible and shareable.

This walkthrough covers:

* Installing Anaconda to run Jupyter
* Launching and using Jupyter Notebook (kernels, running cells, common pitfalls)
* Creating a secure `.env` file for your API key and loading it in Python
* Creating a GitHub repository and committing your project safely

***

## 1) Install Anaconda (to run Jupyter)

1. Visit the Anaconda distribution page: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)
2. Download the free distribution for your operating system.
3. You can skip account registration and proceed with the installer.
4. After installation, launch Anaconda Navigator to access Jupyter Notebook and other tools.

<Frame>
  <img alt="The image shows the Anaconda Navigator interface with various applications listed, such as PyCharm and JupyterLab, displaying options to install or launch them." />
</Frame>

***

## 2) Launching Jupyter Notebook

* Start Jupyter Notebook from Anaconda Navigator (or run `jupyter notebook` from a terminal). It opens in your default browser at a local URL such as `http://localhost:8888/tree`.
* Create a project folder: click New → New Folder, rename it (e.g., `Demo Project`) and open it.
* Create a new notebook inside the folder: New → Python 3 (or an available kernel).
* Rename the notebook by clicking the title (e.g., change "Untitled" to `Demo`).

The menu bar contains File, Edit, View, Run, Kernel, Settings, Help. The toolbar provides quick actions: run cell, move cells, cut/copy/paste, restart kernel, etc.

<Frame>
  <img alt="The image shows a Jupyter notebook interface with the &#x22;Run&#x22; menu open, highlighting the &#x22;Run Selected Cell&#x22; option." />
</Frame>

### Kernel & run controls — quick reference

| Action       | What it does                                                                           |
| ------------ | -------------------------------------------------------------------------------------- |
| Interrupt    | Stops currently executing code (useful for infinite loops or long-running operations). |
| Restart      | Restarts the kernel and clears in-memory state (variables, imports).                   |
| Shutdown     | Ends the kernel session.                                                               |
| Run cell (▶) | Executes the current cell and advances depending on the option chosen.                 |

<Callout icon="lightbulb">
  Tip: If your notebook behaves unexpectedly (old variables, mismatched outputs), use Kernel → Restart & Clear Output to get a clean runtime and reproduce results deterministically.
</Callout>

***

## 3) Examples — running cells and managing the kernel

Infinite loop example (run with caution):

```python theme={null}
while True:
    print("Hi")
```

If you execute this, it will continually print until you interrupt the kernel (Kernel → Interrupt or the stop button).

Common error example (Python is case-sensitive):

```python theme={null}
while true:
    print("hi")
```

This raises a `NameError` because `true` (lowercase) is not defined in Python. The correct boolean literal is `True`.

### Cell execution order and kernel state

Cells execute in the kernel's current state. If you modify a later cell but do not re-run it, the kernel will still use the previously executed value.

Example:

```python theme={null}
foo = 1 + 1
print(foo)  # outputs: 2
```

If you later change another cell to:

```python theme={null}
foo = 1 + 1 + 1
