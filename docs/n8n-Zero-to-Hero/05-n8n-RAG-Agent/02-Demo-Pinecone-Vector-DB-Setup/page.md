# Example output:
# Docker Compose version v2.23.3
```

Helpful links:

* Docker docs: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
* Docker Compose CLI plugin: [https://docs.docker.com/compose/cli-command/](https://docs.docker.com/compose/cli-command/)

## 4 — Clone the repository and configure environment

Clone the n8n self-hosted AI starter kit and prepare the environment file:

```bash theme={null}
git clone https://github.com/n8n-io/self-hosted-ai-starter-kit
cd self-hosted-ai-starter-kit
cp .env.example .env
```

Edit `.env` and set relevant variables. Minimum example (only key variables shown):

```text theme={null}
POSTGRES_USER=root
POSTGRES_PASSWORD=password
POSTGRES_DB=n8n

N8N_ENCRYPTION_KEY=super-secret-key
N8N_USER_MANAGEMENT_JWT_SECRET=even-more-secret
N8N_DEFAULT_BINARY_DATA_MODE=filesystem

# Disable secure cookie for demo on a non-HTTPS public IP.
N8N_SECURE_COOKIE=false

# For Mac users running OLLAMA locally
# OLLAMA_HOST=host.docker.internal:11434
```

Notes:

* Ensure variable names are `N8N_` prefixed and `POSTGRES_DB` is `n8n`.
* `N8N_SECURE_COOKIE=false` is used here because the demo uses HTTP. For production with HTTPS, set `N8N_SECURE_COOKIE=true`.
* Replace `N8N_ENCRYPTION_KEY` and `N8N_USER_MANAGEMENT_JWT_SECRET` with strong, unique secrets.

## Quick reference — Ports and services

| Service  |    Default Port | Notes                                        |
| -------- | --------------: | -------------------------------------------- |
| n8n UI   |          `5678` | HTTP access in demo; use HTTPS in production |
| Ollama   |         `11434` | Local LLM server (if enabled in compose)     |
| Qdrant   | `6333` / `6334` | Vector DB used by starter kit                |
| Postgres |          `5432` | Database used by n8n                         |

## 5 — Start the stack with Docker Compose

Start services using the Compose profile included in the repo:

```bash theme={null}
docker compose --profile cpu up -d
```

This command pulls images and creates volumes. It may take several minutes (n8n, postgres, ollama, qdrant, etc.). Verify containers:

```bash theme={null}
docker ps
```

Example output (IDs and images will differ):

```text theme={null}
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                 PORTS                                  NAMES
c5549fabe571   n8nio/n8n:latest              "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes           0.0.0.0:5678->5678/tcp                 n8n
653b4f492de6   postgres:16-alpine            "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes (healthy)  5432/tcp                               self-hosted-ai-starter-kit_postgres-1
3bc8a2aeb73b   ollama/qdrant                 "/start-service.sh"      2 minutes ago   Up 2 minutes           0.0.0.0:6333->6333/tcp, 6334/tcp       qdrant
1f6b0c27bd91   ollama/ollama:latest          "/bin/ollama serve"      2 minutes ago   Up 2 minutes           0.0.0.0:11434->11434/tcp               ollama
```

Troubleshooting:

* Use `docker compose logs -f` or `docker compose logs <service>` to inspect startup issues.
* Ensure sufficient disk and CPU on the instance; Ollama and Qdrant are resource-intensive.

## 6 — Access n8n in the browser

Open:

```text theme={null}
http://<PUBLIC_IP>:5678
```

Replace `<PUBLIC_IP>` with your EC2 instance public IPv4 address. On first access you will be prompted to create an owner account (email, first name, last name, password).

<Frame>
  <img alt="The image shows a setup page for creating an owner account on n8n, requiring email, first name, last name, and password details. There's also an option to receive security and product updates." />
</Frame>

Once signed in, you will see the n8n dashboard and a default demo workflow — the same n8n experience but now running on your EC2 instance. Ollama and the other services in the repo are available to workflows as configured.

Monitor EC2 resource usage (CPU, network, disk) from the EC2 console to observe the impact of running these services.

<Frame>
  <img alt="The image shows an Amazon EC2 dashboard displaying the details and monitoring graphs for a running instance labeled &#x22;n8n-demo.&#x22; It includes metrics such as network packets, bytes, and CPU credit usage." />
</Frame>

Here is an example workflow that uses a Chat Trigger, a basic LLM chain, and an Ollama chat model — components you can test once Ollama is running.

<Frame>
  <img alt="The image shows a workflow editor interface with components connected in a sequence, including a &#x22;Chat Trigger,&#x22; &#x22;Basic LLM Chain,&#x22; and &#x22;Ollama Chat Model.&#x22; The layout is part of a software tool for creating automated processes." />
</Frame>

## Closing notes

* This walkthrough demonstrates a simple self-hosted n8n setup on EC2 using Docker Compose. If you prefer a managed service, consider [n8n Cloud](https://n8n.io/cloud).
* For production:
  * Terminate public-only SSH/n8n access; restrict by IP or use a bastion/VPN.
  * Enable HTTPS (reverse proxy, load balancer, or TLS termination).
  * Use secure secret management, backups, and monitoring/alerts.
* Learn more:
  * Docker docs: [https://docs.docker.com/](https://docs.docker.com/)
  * AWS EC2: [https://docs.aws.amazon.com/ec2/](https://docs.aws.amazon.com/ec2/)
  * n8n self-hosted starter kit: [https://github.com/n8n-io/self-hosted-ai-starter-kit](https://github.com/n8n-io/self-hosted-ai-starter-kit)
  * KodeKloud Docker course: [https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner)
  * KodeKloud EC2 course: [https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

If you want, I can provide a step-by-step production-ready recipe (HTTPS, domain, automated backups, and secure security group rules).

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/ec070482-ed97-417b-8105-a45836512736/lesson/6f8e5d55-d07b-4911-a899-aae559c93935)


# Demo Pinecone Vector DB Setup

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-RAG-Agent/Demo-Pinecone-Vector-DB-Setup/page

Guide to automating Google Drive document ingestion with n8n, chunking and embedding text using OpenAI, and upserting vectors into Pinecone for RAG-style retrieval.

Before you build a RAG (retrieval-augmented generation) AI agent that queries a contextual knowledge base, you need to store your document repository as vectors in a vector database. This guide shows how to automate that process using n8n to download files from Google Drive, chunk them, generate embeddings with OpenAI, and upsert vectors into Pinecone.

<Frame>
  <img alt="The image shows a workflow diagram in a software interface with nodes connected to perform tasks, including a file upload trigger, looping over items, getting documents from Google Drive, using OpenAI for embeddings, and storing vectors in Pinecone." />
</Frame>

Overview

* Provider examples: Pinecone, Supabase. This walkthrough uses Pinecone.
* Goal: Let team members drop files into a Google Drive folder and have n8n automatically download, chunk, embed, and upsert them into a Pinecone index.
* High-level workflow:
  * Google Drive trigger watches a folder for new files.
  * Loop node processes each file individually.
  * Google Drive download node retrieves the file in binary.
  * The document is split into chunks, embedded with OpenAI, and upserted into Pinecone.

Why use a vector database?

* Traditional SQL/datastore systems handle exact-match queries.
* Vector DBs like Pinecone store embeddings and perform similarity search to find semantically similar content — ideal for retrieval in RAG agents.

What is an embedding?

* An embedding is a numeric vector representing semantic meaning of text, images, or audio.
* Embeddings act like coordinates in a high-dimensional space; semantically related items are close to one another.

Workflow components

| Node / Component                  |                                Purpose | Notes                                                        |
| --------------------------------- | -------------------------------------: | ------------------------------------------------------------ |
| Google Drive Trigger              |           Detect new files in a folder | Polling-driven; choose a short interval for faster ingestion |
| Loop Over Items                   |  Process multiple uploads individually | Ensures each file is separately chunked & upserted           |
| Google Drive — Download File      |         Retrieve file in binary format | Binary preferred for downstream loaders                      |
| Default Data Loader               | Auto-detect file type and extract text | Supports PDFs, Word docs, images (OCR), etc.                 |
| Recursive Character Text Splitter |     Break text into overlapping chunks | Preserves context using chunk size and overlap               |
| Embeddings (OpenAI)               |              Produce numerical vectors | Use same model as Pinecone index                             |
| Pinecone Vector Store             |           Upsert vectors into an index | Requires index and API key                                   |

The workflow starts with a file upload trigger that monitors a specific Google Drive folder for new files.

<Frame>
  <img alt="This image shows a software interface for setting up a &#x22;File Upload Trigger&#x22; with parameters including folder selection, polling mode, and options for changes involving a specific folder." />
</Frame>

Typical trigger settings

* Poll the folder every minute for near-real-time ingestion.
* Download files in `binary` format (required by the default data loader used later).

Handle multiple uploads
Because users may upload several files at once, add a Loop Over Items node to iterate over each file and process them individually. This guarantees each document is chunked and upserted as a separate set of vectors.

Pinecone Vector Store node — common attachments

* Embeddings node (OpenAI embeddings in this example).
* Default Data Loader to handle varying file formats (PDF, DOCX, images).
* Recursive Character Text Splitter to slice documents into semantically sensible, overlapping chunks.

The default data loader accepts `binary` or JSON input and prepares the text for embedding. The Recursive Character Text Splitter divides large text blocks into overlapping chunks, attempting to preserve semantic integrity across chunk boundaries.

<Frame>
  <img alt="The image shows a software interface with a &#x22;Recursive Character Text Splitter&#x22; configuration, including parameters for chunk size and overlap. There are sections for inputs on the left and an output section on the right." />
</Frame>

Key splitter settings

* Chunk size: maximum characters per chunk (e.g., `500`).
* Chunk overlap: characters overlapping between chunks (e.g., `50`) to maintain context.

> **lightbulb** Start with a chunk size around `400–700` characters and an overlap of `10–15%`. Adjust based on document structure and downstream model prompt length—smaller chunks increase retrieval precision but can increase vector count and cost.

Step-by-step: Build this in n8n

1. Google Drive Trigger

* Add a Google Drive node and set it to watch your chosen folder (example: "Pinecone Folder").
* Trigger on `File created` and set polling to `1 minute`.
* Test by uploading a sample file (e.g., a PDF SOP for a fictional airline "AirNova"). The trigger should detect the upload and start the workflow.

2. Loop Over Items

* Add a Loop Over Items node so multiple uploaded files are processed one at a time.
* For single-file scenarios, batch size `1` is typical.

3. Google Drive — Download File

* Use the Google Drive `Download File` node.
* Supply the file ID (or `webContentLink` per node requirements) from the trigger as input to download the file in `binary`.
* Execute this step to verify the file is retrieved and opens correctly in downstream nodes.

4. Pinecone Vector Store — Add Documents to Vector Store

* Add a Pinecone Vector Store node and choose the `Add Documents to Vector Store` action.
* Required: a Pinecone index and an API key. If you don’t have them, create an account at [https://www.pinecone.io](https://www.pinecone.io) and set up an index.

Creating a Pinecone index (high level)

| Setting          | Recommendation                                                             |
| ---------------- | -------------------------------------------------------------------------- |
| Index name       | e.g., `AirNova-SOP-Index`                                                  |
| Embedding model  | Use the same model you will run in n8n, e.g., `text-embedding-3-small`     |
| Vector dimension | Match the embedding model output (for `text-embedding-3-small` use `1536`) |
| Deployment type  | Serverless or appropriate managed option                                   |
| Cloud region     | Select a region close to your n8n runtime for latency                      |

If vector dimension does not match the model output when upserting, you will receive an error — ensure dimensions align exactly.

<Frame>
  <img alt="The image shows a Pinecone interface for creating a new index, featuring configuration options for embedding models. There are starter usage details and a button to create the index." />
</Frame>

After creating the index, generate an API key in Pinecone, copy it immediately, then paste it into the Pinecone node credentials in n8n and save.

<Frame>
  <img alt="The image shows a dialog box indicating that an API key named &#x22;airnova-api&#x22; has been generated on the Pinecone platform. It advises users to copy and save the key immediately for security reasons." />
</Frame>

> **warning** API keys are shown only once in Pinecone. Copy and store your key securely (use a secrets manager). Do not commit API keys to version control.

5. Embeddings configuration in n8n

* In the Pinecone Vector Store node, set Embeddings to OpenAI.
* Select the same embedding model you used when creating the Pinecone index: `text-embedding-3-small`.

6. Default Data Loader

* Configure Default Data Loader:
  * Type: `binary` (we downloaded files in binary format).
  * Loader name: optional (e.g., "Data Loader Binary").
  * Load mode: `Load All Input Data`.
  * Enable automatic type detection so PDFs, images, and other types are handled automatically.

7. Text splitter settings

* Choose Custom text splitter and attach Recursive Character Text Splitter.
* Example settings:
  * Chunk size: `500`
  * Chunk overlap: `50` (≈10%)
* Tune these as needed based on document density and RAG prompt window.

Wire the nodes in this order:
Google Drive Trigger → Loop Over Items → Google Drive Download → Pinecone Vector Store (with Embeddings, Default Data Loader, and Recursive Character Text Splitter)

Run a test execution to verify the end-to-end flow.

<Frame>
  <img alt="The image shows a workflow in n8n, a workflow automation tool, featuring nodes like Google Drive Trigger, Loop Over Items, Pinecone Vector Store, and Embeddings OpenAI, interconnected to process files and store data. The interface includes options for execution control and navigation." />
</Frame>

What to expect

* The embedding model will process each chunk produced by the text splitter.
* The Pinecone node will upsert vectors into your index.
* Each upserted item will typically include: chunk text, vector embedding, and metadata (source file, chunk index, timestamps).

<Frame>
  <img alt="The image shows a user interface of a database management system called Pinecone, displaying details about PDF documents, including scores, text, and metadata." />
</Frame>

Example outcome

* A single SOP PDF in this demo produced 10 chunks that were embedded and upserted into the `AirNova` index. Each vector entry contains chunk text plus metadata for retrieval.

Next steps

* Build a RAG AI agent that queries the same Pinecone index to retrieve context for answering customer queries.
* Combine retrieval results with a generation model to produce accurate, context-aware responses driven by your uploaded documents.

Links and references

* Pinecone: [https://www.pinecone.io](https://www.pinecone.io)
* OpenAI embeddings models: [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings)
* n8n documentation: [https://docs.n8n.io](https://docs.n8n.io)

That completes the automated pipeline for upserting Google Drive documents into a Pinecone vector store using n8n.

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/0fde2722-cb9f-4240-bedb-c3dbcb75ba79/lesson/45c847f7-4255-4ea3-b9cf-790e4f8310a5)
