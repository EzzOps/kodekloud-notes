# Code Review With a Codeowners File

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Code-Review-With-a-Codeowners-File/page

Explains GitHub CODEOWNERS files assigning ownership of files and directories to auto-request reviewers, pattern rules, placement options, and branch protection effects.

What is a CODEOWNERS file?

A `CODEOWNERS` file defines which people or teams are responsible for specific files, directories, or patterns within a GitHub repository. By assigning ownership, you ensure that changes touch the right subject matter experts and that required code reviews are requested automatically when those files change. This improves review quality, speeds up onboarding, and helps enforce governance through branch protection rules.

<Frame>
  <img alt="The image shows a directory structure of a project repository with CODEOWNER files in various folders, highlighting its purpose to define ownership and ensure proper code review." />
</Frame>

Where to put the CODEOWNERS file

GitHub recognizes a `CODEOWNERS` file when placed in any of these repository locations:

* The repository root
* The `.github/` folder
* The `docs/` directory

A typical repository layout with `CODEOWNERS` files might look like this:

```text theme={null}
my-project-repo/
├── .github/
│   └── CODEOWNERS
├── docs/
│   └── CODEOWNERS
├── src/
│   └── app.py
├── LICENSE
└── CODEOWNERS
```

Recommended locations and behaviors

|   Location | Purpose                          | Notes                                      |
| ---------: | -------------------------------- | ------------------------------------------ |
|       Root | Global rules for the repository  | Applied to most repos; easy to find        |
| `.github/` | Centralized repo configuration   | Useful for shared config across many repos |
|    `docs/` | Documentation-specific ownership | Scope ownership to docs-only changes       |

Assigning owners using patterns

`CODEOWNERS` uses pattern matching similar to `.gitignore`. Patterns can target extensions, filenames, or directories. Owners are GitHub users or teams in the form `@username` or `@org/team`.

Examples:

```text theme={null}
