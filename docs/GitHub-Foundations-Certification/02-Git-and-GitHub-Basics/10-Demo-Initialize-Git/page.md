# or the newer command:
git switch -c exploring-coloring
```

After switching, edits affect only `exploring-coloring` until you merge or rebase them into `main`.

Example branch listing after creation and checkout:

```bash theme={null}
git branch --list
* exploring-coloring
  main
```

## Example changes (style and gameplay)

Imagine you want to update UI colors and increase the number of lives in a browser game. Here are representative excerpts from `style.css` and `script.js` that show the changes you might make on the `exploring-coloring` branch.

Updated CSS variables (selective excerpt from `style.css`):

```css theme={null}
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --dark-bg: #0f0f1e;
  --card-bg: rgba(255, 255, 255, 0.1);
  --card-border: rgba(255, 255, 255, 0.2);
  --accent-cyan: #00ff51;   /* changed to a greenish tint */
  --accent-lime: #87d20a;
  --accent-purple: #c24cf6;
  --text-primary: #ffffff;
  --text-secondary: #b0b0c0;
  --power-multi: #f6b6b6;
  --power-paddle: #4ecdc4;
  --power-bullet: #ffd93d;
}
```

Representative game state in `script.js` (cleaned and corrected):

```javascript theme={null}
const gameState = {
  currentLevel: 1,
  score: 0,
  highScore: parseInt(localStorage.getItem('blockBusterHighScore'), 10) || 0,
  lives: 3,
  isPaused: false,
  isGameRunning: false,
  balls: [],
  particles: [],
  bullets: [],
  activePowerups: [],
  powerups: {
    multiBall: { active: false, activationTime: null },
    megaPaddle: { active: false, activationTime: null },
    bulletMode: { active: false, activationTime: null }
  },
  bulletFireCounter: 0
};

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
```

Update the `startGame` function so fresh games start with five lives:

```javascript theme={null}
function startGame() {
  gameState.currentLevel = 1;
  gameState.score = 0;
  gameState.lives = 5; // give players five lives on a fresh start
  gameState.activePowerups = [];
  gameState.isGameRunning = true;
  gameState.highScore = parseInt(localStorage.getItem('blockBusterHighScore'), 10) || 0;

  // Toggle screens (example IDs; adapt to your markup)
  document.getElementById('welcomeScreen').classList.add('hidden');
  document.getElementById('gameOverScreen').classList.add('hidden');
  document.getElementById('gameScreen').classList.remove('hidden');
}
```

Save these files while you are on `exploring-coloring` and test the app. You should see the updated color scheme and five starting lives.

## Staging and committing changes

Check your working tree:

```bash theme={null}
git status
```

Example output when two files changed:

```bash theme={null}
On branch exploring-coloring
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  modified:   script.js
  modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
```

Stage and commit your edits:

```bash theme={null}
git add script.js style.css
git commit -m "updated color and lives"
```

Example commit output:

```bash theme={null}
[exploring-coloring 6def81] updated color and lives
 2 files changed, 2 insertions(+), 2 deletions(-)
```

If you prefer a GUI, VS Code's Source Control view provides staging, diffing, and committing.

## Useful Git commands (quick reference)

| Action            | Command                                            | Notes                                                   |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------- |
| List branches     | `git branch --list`                                | Shows local branches; `git branch -a` lists remotes too |
| Create branch     | `git branch <name>`                                | Creates a branch pointer without switching              |
| Create and switch | `git checkout -b <name>` or `git switch -c <name>` | Convenience for create+checkout                         |
| Show status       | `git status`                                       | What’s changed and what’s staged                        |
| Stage files       | `git add <file>`                                   | Stage changes for the next commit                       |
| Commit            | `git commit -m "message"`                          | Records staged snapshot                                 |
| Show log          | `git log`                                          | See the commit history                                  |

## Inspecting history across branches

`git log` shows commits reachable from HEAD. These variations help visualize branch structure and history:

| Purpose                                          | Command                           | Example output notes                         |
| ------------------------------------------------ | --------------------------------- | -------------------------------------------- |
| Full log (current branch)                        | `git log`                         | All commits on the current branch            |
| All branches with graph                          | `git log --all --graph`           | ASCII graph showing divergence               |
| Compact, one-line per commit across all branches | `git log --all --graph --oneline` | Easier to see branching and `HEAD` positions |

Example compact output (actual hashes will differ):

```text theme={null}
* 6def81 (HEAD -> exploring-coloring) updated color and lives
* 5bb781 fixed a typo mistake
* 437c54 initial commit
```

The `--graph` and `--oneline` flags are especially helpful for visualizing how branches diverge and where `HEAD` currently points.

> **warning** Before merging, ensure you don't accidentally commit sensitive files (API keys, large binaries) and resolve any merge conflicts locally. Run your test suite or smoke tests after merging to confirm behavior.

## Merging back into main

When your changes are tested and ready:

1. Switch to `main`:
   ```bash theme={null}
   git checkout main
   # or:
   git switch main
   ```
2. Update `main` from the remote:
   ```bash theme={null}
   git pull origin main
   ```
3. Merge your feature branch:
   ```bash theme={null}
   git merge exploring-coloring
   ```
4. Resolve any conflicts, run tests, then push:
   ```bash theme={null}
   git push origin main
   ```

Alternatively, open a pull request in your Git hosting service (GitHub, GitLab, Bitbucket) to get peer review and automated CI checks before merging.

## Links and further reading

* Git branching basics: [https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
* `git` reference: [https://git-scm.com/docs](https://git-scm.com/docs)
* VS Code Source Control: [https://code.visualstudio.com/docs/editor/versioncontrol](https://code.visualstudio.com/docs/editor/versioncontrol)

***

By using a dedicated branch like `exploring-coloring`, you keep your experiments isolated from `main`, enabling safe iteration and easier collaboration. When ready, merge via PR or locally following your team's workflow.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/b6635e11-04b9-419a-a12a-13fd21c84c53)


# Demo Initialize Git

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Demo-Initialize-Git/page

Guide to initializing and using Git in a project, covering installation check, repository initialization, staging, committing, restoring files, viewing history, and configuring author identity.

In this lesson you'll initialize a Git repository inside the Blockbuster project folder to start tracking changes, enable easy rollbacks, and keep a clear project history.

What you'll learn:

* Verify Git is installed.
* Initialize a repository and inspect its status.
* Stage and commit files.
* Restore deleted files from history.
* Configure author identity for commits.

Prerequisites

* Git installed on your machine. Many Ubuntu distributions include Git by default.
* If you're unsure, verify with:

```bash theme={null}
git version
