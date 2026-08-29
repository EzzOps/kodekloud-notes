# VSTest task removed -> logic errors go unchecked
```

Always include the `VSTest@2` task to enforce your unit tests:

```yaml theme={null}
- task: VSTest@2
  inputs:
    platform: '$(buildPlatform)'
    configuration: '$(buildConfiguration)'
```

***

## Conclusion

By integrating MSTest unit tests into your Azure DevOps YAML pipeline, you establish a robust CI process that catches logic errors early. This simple setup increases confidence in code quality and ensures that only tested code is deployed.

***

## References

* [Azure DevOps Pipelines YAML schema](https://docs.microsoft.com/azure/devops/pipelines/yaml-schema)
* [MSTest Unit Testing Framework](https://docs.microsoft.com/visualstudio/test/mstest-unit-test-framework)
* [Azure Repos Git](https://docs.microsoft.com/azure/devops/repos/git)
* [Continuous Integration (CI) in Azure DevOps](https://docs.microsoft.com/azure/devops/learn/what-is-continuous-integration)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/f114915a-674b-4c1a-a7f2-7a5444db938b/lesson/313bfe6a-2472-46f0-bd89-44d07d6bc1f5)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Pipeline-Automation/Introduction/page

This lesson covers implementing orchestration and automation solutions using Azure DevOps, focusing on security, testing strategies, code coverage, and external tool integrations.

In this lesson, we’ll begin our journey into implementing an orchestration and automation solution using Azure DevOps. With its rich suite of tools, Azure DevOps helps you build, test, and deploy applications while ensuring security and reliability throughout the pipeline.

We’ll cover:

1. Dependency and security scanning
2. Testing strategies (unit, integration, load)
3. Code coverage analysis
4. Integrations with external tools

Let’s dive in!

***

## Dependency and Security Scanning

Ensuring that your codebase is free from vulnerable or outdated dependencies is a critical first step. Azure Pipelines supports multiple scanning tools and can block builds on detected risks.

> **lightbulb** Run dependency scans early in your pipeline to catch issues before they propagate downstream.

![The image is a slide titled "Dependency and Security Scanning" with three bullet points: "Exploring Dependency Scanning in Azure Pipelines," "Tools for Dependency Scanning," and "Understanding Security Scanning."](https://kodekloud.com/kk-media/image/upload/v1752867760/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/dependency-security-scanning-azure-pipelines.jpg)

### Key Steps

* Configure the `dependency-check` or `npm audit` task in your YAML
* Integrate vulnerability reports in Pull Request checks
* Automate patching and updates

### Common Tools Comparison

| Tool             | Purpose                              | Documentation                                                                                                                                                  |
| ---------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WhiteSource Bolt | Open-source vulnerability scanning   | [https://docs.microsoft.com/azure/devops/pipelines/ecosystems/whitesource-bolt](https://docs.microsoft.com/azure/devops/pipelines/ecosystems/whitesource-bolt) |
| SonarCloud       | Code quality & security analysis     | [https://sonarcloud.io/documentation](https://sonarcloud.io/documentation)                                                                                     |
| OWASP ZAP        | Dynamic application security testing | [https://owasp.org/www-project-zap/](https://owasp.org/www-project-zap/)                                                                                       |
| Dependabot       | Automated dependency updates         | [https://github.com/dependabot/dependabot-core](https://github.com/dependabot/dependabot-core)                                                                 |

***

## Testing in CI/CD

Testing is the backbone of any reliable pipeline. By running tests automatically, you can catch regressions and performance issues before they reach production.

![The image is a slide titled "Local Tests, Unit Tests, Integration Tests, and Load Tests," listing four topics: the importance of testing in CI/CD, configuring unit tests, setting up integration tests, and implementing load tests.](https://kodekloud.com/kk-media/image/upload/v1752867762/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/local-tests-unit-integration-load-tests.jpg)

| Test Type          | Goal                                      | Azure Pipeline Task                 |
| ------------------ | ----------------------------------------- | ----------------------------------- |
| Unit Tests         | Verify individual components              | `DotNetCoreCLI@2` / `npm test`      |
| Integration        | Validate interactions between modules     | `VSTest@2` / `pytest`               |
| Load / Performance | Measure application behavior under stress | Apache JMeter task / custom scripts |
| Smoke / Sanity     | Quick verification of critical features   | Inline PowerShell / Bash scripts    |

### Best Practices

* Run unit tests on each PR
* Isolate integration tests in a dedicated environment
* Schedule load tests during off-peak hours

***

## Code Coverage Analysis

Tracking code coverage helps ensure that your tests exercise the most critical parts of your application.

![The image is a slide titled "Understanding Code Coverage," listing five topics related to code coverage, including introduction, workings, setup in Azure Pipelines, analysis, and best practices.](https://kodekloud.com/kk-media/image/upload/v1752867763/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/understanding-code-coverage-topics-slide.jpg)

### Coverage Workflow

1. Instrument your code (e.g., `coverlet`, `nyc`)
2. Run tests with coverage flags enabled
3. Publish coverage reports via `PublishCodeCoverageResults@1`
4. Analyze gaps and write additional tests

> **lightbulb** Aim for at least 80% coverage on critical modules, but prioritize test quality over quantity.

***

## Integrating External Tools

Round out your end-to-end DevOps workflow by connecting pipelines to security scanners, artifact repositories, and alerting systems.

| Integration              | Purpose                       | Azure DevOps Extension                    |
| ------------------------ | ----------------------------- | ----------------------------------------- |
| Azure Container Registry | Store and scan Docker images  | `Azure Container Registry Task`           |
| GitHub Advanced Security | Code scanning on PRs          | GitHub integration via service connection |
| Artifactory              | Universal artifact repository | JFrog Artifactory plugin                  |
| PagerDuty / Teams        | Alert on pipeline failures    | Notification settings in Project Services |

> **triangle-alert** Always secure service connections and protect access tokens using [Azure Key Vault](/docs/pipelines/library/key-vault).

***

## Next Steps

You now have the framework to:

* Automate dependency and security checks
* Enforce comprehensive testing strategies
* Monitor and improve code coverage
* Integrate with external tools for a seamless DevOps lifecycle

Proceed to the next lesson to build and deploy your first containerized application with Azure Pipelines.

***

## References

* [Azure DevOps Documentation](https://docs.microsoft.com/azure/devops/)
* [Azure Pipelines Security Scanning](https://docs.microsoft.com/azure/devops/pipelines/ecosystems/security)
* [Azure Test Plans](https://docs.microsoft.com/azure/devops/pipelines/test/)
* [Code Coverage in Azure DevOps](https://docs.microsoft.com/azure/devops/pipelines/test/coverage)
* [Azure DevOps Marketplace](https://marketplace.visualstudio.com/azuredevops)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/f114915a-674b-4c1a-a7f2-7a5444db938b/lesson/80c197b9-b7e8-443e-990b-df2c5f0e9714)
