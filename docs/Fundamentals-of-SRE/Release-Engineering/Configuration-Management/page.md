# Configuration Management

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Release-Engineering/Configuration-Management/page

Guide on configuration management for SREs covering risks, common failures, and best practices like treating configuration as code, versioning, CI gates, feature flags, and staged rollouts

Hello again and welcome back.

In this lesson we'll explore configuration management — why it matters, common failure modes, and practical ways to manage configuration safely and reliably. Code tends to get the spotlight, but many major outages originate from configuration mistakes. When treated correctly, configuration becomes just another form of code: reviewable, testable, and auditable.

Why does configuration management matter? Configuration is often the silent reliability risk. Studies and postmortems show a large percentage of outages are caused by configuration errors. These issues are harder to debug, often skipped in automated tests, and can have immediate, widespread impact.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Configuration Management Matters&#x22; featuring an &#x22;Expensive Hall of Fame&#x22; of major cloud outages. It lists Facebook BGP (2021) — a 6-hour global outage, Google GCE Metadata (2019) — global VM/auth failure, and AWS us-east-1 (2017) — a typo that caused a multi-hour outage." />
</Frame>

These examples are not edge cases — they show how a single misconfiguration can cascade into large-scale outages.

Configuration changes are deceptively risky because they frequently skip code review and automated testing. Engineers may push config updates directly to production hoping “nothing breaks.” One bad setting can take down a service instantly; a misconfigured access control can even lock you out of the systems needed to restore service.

For SREs, misconfigurations are a common and recurring incident source: time spent debugging config issues often exceeds time spent debugging application code. That’s why configuration deserves the same rigor as application code: version control, review, CI, testing, and traceability.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Configuration Management Matters&#x22; that highlights &#x22;Why Configuration Is Dangerous.&#x22; It shows three numbered points with icons: 01) Config often skips review, 02) Can break everything instantly, and 03) Can lock you out of fixes." />
</Frame>

Common configuration problems follow a few repeatable patterns:

|                   Problem | What happens                                 | Typical consequence                              |
| ------------------------: | -------------------------------------------- | ------------------------------------------------ |
|       Manual config drift | One-off fixes applied directly in production | Divergent server states, hard-to-reproduce bugs  |
|   Sensitive data exposure | Secrets committed or stored in plaintext     | Leak of credentials or keys                      |
| Environment inconsistency | Different settings across dev/staging/prod   | Bugs that only appear in production              |
|      Uncontrolled changes | Repeated tweaks by many engineers            | No clear owner or source of truth for live state |

Common pitfalls include:

* Manual config drift: a 3 AM production patch that never propagates.
* Sensitive data exposure: credentials accidentally committed or left in public files.
* Environment inconsistency: dev/staging/prod mismatch causing unexpected behavior.
* Uncontrolled changes: multiple engineers iterating until no one knows the canonical state.

Examples of risky config material:

```python theme={null}
