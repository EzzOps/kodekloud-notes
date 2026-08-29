# Demo Describe the Features of the User Profile

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Entities/Demo-Describe-the-Features-of-the-User-Profile/page

Guide to GitHub user profile features and customization including profile README, pinned repositories, contributions calendar, achievements, contact details, and tips for curating a public presence

This guide walks through the primary features of a GitHub user profile: what you can customize, how profile READMEs work, how contributions and achievements appear, and quick tips for curating your public presence on GitHub.

I’m signed into GitHub in a browser with a newly created account. The account was created only a few hours ago, so it currently has no public repositories and no visible contributions. You can edit profile details directly from your profile page or the Settings menu, but first let’s inspect a more active profile to understand the typical features and layout.

To find users, repositories, or other content on GitHub, use the global search. In this example, I searched for a user named “Coding Joe” so we can review a profile with clear activity and metadata.

<Frame>
  <img alt="This image shows a GitHub profile page for a user named &#x22;codingjoe,&#x22; featuring a profile picture, bio, and details about packages and projects related to Django and Python." />
</Frame>

## Profile header and contact details

The top of a profile lets you present your public identity on GitHub. Typical editable fields include:

| Field                        | Purpose                                                    | Where to edit                  |
| ---------------------------- | ---------------------------------------------------------- | ------------------------------ |
| Profile picture              | Visual identity for comments and commits                   | Edit profile                   |
| Display name                 | How your name appears across GitHub (e.g., Johannes Maron) | Edit profile                   |
| Username                     | Your unique GitHub handle shown in URLs and mentions       | Account creation / Settings    |
| Bio / About                  | Short description of who you are, your focus, and links    | Edit profile or profile README |
| Location / Time zone / Email | Optional contact details                                   | Edit profile                   |
| Website & social links       | Link to personal site, Twitter, LinkedIn, etc.             | Edit profile                   |

Scrolling further down a profile reveals a Sponsoring and Sponsors section. GitHub supports sponsorship for maintainers and projects; you can sponsor others or be sponsored. Sponsorship is a broader topic—see the GitHub Sponsors docs for details.

Profiles also display achievements—automatic badges earned for milestones and special contributions (for example, an Arctic Code Vault Contributor badge or a badge for co-authoring commits that are merged). Badges are granted automatically when criteria are met.

Profiles list organizations you belong to and include an optional profile README (the “About” section) where you can provide a richer introduction, links, project highlights, or even a mini portfolio.

<Frame>
  <img alt="The image shows a GitHub profile summary featuring achievements, highlights, organizations, and details of various Python and JavaScript repositories, including package versions, licenses, and download statistics." />
</Frame>

## Pinned repositories and the repository list

Pinned repositories let you curate which projects appear on the front of your profile. If you have many repositories, pinning ensures visitors see the projects you want to highlight first. Below the pinned section, GitHub lists all repositories you own and shows counts for Repositories, Projects, Stars, and Sponsors.

<Frame>
  <img alt="The image shows a GitHub profile page with pinned repositories and a contributions graph. The repositories are mainly related to Django projects in Python." />
</Frame>

## Contributions calendar and activity

The contributions calendar (heatmap) visualizes activity throughout the year. Each cell represents contributions for a specific date. If you’ve been active for multiple years, GitHub displays separate heatmaps for each year. Below the calendar, a detailed activity timeline summarizes recent commits, PRs, issues, and reviews.

<Frame>
  <img alt="The image is a screenshot of a GitHub contributions page showing a calendar heatmap of coding activity over the past year, along with an activity overview chart displaying the percentages of commits, pull requests, code reviews, and issues." />
</Frame>

Stars are a bookmarking and discovery feature: starring a repository signals interest and adds it to your starred list. You can browse another user’s starred repositories and star them yourself; starred repos can be organized into lists.

## Quick actions and profile settings

Because my account is new, my profile shows very little information. To add details to your profile:

* Click Edit profile on your profile page or open Settings > Public profile.
* Add your name, bio, pronouns, company, location, time zone, email, and social links.
* Pin repositories you want visitors to see first.

I updated the displayed name to Siddharth Barahalikar and saved the profile — this display name appears across GitHub when I contribute or when people mention me. You can change this later at any time.

> **warning** Avoid exposing sensitive personal information (like private email addresses or exact home addresses) in your public profile or README. Use links to controlled contact channels instead.

## Profile README — make your profile more engaging

One of the most powerful profile features is the profile README. To create a profile README:

1. Create a **public** repository whose name exactly matches your GitHub username.
2. Initialize it with a `README.md` file.
3. Edit `README.md` with whatever content you want to display on your profile (Markdown, badges, images, tables, etc.).

For example, I created a public repository named `sid-gh900` and initialized it with a README.

<Frame>
  <img alt="The image shows a GitHub screen for creating a new repository with options to add a description, choose visibility, add a README, a .gitignore, and a license. There's a dropdown menu displaying visibility options for either public or private access." />
</Frame>

> **lightbulb** To make a profile README appear on your public profile: create a public repository whose name exactly matches your GitHub username, initialize it with a `README.md`, and then edit that README to contain the content you want displayed on your profile.

After creating the repository, GitHub recognizes it as the special profile repository and shows a note to that effect.

<Frame>
  <img alt="The image shows a GitHub repository page named &#x22;sid-gh900/sid-gh900&#x22; with a README file that says &#x22;Hi there 👋&#x22;. It indicates this is a special repository that appears on the owner's public profile." />
</Frame>

You can edit the README directly in GitHub’s online editor: modify the Markdown, preview it, and commit the changes to the repository’s default branch (usually `main`).

<Frame>
  <img alt="This image shows a GitHub repository page with the user editing the README.md file. The interface displays the code editor and some template text inside the file." />
</Frame>

After committing your changes, the README renders on your public profile. Use Markdown for headings, tables, badges, images, and layout to create a professional-looking introduction, project highlights, or a mini-portfolio.

<Frame>
  <img alt="The image shows a GitHub user profile page with a username &#x22;siddharth-gh-newbie,&#x22; featuring a placeholder profile picture and a README section describing an aspiring software developer's learning goals and projects." />
</Frame>

## Final notes and next steps

* Add repositories and make contributions to populate the contributions graph and repository list.
* Use the profile README to surface your most important projects and information.
* Pin repositories to highlight the work you want visitors to see first.
* Consider exploring GitHub Sponsors if you maintain open source projects and want to accept funding.

Further reading:

* GitHub Docs — Profile README: [https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-your-profile-readme](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-your-profile-readme)
* GitHub Docs — GitHub Sponsors: [https://docs.github.com/en/sponsors](https://docs.github.com/en/sponsors)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/568cc659-10e8-4a0c-949d-77f390d59838/lesson/d868d192-fa6d-4eb7-b449-6bbc52004bc3)
