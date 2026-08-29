# GitHub Codespaces

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/GitHub-Codespaces/page

Cloud-hosted, containerized development environments integrated with GitHub providing instant, reproducible VS Code workspaces and seamless collaboration

What is GitHub Codespaces?

GitHub Codespaces is a cloud-hosted development environment tightly integrated with GitHub. It delivers a containerized, high-performance workspace so you can write, run, and debug code directly in your browser or from a local IDE. Codespaces removes local setup friction and provides a consistent, reproducible developer environment for teams of any size.

Below is a small Ruby class example — the kind of code you could edit, run, and debug inside a Codespace.

```ruby theme={null}
class Emotion
  attr_reader :label, :pronounceable_label

  # Public: Get the Emoji that this reaction's content represents.
  #
  # Returns an Emoji.
  def initialize(content:, label: nil, pronounceable_label: nil, emoji_character: nil)
    @content = content
    @label = label || @content
    @pronounceable_label = pronounceable_label || @label
    @emoji_character = emoji_character || Emoji.find_by_alias(@content)
    @platform_enum = @pronounceable_label.gsub("_", "").upcase

    freeze
  end
end

Emotion.create(content: "1", pronounceable_label: "thumbs up")
Emotion.create(content: "0", pronounceable_label: "thumbs down")
```

By hosting the environment in the cloud, Codespaces eliminates the need for complex local software installations and ensures that your development setup remains consistent across the entire team.

<Frame>
  <img alt="The image shows a promotional graphic for GitHub Codespaces, featuring a code editor interface and highlighting its capabilities with CPUs and memory." />
</Frame>

Key technical capabilities

Codespaces focuses on rapid onboarding and reproducibility. A Codespace can provision in seconds with the repository source, runtimes, and dependencies already installed. It surfaces the full Visual Studio Code experience — including the integrated terminal, debuggers, and support for the VS Code extensions ecosystem.

You can capture the exact environment as code using a repository-scoped configuration like `devcontainer.json` (and an optional `Dockerfile`). This approach defines the toolchain, OS, editor settings, and extensions the environment should contain so every developer works with an identical setup.

<Callout icon="lightbulb">
  Define development environments with `devcontainer.json` and [Dockerfiles](https://docs.docker.com/engine/reference/builder/) so Codespaces can reproduce the same toolset and settings for every developer.
</Callout>

Features at a glance

|               Feature | What it provides                                         | Example / Notes                           |
| --------------------: | -------------------------------------------------------- | ----------------------------------------- |
|  Instant provisioning | Spin up a ready-to-code environment in seconds           | Pre-installs repo dependencies and tools  |
|     Full-featured IDE | Native VS Code interface in the browser or local VS Code | Integrated terminal, debugger, extensions |
| As-code configuration | Reproducible dev environments via `devcontainer.json`    | Use a `Dockerfile` to pin OS and tooling  |
| Hardware independence | Work from low-powered machines or tablets                | Compute runs on GitHub-hosted VMs         |
|   Integrated workflow | Work with Git, PRs, CI, and Actions inside Codespaces    | Run tests and debug before merging        |

<Frame>
  <img alt="The image lists technical features such as instant provisioning, a full-featured IDE, &#x22;as-code&#x22; configuration, and hardware independence, presented in individual colored boxes." />
</Frame>

Collaboration and workflow integration

Because Codespaces is native to GitHub, you can perform Git operations, review pull requests, run CI workflows with GitHub Actions, manage branches, and collaborate with teammates without leaving the development environment. This keeps the full development loop — code, test, and review — tightly integrated and efficient.

Links and references

* [Visual Studio Code](https://code.visualstudio.com) — IDE that Codespaces exposes in the browser and desktop.
* [devcontainer.json documentation](https://code.visualstudio.com/docs/devcontainers/containers) — Define reproducible development environments.
* [VS Code Marketplace](https://marketplace.visualstudio.com/vscode) — Install extensions that run inside Codespaces.
* [Git documentation](https://git-scm.com/) — Git basics and commands.
* [GitHub Pull Requests](https://docs.github.com/en/pull-requests) — Review and collaborate on code.
* [GitHub Actions](https://docs.github.com/en/actions) — Automate CI/CD workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/32e88d7b-0029-4cec-a98f-4be14fd8be5b" />
</CardGroup>
