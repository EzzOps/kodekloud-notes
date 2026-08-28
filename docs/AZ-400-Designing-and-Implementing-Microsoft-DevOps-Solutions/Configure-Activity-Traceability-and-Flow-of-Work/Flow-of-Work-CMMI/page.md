# Flow of Work CMMI

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configure-Activity-Traceability-and-Flow-of-Work/Flow-of-Work-CMMI/page

This article explores the CMMI process template in Azure DevOps for structured process improvement and governance.

In this lesson, we dive into the Capability Maturity Model Integration (CMMI) process template available in Azure DevOps. CMMI delivers a structured framework for process improvement, rigorous audit trails, and decision tracking—ideal for teams managing complex requirements, change requests, and risk mitigation.

## When to Choose CMMI

<Callout icon="lightbulb">
  CMMI is designed for organizations that require formal governance, regulatory compliance, and comprehensive traceability across all deliverables.
</Callout>

* Formalize process improvement and governance
* Maintain an immutable audit trail of key decisions
* Track detailed requirements, change requests, and risks
* Support enterprise-level change management and compliance

## Azure DevOps CMMI Work Item States

CMMI enforces a four-stage lifecycle for every work item:

1. **Proposal**\
   New work items or change requests are defined and evaluated.
2. **Active**\
   Items under detailed development, analysis, or review.
3. **Resolved**\
   Completed work is marked as addressed, awaiting verification.
4. **Closed**\
   Final approval, sign-off, and archival.

<Frame>
  ![The image illustrates a "Flow of Work" diagram for CMMI, showing stages labeled as Proposal, Active, Resolved, and Closed, connected to a central "States" icon.](https://kodekloud.com/kk-media/image/upload/v1752867410/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Flow-of-Work-CMMI/cmmi-flow-of-work-diagram.jpg)
</Frame>

## CMMI Work Item Types

The CMMI template in Azure DevOps includes these core work item types, ensuring end-to-end traceability:

| Work Item Type | Purpose                                             | Example                             |
| -------------- | --------------------------------------------------- | ----------------------------------- |
| EPIC           | High-level objective spanning multiple releases     | Migrate legacy reports to Power BI  |
| Feature        | Discrete deliverable within an EPIC                 | Implement OAuth2 authentication     |
| Requirement    | Specific criteria derived from a Feature            | Support multi-factor login          |
| Task           | Atomic unit of work linked to a Requirement         | Write API integration tests         |
| Bug            | Code or configuration defects                       | Fix null-pointer exception in login |
| Change Request | Proposed change to scope, schedule, or cost         | Adjust sprint backlog for new UI    |
| Issue          | Immediate impediment or blocker                     | Resolve build pipeline failures     |
| Review         | Formal evaluation and approval record               | UX design review checklist          |
| Risk           | Potential future problem requiring mitigation plans | Single point of failure in database |

## Testing Structure in CMMI

A modular testing hierarchy promotes reusability and comprehensive coverage:

* **Test Plan**\
  Overall testing strategy, scope, and goals.
* **Test Suite**\
  Logical grouping of related test cases.
* **Test Case**\
  Detailed steps verifying a specific feature or requirement.
* **Shared Steps**\
  Reusable sequences (e.g., login, API call) across multiple test cases.
* **Shared Parameters**\
  Data sets enabling data-driven testing scenarios.

<Frame>
  ![The image is a flowchart illustrating a testing process, starting with "Test Plan" and progressing through "Test Suite," "Test Case," and ending with "Shared Steps" and "Shared Parameters."](https://kodekloud.com/kk-media/image/upload/v1752867412/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Flow-of-Work-CMMI/testing-process-flowchart-test-plan.jpg)
</Frame>

## Feedback Management Workflow

CMMI embeds structured feedback loops to engage stakeholders early and often:

1. **Feedback Request**\
   Invite stakeholders to review features, designs, or deliverables.
2. **Feedback Response**\
   Gather comments, suggestions, or approval decisions.

<Frame>
  ![The image shows a flowchart with two connected boxes labeled "Feedback Request" and "Feedback Response," illustrating a feedback process.](https://kodekloud.com/kk-media/image/upload/v1752867414/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Flow-of-Work-CMMI/feedback-request-response-flowchart.jpg)
</Frame>

## Code Review Workflow

Ensuring code quality and compliance through peer reviews:

1. **Code Review Request**\
   Developer submits code changes for evaluation.
2. **Code Review Response**\
   Reviewers provide feedback, approval, or additional change requests.

<Frame>
  ![The image shows a flowchart with two connected boxes labeled "Code Review" and "Code Review Response," indicating a process or sequence.](https://kodekloud.com/kk-media/image/upload/v1752867414/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Flow-of-Work-CMMI/code-review-flowchart-process-sequence.jpg)
</Frame>

## Next Steps

With the CMMI process template established, our next topic will cover **activity traceability**, enabling you to link requirements, tasks, test cases, and code changes for full lifecycle visibility.

## References

* [Azure DevOps Process Templates](https://docs.microsoft.[AWS_SECRET_ACCESS_KEY]work/process-templates)
* [CMMI Model Overview](https://cmmiinstitute.com/)
* [Azure DevOps Work Item Types](https://docs.microsoft.com/azure/devops/boards/work-items/about-work-items)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/503e97d4-be52-440b-8a4e-8610d1eca6ed/lesson/09f0747a-489b-4886-a6c6-36690f3793a4" />
</CardGroup>
