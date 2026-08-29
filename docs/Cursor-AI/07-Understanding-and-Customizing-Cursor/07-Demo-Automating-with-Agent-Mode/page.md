# Demo Automating with Agent Mode

Source: https://notes.kodekloud.com/docs/Cursor-AI/Understanding-and-Customizing-Cursor/Demo-Automating-with-Agent-Mode/page

This walkthrough explores using Agent Mode in Cursor AI to automate a Python project, including data processing, test generation, and documentation.

In this walkthrough, we’ll explore how to use **Agent Mode** in Cursor AI to automate a full Python project—from reading customer data to generating tests and documentation—in minutes. You’ll learn how to:

* Enable and configure **Autocompletion** safely.
* Define an allowlist/denylist for automated commands.
* Generate code, tests, and docs with a single instruction set.
* Run and verify the output locally using a Python virtual environment.

## Prerequisites

* Cursor AI with **Agent Mode** enabled
* Python 3.8 or higher installed
* A CSV file named `customers.csv` containing customer data

## 1. Enable Autocompletion Mode

First, open **Cursor Settings** and turn on **Autocompletion mode**. Read the disclaimer carefully before proceeding.

> **triangle-alert** Enabling Autocompletion mode may increase the risk of prompt injection. Only proceed if you trust the source of your prompts.

![The image shows a software interface with a dark theme, displaying a "Cursor Settings" menu with various options related to auto-run mode, command allowlist/denylist, and file protection. A file named "customers.csv" is open in the sidebar.](https://kodekloud.com/kk-media/image/upload/v1752872787/notes-assets/images/Cursor-AI-Demo-Automating-with-Agent-Mode/cursor-settings-dark-theme-interface.jpg)

### Configure Autocompletion Settings

| Setting           | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| Auto Run Prompt   | Natural-language instructions the agent will execute automatically.       |
| Command Allowlist | List commands the agent is permitted to run (e.g., `pip install pytest`). |
| Command Denylist  | Block undesired commands (e.g., `rm -rf /`).                              |
| File Protection   | Prevent deletion or modification of critical files.                       |
| MCP Tools         | Disable resource-intensive operations to control cloud costs.             |

Save these settings and switch to **Agent** mode.

## 2. Attach Data and Select Model

1. Upload `customers.csv` (large CSV with customer records).
2. Choose whether to include the full context or let the agent use intelligent compression.
3. Select your model (e.g., `gpt-4o-cloud`).

## 3. Provide an Instruction List

Ask the agent to perform these steps:

1. Create `process_customers.py` to read `customers.csv`.
2. Extract first and last names → write to `namevalues.csv`.
3. Extract phone numbers → write to `phone.txt`.
4. Install `pytest`.
5. Generate a `pytest` test suite validating the script.

Click **Generate**. The agent will:

* Read the first 200 lines of `customers.csv`.
* Produce `process_customers.py` with data-processing logic.
* Create unit tests in `test_process_customers.py`.
* Display all proposed code changes for your approval.

Once you **Accept**, the files appear in your workspace.

## 4. Set Up Your Local Environment

Open a terminal and create a Python virtual environment:

```bash theme={null}
