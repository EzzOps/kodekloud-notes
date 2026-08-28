# Self Hosting Locally With Docker Desktop and Ollama

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Optional-Setups/Self-Hosting-Locally-With-Docker-Desktop-and-Ollama/page

Guide to self-hosting n8n with Docker Desktop and Ollama, using a starter kit to run local LLMs, Postgres, and Qdrant via Docker Compose.

In this lesson you'll learn how to run n8n locally using Docker Desktop and the n8n-io/self-hosted-ai-starter-kit repository, which includes Ollama as a local LLM runtime. Follow the steps below to clone the starter kit, configure environment variables, and bring up the stack with Docker Compose.

<Frame>
  <img alt="The image shows a GitHub repository for a &#x22;Self-hosted AI Starter Kit&#x22; by n8n, featuring various files and an overview of the project's purpose. It includes sections for code, pull requests, discussions, and other repository details." />
</Frame>

Overview

* Clone the n8n self-hosted AI starter kit repository.
* Copy and edit the `.env` file to configure secrets and host settings.
* Start the stack with Docker Compose using the profile appropriate for your hardware.
* Open n8n at [http://localhost:5678](http://localhost:5678) and create an owner account.
* Inspect and run the demo workflow that uses a local Ollama model.

Prerequisites

| Requirement                            | Notes / Links                                                                                                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker Desktop                         | Install for Windows or macOS: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)                        |
| Git                                    | Needed to clone the repository                                                                                                                        |
| (Optional) Ollama installed separately | If you prefer managing Ollama outside the compose stack, install via [https://ollama.ai/docs](https://ollama.ai/docs) and set `OLLAMA_HOST` in `.env` |

<Frame>
  <img alt="The image shows the Docker website with an emphasis on downloading Docker Desktop for different platforms, including Mac (Apple Silicon and Intel) and Windows (AMD64). It also includes navigation options and a banner about building AI agents." />
</Frame>

Step 1 — Clone the repo and create your `.env`

```bash theme={null}
git clone https://github.com/n8n-io/self-hosted-ai-starter-kit.git
cd self-hosted-ai-starter-kit
cp .env.example .env
