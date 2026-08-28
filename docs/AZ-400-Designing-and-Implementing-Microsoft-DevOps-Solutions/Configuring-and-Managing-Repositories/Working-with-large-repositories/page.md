# Working with large repositories

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Working-with-large-repositories/page

This guide explores strategies and tools to optimize workflow in large Git repositories, addressing challenges like slow operations and managing large files.

As projects evolve, repositories often accumulate extensive commit histories and hefty binary assets. These factors can slow down everyday Git operations like `clone`, `fetch`, and `checkout`. This guide explores strategies and tools to keep your workflow snappy—even in very large repositories.

## Challenges in Large Repositories

Long histories, numerous branches, and large binaries contribute to degraded performance. Cloning or fetching a repo with hundreds of megabytes (or gigabytes) of data can take minutes or even hours.

<Frame>
  ![The image illustrates challenges in managing large code repositories, highlighting extensive commit histories and the presence of large binary files.](https://kodekloud.com/kk-media/image/upload/v1752867525/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/code-repository-management-challenges.jpg)
</Frame>

## Optimize Clone Time with a Shallow Clone

A *shallow clone* downloads only the most recent commits and omits deep history:

```bash theme={null}
git clone --depth <number-of-commits> <repository-url>
```

Replace `<number-of-commits>` with how many commits you need (e.g., `1` for just the latest). This approach can reduce clone time and disk usage dramatically.

<Frame>
  ![The image illustrates a concept of optimizing history in large repositories, showing folders labeled "Code" and "Clone" connected to a large repository icon. It suggests using shallow cloning to speed up cloning time.](https://kodekloud.com/kk-media/image/upload/v1752867525/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/optimizing-history-large-repositories-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Shallow clones are ideal for read-only CI jobs or quick code reviews, but avoid them if you need full history for debugging or releases.
</Callout>

## Managing Large Files

Storing large binaries in Git can bloat your `.git` directory. Two popular tools help:

### Git Large File Storage (LFS)

Git LFS moves big assets—audio, video, datasets—to a separate server while keeping lightweight pointers in your repo:

```bash theme={null}
git lfs install
```

Then track files by pattern:

```bash theme={null}
git lfs track "*.psd"
git add .gitattributes
```

<Frame>
  ![The image illustrates Git Large File Storage (LFS), showing how it replaces large files like audio, video, and graphics with text pointers in Git, while storing the actual file contents on a remote server.](https://kodekloud.com/kk-media/image/upload/v1752867526/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/git-lfs-large-file-storage-diagram.jpg)
</Frame>

### Git-Fat

An alternative is **Git-Fat**, which also offloads large blobs and keeps pointer files in your Git history:

```bash theme={null}
git fat init
git fat track "*.zip"
```

<Frame>
  ![The image is an infographic about "Git-Fat," a tool for handling large files in Git repositories, showing how it manages audio, video, and graphics files to reduce repository size.](https://kodekloud.com/kk-media/image/upload/v1752867527/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/git-fat-large-files-infographic.jpg)
</Frame>

## Cross-Repository Sharing

To avoid duplicate code, share common libraries or components across projects. You can use Git submodules, subtrees, or a package manager.

| Method    | Description                                  | Example Command                                   |
| --------- | -------------------------------------------- | ------------------------------------------------- |
| Submodule | Embed another repo at a fixed path           | `git submodule add <repo-url> path/to/module`     |
| Subtree   | Merge external repo into a subdirectory      | `git subtree add --prefix=lib/my-lib <repo> main` |
| Package   | Publish and consume via npm, Maven, or NuGet | `npm install @myorg/my-lib`                       |

<Frame>
  ![The image illustrates cross-repository sharing, showing two repositories (A and B) connected by shared code and components to reduce duplication and improve maintainability.](https://kodekloud.com/kk-media/image/upload/v1752867530/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/cross-repository-sharing-code-components.jpg)
</Frame>

## Sparse Checkout for Partial Working Copies

If you only need a subset of files, *sparse checkout* lets you clone the full Git history but only check out selected paths:

```bash theme={null}
git clone <repository-url>
cd <repo-directory>
git sparse-checkout init --cone
git sparse-checkout set path/to/folder another/path
```

This keeps your working tree lean by populating only the directories you specify.

<Frame>
  ![The image illustrates the concept of sparse-checkout, showing a diagram with "Repository A" and "Repository B" connected to "Large Repositories," highlighting the ability to check out only a subset of a repository.](https://kodekloud.com/kk-media/image/upload/v1752867531/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/sparse-checkout-repositories-diagram.jpg)
</Frame>

## Partial Clone to Defer Large Object Downloads

A *partial clone* avoids downloading all blobs up front and fetches objects on demand:

```bash theme={null}
git clone --filter=blob:none <repository-url>
cd <repo-directory>
git sparse-checkout init --cone       # optional, to combine with sparse checkout
```

Git will automatically retrieve missing objects the first time you access them.

<Frame>
  ![The image is a flowchart illustrating the process of a partial clone in Git, showing steps to initialize a repository, enable partial clone, and download necessary or all Git objects based on the decision.](https://kodekloud.com/kk-media/image/upload/v1752867532/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/git-partial-clone-flowchart.jpg)
</Frame>

## Background Prefetch to Keep Objects Up to Date

Enable background prefetching so Git periodically pulls object data from remotes—reducing wait times during normal fetch operations:

```bash theme={null}
git config --global fetch.writeCommitGraph true
git config --global fetch.showForcedUpdates true
git config --global remote.origin.promisor true
git config --global core.commitGraph true
```

With these settings, Git maintains an up-to-date local object database that accelerates subsequent fetches.

<Frame>
  ![The image is an infographic titled "Background Prefetch," illustrating a process for downloading Git object data from large repositories every hour to reduce time for foreground Git fetch calls.](https://kodekloud.com/kk-media/image/upload/v1752867533/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Working-with-large-repositories/background-prefetch-git-object-infographic.jpg)
</Frame>

## Links and References

* [Git Documentation: Caching and cloning](https://git-scm.com/docs/git-clone)
* [Git LFS Official Site](https://git-lfs.github.com/)
* [Managing Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/51daa0af-ed43-4117-b0bb-458696c27319" />
</CardGroup>
