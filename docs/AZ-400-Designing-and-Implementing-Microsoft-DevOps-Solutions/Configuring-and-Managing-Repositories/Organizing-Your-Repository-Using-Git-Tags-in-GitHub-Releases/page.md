# Organizing Your Repository Using Git Tags in GitHub Releases

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Organizing-Your-Repository-Using-Git-Tags-in-GitHub-Releases/page

This article explains how to use Git tags and GitHub Releases to organize and version your codebase effectively.

GitHub Releases provide official, versioned snapshots of your codebase. Each Release is backed by a Git tag, marking a precise point in your commit history. Leveraging Releases and tags helps you:

* Clearly identify versions (e.g., v1.0.0, v2.1.3)
* Distribute binaries and assets
* Publish detailed release notes and changelogs

<Frame>
  ![The image explains the concepts of releases and tags in GitHub, highlighting that releases are official snapshots tied to version numbers, based on Git tags, which help organize and track code changes.](https://kodekloud.com/kk-media/image/upload/v1752867519/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Organizing-Your-Repository-Using-Git-Tags-in-GitHub-Releases/github-releases-tags-concepts-explained.jpg)
</Frame>

## Prerequisites

* [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated (`gh auth login`).
* A Git repository with commits you want to release.

## 1. Creating a Release Tag with GitHub CLI

Use the `gh release create` command to generate a Git tag and corresponding GitHub Release.

Basic syntax:

```bash theme={null}
gh release create <tag-name>
```

Example:

```bash theme={null}
gh release create v1.0.0
```

This creates both the `v1.0.0` Git tag and the GitHub Release entry.

<Callout icon="lightbulb">
  If this is your first time using the GitHub CLI, run `gh auth login` to authenticate.
</Callout>

### 1.1 Adding a Title and Release Notes

To provide context, include a title and detailed notes:

```bash theme={null}
gh release create v1.0.0 \
  --title "Initial Release" \
  --notes "Features: user authentication, API endpoints, UI enhancements."
```

| Flag         | Description                             | Example                                       |
| ------------ | --------------------------------------- | --------------------------------------------- |
| --title      | Sets the release title                  | `--title "Initial Release"`                   |
| --notes      | Supplies the body of the release notes  | `--notes "Bug fixes and performance updates"` |
| --draft      | Marks the release as a draft            | `--draft`                                     |
| --prerelease | Designates the release as a pre-release | `--prerelease`                                |

<Callout icon="triangle-alert">
  Once a tag is published as a public Release, avoid rewriting or deleting it—immutable tags preserve release integrity.
</Callout>

## 2. Understanding Semantic Versioning

Semantic Versioning (SemVer) is a widely adopted specification for version numbers in the form MAJOR.MINOR.PATCH. It clarifies how version numbers change with each type of update:

| Version Segment | When to Increment                                     | Example Change |
| --------------- | ----------------------------------------------------- | -------------- |
| MAJOR           | Incompatible API changes                              | 1.0.0 → 2.0.0  |
| MINOR           | Backwards-compatible functionality additions          | 1.1.0 → 1.2.0  |
| PATCH           | Backwards-compatible bug fixes and performance tweaks | 1.0.0 → 1.0.1  |

<Callout icon="lightbulb">
  Refer to the [SemVer specification](https://semver.org/) for detailed guidelines on version numbering.
</Callout>

## 3. Links and References

* [GitHub CLI Manual: gh release create](https://cli.github.com/manual/gh_release_create)
* [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
* [Semantic Versioning 2.0.0](https://semver.org/)

## 4. Example Workflow

1. Commit your changes:
   ```bash theme={null}
   git add .
   git commit -m "Implement user login feature"
   ```
2. Create and push a new tag with Release:
   ```bash theme={null}
   gh release create v1.1.0 \
     --title "Login Feature Release" \
     --notes "Added OAuth2-based login, session management."
   ```
3. Verify on GitHub under **Releases** to confirm the entry and assets.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/fdd1a43e-a64f-4d0f-879a-7932deb75435" />
</CardGroup>
