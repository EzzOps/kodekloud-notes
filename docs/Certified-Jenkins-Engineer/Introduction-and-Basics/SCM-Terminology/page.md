# Clone a repository
git clone https://github.com/example/repo.git 

# Create and switch to a new branch
git checkout -b feature/new-endpoint 

# Add files to staging area
git add . 

# Commit changes with a message
git commit -m "Add new endpoint for user data" 

# Push branch to remote
git push origin feature/new-endpoint
```

## Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Git Documentation](https://git-scm.com/doc)
* [GitHub Guides](https://guides.github.com/)
* [Terraform Registry](https://registry.terraform.io/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2e8ea9bb-e5bb-428e-85d9-89f2eb816adb/lesson/ed0284be-2a62-429b-acb0-3d2ffbd53e23" />
</CardGroup>


# SCM Terminology

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Introduction-and-Basics/SCM-Terminology/page

This article covers Source Control Management terminology and best practices for using Git in Jenkins CI/CD pipelines.

Effective Source Control Management (SCM) is the foundation of reliable CI/CD pipelines in Jenkins. By storing your application code in a versioned repository—commonly referred to as a **repo**—you gain access to branching, change history, and granular permissions that enhance collaboration and security.

Best practices for repository organization:

* Maintain one repository per product or microservice
* Assign **read**, **write**, or **admin** roles to teams or individuals
* Protect the main branch with branch protection rules in your SCM

## Standard Git Workflow

A consistent workflow ensures that developers can work in parallel without destabilizing the main codebase. Below is a step-by-step guide using Git commands:

1. Clone the repository
   ```bash theme={null}
   git clone https://github.com/your-org/your-repo.git
   ```
2. Create a feature branch
   ```bash theme={null}
   git checkout -b feature/your-feature-name
   ```
3. Develop and test locally
   * Make code changes in your IDE
   * Run unit tests or integration tests
4. Commit your changes
   ```bash theme={null}
   git add .
   git commit -m "Implement user authentication flow"
   ```
5. Push your branch to the remote
   ```bash theme={null}
   git push -u origin feature/your-feature-name
   ```

<Callout icon="lightbulb">
  Use clear, descriptive branch names (e.g., `feature/payment-api`) to make pull request reviews and CI/CD tracking easier.
</Callout>

<Frame>
  ![The image is a flowchart illustrating the process of modifying code using GitHub, involving cloning, branching, updating, testing, committing, and pushing changes.](https://kodekloud.com/kk-media/image/upload/v1752870590/notes-assets/images/Certified-Jenkins-Engineer-SCM-Terminology/github-code-modification-flowchart.jpg)
</Frame>

## Key SCM Terms

Below is a quick reference table for essential Git concepts you’ll encounter in Jenkins pipelines and code reviews:

| Term              | Description                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------- |
| Diff              | A line-by-line comparison showing additions, deletions, and modifications between file versions.        |
| Commit            | A snapshot of your codebase at a given point, bundling one or more diffs with a commit message.         |
| HEAD              | A movable pointer referencing the latest commit on your current branch (the tip of development).        |
| Pull Request (PR) | A request to merge changes from one branch into another, enabling discussion and review before merging. |

<Callout icon="triangle-alert">
  Never push directly to the protected `main` branch. Always open a pull request to enforce code reviews, automated testing, and compliance checks.
</Callout>

<Frame>
  ![The image illustrates SCM (Source Control Management) terminology with a diagram showing a branching and merging process, including a pull request and discussions leading to changes. It also lists terms like Diff, Commit, Head, and Pull Request (PR).](https://kodekloud.com/kk-media/image/upload/v1752870591/notes-assets/images/Certified-Jenkins-Engineer-SCM-Terminology/scm-branching-merging-diagram.jpg)
</Frame>

## References

* [Git Official Documentation](https://git-scm.com/doc)
* [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
* [Jenkins SCM Plugin](https://plugins.jenkins.io/scm/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2e8ea9bb-e5bb-428e-85d9-89f2eb816adb/lesson/c0cd6177-dafd-4daf-9144-72c719c2d275" />
</CardGroup>
