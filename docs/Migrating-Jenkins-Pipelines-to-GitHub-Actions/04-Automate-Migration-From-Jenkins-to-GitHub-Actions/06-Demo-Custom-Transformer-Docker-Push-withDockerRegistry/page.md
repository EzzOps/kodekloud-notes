# This item has no matching transformer
# - withDockerRegistry:
#   - key: credentialsId
#     value:
#       isLiteral: true
#       value: docker-hub-credentials
#   - key: url
#     value:
#       isLiteral: true
Trivy_Vulnerability_Scanner:
  name: Trivy Vulnerability Scanner
  runs-on:
    - ubuntu-latest
  needs: Build_Publish_Image
```

Identifying which `sh` steps contain Docker commands

* We ran a dry-run with a helper transformer that prints each `sh` identifier to locate the embedded Docker command.

Command used:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers helper-transformer.rb
```

Example `sh` identifier JSON for the Docker build:

```json theme={null}
{
  "name": "sh",
  "arguments": [
    {
      "key": "script",
      "value": {
        "isLiteral": true,
        "value": "docker build -t siddharth67/solar-system:$GIT_COMMIT ."
      }
    }
  ]
}
```

This confirmed the `docker build` command appears in the `sh` identifier and is transformable.

Custom `sh` transformer: extract and convert the `docker build`

* We added a transformer that targets `sh` nodes and only transforms steps that match the specific `docker build` invocation for this repository/image.
* The transformer substitutes hard-coded values with GitHub Actions variables, e.g. `siddharth67` → `vars.DOCKERHUB_USERNAME`, `solar-system` → `vars.IMAGE_NAME`, and `$GIT_COMMIT` → `github.sha`.

Add this Ruby transformer (example name: `ss-pipeline-transformer.rb`):

```ruby theme={null}
transform "sh" do |item|
  # Safely extract the shell script from the 'sh' identifier
  script = item.dig("arguments", 0, "value", "value").to_s

  if script.include?("docker build") && script.include?("siddharth67/solar-system")
    # Replace hard-coded values with GitHub Actions variables
    converted_script = script
      .gsub('siddharth67', '${{ vars.DOCKERHUB_USERNAME }}')
      .gsub('solar-system', '${{ vars.IMAGE_NAME }}')
      .gsub('$GIT_COMMIT', '${{ github.sha }}')

    # Return a GitHub Actions step
    {
      "name" => "Build Docker image",
      "run" => converted_script,
      "shell" => "bash"
    }

  else
    # Skip transformation for certain known commands already handled elsewhere
    next nil if item.dig("arguments", 0, "value", "value") == "npm test"
  end
end
```

Notes on the transformer

* Uses `dig` to safely navigate nested JSON and extract the script string.
* Matches only the intended `docker build` for this repository to avoid false positives.
* Substitutions convert Jenkins-specific/ hard-coded values to GitHub Actions expressions: use `vars.DOCKERHUB_USERNAME`, `vars.IMAGE_NAME`, and `github.sha`.
* The transformer returns a hash that becomes a GitHub Actions step with `name`, `run`, and `shell`.

Re-running the dry-run (with this transformer)

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers ss-pipeline-transformer.rb
```

Result: The Build Publish Image job now contains a step named "Build Docker image" with the `docker build` command converted and variables substituted (no hard-coded credentials or commit tags remain).

Best-practice mapping (quick reference)

| Jenkins construct                                             |                                                                              GitHub Actions equivalent | Notes / Example                                                            |
| ------------------------------------------------------------- | -----------------------------------------------------------------------------------------------------: | -------------------------------------------------------------------------- |
| `sh 'docker build -t owner/repo:$GIT_COMMIT .'`               |       `run: docker build -t ${{ vars.DOCKERHUB_USERNAME }}/${{ vars.IMAGE_NAME }}:${{ github.sha }} .` | Replace `owner`, `repo`, and Jenkins variables with `vars` / `github.sha`. |
| `withDockerRegistry(credentialsId: 'docker-hub-credentials')` | `uses: docker/login-action@v2` or `` `run: echo ${{ secrets.DOCKERHUB_TOKEN }} \| docker login ...` `` | Requires mapping Jenkins credentials to GitHub Secrets.                    |
| `publishHTML([...])`                                          |                                         Upload artifact or use a GH Action that publishes HTML reports | Use `actions/upload-artifact` or a static-site publish workflow.           |

<Callout icon="lightbulb">
  Define the repository or organization variables used by the transformer (for example, `vars.DOCKERHUB_USERNAME` and `vars.IMAGE_NAME`) in your GitHub repository or organization settings so the workflow can access them at runtime. For more, see [Using variables in GitHub Actions](https://docs.github.com/en/actions/using-workflows/variables).
</Callout>

Warning about credentials and registry authentication

<Callout icon="warning">
  Do not store credentials directly in workflows. Map Jenkins `credentialsId` to GitHub Secrets (e.g. `secrets.DOCKERHUB_USERNAME` and `secrets.DOCKERHUB_TOKEN`) or use `docker/login-action` with secure inputs. You will need a separate transformer for `withDockerRegistry` to perform this mapping correctly.
</Callout>

What remains to be done

* Transform `withDockerRegistry` blocks:
  * Create a transformer that recognizes `withDockerRegistry` and emits a GitHub Actions step to authenticate to the container registry (for example, `docker/login-action`), mapping Jenkins credentials to `secrets.*`.
* Ensure Trivy/report publishing:
  * If Trivy steps are in `sh`, they can be transformed similarly. Add steps to upload artifacts or publish HTML reports (e.g., `actions/upload-artifact`).
* Validate end-to-end:
  * Run the importer in dry-run first, then with real output, and test the generated workflow in a branch.

References

* Jenkinsfile syntax: [https://www.jenkins.io/doc/book/pipeline/jenkinsfile/](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
* GitHub Actions expressions and variables: [https://docs.github.com/en/actions/learn-github-actions/expressions](https://docs.github.com/en/actions/learn-github-actions/expressions)
* docker/login-action: [https://github.com/docker/login-action](https://github.com/docker/login-action)
* Trivy: [https://aquasecurity.github.io/trivy/latest/](https://aquasecurity.github.io/trivy/latest/)

That's it — we converted the embedded `docker build` in `sh` into a proper GitHub Actions `run` step and replaced hard-coded values with workflow variables. Next step: implement a transformer to convert `withDockerRegistry` into secure GitHub Actions authentication and finalize the push flow.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/f84d4317-bb2f-4d8e-8b18-ce4eec765ecf" />
</CardGroup>


# Demo Custom Transformer Docker Push withDockerRegistry

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-Docker-Push-withDockerRegistry/page

Shows how to transform Jenkins withDockerRegistry and docker push into GitHub Actions steps using docker/login-action and docker/build-push-action with variable substitution.

This article demonstrates how to create a custom transformer that converts Jenkins' `withDockerRegistry` step into equivalent GitHub Actions steps (Docker login + build/push). In Jenkins, `withDockerRegistry` provides Docker credentials so the pipeline can log in (e.g., to Docker Hub) and run `docker push`. When migrating to GitHub Actions, the common equivalent is `docker/login-action` (authentication) and `docker/build-push-action` (build + push), or a separate `docker build` step with a subsequent push.

What you'll learn

* How `withDockerRegistry` maps to GitHub Actions.
* How to extract the `docker push` command from the imported Jenkins JSON.
* How to write a concise custom transformer (example in Ruby) that emits Actions steps with proper variable substitution.
* How to prepare GitHub repository variables and secrets needed by the converted workflow.

## Relevant Jenkins pipeline excerpt

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Code Coverage') {
      agent {
        docker {
          image 'node:24'
          args '-u root:root'
        }
      }
      steps {
        catchError(buildResult: 'SUCCESS', message: 'Oops! it will be fixed in future releases', stageResult: 'UNSTABLE') {
          sh 'npm run coverage'
        }
        publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'coverage'])
      }
    }

    stage('Build Publish Image') {
      steps {
        sh 'docker build -t siddharth67/solar-system:$GIT_COMMIT .'
        withDockerRegistry(credentialsId: 'docker-hub-credentials', url: "") {
          sh 'docker push siddharth67/solar-system:$GIT_COMMIT'
        }
      }
    }

    stage('Trivy Vulnerability Scanner') {
      steps {
        sh '''trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet'''
        sh '''trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" -o trivy-report.html'''
        publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: './', reportFiles: 'trivy-report.html', reportName: 'Trivy Report'])
      }
    }
  }
}
```

## What `withDockerRegistry` does

* Supplies Docker credentials (from Jenkins credentials store) to allow `docker push`.
* For migration, the natural mapping in GitHub Actions is:
  * `docker/login-action` — to authenticate to a registry.
  * `docker/build-push-action` — to build and push images (can also be split into `docker build` + `docker push`).

## Marketplace actions and references

Search the GitHub Actions Marketplace for Docker-related actions. Typical choices:

* `docker/login-action@v3` — login to Docker Hub (or other registries).
* `docker/build-push-action@v6` — build and push images.

<Frame>
  <img alt="A dark-themed screenshot of the GitHub Marketplace Actions page with a search for &#x22;docker.&#x22; The page shows the &#x22;Enhance your workflow with extensions&#x22; header and multiple Docker-related action cards like &#x22;Build and push Docker images&#x22; and &#x22;Docker Login.&#x22;" />
</Frame>

Useful links

* docker/login-action: [https://github.com/docker/login-action](https://github.com/docker/login-action)
* docker/build-push-action: [https://github.com/docker/build-push-action](https://github.com/docker/build-push-action)
* Trivy: [https://aquasecurity.github.io/trivy/latest/](https://aquasecurity.github.io/trivy/latest/)

## Minimal GitHub Actions job example

If you need to both build and push in one job, the typical pattern is:

```yaml theme={null}
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
```

If your Jenkins pipeline already performed `docker build` earlier, you can issue only the login and `docker push` steps (or use `build-push-action` to only push an already built image).

## What the importer produced (problem)

The importer emitted a job with an unrecognized `withDockerRegistry` node in the Jenkins JSON. The children included an `sh` step with `docker push <image>:$GIT_COMMIT`, but no existing transformer handled it — so we create one.

Example simplified JSON snippet the transformer receives

```yaml theme={null}
name: Build Publish Image
runs-on:
  - ubuntu-latest
needs: Code_Coverage
steps:
  - name: checkout
    uses: actions/checkout@v4.1.0
  - name: Build Docker image
    run: docker build -t ${{ vars.DOCKERHUB_USERNAME }}/${{ vars.IMAGE_NAME }}:${{ github.sha }} .
    shell: bash
