# Essential Prerequisites

Source: https://notes.kodekloud.com/docs/LangGraph/Course-Introduction/Essential-Prerequisites/page

Overview of practical Python, package, API, and JSON skills needed to start using LangGraph and build model-driven workflows

Before we dive into LangGraph, having a few practical skills will make the learning curve much smoother. LangGraph is Python-based and focuses on composing model-driven workflows, so the following foundations are most useful.

## Core skills (quick overview)

* Python fundamentals: writing and calling functions, working with dictionaries, and using lists to manage sequences of data.
* Package usage and typing: importing and using external packages (for example, [LangChain](https://learn.kodekloud.com/user/courses/langchain)) and annotating types with the [`typing` module](https://docs.python.org/3/library/typing.html).
* APIs and structured data: familiarity with REST APIs and JSON payloads — reading, parsing, and transforming JSON (which maps naturally to Python dictionaries and lists).

> **lightbulb** You do not need advanced AI or graph-theory knowledge to follow this lesson. We’ll introduce required concepts as we go; curiosity and basic Python are the most important prerequisites.

## Why these skills matter

* Python skills let you assemble nodes, functions, and data structures that form LangGraph workflows.
* Knowing how to import and work with third-party packages helps when integrating models, tools, or utilities.
* Comfort with JSON and APIs is essential because many LangGraph workflows exchange structured state with external services or tools.

<Frame>
  <img alt="The image outlines a Python skills checklist including writing functions, using dictionaries, manipulating lists, and importing external packages. It has a simple layout with text on a dark and light background." />
</Frame>

## Practical experience that helps

* Interacting with REST APIs using tools like [Postman](https://learning.postman.com/docs/getting-started/introduction/) or [cURL](https://curl.se/) prepares you to inspect requests/responses and iterate quickly.
* Parsing nested JSON payloads into Python dictionaries and lists will be a frequent task when mapping external state to nodes in a graph.
* Understanding how to pass structured data between functions (or nodes) is directly applicable to designing LangGraph workflows.

<Frame>
  <img alt="The image outlines five tasks related to JSON and API familiarity, including interacting with external APIs, understanding REST API patterns, using tools like Postman or cURL, parsing JSON data structures, and managing structured state in workflows." />
</Frame>

## If you’ve used LangChain before

LangChain introduces chains: sequential processing patterns that pass input through a model and collect output. LangGraph builds on these same ideas but generalizes them into graph-structured workflows:

* Chains → linear sequences of steps
* Tools & memory → external calls and state retention
* LangGraph → directed graphs of nodes, where state and control flow can branch, merge, and reconnect

We’ll surface the core concepts early so newcomers can follow along even without deep prior experience.

<Frame>
  <img alt="The image outlines five optional LangChain basics, including understanding chains, recognizing tool usage, using memory, seeing LangGraph as an extension, and expecting foundational concepts." />
</Frame>

## Quick prerequisites checklist

| Skill area                       | Why it helps                                       | Example resources                                                                                                    |
| -------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Python basics                    | Build and compose functions/nodes                  | [Python Basics](https://learn.kodekloud.com/user/courses/python-basics)                                              |
| Package management & typing      | Integrate models & annotate interfaces             | `typing` module docs: [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html) |
| APIs & JSON                      | Connect external services and map structured state | [Postman docs](https://learning.postman.com/docs/getting-started/introduction/), [cURL](https://curl.se/)            |
| LangChain familiarity (optional) | Helpful mental model for sequential workflows      | [LangChain course](https://learn.kodekloud.com/user/courses/langchain)                                               |

## Final note

You don’t need graph theory, heavy math, or advanced deployment experience to start. This lesson emphasizes practical patterns, analogies, and hands-on code examples so you can build intuition while learning how intelligent workflows coordinate state, tools, and models.

If you’re comfortable writing functions, manipulating dictionaries and lists, and calling external APIs, you’re ready to proceed.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/11d0578c-2a76-40f7-be25-905be94f24f8/lesson/efa6ec57-c17b-46a5-9802-82ed26f647ab)
