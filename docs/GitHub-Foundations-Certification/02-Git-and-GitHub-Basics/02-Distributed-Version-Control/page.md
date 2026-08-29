# show current directory
pwd
/home/batman/block-buster

# list files in the project
ls
README.md  index.html  script.js  style.css
```

How to run the app locally

* Open the project in VS Code.
* Use the Live Server extension (or Show Preview) to open `index.html` in a browser or the editor preview.
* The game is a classic brick-breaker: control a paddle, bounce the ball, destroy bricks, progress through levels and power-ups.

<Frame>
  <img alt="The image shows a screenshot of a video game called &#x22;Block Buster,&#x22; displaying a play area with multicolored blocks and game stats such as score, level, and lives." />
</Frame>

What happens if `script.js` is missing
Imagine `script.js` was accidentally removed (by a cleanup script or manual error). When you refresh the preview or browser, the page will fail to run because the browser cannot load the missing JavaScript file.

Open Developer Tools → Network (or Console) to inspect resource loading. You will see a 404 error for the missing `script.js`:

<Frame>
  <img alt="The image shows a browser window with a developer tools network activity panel open at the bottom, displaying data about various resource requests, and a title &#x22;BLOCK BUSTER&#x22; at the top." />
</Frame>

Typical console/network error:

```text theme={null}
GET http://localhost:3000/script.js net::ERR_ABORTED 404 (Not Found)
WebSocket connection to 'ws://127.0.0.1:3000/02441247d92323efa697b17597644feb273ad' failed:
```

Consequences

* The game UI may load, but interactive features provided by `script.js` will not work.
* Without the JS, keyboard handlers, game initialization, and other features are unavailable — rendering the game unusable.
* Manually reconstructing deleted files is time-consuming and error-prone, especially for larger projects.

> **warning** If you don’t have a backup of `script.js`, restoring the exact logic and state can be difficult. Browser errors like `404` and `net::ERR_ABORTED` indicate a missing or incorrectly referenced asset.

Why use Git here
Git provides a versioned safety net so you can:

* Recover deleted or modified files (for example, `git restore <file>`).
* Revert to previous commits or branches when something breaks.
* Track changes and collaborate without losing history.

Quick reference — common Git recovery commands

| Use case                                      | Command example                           |
| --------------------------------------------- | ----------------------------------------- |
| Initialize a repo                             | `git init`                                |
| Stage files                                   | `git add .`                               |
| Commit changes                                | `git commit -m "Initial commit"`          |
| Restore a deleted file from the latest commit | `git restore --source=HEAD -- script.js`  |
| Restore a file from a specific commit         | `git checkout <commit-hash> -- script.js` |

Next steps

* Install Git (if not present): [Git Downloads](https://git-scm.com/downloads)
* Initialize the repository inside `block-buster`: `git init`
* Add and commit the current project state so files like `script.js` can be restored later

> **lightbulb** Using Git early in a project prevents accidental data loss and makes recovery straightforward. See the [official Git documentation](https://git-scm.com/doc) for detailed guidance on installation and common workflows.

References

* [Git Documentation](https://git-scm.com/doc)
* Live Server extension for VS Code — search the VS Code marketplace for "Live Server" to install and run previews locally.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/bd8694bc-317c-4ad2-908c-2fa45744aab2)


# Distributed Version Control

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Distributed-Version-Control/page

Explains differences between centralized and distributed version control, highlights Git’s distributed advantages for offline work, redundancy, and team collaboration with remotes like GitHub

This page compares distributed and centralized version control systems and explains why Git’s distributed design changed how teams collaborate.

Legacy centralized systems such as [CVS](https://en.wikipedia.org/wiki/Concurrent_Versions_System), [Subversion](https://subversion.apache.org/), and [Perforce](https://www.perforce.com/) rely on a single central server that stores the entire project history. That central server is a single point of failure: if it goes down, developers can be blocked and the project history can become difficult to recover.

<Frame>
  <img alt="The image compares Central Version Control Systems (CVS, SVN, Perforce) and Distributed Version Control System (Git), illustrating their workflows with repositories and working copies." />
</Frame>

Git is a distributed version control system: every developer’s clone contains a full, independent copy of the repository — including the entire commit history. That architecture provides several practical advantages for both solo and team workflows:

* Work offline: you can commit locally without network access, keeping incremental history on your machine.
* Reduced coupling to remotes: network connectivity is required only when exchanging changes with a remote (for example, `push`, `fetch`, or `pull`).
* Redundancy and recovery: any clone with the required history can act as a backup of the project, reducing the risk of total data loss (note: shallow clones that omit older commits are an exception).

Common Git operations you’ll use when collaborating with remotes:

```bash theme={null}
