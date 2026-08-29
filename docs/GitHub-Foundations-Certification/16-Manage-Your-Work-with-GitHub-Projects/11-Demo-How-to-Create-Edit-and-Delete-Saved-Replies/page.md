# Demo How to Create Edit and Delete Saved Replies

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Manage-Your-Work-with-GitHub-Projects/Demo-How-to-Create-Edit-and-Delete-Saved-Replies/page

Guide to create edit and delete personal GitHub saved replies and use them in issue and pull request comments to speed common responses

Saved replies let you convert repetitive issue and pull request responses into reusable snippets you can insert in a couple of clicks. This speeds up triage, onboarding messages, duplicate issue responses, and standard troubleshooting guidance across repositories.

In this guide you'll learn how to:

* Create saved replies in your personal settings
* Insert saved replies into issue and PR comment boxes
* Edit and delete saved replies when they are no longer needed

Repository view (starting point)

<Frame>
  <img alt="The image shows a GitHub repository page for a project called &#x22;block-buster,&#x22; which appears to be an enhanced version of a Brick Breaker game. The page lists several files, including index.html, script.js, and style.css, and mentions recent commits." />
</Frame>

When to use saved replies

* Use saved replies for routine acknowledgements (e.g., "thanks for the contribution"), standard next steps, or links to common resources.
* Saved replies reduce typing and help ensure consistent wording across team members who share an account.

Using saved replies in Issues and Pull Requests
You can insert saved replies directly from any issue or pull request comment box. Open a comment box, choose the "Saved replies" option (or the slash command if available), and pick the reply you want; it will be inserted into the editor so you can post it immediately or edit it first.

Example issue view showing where to add a comment:

<Frame>
  <img alt="This image shows a GitHub issue page titled &#x22;dummy title #2,&#x22; with options to add a comment, manage notifications, and track related activity. The interface includes buttons for editing and managing the issue." />
</Frame>

Where to create saved replies
Saved replies are created and managed in your personal GitHub settings. They are tied to your account, not to a specific repository.

> **lightbulb** Saved replies are personal to your GitHub account. After you create them, they will appear whenever you write comments on issues and pull requests for repositories you can access with that account.

Create (example) — Settings view
To add a saved reply:

1. Open GitHub and go to Settings → Codes & automation → Saved replies (or open the Saved replies section from your account settings).
2. Click Add saved reply (or a similar button).
3. Enter a short title and the response text you want to reuse.
4. Save it. The reply is now available in comment boxes.

Screenshot of adding a saved reply:

<Frame>
  <img alt="The image shows a GitHub settings page where a user is adding a &#x22;Saved Reply&#x22; with the title &#x22;Welcome Contributor.&#x22; The text box includes a thank-you message for contributors." />
</Frame>

Example saved reply content

```text theme={null}
Welcome Contributor

Thank you so much for taking the time to contribute to this project. We appreciate your effort. The team will review this shortly.
```

Quick reference table

| Action | Where to find it                          | Example / tip                                             |
| ------ | ----------------------------------------- | --------------------------------------------------------- |
| Create | Settings → Saved replies                  | Give it a clear title like `Welcome Contributor`          |
| Insert | Issue/PR comment box → Saved replies menu | Use slash commands if supported to speed insertion        |
| Edit   | Settings → Saved replies → Edit           | Update wording or links whenever processes change         |
| Delete | Settings → Saved replies → Delete         | Deleted replies are removed from your account immediately |

How to insert a saved reply in a comment

* Click into the comment box on an issue or PR.
* Select the "Saved replies" menu (or open the slash command menu `/`).
* Choose the saved reply; its text will populate the editor.
* Optionally edit the text to include issue-specific context, then submit the comment.

Edit and delete saved replies

* Edit: Open Settings → Saved replies, choose the saved reply, make changes, and save.
* Delete: Open Settings → Saved replies and click the delete option next to the reply you want to remove. Deleted replies are removed from your personal list and no longer appear in the saved replies menu.

> **warning** Avoid storing sensitive or account-specific data (like credentials or private links) in saved replies, since they are easily inserted into public issues or PRs by mistake.

Additional resources

* Official GitHub docs: Creating and managing saved replies — [https://docs.github.com/en/issues/commenting-on-issues-and-pull-requests/creating-and-managing-saved-replies](https://docs.github.com/en/issues/commenting-on-issues-and-pull-requests/creating-and-managing-saved-replies)

Summary
Saved replies are a small change that yields large time savings for maintainers: create concise, reusable responses in Settings, insert them from any issue or PR comment box, and keep them fresh by editing or deleting as your workflow evolves.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/ea8debf3-e967-4df3-9968-cc820bd2536d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/03627466-2174-481f-9a59-e83857864a8e)
