# n8n Marketing Team Agents Combined Build

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Multi-Workflow-Advanced-Build-Long/n8n-Marketing-Team-Agents-Combined-Build/page

Guide to building an n8n marketing master workflow that orchestrates AI agents and sub-workflows for Slack triggered image, video, caption, blog creation and optional research.

In this lesson we combine previously covered concepts and sub-workflows into a single master workflow that orchestrates multiple AI agents and tools. The goal: let a single Slack command trigger image/video generation, caption writing, blog post creation, and optional research — all coordinated by a Marketing Team Master Agent running in n8n.

<Frame>
  <img alt="The image depicts a workflow diagram in a software interface called n8n, showing interconnected components for automating marketing tasks using tools like Slack, GPT-5 LLM, and various agents for content creation and research." />
</Frame>

Overview

* Trigger: Slack message in a dedicated marketing channel.
* Orchestrator: Marketing Team Master Agent (LLM-based).
* Tools/sub-workflows: text-to-image, text-to-video, caption writer, blog copywriter, plus optional research (Perplexity).
* Output channels: Slack posts, Google Docs links, or other delivery nodes.

Slack trigger and channel setup
The workflow begins with a Slack trigger tied to a dedicated channel and bot integration. For this demo the channel and bot are named `marketing-agent-team-demo`, allowing team members to message the master agent directly.

<Frame>
  <img alt="The image shows a Slack interface with the &#x22;Integrations&#x22; tab open in the #marketing-team channel, displaying options for adding automation and apps." />
</Frame>

Marketing Team Master Agent
The master agent is an LLM node configured with a system message instructing it to act as the marketing team AI: decide which sub-workflows to call, orchestrate external tools, and return consolidated outputs.

Key responsibilities:

* Parse the user request.
* Optionally call a research tool for up-to-date facts.
* Decide whether to create image(s), video(s), captions, and/or a blog post.
* Call sub-workflows with concise inputs (e.g., `image idea`, `video idea`, `blog post idea`) and consolidate returned outputs for Slack or other channels.

<Frame>
  <img alt="This image shows a software interface for a &#x22;Marketing Team Master Agent&#x22; with parameters and system messages for creating marketing content. The interface includes options for executing nodes and setting mock data." />
</Frame>

Master agent UI and orchestration view
The UI shows the tools available to the master agent and a place to author system messages, mock data, and execution options. The master uses a small toolbox of callable sub-workflows and external APIs to keep responsibilities clear and modular.

<Frame>
  <img alt="The image displays a split-screen interface of a workflow or automation tool with instructions for a marketing AI agent on one side and the corresponding results or outputs on the other. This setup includes details on tools and instructions for creating marketing content." />
</Frame>

Design pattern: modular sub-workflows
All content-creation tasks live in small, focused sub-workflows. Each accepts a minimal, well-defined input and returns its final result to the main workflow. This makes testing and debugging easier and keeps the main agent lightweight.

Summary table of sub-workflows

| Sub-workflow       | Primary input    | Output                   | Typical tech                          |
| ------------------ | ---------------- | ------------------------ | ------------------------------------- |
| Text-to-Image      | `image idea`     | Image URL(s)             | Image API (prompt agent)              |
| Text-to-Video      | `video idea`     | Video URL / job metadata | Veo3 (or other video API)             |
| CaptionWriter      | media URL(s)     | Multiple caption options | Anthropic / chat model                |
| BlogPostCopywriter | `blog post idea` | Google Doc link          | RAG with Pinecone + Doc create/update |

Implementation notes and tooling

* Think / intermediate reasoning: The master agent includes a "Think" option so it can plan multi-step flows before taking action. This is useful for deciding which sub-workflows to call and in what order.
* Short memory: Keep a small context window (e.g., 10 entries) for conversational state and recent requests.
* Research: Connect Perplexity (`https://www.perplexity.ai`) as an optional research tool; the master agent decides whether to call it depending on the user’s request.

<Frame>
  <img alt="The image shows a workflow diagram in n8n, involving various tools and triggers for automating marketing tasks, including Slack integration, GPT-5 LLM operations, research, content creation, and copywriting. The interface includes controls for editing, executing, and evaluating workflows." />
</Frame>

How to adapt sub-workflows for calling (best practices)
When converting a standalone workflow into a called sub-workflow, follow these rules:

* Remove the original trigger (e.g., Chat Message) since input will be supplied by the caller.
* Add an Execute Sub-workflow node with a defined input field such as `video idea` or `image idea`.
* Ensure the internal prompt agent (VideoPrompt/ImagePrompt) uses the passed variable as the user prompt (drag the variable into the prompt field).
* Remove delivery nodes (e.g., Gmail) from the sub-workflow so the final node returns the result (URL or JSON) to the main workflow for consolidation.

<Frame>
  <img alt="The image depicts a workflow setup in n8n, showing a series of connected nodes for automating tasks like receiving messages, video prompting, making HTTP requests, waiting, and sending emails. The interface includes options for execution, evaluation, and navigation." />
</Frame>

> **lightbulb** When using sub-workflows, configure them to return their result as the output of their last node. The main workflow will receive that output as the sub-workflow's response and can then consolidate or forward it (e.g., post the image/video link to Slack, or pass the Google Doc link back to the user).

Passing minimal inputs

* The master workflow should pass only a short descriptive input (e.g., `video idea`) into the Create Video sub-workflow. The sub-workflow’s VideoPrompt node constructs the full prompt for the video API.
* Same for images: send an `image idea` into the Create Image sub-workflow; let the ImagePrompt agent build the API prompt.
* This reduces the cognitive load on the master agent and isolates prompt engineering within each sub-workflow.

Caption writer and blog copywriter

* CaptionWriter: Accepts media output (image/video URL) and returns several caption options. In this demo we used an Anthropic chat model for caption tone and brevity (`https://www.anthropic.com`).
* BlogPostCopywriter: Implemented as a RAG-style agent — it accepts a `blog post idea`, queries a Pinecone vector store for references and style guidance, generates the post, creates/updates a Google Doc in a designated folder, and returns the Doc link.

We populate Pinecone by upserting existing blog posts and brand guidelines (e.g., exported from Google Drive) so generated content follows brand voice.

Main workflow execution example
Below is the overall execution pattern: the master agent receives a Slack trigger, optionally performs research, decides which sub-workflows to call, waits for responses, and then consolidates and posts results back to Slack (or another destination).

<Frame>
  <img alt="The image shows a workflow diagram in an automation tool, featuring a &#x22;Marketing Team Master Agent&#x22; connected to various tools like &#x22;Slack Trigger,&#x22; &#x22;OpenAI Chat Model,&#x22; &#x22;Research Tool,&#x22; and &#x22;Content Creation.&#x22;" />
</Frame>

Example Slack input:
"@marketing-agent-team-demo, create a LinkedIn post about the latest update with [AWS EKS](https://learn.kodekloud.com/user/courses/aws-eks)."

Flow for the example:

1. Slack trigger activates the master agent.
2. Master agent optionally calls Perplexity for recent AWS EKS updates.
3. Master decides to generate an image and captions.
4. Master calls Text-to-Image and CaptionWriter sub-workflows (in parallel or sequence).
5. Once sub-workflows return (image URL + captions), master consolidates and posts back to Slack.

Result preview in Slack

<Frame>
  <img alt="The image shows a Slack channel named &#x22;#marketing-team&#x22; with a message discussing AWS EKS features, including an image preview about &#x22;Amazon EKS: What's New.&#x22;" />
</Frame>

Video generation flow

* The master calls the Text-to-Video sub-workflow and the CaptionWriter in parallel.
* Video generation typically takes longer; the video sub-workflow returns JSON metadata and a final video URL when complete.
* The master consolidates the video URL and caption options, posts them to Slack, and/or provides a download link.

<Frame>
  <img alt="The image is a screenshot of a Slack channel named &#x22;#marketing-team&#x22; where there is a message with a medieval-themed analogy for Kubernetes infrastructure, comparing various components to elements of a kingdom." />
</Frame>

Example video API output (trimmed)

```json theme={null}
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "d66f959b5914abf81629f9130582c3",
    "model": "google/veo3-fast",
    "outputs": [
      "https://d1q70pf5vjyehc.cloudfront.net/"
    ],
    "urls": {
      "get": "https://api.wavespeed.ai/api/v3"
    },
    "has_nsfw_contents": [false],
    "status": "completed",
    "created_at": "2025-08-19T11:34:26Z",
    "error": "",
    "executionTime": 54710,
    "timings": {
      "inference": 54710
    }
  }
}
```

Caption writer output
CaptionWriter returns multiple caption options (e.g., Option 1, Option 2, Option 3). The master packages these with the media link so the marketing team can review and choose.

Blog post generation example
When asked to create a blog post (e.g., "The impact of Kubernetes on enterprise operations"), the master called the BlogPostCopywriter sub-workflow. That workflow used Pinecone for reference retrieval, generated the post, created a Google Doc, and returned the Doc link.

<Frame>
  <img alt="The image is a screenshot of a Slack channel named &#x22;#marketing-team&#x22; discussing Kubernetes concepts with a medieval metaphor, including terms like namespaces, pods, and ingress. There's also a message to create a blog post about the impact of Kubernetes on enterprise operations." />
</Frame>

The generated Google Doc contained a full draft titled "The Impact of Kubernetes in Enterprise Operations in 2025." The overall quality closely follows the reference content uploaded into Pinecone; adjust the RAG prompts and style documents to refine tone and structure.

Kubernetes manifest snippets (example)
Below are example manifest snippets that were referenced in the discussion. These can be used as sample YAML for demonstrations or included in blog drafts.

```yaml theme={null}
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web-service
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-service
spec:
  replicas: 6
  selector:
    matchLabels:
      app: web-service
  template:
    metadata:
      labels:
        app: web-service
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
      containers:
        - name: web
          image: nginx:stable
          ports:
            - containerPort: 80
```

Operational tips and troubleshooting

* Test each sub-workflow independently. When a sub-workflow errors, open it directly to inspect logs and node outputs.
* Configure sub-workflows to return outputs on their final node so the master can consolidate easily.
* Use a short memory for conversational context and a separate persistent store (Pinecone) for long-term references and brand guidelines.
* For production: add retry policies, timeouts, and backoff strategies on nodes that call external APIs.

Next steps
In the next lesson we'll cover error handling and retry strategies, granular timeouts, circuit-breakers for third-party APIs, and advanced observability for production-grade workflows.

Links and references

* Perplexity: [https://www.perplexity.ai](https://www.perplexity.ai)
* Pinecone: [https://www.pinecone.io](https://www.pinecone.io)
* Anthropic: [https://www.anthropic.com](https://www.anthropic.com)
* Google Docs: [https://docs.google.com](https://docs.google.com)
* AWS EKS overview: [https://learn.kodekloud.com/user/courses/aws-eks](https://learn.kodekloud.com/user/courses/aws-eks)

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/ecea31ee-4354-456c-af0b-71a3b5c04c5a/lesson/048dc025-47c4-457d-b16a-50cc3c4a8680)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/ecea31ee-4354-456c-af0b-71a3b5c04c5a/lesson/139a3fc7-2e46-4049-9f3d-ab7790ec9e91)
