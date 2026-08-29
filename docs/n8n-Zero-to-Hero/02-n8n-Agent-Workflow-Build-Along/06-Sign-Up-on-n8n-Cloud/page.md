# Sign Up on n8n Cloud

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Agent-Workflow-Build-Along/Sign-Up-on-n8n-Cloud/page

Guide to creating an n8n Cloud account, configuring workspace settings, projects, and starting your first workflow.

Before we build workflows, let’s get your n8n Cloud workspace ready. If you plan to experiment in the KodeKloud n8n Data Environments, labs, or playgrounds first, you can skip creating a Cloud account for now — those environments already include everything you need.

<Callout icon="lightbulb">
  If you want to jump straight into building, feel free to skip registration and continue to the next lesson — the lab environment already provides everything needed.
</Callout>

1. Visit [n8n.io](https://n8n.io) and click Get Started to create a free account. Provide your credentials, complete the human verification, and submit the short onboarding questionnaire — it’s optional and doesn’t restrict functionality.

<Frame>
  <img alt="The image is a website landing page for n8n, highlighting AI workflow automation for technical teams with options to get started or talk to sales. It features a lightning bolt graphic and lists different use cases for various departments." />
</Frame>

2. The onboarding asks about the apps and integrations you expect to use. This only helps tailor suggestions — n8n gives access to all nodes regardless of your choices. Pick a few that match your use case.

<Frame>
  <img alt="The image shows a survey asking how the user heard about &#x22;n8n,&#x22; with options including Google, Twitter, LinkedIn, YouTube, and others. The chosen option is YouTube, and there is a submit button below the list." />
</Frame>

3. Invite teammates during onboarding if you want shared access to the workspace; otherwise skip and invite later from Settings → Users.

<Frame>
  <img alt="The image shows a screen prompting the user to invite team members to a workspace by entering their email. There are options to add more users, skip, or invite." />
</Frame>

4. Wait a minute for your workspace to provision. When it’s ready, click Start automating to open the workflow canvas and begin creating.

<Frame>
  <img alt="The image shows a notification that a workspace is ready, with a button to &#x22;Start automating.&#x22; Below, there is a YouTube video thumbnail for an &#x22;n8n Quick Start&#x22; tutorial." />
</Frame>

## Recommended billing and launch setup

Before you start building, open Settings and configure a few defaults. These improve collaboration, logging, and scheduling reliability.

The dashboard gives quick access to Projects, Settings, and sample flows to help you get started.

<Frame>
  <img alt="The image shows an interface of the n8n platform, displaying a dashboard with options to start a new project from scratch or test an AI agent. It includes a sidebar with options for projects, settings, and help." />
</Frame>

Personalization and basic profile

* Set UI theme to light or dark via Settings → Personalization and click Save.
* Confirm your name and email for audit trails and team visibility.

<Frame>
  <img alt="The image displays a personal settings page, showing fields for basic information such as first name and email, security options, and theme personalization. It also includes navigation options on the left for users, external secrets, environments, and other settings." />
</Frame>

Projects and folders

* Organize workflows using Projects and Folders. Create a folder like `Tutorials` or `Build-Along` to keep related workflows grouped.
* Add only the necessary members to a project to control access.

I created a project named Description Demo and saved it — you can replicate that project structure or adapt it for your team.

<Frame>
  <img alt="The image shows a software interface for managing projects, with options to set a project icon and name, add a description, and manage project members. There is also a &#x22;Danger zone&#x22; section for deleting the project and buttons for saving changes." />
</Frame>

Admin panel checklist

* Verify workspace-level settings (n8n version, time zone).
* Configure Executions to capture the execution logs you need (consider enabling all options while learning to make debugging easier).
* Enable Verified Community Nodes to broaden available integrations with community-contributed nodes.
* For teams, set up External Secrets and SSO as required.

Quick settings checklist

| Area       | Recommendation                                                            |
| ---------- | ------------------------------------------------------------------------- |
| Theme      | Set to `Light` or `Dark` in Settings → Personalization                    |
| Time zone  | Configure in Admin → Time zone so scheduled triggers run as expected      |
| Executions | Enable full logging during development to assist debugging                |
| Updates    | Cloud: automatic. Self-hosted: pull updates regularly (see warning below) |
| Nodes      | Enable `Verified Community Nodes` to access community integrations        |

<Callout icon="warning">
  If you self-host, plan a regular update cadence (for example, pull the latest Docker image weekly or monthly) to keep nodes, security patches, and new features current.
</Callout>

## Getting started with your first workflow

Once settings are saved, click Start from Scratch to open a blank canvas and begin building your first workflow. If you prefer testing in a sandbox, the KodeKloud playground n8n environment is a good alternative before committing to Cloud.

Note: Cloud accounts typically include a trial period (for example, you might see a `14-day trial` banner while evaluating n8n Cloud). Use the trial to explore features and decide whether to continue with Cloud or migrate to self-hosting later.

That completes setup. In the next lesson we’ll open the blank canvas and start building reliable workflows step by step.

Further reading and references

* n8n Documentation: [https://docs.n8n.io](https://docs.n8n.io)
* n8n Community: [https://community.n8n.io](https://community.n8n.io)
* KodeKloud n8n Playground (if applicable to your course)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/bb244392-b429-4a6d-b12e-e29ae7f27d5d" />
</CardGroup>
