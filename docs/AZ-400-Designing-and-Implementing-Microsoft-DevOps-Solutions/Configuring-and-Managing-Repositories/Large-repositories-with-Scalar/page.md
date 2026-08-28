# Large repositories with Scalar

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Large-repositories-with-Scalar/page

This guide explores challenges of large Git repositories and presents strategies to optimize performance using Scalar and Git extensions.

When a Git repository grows to tens or hundreds of gigabytes—especially with binary assets like images, audio, or video—standard Git operations (clone, fetch, checkout) can become painfully slow. In this guide, we’ll explore the core challenges of large repositories and present seven practical strategies to accelerate your workflows using Scalar, Git extensions, and repository layout techniques.

## Challenges in Managing Large Repositories

Large repos combine deep commit histories with sizable binary files, which leads to:

* Slow `git clone` and `git fetch`
* Long checkout times
* Increased local disk usage
* Stale objects and packfiles

<Frame>
  ![The image illustrates challenges in managing large code repositories, highlighting extensive commit histories and the presence of large binary files.](https://kodekloud.com/kk-media/image/upload/v1752867509/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/code-repository-management-challenges.jpg)
</Frame>

***

## 1. Shallow Cloning

A **shallow clone** limits the commit history you download, drastically reducing clone time and disk usage.

```bash theme={null}
git clone --depth <number-of-commits> <repository-url>
```

Replace `<number-of-commits>` with the number of recent commits you need.

<Callout icon="lightbulb">
  Shallow clones omit older history, so `git log --follow` and certain bisecting operations may not work as expected.
</Callout>

<Frame>
  ![The image illustrates a concept of optimizing history in large repositories, showing folders labeled "Code" and "Clone" connected to a large repository icon. It suggests using shallow cloning to speed up cloning time.](https://kodekloud.com/kk-media/image/upload/v1752867510/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/optimizing-history-large-repositories-diagram.jpg)
</Frame>

***

## 2. Git Large File Storage (LFS)

**Git LFS** offloads large binary files to a remote LFS server while storing lightweight text pointers in your repo’s history.

```bash theme={null}
git lfs install
git lfs track "*.psd"
git add .gitattributes
git commit -m "Track design files with Git LFS"
```

<Callout icon="triangle-alert">
  Git LFS can incur additional bandwidth and storage costs on hosted services. Check your LFS quota before adopting large-scale storage.
</Callout>

<Frame>
  ![The image illustrates Git Large File Storage (LFS), showing how it replaces large files like audio, video, and graphics with text pointers in Git, while storing the actual files on a remote server.](https://kodekloud.com/kk-media/image/upload/v1752867512/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/git-lfs-large-file-storage-diagram.jpg)
</Frame>

***

## 3. Alternative: Git-Fat

**Git-Fat** is a lightweight alternative to LFS that stores large assets in a separate backend (e.g., S3, your own server) and keeps only references in Git.

```bash theme={null}
git clone https://github.com/jedbrown/git-fat.git
git-fat init
git-fat track "*.zip"
git add .gitfat
git commit -m "Enable Git-Fat for large archives"
```

<Frame>
  ![The image is an infographic about "Git-Fat," illustrating how it helps manage large files like audio, video, and graphics in Git repositories to reduce size.](https://kodekloud.com/kk-media/image/upload/v1752867513/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/git-fat-large-files-infographic.jpg)
</Frame>

***

## 4. Cross-Repository Sharing

Extract common libraries or components into a shared repo or package registry to **avoid duplication** across multiple projects.

* Create a `common-ui` or `shared-utils` repository
* Publish versions to npm, PyPI, or a private registry
* Reference in other repos as a dependency

<Frame>
  ![The image illustrates cross-repository sharing, showing two repositories (A and B) connected by shared code and components. It emphasizes reducing duplication and improving maintainability.](https://kodekloud.com/kk-media/image/upload/v1752867513/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/cross-repository-sharing-code-components.jpg)
</Frame>

***

## 5. Sparse Checkout

**Sparse checkout** lets you clone the full repo, but check out only specific directories or files to your working tree.

```bash theme={null}
git clone --no-checkout <repository-url>
cd <repo>
git sparse-checkout init --cone
git sparse-checkout set src/docs/
git checkout main
```

<Frame>
  ![The image illustrates the concept of sparse-checkout, showing a diagram with "Repository A" and "Repository B" as subsets of "Large Repositories," emphasizing checking out only needed files.](https://kodekloud.com/kk-media/image/upload/v1752867514/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/sparse-checkout-repositories-diagram.jpg)
</Frame>

***

## 6. Partial Clone

A **partial clone** defers downloading large Git objects until they’re actually needed, reducing initial clone size.

```bash theme={null}
git clone --filter=blob:none --no-checkout <repository-url>
cd <repo>
git checkout main
```

<Frame>
  ![The image is a flowchart illustrating the process of a partial clone in Git. It shows the steps from initializing a Git repository to deciding whether to enable a partial clone, leading to downloading either necessary or all Git objects.](https://kodekloud.com/kk-media/image/upload/v1752867515/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/git-partial-clone-flowchart-illustration.jpg)
</Frame>

***

## 7. Background Prefetch

Enable **background prefetch** to automatically download Git objects from remotes (e.g., hourly), so `git fetch` runs almost instantly.

```bash theme={null}
git config --global scalar.foregroundPrefetch false
scalar clone <repository-url>
```

<Frame>
  ![The image is an infographic titled "Background Prefetch," illustrating a feature that downloads Git object data from large repositories every hour to reduce time for foreground Git fetch calls.](https://kodekloud.com/kk-media/image/upload/v1752867516/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Large-repositories-with-Scalar/background-prefetch-git-object-infographic.jpg)
</Frame>

***

## Strategy Overview

| Strategy                 | Use Case                                               | Example Command                              |
| ------------------------ | ------------------------------------------------------ | -------------------------------------------- |
| Shallow Clone            | Speed up clones with limited history                   | `git clone --depth 10 https://...`           |
| Git LFS                  | Manage large binaries (audio, video, graphics)         | `git lfs track "*.mp4"`                      |
| Git-Fat                  | Alternative external storage for large assets          | `git-fat init`                               |
| Cross-Repository Sharing | Reuse shared code across multiple projects             | Publish to npm/PyPI or `git submodule`       |
| Sparse Checkout          | Check out only needed directories                      | `git sparse-checkout set docs/`              |
| Partial Clone            | Delay blob downloads until required                    | `git clone --filter=blob:none`               |
| Background Prefetch      | Automate object prefetch to speed up interactive fetch | `git config scalar.foregroundPrefetch false` |

***

## Links and References

* [Git Large File Storage (LFS) Documentation](https://git-lfs.github.com/)
* [Git-Fat GitHub Repository](https://github.com/jedbrown/git-fat)
* [Sparse Checkout Guide](https://git-scm.com/docs/git-sparse-checkout)
* [Partial Clone and Fetch](https://git-scm.com/docs/partial-clone)
* [Scalar: Accelerate Monorepos](https://github.com/microsoft/scalar)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/59a97bb6-e107-4be5-aada-3bcf9b44d396" />
</CardGroup>
