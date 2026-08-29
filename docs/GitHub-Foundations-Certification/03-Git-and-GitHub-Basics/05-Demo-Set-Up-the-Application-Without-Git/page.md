# switch to main
$ git checkout main
Switched to branch 'main'

# merge the changes from exploring-coloring into main
$ git merge exploring-coloring -m "merging new color and lives"
Updating 4b0f8f3..6deef81
Fast-forward
 script.js | 2 ++
 style.css | 2 ++
 2 files changed, 4 insertions(+), 0 deletions(-)
```

After this fast-forward merge, `main` now includes the updates from `exploring-coloring` (player starts with 5 lives and the styling changes). Run the app from `main` to verify the UI and behavior.

Quick reference: common git merge commands

| Command                           | Purpose                                         |
| --------------------------------- | ----------------------------------------------- |
| `git checkout main`               | Switch to the target branch before merging      |
| `git merge <source>`              | Merge `<source>` branch into the current branch |
| `git log --all --graph --oneline` | View a compact, graph-style commit history      |
| `git branch --delete <branch>`    | Delete a local branch once merged               |

Inspecting commit history
Use a compact graph log to confirm branches were combined and to visualize commit pointers.

Example:

```bash theme={null}
$ git log --all --graph --oneline
* 6deef81 (HEAD -> main, exploring-coloring) updated color and lives
* 4b0f8f3 updated the main heading
* 5b5781a fixed a typo
* 4374c54 initial commit
```

In this example both `main` and `exploring-coloring` point to the same latest commit after the fast-forward.

Deleting the feature branch locally
If you no longer need the feature branch locally, delete it to keep your branch list tidy.

Example:

```bash theme={null}
$ git branch --delete exploring-coloring
Deleted branch exploring-coloring (was 6deef81).
```

Final history after deletion:

```bash theme={null}
$ git log --all --graph --oneline
* 6deef81 (HEAD -> main) updated color and lives
* 4b0f8f3 updated the main heading
* 5b5781a fixed a typo
* 4374c54 initial commit
```

<Callout icon="lightbulb">
  Fast-forward merges are simple and clean: Git advances the target branch pointer when there are no divergent commits. If your branches have diverged, Git will create a merge commit. Teams often choose between merge commits and rebasing based on their preferred history style—pick the workflow that matches your team's collaboration model.
</Callout>

Summary

* Local merging: `git checkout <target>` then `git merge <source>`.
* Fast-forward merges move the branch pointer without creating a merge commit.
* Always verify the merge by opening files, running the app, and inspecting the log.
* Clean up local feature branches with `git branch --delete <branch>` when they're no longer needed.

Related resources

* [Git merge documentation](https://git-scm.com/docs/git-merge)
* [Git branching basics](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
* [GitHub Pull Requests overview](https://docs.github.com/en/pull-requests)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/9fafcba5-3094-4afc-8837-5e2f1927739d" />
</CardGroup>


# Demo Set Up the Application Without Git

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Demo-Set-Up-the-Application-Without-Git/page

Demonstrates running the Block Buster game locally without Git, shows effects of a missing script.js file, and explains how Git can recover deleted files.

This guide walks through running the Block Buster game locally without Git and demonstrates what happens when a required file is missing. You’ll see how the browser reports missing assets and why Git is useful as a safety net to recover deleted files.

Environment used for this demo

* Editor: Visual Studio Code
* OS: Ubuntu (virtual machine)
* Project folder: `block-buster`

Project contents

* `index.html` — the HTML entry point
* `style.css` — styling for the game
* `script.js` — JavaScript logic (keyboard handlers, game setup)
* `README.md` — project notes and instructions

Small excerpt from `script.js` (keyboard handlers and initial setup):

```javascript theme={null}
document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') keyboard.left = false;
    if (e.key === 'ArrowRight') keyboard.right = false;
});

// ==== INITIAL SETUP ====
document.getElementById('welcomeHighScore').textContent = gameState.highScore;
```

From a shell inside the project directory you can confirm the location and files:

```bash theme={null}
