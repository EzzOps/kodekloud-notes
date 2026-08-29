# Interview Byte Make the Numbers Earn Their Place

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Put-It-All-Together/Interview-Byte-Make-the-Numbers-Earn-Their-Place/page

Guides system design interview estimation by demonstrating how to calculate and verbalize assumptions and rounded traffic numbers to inform architecture and capacity planning.

When answering an estimation question in a system-design interview, always tie your numbers back to the architecture you propose. Speak your assumptions and rounding out loud so the interviewer can follow and validate your trade-offs. Walk through one concrete example and announce each rounding as you go.

Step-by-step example (announce each assumption and rounding):

1. State the core user assumptions:

   * Total users: `100,000,000`
   * Daily active rate: `20%` (0.20)
   * Feed opens per active user per day: `20`

   Calculate reads per day:

   ```text theme={null}
   100,000,000 × 0.20 × 20 = 400,000,000 reads/day
   ```

2. Convert reads per day to reads per second.
   * Say aloud: “I’ll call a day one hundred thousand seconds” (a convenient mental rounding; actual day = 86,400s).
   ```text theme={null}
   400,000,000 reads / 100,000 seconds ≈ 4,000 reads/second
   ```

3. Account for traffic peaks with a peak factor (common practice: 3–5×).
   * Announce: “I’ll round peak traffic to about 3–5×; let’s call it 15,000 reads/s for planning.”
   ```text theme={null}
   4,000 × 3–5 ≈ 12,000–20,000 reads/second → plan ~15,000 reads/second
   ```

Use these verbal signals during the interview: “I’ll call a day one hundred thousand seconds” and “I’ll round peak traffic to about 3–5×, so let’s call it 15,000 reads/s.” Interviewers are evaluating your assumptions, reasoning, and trade-offs—not just the arithmetic.

<Frame>
  <img alt="The image features a calculation of application reads, using a hypothetical scenario of 100 million users with 20% active daily, leading to approximately 15,000 reads per second during peak times. Two stick figures are labeled as &#x22;Interviewer&#x22; and &#x22;You.&#x22;" />
</Frame>

> **lightbulb** Say your assumptions and rounding aloud. Those are the signals interviewers use to grade your reasoning.

Quick reference constants to memorize

| Constant                            | Why it helps                                                                                       |
| ----------------------------------- | -------------------------------------------------------------------------------------------------- |
| `1 day ≈ 100,000 seconds`           | Fast mental conversion for per-second estimates (actual = 86,400s). Announce that you’re rounding. |
| `1,000,000 requests/day ≈ 12 req/s` | Helpful benchmark: `1,000,000 / 86,400 ≈ 11.6` → round to `12` for quick sizing.                   |

How to use these numbers in design decisions

* Use the final reads/s to size front-end load balancers, web server pods, and API capacity.
* Multiply by average request cost (CPU, DB reads, cache hit rate) to size back-end services and databases.
* Convert reads/sec to IOPS, network bandwidth, and cache memory needs as you pick components (CDN, Redis, read replicas, etc.).

Further reading and references

* [System Design Basics](https://en.wikipedia.org/wiki/System_design)
* [Capacity Planning and Load Estimation](https://aws.amazon.com/architecture/well-architected/)

Memorize these two handy mental constants and always narrate your rounding choices — that clarity is often worth more than perfect arithmetic during interviews.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/7d9bce38-0967-4516-9f37-86b633ac4e22/lesson/0985f5d0-7f52-49aa-97ff-1ec17aa1c3d4)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/7d9bce38-0967-4516-9f37-86b633ac4e22/lesson/4b0a49a5-254c-45e3-813b-23e25168bf26)
