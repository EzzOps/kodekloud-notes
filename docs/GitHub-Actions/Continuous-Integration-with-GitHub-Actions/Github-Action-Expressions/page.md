# Run actions/cache@v3
Cache Size: ~7 MB (702593 B)
/usr/bin/tar -xf .../cache.tzst ...
Cache restored successfully
Cache restored from key: Linux-node-modules-6224ef692577e18835ac17794c9dc34656c2d8679585a7255cee00452bc1ef7

# Run npm install
up to date, audited 365 packages in 965ms
...
```

Install times drop from 10–20s to \~1s.

<Frame>
  ![The image shows a GitHub Actions workflow interface, displaying the details of a unit testing job for a project named "solar-system," including steps like caching NPM dependencies and installing dependencies.](https://kodekloud.com/kk-media/image/upload/v1752876494/notes-assets/images/GitHub-Actions-Cache-Node-Dependencies/github-actions-solar-system-testing-workflow.jpg)
</Frame>

## Conclusion

By caching `node_modules` with [actions/cache](https://github.com/actions/cache), you’ll see faster CI runs and reduced compute costs. In our next article, we’ll cover advanced cache invalidation strategies when dependencies change.

## Links and References

* [actions/cache on GitHub](https://github.com/actions/cache)
* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Setup Node.js Action](https://github.com/actions/setup-node)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/cd45c292-41c6-49af-90e3-8b714e17235c" />
</CardGroup>


# Github Action Expressions

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Github-Action-Expressions/page

This guide explores advanced expression syntax for GitHub Actions to enhance CI/CD pipeline flexibility.

In this guide, we’ll dive into advanced expression syntax for GitHub Actions to build more flexible CI/CD pipelines. You’ll learn how to:

* Control step and job execution with `if` conditions
* Allow workflows to continue after failures using `continue-on-error`
* Inspect outcomes with status-check functions (`success()`, `failure()`, etc.)

Before we explore expressions, let’s review a sample workflow to see common pitfalls.

***

## Sample Workflow Overview

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
          export apikey=$3CuR3-t0k3N
          echo "Running Tests ... ..."
      - name: Testing on Windows
        run: |
          Set-Variable -Name "apikey" -Value "$3CuR3-t0k3N"
          echo "Running Tests ... ..."
  reports:
    needs: testing
    runs-on: ubuntu-latest
    steps:
      - name: Upload Report to AWS S3
        run: echo "Uploading reports ... ..." && exit 1
  deploy:
    runs-on: ubuntu-latest
    needs: reports
```

**Jobs Breakdown**

1. **testing**: Runs tests on both Windows and Ubuntu, setting an `apikey`.
2. **reports**: Uploads test results to [AWS S3](https://aws.amazon.com/s3) and deliberately fails.
3. **deploy**: Depends on the `reports` job.

Because the Ubuntu runner uses Bash’s `export` (and PowerShell commands won’t execute on Linux), the `testing` job fails for one matrix entry, blocking all downstream jobs.

<Callout icon="triangle-alert">
  Storing secrets directly in your workflow can expose them in logs. Use [GitHub Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets) instead.
</Callout>

***

## Core Expressions in GitHub Actions

Expressions let you dynamically control when a step or job runs. There are three main categories:

1. Conditional execution with `if`
2. Error handling with `continue-on-error`
3. Status inspection functions (`success()`, `failure()`, etc.)

***

### 1. Conditional Execution with `if`

Use `if` to evaluate expressions based on contexts, comparisons, and built-in functions:

```yaml theme={null}
steps:
  - name: Run unit tests only on Linux
    if: runner.os == 'Linux'
    run: ./run-tests.sh

jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: ./deploy.sh
```

* `runner.os`, `github.ref`, and other [contexts](https://docs.github.com/actions/learn-github-actions/contexts) provide metadata.
* Combine expressions using `&&`, `||`, `==`, `!=`, and functions.

***

### 2. Allowing Failures with `continue-on-error`

By default, a failed step stops its job. Enable `continue-on-error` to proceed even if a step or job fails:

```yaml theme={null}
