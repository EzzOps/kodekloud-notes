# include:
#   - template: Security/Code-Quality.gitlab-ci.yml
```

### Example `.gitlab-ci.yml`

A minimal pipeline running SAST and Node.js unit tests:

```yaml theme={null}
stages:
  - .pre
  - test

include:
  - template: Jobs/SAST.gitlab-ci.yml

variables:
  SCAN_KUBERNETES_MANIFESTS: "true"

.prepare_nodejs_environment:
  image: node:16
  before_script:
    - npm ci

sast:
  stage: .pre

unit_testing:
  stage: test
  extends: .prepare_nodejs_environment
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    paths:
      - test-results.xml
    reports:
      junit: test-results.xml
```

After pushing, you’ll see SAST in `.pre` followed by `unit_testing` in `test`.

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a project named "Solar System NodeJS Pipeline," displaying the status of various jobs such as "kubesec-sast" and "unit\_testing."](https://kodekloud.com/kk-media/image/upload/v1752877410/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-cicd-solar-system-pipeline.jpg)
</Frame>

## Viewing SAST Reports

Each SAST job outputs a `gl-sast-report.json`. Download and inspect it with any JSON viewer.

### Example KubeSec Report

```json theme={null}
{
  "version": "15.0.7",
  "vulnerabilities": [],
  "scan": {
    "analyzer": {
      "id": "kubesc",
      "name": "Kubesc",
      "version": "4.0.10"
    },
    "scanner": {
      "id": "kubesc",
      "name": "Kubesc",
      "version": "2.14.0"
    }
  },
  "type": "sast"
}
```

### Example NodeJsScan Report

```json theme={null}
{
  "version": "15.0.7",
  "vulnerabilities": [
    {
      "id": "2d92ba5c9c2e73c14c5a0da201ba74110e14c4ec9640dbf1becfcb05c5295b",
      "name": "node_nosqli_injection",
      "description": "Untrusted user input in findOne() can result in NoSQL Injection.",
      "severity": "High",
      "location": {
        "file": "app.js",
        "start_line": 44,
        "end_line": 53
      },
      "identifiers": [
        {
          "type": "njsscan_rule_type",
          "value": "CWE-943"
        }
      ],
      "scanner": {
        "id": "nodejs-scan",
        "name": "NodeJsScan"
      }
    }
  ]
}
```

Even when vulnerabilities are flagged, subsequent jobs run by default. In higher tiers, issues appear in the Security Dashboard and MR views.

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a project called "Solar System NodeJS Pipeline," displaying the status of various jobs and tests. The pipeline has passed, with jobs like "kubsec-sast," "nodejs-scan-sast," and "unit\_testing" completed successfully.](https://kodekloud.com/kk-media/image/upload/v1752877411/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-SAST/gitlab-ci-cd-solar-system-pipeline.jpg)
</Frame>

***

## Links and References

* [GitLab SAST Documentation](https://docs.gitlab.com/ee/user/application_security/sast/)
* [Semgrep on GitLab](https://gitlab.com/gitlab-org/security-products/semgrep)
* [NodeJsScan on GitLab](https://gitlab.com/gitlab-org/security-products/nodejs-scan)
* [KubeSec on GitLab](https://gitlab.com/gitlab-org/security-products/kubesec)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/40274151-e190-40ee-bc8d-b36797520108" />
</CardGroup>


# Template and Types of Includes

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Template-and-Types-of-Includes/page

Learn to streamline GitLab CI/CD pipelines with reusable templates and includes to reduce YAML duplication and enhance project consistency.

In this lesson, you’ll discover how to streamline your GitLab CI/CD pipelines using reusable templates and various include types. By the end, you’ll be able to eliminate repetitive YAML, enforce consistency across projects, and leverage GitLab’s built-in templates and external includes.

## The Challenge of Repetitive CI YAML

When you define similar jobs (e.g., unit tests, code coverage) across multiple repositories, you often end up duplicating large blocks of configuration:

```yaml theme={null}
