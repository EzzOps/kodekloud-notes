# Adding and Configuring Dev Containers

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/Adding-and-Configuring-Dev-Containers/page

Guide to defining and configuring devcontainer.json for reproducible development environments in GitHub Codespaces, including images, extensions, ports, lifecycle hooks, and features.

What are dev containers and how can we configure them for [GitHub Codespaces](https://github.com/features/codespaces)?

This guide explains the purpose of dev containers and shows how to use a `devcontainer.json` file to define a consistent, fully featured development workspace. A dev container is a Docker container configured to provide a reproducible environment that includes the operating system, runtimes, tooling, VS Code extensions, and automated setup steps.

In [GitHub Codespaces](https://github.com/features/codespaces), each session runs inside one of these containers on a high-performance VM. By defining your environment as code, every developer—regardless of their local setup—gets the exact same tools, runtimes, and editor settings.

Here is a representative `devcontainer.json` (JSON with comments / JSONC) showing common configuration options:

```json theme={null}
{
  "name": "Full Stack Environment",
  // 1. Define the base image (the operating system and runtime)
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  // 2. Install VS Code extensions automatically for the team
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  },
  // 3. Forward ports to allow browser access to the running app
  "forwardPorts": [3000, 8080],
  // 4. Run commands AFTER the container is created (e.g., install dependencies)
  "postCreateCommand": "npm install",
  // 5. Use 'features' to quickly add extra tools like the GitHub CLI
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  // 6. Set the user to 'vscode' rather than 'root' for security
  "remoteUser": "vscode"
}
```

Why this matters

* Reproducibility: Everyone uses the same base image, runtime, and extensions.
* Onboarding: New contributors can start coding without manual environment setup.
* CI parity: You can match local development containers to CI images to reduce "works on my machine" issues.

Where to place this file

* Place the `devcontainer.json` file in the repository root under `.devcontainer/` (for example `.devcontainer/devcontainer.json`). Both [GitHub Codespaces](https://github.com/features/codespaces) and [VS Code Remote - Containers](https://code.visualstudio.com/docs/remote/containers) look here to build the workspace container.

Key fields in `devcontainer.json`

| Property                           |                                                               Purpose | Example                                                         |
| ---------------------------------- | --------------------------------------------------------------------: | --------------------------------------------------------------- |
| `name`                             |                                 Human-friendly name for the container | `"Full Stack Environment"`                                      |
| `image` / `build`                  | Use a prebuilt image (`image`) or build from a `Dockerfile` (`build`) | `"image": "mcr.microsoft.com/devcontainers/javascript-node:20"` |
| `customizations.vscode.extensions` |    Auto-install VS Code extensions for anyone who opens the container | `["dbaeumer.vscode-eslint"]`                                    |
| `customizations.vscode.settings`   |                                   Workspace-specific VS Code settings | `"editor.formatOnSave": true`                                   |
| `forwardPorts`                     |                       Ports to expose from the container for previews | `[3000, 8080]`                                                  |
| `postCreateCommand`                |       One-time setup commands that run after the container is created | `"npm install"`                                                 |
| `postStartCommand`                 |                     Commands that run every time the container starts | `"./scripts/start-services.sh"`                                 |
| `postAttachCommand`                |          Commands that run after the editor attaches to the container | `"echo 'Welcome to the container!'"`                            |
| `features`                         |            Quick install of common tools using Dev Container Features | `{"ghcr.io/devcontainers/features/github-cli:1":{}}`            |
| `remoteUser`                       |    Non-root user to use inside the container for interactive sessions | `"vscode"`                                                      |

Lifecycle hooks and when to use them

| Hook                |                                       When it runs | Typical use cases / examples                                                            |
| ------------------- | -------------------------------------------------: | --------------------------------------------------------------------------------------- |
| `postCreateCommand` | Once, after the container is created (first build) | Install dependencies (`npm install`, `pip install -r requirements.txt`), scaffold files |
| `postStartCommand`  |                              Every container start | Start background processes, local services (`./scripts/start-dev-db.sh`)                |
| `postAttachCommand` |                          After the editor attaches | Display a welcome message, open specific files, run interactive checks                  |

Example: when to use `postCreateCommand` vs `postStartCommand`

* Use `postCreateCommand` for one-time setup tasks that should only run when the container is first built (for example, `npm install` or generating boilerplate files).
* Use `postStartCommand` for tasks that should run whenever the container starts (for example, starting a local database or a background watcher).

> **warning** Do not store secrets (API keys, passwords) directly in `devcontainer.json` or committed scripts. Use environment variables provided by Codespaces, GitHub Actions secrets, or other secret-management tools to inject sensitive values at runtime.

Features, tooling, and extensions

* Use the [Dev Container Features registry](https://github.com/devcontainers/features) to add common tooling quickly (GitHub CLI, Docker CLI, Python, Node.js, terraform, etc.).
* Extensions listed under `customizations.vscode.extensions` will be automatically installed for anyone opening the container—this ensures team-wide consistency for linters, formatters, and language tooling.

> **lightbulb** Dev container configuration files are JSONC (JSON with comments). To keep the `devcontainer.json` concise and maintainable, put longer or sensitive setup logic into scripts in the repository (for example, `scripts/setup.sh`) and invoke them from `postCreateCommand` or other hooks.

Summary

* A `devcontainer.json` makes your development environment portable and reproducible across machines and Codespaces.
* Store it in `.devcontainer/devcontainer.json` and use it to define the base image or Dockerfile, editor customizations, forwarded ports, lifecycle hooks, and optional features.
* In GitHub Codespaces, this file instructs Codespaces how to build each workspace container so every team member has the same environment.

Links and references

* [Dev Containers documentation (Microsoft)](https://code.visualstudio.com/docs/devcontainers/containers)
* [GitHub Codespaces](https://github.com/features/codespaces)
* [Dev Container Features registry](https://github.com/devcontainers/features)
* [GitHub CLI](https://cli.github.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/a5dff2f2-bf7e-49e1-9612-f1f4b74f044d)
