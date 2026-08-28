# Pipeline Configure Coverage and Archive Reports

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Pipeline-Configure-Coverage-and-Archive-Reports/page

This guide explains setting up a parallel code coverage job in GitLab CI/CD alongside unit tests and archiving reports.

In this guide, you’ll learn how to set up a parallel code coverage job alongside unit tests in GitLab CI/CD, archive reports, and surface coverage metrics in the UI.

## Base Unit Testing Job

This `unit_testing` job runs in the `test` stage, installs dependencies, executes tests, and collects JUnit reports:

```yaml theme={null}
stages:
  - test

variables:
  MONGO_URI: 'mongodb+srv://superCluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD

unit_testing:
  stage: test
  image: node:17-alpine3.14
  before_script:
    - npm install
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: Moca-Test-Result
    paths:
      - test-results.xml
  reports:
    junit: test-results.xml
```

## Adding a Parallel Code Coverage Job

Create a `code_coverage` job that reuses the Node.js image and installs dependencies. The `npm run coverage` command (powered by [NYC](https://github.com/istanbuljs/nyc)) generates a Cobertura XML report.

```yaml theme={null}
code_coverage:
  stage: test
  image: node:17-alpine3.14
  before_script:
    - npm install
  script:
    - npm run coverage
  artifacts:
    name: Code-Coverage-Result
    when: always
    expire_in: 3 days
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  coverage: '/All files[^|]*\|[^|]*\s+([0-9.]+)%/'
```

## Supported Artifact Report Types

GitLab CI/CD supports multiple report formats under [`artifacts:reports`](https://docs.gitlab.com/ee/ci/yaml/#artifactsreports). Use the table below to choose the appropriate type:

| Report Type          | Description                         | Example                                                                                                   |
| -------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------- |
| junit                | JUnit XML test reports              | `reports:\n  junit: test-results.xml`                                                                     |
| coverage\_report     | Cobertura coverage results          | `reports:\n  coverage_report:\n    coverage_format: cobertura\n    path: coverage/cobertura-coverage.xml` |
| codequality          | Static code analysis (Code Quality) | `reports:\n  codequality: gl-code-quality-report.json`                                                    |
| dependency\_scanning | Dependency vulnerability report     | `reports:\n  dependency_scanning: gl-dependency-scanning-report.json`                                     |

<Frame>
  ![The image shows a GitLab documentation page about CI/CD artifact report types, detailing how to use artifacts:reports for collecting various reports in jobs. The page includes a sidebar with navigation links and a list of report types on the right.](https://kodekloud.com/kk-media/image/upload/v1752877269/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Configure-Coverage-and-Archive-Reports/gitlab-cicd-artifact-reports.jpg)
</Frame>

## Coverage Report Configuration

To enable GitLab’s built-in coverage display, specify the Cobertura format and the XML path in `artifacts:reports`:

```yaml theme={null}
artifacts:
  reports:
    coverage_report:
      coverage_format: cobertura
      path: coverage/cobertura-coverage.xml
```

## Extracting Coverage Percentage

GitLab can parse test logs and extract a coverage percentage using a regular expression. For NYC’s “All files” summary line, use:

```yaml theme={null}
coverage: '/All files[^|]*\|[^|]*\s+([0-9.]+)%/'
```

<Callout icon="lightbulb">
  Make sure your coverage tool prints a summary line matching this pattern. Adjust the regex if your output differs.
</Callout>

<Frame>
  ![The image shows a GitLab documentation page detailing test coverage examples with regex patterns for various programming languages and tools. The sidebar includes navigation links related to code coverage and testing.](https://kodekloud.com/kk-media/image/upload/v1752877271/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Configure-Coverage-and-Archive-Reports/gitlab-test-coverage-regex-examples.jpg)
</Frame>

## Full CI Configuration with a Dependent Sample Job

Combine both jobs and add a `sample-job` that depends on `code_coverage`. This ensures downstream work only runs if coverage passes (or you enable `allow_failure`).

```yaml theme={null}
stages:
  - test

variables:
  MONGO_URI: 'mongodb+srv://superCluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD

unit_testing:
  stage: test
  image: node:17-alpine3.14
  before_script:
    - npm install
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: Moca-Test-Result
    paths:
      - test-results.xml
  reports:
    junit: test-results.xml

code_coverage:
  stage: test
  image: node:17-alpine3.14
  before_script:
    - npm install
  script:
    - npm run coverage
  artifacts:
    name: Code-Coverage-Result
    when: always
    expire_in: 3 days
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  coverage: '/All files[^|]*\|[^|]*\s+([0-9.]+)%/'

sample-job:
  stage: test
  needs:
    - code_coverage
  image: node:17-alpine3.14
  script:
    - echo "Running sample job"
```

Once you push this `.gitlab-ci.yml`, the GitLab pipeline graph clearly shows `unit_testing`, `code_coverage`, and `sample-job` in parallel:

<Frame>
  ![The image shows a GitLab Pipeline Editor interface with a successful pipeline status and a visualization of jobs including "unit\_testing," "code\_coverage," and "sample-job."](https://kodekloud.com/kk-media/image/upload/v1752877272/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Configure-Coverage-and-Archive-Reports/gitlab-pipeline-editor-success-jobs.jpg)
</Frame>

## Pipeline Execution and Coverage Failure

If the coverage threshold defined in your `package.json` isn’t met, the `code_coverage` job fails and downstream jobs are skipped by default.

<Callout icon="triangle-alert">
  A failed coverage check will block any jobs that depend on it. To continue the pipeline regardless of coverage, you can set `allow_failure: true` on the coverage job.
</Callout>

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a NodeJS project named "Solar System," where a job named "code\_coverage" has failed, while "unit\_testing" has succeeded.](https://kodekloud.com/kk-media/image/upload/v1752877273/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Configure-Coverage-and-Archive-Reports/gitlab-cicd-solar-system-pipeline.jpg)
</Frame>

Example logs from NYC:

```bash theme={null}
> nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test.js --timeout 10000 --exit
...
ERROR: Coverage for lines (88.88%) does not meet global threshold (90%)
| File       | % Branch | % Funcs | % Lines | Uncovered Line #s |
|------------|----------|---------|---------|-------------------|
| All files  | 88.88    | 50      | 87.50   | 88.88             |
```

Your `package.json` might include:

```json theme={null}
{
  "scripts": {
    "coverage": "nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test.js"
  },
  "nyc": {
    "check-coverage": true,
    "lines": 90
  }
}
```

## Coverage Percentage in the GitLab UI

With the `coverage` regex in place, GitLab extracts the percentage (e.g., **88.88%**) and displays it in the pipeline view:

<Frame>
  ![The image shows a GitLab pipeline interface for a NodeJS project, indicating a failed pipeline with 11 tests, all of which passed successfully.](https://kodekloud.com/kk-media/image/upload/v1752877274/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Configure-Coverage-and-Archive-Reports/gitlab-pipeline-nodejs-failed-tests.jpg)
</Frame>

In this scenario, coverage is below the 90% threshold, causing `code_coverage` to fail and skipping `sample-job`:

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a NodeJS project named "Solar System," displaying job statuses including one failed, one passed, and one skipped job. The "code\_coverage" job has a coverage percentage of 88.88%.](https://kodekloud.com/kk-media/image/upload/v1752877275/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Configure-Coverage-and-Archive-Reports/gitlab-cicd-solar-system-pipeline-2.jpg)
</Frame>

***

Next, we’ll look at strategies to allow selective failures and continue pipeline execution even when coverage checks fail.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/16a8435e-ad47-47f9-9187-57b3fe688ebb" />
</CardGroup>
