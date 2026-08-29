# Customizations With GitHub Codespaces

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/Customizations-With-GitHub-Codespaces/page

How to customize GitHub Codespaces with dev containers, dotfiles, settings sync, machine sizing, and preferred editors.

How can you personalize GitHub Codespaces to match your workflow?

GitHub Codespaces provides a flexible, cloud-hosted development environment that can be tailored at both the team and individual level. A project's dev container establishes team-wide defaults, and then you can add personal layers of customization that persist across every Codespace you create.

## 1. Environment synchronization

The first customization layer is environment synchronization. This keeps your development experience consistent across local VS Code and the web editor by syncing themes, keybindings, snippets, and editor settings.

You can also use a dotfiles repository by linking it to your GitHub account. When you configure dotfiles, GitHub automatically clones the repository and executes any setup scripts during Codespace creation, applying shell aliases, environment variables, and personal tooling preferences.

Example dotfiles aliases (place this in your dotfiles setup script or shell config):

```bash theme={null}
#!/usr/bin/env bash
