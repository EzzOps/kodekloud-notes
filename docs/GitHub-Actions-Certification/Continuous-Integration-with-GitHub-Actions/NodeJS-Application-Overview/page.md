# 1. Update your feature branch
git pull

# 2. Install nodemon and update lockfile
npm install nodemon --save

# 3. Review changes
git diff package.json package-lock.json

# 4. Commit and push
git add package.json package-lock.json
git commit -m "Add nodemon dependency"
git push
```

After this, your `package.json` dependencies look like:

```json theme={null}
{
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.18.2",
    "mocha-junit-reporter": "2.2.1",
    "mongoose": "5.13.20",
    "nodemon": "^3.0.1",
    "nyc": "^15.1.0"
  }
}
```

And `package-lock.json` is updated, producing a new hash.

<Callout icon="lightbulb">
  Using `npm install --save` updates both `package.json` and `package-lock.json`, ensuring the cache key changes automatically.
</Callout>

## Workflow Configuration

Include these steps in your `.github/workflows/ci.yml`:

| Step                   | Action                       | Description                                         |
| ---------------------- | ---------------------------- | --------------------------------------------------- |
| Setup Node.js          | uses: actions/setup-node\@v3 | Installs Node.js for the specified version.         |
| Cache NPM dependencies | uses: actions/cache\@v3      | Caches `node_modules` keyed by the lockfile’s hash. |
| Install Dependencies   | run: npm install             | Restores or installs NPM packages.                  |

```yaml theme={null}
- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: ${{ matrix.nodejs_version }}

- name: Cache NPM dependencies
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-modules-${{ hashFiles('package-lock.json') }}

- name: Install Dependencies
  run: npm install
```

Because the cache key is based on `hashFiles('package-lock.json')`, any modification to your lockfile results in a cache miss.

## Triggering the Workflow and Cache Invalidation

Once you push the updated lockfile:

1. **Cache NPM dependencies**: No existing cache matches the new key, so the step falls back to installing from npm.
2. **Install Dependencies**: `npm install` populates `node_modules`.
3. **Upload Cache**: One job uploads the newly generated cache.
4. **Parallel Jobs**: Other jobs may see “Failed to save cache” if they attempt an upload after the first; this is expected.

<Frame>
  ![The image shows a GitHub Actions workflow interface for a project named "solar-system," displaying the status of unit testing jobs on different environments, with a focus on caching NPM dependencies.](https://kodekloud.com/kk-media/image/upload/v1752875952/notes-assets/images/GitHub-Actions-Certification-Invalidate-Cache/github-actions-solar-system-workflow.jpg)
</Frame>

<Callout icon="triangle-alert">
  In parallel builds, only the first job to upload the cache succeeds. Subsequent jobs will skip uploading the same key.
</Callout>

## Inspecting Cache Behavior Across Jobs

During a run, you might see logs like:

```text theme={null}
Cache not found for input key, proceeding to npm install...
```

or

```text theme={null}
Uploading cache...
/usr/bin/tar --posix -cf cache.tzst --exclude cache.tzst -P -C /home/runner/work/solar-system/solar-system --files-from manifest.txt --use-compress-program=zstdmt
```

<Frame>
  ![The image shows a GitHub Actions workflow interface with a list of jobs, including unit testing and code coverage, indicating successful completion of tasks. The highlighted section is "Cache NPM dependencies" under a unit testing job.](https://kodekloud.com/kk-media/image/upload/v1752875953/notes-assets/images/GitHub-Actions-Certification-Invalidate-Cache/github-actions-workflow-unit-testing-cache.jpg)
</Frame>

This demonstrates how one job restores or saves the cache, while others detect it’s already stored and skip.

## Viewing Saved Caches

You can review cache details in the GitHub Actions UI under the workflow run or by examining the tar logs. Example:

<Frame>
  ![The image shows a GitHub Actions interface displaying cache details for a project, including cache names, sizes, and usage times.](https://kodekloud.com/kk-media/image/upload/v1752875954/notes-assets/images/GitHub-Actions-Certification-Invalidate-Cache/github-actions-cache-details-interface.jpg)
</Frame>

## Conclusion

By hashing `package-lock.json` in your cache key:

1. Each dependency update generates a new hash.
2. The cache restore step misses on outdated keys.
3. Dependencies are installed from scratch.
4. A fresh cache is uploaded for subsequent runs.

## Links and References

* [actions/cache@v3](https://github.com/actions/cache)
* [actions/setup-node@v3](https://github.com/actions/setup-node)
* [hashFiles function](https://docs.github.com/en/actions/learn-github-actions/expressions#hashfiles)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/1426e076-2d73-49e0-81a3-862d245b7840" />
</CardGroup>


# NodeJS Application Overview

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/NodeJS-Application-Overview/page

This article provides an overview of setting up a minimal Node.js application and preparing for a custom GitHub Action workflow.

Node.js is a powerful, open-source JavaScript runtime built on Chrome’s V8 engine. It enables you to execute JavaScript on the server side, allowing you to use a single language across your entire stack. In this guide, we’ll explore the basics of a minimal Node.js project and prepare for creating a custom GitHub Action workflow.

<Callout icon="lightbulb">
  Node.js runs on Windows, macOS, and most Linux distributions. Ensure you’re using a supported version for compatibility.
</Callout>

## Prerequisites

Verify your installed versions:

```bash theme={null}
$ node -v
v18.16.0

$ npm -v
9.8.1
```

> You should have Node.js (v14+) and npm installed.\
> If not, download them from [Node.js Official Site][nodejs].

## Project Structure

A minimal Node.js project typically includes these elements:

| Item           | Description                                                           |
| -------------- | --------------------------------------------------------------------- |
| package.json   | Metadata: name, version, dependencies, and custom scripts.            |
| node\_modules/ | Automatically generated by `npm install`; contains all your packages. |
| index.js       | Entry point for your application—your core business logic.            |
| test.js        | Unit tests and integration tests for your functions and endpoints.    |

## Installing Dependencies

Install all required libraries listed in `package.json`:

```bash theme={null}
npm install
```

<Callout icon="lightbulb">
  This command reads `package.json` and populates the `node_modules/` directory with every dependency.
</Callout>

## Running Tests

Execute your tests as defined in the `test` script of `package.json`:

```bash theme={null}
npm test
```

A successful run will output results and confirm that all test cases pass.

## Starting the Application

Launch the server using the `start` script:

```bash theme={null}
npm start
```

By default, the app listens on port 3000. Verify the endpoint:

```bash theme={null}
curl http://localhost:3000/hello
