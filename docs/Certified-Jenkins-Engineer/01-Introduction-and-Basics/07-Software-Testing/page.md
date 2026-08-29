# Software Testing

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Introduction-and-Basics/Software-Testing/page

This article discusses effective software testing practices within the CI/CD pipeline to enhance code quality and maintain system integrity.

Effective software testing is essential in the CI/CD pipeline to catch defects early, improve code quality, and enable safe refactoring. By integrating a robust test suite into your development workflow, you can ensure that every change maintains system integrity and performance.

![The image lists different types of software testing, including unit, integration, smoke, functional, non-regression, acceptance, code quality, performance, security, and manual testing.](https://kodekloud.com/kk-media/image/upload/v1752870593/notes-assets/images/Certified-Jenkins-Engineer-Software-Testing/software-testing-types-list.jpg)

## Common Types of Software Testing

* **Unit Testing**\
  Verifies individual functions or methods in isolation.
* **Integration Testing**\
  Ensures that modules or services communicate correctly.
* **Smoke Testing**\
  A quick, surface-level check of critical features.
* **Functional Testing**\
  Validates the software against functional requirements.
* **Non-Regression Testing**\
  Confirms that new changes haven’t broken existing functionality.
* **Acceptance Testing**\
  Tests the system from an end-user perspective.
* **Code Quality & Static Analysis**\
  Identifies code smells, style violations, and potential bugs using tools like ESLint or SonarQube.
* **Performance Testing**\
  Measures responsiveness and stability under load.
* **Security Testing**\
  Scans for vulnerabilities such as SQL injection or cross-site scripting.
* **Manual Testing**\
  Exploratory or UX-focused tests performed by QA engineers.

## Test Categories by Execution Speed

| Category         | Test Types                                         | Purpose                                 |
| ---------------- | -------------------------------------------------- | --------------------------------------- |
| Fast Automated   | Unit Tests, Integration Tests, Smoke Tests         | Immediate feedback on code changes      |
| Slower Automated | Functional Tests, Non-Regression Tests, Acceptance | Comprehensive validation before release |
| Manual           | Exploratory Testing, User-Experience Validation    | Human-driven scenarios and edge cases   |

> **lightbulb** Manual testing is best reserved for exploratory scenarios and usability validation after your automated suites pass.

## Balanced Testing Strategy

A layered testing approach optimizes feedback loops and resource usage:

1. **Run Unit Tests First**\
   Trigger these on every commit for fast error detection.
2. **Schedule Higher-Level Tests**\
   Execute functional, non-regression, and acceptance tests on a build server or nightly job.
3. **Investigate Failures from Bottom Up**\
   Always start with unit or integration test errors to pinpoint the root cause.

> **triangle-alert** Skipping unit tests can lead to cascading failures in higher-level tests. Always fix the smallest failing test before moving up the testing pyramid.

![The image outlines four testing principles: Speed and Frequency, Cost Effectiveness, Failure Analysis, and Cascade Effect, each represented with an icon.](https://kodekloud.com/kk-media/image/upload/v1752870594/notes-assets/images/Certified-Jenkins-Engineer-Software-Testing/testing-principles-icons-outline.jpg)

## Key Testing Principles

| Principle           | Description                                                                               |
| ------------------- | ----------------------------------------------------------------------------------------- |
| Speed and Frequency | Run low-level tests (unit/integration) on every change; reserve resource-intensive tests. |
| Cost Effectiveness  | Maximize automated coverage where maintenance effort yields high ROI.                     |
| Failure Analysis    | Address unit/integration failures before reviewing higher-level test results.             |
| Cascade Effect      | Trace broad test failures back to the smallest component to locate defects efficiently.   |

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [CI/CD Best Practices](https://www.redhat.com/en/topics/devops/what-is-ci-cd)
* [Software Testing Fundamentals](https://www.guru99.com/software-testing.html)
* [SonarQube Static Analysis](https://www.sonarqube.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2e8ea9bb-e5bb-428e-85d9-89f2eb816adb/lesson/95109e6f-3c7f-4467-8778-d97625495ce6)
