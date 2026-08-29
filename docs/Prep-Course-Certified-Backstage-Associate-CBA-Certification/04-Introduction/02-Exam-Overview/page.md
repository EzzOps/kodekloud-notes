# Copy dotfiles (use a glob that excludes '.' and '..'). The command may fail
# if no dotfiles are present, so the '|| true' prevents an error in such cases.
cp -r ~/template-lab-skaffold/.[!.]* ~/backstage/templates/skaffold/ || true
```

> **warning** If your source folder contains no dotfiles (hidden files beginning with `.`), the `cp` glob may fail. The `|| true` in the command prevents the script from exiting with an error in that case.

## Course structure — what you'll learn

The course is organized so you build from fundamentals to production operations. Below is a high-level map of modules and core topics.

| Module                  | Key Topics                                                             |
| ----------------------- | ---------------------------------------------------------------------- |
| Backstage Fundamentals  | Overview, architecture, benefits, use cases                            |
| Catalog & Entities      | Registering components, entity kinds, relationships                    |
| Scaffolding & Templates | Creating templates, standardizing component creation, automation       |
| TechDocs & Search       | Writing TechDocs, configuring search and documentation discoverability |
| Plugins & UI            | Custom UI, creating and integrating plugins, sidebar/navigation        |
| Operations & Deployment | DB configuration, authentication, Docker, deployment strategies        |
| Exam Prep & Labs        | Practice exercises, exam-style questions, readiness checklist          |

<Frame>
  <img alt="A slide titled &#x22;Backstage Architecture&#x22; showing frontend and backend boxes with Catalog and GitLab plugin blocks, arrows to a GitLab logo and a database icon. A small circular video thumbnail of a speaker appears in the bottom-right corner." />
</Frame>

This architecture diagram highlights the split between the Backstage frontend and backend, integrations (e.g., GitLab), and persistent storage. Understanding these components helps you plan deployments and integrations.

You will learn how to use Backstage's Catalog to define and manage entities — registering components, systems, domains, APIs, and more — and how relationships between entities model your organization’s software landscape.

<Frame>
  <img alt="A presentation slide titled &#x22;Exploring Other Entity Kinds&#x22; showing hexagonal icons for Users, Groups, Templates, Systems, Domains and a central &#x22;Entity&#x22; tile. A small circular video of a presenter appears in the bottom-right corner." />
</Frame>

Templates and scaffolding standardize how teams create services and infrastructure. We'll walk through creating and using templates so teams consistently provision repos, CI/CD, and infrastructure.

<Frame>
  <img alt="A screenshot of a GitHub repository page showing the &#x22;backstage-templates/templates&#x22; folder with several .yaml files (the cursor pointing at api-template.yaml). A small circular video feed of a presenter appears in the bottom-right." />
</Frame>

Doc-driven development becomes easier with TechDocs and search. You'll configure TechDocs to publish documentation from source (Markdown) and tune Backstage search so teams find the information they need fast.

<Frame>
  <img alt="A presentation slide titled &#x22;Search&#x22; with a teal stacked logo on the left and a rounded info card labeled &#x22;Main Benefits&#x22; containing an illustration of a developer. A small circular webcam feed showing a person's face appears in the bottom-right corner." />
</Frame>

You will also learn how to customize the UI and extend Backstage through plugins. Building plugins allows you to integrate tools, surface custom reports, and adapt Backstage to your organization’s workflows.

Here is an example JSX snippet showing how sidebar items can be defined in a Backstage app. This demonstrates common navigation entries (Docs, Create, Register) and a Settings group:

```jsx theme={null}
<SidebarItem icon={LibraryBooks} to="docs" text="Docs" />
<SidebarItem icon={CreateComponentIcon} to="create" text="Create..." />
<SidebarItem icon={RegisterIcon} to="catalog-import" text="Register" />
{/* End global nav */}
<SidebarDivider />
<SidebarScrollWrapper>
  {/* Items in this group will be scrollable if they run out of space */}
</SidebarScrollWrapper>
</SidebarGroup>
<SidebarSpace />
<SidebarDivider />
<SidebarGroup label="Settings" icon={<UserSettingsSignInAvatar />} to="/settings">
  {/* Settings items go here */}
</SidebarGroup>
```

Finally, we'll cover essential production topics: database configuration, authentication and SSO, secrets management, logging and monitoring, and deployment options (including Docker and Kubernetes patterns) so you can operate Backstage reliably at scale.

By the end of this course you will be ready to deploy and operate Backstage, build and integrate plugins, author templates, manage the Catalog, and publish TechDocs — and you'll be well-prepared to take the Certified Backstage Associate exam.

## Links and references

* [Backstage official site — Backstage.io](https://backstage.io)
* [Backstage — The Software Catalog](https://backstage.io/docs/features/software-catalog)
* [TechDocs — Backstage documentation](https://backstage.io/docs/features/techdocs/what-is-techdocs)
* KodeKloud community forums — connect with peers, ask questions, and share progress

Join our KodeKloud community to collaborate with fellow learners and get help as you practice the labs and prepare for the exam.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/aa692961-a0a1-49f4-b0c5-d3af3b5afb4b/lesson/42f973bf-4500-4f5d-b13b-24b64f62ed7f)


# Exam Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Introduction/Exam-Overview/page

Overview of the Certified Backstage Associate exam format, domains, weights, and key competencies to study, with study tips and links to Backstage documentation.

This lesson summarizes the Certified Backstage Associate (CBA) exam format and the exam domains you should focus on. Read through each domain to understand the competencies tested and its approximate weight toward your final score.

The exam is proctored online and timed at 90 minutes. Questions are multiple-choice with a single correct answer. There are no hands-on or lab-based tasks — you will not be required to log into any terminals. If you pass, the certification is valid for two years.

> **lightbulb** The exam is 90 minutes long, proctored online, multiple-choice (single answer), with no lab exercises. The certification remains valid for two years after passing.

Exam domains at a glance:

|                         Domain | Weight | Core focus                                                                                                                                 |
| -----------------------------: | :----: | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Backstage Development Workflow |   24%  | Local development, TypeScript build and tooling, npm/Yarn dependency management, and building Docker images of Backstage apps.             |
|       Backstage Infrastructure |   22%  | Backstage configuration, deployment to production, and understanding client–server architecture and component interactions.                |
|              Backstage Catalog |   22%  | Using and populating the software catalog, annotations, entity registration (manual & automated), and troubleshooting ingestion pipelines. |
|          Customizing Backstage |   32%  | Frontend vs backend plugins, creating and modifying plugins, React and Material-UI usage, and theming/backstage UI customization.          |

Below are expanded summaries for each domain with the specific competencies to prioritize when preparing.

Backstage Development Workflow — 24%

* Build and run Backstage projects locally (create-app flow and local dev servers).
* TypeScript compilation and troubleshooting typical TypeScript issues.
* Install and manage dependencies using `npm` and Yarn across Backstage packages.
* Use Docker to containerize a Backstage app and understand basic Dockerfile patterns for Backstage services.

<Frame>
  <img alt="A presentation slide titled &#x22;Domains & Competencies&#x22; with a donut chart highlighting 24% for &#x22;Backstage Development Workflow.&#x22; To the right is a rounded box listing related skills like building and running Backstage projects locally, compiling with TypeScript, installing dependencies with NPM/Yarn, and using Docker." />
</Frame>

Backstage Infrastructure — 22%

* Know the Backstage framework components and where configuration lives (`app-config.yaml` and environment layering).
* Deploy Backstage to production environments (container orchestration basics, reverse proxies, and static asset serving).
* Understand the client–server architecture: how the frontend communicates with backend plugins and service discovery patterns.

<Frame>
  <img alt="A presentation slide titled &#x22;Domains & Competencies&#x22; with a donut chart highlighting a 22% slice for &#x22;Backstage Infrastructure.&#x22; Beside it is a purple-bordered box listing competencies: understand the Backstage framework, configure Backstage, deploy it to production, and understand its client‑server architecture." />
</Frame>

Backstage Catalog — 22%

* Understand the purpose of the Backstage software catalog and when to use it.
* Populate the catalog with applications, components, and organizational entities using YAML descriptors.
* Use annotations and register entity locations both manually and via automated discovery/ingestion.
* Troubleshoot entity ingestion issues and configure automated ingestion pipelines.

<Frame>
  <img alt="A slide titled &#x22;Domains & Competencies&#x22; showing a donut chart with a 22% slice labeled &#x22;Backstage Catalog.&#x22; A blue-green box lists Backstage Catalog competencies like understanding and populating the catalog, using annotations, and troubleshooting/manual/automated entity ingestion." />
</Frame>

Customizing Backstage — 32%

* Distinguish between frontend and backend plugins and know typical responsibilities for each.
* Create and customize plugins (frontend and backend) to add functionality and integrations.
* Modify React code within a Backstage app to add features and change appearance.
* Use Material-UI components and layout primitives to extend and standardize the UI.
* Apply theming and design tokens to adjust the overall look-and-feel of your Backstage instance.

<Frame>
  <img alt="A presentation slide titled &#x22;Domains & Competencies&#x22; with a donut chart highlighting &#x22;Customizing Backstage&#x22; at 32%. To the right, a green panel lists bullet points about frontend vs backend plugins, customizing Backstage plugins, editing React code in the Backstage app, and using Material‑UI components." />
</Frame>

Study tips

* Map your study time to the domain weights — allocate more time to Customizing Backstage (32%) and Development Workflow (24%).
* Practice local development flows: scaffold an app, run the dev server, add a simple plugin (frontend and backend), and build a Docker image.
* Read the official Backstage docs and examine example plugins to understand patterns and conventions.

Links and references

* [Backstage Documentation](https://backstage.io/docs/)
* [Backstage GitHub Repository](https://github.com/backstage/backstage)
* [Backstage Software Catalog Guide](https://backstage.io/docs/features/software-catalog)

Focus your review on the competencies listed under each domain to prepare effectively for the exam. Good luck with your preparation!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/aa692961-a0a1-49f4-b0c5-d3af3b5afb4b/lesson/e024f866-4cb2-4435-a611-90e349547970)
