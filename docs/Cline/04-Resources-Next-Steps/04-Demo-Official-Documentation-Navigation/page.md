# Create the MCP directory
mkdir -p "/Users/jeremy/Documents/Cline/MCP"

# Clone the Ollama MCP server repository
git clone https://github.com/NightTrek/Ollama-mcp.git "/Users/jeremy/Documents/Cline/MCP/Ollama-mcp"

# Change into the project
cd "/Users/jeremy/Documents/Cline/MCP/Ollama-mcp"
```

Install dependencies (preferred `pnpm`, fallback `npm`):

```bash theme={null}
# Preferred
pnpm install

# If pnpm is not available, fallback
npm install

# Build step (use the repo's scripts)
npm run build
```

Console output example when `pnpm` is missing:

```console theme={null}
(venv) jeremy@MACSTUDIO Ollama-mcp % pnpm install
zsh: command not found: pnpm
(venv) jeremy@MACSTUDIO Ollama-mcp %
```

> **warning** If Cline updates your client MCP settings file, back it up first. Make sure the `args` path points to the built entrypoint (`build/index.js`) and that any environment variables (like `OLLAMA_HOST`) use the correct host/port for your environment.

### Example MCP settings entry

Cline will propose adding an MCP server entry to your client settings JSON. Below is a canonical example—adjust paths and env values for your machine. Place this in your Cline settings file (path depends on platform and Cline configuration):

```json theme={null}
{
  "mcpServers": {
    "github.com/NightTrek/Ollama-mcp": {
      "command": "node",
      "args": ["/Users/jeremy/Documents/Cline/MCP/Ollama-mcp/build/index.js"],
      "env": {
        "OLLAMA_HOST": "http://127.0.0.1:11434"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Verifying the MCP server from Cline

After installation and configuration, Cline can start the MCP server and call its tools. Example interactions:

* List installed local models (tool returns structured JSON):

```json theme={null}
{
  "name": "llama3.2:1b"
}
```

* Request model details (tool returns a human-readable summary):

```text theme={null}
Model
  architecture    llama
  parameters      1.2B
  context length  131072
  embedding length 2048
  quantization    Q8_0

Capabilities
  completion
  tools

License
  LLAMA 3.2 COMMUNITY LICENSE AGREEMENT
  Llama 3.2 Version Release Date: September 25, 2024
  ...
```

If Cline receives these responses, the Ollama MCP server is reachable and functioning. From there, any tools exposed by the MCP server are usable directly within Cline (for example, querying local Ollama models through Cline’s tool interface).

## Quick reference

| Task              | Command / Setting                                                                                      | Notes                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Create MCP folder | `mkdir -p "/Users/jeremy/Documents/Cline/MCP"`                                                         | Use your own local path                                                                 |
| Clone repo        | `git clone https://github.com/NightTrek/Ollama-mcp.git "/Users/jeremy/Documents/Cline/MCP/Ollama-mcp"` | Matches marketplace package source                                                      |
| Install deps      | `pnpm install` or `npm install`                                                                        | Cline tries `pnpm` first, then `npm`                                                    |
| Build             | `npm run build`                                                                                        | Use repo-provided build script                                                          |
| MCP settings      | See JSON snippet above                                                                                 | Ensure `args` points to built `index.js` and env vars (e.g., `OLLAMA_HOST`) are correct |
| Test              | Use Cline’s tool interface to list models and show details                                             | Successful responses confirm configuration                                              |

## Checklist (final)

* Ensure package manager availability; Cline auto-falls back if needed.
* Back up your client MCP settings before any changes.
* Confirm MCP settings JSON points to the repository’s built entrypoint and includes required `env` values.
* Test by listing models and requesting model details from Cline.

This workflow makes it straightforward to discover, install, and integrate MCP servers from the Cline Marketplace into your local Cline environment—enabling new tools and capabilities with minimal manual configuration.

- [Watch Video](https://learn.kodekloud.com/user/courses/cline/module/994745b4-8b52-4c0c-ae6c-1afb232520d7/lesson/16a981c6-c803-41de-bfa5-111a6af88da6)


# Demo Official Documentation Navigation

Source: https://notes.kodekloud.com/docs/Cline/Resources-Next-Steps/Demo-Official-Documentation-Navigation/page

Concise guide to Cline official documentation covering model selection, context windows, recommended tooling, provider integrations, local model hardware, and production deployment guidance.

Below is a concise, reorganized guide to the official Cline documentation—highlighting the sections most useful when designing production systems and experimenting with models locally. This version keeps the original sequence of screenshots and examples while improving clarity and SEO by emphasizing key topics: model selection, context windows, recommended tooling, provider-specific guides, and running local models.

## Where docs might live on your machine

Example local documentation paths:

| Operating System | Example Path                               |
| ---------------- | ------------------------------------------ |
| macOS            | `/Users/[your-username]/Documents/Cline`   |
| Windows          | `C:\Users\[your-username]\Documents\Cline` |

These paths are examples only; adjust them to match your environment.

## Model selection and understanding context windows

The official docs contain a clear, practical explanation of context windows and how they affect model choice. Use this guidance to pick models that balance cost, latency, and the context size you need for tasks like long-form summarization, document question answering, or multimodal input.

<Frame>
  <img alt="A dark-themed webpage or documentation titled &#x22;Model Selection Guide&#x22; showing a section on &#x22;Understanding Context Windows&#x22; with explanatory text and a left navigation menu of other topics. The page lists context window sizes for various AI models and includes a right-hand table of contents." />
</Frame>

Key considerations:

* Context size: choose a model whose context window fits your input plus expected output.
* Cost vs. capability: larger-context models typically cost more; consider chunking/summary strategies for very long inputs.
* Use-case fit: some models are optimized for coding, others for dialogue or vision.

## Recommended tech stack for getting started

The docs include a recommended stack—editors, hosting, and common frameworks—so you can bootstrap a Cline-based project quickly.

<Frame>
  <img alt="A dark-themed documentation webpage titled &#x22;Our Favorite Tech Stack&#x22; showing a recommended development stack for new Cline users (2025), listing tools like VS Code, GitHub, Next.js, Tailwind, TypeScript, and Supabase. The layout has a left navigation menu, main content in the center, and a right-side table of contents." />
</Frame>

Typical recommendations:

* Editor: VS Code
* Version control / hosting: GitHub (or Git providers of your choice)
* Front-end: Next.js + Tailwind CSS + TypeScript
* Back-end / storage: Supabase, or any managed DB / object store

## Hosting, production models, and operational notes

The docs explain production considerations—recommended production models, example cost guidance, and deployment patterns (e.g., model choice for inference latency and throughput). They also discuss operational best practices like checkpointing client memory and “plan and act” workflows.

If you need provider-specific instructions, the docs include guides for integrating alternative providers.

## Provider-specific example: xAI Grok (API keys and models)

Cline’s documentation contains provider-specific guides—here’s the Grok example showing steps for obtaining API keys and a list of supported Grok model names.

<Frame>
  <img alt="A dark-themed documentation webpage for xAI (Grok), showing a left navigation menu and a right-side table of contents. The main content displays &#x22;Getting an API Key&#x22; steps and a list of supported Grok models." />
</Frame>

Example Grok model names listed in the docs:

```text theme={null}
grok-2-vision-latest - xAI's Grok-2 Vision model - latest version with image support and 32K context window
grok-2-vision - xAI's Grok-2 Vision model with image support and 32K context window
grok-2-vision-1212 - xAI's Grok-2 Vision model (version 1212) with image support and 32K context window
grok-vision-beta - xAI's Grok Vision Beta model with image support and an 8K context window
grok-beta - xAI's Grok Beta model (legacy) with a 131K context window
```

Tip: match the Grok model's context window to your task; use smaller models for cost-sensitive, short-context tasks, and larger-context models when you need to process long documents or multimodal inputs.

## Running local models — hardware requirements and trade-offs

The docs include a detailed “Hardware Requirements” section that lists recommended GPU, RAM, SSD, and cooling. There’s also a comparison table of common model sizes (7B, 14B, 32B, 70B) and their typical capabilities.

<Frame>
  <img alt="A dark-themed documentation page titled &#x22;Hardware Requirements&#x22; listing recommended GPU, RAM, SSD and cooling, plus a table comparing model sizes (7B, 14B, 32B, 70B) and their capabilities. The screenshot also shows left and right navigation panels for the docs." />
</Frame>

Considerations when running locally:

* Hardware cost and availability vs. managed inference costs
* Precision trade-offs (e.g., FP16 / quantization)
* Memory limits and model sharding strategies
* Cooling and long-running inference reliability

<Frame>
  <img alt="A dark-themed documentation webpage screenshot titled &#x22;Read Me First&#x22; and &#x22;Running Local Models with Cline: What You Need to Know,&#x22; showing explanatory text about why local models are different with a bulleted list. Navigation menus appear in a left sidebar and a page outline on the right." />
</Frame>

> **warning** Running local models requires careful hardware planning. Ensure your GPU, RAM, and storage match the model size you intend to use, and test performance characteristics (latency, memory usage) before moving to production.

## Example minimal project layout referenced by the docs

A minimal example layout from the docs:

```text theme={null}
cline_docs
projectBrief.md
.clinerules
```

This gives you a starting scaffold—add your source code, configuration, and CI/CD files as needed.

> **lightbulb** Bookmark the official docs for ongoing updates and details: [https://docs.agentic.cline.bot](https://docs.agentic.cline.bot). The documentation is actively maintained and is the best source for model names, context window guidance, provider integrations, and hardware notes.

## Quick links and references

* Official docs: [https://docs.agentic.cline.bot](https://docs.agentic.cline.bot)
* Provider guides and model lists: consult each provider’s section in the official docs (e.g., Grok integration)
* Local model guidance: review “Read Me First” and “Running Local Models” before attempting large-model local deployments

This reorganized summary preserves the original screenshots and sequence while clarifying the key decision points: which model to pick, what tooling to use, how to integrate alternate providers, and what to consider when running models locally.

- [Watch Video](https://learn.kodekloud.com/user/courses/cline/module/994745b4-8b52-4c0c-ae6c-1afb232520d7/lesson/d3abf89a-c788-41ca-815c-bdda925c9035)
