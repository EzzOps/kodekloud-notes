# SRE Culture and Philosophy

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Fundamentals-of-SRE/SRE-Culture-and-Philosophy/page

Overview of SRE culture emphasizing shared ownership, data driven decisions, blameless postmortems, psychological safety, SLOs and error budgets to balance reliability and innovation

In this lesson we explore Site Reliability Engineering (SRE) culture and philosophy: the values, practices, and organizational changes that make reliability a shared, measurable responsibility.

SRE culture centers on three interrelated principles:

* Shared ownership
* Data-driven decisions
* Continuous improvement

These principles shape how teams design systems, respond to incidents, and prioritize work.

| Principle              |                                                                                         What it means | Practical example                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------: | --------------------------------------------------------------------------- |
| Shared ownership       |      Teams take end-to-end responsibility for services rather than handing work off to another group. | Developers participate in on-call rotations and reliability design reviews. |
| Data-driven decisions  |      Use measurable targets (SLOs) and error budgets to guide trade-offs between speed and stability. | Decide whether to push a release based on remaining error budget.           |
| Continuous improvement | Learn from incidents, iterate on processes, and invest in both short- and long-term reliability work. | Run blameless postmortems and prioritize remediation tasks in the backlog.  |

Shared ownership removes the “us vs. them” split between development and operations. When engineering teams own their services end-to-end, reliability becomes a shared goal instead of a gatekeeper function, which builds empathy and accountability across the organization.

<Frame>
  <img alt="A presentation slide titled &#x22;SRE – Cultural Pillars&#x22; showing three colored pillars labeled Shared Ownership, Data‑Driven Decision Making, and Continuous Improvement. To the right are bullet points about evolving reliability practices, learning from incidents, improving processes/documentation, and balancing urgent fixes with strategic investments." />
</Frame>

SRE teams rely on data — especially Service Level Objectives (SLOs), Service Level Indicators (SLIs), and error budgets — to guide decisions. These metrics make trade-offs explicit: they focus discussions on system behavior and risk, not on hierarchy or gut feeling.

Continuous improvement recognizes that systems, traffic patterns, and user expectations change. SRE practices emphasize iteration over perfection: learn from incidents, apply short-term mitigations, and invest in long-term resilience to reduce recurrence.

SRE culture intentionally rejects blame because blaming individuals blocks learning. When people fear punishment, they hide mistakes and avoid reporting risks, which undermines reliability and psychological safety.

> **warning** Avoid blaming individuals for incidents. Blame suppresses reporting and learning, increasing systemic risk.

Blamelessness shifts the focus from “who” to “what” — identifying contributing factors, system behaviors, and process gaps.

<Frame>
  <img alt="A slide titled &#x22;Blameless Culture&#x22; presenting &#x22;The Blameless Approach.&#x22; It shows two colorful icons with captions: an orange lightbulb icon labeled &#x22;Assume good intentions and contextual limitations&#x22; and a teal target icon labeled &#x22;Focus on what happened, not who did it.&#x22;" />
</Frame>

Blameless postmortems are a primary tool for this approach. They use neutral, fact-based language, document timelines and system state, and capture concrete remediation steps to prevent recurrence.

> **lightbulb** Blameless postmortems are about understanding and improving systems. Keep language neutral, focus on timelines and root causes, and surface actionable remediation.

<Frame>
  <img alt="A slide titled &#x22;Blameless Culture&#x22; showing &#x22;Blameless Postmortems&#x22; with two gear icons numbered 01 and 02. The first gear says &#x22;Written in neutral, fact‑based language&#x22; and the second says &#x22;Focus on timelines, contributing factors, and remediation.&#x22;" />
</Frame>

Postmortems should be shared broadly to enable organizational learning. For example, Google’s public postmortem culture encouraged system-level fixes instead of repeating the same mistakes, and Etsy uses internal incident reports and newsletters to spread lessons across teams. See Google’s SRE Book for deeper guidance on postmortem culture: [https://sre.google/sre-book/postmortem-culture/](https://sre.google/sre-book/postmortem-culture/)

<Frame>
  <img alt="A presentation slide titled &#x22;Blameless Culture: Real Case Studies&#x22; showing Google and Etsy logos with short notes about Google's public postmortems and Etsy's incident reports. The slide also includes a screenshot of a Google Cloud Status dashboard and a © KodeKloud credit." />
</Frame>

Psychological safety underpins blamelessness. It means team members can speak up, ask questions, and admit mistakes without fear of blame or ridicule. This environment produces more complete incident reports, earlier detection of reliability risks, and a culture willing to innovate.

<Frame>
  <img alt="A slide titled &#x22;Psychological Safety&#x22; showing the definition: feeling free to speak up, admit mistakes, and ask questions without fear of blame or ridicule. To the right is an illustration of two people talking in front of a shield with happy and sad face icons, symbolizing a protected conversation." />
</Frame>

In practice, psychological safety looks like welcoming ideas and concerns, treating mistakes as learning opportunities, and encouraging people to raise issues when something “feels off.” Vulnerability is a strength that enables rapid learning and improvement.

<Frame>
  <img alt="A slide titled &#x22;Psychological Safety&#x22; showing three characteristics. They are: ideas and concerns are welcomed; mistakes are treated as learning opportunities; and team members speak up without fear." />
</Frame>

Why it matters: teams with psychological safety surface issues earlier, produce higher-quality incident analysis, and continuously improve processes and automation — all of which enhance reliability.

<Frame>
  <img alt="A slide titled &#x22;Psychological Safety&#x22; that lists three benefits for reliability. The points are: improves early detection of reliability risks; leads to more complete incident reports; and encourages innovation and process improvement, each shown with an icon." />
</Frame>

Google’s Project Aristotle found that group norms matter more than the exact team composition, with psychological safety being the strongest predictor of team effectiveness. Teams that can take interpersonal risks and speak up perform better overall.

<Frame>
  <img alt="A presentation slide titled &#x22;Psychological Safety&#x22; summarizing Google's Project Aristotle findings: team composition is marked wrong while group norms and psychological safety are checked as important. The slide includes an illustration of a microscope examining a team meeting and a prompt to read a NYT article." />
</Frame>

Balancing reliability and innovation is a practical challenge. The Error Budget model helps: instead of targeting zero failures, teams set measurable SLOs and an allowable failure threshold (the error budget). Error budgets create a shared, objective way to decide when to accelerate changes and when to slow down and invest in reliability improvements.

<Frame>
  <img alt="A slide titled &#x22;Balancing Reliability and Innovation&#x22; that outlines the Error Budget Model. It shows four colored gear icons with short tips: define acceptable unreliability via an SLO, use the error budget to balance change velocity and reliability, create guardrails instead of hard stops, and allow fast progress when systems are stable." />
</Frame>

Shared incentives reinforce healthy behaviors: align SRE and product/development teams on the same metrics, share uptime responsibility, and collaborate on trade-offs. Practices include developer on-call rotations, SRE participation in design reviews, and joint ownership of SLOs.

<Frame>
  <img alt="A presentation slide titled &#x22;Balancing Reliability and Innovation&#x22; highlighting &#x22;Shared Incentives&#x22; with four hexagon icons and brief points. It outlines practices like SREs and dev teams using the same metrics, dev on-call rotation, SREs joining design reviews, and making reliability a shared goal." />
</Frame>

Implementing SRE culture requires time, deliberate practice, and leadership sponsorship. It changes how teams behave under pressure and how decisions are made.

Key implementation steps (concise):

| Action                                 |                                                                    Purpose |
| -------------------------------------- | -------------------------------------------------------------------------: |
| Leadership buy-in                      | Make reliability a visible organizational priority and allocate resources. |
| Establish psychological safety         |                   Encourage candid retros and open reporting without fear. |
| Blameless postmortems with peer review |                        Surface root causes and agreed remediation actions. |
| Share incident reports broadly         |                            Promote cross-team learning and systemic fixes. |
| Set shared SLOs across teams           |              Align priorities and create a common language for trade-offs. |

<Frame>
  <img alt="A presentation slide titled &#x22;Implementing SRE Culture&#x22; showing five key implementation steps. The cards list actions like getting leadership buy‑in for reliability goals, normalizing psychological safety and blameless postmortems, sharing incident reports org‑wide, and setting shared SLOs across teams." />
</Frame>

Common challenges include resistance to dropping blame, difficulty measuring cultural progress, inconsistent adoption across teams, and reverting to old habits under stress.

| Common challenge        |                                       How it shows up | Mitigation                                                                     |
| ----------------------- | ----------------------------------------------------: | ------------------------------------------------------------------------------ |
| Blame culture persists  | Team members hide errors or avoid reporting incidents | Leadership modeling, coaching, blameless postmortems                           |
| Hard-to-measure culture | Lack of metrics for psychological safety and learning | Use surveys, incident-report quality metrics, and remediation completion rates |
| Uneven adoption         |   Some teams follow SRE practices while others do not | Share success stories, rotate personnel, and set org-level SLOs                |

<Frame>
  <img alt="A presentation slide titled &#x22;Implementing SRE Culture&#x22; with the heading &#x22;Common Challenges.&#x22; It lists three issues—resistance to giving up the blame culture, lack of metrics for cultural progress, and uneven adoption across teams—along with a central prohibition symbol." />
</Frame>

Real examples show cultural change is possible. Slack shifted from silence to curiosity by running reliability-focused retros and shared postmortems, turning incident analysis into teaching tools that drove cross-functional improvement.

<Frame>
  <img alt="A presentation slide titled &#x22;Implementing SRE Culture&#x22; featuring the Slack logo and the heading &#x22;An Example From Slack.&#x22; Two rounded text boxes note that reliability-focused retros shifted silence to curiosity and that postmortems became internal teaching tools fostering cross‑functional improvement." />
</Frame>

If you’re early in your SRE career, you don’t have to drive the full cultural transformation alone. Start with small, consistent actions:

* Learn your team’s current norms and communication patterns.
* Volunteer for on-call or postmortem participation to gain experience.
* Raise concerns constructively and suggest data-driven improvements.
* Share learning and automation work that reduces toil and improves reliability.

Small, steady contributions to psychological safety, learning, and shared ownership compound into meaningful change over time.

Further reading and references

* Google SRE Book — Postmortem Culture: [https://sre.google/sre-book/postmortem-culture/](https://sre.google/sre-book/postmortem-culture/)
* Project Aristotle summary on team effectiveness: [https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html](https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html)
* Practical guides on SLOs and error budgets: search “SLO error budget best practices” for vendor-neutral resources and case studies.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/df29fdca-b56b-4828-a8cc-abd0bb37ed70/lesson/8de449b6-a220-48ca-894f-645ac86d09ae)
