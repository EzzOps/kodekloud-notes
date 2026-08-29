# Example output:
# git version 2.34.0
```

If Git is missing or you want to upgrade, visit [https://git-scm.com](https://git-scm.com) for installers or use your platform package manager. Common install commands:

```bash theme={null}
# Debian/Ubuntu
sudo apt-get install git
# Or via the official Git PPA
sudo add-apt-repository ppa:git-core/ppa
sudo apt update && sudo apt install git

# RHEL/CentOS / Fedora
sudo yum install git        # older Fedora / CentOS
sudo dnf install git        # newer Fedora

# Gentoo
sudo emerge --ask --verbose dev-vcs/git

# Arch
sudo pacman -S git
```

Initialize a repository

1. Change into your project directory (for example, the `Blockbuster` folder).
2. Before initialization you should not see a `.git` directory:

```bash theme={null}
ls -a
# Example output:
# .  ..  README.md  index.html  script.js  style.css
```

3. Initialize the repository:

```bash theme={null}
git init
# Example output:
# Initialized empty Git repository in /path/to/Blockbuster/.git/
```

4. Confirm the `.git` directory exists:

```bash theme={null}
ls -a
# Example output:
# .  ..  .git  README.md  index.html  script.js  style.css
```

Check repository status
After initialization, check the repo status to see which files are untracked:

```bash theme={null}
git status
# Example output:
# On branch main
#
# No commits yet
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#         README.md
#         index.html
#         script.js
#         style.css
#
# nothing added to commit but untracked files present (use "git add" to track)
```

Stage files for commit
You can stage individual files or stage all current files. To stage everything in the directory:

```bash theme={null}
git add .
git status
# Example output:
# On branch main
#
# No commits yet
#
# Changes to be committed:
#   (use "git rm --cached <file>..." to unstage)
#         new file:   README.md
#         new file:   index.html
#         new file:   script.js
#         new file:   style.css
```

Commit staged files
Create the initial commit with a descriptive message:

```bash theme={null}
git commit -m "initial commit"
# Example output:
# [main (root-commit) 4374c54] initial commit
#  4 files changed, 1472 insertions(+)
#  create mode 100644 README.md
#  create mode 100644 index.html
#  create mode 100644 script.js
#  create mode 100644 style.css
```

Verify a clean working tree:

```bash theme={null}
git status
# On branch main
# nothing to commit, working tree clean
```

Restore deleted files from history
Git can restore files removed from the working tree if they existed in the last commit.

```bash theme={null}
# Delete the file
rm script.js
ls
# Example output:
# Check status after deletion
git status
# Example output:
# On branch main
# Changes not staged for commit:
#   (use "git add/rm <file>..." to update what will be committed)
#   (use "git restore <file>..." to discard changes in working directory)
#         deleted:    script.js
#
# Restore the file from the last commit
git restore script.js

# Verify the working tree is clean again
git status
# On branch main
# nothing to commit, working tree clean
```

Make a small change and commit
Edit `README.md` (for example, fix a typo), then stage and commit the change:

```bash theme={null}
git status
# On branch main
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git restore <file>..." to discard changes in working directory)
git add README.md
git commit -m "fixed a typo mistake"
# Example output:
# [main 5bb781a] fixed a typo mistake
#  1 file changed, 1 insertion(+), 1 deletion(-)
```

Inspect commit history
View the commit log to see past commits, authorship, and timestamps:

```bash theme={null}
git log
# Example output:
# commit 5bb781a27c4de1ab63cc6d5966866dfe40e (HEAD -> main)
# Author: admin <admin@local.com>
# Date:   Sun Apr 26 17:14:04 2026 +0000
#
#     fixed a typo mistake
#
# commit 437c45f4e553e10e09a57f2235fa3961c610
# Author: admin <admin@local.com>
# Date:   Sun Apr 26 17:11:49 2026 +0000
#
#     initial commit
```

Configure author identity
Git records the author for every commit using `user.name` and `user.email`. You can set these globally (applies to all repositories for your user) or locally (only for the current repository).

Set a global identity:

```bash theme={null}
git config --global user.email "siddharth@sid.com"
git config --global user.name "Siddharth"
```

Or set them only for the current repository:

```bash theme={null}
git config user.email "siddharth@sid.com"
git config user.name "Siddharth"
```

After updating the config, make another commit and verify the author fields:

```bash theme={null}
git add README.md
git commit -m "updated the main heading"
git log
# Example output:
# commit 4b0f8f3dbf90d36d464cabf874a321646eadc13 (HEAD -> main)
# Author: Siddharth <siddharth@sid.com>
# Date:   Sun Apr 26 17:16:25 2026 +0000
#
#     updated the main heading
#
# commit 5bb781a27c4de1ab63cc6d5966866dfe40e
# Author: admin <admin@local.com>
# Date:   Sun Apr 26 17:14:04 2026 +0000
#
#     fixed a typo mistake
#
# commit 437c45f4e553e10e09a57f2235fa3961c610
# Author: admin <admin@local.com>
# Date:   Sun Apr 26 17:11:49 2026 +0000
#
#     initial commit
```

> **lightbulb** If you are working on a shared machine or with multiple identities, prefer using `git config --local` (inside the repo) to avoid changing your global settings. You can always override per-repository with the local config.

Quick reference — common Git commands

| Task                          | Command                                            |
| ----------------------------- | -------------------------------------------------- |
| Check Git version             | `git version`                                      |
| Initialize repo               | `git init`                                         |
| Show status                   | `git status`                                       |
| Stage all files               | `git add .`                                        |
| Stage a file                  | `git add README.md`                                |
| Commit staged changes         | `git commit -m "message"`                          |
| Restore file from last commit | `git restore <file>`                               |
| View commit history           | `git log`                                          |
| Set global user email         | `git config --global user.email "you@example.com"` |
| Set local user name           | `git config user.name "Your Name"`                 |

Links and references

* Official Git: [https://git-scm.com](https://git-scm.com)
* Git documentation: [https://git-scm.com/doc](https://git-scm.com/doc)
* Git config documentation: [https://git-scm.com/docs/git-config](https://git-scm.com/docs/git-config)

This completes the basic Git initialization workflow: verify/install Git, initialize the repository, stage and commit files, restore files from history, and configure author identity.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/a31cba95-cbe1-4294-b31f-3cc8cc277e0b)


# Demo Local Branch Merge

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Demo-Local-Branch-Merge/page

Guide showing how to perform and verify a fast-forward local Git merge, inspect history, and clean up feature branches

Merging combines changes from one Git branch into another so you can integrate separate work into a single codebase. This guide shows a simple local merge workflow (fast-forward example), how to inspect history afterward, and how to clean up the feature branch.

Scenario

* Branch `exploring-coloring`: player starts with 5 lives and UI color changed to green.
* Branch `main`: player starts with 3 lives and original colors remain.

Below are the relevant file excerpts before merging.

script.js on main (shows 3 lives):

```javascript theme={null}
function startGame() {
    gameState.currentLevel = 1;
    gameState.score = 0;
    gameState.lives = 3;
    gameState.activePowerups = [];
    gameState.highScore = localStorage.getItem('blockBusterHighScore') || 0;

    document.getElementById('welcomeScreen').classList.remove('active');
    document.getElementById('gameOverScreen').classList.remove('active');
    document.getElementById('gameScreen').classList.add('active');

    document.getElementById('levelBadge').textContent = 'LEVEL 1';
    updateUI();
}
```

script.js on exploring-coloring (shows 5 lives and a few UI tweaks):

```javascript theme={null}
function startGame() {
    gameState.currentLevel = 1;
    gameState.score = 0;
    gameState.lives = 5;
    gameState.activePowerups = [];
    gameState.highScore = localStorage.getItem('blockBusterHighScore') || 0;

    document.getElementById('welcomeScreen').classList.add('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');

    document.getElementById('levelBadge').textContent = 'LEVEL 1';
    updateUI();
    init();
    draw();
}

function nextLevel() {
    gameState.currentLevel++;
}
```

When to expect a fast-forward merge
A fast-forward merge happens when the target branch (e.g., `main`) has no new commits since the source branch diverged. In that case Git simply moves the `main` pointer forward so it points to the same commit as the source branch. If both branches have unique commits, Git creates a merge commit unless you rebase first.

Performing a local merge (fast-forward example)

1. Checkout the target branch you want to merge into (usually `main`).
2. Merge the source branch into it.

Example commands and output:

```bash theme={null}
