# Demo Ollama Setup and Walkthrough

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Introduction/Demo-Ollama-Setup-and-Walkthrough/page

Guide to installing and using Ollama to run and manage open source large language models locally, including installation, CLI and GUI workflows, model commands, and local API usage.

In this lesson we'll walk through installing Ollama and using it to run large language models (LLMs) locally. Ollama lets you download open-source models and run them on your machine instead of relying on cloud-hosted LLMs. These models behave similarly to GPT-family models: you can send prompts interactively, run them as a server with an HTTP API, or call them from scripts and applications.

Key benefits:

* Run models locally for lower latency and data privacy.
* Use CLI or GUI workflows to pull, run, and manage models.
* Integrate local models into apps via a local API (default: `127.0.0.1:11434`).

Supported platforms: macOS, Linux (including WSL), and Windows. Installers: DMG for macOS, EXE for Windows, and a curl-based shell installer for Linux.

## Install (Linux / WSL)

On Linux or Windows Subsystem for Linux, install with the curl installer:

```bash theme={null}
curl -fsSL https://ollama.com/install.sh | sh
```

> **lightbulb** The installer will prompt for `sudo` when needed and installs Ollama under `/usr/local` by default. Running this command inside WSL is the fastest way to get set up on Windows using the Windows Subsystem for Linux environment.

A typical install run looks like this:

```bash theme={null}
$ curl -fsSL https://ollama.com/install.sh | sh
>>> Installing ollama to /usr/local
[sudo] password for jeremy:
>>> Downloading Linux amd64 bundle
######################################################################## 100.0%
>>> Creating ollama user...
>>> Adding ollama user to render group...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
Created symlink /etc/systemd/system/default.target.wants/ollama.service → /etc/systemd/system/ollama.service.
Nvidia GPU detected.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
```

After installation, run `ollama` to view the top-level help and available subcommands.

## Command-line overview

Running the `ollama` command with no arguments prints the high-level help and available commands:

```bash theme={null}
$ ollama
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  signin      Sign in to ollama.com
  signout     Sign out from ollama.com
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.
```

## Windows / GUI installer

The macOS and Windows installers include an optional GUI. The GUI lets you browse models, view metadata, and download models with a few clicks. The installer keeps your models if you upgrade an existing install.

<Frame>
  <img alt="The image shows the installation progress of &#x22;Ollama&#x22; on a computer, with a progress bar and file extraction details. A cartoon llama graphic is displayed in the top right corner." />
</Frame>

## Model selection (GUI)

If you prefer a graphical workflow, the GUI lets you preview model descriptions, inspect sizes and parameters, and download models directly.

<Frame>
  <img alt="The image displays a software interface with a selection menu for AI models, accompanied by a simple cartoon doodle resembling a llama." />
</Frame>

## Common commands

Use the table below as a quick reference for common Ollama commands and their use cases.

|               Command | Purpose                                              | Example                          |
| --------------------: | ---------------------------------------------------- | -------------------------------- |
|         `ollama list` | List models downloaded to your machine               | `ollama list`                    |
|           `ollama ps` | Show running models and resource usage               | `ollama ps`                      |
|         `ollama pull` | Download a model without running it                  | `ollama pull qwen3:0.6b`         |
|          `ollama run` | Download (if needed) and start a model interactively | `ollama run qwen3:0.6b`          |
| `ollama show <model>` | Inspect model metadata and runtime parameters        | `ollama show deepseek-r1:latest` |
|  `ollama stop <name>` | Stop a running model                                 | `ollama stop qwen3:0.6b`         |

## Listing installed models

From the CLI, `ollama list` shows models you have already downloaded:

```bash theme={null}
C:\Users\jerem>ollama list
NAME                ID              SIZE     MODIFIED
deepseek-r1:latest  6995872bfe4c    5.2 GB   22 hours ago
gemma3:4b           a2af6cc3eb7f    3.3 GB   22 hours ago
```

## Inspecting a model

Use `ollama show <model>` to view architecture, parameter counts, context length, quantization, and default runtime parameters. Note: some models include special stop tokens that look like angle-bracket tokens — always display or reference those tokens inside code formatting to avoid MDX parsing issues.

```bash theme={null}
C:\Users\jerem>ollama show deepseek-r1:latest
Model
  architecture          qwen3
  parameters            8.2B
  context length        131072
  embedding length      4096
  quantization          Q4_K_M

Capabilities
  completion
  thinking

Parameters
  stop                  "<| begin_of_sentence |> "
  stop                  "<| end_of_sentence |> "
  stop                  "<| User |> "
  stop                  "<| Assistant |> "
  temperature           0.6
  top_p                 0.95

License
  MIT License
  Copyright (c) 2023 DeepSeek
```

## Downloading and running models

You can either `pull` a model to download it only, or `run` a model to download (if necessary) and start an interactive session:

```bash theme={null}
C:\Users\jerem>ollama pull qwen3:0.6b
