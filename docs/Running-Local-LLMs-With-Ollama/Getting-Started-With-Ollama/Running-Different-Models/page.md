# Running Different Models

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Getting-Started-With-Ollama/Running-Different-Models/page

Explore how to run various vision-capable models using Ollama, including browsing the model registry and utilizing CLI and API for local execution.

````markdown theme={null}
Having installed Ollama and run your first LLaMA 3.2 model locally, it’s time to explore Ollama’s full model registry and try a vision-capable model. In this guide, we’ll:

- Browse and filter models on the Ollama website  
- Examine a LLaVA multimodal model’s specs  
- Run vision-enabled models locally via CLI and API  
- Compare other image-capable options  

---

## 1. Browse Ollama’s Model Registry

Head over to the [Ollama website](https://ollama.com) and click **Models** in the navigation bar. You’ll see a list of supported AI models complete with architecture, parameter count, and quantization settings:

<Frame>
![The image shows a webpage from Ollama, displaying a list of AI models such as "deepseek-r1" and "llama3.3" with details about their parameters and performance. There are options to filter models by categories like Embedding, Vision, and Tools.](https://kodekloud.com/kk-media/image/upload/v1752883726/notes-assets/images/Running-Local-LLMs-With-Ollama-Running-Different-Models/ollama-ai-models-list-webpage.jpg)
</Frame>

Scroll down and select the **Vision** category. The top entry is a LLaMA-based vision model (LLaVA). Click it to view its details.

---

## 2. Inspect the Vision Model Specification

On the model detail page, you’ll find:

| Model   | Parameters | Quantization | Use Case               |
|---------|------------|--------------|------------------------|
| LLaVA   | 7.24 B     | Q4_0 (text)  | Image understanding    |
| CLIP    | 312 M      | F16          | Vision encoder support |

Below is the YAML metadata for LLaVA:

```yaml
model:
  arch: llama
  parameters: 7.24B
  quantization: Q4_0
projector:
  arch: clip
  parameters: 312M
  quantization: F16
params:
  stop: ["[INST]", "[/INST]"]
template: "[INST] {{ if .System }}{{ .System }} {{ end }}{{ .Prompt }}…"
license: "Apache License Version 2.0, January 2004"
```text

<Callout icon="lightbulb" color="#1CB2FE">
You can pass images to this model in your prompts and receive detailed descriptions. Below we’ll cover both the interactive CLI and the local API approach.
</Callout>

---

## 3. Using CLI and Local API

### Interactive CLI

```bash
