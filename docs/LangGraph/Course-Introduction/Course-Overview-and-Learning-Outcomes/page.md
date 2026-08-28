# Disallow images that end with ":latest"
!object.spec.image.endsWith(":latest")

# Ensure replicas are between 1 and 10 (inclusive)
object.spec.replicas >= 1 && object.spec.replicas <= 10
```

Summary of the rules enforced

| Check                      | Example CEL                                               | Rationale                                                         |
| -------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| Disallow moving image tags | `!object.spec.image.endsWith(":latest")`                  | Ensures reproducible deployments by forcing immutable tags.       |
| Replica count range        | `object.spec.replicas >= 1 && object.spec.replicas <= 10` | Prevents accidental scale-to-zero or unreasonably large replicas. |

This demo includes a ValidatingAdmissionPolicy and a matching ValidatingAdmissionPolicyBinding for these rules. You'll see two test cases: applying an invalid WebApp manifest (to observe rejection) and applying a valid manifest (to observe acceptance). The provided policy manifest uses placeholders so you can insert the CEL expressions and validate the API server behavior.

Example fragment in the policy manifest where you fill in CEL expressions:

```yaml theme={null}
validations:
  - expression: "<your CEL here>"
  - expression: "<your CEL here>"
```

<Callout icon="lightbulb">
  Policies and bindings are distinct: policies hold logic and messages, while bindings control scope and enforcement. This lets you stage validation rules in the cluster before applying them to requests.
</Callout>

References and further reading

* Validating Admission Policies: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionpolicy](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionpolicy)
* Common Expression Language (CEL): [https://opensource.google/docs/cel/](https://opensource.google/docs/cel/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/06ac03ac-518a-4bc6-b2f8-6ed63fcb26d5/lesson/4201bc54-9684-4c44-afda-8553eab1dd40" />
</CardGroup>


# Course Overview and Learning Outcomes

Source: https://notes.kodekloud.com/docs/LangGraph/Course-Introduction/Course-Overview-and-Learning-Outcomes/page

Introductory LangGraph course teaching graph-based AI workflows, state management, memory, conditional logic, human-in-the-loop patterns, and observability with hands-on modules and labs.

Welcome to the LangGraph beginner course — a practical, hands-on introduction to designing graph-based AI applications and agentic systems. This lesson series teaches you how to structure workflows with explicit control, state management, memory, and human-in-the-loop patterns so you can build reliable, observable AI systems for real-world use cases.

<Callout icon="lightbulb">
  This lesson is beginner-friendly: you don't need prior graph theory or advanced AI knowledge. We'll use practical analogies and hands-on examples to build intuition.
</Callout>

What is LangGraph and why it matters
LangGraph extends [LangChain](https://learn.kodekloud.com/user/courses/langchain) with a structured graph model that helps you manage complex flows. Instead of ad-hoc chains, LangGraph lets you compose nodes, edges, and paths into transparent workflows that can:

* Maintain and inspect state across runs
* Support conditional branching and decision logic
* Implement short- and long-term memory strategies
* Orchestrate human-in-the-loop handoffs and interruptions
* Provide instrumentation for debugging and observability

<Frame>
  <img alt="The image is a diagram explaining &#x22;LangGraph,&#x22; a framework that builds on LangChain by adding a structured graph model to manage complex workflows. It shows a connection between a framework and a graph model leading to complex workflows." />
</Frame>

Learning outcomes — what you'll be able to do
By the end of this course you will be able to:

* Understand graph primitives (nodes, edges, execution semantics) and compose them into end-to-end workflows.
* Implement conditional paths and branching logic for robust decision-making.
* Manage transient and persistent state across graph runs.
* Apply short-term (contextual) and long-term memory strategies using datastores and retrieval mechanisms.
* Design human-in-the-loop patterns like approvals, handoffs, and interruptions.
* Instrument graphs for observability, traceability, and reliable debugging.

Course structure and learning path
This course is organized to move you from foundational concepts to advanced production patterns. Each module includes slide-based instruction, walkthrough demos, and optional labs so you can practice and apply the patterns immediately.

Modules at a glance
The course is divided into eight focused modules. The following table and module list provide a quick reference and learning path.

| Module   | Focus                          | What you’ll practice                                    |
| -------- | ------------------------------ | ------------------------------------------------------- |
| Module 1 | Graph primitives               | Nodes, edges, execution semantics, basic graph creation |
| Module 2 | Paths & decisions              | Conditional routing, branching, decision nodes          |
| Module 3 | State management               | Local and runtime state patterns                        |
| Module 4 | Context & short-term memory    | Session-level memory and contextualization              |
| Module 5 | Long-term memory & persistence | Datastore integration and retrieval patterns            |
| Module 6 | Human-in-the-loop              | Interruptions, approvals, handoffs                      |
| Module 7 | Debugging & observability      | Tracing, logging, replayable traces                     |
| Module 8 | Wrap-up & projects             | Self-challenges, next steps, real-world projects        |

1. Module 1 — Graph primitives (nodes, edges, execution semantics)
2. Module 2 — Paths and decisions (conditional routing, branching)
3. Module 3 — State management (local and runtime state)
4. Module 4 — Context and short-term memory (session-level memory)
5. Module 5 — Long-term memory and persistence (datastores, retrieval)
6. Module 6 — Human-in-the-loop patterns (interruptions, approvals, handoffs)
7. Module 7 — Advanced debugging and observability (tracing, logging, replay)
8. Module 8 — Wrap-up, self-challenges, and next steps (projects and further learning)

Each module builds on the prior one and includes demos, visuals, and labs to reinforce learning and help you apply the patterns to real problems.

<Frame>
  <img alt="The image is a course structure overview featuring eight modules and over 40 lectures, including demos, visuals, and labs. Each module builds on the previous one, covering topics like graph primitives, state management, and advanced debugging." />
</Frame>

Who this course is for

* Beginners to LangGraph or [LangChain](https://learn.kodekloud.com/user/courses/langchain) who want a structured introduction.
* Developers familiar with prompts and chains who want to move to modular, conditional, and persistent agentic systems.
* Practitioners who need practical patterns for memory, control, and human-in-the-loop interactions.

How to get the most from this course

* Follow modules sequentially — each lesson builds on previous concepts.
* Reproduce demos locally and experiment with node/edge variations.
* Use the labs to apply patterns to domain problems (e.g., planning, customer support, scheduling).
* Instrument and replay flows to learn debugging and observability techniques.

Links and references

* [LangChain (course)](https://learn.kodekloud.com/user/courses/langchain) — Related foundational material.
* Official LangChain docs — refer to LangChain’s documentation for integrations and models.

Welcome to LangGraph — by the end of this series you'll be able to design modular, conditional graphs that handle real-world complexity with controllable, observable behavior.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-2a76-40f7-be25-905be94f24f8/lesson/6a20cbba-80d0-4d07-bc5f-186c6b4a5394" />
</CardGroup>
