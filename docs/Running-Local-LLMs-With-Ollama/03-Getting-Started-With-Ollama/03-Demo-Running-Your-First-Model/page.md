# Demo Running Your First Model

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Getting-Started-With-Ollama/Demo-Running-Your-First-Model/page

This guide explains how to run Meta's Llama 3.2 large language model locally using the Ollama application and CLI.

Assuming you’ve already installed the Ollama application and CLI on your machine, this guide walks you through running your first large language model (LLM)—Meta’s Llama 3.2—entirely offline. Ollama supports many popular models, so feel free to substitute your preferred one.

## Prerequisites

* Ollama CLI installed and configured
* At least 4 GB of free RAM
* \~2 GB of disk space for the Llama 3.2 model
* A modern terminal (macOS, Linux, or WSL on Windows)

> **triangle-alert** Downloading and storing LLMs locally can consume significant disk space and memory. Ensure you have adequate resources before proceeding.

## 1. Pulling and Running the Model

Open your terminal and execute:

```bash theme={null}
ollama run llama3.2
```

Since this is your first run, Ollama will fetch the model from the registry—similar to Docker pulling an image:

```bash theme={null}
> ollama run llama3.2
pulling manifest
pulling dde5aa3fc5ff... 100%
pulling 966de95ca8a6... 100%
...
verifying sha256 digest
writing manifest
success
```

Once the download completes, Ollama verifies integrity, writes the manifest, and presents an interactive `>>>` prompt.

> **lightbulb** All inference happens locally—your data remains on your device and no internet connection is needed after download.

## 2. Basic Interaction

At the `>>>` prompt, type any message:

```bash theme={null}
>>> hey! how are you feeling?
```

You should see a response like:

```text theme={null}
I’m just a language model, I don’t have feelings or emotions like humans do. However, I’m functioning properly and ready to help with any questions or tasks you may have! How about you? How’s your day going so far?
>>> send a message (/?) for help
```

## 3. Experimenting with Prompts

Try a creative prompt:

```bash theme={null}
>>> Compose a poem on DevOps.
```

The model generates a multi-paragraph poem in seconds. To discover built-in session commands, enter:

```bash theme={null}
>>> /?
```

### Available Session Commands

| Command         | Description                       |
| --------------- | --------------------------------- |
| `/set`          | Set session variables             |
| `/show`         | Display model information         |
| `/load <model>` | Load a different model or session |
| `/save <model>` | Save your current session state   |
| `/clear`        | Clear conversation context        |
| `/bye`          | Exit the interactive session      |
| `/?` or `/help` | Show help for commands            |

Use triple quotes (`"""`) to start a multi-line message.

## 4. Resetting Context

To clear memory of previous interactions:

```bash theme={null}
>>> /clear
Cleared session context
>>> send a message (/?) for help
```

Now the model won’t recall what you asked before clearing. This is useful for isolated tests or debugging prompts.

## 5. Performing Calculations

Ollama LLMs can even handle simple math. For example:

```bash theme={null}
>>> What is 12% compound interest on 5000 over 5 years?
```

Sample response:

```text theme={null}
FV = PV × (1 + r)^n

Where:
  FV = Future Value
  PV = Present Value = $5000
  r  = Annual rate = 12% = 0.12
  n  = Number of years = 5

Calculation:
  FV = $5000 × (1 + 0.12)^5
     ≈ $8,811.71
```

## 6. Exiting the Session

When you’re finished, leave the chat with:

```bash theme={null}
>>> /bye
Goodbye!
```

You’ll return to your normal terminal prompt.

***

You’ve now run and interacted with a large language model locally using Ollama. Explore other models, tweak prompts, and enjoy full offline inference for enhanced privacy and performance. Happy experimenting!

- [Watch Video](https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/836a96fe-9951-42b6-83ba-a602299c87c9/lesson/a9c4c459-714f-46a1-98c4-d113115b572a)
