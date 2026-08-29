# inside the repository
$ git branch --list
* main

$ git branch --list -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature-1
  remotes/origin/main
```

If a remote branch (`feature-1`) exists and you want it locally, create a local tracking branch.

```bash theme={null}
# If your Git auto-creates tracking branches:
git checkout feature-1

# or explicitly create a local branch that tracks the remote:
git checkout -b feature-1 origin/feature-1

# or with the modern command:
git switch --track origin/feature-1
```

## 5. Make changes locally and push to the feature branch

Open the project in your editor (for example, Visual Studio Code) and make changes to `README.md` or add new files/folders. The image below shows a README open while on a feature branch in VS Code.

<Frame>
  <img alt="The image shows a Visual Studio Code workspace with a README.md file open, detailing a &#x22;Block Buster - Game&#x22; project using HTML, CSS, and JavaScript. There's also a terminal at the bottom displaying the current Git branch and repository information." />
</Frame>

When your edits are ready, stage, commit, and push them to the remote feature branch. You can use the editor's GUI or run these commands in the terminal:

```bash theme={null}
git add README.md
git commit -m "modified README file"
git push origin feature-1
```

<Frame>
  <img alt="The image shows a Visual Studio Code workspace with a project open, displaying a README.md file outlining features and technical details. A terminal at the bottom is ready for input, set on a feature branch." />
</Frame>

### Common Git troubleshooting (authentication / permissions)

If a push fails with a permission issue, you may see:

```bash theme={null}
$ git push origin feature-1
remote: Permission to sid-gh900/block-buster.git denied to alice-mcberry.
fatal: unable to access 'https://github.com/sid-gh900/block-buster.git/': The requested URL returned error: 403
```

A few diagnostic steps:

1. Check the currently configured remotes:
   ```bash theme={null}
   git remote -v
   ```

2. If credentials are cached and causing issues, make Git prompt for credentials by unsetting the credential helper (this may vary by OS):
   ```bash theme={null}
   git config --global --unset credential.helper
   ```
   Note: macOS Keychain, Windows Credential Manager, or other external helpers may store credentials outside Git; remove them via your OS credential manager if needed.

3. Optionally embed your username in the remote URL so Git prompts for a password for that user:
   ```bash theme={null}
   git remote set-url origin https://sid-gh900@github.com/sid-gh900/block-buster.git
   git remote get-url origin
   # origin  https://sid-gh900@github.com/sid-gh900/block-buster.git (fetch)
   ```

Important: GitHub no longer accepts account passwords for Git operations over HTTPS. Use a personal access token (PAT) instead.

<Callout icon="lightbulb">
  When pushing over HTTPS, provide a [personal access token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) as the password. Alternatively, configure an SSH key and use the SSH clone URL to avoid HTTPS-based token prompts.
</Callout>

## 6. Create and use a Personal Access Token (PAT)

To create a PAT: go to GitHub Settings → Developer settings → Personal access tokens (classic) or choose the newer fine‑grained tokens depending on your needs. For pushes you typically need `repo` scope (or repository-specific scopes for fine‑grained tokens). Set an expiration, generate the token, and copy it immediately — GitHub shows it only once.

<Frame>
  <img alt="The image shows a GitHub interface for creating a new personal access token (classic) with options for setting its expiration and permissions. Options for expiration include specific days or no expiration." />
</Frame>

When prompted for credentials during `git push`:

* Enter your GitHub username.
* Paste the PAT when asked for the password.

A successful push looks like:

```bash theme={null}
$ git push origin feature-1
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 20 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 2.38 MiB | 0 bytes/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
To https://github.com/sid-gh900/block-buster.git
   abcdef1..1234567  feature-1 -> feature-1
```

If you need to view, edit, or revoke tokens later, go to Developer settings → Personal access tokens in your GitHub account.

<Frame>
  <img alt="The image shows the GitHub Developer Settings page for personal access tokens, with an example token displayed for copying or deletion." />
</Frame>

<Callout icon="warning">
  Never commit your personal access tokens, SSH private keys, or other secrets into a repository. Use environment variables, secret managers, or GitHub Secrets for CI workflows instead.
</Callout>

## 7. Confirm changes on GitHub

Back on GitHub you can browse the `feature-1` branch to confirm your pushed changes, including README updates, images, code blocks, and project structure.

<Frame>
  <img alt="The image shows a GitHub repository page for a project called &#x22;Block Buster - Game.&#x22; It includes a README section with instructions for downloading and playing a brick breaker game built with HTML5, CSS, and JavaScript." />
</Frame>

<Frame>
  <img alt="The image shows a GitHub README section that lists features of a game, including core gameplay mechanics, power-ups, and technical features like responsive design and data persistence." />
</Frame>

## Quick reference — common commands

| Action                              | Command / Example                                               |
| ----------------------------------- | --------------------------------------------------------------- |
| Clone a repo                        | `git clone https://github.com/<owner>/<repo>.git`               |
| List branches                       | `git branch --list`                                             |
| List remote branches                | `git branch -a`                                                 |
| Create local branch tracking remote | `git checkout -b feature-1 origin/feature-1`                    |
| Switch to branch (modern)           | `git switch feature-1` or `git switch --track origin/feature-1` |
| Stage & commit                      | `git add README.md` then `git commit -m "message"`              |
| Push branch                         | `git push origin feature-1`                                     |
| View remotes                        | `git remote -v`                                                 |

## Summary

This workflow demonstrates how to:

* Create a repository on GitHub (including `README.md` and `.gitignore`).
* Upload files via the web UI or work locally after cloning.
* Create and switch to feature branches.
* Clone repositories and manage branches locally.
* Resolve common authentication issues by using a Personal Access Token (PAT) for HTTPS pushes, or by using SSH keys.

This article focuses on the basic operations described above. It does not cover pull requests, merging `feature-1` into `main`, or repository access controls in depth. To invite collaborators (for code review or contributions) go to the repository Settings → Manage access and add reviewers or contributors (for example, `Siddharth` and `Alice McBury`).

Further reading:

* [GitHub Docs — Creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository)
* [GitHub Docs — Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/8933863d-4b81-4c80-90af-2f28f8519020/lesson/64cd2e1d-48ba-4a66-b56b-a734cbb54727" />
</CardGroup>


# Demo Explain Feature Previews

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Repositories/Demo-Explain-Feature-Previews/page

How to enable and use GitHub Feature Previews to try experimental tools like slash commands, command palette, and colorblind themes for accessibility and productivity

GitHub Feature Previews let you opt in to experimental or early-stage functionality—such as public previews—so you can try upcoming features before they roll out to everyone. This is useful for testing new workflows (e.g., slash commands, the Command Palette) and accessibility options (e.g., colorblind themes) in your account.

To enable Feature Previews:

* Open your profile menu (click your user photo).
* Select **Feature preview**.
* Toggle the previews you want to try and refresh the page to apply changes.

<Frame>
  <img alt="The image shows a GitHub settings menu, highlighting the &#x22;Feature Preview&#x22; section with options for &#x22;Colorblind themes&#x22;. It displays theme choices for colorblind users, including light and dark modes for Protanopia and Deuteranopia." />
</Frame>

Common previews you may see enabled by default include slash commands and colorblind themes. Slash commands shorten repetitive Markdown tasks—like inserting tables—while colorblind themes provide accessible light and dark variants tailored for different types of color vision.

<Frame>
  <img alt="The image shows a GitHub profile interface with a feature preview window open, listing options like colorblind themes, command palette, and slash commands. The slash commands description highlights its use for simplifying Markdown typing." />
</Frame>

Another productivity-focused preview is the Command Palette. When enabled, it gives you a fast, keyboard-driven way to jump between repositories, projects, issues, and pull requests and provides a unified search for issues and PRs.

How to enable and use the Command Palette:

1. Toggle the **Command Palette** option in Feature Previews.
2. Refresh the page after enabling the toggle.
3. Press `Ctrl+K` on Windows/Linux or `Cmd+K` on macOS to open the palette.
4. Start typing the repository, issue, or action you want to jump to and select it from the popup.

<Frame>
  <img alt="The image shows a screenshot of a GitHub feature preview menu with options like &#x22;Command Palette&#x22; and &#x22;Slash Commands&#x22; highlighted. Additionally, there are account settings visible in the sidebar, suggesting it's taken from a user profile page." />
</Frame>

If the Command Palette shortcut doesn’t open GitHub’s palette right away, your browser may be intercepting the keys. Always refresh after toggling a preview so the page registers the new behavior.

<Callout icon="lightbulb">
  Remember to refresh the page after enabling a Feature Preview. Many keyboard shortcuts are captured by the browser until the page reloads with the feature active.
</Callout>

Quick reference: common Feature Previews

| Feature           | What it does                                                         | How to use                                               |
| ----------------- | -------------------------------------------------------------------- | -------------------------------------------------------- |
| Slash commands    | Insert common Markdown structures quickly (e.g., tables)             | Type `/` in an editor and choose a command               |
| Colorblind themes | Provides accessible light/dark themes for various color vision types | Toggle in Feature preview > choose theme, then refresh   |
| Command Palette   | Keyboard-driven navigation and search across repos, issues, PRs      | Enable in Feature preview → refresh → `Ctrl+K` / `Cmd+K` |

Resources and further reading:

* [GitHub Docs](https://docs.github.com/) — official documentation and guides for account settings and feature previews.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/8933863d-4b81-4c80-90af-2f28f8519020/lesson/f2290f86-b8e6-44f2-ac5f-42ba8d9ccee3" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/8933863d-4b81-4c80-90af-2f28f8519020/lesson/e4fbe9ad-259c-435c-b16f-15bdf5b8b90f" />
</CardGroup>
