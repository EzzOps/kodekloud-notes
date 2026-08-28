# (but do not run this cell)
```

and then re-run the `print(foo)` cell without running the updated assignment cell, the output remains `2`. To update the kernel state, run the assignment cell or restart and re-run the notebook in order.

Restarting the kernel (Kernel → Restart & Clear Output) clears state and outputs and is useful to confirm reproducibility.

***

## 4) Store a secure `.env` file for your API key

Keeping secrets outside source control is essential. Create a `.env` file locally and never commit it.

Create `.env` programmatically (replace `YOUR_OPENAI_API_KEY` with your real key after you obtain it):

```python theme={null}
with open(".env", "w") as f:
    f.write("OPENAI_API_KEY=YOUR_OPENAI_API_KEY")
```

Add `.env` to `.gitignore` before committing:

```text theme={null}
.env
```

Example `.env` content (do not paste real keys into shared or public files):

```text theme={null}
OPENAI_API_KEY=[OPENAI_API_KEY]
```

<Callout icon="warning">
  Do not commit `.env` or your API keys to GitHub. Keep secrets out of version control and use environment-specific secret management in production.
</Callout>

***

## 5) Getting your OpenAI API key

1. Go to the OpenAI dashboard: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Log in or create an account.
3. From the dashboard, open Settings (cogwheel) → API keys.
4. Create a new secret key, give it a descriptive name (e.g., `Demo API Key final`), and copy it immediately — the secret is shown only once.

<Frame>
  <img alt="The image shows an API key management interface on the OpenAI platform, displaying a &#x22;Save your key&#x22; pop-up with an API key and instructions. The background lists several API keys with options to edit or delete them." />
</Frame>

After creating the key, paste it into your `.env` file (or update the file manually).

***

## 6) Loading environment variables in Python

Install python-dotenv if not already installed:

```bash theme={null}
pip install python-dotenv
```

Load the `.env` and verify the key is present:

```python theme={null}
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("OPENAI_API_KEY") is not None)  # Should print: True
```

***

## 7) Add a small code test to the notebook

Add a few simple cells to confirm everything runs:

```python theme={null}
print(1)
print("Hello World")
```

***

## 8) Set up a GitHub repository and commit safely

1. Sign in to GitHub: [https://github.com](https://github.com)
2. Create a new repository (e.g., `Demo-API-Setup`). Choose private if you prefer and add a README.

<Frame>
  <img alt="The image shows a GitHub interface for creating a new repository. It features fields for the repository name, description, visibility options, and additional setup choices like adding a README file." />
</Frame>

Confirm `.gitignore` includes `.env` before committing.

Quick Git commands (run from your project root):

| Command                                                                     | Purpose                                            |
| --------------------------------------------------------------------------- | -------------------------------------------------- |
| `git init`                                                                  | Initialize a new repository                        |
| `git add .`                                                                 | Stage all files (ensure `.gitignore` is set first) |
| `git commit -m "Initial commit"`                                            | Create the first commit                            |
| `git branch -M main`                                                        | Rename the default branch to `main`                |
| `git remote add origin https://github.com/your-username/Demo-API-Setup.git` | Add your remote (replace with your URL)            |
| `git push -u origin main`                                                   | Push commits to GitHub and set upstream            |

Replace the remote URL with your repository's HTTPS or SSH URL.

***

## Wrap-up

You have completed the essential setup:

* Installed Anaconda and launched Jupyter Notebook.
* Learned to manage kernels and run cells reliably.
* Created and loaded a secure `.env` file for your OpenAI API key using `python-dotenv`.
* Created a GitHub repository and prepared your project to avoid committing secrets.

Use this workflow for future projects to keep secrets safe, ensure reproducibility, and maintain clear version control for notebooks.

***

## Links and references

* Jupyter: [https://jupyter.org](https://jupyter.org)
* Anaconda distribution: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)
* OpenAI API keys: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
* python-dotenv: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
* GitHub: [https://github.com](https://github.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/145dc5be-8a43-4ff3-ba90-7d93e142a799/lesson/3dae1676-8e6d-4381-bd26-7f60cec87508" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents/module/145dc5be-8a43-4ff3-ba90-7d93e142a799/lesson/8c350622-2e2d-40a2-be1f-8473b1438a8d" />
</CardGroup>


# Development Environment Overview

Source: https://notes.kodekloud.com/docs/AI-Agents/Building-AI-Agents/Development-Environment-Overview/page

Overview of using Jupyter and GitHub to build reproducible, collaborative development environments and workflows for AI agent engineering.

Welcome back.

This lesson reviews the development-environment landscape for AI agent engineering, focusing on Jupyter Notebook and GitHub. We'll explain why a reproducible, collaborative environment matters for agents and provide practical guidance, commands, and patterns you can apply immediately.

We’ll cover:

* The role of development environments in AI agent engineering
* What Jupyter is and why it fits agent workflows
* Key Jupyter features for AI workflows
* What GitHub is and why it matters for agents
* GitHub features for collaboration and CI/CD
* Version-control practices for agent projects
* How to integrate Jupyter with GitHub (plus commands and examples)
* A concrete end-to-end example workflow
* Common pitfalls and how to avoid them
* Useful tools and extensions for Jupyter and GitHub
* Security and best practices
* Summary and next steps

AI agents combine prompts, tool calls, LLM invocations, and memory/state management. A solid development environment accelerates experimentation, ensures reproducibility, and enables safe collaboration. In short, Jupyter and GitHub are not just conveniences — they are foundational for building, debugging, and iterating on agent systems.

<Frame>
  <img alt="The image is an infographic titled &#x22;Why a Solid Dev Environment Matters for Agents,&#x22; highlighting benefits like promoting clean AI development, supporting rapid prototyping, scaling agent pipelines, enabling collaboration, and centralizing code and experiments." />
</Frame>

Why development environments matter for agents

* Centralize code, experiments, and documentation so results are reproducible and auditable.
* Enable rapid, iterative testing (change prompts or parameters and see results immediately).
* Support automated testing, CI/CD, and controlled rollouts as agents evolve.
* Reduce onboarding friction by standardizing development environments across teams.

<Frame>
  <img alt="The image illustrates the role of development environments, highlighting their importance in centralizing code, fostering collaboration, ensuring reproducibility, enabling rapid prototyping, and aiding debugging and scaling. It features a semicircular diagram with labeled sections, each associated with a unique icon representing these functions." />
</Frame>

## Jupyter: overview and why it fits agent workflows

Jupyter is an open-source, interactive environment that runs in the browser and combines executable code, outputs, visualizations, and Markdown documentation in a single notebook file (`.ipynb`). It’s a natural fit for agent development because:

* Incremental, cell-based execution enables fast experimentation: tweak prompts, embeddings, or tool calls and inspect responses without rerunning unrelated initialization.
* The mixed code/Markdown format is ideal for documenting design choices, hypotheses, and results alongside runnable code.
* Jupyter supports many languages (Python, Julia, R), but Python is the dominant choice for LLM, embeddings, and agent toolchains.
* You can import SDKs and libraries (for example, OpenAI SDKs and LangChain) directly in notebooks to prototype integrations quickly.

Resources:

* [Introduction to OpenAI](https://learn.kodekloud.com/user/courses/introduction-to-openai)
* [LangChain course](https://learn.kodekloud.com/user/courses/langchain)

### Key Jupyter features for agent development

* Cell-based execution for incremental testing of code that calls external APIs or manipulates memory.
* Inline visualizations and stdout/stderr outputs to inspect agent behavior and tool responses.
* Markdown cells to explain experiment intent, assumptions, and conclusions next to code.
* Extensible ecosystem (JupyterLab, nbextensions, VS Code/Jupyter plugins) for navigation, Git integration, and productivity.

## GitHub: why it matters for agent projects

GitHub, built around Git, is the standard platform for collaborative development and version control. For agent projects it provides:

* A complete history of changes so you can restore previous prompt states, tool configs, or decision logic.
* Pull requests and issue tracking for asynchronous collaboration and structured code review.
* Automation through GitHub Actions for CI, testing, and deployment pipelines.
* Integration with assistive tools like GitHub Copilot to speed development and refactoring.
* A centralized place to publish and discover open-source agent frameworks and integrations.

<Frame>
  <img alt="The image illustrates the importance of GitHub, highlighting its features like change tracking, issue management, and code rollback. It also mentions GitHub as a central hub for publishing frameworks, tools, and open-source projects." />
</Frame>

### GitHub features especially helpful for AI projects

* Fine-grained change history for code, prompts, and configuration.
* Branching and pull requests to isolate experiments and review behavior changes.
* GitHub Actions for automated linting, unit tests, notebook validation, and deployments.
* Issue templates, project boards, and discussions to track experiments, evaluations, and reproducibility tasks.

## Version control practices for agent projects

Version control in agent projects goes beyond tracking source files — it manages evolving prompts, toolchains, and data dependencies. Best practices:

* Use branches to isolate experiments and new capabilities.
* Write descriptive commit messages that explain why a prompt or architecture changed (not just what changed).
* Use code reviews to discuss behavioral differences and regressions.
* Track experiments and model artifacts separately (see DVC / MLflow below).

<Frame>
  <img alt="The image is an infographic titled &#x22;Version Control in Agent Projects,&#x22; illustrating three benefits: tracking changes, enabling branching, and supporting peer reviews and controlled releases." />
</Frame>

## Integrating Jupyter with GitHub — practical tips and commands

Notebooks are JSON files (`.ipynb`) and can produce noisy diffs because they store outputs. Use the following strategies to keep repositories clean and maintainable.

Recommended tooling and patterns:

* Remove outputs before committing:
  * Use `nbstripout` to automatically clear outputs on commit.
  * Example installation and activation:
    ```bash theme={null}
    pip install nbstripout
    nbstripout --install
    ```
* Use pre-commit hooks for consistent repo hygiene:
  * Example `.pre-commit-config.yaml` snippet:
    ```yaml theme={null}
    repos:
      - repo: https://github.com/kynan/nbstripout
        rev: v0.5.0
        hooks:
          - id: nbstripout
    ```
  * Install:
    ```bash theme={null}
    pip install pre-commit
    pre-commit install
    ```
* Use Git LFS for large artifacts (embeddings, model checkpoints):
  ```bash theme={null}
  git lfs install
  git lfs track "*.onnx"
  git add .gitattributes
  ```
* Use `papermill` for parameterized runs (turn notebooks into reproducible, parameter-driven jobs):
  ```bash theme={null}
  pip install papermill
  papermill input.ipynb output.ipynb -p param_name value
  ```
* Use `nbdime` for notebook-aware diffs and merges:
  ```bash theme={null}
  pip install nbdime
  nbdime config-git --enable
  ```

Best UX workflow:

* Prototype in a notebook.
* Extract stable code into Python modules or packages.
* Keep notebooks for orchestration, examples, and documentation; put production logic into versioned modules.
* Use GitHub Codespaces, JupyterLab, or VS Code to synchronize work across collaborators.

## Example end-to-end agent development workflow

1. Prototype in Jupyter:
   * Create prompt templates, test API calls, and log results in Markdown and output cells.
2. Stabilize logic:
   * Extract reusable code into modules (e.g., `agents/core.py`, `agents/tools.py`) and add unit tests.
3. Commit and clean:
   * Commit notebooks and scripts to GitHub. Use `.gitignore` to exclude secrets and `nbstripout` to strip outputs.
4. Branch and experiment:
   * Use feature branches per experiment, then open pull requests to review behavior changes.
5. Automate:
   * Use GitHub Actions to run linting, unit tests, and notebook validation on PRs.
6. Deploy and test:
   * Deploy to staging and run integration tests before promoting to production.

Common Git commands for this flow:

```bash theme={null}
git checkout -b feature/prompt-refactor
git add .
git commit -m "Refactor prompt to improve slot-filling"
git push origin feature/prompt-refactor
```

<Frame>
  <img alt="The image depicts an example workflow for an agent project lifecycle, illustrating steps such as starting a prototype in Jupyter, pushing versions to GitHub, and merging changes documented in a README." />
</Frame>

## Common pitfalls and mitigations

* Large outputs and binary artifacts increase repository size and create noisy diffs.
  * Mitigation: enable `nbstripout`, use Git LFS, and clear outputs before committing.
* Merge conflicts in `.ipynb` files due to JSON format.
  * Mitigation: break code into modules, do smaller, frequent merges, and use `nbdime` to resolve notebook diffs.
* Accidental commit of sensitive data (API keys, tokens).
  * Mitigation: put secrets in `.env`, add them to `.gitignore`, use secret scanning, and rotate credentials if exposed.
* Monolithic notebooks mixing experiments and production logic.
  * Mitigation: modularize and keep notebooks primarily for orchestration and documentation.

<Callout icon="warning">
  Avoid committing credentials or large outputs. Use `.gitignore`, `.env` files, secret scanners, `nbstripout`, and Git LFS to keep your repository secure and performant.
</Callout>

## Tools and extensions to improve workflow

* nbextensions: code folding, variable inspectors, table of contents for classic notebooks.
* JupyterLab: modern multi-tab interface with terminals and rich extensions.
* GitHub Codespaces: cloud dev environments with Jupyter pre-installed for consistent environments.
* VS Code + Jupyter plugin: edit notebooks locally with robust Git and debugging support.
* DVC and MLflow: version and track datasets, models, and experiments.

Useful quick-reference table

| Tool / Feature | Purpose                      | Example / Command                                     |
| -------------- | ---------------------------- | ----------------------------------------------------- |
| `nbstripout`   | Remove outputs before commit | `nbstripout --install`                                |
| `pre-commit`   | Enforce repository hooks     | `pre-commit install`                                  |
| Git LFS        | Track large model artifacts  | `git lfs install`                                     |
| `papermill`    | Parameterized notebook runs  | `papermill in.ipynb out.ipynb -p learning_rate 0.001` |
| `nbdime`       | Notebook-aware diffs/merges  | `nbdime config-git --enable`                          |
| DVC / MLflow   | Experiment & data tracking   | See DVC and MLflow docs                               |

<Frame>
  <img alt="The image lists five productivity tools and extensions: nbextensions, Jupyter Lab, GitHub Codespaces, VS Code + Jupyter Plugin, and DVC or MLflow, with brief descriptions of their features." />
</Frame>

## Security and best practices (brief)

* Never hard-code API keys in notebooks. Use environment variables, `.env` files, or secret managers.
* Add tests and linters to CI/CD to catch regressions in prompt handling and tool integrations.
* Modularize production logic into versioned packages; use notebooks for experiments and documentation.
* Keep a CHANGELOG or use detailed commit messages to record rationale for prompt and architecture changes.

<Callout icon="lightbulb">
  Best practices summary: modularize code, use branches and pull requests, log key changes, and never commit secrets. These habits improve reproducibility, collaboration, and long-term maintainability of agent projects.
</Callout>

## Summary and next steps

Jupyter and GitHub together form a powerful foundation for building AI agents:

* Use Jupyter notebooks for rapid prototyping, interactive debugging, and documentation.
* Use GitHub for version control, code review, CI/CD, and collaboration.
* Adopt tooling like `nbstripout`, `nbdime`, GitHub Actions, and Git LFS to keep repos clean and reproducible.
* Move stable logic into modular Python packages and track experiments with DVC or MLflow.

Actionable next steps:

* Add `nbstripout` and a `pre-commit` config to your repo.
* Start a branch-based workflow for experiments.
* Configure a simple GitHub Actions workflow to run linting and tests on PRs.
* Create a short README that documents how to run notebooks, tests, and parameterized runs.

By investing in these development practices now, you make agent engineering faster, safer, and more collaborative as your project grows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/145dc5be-8a43-4ff3-ba90-7d93e142a799/lesson/648a1e3d-ddf1-4a2d-8a66-3a0435514483" />
</CardGroup>
