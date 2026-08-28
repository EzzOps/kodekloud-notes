# Flow of Work SCRUM

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configure-Activity-Traceability-and-Flow-of-Work/Flow-of-Work-SCRUM/page

This article explains the Scrum framework in Azure DevOps, detailing work item hierarchy, lifecycle, and when to use the Scrum template.

Scrum is an agile framework that structures development into fixed-length iterations called **sprints**, enabling rapid feedback, continuous improvement, and high adaptability. In **Azure DevOps**, the Scrum process template extends the Basic process by introducing three additional states—**Approved**, **Committed**, and **Removed**—to give teams finer control over work-item progress and feedback loops.

<Frame>
  ![The image is a slide titled "When to use a SCRUM template?" with three points: "Team anatomy emphasized," "Frequent stakeholder feedback," and "Agile product development," each accompanied by an icon.](https://kodekloud.com/kk-media/image/upload/v1752867420/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Flow-of-Work-SCRUM/scrum-template-usage-points-slide.jpg)
</Frame>

**When to choose a Scrum template in Azure DevOps?**

* You want to emphasize clear **team roles** and self-organization.
* You require **frequent stakeholder feedback** to guide development.
* You plan for **rapid, iterative delivery** aligned with agile product development.

***

## Scrum Work-Item Hierarchy

Azure DevOps organizes Scrum work items into a clear hierarchy. This structure helps you map strategic goals to deliverable tasks and defects.

| Work Item                      | Purpose                                    | Example                               |
| ------------------------------ | ------------------------------------------ | ------------------------------------- |
| **Epic**                       | High-level initiative spanning releases    | Launch international payments support |
| **Feature**                    | Group of related PBIs delivering value     | Payment authorization workflow        |
| **Product Backlog Item (PBI)** | User story, bug, or task driving a feature | “As a user, I want 3D Secure...”      |
| **Task**                       | Specific work unit derived from a PBI      | Implement UI validation, write tests  |
| **Bug**                        | Defect tracked and prioritized like a PBI  | Fix transaction timeout error         |
| **Impediment**                 | Blocker preventing sprint progress         | Waiting on external API keys          |

<Callout icon="lightbulb">
  Track PBIs and bugs on the **Kanban board** for visibility, then split them into **Sprint tasks** on the taskboard to manage day-to-day work and remaining effort.
</Callout>

***

## Backlog-Item Lifecycle in Scrum

The lifecycle of a backlog item in Scrum—from creation through completion or removal—follows a set of well-defined states:

<Frame>
  ![The image is a workflow diagram showing the progression of a backlog item through stages: New, Approved, Committed, and Done. Each stage includes a condition, such as approval by the product owner or commitment by the team.](https://kodekloud.com/kk-media/image/upload/v1752867421/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Flow-of-Work-SCRUM/backlog-item-workflow-diagram-stages.jpg)
</Frame>

1. **New**
   * A PBI (feature, bug, or task) is created to capture stakeholder requirements.
2. **Approved**
   * The Product Owner validates alignment with goals and approves it for sprint planning.
3. **Committed**
   * The team pulls the approved item into the sprint backlog and commits to delivering it.
4. **Done**
   * The work meets the **Definition of Done**, passes all acceptance criteria, and is closed.
5. **Removed**
   * At any point, items can be removed if priorities shift or the work is no longer needed.

Throughout each sprint, newly discovered work is added to the backlog, reprioritized, and planned in upcoming iterations. This iterative loop ensures that the team continuously delivers value and adapts to stakeholder feedback.

***

## Links and References

* [Azure DevOps Scrum process template](https://docs.microsoft.com/azure/devops/boards/work-items/guidance/scrum-process)
* [The Scrum Guide](https://scrumguides.org/)
* [Kanban board in Azure DevOps](https://docs.microsoft.com/azure/devops/boards/boards/kanban)
* [Definition of Done](https://www.scrum.org/resources/definition-of-done)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/503e97d4-be52-440b-8a4e-8610d1eca6ed/lesson/d997b7d7-8696-4196-a70a-8564018a9a57" />
</CardGroup>
