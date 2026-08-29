# Demo Different Options in Discussion

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Discussions/Demo-Different-Options-in-Discussion/page

Guide to using GitHub Discussions to manage community Q&A, including answering, voting, accepting answers, pinning, locking, and converting discussions into issues for tracking

This guide walks through how GitHub Discussions supports community Q\&A in a repository, showing how contributors and maintainers can answer, vote, accept answers, pin or lock conversations, and convert useful threads into issues for tracking. These workflows keep context visible while enabling maintainers to take action on reproducible bugs or feature requests.

Viewing and answering a discussion

* Sign in to your GitHub account and open the Discussions tab in the repository (for example, the Block Buster repo).
* Browse the Q\&A section to find unanswered questions. Any participant can reply—answers may include suggestions, workarounds, or debugging steps.
* In this example, one reply explains the high score is saved as a browser cookie and recommends clearing cookies and cache to reset it.

<Frame>
  <img alt="The image shows a GitHub discussion page where a user asks about how high scores are saved in a game, and a collaborator responds that it's saved as a cookie in the browser." />
</Frame>

Switching accounts to see other answers

* Different contributors may answer the same question from their perspective. Sign out and sign in as another user to view other responses or contribute your own.
* For the same high-score question, another user suggested it’s stored in `localStorage` and mentioned a reset button on the welcome screen.
* Community members can upvote helpful answers to surface useful solutions.

Maintainers marking the correct answer

* Collaborators and maintainers review answers and can mark one as the accepted/correct answer.
* Marking an answer accepted highlights it (green border) and places it directly under the question so readers can find the accepted solution quickly without scrolling through long threads.

<Frame>
  <img alt="The image shows a GitHub discussion thread about how to save and reset the high score in a browser, with comments suggesting different methods." />
</Frame>

Why the accepted answer appears under the question

* Large threads can be time-consuming to read. Showing the accepted answer immediately under the question helps future readers find the solution fast and reduces duplicated effort from repeated replies.

<Frame>
  <img alt="The image is a screenshot of a GitHub discussion page where users are discussing how the high score is saved in a game called Block Buster 2026, with answers mentioning using the browser's localStorage and cookies." />
</Frame>

Pinning and locking discussions

* Use the options on the right side of a discussion to pin or lock the conversation.
  * Pin a discussion to surface it on the Discussions home page and choose an accent color when pinning.
  * You may pin up to four discussions per repository to keep important topics visible.
  * Lock a discussion to stop new replies when a thread is complete or becoming unproductive.

> **lightbulb** Pinned discussions make important topics easy to find. Remember the limit: you can pin up to four discussions per repository.

Creating an issue from a discussion

* If a discussion contains a reproducible bug, a clear feature request, or an actionable task, convert it into an issue using “Create issue from discussion.”
* GitHub pre-populates the new issue’s title and description, includes a link back to the original discussion, and records the user who posted the thread.
* The generated issue body references the discussion ID so the two remain linked for traceability and context.

<Frame>
  <img alt="The image shows a GitHub interface for creating a new issue in a repository named &#x22;block-buster,&#x22; with a title field asking about how the high score is saved and a description field containing a detailed inquiry originally posted by a user." />
</Frame>

After creating the issue

* The new issue links back to the discussion by ID, preserving the original conversation and attribution for maintainers and contributors.
* Continue using Discussions for community Q\&A while tracking fixes and triage items in the Issues tab.

> **lightbulb** Creating an issue from a discussion preserves context and attribution while enabling maintainers to triage and track work in the Issues tab.

Quick reference — who can do what

| Action                       | Who can perform it                                      | Notes / Example                                                                 |
| ---------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Post an answer               | Any signed-in user                                      | Community replies, suggestions, or workarounds (e.g., `localStorage`, cookies). |
| Upvote an answer             | Any signed-in user                                      | Helps surface helpful replies.                                                  |
| Mark accepted answer         | Repository maintainers & collaborators                  | Highlights the accepted solution under the question.                            |
| Pin a discussion             | Maintainers & collaborators                             | Up to four pinned discussions per repo.                                         |
| Lock a discussion            | Maintainers & collaborators                             | Prevents new replies when appropriate.                                          |
| Create issue from discussion | Maintainers & collaborators (or users with permissions) | Auto-populates issue body and links back to the discussion ID.                  |

See also

* GitHub Discussions docs: [https://docs.github.com/en/discussions](https://docs.github.com/en/discussions)
* GitHub Issues documentation: [https://docs.github.com/en/issues](https://docs.github.com/en/issues)

Keywords: GitHub Discussions, accepted answer, pin discussion, lock discussion, create issue from discussion, upvote answer, repository maintainers.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/f42f6458-b9ea-4ebb-8cbd-261b2393e622/lesson/7aebf1c5-2e99-4d0f-ae7e-ec9cd5c79e81)
