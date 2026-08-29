# … other jobs …
```

![The image shows a GitLab CI/CD Catalog interface with a list of components available for improving pipeline functionality. It includes a feedback section and a search bar for exploring components.](https://kodekloud.com/kk-media/image/upload/v1752877346/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-cicd-catalog-interface.jpg)

Click **code-quality** to view usage details and inspect its repository files:

![The image shows a GitLab repository interface for a project named "Code Quality," displaying a list of files and folders with their last commit messages and update times.](https://kodekloud.com/kk-media/image/upload/v1752877347/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-code-quality-repo-interface.jpg)

Snippet from the component’s template:

```yaml theme={null}
code_quality:
  artifacts:
    paths:
      - gl-code-quality-report.json
  rules:
    - if: $CI_MERGE_REQUEST_ID || $CI_COMMIT_TAG || $CI_COMMIT_BRANCH
```

## 2. Add Code Quality to Your Pipeline

Start with a basic Node.js pipeline:

```yaml theme={null}
stages:
  - test

.prepare_nodejs_environment: &prepare_nodejs
  image: node:14
  before_script:
    - npm install

unit_testing:
  stage: test
  extends: *prepare_nodejs
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

Include the Code Quality component before defining your jobs:

```yaml theme={null}
include:
  - component: gitlab.com/gitlab-components/code-quality/code-quality@1.0

stages:
  - test

# … your existing jobs … #
```

Once committed, the pipeline adds a `code_quality` job automatically:

![The image shows a GitLab interface with a pipeline editor, indicating a successful pipeline run with stages for code quality and unit testing. The sidebar includes options like Issues, Merge requests, and Pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877347/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-pipeline-editor-successful-run.jpg)

### View the Merged Configuration

Click **View full config** in the pipeline editor to see how your `.gitlab-ci.yml` merges with the Code Quality template:

```yaml theme={null}
code_quality:
  stage: test
  image: docker:20.10.12
  allow_failure: true
  services:
    - name: docker:20.10.12-dind
      command: ["--tls=false", "--host=tcp://0.0.0.0:2375"]
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: ""
  script:
    - export SOURCE_CODE=$PWD
    - docker pull -q $CI_TEMPLATE_REGISTRY_HOST/gitlab-org/ci-cd/codequality:0.96.0
    - docker run --rm \
        --volume "$SOURCE_CODE":/code \
        --volume /var/run/docker.sock:/var/run/docker.sock \
        $CI_TEMPLATE_REGISTRY_HOST/gitlab-org/ci-cd/codequality:0.96.0 /code
  artifacts:
    reports:
      codequality:
        - gl-code-quality-report.json
    expire_in: 1 week
  rules:
    - if: '$CI_COMMIT_TAG || $CI_COMMIT_BRANCH'
      when: always
```

By default, `allow_failure: true` ensures Code Quality issues don’t block merges.

## 3. Customize Stages & Report Formats

GitLab supports two special stages: `.pre` and `.post`. Assign `code_quality` to `.pre` for early feedback:

```yaml theme={null}
stages:
  - ".pre"
  - test
  - build
  - deploy
  - ".post"

include:
  - component: gitlab.com/gitlab-components/code-quality/code-quality@1.0

code_quality:
  stage: ".pre"
```

To generate an HTML report instead of JSON:

```yaml theme={null}
code_quality:
  stage: ".pre"
  variables:
    REPORT_FORMAT: html
  artifacts:
    paths:
      - gl-code-quality-report.html
    reports:
      codequality: []
```

This stores `gl-code-quality-report.html` as a job artifact.

## 4. Pipeline Run & Artifacts

Triggering a commit runs both `code_quality` and `unit_testing` jobs:

![The image shows a GitLab CI/CD pipeline interface for a NodeJS project, displaying stages for code quality and unit testing. The pipeline is currently running, with one job in progress.](https://kodekloud.com/kk-media/image/upload/v1752877348/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-cicd-nodejs-pipeline.jpg)

Inspect logs to see the analysis steps:

```bash theme={null}
$ export SOURCE_CODE=$PWD
$ docker pull -q $CI_TEMPLATE_REGISTRY_HOST/gitlab-org/ci-cd/codequality:0.96.0
$ docker run --rm \
    --volume "$SOURCE_CODE":/code \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    ...
```

Browse the HTML or JSON report via the job’s **Browse** link. The report groups findings by:

* Bug Risk
* Complexity
* Duplication
* Style

For inline MR annotations, GitLab uses the JSON report.

### Example Findings

**Bug Risk**

```javascript theme={null}
throw new Error('Request failed.');
}).catch(function(error) {
  alert("Ooops, We have 8 planets.\nSelect a number from 0 - 8");
  console.log(error);
})
```

**Duplication**

```javascript theme={null}
describe('Fetching Planet Details', () => {
  it('should fetch Mercury', (done) => {
    const payload = { id: 1 };
    chai.request(server)
      .post('/planet')
      .send(payload);
      .end((err, res) => {
        res.should.have.status(200);
        res.body.should.have.property('name').eql('Mercury');
        done();
      });
  });
});
```

## Additional Code Quality Features

Top-tier GitLab plans unlock more advanced tools:

| Feature                             | Availability    |
| ----------------------------------- | --------------- |
| Pipeline view inline annotations    | Premium & above |
| Project Quality Dashboard summaries | Ultimate        |
| Merge Request **Changes** view      | Ultimate        |

![The image shows a GitLab documentation page detailing features available per tier (Free, Premium, Ultimate) for code quality. It includes a table listing features like configuring scanners and generating report artifacts.](https://kodekloud.com/kk-media/image/upload/v1752877360/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-code-quality-features-table-2.jpg)

After review, your pipeline completes successfully:

![The image shows a GitLab pipeline interface for a NodeJS project, displaying a successful pipeline run with stages for code quality and unit testing.](https://kodekloud.com/kk-media/image/upload/v1752877362/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Component-Code-Quality/gitlab-pipeline-nodejs-success.jpg)

That’s it! You’ve integrated and customized GitLab’s Code Quality component to elevate your CI/CD standards.

***

## Links and References

* [GitLab CI/CD Components Catalog][catalog-docs]
* [Code Climate](https://codeclimate.com/)
* [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)

[catalog-docs]: https://docs.gitlab.com/ee/ci/components/README.html

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/a6fa4504-3b90-44fa-8212-4527665bd8d3)


# Extends Reuse Configuration NodeJS Jobs

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Extends-Reuse-Configuration-NodeJS-Jobs/page

Learn to reuse configuration in GitLab CI/CD pipelines using the extends keyword to eliminate duplication and streamline job definitions.

Learn how to eliminate duplication in your GitLab CI/CD pipelines by reusing configuration with the `extends` keyword. This guide covers three primary strategies:

| Method                 | Description                                       | Example                                     |
| ---------------------- | ------------------------------------------------- | ------------------------------------------- |
| `extends`              | Inherit settings from hidden jobs (templates)     | `.rspec` → `rspec 1`                        |
| YAML anchors & aliases | Reuse blocks of config (scripts, variables, etc.) | `&default_scripts` / `*default_scripts`     |
| Reference tags         | Share tags or other fields across multiple jobs   | `tags: &common_tags` / `tags: *common_tags` |

> **lightbulb** You can combine `include` with `extends` to pull in templates from external files and inherit from them in one step.

## 1. Anchors & Aliases

Use YAML anchors to define reusable snippets:

```yaml theme={null}
.default_scripts: &default_scripts
  - ./default-script1.sh
  - ./default-script2.sh

job1:
  script:
    <<: *default_scripts
```

## 2. Using `extends`

Define hidden jobs (prefixed with a dot) as templates, then inherit from them:

```yaml theme={null}
.tests:
  rules:
    - if: $CI_PIPELINE_SOURCE == "push"

.rspec:
  extends: .tests
  script:
    - rake rspec

rspec 1:
  extends: .rspec
  variables:
    RSPEC_SUITE: '1'

rspec 2:
  extends: .rspec
  variables:
    RSPEC_SUITE: '2'
```

GitLab supports up to 11 inheritance levels, but keeping it under three levels is recommended:

> **triangle-alert** Deep inheritance trees can become hard to maintain. Aim for 2–3 levels only.

### Multi-template Inheritance

You can merge multiple hidden jobs:

```yaml theme={null}
.only-important:
  variables:
    URL: "http://my-url.internal"
    IMPORTANT_VAR: "details"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_BRANCH == "stable"
  tags:
    - production
  script:
    - echo "Hello world!"

.in-docker:
  image: alpine
  variables:
    URL: "http://docker-url.internal"
  tags:
    - docker

rspec:
  extends:
    - .only-important
    - .in-docker
  variables:
    GITLAB: "is-awesome"
  script:
    - rake rspec
```

## 3. Refactoring NodeJS Test Jobs

Imagine a pipeline where the **test** stage contains two nearly identical NodeJS jobs: `unit_testing` and `code_coverage`. To speed up feedback, other stages are commented out.

![The image shows a GitLab pipeline editor with a visual representation of a CI/CD pipeline, including stages like testing, containerization, and deployment.](https://kodekloud.com/kk-media/image/upload/v1752877367/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Extends-Reuse-Configuration-NodeJS-Jobs/gitlab-pipeline-ci-cd-editor.jpg)

Both jobs share the following configuration:

```yaml theme={null}
stage: test
image: node:17-alpine3.14
services:
  - name: siddharth67/mongo-db:non-prod
    alias: mongo
    pull_policy: always
variables:
  MONGO_URI: 'mongodb://mongo:27017/superData'
  MONGO_USERNAME: non-prod-user
  MONGO_PASSWORD: non-prod-password
cache:
  key:
    files:
      - package-lock.json
    prefix: node_modules
  policy: pull-push
  when: on_success
  paths:
    - node_modules
before_script:
  - npm install
```

### 3.1 Create a Hidden Template

Extract the shared configuration into a single hidden job:

```yaml theme={null}
.prepare_nodejs_environment:
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
      alias: mongo
      pull_policy: always
  variables:
    MONGO_URI: 'mongodb://mongo:27017/superData'
    MONGO_USERNAME: non-prod-user
    MONGO_PASSWORD: non-prod-password
  cache:
    policy: pull-push
    when: on_success
    paths:
      - node_modules
    key:
      files:
        - package-lock.json
      prefix: node_modules
  before_script:
    - npm install
```

### 3.2 Refactor Job Definitions

Have both jobs inherit from the `.prepare_nodejs_environment` template:

```yaml theme={null}
unit_testing:
  stage: test
  extends: .prepare_nodejs_environment
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: Moca-Test-Results
    paths:
      - test-results.xml
    reports:
      junit: test-results.xml

code_coverage:
  stage: test
  extends: .prepare_nodejs_environment
  script:
    - npm run coverage
  artifacts:
    name: Code-Coverage-Report
    when: always
    expire_in: 3 days
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  coverage: /All files[^|]*\|[^|]*\s+(\d+\.\d+)/
  allow_failure: true
```

## 4. Inspecting the Merged Configuration

GitLab’s **CI Lint** or **Full configuration** view will show the merged result for `unit_testing`:

```yaml theme={null}
unit_testing:
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
      alias: mongo
      pull_policy: always
  variables:
    MONGO_URI: mongodb://mongo:27017/superData
    MONGO_USERNAME: non-prod-user
    MONGO_PASSWORD: non-prod-password
  cache:
    policy: pull-push
    when: on_success
    paths:
      - node_modules
    key:
      files:
        - package-lock.json
      prefix: node_modules
  before_script:
    - npm install
  script:
    - npm test
  artifacts:
    paths:
      - test-results.xml
```

## 5. Pipeline Execution

When you commit these changes, both `unit_testing` and `code_coverage` run in parallel with the shared setup:

```bash theme={null}
$ npm install
$ npm test
