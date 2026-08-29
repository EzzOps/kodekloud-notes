# Cloud IAM Access Approval

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Cloud-IAM-Access-Approval/page

Guide to Cloud IAM Access Approval explaining manual review workflow for sensitive roles, time-bound permissions, approval best practices, approvers' checks, auditing and automated revocation.

Hello and welcome back.

Earlier we explored Cloud IAM groups and how grouping users simplifies access management at scale. In this lesson we focus on Access Approval: a common organizational control that enforces manual review for sensitive permissions and helps implement least privilege and temporary access.

## How the access-approval flow works

At a high level, the access-approval workflow follows these steps:

1. A user determines they need additional permissions to complete a task (for example, creating a VPC network).
2. The user submits an access request through the organization's request system.
3. The request is reviewed by approvers according to defined policy and sensitive-role requirements.
4. If approved, the user receives the requested permission(s) for a defined duration (time-bound grant).
5. After the duration ends, the granted access is automatically removed.

First, the user must request access. Some organizations grant broad default access for non-sensitive exploration, but for privileged operations you should require explicit requests so users understand the scope of what they are asking for.

When a user requests access they should clearly specify what they need and why. For example: "I need the role `compute.networkAdmin` to create a VPC network." Always grant only the permissions requested — this enforces the least privilege principle and reduces blast radius.

Next, the request enters the approval flow. Reviewers should verify:

* Whether the requester already has the needed access (to avoid redundant approvals).
* Whether the requested role actually contains the permissions required for the task.
* Whether the role or permissions are classified as sensitive under your policy (those should require manual approval).

<Frame>
  <img alt="A diagram titled &#x22;Simplified Access Approval Process&#x22; showing a timeline of steps: User Request Access → Access Approval → Approver → User Creates VPC → Access Expires. Below it is a note that an access approval policy is configured so sensitive roles require manual approval." />
</Frame>

## Approvers and what they need

Approvers are typically organization administrators or designated custodians (for example, a director of SRE or a DevOps manager). When a request arrives, approvers need concise, actionable information to decide quickly:

* Who is requesting access.
* Why they need it (business justification).
* Exactly which role or permission is requested.
* How long the access is needed (requested duration).

Use a standardized approval checklist to reduce ambiguity and speed decisions. The following table summarizes required request fields and examples:

| Field                  | Why it matters                              | Example                             |
| ---------------------- | ------------------------------------------- | ----------------------------------- |
| Requester              | Identify the user and check existing access | `alice@example.com`                 |
| Business justification | Validates need and audit trail              | "Create VPC for onboarding project" |
| Role / Permission      | Ensures the grant matches the task          | `compute.networkAdmin`              |
| Duration               | Limits exposure via time-bound access       | `4 hours` or `3 days`               |
| Evidence / Links       | Attach relevant tickets or runbooks         | Link to Jira ticket or runbook      |

Common request channels include Jira, ServiceNow, identity governance platforms (e.g., SailPoint), or an internal portal/console.

| Channel                                         | Purpose                                        |
| ----------------------------------------------- | ---------------------------------------------- |
| [Jira](https://www.atlassian.com/software/jira) | Track approvals and link to change requests    |
| [ServiceNow](https://www.servicenow.com/)       | ITSM-driven approvals                          |
| Identity governance platforms (e.g., SailPoint) | Centralized entitlement requests and lifecycle |
| Internal portal / console                       | Lightweight self-service with audit trail      |

<Frame>
  <img alt="A slide titled &#x22;Simplified Access Approval Process&#x22; showing a horizontal workflow: User Request Access → Access Approval → Approver → User Creates VPC → Access Expires, with icons for each step. Below the timeline are bullets describing the approver notification and what the access request should contain." />
</Frame>

## After approval: performing the task and automatic expiry

Once access is approved and granted, the user performs the task (for example, creating the VPC). Ensure that the system issues permissions only for the requested time window, and that the grant is auditable.

<Frame>
  <img alt="A titled diagram showing a simplified access approval process as a horizontal timeline with icons and steps: &#x22;User Request Access,&#x22; &#x22;Access Approval,&#x22; &#x22;Approver,&#x22; &#x22;User Creates VPC&#x22; (highlighted), and &#x22;Access Expires.&#x22; A note below states the user now has permission to create the VPC network." />
</Frame>

Automated expiry and removal of temporary grants are essential. Without time-bound grants and automated revocation, environments accumulate excessive privileges and drift occurs in IAM policies. Use automated workflows to:

* Enforce time-limited access by default.
* Audit all granted requests and expirations.
* Revoke access automatically when the duration ends.

<Callout icon="lightbulb">
  Plan requests so they include the reason and a justified duration, and ensure your approval workflow enforces automatic revocation when the duration ends.
</Callout>

## Best practices and further reading

* Enforce least privilege: prefer role/permission granularity over broad roles.
* Require manual approval for roles that map to sensitive permissions.
* Integrate approvals with ticketing or identity governance to maintain audit trails.
* Use short, justifiable durations and automate revocation.
* Regularly review temporary-access logs to detect anomalies and reduce drift.

Further reading and related resources:

* [Google Cloud IAM documentation](https://cloud.google.com/iam/docs)
* [Atlassian Jira](https://www.atlassian.com/software/jira)
* [ServiceNow](https://www.servicenow.com/)
* [SailPoint identity governance](https://www.sailpoint.com/)

That is it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/26b9d717-98d8-4a8c-87ed-38208f82d8b2" />
</CardGroup>
