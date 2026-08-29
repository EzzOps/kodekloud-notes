# Stateless vs Stateful

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Stateless-vs-Stateful/page

Explains stateless versus stateful servers and how to centralize sessions for scalable, disposable servers.

Understanding the difference between stateless and stateful systems is a foundational concept in scalable system design. We'll walk through a concrete scenario and practical guidance for making servers disposable and resilient.

Imagine your photo app runs on ten identical servers behind a load balancer. Traffic is distributed evenly — until users begin reporting that they're getting logged out even though you didn't change any code. What happened?

When Alan logs in, his request might be handled by Server One. That server creates a login session — a small note in memory saying "Alan is authenticated." On every subsequent request, the server checks this note rather than asking for Alan's password again. Server One stores that session note in its own memory.

A few minutes later Alan navigates to another page and the load balancer routes his request to Server Five. Server Five looks in its own memory and doesn’t find Alan’s session (it was stored only on Server One). Server Five replies, "Who are you? Please log in." Now Alan is confused and thinks he’s logged out.

<Frame>
  <img alt="The image is a diagram illustrating a login process through a load balancer which directs the request to Server One or Server Five. Server One's memory is displayed, while Server Five's memory shows a question mark, indicating missing information." />
</Frame>

This is the single biggest thing that breaks when you move from one server to many. On a single server, keeping login sessions in local memory works fine because every request hits the same machine. Once a load balancer spreads requests across multiple servers, user-specific data gets scattered: different machines remember different users.

Because each server keeps per-user session data in its own memory, we call those servers stateful. "Stateful" means the application stores knowledge of previous requests (for example, login session details) inside the server itself.

Stateless servers, by contrast, do not retain important per-user state between requests. They handle a request, send a response, and forget anything that isn’t needed for future requests. The user session must live in a shared, durable store that every server can access (for example, a cache like Redis, a database, or tokens stored in signed cookies).

> **lightbulb** Make sessions shared: write login sessions to a common store (e.g., `Redis`, a database, or signed cookies). When any server receives a request, it reads the session from that shared place and continues the user’s flow.

With a shared session store, when Alan logs in via Server One, the login session is written centrally. If his next request hits Server Five, Server Five reads the same shared store, finds the session, and Alan stays logged in. This fixes the logout problem.

Another approach people sometimes use is session affinity (sticky sessions). With sticky sessions, the load balancer is configured to always send a particular user’s requests to the same server: if Alan first hit Server One, the balancer will keep routing Alan to Server One.

<Frame>
  <img alt="The image illustrates a flowchart of sticky sessions, showing a login interface connecting to a load balancer, which consistently directs traffic to a specific server." />
</Frame>

> **warning** Sticky sessions can mask the underlying problem but reintroduce single-server failure and uneven load. If the pinned server fails, affected users lose their sessions. Sticky sessions also prevent the load balancer from distributing traffic evenly.

Login sessions aren’t the only thing that can make a server stateful. Ask yourself: if this server disappeared right now, would any user lose something? If the answer is yes — that data makes the server stateful. Any user-continuity data stored only on one server (in RAM or on the server’s local disk) should be moved to a shared store so the server can be disposable.

<Frame>
  <img alt="The image illustrates a concept about stateful data with a focus on user sessions, data that makes it stateful, and a shared store, emphasizing the question, &#x22;Would any user lose something?&#x22;" />
</Frame>

To be absolutely clear: storing photos in a database or cloud storage does not make your application stateful. Those photos live outside the app server. Stateful means the server itself keeps information (in memory or on its local disk) that would be lost if the server disappears.

<Frame>
  <img alt="The image illustrates the concept of stateful and stateless systems, showing an app interacting with a load balancer, a database, and cloud storage, emphasizing that &#x22;stateful&#x22; does not simply mean data storage." />
</Frame>

The primary question is not whether your app stores data (it does), but where that data lives and whether the server depends on its own local copy for correctness.

Below is a quick categorization of common tasks in a photo app and whether they are typically stateless or stateful.

| Task                                                          | Category  | Why                                                                                                                                 |
| ------------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Uploading a photo                                             | Stateless | The request contains the photo; the server writes it to external storage and forgets it.                                            |
| Downloading a photo                                           | Stateless | The request specifies which photo to fetch from external storage.                                                                   |
| Applying a filter / Searching photos / Fetching photo details | Stateless | Each request includes the parameters needed; no per-user continuity state is required.                                              |
| Login / Session management                                    | Stateful  | The app must remember that a user is authenticated between requests; session data must be centralized or encoded in a shared token. |

<Frame>
  <img alt="The image is a diagram of a photo app's architecture, showing a smartphone interface, load balancer, and tasks sorted into stateless (such as uploading photos) and stateful (login sessions) categories." />
</Frame>

Practical checklist for making servers stateless

* Move per-user session data to a shared store (Redis, database, or signed tokens).
* Avoid storing user-continuity data on local disk or in RAM that isn't replicated.
* Prefer external, durable stores for files (S3 / object storage) and metadata in databases.
* Make servers replaceable: you should be able to restart, add, or remove them without affecting users.

Place any user-specific, per-request continuity data in the shared store, not on individual app servers. Keeping app servers stateless is one of the first rules of scaling: servers become disposable. Add one, kill one, or restart one — and no user notices.

<Frame>
  <img alt="The image illustrates the concept of stateless app servers, showing a mobile app interface, a load balancer directing traffic to servers, and a shared data store." />
</Frame>

Links and references

* Redis: [https://redis.io](https://redis.io)
* Session affinity (sticky sessions): [https://en.wikipedia.org/wiki/Session\_affinity](https://en.wikipedia.org/wiki/Session_affinity)
* Best practices for session management: [https://owasp.org/www-community/controls/Session\_Management](https://owasp.org/www-community/controls/Session_Management)
* Cloud object storage (S3): [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/39800f71-299e-46c1-a72d-dd5c14a29f93)
