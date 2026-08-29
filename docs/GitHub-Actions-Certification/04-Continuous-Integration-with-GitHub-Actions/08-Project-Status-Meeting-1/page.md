# Expected output: Hello World!
```

<Callout icon="triangle-alert">
  If port 3000 is in use, modify the port in `index.js` or set the `PORT` environment variable before starting.
</Callout>

***

With your Node.js application up and running, you’re now ready to integrate it into a custom GitHub Action. In the next section, we’ll build a workflow file that automates tests and deployment.

## Links and References

* [Node.js Official Site][nodejs]
* [npm Documentation][npm]
* [GitHub Actions][gh-actions]

[nodejs]: https://nodejs.org/

[npm]: https://docs.npmjs.com/

[gh-actions]: https://docs.github.com/actions/overview

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/02991ce3-eae5-4497-85f9-5ec12eaee9c3" />
</CardGroup>


# Project Status Meeting 1

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Project-Status-Meeting-1/page

This article outlines the approach for creating a GitHub Actions workflow for a Node.js application, detailing foundational tasks for CI/CD pipeline setup.

In this article, we’ll outline our approach for creating a robust [GitHub Actions](https://docs.github.com/en/actions) workflow tailored to a [Node.js](https://nodejs.org/) application. You’ll find an overview of each phase, the reasoning behind every step, and inline comments to clarify context and intent.

## Overview of Phase 1 Tasks

We’ve divided the initial work into four foundational tasks to set up our CI/CD pipeline:

| Task Number | Task Description                                                  |
| ----------- | ----------------------------------------------------------------- |
| 1           | Analyze the Node.js application structure                         |
| 2           | Identify dependencies and runtime requirements                    |
| 3           | Define DevOps requirements (testing frameworks, coverage metrics) |
| 4           | Prepare the repository for CI/CD integration                      |

<Callout icon="lightbulb">
  Completing these tasks ensures we have a clear understanding of the codebase and the prerequisites for automated workflows.
</Callout>

### Task 1: Analyze the Application Structure

* Review the directory layout (`src/`, `tests/`, `package.json`, etc.).
* Ensure all entry points and scripts are documented in `package.json`.

### Task 2: Identify Dependencies & Runtime

* Inspect `dependencies` and `devDependencies` in `package.json`.
* Verify Node.js engine compatibility in the `engines` field.

### Task 3: Define DevOps Requirements

* Choose a testing framework: [Jest](https://jestjs.io/) or [Mocha](https://mochajs.org/).
* Set coverage thresholds (e.g., 80% line coverage).
* Decide on linting rules (e.g., ESLint with Airbnb config).

### Task 4: Prepare for CI/CD

* Add or update `README.md` with build and test instructions.
* Store environment variables and secrets in GitHub repository settings.
* Create a skeleton `.github/workflows/ci.yml` file.

<Callout icon="triangle-alert">
  Never commit sensitive values (API keys, passwords) to the repo. Use GitHub Secrets for secure storage.
</Callout>

## Upcoming Workflow Implementation

After the initial setup, we’ll implement a modular GitHub Actions workflow with dedicated jobs for:

* Running unit tests
* Generating code coverage reports
* Building and publishing Docker images

Each job will be defined in its own section of the workflow file to maintain clarity and ease of maintenance.

## Next Steps

1. Conduct a code review of the Node.js application.
2. Confirm build scripts and environment variable usage in `package.json`.
3. Select and configure the testing framework.
4. Integrate a coverage tool like [Istanbul/NYC](https://istanbul.js.org/docs/advanced/nyc).
5. Develop GitHub Actions jobs for:
   * Executing tests
   * Publishing coverage artifacts
   * Building & pushing Docker images

With this foundation, we’ll achieve a fully automated CI/CD pipeline that guarantees reliability and faster releases for our Node.js application.

## Links & References

* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Node.js Official Site](https://nodejs.org/)
* [Jest Testing Framework](https://jestjs.io/)
* [Mocha Testing Framework](https://mochajs.org/)
* [Istanbul/NYC Code Coverage](https://istanbul.js.org/docs/advanced/nyc)
* [Docker Official Site](https://www.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/dddd1140-bc2d-4fea-809d-ad09e1f4e620" />
</CardGroup>
