# Why Backstage

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Why-Backstage/page

Explains why Backstage and Internal Developer Portals centralize tools, docs, ownership, dependency visibility, templates and self service to reduce developer friction and speed delivery.

In this lesson we’ll explain why Backstage exists and the problems it solves. You’ll learn common developer pain points—tool fragmentation, scattered documentation, hidden dependencies, slow provisioning, and repetitive project setup—and how a centralized Internal Developer Portal (IDP) addresses them.

Developers rarely spend their day only in an IDE. Instead they constantly jump between systems: source control, CI/CD, docs, observability, alerting, cloud consoles, cost tools, chat, and more. That creates heavy context switching, many open tabs, and wasted time.

Developers frequently:

* Open [GitHub](https://github.com/) (or another VCS) to inspect code and create pull requests.
* Review CI/CD pipelines and build logs after each push.
* Consult documentation for internal or external services they depend on.
* Monitor observability dashboards ([Prometheus](https://prometheus.io/), [Grafana](https://grafana.com/), [OpenTelemetry](https://opentelemetry.io/)).
* Handle alerts and incident management tools.
* Use cloud consoles ([AWS](https://aws.amazon.com/), [Azure](https://azure.microsoft.com/), [GCP](https://cloud.google.com/)) to manage infrastructure.
* Check [FinOps](https://www.finops.org/) or cost-tracking tools to control spend.

This constant switching wastes time and attention: developers must remember where resources live and often re-orient themselves when moving between tools.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Backstage?&#x22; shows a person working at a laptop surrounded by tech logos (GitHub, Travis CI, Prometheus, Grafana, AWS, Azure, FinOps). To the right is a numbered list summarizing reasons and tools (source control, CI/CD, docs, observability, alerting, cloud consoles, FinOps)." />
</Frame>

Onboarding new hires is especially painful: they receive dozens of links and must discover, memorize, or bookmark them all. A single portal that aggregates links, tools, and documentation greatly reduces friction and speeds productivity.

One core goal of Backstage is to provide that single, consistent portal—so teams can find tools and information faster and spend more time writing code.

Dispersed and inconsistent documentation is another major problem. Imagine integrating with an internal service owned by another team: docs may live in [Confluence](https://www.atlassian.com/software/confluence), [Google Docs](https://docs.google.com/), an internal wiki, or `gh-pages`. Each team may use different conventions, making search and discovery slow. When docs are out of date, you must find the service owner to confirm behavior.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Backstage?&#x22; showing four team panels (Team A: Confluence, Team B: Google Docs, Team C: Internal Website, Team D: GitHub Pages) with a developer icon in the center. On the right is a large green dashboard/checklist labeled &#x22;Team C - Internal website&#x22; representing a consolidated internal site." />
</Frame>

Outdated or missing docs are common in large orgs. Finding the right owner can be hard—sometimes the owner has left, or access controls make discovery slow. That whole chain (search → find wrong docs → identify owner → fix docs) can cost hours.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Backstage?&#x22; showing icons for a developer, code, and a document, with a warning label that reads &#x22;Document is outdated.&#x22;" />
</Frame>

The support chain can be long: search for docs, discover they’re incorrect, then escalate to find who can fix them—leading to unnecessary delays.

<Frame>
  <img alt="A slide titled &#x22;Why Backstage?&#x22; showing a developer icon labeled &#x22;Developer from Team X&#x22; next to a chat dialog where someone asks for help with outdated documentation and receives an automated reply that the contact no longer works at the company." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Why Backstage?&#x22; showing three rounded cards with icons and complaints: &#x22;Spent hours searching through different platforms,&#x22; &#x22;Struggled to identify the current owner of the service,&#x22; and &#x22;Wasted time finding docs and contacts instead of coding.&#x22;" />
</Frame>

A searchable, centralized catalog that lists every application, its documentation, and its owner solves this: search by name or functionality, view docs and owners quickly, and contact the right person without chasing stale links.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Backstage?&#x22; showing a blue &#x22;Central Hub&#x22; icon linked to three boxes labeled &#x22;Searchable Location,&#x22; &#x22;Documentation,&#x22; and &#x22;Ownership.&#x22; The slide uses soft pastel colors and simple line icons." />
</Frame>

Dependency visibility is equally critical. Consider a customer complaining that they never receive email. You inspect the app and see it uses a third-party email provider. The developer who implemented it may have left, and docs may be missing. You could read the code and patch it, but that change might break other services that rely on the same integration.

Below are two typical Python examples for sending email—one using SendGrid and another using a generic SMTP provider. These examples show how integrations differ and why knowing usage and ownership matters.

SendGrid example (uses environment variables for credentials):

```python theme={null}
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = "customer@example.com"
SUBJECT = "Welcome to Our Application!"
BODY = "Thank you for using our app! We are glad to have you onboard."

if not SENDGRID_API_KEY or not SENDER_EMAIL:
    raise EnvironmentError("Missing SendGrid configuration. Check environment variables.")

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

from_email = Email(SENDER_EMAIL)
to_email = To(RECEIVER_EMAIL)
subject = SUBJECT
content = Content("text/plain", BODY)

mail = Mail(from_email, to_email, subject, content)

try:
    response = sg.send(mail)
    print(f"Email sent successfully! Status Code: {response.status_code}")
except Exception as e:
    print(f"Failed to send email: {e}")
```

SMTP example (TLS and configurable port):

```python theme={null}
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = "customer@example.com"
SUBJECT = "Welcome to Our Application!"
BODY = "Thank you for using our app! We are glad to have you onboard."

if not SMTP_SERVER or not SENDER_EMAIL or not SENDER_PASSWORD:
    raise EnvironmentError("Missing SMTP configuration. Check environment variables.")

message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL
message["Subject"] = SUBJECT
message.attach(MIMEText(BODY, "plain"))

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
```

<Callout icon="warning">
  Swapping email providers (or any integration) without full visibility into downstream consumers can break production systems. A catalog with dependency graphs helps you see which services rely on a given integration before making changes.
</Callout>

<Frame>
  <img alt="An illustration of a person sitting with a laptop on the left and a large browser-style error panel on the right. The panel shows &#x22;503 Service Unavailable&#x22; with the message &#x22;A critical dependency is missing. Please try again later.&#x22;" />
</Frame>

A catalog that documents applications, integrations, and dependency graphs helps teams identify impact and avoid accidental breakages.

<Frame>
  <img alt="A slide titled &#x22;Why Backstage?&#x22; showing a central &#x22;Software Repository (Documentation Hub)&#x22; that branches to four boxes labeled Software A, B, C, and D. Each software box points down to a corresponding &#x22;Dependent on Software A/B/C/D&#x22; box." />
</Frame>

Another repetitive organizational burden is creating a new project. Typical manual steps:

* Create a repository in GitHub (sometimes via a ticket).
* Provision infra (Kubernetes cluster, cloud resources) through an infra team.
* Configure CI/CD, linting, testing, and repo permissions.
* Create databases, DNS entries, and other required resources.
* Deploy the application.

Manual completion of these steps is slow and error-prone. Templates and a single “create new project” workflow reduce friction and ensure consistent company standards.

<Frame>
  <img alt="An infographic flowchart titled &#x22;Why Backstage?&#x22; showing onboarding steps for a software project. It outlines tasks like creating a GitHub repo and raising access tickets, setting up repo permissions, tooling (linting/CI), provisioning a Kubernetes cluster, databases and DNS, and finally deploying the application." />
</Frame>

Platform teams can manage templates for languages and frameworks, enforce security and best practices, and enable developers to provision a new project with a button click instead of dozens of manual steps.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Backstage?&#x22; showing a three-step colored flow—&#x22;Manual tasks eliminated,&#x22; &#x22;Button click,&#x22; and &#x22;Template applied&#x22;—with short descriptions about automating project setup across services like GitHub, AWS and Kubernetes. The slide is branded © KodeKloud." />
</Frame>

Resource provisioning is another common bottleneck. Developers often lack permission to create resources directly and must request infra teams, resulting in waiting time. A portal that provides self-service requests with approval workflows and automated provisioning reduces delays while preserving governance.

A typical self-service flow:

1. Developer fills a form describing the resource and configuration.
2. Infra reviews and approves the request.
3. The portal provably provisions the resource and grants access.

This preserves guardrails and audits while speeding delivery.

All these scenarios—tool fragmentation, scattered docs, unknown ownership, hidden dependencies, repetitive scaffolding, and slow provisioning—are the primary drivers for adopting an Internal Developer Portal.

<Frame>
  <img alt="A slide titled &#x22;Internal Developer Portals&#x22; illustrating a development team feeding into a portal that provides tools, documentation, and resources, which then drives code, test, and deploy stages. The footer highlights benefits: single pane of glass, simplified workflow, and enhanced developer experience." />
</Frame>

<Callout icon="lightbulb">
  An Internal Developer Portal (IDP) is a centralized platform that aggregates tools, documentation, ownership information, templates, and self-service capabilities to streamline developer workflows, reduce context switching, and enforce organizational standards.
</Callout>

Common IDP features (summary table)

| Feature                   | Purpose                               | Example                                  |
| ------------------------- | ------------------------------------- | ---------------------------------------- |
| Catalog                   | Central registry of services and apps | Searchable entries for each component    |
| Documentation Hub         | Co-locate docs and code               | API docs, runbooks, integration guides   |
| Ownership Tracking        | Show which team/person owns a service | Contact info and on-call links           |
| Dependency Graphs         | Visualize downstream impacts          | Service A → Service B relationships      |
| Templates & Scaffolding   | Automate project creation             | Language/framework project templates     |
| Admin Controls            | Enforce policies and guardrails       | Security and compliance checks           |
| Self-Service Provisioning | Request and auto-provision resources  | Form → approval → cloud API provisioning |
| Extensibility             | Integrate with tools via plugins      | CI, secrets manager, observability       |

<Frame>
  <img alt="A slide titled &#x22;IDPs – Features&#x22; showing five numbered cards with colorful icons and short descriptions. The cards list: 01 Catalog, 02 Documentation Hub, 03 Ownership Tracking, 04 Templates, and 05 Admin Controls." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;IDPs – Features&#x22; showing two feature cards: &#x22;Search and Discoverability&#x22; with a magnifying-glass icon and &#x22;Scorecards&#x22; with a dashboard icon. Each card includes a short blurb about finding software components and viewing app health/security." />
</Frame>

IDPs deliver measurable benefits:

* Streamlined accessibility: consolidate APIs, services, and tools in one searchable place.
* Centralized documentation: keep docs next to code and examples.
* Clear ownership and improved collaboration: find the right person fast.
* Accelerated development: reuse templates, SDKs, and boilerplates.
* Faster onboarding: new hires can access toolchains and knowledge quickly.
* Self-service with guardrails: provision resources safely without manual infra intervention.
* Governance and compliance: templates and workflows enforce standards.

<Frame>
  <img alt="A presentation slide titled &#x22;IDPs – Benefits&#x22; showing seven numbered cards with colorful icons and short labels like Streamlined accessibility, Effective documentation, Enhanced collaboration, Accelerated development, Faster onboarding, Self-service capabilities, and Governance." />
</Frame>

Backstage’s role is to provide the foundation for building an IDP. It is an open source platform that offers:

* A searchable software catalog.
* A documentation hub and tech docs integration.
* Templates and scaffolding for consistent project creation.
* Plugins to integrate with CI/CD, cloud providers, observability, and more.
* UI components and workflows for governance and self-service.

Throughout this lesson series, think of Backstage as the tool to build a single-pane-of-glass developer portal that directly addresses the fragmentation and friction we’ve covered.

Useful references

* Backstage (official): [https://backstage.io/](https://backstage.io/)
* Backstage Catalog concepts: [https://backstage.io/docs/features/software-catalog/what-is-the-catalog](https://backstage.io/docs/features/software-catalog/what-is-the-catalog)
* Internal Developer Portal guidance: [https://cloud.google.com/solutions/internal-developer-portal](https://cloud.google.com/solutions/internal-developer-portal)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/63b3da56-6a9c-43f4-b93e-74bb3614c527" />
</CardGroup>
