# .gitlab-ci.yml
unit_testing:
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
  cache:
    policy: pull-push
    key:
      files:
        - package.json
      paths:
        - node_modules
  before_script:
    - npm install
  script:
    - npm test

code_coverage:
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
  cache:
    policy: pull-push
    key:
      files:
        - package.json
      paths:
        - node_modules
  before_script:
    - npm install
  script:
    - npm run coverage
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
```

Maintaining these blocks manually is error-prone and time-consuming. Templates and includes help you define once and reuse everywhere.

## GitLab CI/CD Templates

GitLab provides two primary template categories:

* **Pipeline Templates**\
  Full end-to-end CI/CD workflows for common project types (Node.js, Ruby on Rails, etc.).
* **Job Templates**\
  Standalone jobs for tasks like security scans, linting, or Docker builds.

By including a template, you inherit predefined stages and jobs, then override or extend only what’s unique to your project.

<Callout icon="lightbulb">
  Built-in templates live in the [`gitlab-org/gitlab` repository][gitlab-templates]. You can also publish your own templates in a dedicated project.
</Callout>

### Example: Reusing a Node.js Pipeline Template

Team A and Team B share a common Node.js template but customize deployment targets:

* **Team A**
  * Registry: Docker Hub
  * Deployment: AWS EKS
* **Team B**
  * Registry: Google Container Registry
  * Deployment: GKE

Both pipelines run the same stages—unit testing, code coverage, build & push, deploy—but inject different variables, credentials, and `script` overrides.

<Frame>
  ![The image is a flowchart showing CI/CD pipelines for two projects, "Project A/Repo A" and "Project B/Repo B," both using a "NodeJS Template" for processes like unit testing, code coverage, building/pushing to Docker Hub, and deploying to EKS.](https://kodekloud.com/kk-media/image/upload/v1752877412/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Template-and-Types-of-Includes/ci-cd-pipelines-flowchart-nodejs.jpg)
</Frame>

## Key Takeaways

* Reusable templates accelerate onboarding and ensure best practices.
* Modular design lets teams opt into only the stages they require.
* Customization points (variables, `before_script`, `after_script`) handle project-specific needs.

## Types of Includes

GitLab CI/CD supports four include sources:

| Include Type | Description                                   | YAML Example                                                                                      |
| ------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| local        | Files in the same repo/branch                 | `- local: 'jobs/.after-script.yml'`                                                               |
| remote       | YAML from an external URL                     | `- remote: 'https://example.com/ci/.before-script.yml'`                                           |
| project      | Files in another project on the same instance | `- project: 'my-group/avengers-project'`<br />`  ref: main`<br />`  file: '/jobs/.gitlab-ci.yml'` |
| template     | GitLab’s built-in CI templates                | `- template: 'Code-Quality.gitlab-ci.yml'`                                                        |

<Callout icon="triangle-alert">
  When using `local` includes, the default branch is `HEAD`. Specify `ref` if you need a different branch or tag.
</Callout>

### Conditional Includes

You can apply includes only under specific conditions using `rules`:

```yaml theme={null}
include:
  - template: 'Code-Quality.gitlab-ci.yml'
    rules:
      - if: '$CI_COMMIT_BRANCH =~ /^feature\//'
        when: always
```

This ensures that the Code-Quality template is only included for feature branches.

## References

* [GitLab CI/CD Includes Documentation][includes-docs]
* [GitLab CI/CD Templates Overview][templates-docs]

[gitlab-templates]: https://gitlab.com/gitlab-org/gitlab/-/tree/master/lib/gitlab/ci/templates

[includes-docs]: https://docs.gitlab.com/ee/ci/yaml/includes.html

[templates-docs]: https://docs.gitlab.com/ee/ci/yaml/#using-built-in-ci-templates

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/55d8534e-2819-4856-8d32-b5c5fb513fd6" />
</CardGroup>


# AutoDevOps Customization

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Auto-DevOps/AutoDevOps-Customization/page

Learn to customize your GitLab Auto DevOps pipeline for a timed incremental rollout deployment strategy, enhancing your CI/CD process.

In this guide, learn how to tailor your GitLab Auto DevOps pipeline to implement a **timed incremental rollout** deployment strategy. You’ll enable this strategy, override default jobs, and customize which tests and scans run to streamline your CI/CD process.

## Timed Incremental Rollout Strategy

A timed incremental rollout gradually shifts traffic in phases:

* Step 1: 10% traffic
* Step 2: 25% traffic
* Step 3: 50% traffic
* Step 4: 100% traffic

Each phase pauses for 5 minutes by default, giving you time to validate stability and, if necessary, roll back.

<Frame>
  ![The image shows a GitLab CI/CD settings page with options for configuring Auto DevOps pipelines and deployment strategies. The sidebar includes navigation options like Deploy, Operate, and Monitor.](https://kodekloud.com/kk-media/image/upload/v1752877054/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-cicd-auto-devops-settings.jpg)
</Frame>

To enable the timed rollout:

1. Go to **Settings > CI/CD > Auto DevOps**
2. Select **Continuous deployment to production using timed incremental rollout**
3. Click **Save changes**

<Callout icon="lightbulb">
  Adjust the interval between rollout steps by setting the `AUTO_DEPLOY_WAIT_TIME` variable in your `.gitlab-ci.yml` or project settings.
</Callout>

## Reviewing Current Pipelines

Out of the box, Auto DevOps runs up to 17 jobs across multiple stages. You can disable unused jobs—like certain tests or scans—to speed up your pipeline while retaining essential checks like secret detection.

<Frame>
  ![The image shows a GitLab interface displaying a list of CI/CD pipelines with their statuses, such as "Warning," "Passed," and "Canceled." Each pipeline entry includes details like the branch name, commit ID, and the user who created it.](https://kodekloud.com/kk-media/image/upload/v1752877055/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-cicd-pipelines-statuses.jpg)
</Frame>

## Adding Your Own `.gitlab-ci.yml`

Override or extend Auto DevOps by adding a custom CI configuration file at your repository root:

<Frame>
  ![The image shows a GitLab repository interface with a list of files and their last commit messages. The repository is named "solar-system-autodevops" and includes files like app-controller.js and README.md.](https://kodekloud.com/kk-media/image/upload/v1752877056/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-repository-solar-system-autodevops.jpg)
</Frame>

1. In **Files**, click **+** and name the file `.gitlab-ci.yml`.
2. Choose **Apply a template** or start from scratch.

<Frame>
  ![The image shows a GitLab interface where a new file named .gitlab-ci.yml is being created, with a dropdown menu displaying various template options.](https://kodekloud.com/kk-media/image/upload/v1752877057/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-ci-yml-file-creation.jpg)
</Frame>

## Including the Auto DevOps Template

Pull in the default Auto DevOps jobs without copying the full configuration:

```yaml theme={null}
include:
  template: Auto-DevOps.gitlab-ci.yml
```

Open **CI/CD > Editor**, paste the snippet, then click **Visualize** to inspect all jobs and stages.

<Frame>
  ![The image shows a GitLab pipeline editor interface with a visualized pipeline flow, including stages like "staging," "canary," and "production," along with various rollout steps.](https://kodekloud.com/kk-media/image/upload/v1752877058/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-pipeline-editor-visualization.jpg)
</Frame>

## Auto DevOps Variables

The default template defines many variables you can override:

| Variable                    | Purpose                                | Example Default              |
| --------------------------- | -------------------------------------- | ---------------------------- |
| `AUTO_BUILD_IMAGE_VERSION`  | Build image version                    | `v1.51.0`                    |
| `AUTO_DEPLOY_IMAGE_VERSION` | Deploy image version                   | `v2.80.1`                    |
| `DAST_VERSION`              | Version of DAST scans                  | `4`                          |
| `SECURE_ANALYZERS_PREFIX`   | Registry prefix for security analyzers | `$CI_TEMPLATE_REGISTRY_HOST` |
| `POSTGRES_USER`             | Username for review app database       | `user`                       |
| `POSTGRES_PASSWORD`         | Password for review app database       | `testing-password`           |

Override these under **Settings > CI/CD > Variables** or in your `.gitlab-ci.yml`.

## Disabling Unneeded Jobs

Disable specific Auto DevOps jobs by setting their variables to `"true"`:

```yaml theme={null}
variables:
  TEST_DISABLED: "true"
  CODE_QUALITY_DISABLED: "true"
  DEPENDENCY_SCANNING_DISABLED: "true"
  LICENSE_MANAGEMENT_DISABLED: "true"
  SAST_DISABLED: "true"
  PERFORMANCE_DISABLED: "true"
  BROWSER_PERFORMANCE_DISABLED: "true"
  REVIEW_DISABLED: "true"
  CONTAINER_SCANNING_DISABLED: "true"
```

See the [Auto DevOps variables documentation](https://docs.gitlab.com/ee/topics/autodevops/variables.html) for a complete list:

<Frame>
  ![The image shows a GitLab documentation page detailing CI/CD variables, job names, and descriptions for disabling jobs. The left sidebar lists various documentation topics, and the right side provides a table with job-related information.](https://kodekloud.com/kk-media/image/upload/v1752877059/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-ci-cd-variables-documentation.jpg)
</Frame>

## Full Example `.gitlab-ci.yml`

Combine the include and disabling variables to simplify your pipeline:

```yaml theme={null}
include:
  template: Auto-DevOps.gitlab-ci.yml

variables:
  DAST_DISABLED: "true"
  CODE_QUALITY_DISABLED: "true"
  DEPENDENCY_SCANNING_DISABLED: "true"
  LICENSE_MANAGEMENT_DISABLED: "true"
  SAST_DISABLED: "true"
  PERFORMANCE_DISABLED: "true"
  BROWSER_PERFORMANCE_DISABLED: "true"
  REVIEW_DISABLED: "true"
  CONTAINER_SCANNING_DISABLED: "true"
```

Commit and push to trigger a streamlined set of jobs:

<Frame>
  ![The image shows a GitLab pipeline interface with a series of jobs including build, test, and incremental rollout stages. The pipeline is currently running, and the jobs are organized by stage.](https://kodekloud.com/kk-media/image/upload/v1752877060/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-pipeline-jobs-interface.jpg)
</Frame>

## Running the Timed Rollout

After **build** and **test**, the pipeline moves through timed rollout steps (10%, 25%, 50%, 100%). Each step waits for the configured interval before proceeding.

<Frame>
  ![The image shows a GitLab pipeline interface with a customized AutoDevOps job in progress, displaying stages like build, test, and incremental rollout percentages.](https://kodekloud.com/kk-media/image/upload/v1752877061/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-pipeline-autodevops-job.jpg)
</Frame>

Before the 10% rollout, protected environments require manual approval:

<Frame>
  ![The image shows a GitLab interface with a job titled "timed rollout 10%" that has not been triggered yet. It includes options for managing jobs and viewing related information.](https://kodekloud.com/kk-media/image/upload/v1752877062/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-timed-rollout-job-interface.jpg)
</Frame>

Click **Run job** to start, and track progress:

<Frame>
  ![The image shows a GitLab pipeline interface with a job titled "timed rollout 10%" currently running. It includes details about the job's status, commit, and pipeline information.](https://kodekloud.com/kk-media/image/upload/v1752877063/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-timed-rollout-job-status.jpg)
</Frame>

Once complete, the next step (25%) begins automatically after the timer expires:

<Frame>
  ![The image shows a GitLab pipeline interface for a customized AutoDevOps job, displaying stages like build, test, and incremental rollout with various completion statuses.](https://kodekloud.com/kk-media/image/upload/v1752877065/notes-assetshttps://kodekloud.com/kk-media/image/upload/v1752877065/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-AutoDevOps-Customization/gitlab-pipeline-autodevops-job-2.jpg)
</Frame>

Under the hood, Auto DevOps runs:

```bash theme={null}
auto-deploy deploy canary $ROLLOUT_PERCENTAGE
```

## Inspecting the Deployment

Verify canary and stable pods using the Kubernetes CLI:

```bash theme={null}
kubectl -n production get pods
