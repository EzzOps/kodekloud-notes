# Chains

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Chains/page

Explains LangChain chains as modular, composable pipelines connecting prompts, models, retrieval, parsing, memory, and functions to build sequential, parallel, conditional, and stateful workflows.

The name LangChain highlights that the framework is centered on chains — composable pipelines that connect modular components to perform multi-stage tasks. Chains let you assemble prompts, models, functions, retrievers, output parsers, memory, and even other chains into a single workflow that produces a final result for your application.

Chains can be composed in different topologies:

* Sequential: components run in a defined order, with each step receiving the previous step's output (for example: prompt → LLM → output parser).
* Parallel / concurrent: multiple components run at the same time (for example: multiple retrievers or API calls), and their outputs are aggregated and passed downstream.
* Conditional / routing: logic chooses which sub-chain to run based on input or intermediate results.
* Stateful / memory-enabled: chains incorporate memory components to maintain context across invocations (useful for chat or multi-turn workflows).

<Frame>
  <img alt="The image shows a stylized chain divided into three colored sections labeled &#x22;Prompts,&#x22; &#x22;Models,&#x22; and &#x22;Functions.&#x22; The sections are connected, visually representing a process or workflow." />
</Frame>

Practical patterns and when to use them:

* One-off responses: Use a minimal sequential chain (prompt → LLM) when you only need a single formatted response.
* Retrieval-augmented generation (RAG): Add a retriever step before the LLM to fetch relevant documents from a knowledge base, then synthesize the retrieved context with the model output.
* Enforced output format: Insert an output parser after the model to validate, normalize, or transform responses into structured formats (JSON, CSV, etc.).
* Stateful conversations: Add memory to persist prior conversation turns or results and feed them back into the prompt/context.
* Parallel enrichment: Run multiple retrievers, APIs, or models in parallel and then aggregate outputs (rank, dedupe, or fuse) before the final step.
* Composability: Build sub-chains and reuse them as single components inside larger pipelines.

Table: Common chain types, use cases, and conceptual examples

| Chain Type            | Use Case                                          | Conceptual Example                                       |             |
| --------------------- | ------------------------------------------------- | -------------------------------------------------------- | ----------- |
| Sequential            | Single linear flow (prompt → model → parser)      | `prompt -> LLM -> OutputParser`                          |             |
| Retrieval + LLM (RAG) | Augment model with external documents             | `retriever -> combine -> LLM -> parser`                  |             |
| Parallel / Concurrent | Enrich results or call multiple APIs concurrently | `parallel([retrieverA, retrieverB]) -> aggregate -> LLM` |             |
| Router / Conditional  | Route input to different sub-chains               | \`router(input) -> subchainA                             | subchainB\` |
| Stateful (Memory)     | Maintain context across turns                     | `memory + prompt -> LLM -> memory.update()`              |             |

Example snippets (conceptual pseudo-code)

* Simple sequential chain (prompt → LLM → parser)

```python theme={null}
