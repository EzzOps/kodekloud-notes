# block-buster
An enhanced version of the Block Buster Brick Breaker game with advanced features
```

When you try to commit to the protected `main` branch, GitHub prevents the direct commit and offers to create a new branch with your changes and open a pull request. Because the bypass list was left empty, even repository administrators must follow the same PR-based workflow.

If you proceed by creating a branch and editing a source file (for example adding a line to `script.js`), the changes will be committed to the new branch and a pull request will be created.

Example change in `script.js`:

```javascript theme={null}
// ==== GAME STATE ====

const gameState = {
    currentLevel: 1,
    score: 0,
    highScore: localStorage.getItem('blockBusterHighScore') || 0,
    lives: 3,
    isPaused: false,
    isGameRunning: false,
    balls: [],
    particles: [],
    bullets: [],
    activePowerups: [],
    powerups: {
        multiBall: { active: false, activationTime: 0 },
        megaPaddle: { active: false, activationTime: 0 },
        bulletMode: { active: false, activationTime: 0 }
    },
    bulletFireCounter: 0
};

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let paddle = {
    x: (canvas.width - 100) / 2,
    y: canvas.height - 25
};
```

When you push the branch, GitHub will pre-fill the pull request title and description based on your commit and branch name.

<Frame>
  <img alt="This image shows a GitHub interface for creating a pull request, with options to add a title, description, and reviewers. The title field is populated with &#x22;Update script.js.&#x22;" />
</Frame>

If a `CODEOWNERS` file is present, GitHub automatically requests reviews from the listed code owners (in this demo, Alice is assigned). The PR UI will clearly indicate required reviews and any other merge prerequisites.

<Frame>
  <img alt="The image shows a GitHub pull request page for updating the script.js file in a repository. It indicates the request is open, awaiting review, and requires at least one approving review to merge." />
</Frame>

## Required checks and merging

Required status checks—such as CI builds, linters, or CodeQL scans—run automatically as part of the PR. The pull request cannot be merged until both of the following conditions are met:

* The configured minimum number of approving reviews have been provided.
* All required status checks (for example, code scanning workflows) have completed and passed or otherwise met the configured criteria.

Once those conditions are satisfied, the merge button becomes available. Changes will be merged using whichever merge methods you allowed in the ruleset (merge, squash, or rebase).

## Links and references

* [Branch protection rules — GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
* [CODEOWNERS — GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
* [CodeQL — GitHub Docs](https://docs.github.com/en/code-security/code-scanning/using-code-scanning-with-codeql/about-code-scanning-with-codeql)
* [GitHub Actions — GitHub Docs](https://docs.github.com/en/actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/92adbba3-4e90-404b-9c11-790e5830373f" />
</CardGroup>


# Demo Create a GitHub Organization

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Demo-Create-a-GitHub-Organization/page

Guide to creating a GitHub organization and managing repositories, teams, permissions, plans, and governance for collaboration.

In this lesson you'll create a GitHub organization and learn how to centrally manage repositories, teams, and permissions. Organizations provide a shared workspace to manage access, apply governance, and coordinate collaboration across multiple people and projects.

Prerequisites:

* An active GitHub account (personal or business).
* An email address you can access for verification and invitations.

To get started, open your GitHub account, click your profile image, and select Organizations.

<Frame>
  <img alt="This image shows a GitHub profile page with several repositories listed, including a public template for a game and some private repositories. The user menu is also open on the right side." />
</Frame>

Step-by-step: Create an organization

1. Click Create Organization from the Organizations page. GitHub will present plan options: Free, Team, or Enterprise. Choose the plan that fits your team size and governance needs—Free is often sufficient for small teams and personal projects, while Team and Enterprise add advanced collaboration, security, and compliance features.

<Frame>
  <img alt="The image shows a webpage displaying GitHub's pricing plans for organizations, including Free, Team, and Enterprise options, each with different features and monthly costs." />
</Frame>

Quick comparison of organization plans

| Plan       | Best for                            | Key features                                                                 |
| ---------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| Free       | Individuals and small teams         | Unlimited public/private repos, limited Actions minutes, basic collaboration |
| Team       | Growing teams                       | Advanced access controls, team sync, more Actions minutes, code owners       |
| Enterprise | Organizations with governance needs | Advanced security, SSO, enterprise policies, organization-wide controls      |

2. For this demo, select the Free plan. Enter a unique organization name and a contact email. If the name is already taken, GitHub will prompt you to choose another. You’ll also choose whether the organization belongs to your personal account or a business account.

3. Verify ownership and confirm details. Depending on account settings, verification may occur via email, SSO, or other methods. You can also invite members during setup; invited users will receive an invitation email that they must accept to join.

<Frame>
  <img alt="This image shows a GitHub confirmation page where a user is prompted to verify their identity, with options to enter a code or receive assistance via email." />
</Frame>

<Callout icon="lightbulb">
  Invited members must accept the invitation sent to their email before they appear as members of the organization. Until they accept, invitations will show as pending.
</Callout>

After verification and accepting the Terms of Service, your organization will be created. You can invite additional members later and organize them into teams, assign repository permissions, enforce branch protection rules, and set up issue and PR assignment workflows.

<Frame>
  <img alt="The image shows a GitHub organization page for &#x22;Pixelcraft-Studio-kk&#x22; with options for managing repositories, permissions, and collaborative tasks. There's a message indicating that two members have been invited." />
</Frame>

Repositories and next steps

* If this is a new organization, the Repositories tab may show a message indicating there are no repositories yet. You can create a new repository directly under the organization or transfer existing repositories into it.
* Once you have repositories, start by configuring teams and repository permissions, branch protection, code owners, and CI/CD (GitHub Actions) as needed.

<Frame>
  <img alt="The image shows a GitHub organization's repository page with the message &#x22;This organization has no repositories.&#x22;" />
</Frame>

Resources and further reading

* [GitHub Organizations documentation](https://docs.github.com/en/organizations)
* [Managing organization settings and policies](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-team-access-to-an-organization)
* [GitHub Plans and Pricing](https://github.com/pricing)

<Callout icon="warning">
  If you choose a paid plan (Team or Enterprise), review billing and SSO/SSO provisioning requirements before upgrading to avoid unexpected costs or access changes.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/fc2abae3-5b73-4b29-9cce-5f52d584774b" />
</CardGroup>
