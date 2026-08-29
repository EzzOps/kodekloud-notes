# HCP Terraform Teams Permissions

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/HCP-Terraform-Teams-Permissions/page

Explains HCP Terraform user, team, and permissions models including scope hierarchy, role based access, Owners team, team visibility, tokens, and best practices.

Welcome back.

In this lesson we will cover HCP Terraform teams and permissions so you understand how access is modeled and enforced within the platform.

I’ll assume you already know basic concepts of users, teams, and permissions from other platforms. What matters here is how HCP Terraform structures and applies those concepts.

Users and organizations

A user in HCP Terraform is an individual account tied to an email address — for example, Sarah. A single user can belong to multiple organizations. In other words, Sarah might be a member of a training organization, a development organization, and her own personal organization. Each organization is an isolated environment with its own workspaces, teams, and permissions. What Sarah can do in one organization does not affect what she can do in another.

You can think of it like a GitHub account: a single personal account that can be added to different organizations.

<Frame>
  <img alt="The image illustrates the structure of HCP Terraform users, showing an account linked to multiple organizations: Training, Development, and Personal. It uses a purple color scheme and includes an abstract person icon and email." />
</Frame>

Teams and scope of access

Within an organization, users are grouped into teams. Teams are the primary unit for assigning access because permissions are normally granted to teams rather than to individual users.

Consider two common approaches:

* Granting a team access at the project level so it automatically covers every workspace in that project (including future ones).
* Granting a team access to specific workspaces for a more granular control, useful for sensitive infrastructure like networking.

Both patterns are valid and often used together depending on organizational needs.

<Frame>
  <img alt="The image is a diagram depicting HCP Terraform teams, showing the Mobile App Team and Network Engineering Team, along with their respective projects and workspaces within an HCP Terraform Organization." />
</Frame>

Access model summary

* Users → belong to teams.
* Teams → receive permissions.
* Permissions → determine what actions a team (and therefore its members) can perform.

Granting permissions at the team level simplifies administration and scale.

<Frame>
  <img alt="The image explains the access control hierarchy, featuring three components: &#x22;Users,&#x22; &#x22;Teams,&#x22; and &#x22;Permissions,&#x22; each with a brief description." />
</Frame>

Key rules and best practices

* Permissions are additive. HCP Terraform grants the most permissive effective permission a user has across all their teams. For example, if one team provides read and another provides write to the same workspace, the user receives write access.
* Apply the principle of least privilege. Only grant teams the permissions they actually need, because permissions stack across multiple team memberships.
* Every organization has an Owners team with full admin access across the organization (workspaces, projects, policies, VCS settings, private registry, run tasks, etc.). Owners can manage everything and cannot be deleted. Keep Owners membership small and audit it regularly.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;The Owners Team,&#x22; outlining administrative tasks such as managing policies, workspaces, private registries, VCS settings, policy overrides, and run tasks. It indicates that the Owners team has full admin access in an organization." />
</Frame>

Team visibility and tokens

* Team visibility: Teams can be visible (any organization member can see the team and its membership) or secret (only the team members and organization owners can see it). Secret teams are useful for sensitive groups such as security or incident response teams.
* Team API tokens: Each team can generate API tokens for automation (CI/CD, scripts). A team token inherits the same permissions as the team itself. Historically there was a limit of a single token per team, but HCP Terraform now allows multiple team tokens per team (GA feature).

<Frame>
  <img alt="The image is a presentation slide titled &#x22;HCP Terraform Teams,&#x22; detailing team visibility options (Visible and Secret) and information about team tokens for API operations on workspaces." />
</Frame>

Permission levels (scope hierarchy)

Permissions in HCP Terraform are defined at three levels:

* Organization-level: Broad permissions that apply across the organization (e.g., managing workspaces, policies, VCS settings). The Owners team typically holds these privileges, but you can grant specific organization-level permissions to other teams.
* Project-level: Scoped to a project and all workspaces inside it. Roles can be preset (read, plan, write, admin) or custom. Granting project-level access is an efficient way to manage multiple related workspaces.
* Workspace-level: The most granular scope. Preset roles include read, plan, write, admin, or you can define custom permissions. To perform an apply action, a user/team needs write permission on that workspace.

Remember: permissions are additive across these levels — the most permissive role wins for any given workspace.

<Frame>
  <img alt="The image outlines the hierarchy of organization, project, and workspace permissions, detailing what each level manages and controls. It includes descriptions of permissions at each level, such as manage, read, write, and custom options." />
</Frame>

Practical example

Imagine an organization where the Owners create three teams: AppOne, Mobile, and X. Only owners or those with team management permissions can create teams and assign roles.

* AppOne team:
  * Plan access on production AppOne workspaces (they can queue runs/plans but cannot apply).
  * Write access on dev workspaces (they can plan and apply in dev).

* Mobile team:
  * Write access on dev mobile workspaces (plan and apply).
  * Plan-only access on mobile production workspaces (need approval to apply).

This is a common pattern: tighter controls in production and more permissive access in development. This illustrates role-based access control (RBAC) in practice — assigning the minimum necessary privileges per team and environment.

<Frame>
  <img alt="The image is a diagram explaining Role-Based Access Control (RBAC) for HCP Terraform, showing the hierarchy and permissions of an organization owner and various teams managing different workspaces." />
</Frame>

Exam-focused summary (Terraform Associate)

Make sure you understand:

* The relationship between users, teams, and permissions: users join teams; teams receive permissions.
* Every organization has an Owners team with full access; it cannot be deleted.
* The three permission scopes: organization, project, and workspace.
* Permissions are additive: HCP Terraform grants the highest effective permission a user has across team memberships and scopes.

If you grasp those concepts, you'll be well prepared for exam questions about teams and permissions.

Related topic

A related topic is the private registry — how your organization can share reusable Terraform modules and providers internally.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/e7a977ec-0bc3-4a3f-9736-206462982f6b" />
</CardGroup>
