# .github/workflows/publish-npm.yml
name: Publish npm Package
on:
  push:
    branches: [ main ]
jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
          registry-url: 'https://npm.pkg.github.com/'

      - name: Publish to GitHub Packages
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Build and Push a Docker Image

```yaml theme={null}
# .github/workflows/docker-publish.yml
name: Build and Push Docker Image
on:
  push:
    tags: [ 'v*' ]
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push
        run: |
          docker build -t ghcr.io/${{ github.repository }}/my-app:latest .
          docker push ghcr.io/${{ github.repository }}/my-app:latest
```

#### Deploy a Maven Artifact

```yaml theme={null}
# .github/workflows/maven-deploy.yml
name: Publish Maven Artifacts
on:
  push:
    tags: [ 'v*' ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Java
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '11'
          server-id: github
          settings-path: ${{ github.workspace }}

      - name: Deploy to GitHub Packages
        run: mvn deploy
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Push a .NET NuGet Package

```yaml theme={null}
# .github/workflows/nuget-publish.yml
name: Publish NuGet Package
on:
  push:
    branches: [ main ]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up .NET
        uses: actions/setup-dotnet@v2
        with:
          dotnet-version: '6.x'

      - name: Push to GitHub Packages
        run: |
          dotnet nuget push MyPackage.nupkg \
            --api-key ${{ secrets.GITHUB_TOKEN }} \
            --source "https://nuget.pkg.github.com/${{ github.repository_owner }}/index.json"
```

## Authentication

All of these workflows rely on the built-in `GITHUB_TOKEN`. This secret is automatically created for each workflow run and scoped to the repository:

* Grants read/write access to GitHub Packages.
* Requires no extra setup or manual credential management.
* Automatically expires when the workflow completes.

<Callout icon="lightbulb">
  If you need to publish packages across multiple repositories or organizations, consider using a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with the appropriate scopes.
</Callout>

## Links and References

* [GitHub Packages Documentation](https://docs.github.com/packages)
* [GitHub Actions Documentation](https://docs.github.com/actions)
* [npm Registry](https://www.npmjs.com/)
* [RubyGems](https://rubygems.org/)
* [Apache Maven](https://maven.apache.org/)
* [Docker Hub](https://hub.docker.com/)
* [NuGet Gallery](https://www.nuget.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/c8d70bad-a81b-4bf2-bfbf-55dac325686c" />
</CardGroup>


# Github Action Expressions

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Github-Action-Expressions/page

This article explores using expressions in GitHub Actions to control execution flow of steps and jobs.

This article explores how to use expressions in [GitHub Actions][gh-actions-expressions] to control the execution flow of steps and jobs. We cover:

* Conditional execution with `if`
* Ignoring failures using `continue-on-error`
* Built-in status check functions

## Sample Workflow

The following workflow runs tests on both Ubuntu and Windows, uploads a report to AWS S3 (failing intentionally), and then deploys if the report step completes.

```yaml theme={null}
on: push

jobs:
  testing:
    strategy:
      matrix:
        os: ['windows-latest', 'ubuntu-latest']
    runs-on: ${{ matrix.os }}
    steps:
      - name: Testing on Ubuntu
        run: |
          export apikey=3$CuR3-t0k3N
          echo "Running Tests on Ubuntu..."

      - name: Testing on Windows
        run: |
          Set-Variable -Name "apikey" -Value "3$CuR3-t0k3N"
          echo "Running Tests on Windows..."

  reports:
    needs: testing
    runs-on: ubuntu-latest
    steps:
      - name: Upload Report to AWS S3
        run: |
          echo "Uploading reports..." && exit 1

  deploy:
    needs: reports
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Application
        run: echo "Deploying application..."
```

In this example:

* Ubuntu tests pass.
* Windows commands fail on Linux, causing the `testing` job to abort.
* As a result, `reports` and `deploy` are skipped.

## Conditional Execution with `if`

Use `if` to run steps or jobs only when a condition is met. You can reference contexts like `runner.os`, literals, and functions:

```yaml theme={null}
jobs:
  testing:
    strategy:
      matrix:
        os: ['windows-latest', 'ubuntu-latest']
    runs-on: ${{ matrix.os }}
    steps:
      - name: Testing on Ubuntu
        if: runner.os == 'Linux'
        run: |
          export apikey=3$CuR3-t0k3N
          echo "Running Tests on Ubuntu..."

      - name: Testing on Windows
        if: runner.os == 'Windows'
        run: |
          Set-Variable -Name "apikey" -Value "3$CuR3-t0k3N"
          echo "Running Tests on Windows..."
```

Each step only executes on its intended OS, preventing unsupported commands from running.

## Ignoring Failures with `continue-on-error`

By default, a failed step aborts its job. To let a job succeed even if a step fails, set `continue-on-error: true`. Downstream jobs defined with `needs` will still run if the parent job completes.

<Callout icon="lightbulb">
  The `continue-on-error` attribute applies at the **step** level, not at the job level.
</Callout>

```yaml theme={null}
on: push

jobs:
  testing:
    strategy:
      matrix:
        os: ['windows-latest', 'ubuntu-latest']
    runs-on: ${{ matrix.os }}
    steps:
      - name: Testing on Linux
        if: runner.os == 'Linux'
        run: |
          export apikey=3$CuR3-t0k3N
          echo "Running Tests on Ubuntu..."

      - name: Testing on Windows
        if: runner.os == 'Windows'
        run: |
          Set-Variable -Name "apikey" -Value "3$CuR3-t0k3N"
          echo "Running Tests on Windows..."

  reports:
    needs: testing
    runs-on: ubuntu-latest
    steps:
      - name: Upload Report to AWS S3
        run: |
          echo "Uploading reports..." && exit 1
        continue-on-error: true

  deploy:
    needs: reports
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Application
        run: echo "Deploying application..."
```

Here, even though the upload step fails, `reports` completes successfully and triggers the `deploy` job.

## Status Check Functions

GitHub Actions provides built-in functions to inspect previous outcomes:

| Function      | Returns `true` when…                    |
| ------------- | --------------------------------------- |
| `success()`   | all prior steps and jobs have succeeded |
| `failure()`   | any prior step or job has failed        |
| `cancelled()` | the workflow run was cancelled          |
| `always()`    | always (useful for cleanup steps)       |

Example:

```yaml theme={null}
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build

      - name: Test
        run: npm test
        if: success()

      - name: Notify on Failure
        run: echo "Tests failed!"
        if: failure()

      - name: Cleanup
        run: echo "Cleaning up environment..."
        if: always()
```

These functions help you create resilient, conditional workflows that adapt to your CI/CD pipeline’s status.

## Links and References

* [GitHub Actions Expressions][gh-actions-expressions]
* [GitHub Actions Contexts][gh-actions-contexts]
* [AWS S3][aws-s3]
* [Workflow Syntax for GitHub Actions][gh-actions-syntax]

[gh-actions-expressions]: https://docs.github.com/en/actions/learn-github-actions/expressions

[gh-actions-contexts]: https://docs.github.com/en/actions/learn-github-actions/contexts

[gh-actions-syntax]: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

[aws-s3]: https://aws.amazon.com/s3/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/847fd530-9da2-4011-b69d-2d04ce128dbd" />
</CardGroup>
