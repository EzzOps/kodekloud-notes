# Types of Jenkins Projects

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Types-of-Jenkins-Projects/page

Overview of Jenkins project types and guidance on when to use Freestyle, Pipeline, Multibranch, Maven, Matrix, and Organization Folders, with migration recommendations

Jenkins supports several core project types (commonly called "jobs") to automate builds, tests, and deployments. Choosing the right project type impacts maintainability, reproducibility, and how easily teams can adopt pipeline-as-code. Below is a concise overview of the main Jenkins project types and when to use each.

* Freestyle Project — The simplest, UI-configured job for sequential build steps and small automation tasks.
* Pipeline Project — A pipeline defined in code (typically a `Jenkinsfile`) that supports stages, parallelism, and conditional logic. Available in both Declarative and Scripted syntaxes.
* Multibranch Pipeline — Automatically detects branches in a repository and runs a `Jenkinsfile` for each branch; ideal for workflows with multiple active branches.
* Maven Project — Specialized for Maven-based Java builds: Jenkins detects `pom.xml` and runs standard Maven goals with lifecycle integration.
* Multi-configuration Project (Matrix Project) — Executes the same build across a matrix of axes (for example: OS, JDK, dependency versions).
* Organization Folders — A hierarchical grouping mechanism that auto-discovers repositories and creates jobs (such as multibranch pipelines) for each repository.

<Frame>
  <img alt="A slide titled &#x22;Type of Jenkins Projects&#x22; showing six colorful tiles with icons labeled Freestyle Project, Pipeline Project, Multibranch Pipeline, Maven Project, Multi-configuration Project, and Organization Folders. Each project type is represented by a rounded colored tile with a simple white line icon." />
</Frame>

| Project Type                | Purpose                                                             | When to Use                                                                       |
| --------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Freestyle Project           | UI-driven job with sequential build steps                           | Small, one-off tasks or quick automation where pipeline-as-code is not required   |
| Pipeline Project            | Code-defined CI/CD pipelines using a `Jenkinsfile`                  | Complex workflows needing stages, parallelism, and versioned pipeline definitions |
| Multibranch Pipeline        | Per-branch pipelines created automatically from repository branches | Repositories with multiple active branches, each with its own `Jenkinsfile`       |
| Maven Project               | Maven-specific build support and lifecycle integration              | Java projects that follow Maven conventions (`pom.xml`)                           |
| Multi-configuration Project | Run builds across combinations of environment axes                  | Matrix testing across OS/JDK/dependency variants                                  |
| Organization Folders        | Auto-discover and organize many repositories and their pipelines    | Large organizations managing many repos and teams                                 |

> **lightbulb** Some Jenkins installations expose additional project types or UI features via plugins. When auditing or migrating pipelines, list installed plugins to identify available job types and any extended behavior.

## Freestyle Projects (overview and example)

Freestyle projects are the traditional Jenkins jobs that let you configure a sequence of build steps through the web UI. Typical steps include SCM checkout, shell or batch commands, test runners, build tasks (e.g., Docker build), and artifact publishing. Because configuration is stored in the Jenkins UI, freestyle jobs are quick to create but are not defined as code.

Common patterns:

* A job that clones a repository and runs unit tests.
* A job that builds a Docker image and pushes it to a container registry.
* A downstream job that deploys previously built artifacts.

Freestyle jobs can be chained using upstream/downstream triggers to approximate pipeline behavior, but each job remains an independent configuration.

<Frame>
  <img alt="The left side shows a &#x22;New Item&#x22; form with a Freestyle project selected. The right side is a vertical diagram of chained project stages labeled with icons like Clone Code, Run Tests, Build, and Push." />
</Frame>

### When freestyle is appropriate

* Quick, simple automation tasks that don’t require versioned pipelines.
* Prototyping or ad-hoc jobs where speed of setup matters.
* Teams not yet ready to adopt pipeline-as-code or when legacy constraints prevent moving to `Jenkinsfile`.

## Limitations of Freestyle Projects

Freestyle jobs are reliable for small tasks but show important limitations for modern CI/CD:

1. Limited workflow expressiveness — Build steps run sequentially; advanced branching, parallel execution, and conditional flow require fragile workarounds.
2. Non-code-based configuration — Job settings live in Jenkins UI, making versioning, peer review, and reproducible rollbacks difficult.
3. Maintainability challenges — As the number of freestyle jobs grows, tracking dependencies and global changes becomes error-prone.
4. Limited built-in functionality for advanced pipeline needs — Many delivery patterns (e.g., durable checkout, checkpointing, complex parallelism) are easier with Pipeline projects.
5. No automatic resume after controller failure — Freestyle jobs typically cannot resume where they left off after a controller restart; Pipeline (with durable steps) can do better.

<Frame>
  <img alt="A presentation slide titled &#x22;Freestyle Projects - Limitations&#x22; showing five numbered cards with colored icons. The cards list: Limited Workflow; Non-Code-Based Configuration; Complexity Challenges; Limited Functionality; and Cannot Resume After Failure." />
</Frame>

> **warning** Freestyle projects are generally considered legacy for complex CI/CD. For maintainability, reproducibility, and advanced workflow control, prefer `Pipeline` or `Multibranch Pipeline` with a versioned `Jenkinsfile`.

## Recommendation and next steps

* For modern CI/CD adopt pipeline-as-code: create `Jenkinsfile` in source control and use Pipeline or Multibranch Pipeline projects.
* Use Freestyle only for short-lived or simple tasks where converting to a `Jenkinsfile` is not feasible.
* When migrating, inventory installed plugins and existing freestyle jobs to identify automation that should become code-defined pipelines.

Links and references:

* [Jenkins Pipeline (official docs)](https://www.jenkins.io/doc/book/pipeline/)
* [Jenkins Multibranch Pipeline](https://www.jenkins.io/doc/book/pipeline/multibranch/)
* [Jenkins Plugin Index](https://plugins.jenkins.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/06e39454-0936-47cd-8708-c02914ddcfc3)
