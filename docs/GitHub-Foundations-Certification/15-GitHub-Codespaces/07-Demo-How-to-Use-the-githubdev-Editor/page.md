# check Node.js and GitHub CLI versions
node -v
gh --version
```

Example output:

```bash theme={null}
$ node -v
v24.14.0

$ gh --version
gh version 2.8.0 (2026-03-10)
https://github.com/cli/cli/releases/tag/v2.8.0
```

Quick reference — useful commands:

| Purpose                  | Command                             |
| ------------------------ | ----------------------------------- |
| Check Node               | `node -v`                           |
| Check GitHub CLI         | `gh --version`                      |
| Create and switch branch | `git checkout -b feature-workspace` |
| Stage changes            | `git add <files>`                   |
| Commit changes           | `git commit -m "message"`           |
| Push branch to remote    | `git push -u origin <branch>`       |

## 3. Install optional VS Code extensions

Install any extensions you need inside the Codespace just like you would locally. For live HTML previews, consider:

* Live Preview: [https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server-preview](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server-preview)
* Live Server: [https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

Open the Extensions view in Codespaces and install the extension that matches your workflow.

## 4. Preview the app

The project already includes a simple HTML entry point. Open the file in the editor and use Live Server / Live Preview to launch a browser tab that shows the running game:

```html theme={null}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Block Buster - Enhanced Edition</title>
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <div class="container">
        <!-- Welcome Screen -->
        <div class="screen active welcome-screen" id="welcomeScreen">
            <div class="header">
                <h1 class="title">BLOCK BUSTER</h1>
                <p class="subtitle">Enhanced Edition with Random Levels & Power-ups</p>
            </div>
        </div>
        <div class="game-screen"></div>
    </div>
</body>
</html>
```

Open the app with your chosen preview extension and a new browser tab will display the game.

<Frame>
  <img alt="The image displays a screenshot of a video game called &#x22;Block Buster,&#x22; featuring colorful blocks arranged in a pattern with a paddle and ball at the bottom. The game screen shows various statistics like score, high score, lives, and level indicators." />
</Frame>

## 5. Make a UI change in a feature branch

Create and switch to a new branch before editing:

```bash theme={null}
# create and switch to a feature branch
git checkout -b feature-workspace
```

Open `style.css` (or `style.scss`) and locate the `:root` variables. The existing variables might look like this:

```css theme={null}
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f09f3f 0%, #f5576c 100%);
  --dark-bg: #0f1f20;
  --card-bg: rgba(255, 255, 255, 0.2);
  --card-border: rgba(255, 255, 255, 0.2);
  --accent-cyan: #00d4fa;
  --accent-lime: #8fdc5f;
  --accent-purple: #c24cf6;
  --text-primary: #ffffff;
  --text-secondary: #bbbb0c;
  --power-multi: #ff6bb6;
}
```

To switch the UI accent color, update the variables — here is an example pinker theme:

```css theme={null}
:root {
  --primary-gradient: linear-gradient(180deg, #764ba2 100%);
  --secondary-gradient: linear-gradient(180deg, #f5576c 100%);
  --dark-bg: #0a0a0a;
  --card-bg: #ffffff;
  --card-border: #eaeaea;
  --accent-cyan: #1eb1b7;
  --accent-lime: #78d20a;
  --accent-purple: #c24cf6;
  --text-primary: #ffffff;
  --text-secondary: #bbbb0c;
  --power-multi: #f6bbcb;
}
```

Save the file and refresh the Live Preview tab — CSS variables update immediately so you can iterate quickly.

<Frame>
  <img alt="The image shows a game menu for &#x22;Block Buster&#x22; featuring options for game type, levels, power-ups, high scores, and features, with buttons to start the game or reset scores." />
</Frame>

## 6. Commit and publish your branch

When you're satisfied with the change, stage, commit, and push the branch:

```bash theme={null}
git add style.css
git commit -m "Update accent colors for UI theme"
git push -u origin feature-workspace
```

VS Code may prompt to publish the branch for you (creating the upstream). It can also offer to open a pull request — you can create that PR immediately or from the GitHub UI later.

After pushing, confirm the branch and commit appear on GitHub.

<Frame>
  <img alt="This image shows a GitHub repository page titled &#x22;block-buster,&#x22; featuring various files such as .github, .gitignore, and README.md, along with additional repository details on the right side." />
</Frame>

## 7. Codespace lifecycle: stopped vs deleted

A convenient detail of Codespaces is that stopping a Codespace preserves the VM state (open files and uncommitted changes) so you can resume work later. However, deleting the Codespace permanently removes its data.

<Frame>
  <img alt="The image shows a Visual Studio Code editor with a project containing several files in the sidebar, including &#x22;index.html,&#x22; &#x22;README.md,&#x22; and &#x22;script.js.&#x22; The content of &#x22;newfile&#x22; is displayed in the main window with the text &#x22;some content.&#x22;" />
</Frame>

> **warning** Before deleting a Codespace, commit and push any changes you want to keep. Stopping preserves open files and uncommitted work for your next start, but deleting removes all Codespace data permanently.

## Summary

* Create a Codespace to get an instant cloud-hosted VS Code environment.
* Verify Node.js and `gh` are available, and install any needed extensions.
* Use Live Server / Live Preview to iterate on UI changes quickly.
* Branch, commit, and push changes back to GitHub.
* Stop Codespaces to preserve state; delete only when you no longer need the instance.

## Links and References

* [GitHub Codespaces documentation](https://docs.github.com/en/codespaces)
* [Visual Studio Code](https://code.visualstudio.com/)
* [Node.js](https://nodejs.org/)
* [GitHub CLI](https://cli.github.com/)
* Live Preview: [https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server-preview](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server-preview)
* Live Server: [https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/eb17349d-56d1-4fbb-b47f-3659970365d6)


# Demo How to Use the githubdev Editor

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/Demo-How-to-Use-the-githubdev-Editor/page

Guide to creating and sharing GitHub Codespaces deep links and using the github.dev web editor for quick repository edits versus full Codespace environments

This guide explains how to create and share GitHub Codespaces deep links for quick environment launch and how to use the lightweight `github.dev` editor to edit repository files without starting a full Codespace. It covers:

* What a Codespaces deep link is and how to generate one
* How to embed a deep link in your README
* How and when to use the `github.dev` web editor for quick edits
* Limitations of `github.dev` and when to opt for a full Codespace

## What is a Codespaces Deep Link?

A Codespaces deep link is a shareable URL that points users to a repository-specific page where they can create or resume a GitHub Codespace. You can include startup parameters in the URL (branch, devcontainer, machine type, etc.) so collaborators open a Codespace with the intended environment immediately.

Official documentation: [Codespaces Deep Link](https://docs.github.com/en/codespaces/developing-in-codespaces/sharing-a-deep-link-to-a-codespace)

### Common URL parameters

| Parameter      | Purpose                                           | Example                                        |
| -------------- | ------------------------------------------------- | ---------------------------------------------- |
| `repository`   | Specifies the repository to open                  | `repository=OWNER/REPO`                        |
| `ref`          | Selects the branch or ref to open                 | `ref=BRANCH`                                   |
| `machine`      | (Optional) Selects machine type                   | `machine=standardLinux`                        |
| `devcontainer` | (Optional) Points to a devcontainer configuration | `devcontainer=.devcontainer/devcontainer.json` |

Example pattern (use the exact snippet GitHub provides or update `OWNER/REPO` and `BRANCH`):

```markdown theme={null}
[Open in Codespaces](https://github.com/codespaces/new?repository=OWNER/REPO&ref=BRANCH)
```

## How to create and share a deep link

1. Open the repository on GitHub.
2. Click the green **Code** button.
3. Choose **Codespaces**, then select **Share a deep link**.
4. Pick an output format: **URL**, **HTML**, or **Markdown**. Use the Markdown snippet for README embedding.

<Frame>
  <img alt="The image shows a GitHub repository page with a pop-up menu for sharing codespace configuration, displaying options for URL, HTML, and Markdown snippets." />
</Frame>

If you choose the Markdown option, paste the snippet into your README so viewers can click it to create a Codespace. The Markdown snippet is ready-to-use and helps contributors launch the repository with the configured environment.

## Edit files quickly with `github.dev` (no Codespace needed)

When you only need to make simple edits (README, docs, small code changes), use the `github.dev` editor — a fast, browser-based VS Code-like editor that edits files directly in the repository without starting a container.

How to open:

* Press the `.` (period) key while viewing the repository on GitHub, or
* Click **Code** and select the `github.dev` option.

In the `github.dev` editor you can:

* Make edits in the browser
* Cancel any unnecessary prompts (for example, GitHub Actions setup prompts)
* Commit changes using the web UI

Committing a small README change from the web UI performs the equivalent local Git commands:

```bash theme={null}
git add README.md
git commit -m "added Codespace deep link"
git push
```

After pushing, the Markdown deep link will be visible in the README. Users who click it will be taken into the Codespaces flow for your repository. If GitHub detects a previous session, it may offer to resume that session or create a new Codespace.

<Frame>
  <img alt="The image shows a GitHub Codespaces interface prompting the user to resume a previous session for a project called &#x22;block-buster,&#x22; with options to resume or create a new codespace." />
</Frame>

When creating a new Codespace, GitHub displays configuration options such as branch selection, machine type, and devcontainer settings so you can launch with the desired environment.

> **lightbulb** The `github.dev` editor is ideal for quick edits, documentation updates, and light browsing of the codebase. It does not run a development container, and you cannot launch terminals or run/debug code from it. Use a full Codespace when you need a runnable environment, terminal access, or debugging capabilities.

## When to use each option

| Task                                            | Use `github.dev`    | Use Codespaces deep link / full Codespace |
| ----------------------------------------------- | ------------------- | ----------------------------------------- |
| Edit README or docs                             | ✅ Fast, lightweight | ❌ Overkill                                |
| Run or debug code                               | ❌ Cannot run/debug  | ✅ Full environment needed                 |
| Configure dev container or machine type         | ❌ Not applicable    | ✅ Include parameters in deep link         |
| Share reproducible environment for contributors | ❌ Not applicable    | ✅ Use deep link with parameters           |

## Links and references

* [Codespaces Deep Link documentation](https://docs.github.com/en/codespaces/developing-in-codespaces/sharing-a-deep-link-to-a-codespace)
* [github.dev — quick editor](https://github.dev)
* [GitHub Codespaces overview](https://docs.github.com/en/codespaces)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/a5e085d4-37f1-4526-8f24-7e49180f8305)
