# Create a lightweight tag pointing to HEAD
git tag v2.0

# Create an annotated tag with a message
git tag -a v2.1 -m "Release 2.1: Added performance improvements"
```

## Listing all tags

```bash theme={null}
# Display all tags sorted alphabetically
git tag
```

## Pushing tags to remote

```bash theme={null}
# Push a specific tag to origin
git push origin v2.0

# Push all local tags at once
git push origin --tags
```

> **triangle-alert** Avoid force-pushing or rewriting existing tags, as this can lead to inconsistencies in collaborators’ repositories.

## Checking out a tag

To view or revert to a tagged commit:

```bash theme={null}
git checkout v2.0
```

This puts your working directory in “detached HEAD” state. To make changes, create a new branch:

```bash theme={null}
git checkout -b hotfix/v2.0-patch
```

## Sorting tags by semantic version

```bash theme={null}
git tag --sort=v:refname
```

This ensures `v1.10` appears after `v1.2`.

## Integrating Git tags with Azure Repos

Tags pushed to Azure Repos can trigger build and release pipelines. For step-by-step guidance, see [Git version control in Azure Repos][azure-repos-git-tags].

***

## Links and References

* [Git Tagging Documentation][git-tags]
* [Git Basics: Tagging][git-tags]
* [Version control with Git in Azure Repos][azure-repos-git-tags]

[git-tags]: https://git-scm.com/book/en/v2/Git-Basics-Tagging

[azure-repos-git-tags]: https://docs.microsoft.com/azure/devops/repos/git/version-control-overview

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/aa5cc79d-807b-457a-902b-b6d82983b569)


# Introduction to managing repositories

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Introduction-to-managing-repositories/page

Learn to manage large Git repositories efficiently, addressing performance issues and collaboration challenges with best practices and advanced tools.

Managing a growing codebase or handling hefty assets can introduce performance bottlenecks and collaboration headaches. In this guide, you’ll learn how to keep your repositories fast, efficient, and well-organized using Git and Azure DevOps.

## Why Large Repositories Matter

As your project scales, you may encounter:

* Sluggish clone, fetch, and checkout commands
* Increased storage costs and longer backups
* CI/CD pipeline slowdowns
* Difficulty reviewing and merging pull requests

## What You’ll Discover

* Typical pain points in large-repo workflows
* Key techniques for optimizing history and assets
* Advanced tools like Git LFS and repository splitting
* Best practices for Git tags and branch organization
* Strategies for data purging and commit recovery

Let’s dive into the challenges and solutions that will keep your large repositories under control!

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/d2868faa-0eb6-4ba1-8bbc-9ffe4f33e508)
