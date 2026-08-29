# …
Job succeeded
```

This approach centralizes maintenance: updating `.prepare_nodejs_environment` applies to all linked jobs.

***

For more on merging hidden jobs or combining `include` with `extends`, see the [GitLab CI/CD documentation on `extends`](https://docs.gitlab.com/ee/ci/yaml/#extends).

## Links and References

* [Optimizing GitLab CI/CD configuration](https://docs.gitlab.com/ee/ci/yaml/#extends)
* [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
* [GitLab Includes](https://docs.gitlab.com/ee/ci/yaml/includes.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/e2b230b7-2726-4bf3-8769-ba01843b5272)


# Optimize CICD configuration files

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Optimize-CICD-configuration-files/page

This article discusses optimizing GitLab CI/CD configuration files through modularization to enhance maintainability and scalability.

When setting up an application pipeline, it’s easy to copy-paste previous CI/CD snippets. While this speeds up the initial setup, it makes maintenance and scaling a headache. By **modularizing** your GitLab CI/CD pipelines, you can:

* Eliminate duplicated code
* Standardize workflows
* Simplify updates as your project grows

![The image outlines strategies for optimizing CI pipeline development, focusing on avoiding copy-pasting, maintenance considerations, and modularization benefits. Each strategy is represented with an icon and a colored background.](https://kodekloud.com/kk-media/image/upload/v1752877368/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Optimize-CICD-configuration-files/ci-pipeline-optimization-strategies.jpg)

GitLab CI/CD provides three powerful mechanisms for DRY pipelines:

| Feature        | Purpose                              | Scope       | Cross-File Support | Syntax                    |
| -------------- | ------------------------------------ | ----------- | ------------------ | ------------------------- |
| Extends        | Inherit and override job definitions | Multi-file  | Yes                | `extends: .base_job`      |
| YAML Anchors   | Reuse blocks within a single file    | Single file | No                 | `&anchor` / `<<: *anchor` |
| Reference Tags | Pull snippets across YAML files      | Multi-file  | Yes                | `!reference [job, key]`   |

![The image is a visual representation of GitLab CI/CD concepts, featuring five colored cards labeled "Extends Keyword," "Anchors," "Reference Tags," "Templates," and "CI/CD Components," each with an icon.](https://kodekloud.com/kk-media/image/upload/v1752877369/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Optimize-CICD-configuration-files/gitlab-cicd-concepts-visualization.jpg)

***

## Hidden Jobs

Jobs prefixed with a dot (`.`) are **hidden**: they never run on their own but serve as reusable templates.

```yaml theme={null}
.hidden_common:
  cache:
    policy: pull-push
    key:
      files: [package.json]
      paths: [node_modules]
  before_script:
    - npm install
```

Use hidden jobs for:

* Common cache rules
* Shared `before_script` steps
* Disabling jobs without deleting them

***

## 1. The `extends` Keyword

Use `extends` to inherit from hidden or other jobs—even across multiple files. GitLab merges parent and child definitions, with child values overriding duplicates.

### Example: Node.js Jobs

```yaml theme={null}
