# Comparing GitHub Desktop and githubcom

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Desktop/Comparing-GitHub-Desktop-and-githubcom/page

Summarizes differences between GitHub Desktop local Git GUI and GitHub.com web collaboration features and how they integrate for development and CI workflows.

What are the differences between GitHub Desktop and the GitHub.com website?

GitHub Desktop is a cross-platform (Windows and macOS) desktop application designed to simplify and accelerate common local Git workflows. It provides an approachable GUI for working with a local copy of a repository: cloning, branch creation, selective staging (granular commits), committing changes (including co-author attribution), and visual diffs for images and other non-text files.

GitHub.com is the central, web-hosted collaboration platform that complements the local workflow. It focuses on social and administrative features that enable teams to coordinate work: forking, starring, watching, creating and triaging issues, opening and reviewing pull requests, configuring CI/CD integrations, managing access controls, and running web-based code reviews and automation.

<Callout icon="lightbulb">
  GitHub Desktop streamlines local Git operations on your machine, while GitHub.com is the collaboration hub where teams coordinate, review, and automate workflows.
</Callout>

Key differences at a glance

* Local vs. remote: Desktop manages a local working copy; GitHub.com manages the remote repository and team collaboration.
* Workflow focus: Desktop optimizes cloning, branching, staging, and committing. GitHub.com provides pull requests, code review, CI/CD, and repository administration.
* Audience: Desktop helps individual developers and contributors perform local Git tasks more easily. GitHub.com supports teams, project managers, and automation systems.

Comparison table

| Area                   | GitHub Desktop                                                                             | GitHub.com (web)                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Primary purpose        | Local development, GUI for Git                                                             | Remote collaboration, repository hosting                                  |
| Typical actions        | Clone, create branches, selectively stage lines, commit, image diff viewer, add co-authors | Fork, pull requests, code review, issues, CI/CD, access control, releases |
| Where it runs          | Windows, macOS (local app)                                                                 | Browser (web)                                                             |
| CI/CD and automation   | Limited (local hooks)                                                                      | Full integration with Actions and external CI systems                     |
| Collaboration features | Basic (co-authoring metadata)                                                              | Rich (reviews, checks, teams, permissions)                                |

How they work together

* Use GitHub Desktop for branch creation, selective staging, and crafting clean commits locally.
* Push branches to GitHub.com to create pull requests, run CI checks, request reviews, and manage releases.
* The two are complementary: Desktop speeds local development tasks; GitHub.com enables collaboration, governance, and automation.

Example: Jenkins Declarative Pipeline for a release flow
Below is a Jenkins Declarative Pipeline (Groovy) snippet that creates a release branch, updates a Maven qualifier to an RC version, and commits the change. The script name and Maven property references are consistent across stages.

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Create Release Branch') {
            steps {
                // Calls a shell script that creates a release branch locally/remotely
                sh 'scripts/create-release-branch.sh'
            }
        }

        stage('Update Maven Qualifier to RC') {
            steps {
                // Use build-helper:parse-version to populate parsedVersion.* properties,
                // then set the new version using versions:set (and optionally versions:commit).
                // We reference parsedVersion.incrementalVersion here.
                sh 'mvn build-helper:parse-version versions:set -DnewVersion=${parsedVersion.majorVersion}.${parsedVersion.minorVersion}.${parsedVersion.incrementalVersion}-RC-0 versions:commit'
            }
        }

        stage('Commit to Release Branch') {
            steps {
                // Commit the version change to the new release branch
                sh 'git add -A && git commit -m "chore(release): bump qualifier to RC" || true'
                sh 'git push origin HEAD'
            }
        }
    }
}
```

Notes on the pipeline snippet

* Script naming: The branch-creation helper is standardized as `scripts/create-release-branch.sh`.
* Maven properties: The snippet uses `parsedVersion.incrementalVersion` (lowercase), which is the standard property produced by `build-helper:parse-version`.
* Maven command sequence: `build-helper:parse-version` defines `parsedVersion.*` properties. `versions:set` accepts the `-DnewVersion` parameter and applies the version change. `versions:commit` can be invoked after `versions:set` within the same execution to clean up any backup POMs. Note that `versions:commit` itself does not take `-DnewVersion`; that parameter belongs to `versions:set`.
* Safe commit: The `git commit` command includes `|| true` to prevent the pipeline from failing if there are no changes to commit.

How GitHub Desktop maps to the pipeline example

* Branch creation: Desktop makes it easy to create and switch to the release branch before running the pipeline.
* Selective staging & commits: Desktop’s GUI supports staging specific lines or files for precise commits (useful for committing version bumps only).
* Co-authoring and metadata: Desktop can add co-authors to commits locally; GitHub.com will display those attributions in the PR.

Links and references

* GitHub Desktop: [https://desktop.github.com/](https://desktop.github.com/)
* GitHub Docs (GitHub.com): [https://docs.github.com/](https://docs.github.com/)
* Jenkins Pipelines: [https://www.jenkins.io/doc/book/pipeline/](https://www.jenkins.io/doc/book/pipeline/)
* Maven Versions Plugin: [https://www.mojohaus.org/versions-maven-plugin/](https://www.mojohaus.org/versions-maven-plugin/)
* build-helper Maven Plugin: [https://www.mojohaus.org/build-helper-maven-plugin/](https://www.mojohaus.org/build-helper-maven-plugin/)

Further reading

* For more on integrating local workflows with remote automation, see the GitHub Actions and CI/CD documentation on the GitHub Docs site.
* For examples of release automation patterns, consult the Jenkins Pipeline examples and Maven plugin documentation linked above.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/8e078d53-27bf-4e45-af88-efdd39fbeb8f/lesson/709e8098-16c2-444d-8ac4-524ff4efbf9f" />
</CardGroup>
