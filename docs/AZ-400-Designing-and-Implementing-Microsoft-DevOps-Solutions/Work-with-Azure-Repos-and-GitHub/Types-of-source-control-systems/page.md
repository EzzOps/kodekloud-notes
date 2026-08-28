# Example: Import a TFVC branch into a new Git repo via Git-TFS
git tfs clone https://tfs-server:8080/tfs/DefaultCollection $/Project/Main --branches=all
```

<Callout icon="lightbulb">
  Start with a non-critical branch (e.g., development) to verify the process before importing protected or release branches.
</Callout>

<Frame>
  ![The image illustrates the process of transitioning from TFVC to Git, highlighting branch-level migration and showing an interface for importing a repository from TFVC.](https://kodekloud.com/kk-media/image/upload/v1752868155/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Transitioning-from-TFVC-to-Git/tfvc-to-git-migration-process-diagram.jpg)
</Frame>

Once the import is successful, repeat for each remaining branch until your entire TFVC repository resides in Git.

## Migration Scopes: Tip vs. Full History

Choose the right migration scope based on your needs:

| Strategy               | Description                                                                       | When to Use                           |
| ---------------------- | --------------------------------------------------------------------------------- | ------------------------------------- |
| Tip Migration          | Only the latest revision (“tip”) is moved to Git.                                 | Rapid cutover with minimal setup      |
| Full History Migration | Every TFVC changeset is converted into a Git commit, preserving complete history. | Full audit trail and compliance needs |

<Callout icon="triangle-alert">
  A **full-history migration** can take significantly longer and may require careful mapping of authors and commit dates. Plan for additional time and storage.
</Callout>

* Tip Migration: Keeps TFVC history archived on the original server for quick switch-over.
* Full History: Ensures end-to-end traceability by importing all historical changesets.

## Benefits of Moving to Git

Adopting Git from TFVC delivers several improvements in workflow and performance:

| Feature          | TFVC Model                      | Git Model                                     |
| ---------------- | ------------------------------- | --------------------------------------------- |
| History Tracking | Changesets stored centrally     | Filesystem snapshots, enabling flexible diffs |
| Branching        | Branches as folders             | Lightweight pointers, quick create/delete     |
| Collaboration    | Centralized checkout/lock model | Distributed clones for offline work           |

<Frame>
  ![The image outlines advantages of transitioning from TFVC to Git, highlighting streamlined migration and differences in branching methods.](https://kodekloud.com/kk-media/image/upload/v1752868156/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Transitioning-from-TFVC-to-Git/tfvc-to-git-advantages-migration-branching.jpg)
</Frame>

* **Distributed Workflow:** Team members can work independently and sync changes asynchronously.
* **Rich Ecosystem:** Leverage integrations with CI/CD pipelines, code review tools, and platform-agnostic hosting.

## Links and References

* [Azure DevOps: Import a TFVC repo into Git](https://learn.microsoft.com/en-us/azure/devops/repos/import/git-import?view=azure-devops)
* [Git-TFS on GitHub](https://github.com/git-tfs/git-tfs)
* [Git Documentation](https://git-scm.com/doc)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/11f92647-aa61-4572-85b2-a96b279268f5/lesson/56e54e6a-e97c-483d-9d98-b8bcc72c06cd" />
</CardGroup>


# Types of source control systems

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Work-with-Azure-Repos-and-GitHub/Types-of-source-control-systems/page

This article explores centralized and distributed source control systems, their architectures, advantages, and ideal use cases for project selection.

In this lesson, we’ll explore the two main models of source control: centralized and distributed. Understanding their architectures, advantages, and use cases will help you choose the right system for your projects.

***

## Centralized Source Control

In a centralized model, a single repository acts as the authoritative source for all code changes. Developers commit directly to this central hub.

<Frame>
  ![The image illustrates a concept of centralized source control with a server repository depicted as a cylinder.](https://kodekloud.com/kk-media/image/upload/v1752868158/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/centralized-source-control-server-repository.jpg)
</Frame>

### Examples of Centralized Systems

<Frame>
  ![The image lists examples of centralized source control systems: Team Foundation Version Control (TFVC), Concurrent Versions System (CVS), Apache Subversion (SVN), and Perforce Helix Core.](https://kodekloud.com/kk-media/image/upload/v1752868160/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/centralized-source-control-systems-examples.jpg)
</Frame>

Common advantages:

* **Scalability**: Handles large codebases efficiently.
* **Access Management**: Fine-grained permission controls.
* **Usage Oversight**: Tracks who made which changes and when.
* **Exclusive Control**: File locking prevents conflicting edits.

<Frame>
  ![The image outlines the advantages of centralized source control, highlighting scalability, access management, and usage oversight.](https://kodekloud.com/kk-media/image/upload/v1752868160/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/centralized-source-control-advantages-outline.jpg)
</Frame>

### When to Choose Centralized Control

* Large, monolithic codebases requiring consistent structure
* Projects needing detailed audit trails and permission scopes
* File types that are difficult to merge concurrently

***

## Distributed Source Control

Each developer has a full local copy of the repository, including its entire history. This architecture boosts autonomy, redundancy, and offline work.

<Frame>
  ![The image illustrates a distributed source control system, showing interactions between a central server repository and two systems (A and B) with pull, push, commit, and replace actions.](https://kodekloud.com/kk-media/image/upload/v1752868162/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/distributed-source-control-system-diagram.jpg)
</Frame>

The most popular distributed systems are Git and Mercurial:

<Frame>
  ![The image lists examples of distributed source control systems: Git and Mercurial.](https://kodekloud.com/kk-media/image/upload/v1752868162/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/distributed-source-control-systems-git-mercurial.jpg)
</Frame>

<Callout icon="lightbulb">
  You get full history access even when offline, making code reviews and commits possible without an internet connection.
</Callout>

**Key Strengths**:

* **Cross-Platform Flexibility**: Runs on Windows, macOS, and Linux.
* **Community-Driven Reviews**: Pull requests streamline collaboration.
* **Offline Functionality**: Full commit, diff, and log capabilities without network access.
* **Complete History in Every Clone**: Every contributor has a backup of the repository.
* **Wide Adoption**: The de facto choice for open-source development.

<Frame>
  ![The image lists the key strengths of distributed source control, including flexibility, community-centric development, offline functionality, history tracking, and growing popularity. Each strength is highlighted in a colorful box with an icon.](https://kodekloud.com/kk-media/image/upload/v1752868164/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/distributed-source-control-strengths-list.jpg)
</Frame>

### Ideal Use Cases for Distributed Control

* Modular or microservice-based codebases
* Open source projects with many external contributors
* Teams spread across different regions
* Cross-platform development environments

<Frame>
  ![The image outlines ideal applications for distributed source control, highlighting its efficiency for compact codebases, open-source projects, remote collaboration, and cross-platform development.](https://kodekloud.com/kk-media/image/upload/v1752868165/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/distributed-source-control-applications-outline.jpg)
</Frame>

***

## Git vs. Team Foundation Version Control (TFVC)

| Feature                | Git (Distributed)                                    | TFVC (Centralized)                                          |
| ---------------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| Repository Model       | Each developer has a full clone locally              | Single central repository; local workspace for latest code  |
| Offline Operations     | Full commit, branch, and history access at all times | Limited to local workspace edits; must check out changes    |
| Branching & Merging    | Lightweight branches, easy merges                    | Heavyweight branching, file locking for conflict prevention |
| Collaboration Workflow | Pull requests, forks, social coding                  | Check-in policies, gated check-ins                          |

<Frame>
  ![The image compares Git and Team Foundation Version Control, highlighting Git as a decentralized system and Team Foundation as a centralized framework.](https://kodekloud.com/kk-media/image/upload/v1752868166/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/git-vs-tfvc-comparison-decentralized-centralized.jpg)
</Frame>

***

## Reasons to Select Git for Source Control

1. **Feature Branching**\
   Isolate new features in dedicated branches before merging.

<Frame>
  ![The image lists reasons for selecting Git for source control, including branching for features, decentralized repositories, integration via pull requests, collaboration with the community, and feedback-driven releases. It also includes a diagram illustrating feature branching.](https://kodekloud.com/kk-media/image/upload/v1752868167/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/git-source-control-reasons-diagram.jpg)
</Frame>

2. **Full Autonomy**\
   Every developer holds a complete, self-contained repository.

<Frame>
  ![The image is a slide titled "Selecting Git for Source Control – Reasons," listing benefits such as decentralized repositories and collaboration, with a diagram illustrating full repositories.](https://kodekloud.com/kk-media/image/upload/v1752868169/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/selecting-git-source-control-benefits-diagram.jpg)
</Frame>

3. **Pull Requests & Code Reviews**\
   Built-in workflows for peer review, discussion, and approval.

<Frame>
  ![The image outlines reasons for selecting Git for source control, highlighting integration via pull requests with a diagram and brief explanations.](https://kodekloud.com/kk-media/image/upload/v1752868170/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/git-source-control-pull-requests-diagram.jpg)
</Frame>

4. **Community Collaboration**\
   Forks and pull requests simplify contributions from any developer.

<Frame>
  ![The image is a slide titled "Selecting Git for Source Control – Reasons," highlighting five reasons, with "Collaboration With the Community" emphasized. It includes a diagram and notes on Git's collaborative benefits.](https://kodekloud.com/kk-media/image/upload/v1752868172/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/selecting-git-source-control-reasons.jpg)
</Frame>

5. **Continuous Integration & Rapid Feedback**\
   Seamless integration with CI/CD pipelines for faster release cycles.

<Frame>
  ![The image outlines reasons for selecting Git for source control, including branching for features, decentralized repositories, integration via pull requests, collaboration with the community, and feedback-driven releases. It also highlights Git's role in enabling continuous integration and incorporating feedback into release cycles.](https://kodekloud.com/kk-media/image/upload/v1752868173/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/git-source-control-reasons-diagram-2.jpg)
</Frame>

***

## Common Objections to Using Git

* **History Rewrites**: Mistakes in rebasing or force-push can alter commit history.
* **Large File Management**: Git isn’t optimized for big binaries; consider [Git LFS](https://git-lfs.github.com/).
* **Steep Learning Curve**: New users may need training to master branching strategies.

<Callout icon="triangle-alert">
  Improper use of `git reset` or `git rebase` can rewrite shared history—coordinate closely with your team.
</Callout>

<Frame>
  ![The image lists three objections to using Git: history management, handling of voluminous files, and educational investment.](https://kodekloud.com/kk-media/image/upload/v1752868174/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Types-of-source-control-systems/git-objections-history-management-voluminous-files.jpg)
</Frame>

***

## Links and References

* [Git Documentation](https://git-scm.com/docs)
* [GitHub Guides](https://guides.github.com/)
* [Mercurial Official Site](https://www.mercurial-scm.org/)
* [Azure DevOps Repos](https://docs.microsoft.com/azure/devops/repos/)
* [Git Large File Storage (LFS)](https://git-lfs.github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/11f92647-aa61-4572-85b2-a96b279268f5/lesson/bd4f73b0-7e7a-4166-8a56-6b495b13d3e1" />
</CardGroup>
