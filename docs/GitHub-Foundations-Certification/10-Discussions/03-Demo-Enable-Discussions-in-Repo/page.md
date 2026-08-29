# Demo Enable Discussions in Repo

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Discussions/Demo-Enable-Discussions-in-Repo/page

How to enable and use GitHub Discussions in a repository, create and categorize the first discussion, manage moderation, and follow best practices for community conversations.

[GitHub Discussions](https://docs.github.com/en/discussions) provide a structured forum for repository communities to have broader conversations that don't fit into issues or pull requests. Use Discussions for brainstorming, Q\&A, polls, announcements, and showcasing work.

> **lightbulb** Use Discussions for general conversation, brainstorming, polls, Q\&A, and announcements that don't fit as issues or pull requests.

## What you'll do in this lesson

1. Open the repository (example: `block-buster`) with an account that has repository settings access (example user: `AZ-1000`).
2. Enable Discussions from the repository Settings.
3. Create the first discussion and choose an appropriate category.

### Quick prerequisites

* You must have repository settings access (Admin or maintain) to enable Discussions.
* Discussions are enabled per-repository; enabling in one repo does not enable them across an organization.

> **warning** You need repository-level settings access to enable Discussions. If you don’t see the Discussions option in Settings, confirm your permission level or contact a repository admin.

## Step 1 — Open repository and enable Discussions

1. Open your repository (for example `block-buster`) and sign in with an account that has repository settings access (e.g. `AZ-1000`).
2. Go to Settings → scroll to the Discussions section to enable it and configure defaults.

After enabling, you can immediately create the repository’s first Discussion.

<Frame>
  <img alt="The image shows the GitHub interface for starting a new discussion in the &#x22;block-buster&#x22; repository. It includes fields to add a discussion title and body, along with sample text and guidelines." />
</Frame>

When creating a discussion, GitHub shows a starter screen with a title and suggested body text. You can accept the defaults or customize the title, body, and labels. By default the first discussion is often posted to the Announcements category unless you choose another category (this default can vary by repository configuration).

## Discussion categories and when to use them

GitHub provides built-in categories so you can organize conversations by intent. Choose the category that best fits the content of your post.

<Frame>
  <img alt="The image shows a GitHub page where users can select a discussion category, with options like Announcements, General, Ideas, Polls, Q&A, and Show and tell. Each category has a &#x22;Get started&#x22; button." />
</Frame>

| Category      | Use case                                   | Example                                   |
| ------------- | ------------------------------------------ | ----------------------------------------- |
| Announcements | Official updates from maintainers          | New release notes or roadmap updates      |
| General       | Casual or miscellaneous project discussion | Community chat or off-topic items         |
| Ideas         | Proposals and brainstorming                | Feature suggestions and RFCs              |
| Polls         | Collect community votes                    | Choosing a default dependency or feature  |
| Q\&A          | Ask/answer support questions               | Troubleshooting, usage help               |
| Show and tell | Showcase work                              | Demos, screenshots, or completed projects |

## Step 2 — Create and publish the discussion

* Select the appropriate category (for this example, choose **Announcements**).
* Enter a clear title and body. Use formatting, code blocks, and links to make the post useful and searchable.
* Submit the discussion. After the first discussion is created, a Discussions tab appears in the repository navigation bar.

<Frame>
  <img alt="The image shows a GitHub Discussions page titled &#x22;Welcome to block-buster Discussions!&#x22; with confetti animation, indicating the creation of the first discussion in a repository." />
</Frame>

## Managing discussions

Once created, discussions behave similarly to issues and include moderation and management features:

* Pin important or featured discussions to keep them prominent.
* Lock conversations to prevent further replies when necessary.
* Convert or transfer a discussion to an issue for actionable items.
* Edit content and adjust labels or categories as needed.
* Use moderation tools to flag or remove inappropriate posts.

## Best practices and tips

* Choose clear, descriptive titles to improve discoverability.
* Use categories consistently so users can find content quickly.
* Encourage maintainers and community members to respond and close conversations when resolved.
* Convert long-running proposals or actionable items into issues to track implementation.

## Links and references

* [GitHub Discussions documentation](https://docs.github.com/en/discussions)
* [GitHub Community Moderation guidance](https://docs.github.com/en/site-policy)

Advanced moderation and detailed category configuration are important topics on their own and can be explored in separate lessons.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/f42f6458-b9ea-4ebb-8cbd-261b2393e622/lesson/a7e8fb2c-c076-4317-907e-151bd36a7eff)
