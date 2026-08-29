# Easier navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

# Shortcuts
alias home='cd ~'
alias back='cd -'
alias d='cd ~/Documents/Dropbox/'
alias d1='cd ~/Downloads/'
alias dt='cd ~/Desktop/'
alias p='cd ~/projects'
alias g='git'
alias cls='clear'
```

Useful links:

* [Using a dotfiles repository](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-your-profile/using-a-dotfiles-repository)
* [Settings Sync for Visual Studio Code](https://code.visualstudio.com/docs/editor/settings-sync)

## 2. Workspace and resource management

The second layer covers workspace sizing and lifecycle controls. Tailor compute resources (CPU and memory) to the demands of your work: heavier builds or data science tasks benefit from more powerful machine types. Configure the region to reduce latency or meet data residency needs.

You can also manage costs and lifecycle with:

* Inactivity timeout (default: 30 minutes) to suspend idle Codespaces
* Auto-delete period for stopped Codespaces (up to 30 days)
* Custom display names to quickly identify multiple active environments

<Frame>
  <img alt="The image shows a setup screen for creating a codespace, highlighting options for Dev container configuration, Region, and Machine type. It includes an example from GitHub Codespaces, with settings like branch, region, and machine specifications." />
</Frame>

## 3. Editor and tooling preferences

The third layer is your editor and tooling choices. Select a primary interface for each session:

* Visual Studio Code (desktop or web)
* JetBrains IDEs via JetBrains Gateway
* JupyterLab for interactive Python/data workflows

Set the default shell for new terminals and preinstall extensions or plugins from the VS Code Marketplace or JetBrains Marketplace to make every Codespace ready for your workflow.

<Frame>
  <img alt="The image shows a user interface for selecting editor and tooling preferences, featuring icons for Visual Studio Code, JetBrains, and Jupyter. Options for default editor, shell customization, and extensions & plugins are also visible." />
</Frame>

Settings Sync can automatically propagate themes, keybindings, and extensions so your personal editor configuration follows you into each Codespace.

## Quick comparison: customization layers

| Layer                 | What it controls                   | Examples                                        |
| --------------------- | ---------------------------------- | ----------------------------------------------- |
| Environment sync      | Personal editor and shell settings | `Settings Sync`, dotfiles, themes, keybindings  |
| Workspace & resources | Compute, region, lifecycle         | Machine type, inactivity timeout, auto-delete   |
| Editor & tooling      | Preferred IDE and extensions       | VS Code, JetBrains Gateway, JupyterLab, plugins |

Resources and references:

* [GitHub Codespaces](https://github.com/features/codespaces)
* [Dev Containers (devcontainer.json)](https://code.visualstudio.com/docs/devcontainers/containers)
* [VS Code Marketplace](https://marketplace.visualstudio.com/)
* [JetBrains Gateway](https://www.jetbrains.com/remote-development/gateway/)

> **lightbulb** Note: Dev container configuration (the project's [devcontainer.json](https://code.visualstudio.com/docs/devcontainers/containers)) defines the canonical, team-wide environment. Personal customizations applied via Settings Sync and dotfiles will be applied where allowed, but dev container settings may override or restrict some changes.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/66edf730-bc7e-4b34-8299-0119d475cfc6)


# Demo Configure a Codespace

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/Demo-Configure-a-Codespace/page

Guide to creating a GitHub Codespace, previewing and editing a web app in cloud VS Code, then committing and pushing UI changes to the repository

In this guide you'll create a GitHub Codespace for the example "block-buster" repository, preview the app in the browser, make a UI change in a feature branch, and push that branch back to GitHub. Using Codespaces lets you skip local environment setup and jump directly into a cloud-hosted VS Code instance with common developer tools preinstalled.

<Frame>
  <img alt="The image shows a GitHub repository page with a code files list, including HTML, CSS, and JavaScript files, and indicates that no codespaces are currently checked out for this repository." />
</Frame>

## 1. Create a Codespace

From the repository page open the Codespaces menu and click Create codespace (choose the main branch or another branch you prefer). After a short initialization step, GitHub launches a browser-hosted Visual Studio Code session with common tools and language runtimes already installed.

<Frame>
  <img alt="The image displays a Visual Studio Code interface running in a web browser, with a project named &#x22;block-buster&#x22; open, showing files like index.html and script.js in the explorer panel. The terminal window displays a welcome message for Codespaces, and a &#x22;Build with Agent&#x22; section is visible on the right." />
</Frame>

## 2. Verify common developer tools

Confirm that Node.js and the GitHub CLI are available in the Codespace terminal:

```bash theme={null}
