# This item has no matching transformer
# - withDockerRegistry:
#   - key: credentialsId
#     value:
#       isLiteral: true
#       value: docker-hub-credentials
#   - key: url
#     value:
#       isLiteral: true
#       value: ''
```

## Transformer goals

The transformer should:

1. Extract the `docker push` command from the child `sh` step.
2. Parse the image name and tag from that push command.
3. Replace Jenkins-specific variables and hardcoded values:
   * `$GIT_COMMIT` → `${{ github.sha }}`
   * Hardcoded username/image → use GitHub Actions variables like `${{ vars.DOCKERHUB_USERNAME }}` and `${{ vars.IMAGE_NAME }}`
4. Emit steps for:
   * Docker login (`docker/login-action@v3`)
   * Build and push (`docker/build-push-action@v6`) or a push-only step if the image is already built

Mapping summary (Jenkins → GitHub Actions)

| Jenkins step                       | GitHub Actions equivalent                                   | Notes                                                                                  |
| ---------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `withDockerRegistry` (credentials) | `docker/login-action@v3`                                    | Use repository-level `vars` and `secrets` to store username and password respectively. |
| `docker build` + `docker push`     | `docker/build-push-action@v6`                               | Can both build and push. If build already exists, you can run push only.               |
| Jenkins env `$GIT_COMMIT`          | `${{ github.sha }}`                                         | Use GitHub predefined contexts.                                                        |
| Hardcoded user/image               | `${{ vars.DOCKERHUB_USERNAME }}` / `${{ vars.IMAGE_NAME }}` | Add as repo variables for reuse.                                                       |

## Example custom transformer (Ruby) — concise

This Ruby transformer (for the importer’s transformer DSL) extracts the push command, rewrites variables, and emits Actions steps for login and build+push:

```ruby theme={null}
transform "withDockerRegistry" do |item|
  # Extract the push command from the child step
  push_command = item["children"].first["arguments"].find { |arg| arg["key"] == "script" }["value"]["value"]
  # Get the last token from "docker push <image:tag>"
  image_tag = push_command.split(' ').last # => "siddharth67/solar-system:$GIT_COMMIT"

  # Build the GitHub Actions steps
  [
    {
      "name" => "Login to Docker Hub",
      "uses" => "docker/login-action@v3",
      "with" => {
        "username" => "${{ vars.DOCKERHUB_USERNAME }}",
        "password" => "${{ secrets.DOCKERHUB_PASSWORD }}"
      }
    },
    {
      "name" => "Build and push",
      "uses" => "docker/build-push-action@v6",
      "with" => {
        "push" => true,
        # Substitute Jenkins variables/hardcoded names to GitHub Actions variables
        "tags" => image_tag.gsub('$GIT_COMMIT', '${{ github.sha }}')
                           .gsub('siddharth67', '${{ vars.DOCKERHUB_USERNAME }}')
                           .gsub('solar-system', '${{ vars.IMAGE_NAME }}')
      }
    }
  ]
end
```

Notes about the transformer

* The transformer replaces Jenkins credential references (`credentialsId`) with GitHub Actions variables and secrets:
  * `username` → `${{ vars.DOCKERHUB_USERNAME }}`
  * `password` → `${{ secrets.DOCKERHUB_PASSWORD }}`
  * `image name` → `${{ vars.IMAGE_NAME }}`
* If the importer already produced an earlier `docker build` step, you can emit a push-only action or leave the build step and use `build-push-action` in push-only mode.

## Resulting GitHub Actions job (after transformer)

```yaml theme={null}
name: Code Coverage HTML Report
path: coverage/lcov-report

Build Publish Image:
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
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: "${{ vars.DOCKERHUB_USERNAME }}"
        password: "${{ secrets.DOCKERHUB_PASSWORD }}"
    - name: Build and push
      uses: docker/build-push-action@v6
      with:
        push: true
        tags: "${{ vars.DOCKERHUB_USERNAME }}/${{ vars.IMAGE_NAME }}:${{ github.sha }}"

Trivy_Vulnerability_Scanner:
  name: Trivy Vulnerability Scanner
  runs-on:
    - ubuntu-latest
  needs: Build_Publish_Image
  steps:
    - name: checkout
      uses: actions/checkout@v4.1.0
```

## Run the importer (dry-run and migrate)

Dry-run (inspect generated workflows):

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers ss-pipeline-transformer.rb
```

Example dry-run output:

```bash theme={null}
[2025-05-23 10:42:08] Output file(s):
[2025-05-23 10:42:08] tmp/dry-run/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
```

To migrate and create a PR:

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/jenkins-demo-org/solar-system \
  --output-dir tmp/migrate \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --custom-transformers ss-pipeline-transformer.rb
```

Example migrate output:

```text theme={null}
[2025-05-23 10:43:11] Pull request: 'https://github.com/jenkins-demo-org/solar-system/pull/5'
```

## Add required repository variables and secrets

Before merging the PR and running workflows, create the required repository-level variables and secrets.

Recommended repository variables and secrets

| Name                 | Type     | Purpose                                                  | Example value  |
| -------------------- | -------- | -------------------------------------------------------- | -------------- |
| `DOCKERHUB_USERNAME` | variable | Docker Hub username used in tags                         | `siddharth67`  |
| `IMAGE_NAME`         | variable | Image repository name used in tags                       | `solar-system` |
| `DOCKERHUB_PASSWORD` | secret   | Docker Hub password (or token) for `docker/login-action` | —              |

Add them in the repository Settings → Actions → Secrets and variables. After creation, they will appear in the repository's Actions > Secrets and variables settings.

<Frame>
  <img alt="A screenshot of a GitHub repository Settings page open to &#x22;Actions secrets / New secret,&#x22; with the Name field filled as &#x22;DOCKERHUB_PASSWORD&#x22; and the Secret textbox empty. The left sidebar shows repository settings and code/automation options." />
</Frame>

Confirm the variables and secrets are visible in Settings:

<Frame>
  <img alt="A dark-themed screenshot of a GitHub repository &#x22;Actions secrets and variables&#x22; settings page showing environment and repository variables (e.g., DOCKERHUB_USERNAME, IMAGE_NAME, MONGO_USERNAME). The left sidebar shows repository settings sections like Branches, Actions, Webhooks, and Secrets and variables." />
</Frame>

## Merge the PR and verify the workflow run

* Merge the pull request created by the importer.
* The merged workflow should trigger and perform: checkout, build (if configured), Docker login, and push to the registry (depending on the emitted job).

Pipeline run status (example):

<Frame>
  <img alt="A dark-themed CI/CD pipeline dashboard showing completed stages (Installing Dependencies, Unit Testing, Code Coverage, Build Publish Image, Trivy Vulnerability Scanner) with green checkmarks. The run status is &#x22;Success&#x22; and a Docker Build summary is visible below." />
</Frame>

Selected sanitized log excerpts

```bash theme={null}
# Docker build layers and outputs
#11 exporting to image
#11 writing image sha256:[SECRET_REDACTED] done
#11 naming to docker.io/siddharth67/solar-system:[AWS_SECRET_ACCESS_KEY] done

1 warning found (use docker --debug to expand):
- SecretsUsedInArgOrEnv: Do not use ARG or ENV instructions for sensitive data (ENV "MONGO_PASSWORD") (line 13)

# Docker login
Run docker/login-action@v3
11 Logging into Docker Hub...
12 Login Succeeded!

# docker/build-push-action process
Run docker/build-push-action@v6
/usr/bin/docker buildx build --iidfile /home/runner/work/_temp/.../build-iidfile.txt --tag siddharth67/solar-system:[AWS_SECRET_ACCESS_KEY] --push https://github.com/jenkins-demo-org/solar-system.git#[AWS_SECRET_ACCESS_KEY]
#10 pushing layer ... done
#10 DONE 5.7s
```

## Key takeaways

* Jenkins `withDockerRegistry` cleanly maps to `docker/login-action` + `docker/build-push-action` in GitHub Actions.
* Custom transformers should:
  * Extract `docker push` (or credential info) from the Jenkins JSON,
  * Substitute Jenkins variables with GitHub contexts and repository variables,
  * Emit the appropriate Actions steps (login and build/push or push-only).
* Create repository-level variables and secrets prior to running the workflow:
  * `DOCKERHUB_USERNAME` and `IMAGE_NAME` (variables).
  * `DOCKERHUB_PASSWORD` (secret).
* `docker/build-push-action` can both build and push—adjust emitted steps if a build is already present.

<Callout icon="lightbulb">
  Remember to create repository variables (`DOCKERHUB_USERNAME`, `IMAGE_NAME`) and repository secrets (`DOCKERHUB_PASSWORD`) before merging; otherwise the workflow will fail at runtime when trying to access those values.
</Callout>

We will cover how to migrate and map the Trivy vulnerability scanner stage into GitHub Actions in a follow-up article. Depending on your preference and requirements, the Trivy step can be implemented as a shell step or via a dedicated action.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/0346a9e2-c11b-486a-88df-df8206654bdf" />
</CardGroup>


# Demo Custom Transformer OWASP Dependency Check 1

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-OWASP-Dependency-Check-1/page

Migrating a Jenkins OWASP Dependency-Check step into a GitHub Actions workflow, inspecting Jenkins JSON with helper transformers and mapping CLI flags and publisher logic to Actions

In this lesson we inspect the OWASP Dependency-Check stage from a Jenkins pipeline and demonstrate how to migrate it into a GitHub Actions workflow. We'll:

* Review the migrated workflow that the importer produced.
* Identify Dependency-Check-related steps that lacked matching transformers.
* Use a helper transformer to print the Jenkins JSON for those steps.
* Map the Jenkins configuration to an appropriate GitHub Action that runs OWASP Dependency-Check.

Overview: the migrated workflow already contains environment variables and a runner configuration. The first job installs dependencies:

```yaml theme={null}
name: ci-pipeline-poll-scm
on:
env:
  MONGO_URI: mongodb+srv://supercluster.d83jj.mongodb.net/superData
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: "${{ secrets.mongo_db_password }}"
jobs:
  Installing_Dependencies:
    name: Installing Dependencies
    runs-on:
      ubuntu-latest
    container:
      image: node:24
      # This item has no matching transformer
      docker:
        key: args
        value:
          isLiteral: true
          value: "-u root:root"
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Install dependencies
        shell: bash
        run: npm install --no-audit
```

A dry-run of the actions-importer confirms the GitHub Actions workflow file was generated:

```bash theme={null}
root@jenkins in /home via 💎
> gh actions-importer dry-run jenkins --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ --output-dir tmp/dry-run --custom-transformers ss-pipeline-transformer.rb
[2025-05-22 18:54:06] Logs: 'tmp/dry-run-log/valet-20250522_185406.log'
[2025-05-22 18:54:07] Output file(s):
[2025-05-22 18:54:07] tmp/dry-run/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml

root@jenkins in /home via 💎 took 15s
```

The pipeline includes an NPM dependency audit job and an OWASP Dependency-Check job. Both migrated, but the Dependency-Check step (and the Dependency-Check publisher) had no matching transformers in the default migration. To implement a correct translation, inspect the JSON representation emitted by the importer for those Jenkins identifiers.

Use a helper transformer that prints the item JSON for multiple identifiers. For example:

```ruby theme={null}
transform "sleep", "dependencyCheck", "dependencyCheckPublisher" do |item|
  puts "JSON for identifier: #{item}"
end
```

Run the importer with the helper transformer to emit the JSON for the dependencyCheck and dependencyCheckPublisher items. Example (abridged) output:

```bash theme={null}
root@jenkins in /home via ◇
> gh actions-importer dry-run jenkins --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ --output-dir tmp/dry-run --custom-transformers ss-pipeline-transformer.rb --custom-transformers helper-transformer.rb
[2025-05-22 19:01:42] Logs: 'tmp/dry-run/log/valet-20250522-190142.log'
JSON for identifier: {"name"=>"dependencyCheck", "arguments"=>[{"key"=>"additionalArguments", "value"=>{"isLiteral"=>true, "value"=>"\n                                --scan './' \n                                --out ./ \n                                --format ALL \n                                --disableYarnAudit \n                                --prettyPrint --failOnCVSS 9"}}, {"key"=>"nvdCredentialsId", "value"=>{"isLiteral"=>true, "value"=>"owasp-dependency-check"}}, {"key"=>"odcInstallation", "value"=>{"isLiteral"=>true, "value"=>"OWASP-DepCheck-10"}}]}
JSON for identifier: {"name"=>"dependencyCheckPublisher", "arguments"=>[{"key"=>"failedTotalCritical", "value"=>{"isLiteral"=>true, "value"=>1}}, {"key"=>"pattern", "value"=>{"isLiteral"=>true, "value"=>"dependency-check-report.xml"}}, {"key"=>"stopBuild", "value"=>{"isLiteral"=>true, "value"=>true}}]}
[2025-05-22 19:01:43] Output file(s):
[2025-05-22 19:01:43] tmp/dry-run/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml

root@jenkins in /home via ◇ took 20s
```

The important fields from the emitted JSON for the `dependencyCheck` step are:

```json theme={null}
{
  "name": "dependencyCheck",
  "arguments": [
    {
      "key": "additionalArguments",
      "value": {
        "isLiteral": true,
        "value": "\n                                --scan './' \n                                --out './' \n                                --format 'ALL' \n                                --disableYarnAudit \n                                --prettyPrint --failOnCVSS 9"
      }
    },
    {
      "key": "nvdCredentialsId",
      "value": {
        "isLiteral": true,
        "value": "owasp-dependency-check"
      }
    },
    {
      "key": "odcInstallation",
      "value": {
        "isLiteral": true,
        "value": "OWASP-DepCheck-10"
      }
    }
  ]
}
```

Notes on the fields:

* `additionalArguments` contains the CLI flags passed to OWASP Dependency-Check. Key items: `--scan` (path), `--out` (output path), `--format` (report formats), and `--failOnCVSS 9` (fail build for CVSS ≥ 9).
* `nvdCredentialsId` and `odcInstallation` are Jenkins-specific entries referencing credentials and installer configurations used to accelerate NVD downloads or select a preinstalled Dependency-Check binary. These typically do not translate directly to ephemeral GitHub Actions runners.

CVSS score ranges are commonly used to gate failures. For reference, scores ≥ 9 are considered Critical, and scores between 7 and 8.9 are High:

<Frame>
  <img alt="A screenshot of a Google Images results page for &#x22;cvss scores,&#x22; showing many thumbnails and charts that display CVSS rating categories (Low, Medium, High, Critical) and score ranges. The browser is in a dark theme with search tabs visible across the top." />
</Frame>

<Callout icon="lightbulb">
  Jenkins' `nvdCredentialsId` and `odcInstallation` point to server-side configuration. When migrating to Actions, prefer a maintained Action or Docker image that packages Dependency-Check. If you need authenticated or mirrored NVD access, you'll need to provide credentials or a custom DB image to the Action.
</Callout>

Because GitHub Actions runners are ephemeral, the typical approach is to use an existing Action that runs Dependency-Check inside a Docker image. The GitHub Marketplace project dependency-check/dependency-check-action runs OWASP Dependency-Check in a container and exposes inputs for common CLI options.

A mapped GitHub Actions job that runs Dependency-Check might look like this:

```yaml theme={null}
on: [push]

jobs:
  depchecktest:
    runs-on: ubuntu-latest
    name: depcheck_test
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build project (example: Maven)
        run: mvn -B -DskipTests clean package

      - name: Run OWASP Dependency-Check
        uses: dependency-check/dependency-check-action@main
        id: depcheck
        with:
          project: 'test'
          path: '.'
          format: 'HTML'
          out: 'reports' # default is 'reports'
          args: >
            --failOnCVSS 9
            --enableRetired

      - name: Upload Dependency-Check report
        uses: actions/upload-artifact@v3
        with:
          name: depcheck-report
          path: ${{ github.workspace }}/reports
```

Key mapping decisions (Jenkins → GitHub Actions):

| Jenkins field / CLI flag              | Purpose                                | GitHub Action mapping / notes                                                                                           |
| ------------------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `--scan`                              | Path(s) to scan                        | Action input `path` (or pass via `args`)                                                                                |
| `--out`                               | Output directory                       | Action input `out`                                                                                                      |
| `--format`                            | Report format(s) (XML/HTML/ALL)        | Action input `format`                                                                                                   |
| `--failOnCVSS <score>`                | Fail build if highest CVSS ≥ score     | Pass as `args: --failOnCVSS 9` or implement follow-up checks                                                            |
| `nvdCredentialsId`, `odcInstallation` | Jenkins-specific credentials/installer | Usually omitted; the Action provides the runtime. Use custom runner or additional Action inputs for special NVD access. |

<Callout icon="warning">
  If your Jenkins pipeline relied on a pre-downloaded NVD DB (via `odcInstallation`) or private NVD credentials, you must plan how to supply that to Actions: either use a self-hosted runner with the database pre-populated or configure the Action to use an authenticated/mirrored NVD feed. Otherwise scans may be slower or behave differently.
</Callout>

Best practices when migrating Dependency-Check:

* Translate CLI flags (`--scan`, `--out`, `--format`, `--failOnCVSS`) into the Action's `with` inputs or into `args`.
* Upload generated reports with `actions/upload-artifact@v3` so they are available in the Actions UI.
* For "publisher" logic (e.g., "fail build if N critical vulnerabilities"), convert to `--failOnCVSS` or implement a follow-up step that parses the XML report and fails the job based on thresholds from the Jenkins `dependencyCheckPublisher` config.

Next steps (next lesson/article):

* Implement a custom transformer that extracts `format`, `failOnCVSS`, `--scan` path, and other important flags from the Jenkins JSON and emits a corresponding GitHub Actions step.
* Translate the Dependency-Check publisher config: detect the XML `pattern`, and translate the "fail build if N criticals" logic into Action flags or a separate report-parsing step.

Links and references:

* dependency-check Action (GitHub Marketplace): [https://github.com/dependency-check/dependency-check-action](https://github.com/dependency-check/dependency-check-action)
* GitHub Actions docs: [https://docs.github.com/actions](https://docs.github.com/actions)
* OWASP Dependency-Check: [https://owasp.org/www-project-dependency-check/](https://owasp.org/www-project-dependency-check/)
* CVSS information: [https://www.first.org/cvss/](https://www.first.org/cvss/)

That's all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/a4ed79cd-6c94-4da8-bd54-62ce3b609bb7" />
</CardGroup>
