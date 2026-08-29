# Demo Describe Members Teams and Roles in a GitHub Organization

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Demo-Describe-Members-Teams-and-Roles-in-a-GitHub-Organization/page

Explains GitHub organization roles, members, outside collaborators, teams, and repository permissions and how to manage access and settings via the GitHub user interface.

In this lesson we'll explain how people are organized and granted access inside a GitHub organization. You'll learn how Owners, Members, Outside Collaborators, and Teams relate to repositories and permissions, and where to manage these settings in the GitHub UI.

## Viewing organization people

To inspect who belongs to an organization, open the organization’s People tab. Members are grouped into Owners and Members; Outside Collaborators are listed separately. Use the membership-type filters to locate Owners, Members, or Outside Collaborators quickly.

<Frame>
  <img alt="The image shows a GitHub organization page with a list of members, their roles, and two-factor authentication status. The interface is dark-themed and includes an &#x22;Invite member&#x22; button." />
</Frame>

## Organization roles: Owners

Owners have full administrative control across the organization: they manage teams, member settings, billing, policies, and can delete the organization. The user who creates the organization is an Owner by default. Limit Owner assignments to trusted administrators.

<Frame>
  <img alt="The image shows a GitHub organization page titled &#x22;Pixelcraft-Studio-kk,&#x22; displaying a member list where one user, marked as an owner with two-factor authentication enabled, is present." />
</Frame>

## Members: default and effective permissions

Organization Members receive the organization’s default repository permission (commonly `Read`), which you can configure. A member’s effective permissions may be raised or restricted by:

* Team memberships (teams can grant broader repo access).
* Repository-level collaborator settings (Manage access / Collaborators & teams).
* Organization or repository policy restrictions.

Open a member’s profile and select **Manage access** to review the repositories they can access and their permission levels.

<Frame>
  <img alt="The image shows a GitHub organization page for &#x22;Pixelcraft-Studio-kk,&#x22; displaying a member profile with access details and security settings." />
</Frame>

## Repository-level permissions

Repository permissions are managed from the repository **Settings → Collaborators & teams** (or **Manage access**). There you can add or remove collaborators, change roles, and create or assign custom roles when available.

<Frame>
  <img alt="The image shows a GitHub repository access settings page for &#x22;Pixelcraft-Studio-kk/block-buster,&#x22; indicating specific user permissions for reading, writing, and admin access. The user has active read access, but no explicit write or admin permissions." />
</Frame>

<Frame>
  <img alt="The image shows a GitHub repository settings page focused on managing access, with options for direct and organization access, and a role selection dropdown. Various user permissions like &#x22;Read,&#x22; &#x22;Triage,&#x22; and &#x22;Write&#x22; are displayed, along with an option to create custom roles." />
</Frame>

Summary of common repository roles:

| Role     | Typical use        | Effect                                                      |
| -------- | ------------------ | ----------------------------------------------------------- |
| `Read`   | View code & issues | Clone and read-only access                                  |
| `Triage` | Manage issues/PRs  | Issue/PR management without write to code                   |
| `Write`  | Contribute code    | Push changes and merge PRs (depending on branch protection) |
| `Admin`  | Full repo control  | Manage settings, collaborators, webhooks                    |

For more details, see the official GitHub documentation on repository permissions: [Managing repository access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories).

## Outside collaborators

Outside collaborators are users who have access to one or more repositories but are not organization Members. This is useful for contractors, temporary contributors, or external partners. From the People tab you can view the repos they can access, invite them to become full organization Members, or remove their access.

<Frame>
  <img alt="The image shows a GitHub organization page for &#x22;Pixelcraft-Studio-kk,&#x22; with a user named &#x22;sidd-harth-1&#x22; listed as an outside collaborator who has access to one repository. There are options to invite the user to the organization or remove access." />
</Frame>

<Callout icon="lightbulb">
  Use outside collaborators to grant repository-scoped access without making someone a full organization Member. Invite them as Members only when they need broader organization-level privileges.
</Callout>

## Teams: group-based access and notifications

Teams let you group Members to manage repository access, notifications, and mentions efficiently. Typical workflows:

* Give `UI-Team` write access to front-end repositories.
* Give `Backend-Team` admin or write access to API repositories.
* Mention a team in an issue or PR to notify all team members with a single handle.

To create a team, supply a name, description, visibility (visible or secret), and notification settings. Teams can also be organized into parent/child hierarchies.

<Frame>
  <img alt="The image shows a GitHub interface for creating a new team, with fields for team name, description, visibility, and notifications settings. The team is named &#x22;UI-Team&#x22; with a description related to UI repositories." />
</Frame>

When you create a team, the creator is added as a team maintainer by default. You can invite additional members and assign other maintainers to manage the team.

<Frame>
  <img alt="This image shows a GitHub team page for &#x22;UI-Team&#x22; under the organization &#x22;Pixelcraft-Studio-kk,&#x22; listing a member named &#x22;sid-gh900.&#x22; The interface includes options for managing team members and roles." />
</Frame>

Teams support features such as flexible repository access scopes, team join requests, and team mentions.

<Frame>
  <img alt="The image is a GitHub interface overview for team features, highlighting flexible repository access, team requests, and team mentions. The page includes options to add a team and learn more." />
</Frame>

Once a team and its members are in place, you can mention the team in issues, pull requests, and comments to notify everyone in the group at once. Use the team handle format, for example: `@org/UI-Team`.

<Frame>
  <img alt="The image shows a GitHub page titled &#x22;Seamless communication with teams,&#x22; highlighting features for team collaboration, and includes a section for managing teams, with one team called &#x22;UI-Team&#x22; selected." />
</Frame>

<Callout icon="warning">
  Grant Owner status sparingly. Prefer teams and repository-level roles to minimize blast radius and adhere to the principle of least privilege.
</Callout>

## Quick reference

* Owners = full organization control — limit assignments.
* Members = organization-scoped users with a default repo permission.
* Outside collaborators = repo-scoped access without organization membership.
* Teams = group-based access, notifications, and easier management.

For additional reading and step-by-step UI guidance, visit:

* [GitHub Organizations documentation](https://docs.github.com/en/organizations)
* [Manage access to your repositories](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/054b8c5d-f32f-49bd-8560-0ee508f60e93" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/68336c1d-1db8-440d-be9c-34d29ee8d4d2" />
</CardGroup>
