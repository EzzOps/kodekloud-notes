# Demo Plan and Act Mode

Source: https://notes.kodekloud.com/docs/Cline/Introduction-to-Cline/Demo-Plan-and-Act-Mode/page

Guide to Cline's Plan and Act modes for AI-driven planning versus automated execution, demonstrated by scaffolding a FastAPI SQLite casting lookup service.

In this lesson we cover Cline's Plan and Act mode — a two-step, AI-guided workflow for structured development: think first, act second. Use Plan mode to analyze context and propose a sequence of steps without touching files. Switch to Act mode when you want Cline to perform the work (create/edit/delete files, run commands, run tests, or launch processes).

Plan mode is ideal for design, architecture, and step-by-step strategies. Act mode is for execution and automation. Many developers use Plan-only workflows to preserve understanding; others prefer Act for speed. Choose the approach that fits your workflow.

> **lightbulb** Plan mode is for analysis, architecture, and step-by-step strategy (no file changes). Act mode performs the actual modifications and commands when you're ready.

Plan vs Act — capabilities at a glance

| Capability                                  |                       Plan mode | Act mode                                   |
| ------------------------------------------- | ------------------------------: | :----------------------------------------- |
| Read repository files and project context   |                               ✓ | ✓                                          |
| Produce architecture and step-by-step plans |                               ✓ | ✓                                          |
| Modify code / create / delete files         |                               ✕ | ✓                                          |
| Run shell commands, tests, or processes     |                               ✕ | ✓                                          |
| Launch external tools (browsers, services)  |                               ✕ | ✓                                          |
| Best for                                    | Reviewing and designing changes | Applying and testing changes automatically |

<Frame>
  <img alt="A dark-themed webpage screenshot of product documentation with a left navigation menu and a central infographic titled &#x22;Plan vs Act Mode Capabilities&#x22; comparing Plan Mode and Act Mode. Below the infographic is a &#x22;Workflow Guide&#x22; section with numbered steps." />
</Frame>

Demo walkthrough — summary and cleaned-up code snippets

This walkthrough demonstrates using Plan mode to design a small project, then switching to Act mode to scaffold and implement it. The example builds a "casting number lookup" API:

* Consumer sends an integer casting number; API returns metadata for that number.
* Data persisted in SQLite.
* Implementation in Python + FastAPI.
* CSV import for bulk data.

1. Start in Plan mode and provide a clear task prompt. Example goals:

* Build a FastAPI service to expose casting lookup endpoints.
* Use SQLAlchemy with SQLite for persistence.
* Provide a CSV import utility to populate the DB.
* Add Pydantic schemas, basic validation, and tests.

A typical synthesized plan includes:

* Create a standard FastAPI project layout.
* Add SQLite + SQLAlchemy database setup.
* Build SQLAlchemy models matching the CSV schema.
* Create import script to ingest CSV into DB.
* Implement API endpoints for list and single lookup.
* Add tests and a small runner to execute them.

2. Review and approve the plan. In Act mode, Cline can create the skeleton and files. For example, the initial shell command to create a typical FastAPI layout:

```bash theme={null}
mkdir -p app/api/endpoints app/db app/models app/schemas app/utils tests examples
touch app/__init__.py app/api/__init__.py app/api/endpoints/__init__.py app/db/__init__.py app/models/__init__.py app/schemas/__init__.py app/utils/__init__.py examples/__init__.py
```

Below are representative, cleaned-up code snippets that match the plan. Adjust fields and types to match your actual CSV.

database.py — SQLite + SQLAlchemy setup

```python theme={null}
