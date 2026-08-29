# test_converter.py (representative header)
import pytest
from converter import (
    miles_to_kilometers,
    kilometers_to_miles,
    gallons_to_liters,
    liters_to_gallons,
    pounds_to_kilograms,
    kilograms_to_pounds,
    fahrenheit_to_celsius,
    celsius_to_fahrenheit
)

class TestDistanceConversions:
    """Test distance conversion functions"""
    # ... test methods ...

class TestVolumeConversions:
    """Test volume conversion functions"""
    # ... test methods ...

class TestMassConversions:
    """Test mass conversion functions"""
    # ... test methods ...

class TestTemperatureConversions:
    """Test temperature conversion functions"""
    # ... test methods ...
```

The test file was edited in VS Code; when saving the test file the editor prompted to write changes:

<Frame>
  <img alt="A screenshot of Visual Studio Code with a text file open containing instructions to create pytest tests for a Python unit-converter (test_converter.py). The integrated terminal shows a prompt asking whether to save the edits to test_converter.py." />
</Frame>

## Running the tests (first run)

Before implementing converter.py, running pytest fails at collection:

```text theme={null}
$ python3 -m pytest -q
ImportError while importing test module 'test_converter.py'
E   ModuleNotFoundError: No module named 'converter'
```

This is the expected “red” step in the red/green/refactor cycle. Now implement the module to satisfy the tests.

## Implementing converter.py

Implementation goals:

* Validate inputs and raise TypeError for non-numeric values.
* Use correct formulas and precise conversion constants.
* Always return a float.

A concise and correct implementation:

```python theme={null}
def _ensure_numeric(value):
    """Internal helper to validate numeric inputs."""
    if not isinstance(value, (int, float)):
        raise TypeError("Input was not a numeric value")


def miles_to_kilometers(miles):
    """Converts miles to kilometers."""
    _ensure_numeric(miles)
    return float(miles) * 1.60934


def kilometers_to_miles(km):
    """Converts kilometers to miles."""
    _ensure_numeric(km)
    return float(km) * 0.621371


def gallons_to_liters(gallons):
    """Converts US gallons to liters."""
    _ensure_numeric(gallons)
    # Precise US gallon to liter factor
    return float(gallons) * 3.785411784


def liters_to_gallons(liters):
    """Converts liters to US gallons."""
    _ensure_numeric(liters)
    return float(liters) * 0.2641720523581484


def pounds_to_kilograms(pounds):
    """Converts pounds to kilograms."""
    _ensure_numeric(pounds)
    return float(pounds) * 0.45359237


def kilograms_to_pounds(kg):
    """Converts kilograms to pounds."""
    _ensure_numeric(kg)
    return float(kg) * 2.2046226218487757


def fahrenheit_to_celsius(fahrenheit):
    """Converts degrees Fahrenheit to Celsius."""
    _ensure_numeric(fahrenheit)
    return (float(fahrenheit) - 32.0) * (5.0 / 9.0)


def celsius_to_fahrenheit(celsius):
    """Converts degrees Celsius to Fahrenheit."""
    _ensure_numeric(celsius)
    return float(celsius) * (9.0 / 5.0) + 32.0
```

## Iterating with pytest

* Re-run pytest after implementing the module and fix any failures.
* Floating-point mismatches can occur between constants used in tests and implementation. Tests should use pytest.approx() to tolerate reasonable differences.
* If a persistent mismatch remains, prefer improving implementation precision rather than loosening tests unless the tests are incorrect.

Example successful test run:

```text theme={null}
$ python3 -m pytest -q
........................................  # all tests pass (representative)
40 passed in 0.12s
```

<Callout icon="lightbulb">
  LLMs (such as Claude Code) are powerful for generating comprehensive, mechanical test suites and scaffolding implementations. Always perform human review and iterative testing—LLM outputs are excellent starting points but may need adjustments for precision, edge cases, and integration context.
</Callout>

## Summary and recommendations

* TDD gives you a precise specification and reduces regressions.
* Use Claude Code to speed up repetitive tasks like generating extensive test cases.
* Always run and iterate on tests locally: LLMs may need guidance around precision and edge cases.
* Keep tests deterministic and specific; use pytest.approx() for floating-point assertions with reasonable tolerances.
* Store the test prompts and generated tests in your repository as a reusable starting point for TDD experiments.

Further reading and references:

* [Claude Code course](https://learn.kodekloud.com/user/courses/claude-code-for-beginners)
* [pytest documentation](https://docs.pytest.org/)
* [Python numbers — official docs](https://docs.python.org/3/library/stdtypes.html#numeric-types)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/a295c914-f61e-47bb-8adc-7a3145745aa6/lesson/afd1bb19-60e7-4184-b98b-45e624967de4" />
</CardGroup>


# Demo Working with Claude Code Agents

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Advanced-Features/Demo-Working-with-Claude-Code-Agents/page

Demonstrates creating, configuring, and using Claude Code agents via CLI and SDK to automate code reviews, incident diagnosis, and CI/CD checks, including agent files and best practices.

In this lesson, we’ll walk through creating and using agents in Claude Code. You’ll see both interactive CLI workflows (great for developer iteration) and programmatic SDK examples (ideal for CI/CD automation). The examples below show how to create, configure, and run agents for code review or incident diagnosis, and how to persist those agent definitions in a repository.

<Frame>
  <img alt="A presentation slide titled &#x22;Working with Claude Code Agents&#x22; with a dark curved design on the right containing the word &#x22;Demo&#x22; in blue. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

Overview: two common approaches

* CLI sub-agents: Create sub-agents you can call interactively from the CLI during development and reviews.
* SDK-driven agents: Create and invoke agents programmatically (Python, JS/TS, Go, Ruby, etc.) to automate checks in CI/CD pipelines.

Table: When to use CLI vs SDK

| Approach   | Best for              | Typical use case                                 |
| ---------- | --------------------- | ------------------------------------------------ |
| CLI agents | Interactive iteration | Local development reviews, ad-hoc audits         |
| SDK agents | Automation            | CI/CD checks, scheduled audits, pre-merge gating |

CLI: listing agents and creating one
The CLI shows whether any project agents exist and offers a guided flow for creating new agents. Example CLI output when no agents are present:

```bash theme={null}
cwd: /Users/jeremy/Repos/project/Express-login-demo

> /agents

Agents
No agents found

› Create new agent

No agents found. Create specialized subagents that Claude can delegate to.
Each subagent has its own context window, custom system prompt, and specific tools.
Try creating: Code Reviewer, Code Simplifier, Security Reviewer, Tech Lead, or UX Reviewer.

Built-in (always available):
general-purpose · sonnet
statusline-setup · sonnet
output-style-setup · sonnet

Press ↑↓ to navigate · Enter to select · Esc to go back
```

Create an agent: generation vs manual configuration
You can either generate a draft agent from a description (recommended) or build the agent manually. Generation uses Claude to produce a starting configuration you can edit.

Example selection UI showing the generation option:

```bash theme={null}
cwd: /Users/jeremy/Repos/project/Express-login-demo

> /agents

Create new agent
Creation method

> 1. Generate with Claude (recommended)
2. Manual configuration

Press ↑↓ to navigate · Enter to select · Esc to go back
```

When generating, provide a clear description of the agent’s responsibilities — the tool will create a draft configuration (metadata, system prompt, and rule set) that you can refine.

Tool selection and model selection
Agents can be granted fine-grained tool permissions (e.g., read-only, edit, execution) and you choose the model that balances reasoning capability and cost.

Example tool-selection UI:

```bash theme={null}
cwd: /Users/jeremy/Repos/project/Express-login-demo

> /agents

Create new agent
Select tools

[ Continue ]
────────────────────────
All tools
Read-only tools
> Edit tools
Execution tools
MCP tools
────────────────────────
[ Show advanced options ]

All tools selected

Press Enter to toggle selection · ↑↓ to navigate · Esc to go back
```

Example model-selection UI:

```bash theme={null}
cwd: /Users/jeremy/Repos/project/Express-login-demo

> /agents

Create new agent
Select model
Model determines the agent's reasoning capabilities and speed.

  1. Sonnet           Balanced performance -- best for most agents
  2. Haiku            Fast and efficient for simple tasks
> 3. Inherit from parent  Use the same model as the main conversation

Press ↑↓ to navigate · Enter to select · Esc to go back
```

Confirm and save the agent
After generation and selection, the CLI shows a confirmation summary. Review and save (or save-and-edit) the generated agent:

```bash theme={null}
Create new agent
Confirm and save

Name: code-readability-reviewer
Location: .claude/agents/code-readability-reviewer.md
Tools: Bash, Glob, Grep, LS, Read, WebFetch, TodoWrite, WebSearch, BashOutput, KillBash
Model: Inherit from parent

Description (tells Claude when to use this agent):

    Use this agent when you need to evaluate code for readability, variable naming conventions, and overall code clarity.

System prompt:

    You are a Senior Code Quality Specialist with expertise in software readability, maintainability, and naming conventions across multiple programming languages. Your primary focus is evaluating code for clarity, comprehensibility, and adherence to clean code principles.

Press s or Enter to save, e to save and edit
```

Agent created and listed
Once saved, the agent appears in the project agent list and can be invoked interactively:

```bash theme={null}
cwd: /Users/jeremy/Repos/project/Express-login-demo

> /agents

Agents
4 agents

Created agent: code-readability-reviewer

Create new agent

Project agents (/Users/jeremy/Repos/project/Express-login-demo/.claude/agents)
> code-readability-reviewer .inherit

Built-in agents (always available)
general-purpose · sonnet
statusline-setup · sonnet
output-style-setup · sonnet

Press ↑↓ to navigate · Enter to select · Esc to go back
```

Editing an agent's configuration
Agent definitions are stored as files in your repo (YAML-style metadata plus the system prompt and rules). Open and edit them in your preferred editor.

Example agent metadata:

```yaml theme={null}
name: code-readability-reviewer
description: Use this agent when you need to evaluate code for readability, variable naming conventions, and overall code clarity.
tools: Bash, Glob, Grep, LS, Read, WebFetch, TodoWrite, WebSearch, BashOutput, KillBash
model: inherit
color: green
```

System prompt and review rules (summary)

* Role: Senior Code Quality Specialist focused on readability and maintainability.
* Review checklist:
  * Assess variable and function naming clarity.
  * Flag vague or misleading names (e.g., data, temp, x).
  * Check naming consistency (camelCase vs snake\_case).
  * Suggest descriptive alternatives and refactors.
  * Analyze function length, logic flow, and comment quality.
  * Identify magic numbers and hardcoded values.
  * Provide a readability score (1–10) with reasoning and prioritized fixes.

Using the agent via CLI
Invoke a saved agent from the CLI to run a review. Example interaction and a cleaned-up sample report:

```bash theme={null}
cwd: /Users/jeremy/Repos/project/Express-login-demo

> use the code-readability-reviewer agent to inspect auth.js and give me a report.

• I'll use the code-readability-reviewer agent to analyze the auth.js file and provide you with a readability report.

• code-readability-reviewer(Review auth.js readability)
  Done (2 tool uses · 12.1k tokens · 29.9s)

• The code-readability-reviewer agent has analyzed your auth.js file and provided a comprehensive readability report. Here are the key findings:

Overall Score: 8/10 - The code is well-structured with good naming conventions and follows Express.js patterns effectively.

Main Strengths:
 - Clear variable names like userQuery, isPasswordValid
 - Consistent camelCase naming
 - Proper separation of validation and business logic
 - Good security practices (parameterized queries, password hashing)

Key Areas for Improvement:
 1. Extract database error handling – Error codes (e.g., '28P01', '3D000') should be defined as constants.
 2. Function length – The main handler is 78 lines and could be broken into smaller, testable functions.
 3. Magic strings – Move SQL queries and error code strings into constants.

Recommended Priority Fixes:
 - Define constants for database error codes
 - Extract the authentication logic into a separate function
 - Move hardcoded SQL query to a constant

The code follows security best practices but would benefit from better organization and consistent constant definitions for maintainability.
```

Example Express route (cleaned-up)
Below is a sample Express route that demonstrates the quality improvements an agent might recommend: validation, shorter handler, and clear structure.

```javascript theme={null}
// routes/auth.js
const express = require('express');
const { body, validationResult } = require('express-validator');
const pool = require('../config/database'); // assume configured pg pool
const router = express.Router();

router.post(
  '/login',
  [
    body('email').isEmail().withMessage('Please provide a valid email address').normalizeEmail(),
    body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters long')
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ error: 'Validation failed', details: errors.array() });
    }

    try {
      const { email, password } = req.body;
      // Extracted authentication logic would go here (e.g., verify user and password)
      // Example: const user = await findUserByEmail(email);
      // if (!user || !verifyPassword(password, user.hash)) return res.status(401).send('Unauthorized');

      res.status(200).json({ message: 'Login successful' });
    } catch (err) {
      console.error('Auth error:', err);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
);

module.exports = router;
```

Typical recommendations from the agent

* Define constants for database error codes.
* Extract authentication logic to helper functions for testability.
* Move hardcoded SQL queries into named constants or query builders.
* Add unit tests for extracted functions.

Programmatic use: Python SDK for CI/CD integration
Create and run agents programmatically using the Claude Code SDK. This integrates agents into CI/CD pipelines and automates code-quality checks on pull requests.

Example Python SDK usage (async):

```python theme={null}
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def main():
    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are an SRE agent. Diagnose incidents step-by-step and propose safe fixes.",
            allowed_tools=["Read", "Grep", "Bash"],  # fine-grained control
            max_turns=4
        )
    ) as client:
        await client.query("API error rates just spiked in payments — investigate and propose fixes.")
        async for msg in client.receive_response():
            if hasattr(msg, "content"):
                for block in msg.content:
                    if hasattr(block, "text"):
                        print(block.text, end="")

asyncio.run(main())
```

You can commit agent definitions (YAML) into your repository and call them from CI pipelines to enforce automated checks before merge.

Example agent definition (commit to repo):

```yaml theme={null}
---
name: code-readability-reviewer
description: Use this agent when you need to evaluate code for readability, variable naming conventions, and overall code clarity.
tools: Bash, Glob, Grep, LS, Read, WebFetch, TodoWrite, WebSearch, BashOutput, KillBash
model: inherit
color: green
---
```

Supported models and language SDKs
Claude Code supports multiple model families (examples):

| Model family                     | Use case                               |
| -------------------------------- | -------------------------------------- |
| Claude 4 (Opus, Sonnet variants) | High reasoning, complex tasks          |
| Claude 3.7 (Sonnet variants)     | Balanced performance                   |
| Claude 3.5 (Haiku variants)      | Fast, cost-efficient for simpler tasks |

Example listing (illustrative):

```text theme={null}
