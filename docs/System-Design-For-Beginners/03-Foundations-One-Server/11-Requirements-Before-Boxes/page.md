# Requirements Before Boxes

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/Requirements-Before-Boxes/page

A guide to five core system questions—users and growth, read versus write balance, data durability, latency tolerances, and cost—before designing scalable photo app architecture

You can't design the right system until you know who you’re designing it for and what constraints matter. Before sketching architecture diagrams or picking components, pause and answer a small set of focused questions about usage patterns, durability, latency, and cost.

> **lightbulb** Start by answering a few targeted questions about users, growth, read/write balance, data durability, latency tolerances, and cost. These answers will drive every design decision that follows.

Below we walk through five core questions using a photo-sharing app as an example. For each question we describe why it matters and the concrete implications for system design.

First question: how many users do we have and how fast are they growing?

A photo app with 1,000 users is a very different system from one with 50 million. Assume the app has 10,000 users today and the user count doubles every few months. Design for the millions you’re heading toward, not only for the ten thousand you have now.

<Frame>
  <img alt="The image features a stylized graph indicating user growth over time, marked with &#x22;10k Today,&#x22; alongside a smartphone mockup displaying a social media app interface." />
</Frame>

Second question: is the app read-heavy or write-heavy?

Most photo-sharing apps are read-dominated: users scroll feeds far more than they post. Scrolling creates many more read requests than the relatively infrequent writes for new posts. When reads dominate, optimize the read path (caching, indexing, feed generation) before over-engineering the write path.

<Frame>
  <img alt="The image contrasts &#x22;scrolling&#x22; and &#x22;posting&#x22; habits in terms of frequency per month, with an emphasis on scrolling being read-heavy and posting being write-heavy. A smartphone illustration highlights a &#x22;New Post&#x22; notification." />
</Frame>

Third question: what data can you absolutely never lose, and what can you afford to lose?

Different data has different durability requirements. A user’s original photo file is critical — losing photos destroys trust. Metrics like eventual like-counts or temporary feed ordering discrepancies can often tolerate eventual consistency. Classify data by durability and consistency needs to prioritize storage and replication strategies.

<Frame>
  <img alt="The image shows a comparison between likes in an app (41 likes) and a database (45 likes), with emphasis on the question &#x22;What can you never lose?&#x22;" />
</Frame>

Fourth question: how much latency can we afford?

Different user flows have different perceived latency requirements. Feeds should feel instant — target sub-200ms for perceived responsiveness. Uploading a photo is an interactive task where users expect a few seconds; this path can tolerate heavier processing (e.g., resizing, transcoding, virus scanning) and batched/async workflows.

<Frame>
  <img alt="The image shows a phone interface with a &#x22;New Post&#x22; upload confirmation and the text &#x22;How much latency can you afford?&#x22; at the top." />
</Frame>

Fifth question: what does it cost?

Every replica, cache layer, and additional service increases monthly spend. The right architecture balances durability, latency, and scale at an acceptable cost. Focus engineering effort where it yields the most value (e.g., feed performance and durable object storage for photos) rather than adding components because they’re trendy.

Now synthesize the five questions for this photo app.

* We must design for growth toward millions of users.
* Traffic is heavily read-dominated.
* Photos must be never lost — highest durability.
* Feed reads must be low latency (feel instant).
* Keep infrastructure costs reasonable.

<Frame>
  <img alt="The image highlights five concepts with icons: &#x22;Built for millions,&#x22; &#x22;Heavily read,&#x22; &#x22;Never lose a photo,&#x22; &#x22;Instant feed,&#x22; and &#x22;Keep the bill sane,&#x22; along with the descriptions &#x22;Feed = the hard part,&#x22; &#x22;Photos = safest,&#x22; and &#x22;Uploads = can be slow.&#x22;" />
</Frame>

Summary table — quick reference

| Question                             |                                      Why it matters | Design implication                                                     |
| ------------------------------------ | --------------------------------------------------: | ---------------------------------------------------------------------- |
| How many users and growth rate?      |  Predicts capacity, sharding, and operational needs | Design for scale (sharding/partitioning, autoscaling, CI/CD)           |
| Read-heavy or write-heavy?           |       Determines where to invest engineering effort | Prioritize read path optimizations (caching, precomputed feeds)        |
| What data must never be lost?        |      Determines durability and replication strategy | Store photos in highly durable object storage with backups/replication |
| What latency can each path tolerate? | Dictates sync vs async, user experience constraints | Optimize feed reads for low latency; allow async processing on uploads |
| What does it cost?                   | Constraints on how many layers/replicas you can add | Choose simplest architecture that meets durability/latency needs       |

This mindset — answering requirements before picking components — separates thoughtful system designers from component-collectors. Anyone can say “add cache”; the real skill is justifying why the app needs it and calculating the trade-offs in cost and complexity.

<Frame>
  <img alt="The image contrasts two approaches: &#x22;Designers&#x22; with a crossed-out phrase &#x22;Just Add Cache!&#x22; and various icons, and &#x22;Component-Collectors&#x22; focusing on explaining &#x22;Why This App Needs It.&#x22;" />
</Frame>

> **warning** Don’t build components in search of a problem. Use these five questions to prioritize investments (e.g., caching, replication, CDNs) only where they measurably improve durability, latency, or cost.

If you need a short checklist to carry into architecture sessions, remember these five questions — users & growth, read/write balance, data durability, latency per path, and cost — and use them to justify every architectural choice.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/09a1aad8-6f61-41bf-8505-3e637f6ed00c)
