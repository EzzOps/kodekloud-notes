# 0
```

A **test\_results.xml** file is generated for CI.

## Run Coverage

Generate coverage reports with:

```bash theme={null}
npm run coverage
```

Sample failure output if coverage is below threshold:

```text theme={null}
ERROR: Coverage for lines (88.88%) does not meet global threshold (90%)
```

Verify exit code:

```bash theme={null}
echo $?
# 1
```

Reports are available in the **coverage/** directory (cobertura XML, lcov, JSON summary).

## Start the Application

Launch your server locally:

```bash theme={null}
npm start
```

By default, the server listens on port 3000. Open your browser at:

[http://localhost:3000](http://localhost:3000)

Use the search bar to look up planet details by ID. Data is served from a MongoDB Atlas cluster and displayed in the UI.

![The image shows a webpage about the solar system, featuring an illustration of Saturn with its rings and a description of the planet. There is a search bar labeled "Search the Planet" and a title "Solar System."](https://kodekloud.com/kk-media/image/upload/v1752876519/notes-assets/images/GitHub-Actions-Run-and-Test-NodeJS-App-on-Local-Machine/solar-system-saturn-illustration-webpage.jpg)

## Links and References

* [Node.js Official Site](https://nodejs.org/)
* [Mocha Documentation](https://mochajs.org/)
* [Chai Assertion Library](https://www.chaijs.com/)
* [nyc (Istanbul) Code Coverage](https://github.com/istanbuljs/nyc)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/6d590d33-38aa-4982-a7df-318e8bfb74e8)


# Understanding DevOps Pipeline

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Understanding-DevOps-Pipeline/page

This guide designs a CI/CD pipeline for a Node.js application using GitHub Actions to automate builds, testing, and deployments.

In this guide, we’ll design a CI/CD pipeline for a Node.js application using **GitHub Actions**. Automating each stage ensures consistent builds, rapid feedback, and reliable deployments across development and production clusters.

## Pipeline Overview

| Stage                    | Description                                      |
| ------------------------ | ------------------------------------------------ |
| Source Checkout          | Pull code from GitHub repository                 |
| Unit Testing             | Install dependencies, run tests, archive reports |
| Code Coverage            | Generate coverage metrics (errors ignored)       |
| Containerization         | Build Docker image, smoke test, push to registry |
| Dev Deployment           | Apply Kubernetes manifests, expose via Ingress   |
| Dev Integration Testing  | Validate live endpoint on development cluster    |
| Manual Approval          | Pause for reviewer sign-off                      |
| Prod Deployment          | Deploy to production cluster                     |
| Prod Integration Testing | Verify the production endpoint                   |

***

## 1. Source Checkout

Begin by checking out your repository so that all subsequent jobs have access to your code.

```yaml theme={null}
- name: Checkout source code
  uses: actions/checkout@v3
```

***

## 2. Unit Testing

Install dependencies, execute your test suite, and archive the results. The pipeline will fail on any test errors.

```bash theme={null}
npm ci
npm test
