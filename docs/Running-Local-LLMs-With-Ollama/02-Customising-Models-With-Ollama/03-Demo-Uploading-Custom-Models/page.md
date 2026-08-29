# Demo Uploading Custom Models

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Customising-Models-With-Ollama/Demo-Uploading-Custom-Models/page

Uploading custom models to the Ollama Model Registry simplifies sharing and version control for your team, similar to using Docker Hub for container images.

Distributing Modelfiles for every update can be cumbersome. By uploading custom models to the [Ollama Model Registry](https://ollama.com/), your team can pull the latest version directly—just like using [Docker Hub](https://hub.docker.com) for container images.

In this tutorial, we’ll cover how to:

1. Set up your Ollama account and trust relationship
2. Tag and copy your local model
3. Push the tagged model to the registry
4. Pull and verify your custom model

***

## 1. Set Up Your Ollama Account and Trust Relationship

1. Create an Ollama account at [https://ollama.com/](https://ollama.com/) and sign in.
2. Go to **Settings** → **Ollama Key**.
3. Locate your public SSH key on your local machine:

| OS      | Public Key Path                              |
| ------- | -------------------------------------------- |
| macOS   | `~/.ollama/id_ed25519.pub`                   |
| Linux   | `~/.ollama/id_ed25519.pub`                   |
| Windows | `C:\Users\<username>\.ollama\id_ed25519.pub` |

4. Display and copy your public key:

```bash theme={null}
cat ~/.ollama/id_ed25519.pub
