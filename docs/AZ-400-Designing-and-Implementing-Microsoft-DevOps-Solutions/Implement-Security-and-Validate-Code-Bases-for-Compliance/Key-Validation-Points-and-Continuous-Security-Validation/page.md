# Run a quick baseline scan and generate an HTML report
zap-baseline.py -t https://example.com -r baseline-report.html

# Execute a full-depth active scan with detailed reporting
zap-full-scan.py -t https://example.com -r full-scan-report.html
```

## Integrating ZAP into Your Workflow

* Automate baseline assessments on every build for immediate vulnerability feedback.
* Enable passive scanning during feature development to catch missing headers early.
* Schedule full active scans overnight for exhaustive coverage and historic tracking.

## Links and References

* [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
* [CI/CD Integration Guide](https://www.zaproxy.org/docs/dev/ci/)
* [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/1bd9c8cc-efae-414c-b4be-838e767634f6/lesson/0b2472eb-bbfd-4aff-931a-526dd0b116ed" />
</CardGroup>


# Key Validation Points and Continuous Security Validation

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Implement-Security-and-Validate-Code-Bases-for-Compliance/Key-Validation-Points-and-Continuous-Security-Validation/page

This article discusses integrating validation checks and continuous security validation in DevOps to enhance code quality and reduce risks.

In modern DevOps pipelines, integrating validation checks and continuous security validation is crucial for maintaining code quality and reducing risks. By embracing a **shift-left** strategy, teams can detect issues early—saving time and costs while enhancing overall security posture.

## Key Validation Points Across the DevOps Lifecycle

At every phase of the DevOps lifecycle, targeted validation steps provide rapid feedback. Early detection through IDE plugins or CI scans prevents defects from propagating downstream.

<Frame>
  ![The image outlines key validation points in a software development process, highlighting stages like feedback, CI, development, and testing, with associated tasks such as code review, vulnerability scanning, and performance testing.](https://kodekloud.com/kk-media/image/upload/v1752868027/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Key-Validation-Points-and-Continuous-Security-Validation/software-development-validation-points-diagram.jpg)
</Frame>

| Stage                  | Validation Checks                              | Examples                                        |
| ---------------------- | ---------------------------------------------- | ----------------------------------------------- |
| IDE & Pull Requests    | Static analysis, peer code review              | ESLint, SonarQube, GitHub/GitLab merge requests |
| Continuous Integration | Automated builds, unit & integration tests     | Jenkins, Azure Pipelines, GitLab CI             |
| Development Phase      | Security scans, performance testing            | OWASP ZAP, SonarCloud, JMeter                   |
| Testing Stage          | Penetration testing, infrastructure validation | Metasploit, Terraform `validate`, Chef InSpec   |

<Callout icon="lightbulb">
  Shifting validation left means catching issues in IDEs or CI—before they reach QA or production.
</Callout>

## The True Cost of Defects at Each Stage

Defect remediation cost escalates dramatically the later you catch it. Below are industry averages:

<Frame>
  ![The image illustrates the cost of defects at different stages of software development: Coding (80/defect), Build (240/defect), QA & Security (960/defect), and Production (7,600/defect). It highlights the increasing cost of defects as they progress through the development lifecycle.](https://kodekloud.com/kk-media/image/upload/v1752868027/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Key-Validation-Points-and-Continuous-Security-Validation/cost-of-defects-software-development.jpg)
</Frame>

| Phase         | Average Cost per Defect |
| ------------- | ----------------------- |
| Coding        | \$80                    |
| Build         | \$240                   |
| QA & Security | \$960                   |
| Production    | \$7,600                 |

<Callout icon="lightbulb">
  Fixing a bug during development can cost up to 90% less than patching it in production.
</Callout>

## Shifting Security Left

Embedding security early in your DevOps pipeline empowers developers to remediate vulnerabilities before they become critical.

<Frame>
  ![The image illustrates a process of continuous security validation, emphasizing the need to integrate security early in the development cycle to avoid issues before deployment to production. It shows a flow from coding to production with a focus on shifting security left.](https://kodekloud.com/kk-media/image/upload/v1752868028/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Key-Validation-Points-and-Continuous-Security-Validation/continuous-security-validation-development-cycle.jpg)
</Frame>

Key benefits of shift-left security include:

* Early detection of vulnerabilities in code and dependencies
* Faster, automated remediation workflows
* Significant cost savings per defect

<Callout icon="triangle-alert">
  Delaying security tests until the end of the pipeline can lead to critical vulnerabilities slipping into production.
</Callout>

## Continuous Security Validation and Automation

Automating security checks at every commit, build, and release ensures that security keeps pace with rapid deployments.

<Frame>
  ![The image is about "Continuous Security Validation" and highlights the importance of shifting Secure DevOps practices earlier in the development process to reduce costs, and implementing automated tooling to identify issues.](https://kodekloud.com/kk-media/image/upload/v1752868029/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Key-Validation-Points-and-Continuous-Security-Validation/continuous-security-validation-devops-automation.jpg)
</Frame>

Incorporate these automated security tools:

* Static Application Security Testing (SAST)
* Dynamic Application Security Testing (DAST)
* Software Composition Analysis (SCA)
* Runtime Application Self-Protection (RASP)

<Callout icon="lightbulb">
  Combine multiple tools in your CI/CD pipeline to cover code flaws, third-party risks, and runtime threats.
</Callout>

## Links and References

* [Azure DevOps Documentation](https://learn.microsoft.com/azure/devops/)
* [OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)
* [Jenkins CI](https://www.jenkins.io/)
* [SonarQube](https://www.sonarqube.org/)
* [Terraform Registry](https://registry.terraform.io/)
* [Metasploit Framework](https://www.metasploit.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/1bd9c8cc-efae-414c-b4be-838e767634f6/lesson/a40bc77f-8a71-4069-aa59-125f81e12220" />
</CardGroup>
