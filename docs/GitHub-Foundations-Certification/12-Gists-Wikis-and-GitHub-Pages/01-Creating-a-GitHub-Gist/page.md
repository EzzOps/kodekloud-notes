# Creating a GitHub Gist

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Gists-Wikis-and-GitHub-Pages/Creating-a-GitHub-Gist/page

Explains GitHub Gists, how to create and use them, visibility options, cloning and embedding, use cases, and security and scope best practices.

What are GitHub Gists and how do we create them?

GitHub Gists are lightweight Git repositories designed for sharing single files or small collections of code, configuration, or documentation snippets. Unlike full repositories — which are optimized for multi-file projects, branches, CI/CD, and access controls — Gists provide a fast way to publish examples, diagnostics, or small utilities without the overhead of a full project structure.

<Frame>
  <img alt="The image provides an introduction to &#x22;Gists,&#x22; describing them as lightweight repositories for sharing small code snippets and showing a menu for creating a new gist." />
</Frame>

Key characteristics and visibility

Gists support two visibility options:

* Public gists: Indexed by search engines and discoverable via GitHub search. Use these for community sharing and open collaboration.
* Secret gists: Not indexed or shown on your public profile, but accessible to anyone with the direct URL — they are obscured, not private or encrypted. Treat secret gists as “link-shared” content.

<Frame>
  <img alt="The image explains the difference between creating public and secret gists, highlighting that secret gists are hidden from search engines but accessible via a link, while public gists are visible to everyone." />
</Frame>

Why use a Gist? Features and workflow

* Versioned by Git: Each save creates a new revision/commit. You can view history, compare diffs, and revert changes.
* Markdown support: Write documentation and include images and formatted text alongside code snippets.
* Embeddable: Insert a Gist into a blog or docs with a small JavaScript snippet so it always reflects the latest revision.
* Forkable: Use the Fork button to copy and extend another user’s Gist in your account.
* Cloneable: Treat a Gist as a mini-repo and work on it locally.

Example: clone a Gist locally with Git

```bash theme={null}
