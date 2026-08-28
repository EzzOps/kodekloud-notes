# Define a reusable base job
.base_nodejs_job:
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
  cache:
    policy: pull-push
    key:
      files: [package.json]
      paths: [node_modules]
  before_script:
    - npm install

# Inherit and add specific scripts
unit_testing:
  extends: .base_nodejs_job
  script:
    - npm test

code_coverage:
  extends: .base_nodejs_job
  script:
    - npm run coverage
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

<Callout icon="lightbulb">
  Any update to `.base_nodejs_job` automatically applies to all jobs that extend it, keeping your pipeline DRY and consistent.
</Callout>

***

## 2. YAML Anchors

YAML anchors (`&`) and aliases (`*`) let you reuse blocks **within the same file**.

```yaml theme={null}
# Anchor a base config
.base_node_config: &node_config
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
  cache:
    policy: pull-push
    key:
      files: [package.json]
      paths: [node_modules]
  before_script:
    - npm install

# Merge the anchor into jobs
unit_testing:
  <<: *node_config
  script:
    - npm test

code_coverage:
  <<: *node_config
  script:
    - npm run coverage
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

<Callout icon="triangle-alert">
  YAML anchors do **not** work across multiple files. Use `extends` or `!reference` for cross-file reuse.
</Callout>

***

## 3. Reference Tags

GitLab’s custom `!reference` tag imports specific sections from other jobs **even across files**.

```yaml theme={null}
# In .gitlab-ci-common.yml
.base_nodejs_config:
  cache:
    paths: [node_modules]
  test_script: [npm test]
  code_coverage_script: [npm run coverage]
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual

# In .gitlab-ci.yml
unit_testing:
  image: node:17-alpine3.14
  cache: !reference [.base_nodejs_config, cache]
  before_script: [npm install]
  script: !reference [.base_nodejs_config, test_script]

code_coverage:
  image: node:17-alpine3.14
  before_script:
    - npm install
  script: !reference [.base_nodejs_config, code_coverage_script]
  rules: !reference [.base_nodejs_config, rules]
```

<Callout icon="lightbulb">
  `!reference` tags require GitLab Runner 12.6+ and allow fine-grained imports of job snippets.
</Callout>

***

## Further Reading

* [GitLab CI/CD Pipeline Configuration Reference](https://docs.gitlab.com/ee/ci/yaml/)
* [YAML Anchors and Aliases](https://yaml.org/spec/1.2/spec.html#id2765878)
* [Using `extends` in GitLab CI/CD](https://docs.gitlab.com/ee/ci/yaml/#extends)
* [Reference Tags (`!reference`)](https://docs.gitlab.com/ee/ci/yaml/#reference)

By leveraging hidden jobs with **`extends`**, **YAML anchors**, and **`!reference`** tags, you can keep your GitLab CI/CD pipelines maintainable, scalable, and free from repetition.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/c0d6666b-f0c1-4977-a7c4-caf49deac8a5" />
</CardGroup>


# Reference Tags Reuse Configuration Integration Testing

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Reference-Tags-Reuse-Configuration-Integration-Testing/page

This article explains how to use GitLab CI/CD reference tags and YAML anchors to share configuration snippets across multiple jobs.

In this lesson, we’ll walk through how to leverage GitLab CI/CD reference tags (`!reference`) and standard YAML anchors to share configuration snippets across multiple jobs. By doing so, you can DRY up your pipeline definitions—pulling in values like `image`, `before_script`, or `script` from one job into another and avoiding duplication.

***

## 1. Basic YAML Anchors and `!reference` Tags

GitLab CI/CD supports two primary mechanisms for reusing snippets:

| Method              | Syntax                      | Use Case                                   |
| ------------------- | --------------------------- | ------------------------------------------ |
| YAML Anchors        | `&anchor` / `*alias`        | Share simple lists or maps within the file |
| GitLab `!reference` | `!reference [job, section]` | Import complete sections (`script`, etc.)  |

```yaml theme={null}
