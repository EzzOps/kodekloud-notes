# Project Status Meeting 2

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Project-Status-Meeting-2/page

This article discusses issues with a production MongoDB cluster due to CI pipeline integration and proposes solutions for isolating test environments.

Welcome to the second project status meeting. In this session, we’ll review how our GitHub Actions workflow began impacting the production MongoDB cluster and outline the steps to isolate our test environments.

***

## 1. Issue Discovery

After completing the first four tasks, Alice was summoned to an urgent meeting. The team noticed that their production MongoDB cluster was intermittently unresponsive and slow ever since they integrated unit-testing and code-coverage into their CI pipeline.

### 1.1 Current Test & Coverage Steps

Both the **unit-testing** and **code-coverage** jobs are inadvertently pointing to the production database:

```yaml theme={null}
