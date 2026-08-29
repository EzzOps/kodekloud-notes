# Linking Activity Within a Pull Request

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Linking-Activity-Within-a-Pull-Request/page

Guide to GitHub autolinking methods for referencing issues, pull requests, and commits, explaining formats, examples, and best practices for readable, clickable cross-references.

Cross-linking within a GitHub repository creates an automated trail of context, making it easy to track how issues, pull requests, and commits relate to one another. This guide summarizes the common reference formats GitHub recognizes so your discussions remain concise, clickable, and easy to navigate.

## Issue and pull request references

GitHub recognizes multiple ways to reference issues and pull requests. Each becomes a clickable link and is tracked by GitHub across conversations, timelines, and the network graph.

Common reference formats:

* Direct URL — paste the full issue/PR web address; the UI displays a shortened, clickable representation.
* Shorthand ID — type `#` followed by the issue/PR number (e.g., `#42`) for references within the same repository.
* Legacy/alternate — some tooling or older docs may use the `GH-` prefix (e.g., `GH-42`).
* Cross-repository — reference an item in another repository with `owner/repository#number` (e.g., `octocat/Hello-World#42`).

| Reference style      |                                   When to use | Example                                              |
| -------------------- | --------------------------------------------: | ---------------------------------------------------- |
| Shorthand ID         |               Most common for same-repo links | `#1347`                                              |
| Cross-repo reference |                   Linking across repositories | `octocat/Hello-World#1347`                           |
| Direct URL           | When copying from browser or external systems | `https://github.com/octocat/Hello-World/issues/1347` |
| Legacy format        |         Encountered in older tools or exports | `GH-1347`                                            |

<Frame>
  <img alt="The image is a table explaining different methods for cross-linking issues and pull requests on GitHub, including direct URLs, standard IDs, legacy formats, and cross-repository links, along with when to use each method." />
</Frame>

Examples

```text theme={null}
