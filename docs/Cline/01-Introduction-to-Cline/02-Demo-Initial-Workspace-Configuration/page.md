# Demo Initial Workspace Configuration

Source: https://notes.kodekloud.com/docs/Cline/Introduction-to-Cline/Demo-Initial-Workspace-Configuration/page

Guide to installing and configuring the Cline AI coding extension in VS Code, covering permissions, workspace toggles, context management, model selection, and initial project workflow

Cline is a collaborative AI coder with a large user base (≈1.7M installs and 46k+ GitHub stars). It integrates into several editors — VS Code, VS Code Insiders, Cursor, and Windsurf. This lesson uses VS Code.

Installation is straightforward: pick the VS Code option in your browser, allow the prompt to open Visual Studio Code, then locate Cline in the Extensions view (search for "Cline" if needed).

<Frame>
  <img alt="A dark-themed IDE window showing an extension page for &#x22;Cline&#x22; with its logo, description, screenshots, and marketplace details on the right. The left side shows an empty Explorer/sidebar and bottom panels like Outline and Timeline." />
</Frame>

The extension page highlights features like adding context, creating rules, and workspace controls. Click Install to add Cline to VS Code.

When Cline proposes a command (for example, to start a local dev server) it will request your confirmation. Below is a representative example of that prompt and the diagnostic output Cline can surface when `npm start` encounters compilation issues:

```text theme={null}
Cline wants to execute this command:
npm start

> Command Output

API Request $0.0058

The development server has started, but there are compilation errors in src/App.js. The main issues are:
1. 'useState' is not defined (lines 7 and 8)
2. 'useStae' is defined but never used (line 1)

It looks like there's a typo importing 'useState' (written as 'useStae'). Cline suggests examining src/App.js to fix these issues.

Cline wants to read this file:
src/App.js

PROBLEMS / OUTPUT / TERMINAL

src/App.js
Line 1:17:  'useStae' is defined but never used  (eslint)
Line 7:28:  'useState' is not defined           (eslint)
Line 8:28:  'useState' is not defined           (eslint)

webpack compiled with 1 error and 1 warning
```

After installation you'll be prompted to sign in. The typical first-time flow:

* Click "Get started for free".
* An external authorization page opens for connecting your account.
* After authorization, a dashboard shows usage and billing details.

Next — a quick tour of the Cline sidebar and the most important settings.

## Key workspace toggles

The Cline sidebar exposes several permission toggles that affect how the assistant interacts with your workspace:

* Auto-approve — allow Cline to accept and apply its own suggestions automatically.
* Allow read — permit Cline to read project files you attach to a task.
* Allow edit — permit Cline to modify project files when applying fixes.
* Execute safe commands — allow Cline to run predefined "safe" commands in your terminal.

<Frame>
  <img alt="A dark-themed code editor window (looks like VS Code) with an &#x22;Auto-approve Settings&#x22; sidebar showing permission toggles and quick settings on the left, and a large editor logo with keyboard shortcut hints on the right." />
</Frame>

> **warning** Be cautious enabling "Execute safe commands". On Windows and with some project setups (for example, Python virtual environments like venv or conda), Cline may run installation commands outside your intended environment. That can cause failures and generate additional API calls and costs. It's recommended to keep automatic execution off and run commands yourself when using environments you manage manually.

### Quick reference: toggles and recommendations

| Toggle                | What it does                                               | Recommendation                                                        |
| --------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------- |
| Auto-approve          | Automatically accepts and applies generated changes        | Use only in trusted projects or CI-like contexts                      |
| Allow read            | Lets Cline read files/folders you attach                   | Enable to provide accurate context; limit file set to necessary files |
| Allow edit            | Lets Cline modify files directly                           | Use cautiously; prefer review before applying in new projects         |
| Execute safe commands | Runs pre-approved terminal commands (e.g., install, start) | Keep off for manual environments (venv, conda, WSL)                   |

## Main input and context management

The central input area is where you type tasks and instructions. Use the `@` syntax to attach context items (files, folders, terminal logs) so Cline can make accurate suggestions. Slash commands make workflow faster:

```text theme={null}
/newtask
Create a new task with context from the current task

/smol
Condenses your current context window

/newrule
Create a new Cline rule based on your conversation

/reportbug
Create a GitHub issue with Cline
```

> **lightbulb** Two primary context types affect results and token usage:

  * Conversation context — message history in the task thread. Long histories can dilute the LLM's focus.
  * Project/file context — files and folders you attach. More files = more tokens used.
    Use `/smol` to condense conversation context and reduce token consumption while keeping essential details.

Cline also supports client-specific "rules" generated from a conversation to enforce coding style or guardrails. The `/reportbug` command can open a GitHub issue directly from the extension.

## API provider and model selection

Cline lets you select the API provider and model used for generation. Open the provider dropdown to choose from options like Cline’s default, OpenRouter, Anthropic, Claude, LM Studio, and others. From the same area you can review billing/usage and pick the desired model.

<Frame>
  <img alt="A dark-themed code editor UI with an &#x22;API Provider&#x22; dropdown open showing options like Cline, OpenRouter, Anthropic, Claude, and others. The right side shows a large editor logo and keyboard shortcut hints." />
</Frame>

## What we'll build in this lesson series

This lesson covers initial workspace setup and shows features you'll use while building a small project: a casting number lookup tool.

* Purpose: enter a casting number found on an engine and return details such as motor model and production year.
* Workflow highlights: attaching files for context, creating tasks, configuring models, and using Cline’s suggestions to iterate quickly.

That's the quick tour of the initial workspace and settings. Later in the series we'll dive deeper into creating the casting number lookup, attaching project files for context, and using Cline to generate and apply fixes.

## Links and references

* [Visual Studio Code — Download & Docs](https://code.visualstudio.com/)
* [VS Code Extensions Marketplace](https://marketplace.visualstudio.com/)
* Cline — check the extension page in your editor's marketplace for the latest docs and release notes.

- [Watch Video](https://learn.kodekloud.com/user/courses/cline/module/07505364-dfb1-4691-8f55-ce69bc5e81ec/lesson/e9b7e535-1529-44be-8dd1-702c06a7b7dc)
