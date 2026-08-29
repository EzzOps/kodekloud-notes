# Edit .env to update secrets, passwords and any host settings (e.g., POSTGRES_PASSWORD, OLLAMA_HOST)
```

<Callout icon="lightbulb">
  Open `.env` and update secrets (database credentials, encryption keys, JWT secrets, etc.) before starting the stack. If you plan to use a separately installed Ollama instance, set `OLLAMA_HOST` (for example: `http://localhost:11434`).
</Callout>

Step 2 — Start the stack with Docker Compose
Choose the profile that matches your hardware. Each profile brings up the same services with configuration appropriate to the runtime.

| Profile      | Use case                                           | Command                                  |
| ------------ | -------------------------------------------------- | ---------------------------------------- |
| `cpu`        | CPU-only environments (Mac Apple Silicon / no GPU) | `docker compose --profile cpu up`        |
| `gpu-nvidia` | Linux machines with NVIDIA GPUs and drivers        | `docker compose --profile gpu-nvidia up` |
| `gpu-amd`    | Machines with AMD GPUs                             | `docker compose --profile gpu-amd up`    |

Example:

```bash theme={null}
docker compose --profile cpu up
```

Note: The first run pulls several images (Postgres, Qdrant, n8n, Ollama, etc.). This can take a few minutes depending on network speed.

Common services started

| Service  | Purpose                                  |
| -------- | ---------------------------------------- |
| Postgres | Primary n8n database                     |
| Qdrant   | Vector database for embeddings           |
| n8n      | Workflow editor and runtime              |
| Ollama   | Local LLM runtime used by demo workflows |

Example terminal output (truncated)

```bash theme={null}
Cloning into 'self-hosted-ai-starter-kit'...
remote: Enumerating objects: 161, done.
Receiving objects: 100% (151/151), 9.92 MiB | 4.35 MiB/s, done.
Resolving deltas: 100% (26/26), done.
marconi@Marconi-MacBook-Pro % cd self-hosted-ai-starter-kit
marconi@Marconi-MacBook-Pro self-hosted-ai-starter-kit % cp .env.example .env
marconi@Marconi-MacBook-Pro self-hosted-ai-starter-kit % docker compose --profile cpu up
[+] Running 98/41
 ✔ postgres Pulled  ...
 ✔ qdrant Pulled  ...
 ✔ n8n Pulled  ...
 ✔ ollama Pulled  ...
...
ollama  time=2025-08-26T08:24:08.451Z level=INFO source=logs:130 msg="inference compute" id=0 library=cpu total="7.7 GiB" available="6.8 GiB"
postgres-1 2025-08-26 08:24:08.422 UTC [1] LOG:  starting PostgreSQL 16 on aarch64-unknown-linux-musl
drant 2025-08-26T08:24:08.444UTC INFO drant: 1x unit API Listening on 6333
n8n-import  Successfully imported 2 credentials.
n8n-import  Successfully imported 1 workflow.
n8n  Initializing...
n8n  Editor is now accessible via:
```

Step 3 — Open n8n in your browser

* Go to: [http://localhost:5678](http://localhost:5678)
* On first visit you will be prompted to create an owner account (email, name, password). Any local email works for this self-hosted setup.

<Frame>
  <img alt="The image shows a web page with a form for setting up an owner account, requiring email, first name, last name, and password. There is also an option to receive security and product updates." />
</Frame>

Demo workflow and Ollama integration

* The starter kit automatically imports a demo workflow when n8n starts.
* Open the demo workflow in the editor: it demonstrates a simple LLM chain using an Ollama chat model.
* Create an Ollama credential in n8n and point it to your Ollama host. When using the compose stack, the default is `ollama:11434` (Docker-internal hostname mapped to `localhost:11434` on the host machine).
* Send a sample prompt (for example, "Hey, how's it going?") to test the node. Responses should come from the local Ollama instance running in the compose stack.

<Frame>
  <img alt="The image shows a workflow interface in a software application, featuring a chat trigger connected to two models (Ollama Chat Model and Ollama Model) through a basic LLM chain. There is a chat log at the bottom displaying an interaction with the system." />
</Frame>

Inspecting Docker Desktop

* Use Docker Desktop to view containers, images, networks, and volumes created by the starter kit.
* Stopping the compose stack (or containers) will disconnect n8n from Ollama and other services because they run in the same compose network.
* Volumes hold Postgres and Ollama state; manage them via Docker Desktop if you need to clear or backup data.

<Frame>
  <img alt="The image shows the Docker Desktop interface, focused on the &#x22;Volumes&#x22; section, displaying a list of available self-hosted AI starter kit storage volumes with options to manage them. There is also a section for walkthroughs at the bottom of the screen." />
</Frame>

<Frame>
  <img alt="The image shows the Docker Desktop application with a list of running containers, displaying details like container name, ID, image, ports, CPU usage, and actions available." />
</Frame>

Compose configuration (example)
If you need to change ports, credentials, environment variables, or persistent volumes, edit the repository's docker-compose files. Below is an illustrative excerpt showing volumes, network, and the n8n & Ollama service definitions — update `.env` values as appropriate.

```yaml theme={null}
volumes:
  n8n_storage:
  postgres_storage:
  ollama_storage:
  qdrant_storage:

networks:
  demo:

x-n8n: &n8n-service
  image: n8n/n8n:latest
  networks: ['demo']
  environment:
    - DB_TYPE=postgresdb
    - DB_POSTGRESDB_HOST=postgres
    - DB_POSTGRESDB_USER=${POSTGRES_USER}
    - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
    - N8N_DIAGNOSTICS_ENABLED=false
    - N8N_PERSONALIZATION_ENABLED=false
    - N8N_ENCRYPTION_KEY=
    - N8N_USER_MANAGEMENT_JWT_SECRET=
    - OLLAMA_HOST=${OLLAMA_HOST:-ollama:11434}
  env_file:
    - .env

x-ollama: &ollama-service
  image: ollama/ollama:latest
  container_name: ollama
  networks: ['demo']
  restart: unless-stopped
  ports:
    - "11434:11434"
```

<Callout icon="warning">
  Do not commit your `.env` file to source control. The file contains sensitive values (database passwords, encryption keys, JWT secrets). Use secure storage or environment-specific secrets for production deployments.
</Callout>

References and further reading

* n8n self-hosted AI starter kit: [https://github.com/n8n-io/self-hosted-ai-starter-kit](https://github.com/n8n-io/self-hosted-ai-starter-kit)
* Ollama docs: [https://ollama.ai/docs](https://ollama.ai/docs)
* Docker Desktop: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
* Docker documentation and Compose reference: [https://docs.docker.com/](https://docs.docker.com/)
* Docker training (beginner): [https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner)

Wrap-up

* This starter kit runs n8n, Ollama, Postgres, and Qdrant locally using Docker Desktop, enabling full local development and testing of AI-driven workflows.
* For production-grade deployments, evaluate network security, backups for volumes, and using managed database or vector stores as needed.

That's it — you're ready to build and test n8n workflows locally with a local Ollama LLM.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/ec070482-ed97-417b-8105-a45836512736/lesson/e2950159-f924-4597-abde-533c73c2a034" />
</CardGroup>


# Self Hosting vs Building on n8n Cloud

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Optional-Setups/Self-Hosting-vs-Building-on-n8n-Cloud/page

Comparison of n8n Cloud versus self‑hosting, detailing trade‑offs, pros, cons, and a checklist to choose based on control, cost, security, and operational needs.

When starting with n8n, you’ll face a fundamental decision: deploy on the managed [n8n Cloud](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero-2) service or run a self‑hosted instance. Both approaches are valid; the right choice depends on your priorities for time-to-value, control, cost, security, and operational capacity. This guide compares both options, highlights trade-offs, and offers a practical checklist to help you decide.

## Quick summary

* Use [n8n Cloud](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero-2) for fastest onboarding, minimal operations, and a managed environment.
* Use self‑hosting for full control, private integrations, regulatory compliance, and potential cost savings at scale.
* Evaluate team skills, expected scale, integration surface (public vs private), and compliance needs before choosing.

## n8n Cloud — simplicity and convenience

Why choose it

* Fast onboarding: sign up and start building workflows in minutes.
* Zero infra work: no Docker, Kubernetes, or VM provisioning required.
* Managed maintenance: updates, security patches, and platform health are handled by the provider.
* Built‑in monitoring and official support (plan dependent) for SLA-backed uptime.

Pros

* Immediate productivity for prototypes, MVPs, and smaller teams.
* Reduced operational overhead and fewer maintenance tasks.
* Predictable support channels and managed incident handling.

Trade‑offs

* Subscription costs that scale with usage and plan features.
* Less control over environment configuration, resource allocation, and custom extensions.
* Limited ability to access private/on‑premise resources without additional networking setup.

Best fit

* Individuals, teams prototyping workflows, and organizations that prefer minimal ops effort and vendor‑managed reliability.

## Self‑hosting — control and flexibility

Why choose it

* Complete control over compute, network, storage, and deployment topology.
* Direct access to internal services, private databases, and on‑prem resources.
* Ability to enforce custom security policies, compliance controls, and data residency.

Pros

* Customize instance size, OS, deployment platform (VMs, Kubernetes, Docker Compose).
* Connect securely to private systems without exposing them to the public internet.
* Potential cost advantages when leveraging existing infrastructure at scale.

Trade‑offs

* You are responsible for installation, updates, backups, monitoring, and security patching.
* Requires planning for high availability, redundancy, scaling, and disaster recovery.
* Support is internal or third‑party — no automatic vendor remediation unless contracted.

Best fit

* Production deployments with strict compliance, private network dependencies, or organizations with dedicated DevOps/Platform teams.

## Side‑by‑side comparison

| Area                        | n8n Cloud                  | Self‑hosting             |
| --------------------------- | -------------------------- | ------------------------ |
| Time to first workflow      | Minutes                    | Hours–Days               |
| Infrastructure management   | Managed                    | Customer responsible     |
| Access to private resources | Limited / requires tunnels | Direct / full control    |
| Cost model                  | Subscription               | Infrastructure + ops     |
| Scaling                     | Abstracted by provider     | Customer designs scaling |
| Updates & security          | Managed                    | Customer manages         |
| Compliance/data residency   | Provider dependent         | Fully controllable       |

## Practical considerations and checklist

Before deciding, evaluate each item below and mark what matters most to your project:

* Purpose: prototype, staging, or production?
* Team skills: do you have DevOps or SRE capacity?
* Integration surface: need to reach private databases or on‑prem APIs?
* Compliance: data residency, audit trails, and regulatory controls required?
* Availability & SLAs: does business require high SLA with vendor support?
* Cost horizon: subscription vs. long‑term infrastructure and operational costs?
* Backup & DR: can your team implement backups, restore tests, and failover?
* Monitoring & observability: who will maintain logs, metrics, and alerts?
* Security lifecycle: who will apply CVE patches and manage secrets?

<Callout icon="lightbulb">
  If you’re just starting, try [n8n Cloud](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero-2) to get productive quickly. If you need tighter integrations, data residency, or compliance guarantees, plan a self‑hosted deployment with proper operational practices (automated backups, monitoring, and update procedures).
</Callout>

## Decision patterns (when to choose which)

* Choose n8n Cloud when:
  * You need speed and minimal ops overhead.
  * Your workflows primarily integrate with public SaaS APIs.
  * You want vendor‑managed updates and monitoring.

* Choose self‑hosting when:
  * You must access private networks, on‑prem databases, or internal tools.
  * Regulatory compliance or data residency is mandatory.
  * You prefer to control costs via existing infrastructure and have ops capacity.

## Getting started tips

* If trying n8n Cloud: create a sandbox project, prototype 3–5 workflows, and validate integrations and throughput requirements.
* If self‑hosting:
  * Start with a staging environment mirroring production.
  * Deploy using Kubernetes or Docker Compose depending on scale and team familiarity.
  * Automate backups (database and filesystem) and test restores regularly.
  * Implement monitoring (metrics, logging, alerting) and define RTO/RPO objectives.
  * Harden security: network segmentation, secrets management, and periodic patching.

## Links and references

* [n8n Cloud](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero-2)
* n8n documentation (official): [https://docs.n8n.io/](https://docs.n8n.io/)
* Consider reading about container orchestration if self-hosting on Kubernetes: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

## Summary

* n8n Cloud = speed, convenience, and managed operations.
* Self‑hosting = control, privacy, and custom integrations.
* Choose based on your team’s operational capacity, compliance needs, and the degree of control required. There is no single “correct” option — pick the approach that aligns with your priorities and growth plans.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/ec070482-ed97-417b-8105-a45836512736/lesson/ce2be9a2-9850-4e11-915d-e23abc1d247a" />
</CardGroup>
