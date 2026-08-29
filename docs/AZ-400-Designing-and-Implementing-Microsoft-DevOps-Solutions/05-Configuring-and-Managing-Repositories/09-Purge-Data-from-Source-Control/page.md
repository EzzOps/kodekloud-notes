# Purge Data from Source Control

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Purge-Data-from-Source-Control/page

This guide explains purging data from Git repositories, its importance, tools for cleanup, and practical examples for maintaining a secure codebase.

Purging data from source control is essential for maintaining a clean, efficient, and secure codebase. In this guide, we’ll define purging in the context of Git repositories, explain why it matters, compare the top tools, and walk through hands-on examples.

## What Is Purging?

Purging a repository means removing unwanted or sensitive files from its commit history. This process helps you:

* Reclaim disk space
* Eliminate accidental commits
* Protect secrets from exposure

![The image shows a stack of documents with a magnifying glass, symbolizing examination or review. Below, there's text explaining "Purging" as the process of cleaning up a codebase by removing unnecessary or sensitive files.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867520/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Purge-Data-from-Source-Control/documents-magnifying-glass-purging-review.jpg)

## Why Purge Files?

By cleaning up your Git history, you can:

* **Optimize Performance:** Smaller repos clone and checkout faster.
* **Eliminate Mistakes:** Remove large or accidental commits.
* **Protect Secrets:** Expunge API keys, passwords, and other sensitive data.

![The image lists three reasons for purging files: shrinking repository size for performance, eliminating mistakenly committed large files, and removing files with sensitive information like passwords or API keys.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867521/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Purge-Data-from-Source-Control/purging-files-reasons-repository-size.jpg)

> **lightbulb** Always back up your repository before rewriting history. Purging is irreversible.

## Repository Cleanup Tools

Here’s a quick comparison of the two leading Git history-rewriting tools:

| Tool             | Use Case                                     | Documentation                                                  |
| ---------------- | -------------------------------------------- | -------------------------------------------------------------- |
| Git filter-repo  | Official, highly configurable, fine-grained  | [Git filter-repo](https://github.com/newren/git-filter-repo)   |
| BFG Repo-Cleaner | Fast, simple syntax for common cleanup tasks | [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) |

![The image lists two tools for repository cleanup: "Git filter-repo" and "BFG Repo-Cleaner," with brief descriptions of each.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867522/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Purge-Data-from-Source-Control/repository-cleanup-tools-git-bfg.jpg)

## Practical Examples

### 1. Deleting Large or Unwanted Files

Remove a file named `archive.tar.gz`:

```bash theme={null}
