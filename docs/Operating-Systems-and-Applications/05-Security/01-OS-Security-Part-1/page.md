# OS Security Part 1

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/Security/OS-Security-Part-1/page

Overview of operating system security covering user accounts and privileges, file permissions, app sandboxing, patching and updates, and applying least privilege to protect devices

Security isn't just about passwords or a lock screen. It's about protecting your digital house so only the right people can enter and your private data stays private.

Imagine this scene: Cody is at a café on public Wi‑Fi. She logs in, checks email, plugs in a USB stick borrowed from a friend, and opens a file someone AirDropped. The operating system is the silent home security system: it decides whether that file should be allowed in, whether this user has the right key, and whether that network connection is safe to trust. It locks doors, checks visitors, and protects valuables — all to keep the system secure.

This applies to phones, tablets, laptops, and desktops alike: every device needs basic defenses built into the OS.

<Frame>
  <img alt="A presenter stands on the right wearing a KodeKloud T-shirt. On the left a slide shows tablet, phone and desktop icons with shield symbols and the caption &#x22;Same protections across all devices.&#x22;" />
</Frame>

What this lesson covers

* How the OS enforces user access with accounts and file permissions.
* How updates and patches fix security vulnerabilities.
* Built-in defenses such as firewalls and antivirus.
* System hardening best practices.

<Frame>
  <img alt="A presenter stands on the right in front of a dark purple slide listing numbered cybersecurity topics (user access, updates/patches, firewalls/antivirus, hardening). A small cartoon cat mascot is shown on the left of the slide." />
</Frame>

We’re focusing on protections the operating system itself controls — security built into the design, like a well‑planned home. Broader topics such as network-wide defenses, fleet management, and cloud security are separate subjects.

The front door: user accounts and privileges
When you log into a device, you’re stepping into your digital house. Not all keys open all doors.

* Administrators: the homeowners. They have the master key — install software, change system-wide settings, and grant elevated access to others.
* Standard users: family members. They can personalize their space and run applications, but they can’t change system configuration for everyone.
* Guests: very limited access — typically only a few shared areas.

These distinctions protect valuables — private files, system settings, security controls. If everyone had admin rights, accidental or malicious changes would be easier and far more damaging. On many consumer devices the first account is created with admin privileges by default (e.g., macOS and Windows). For safety, create standard accounts for other users and use admin access only when required.

User accounts, file ownership, and access controls
Your account identifies who you are. Operating systems tie file ownership and permissions to accounts:

* Unix-like systems: owner, group, and others (basic rwx semantics).
* Windows: Access Control Lists (ACLs) for more granular rules.

These controls determine what actions are allowed on files and directories. They are fundamental to containment — preventing unauthorized reading, modification, or execution.

App permissions and sandboxing
Applications don’t automatically get access to everything on your device. Modern OSes prompt for permission and use sandboxing to isolate apps and reduce privacy risks. For example, a photo app must request access to your photos or camera before it can use them.

<Frame>
  <img alt="A large on-screen dialog requests camera access to &#x22;take pictures and detect your face&#x22; with &#x22;Don't Allow&#x22; and &#x22;OK&#x22; buttons. To the right, a presenter wearing a KodeKloud t-shirt stands against a dark background." />
</Frame>

Principle of least privilege
Grant only the minimum access required for a task. Parental controls are simply a different UI exposing restricted permissions — same underlying model. If malware or an unsafe installer runs under a standard account, it cannot make system-wide changes.

Quick reference — account types and typical permissions

| Account type         | Typical privileges                                                | When to use                                                         |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| Administrator / root | Install software, change system configuration, manage other users | System administrators, initial device setup, infrequent maintenance |
| Standard user        | Run apps, change personal settings, create files in user profile  | Daily use by most people to reduce risk                             |
| Guest                | Very limited access to shared resources                           | Temporary users or public kiosk mode                                |

<Frame>
  <img alt="A dark slide with two purple info boxes reading &#x22;01 Accounts: Who you are&#x22; and &#x22;02 Permissions: What you can do&#x22; appears on the left. A man wearing a KodeKloud T-shirt stands and speaks on the right against a black background." />
</Frame>

<Callout icon="lightbulb">
  Use the principle of least privilege: run daily tasks under a standard (non-admin) account and elevate only when necessary.
</Callout>

Patches and updates — why they matter
Software contains bugs. Some bugs become security vulnerabilities. Left unpatched, vulnerabilities are like broken windows or faulty locks — attackers will look for them. Vendors release patches and updates to repair these weaknesses.

* Patch: a targeted code fix for a specific vulnerability.
* Update: a broader package that may include patches, feature improvements, and stability fixes.

<Frame>
  <img alt="A presenter in a KodeKloud t-shirt stands to the right of a stylized purple house graphic that has cracks circled to indicate weak points. The slide headline reads &#x22;Unpatched vulnerabilities = Open doors and cracks.&#x22;" />
</Frame>

Why timely updates reduce risk
Applying updates promptly helps maintain three core security properties:

| Security property | How updates help                                                                  |
| ----------------- | --------------------------------------------------------------------------------- |
| Integrity         | Fixes prevent tampering and ensure system components are authentic and unmodified |
| Confidentiality   | Closes paths attackers can use to extract sensitive data                          |
| Availability      | Prevents crashes, lockouts, or ransomware that can make systems unusable          |

Most modern devices can automatically install updates. While there are situations to defer updates (compatibility testing in enterprise environments), delaying routine security patches increases cumulative exposure: each missed patch adds to the attack surface.

<Frame>
  <img alt="A presentation slide titled &#x22;Bug fixes and security updates&#x22; showing screenshots of macOS and iOS software update dialogs on the left and center, with a presenter wearing a KodeKloud t-shirt on the right." />
</Frame>

Real-world example: browser vulnerabilities
Browsers are a common attack vector (they parse untrusted content and run scripts). When a serious browser vulnerability is identified, vendors often release a patch within days. Release notes might say “bug fixes and security updates,” but behind those words can be a critical fix that closes a window attackers were using.

<Frame>
  <img alt="An illustrated slide showing a laptop and smartphone with gear icons and progress bars, surrounded by small bug icons and the heading &#x22;Browser Vulnerability leads to Patch Release.&#x22; A presenter wearing a KodeKloud T-shirt stands at the right speaking to the camera." />
</Frame>

<Callout icon="warning">
  Critical updates should be applied promptly. Delaying high‑severity patches gives attackers a known path into your systems.
</Callout>

Practical takeaway

* Use separate, non-admin accounts for daily work.
* Approve app permissions only when needed.
* Enable automatic updates where possible, or apply patches promptly.
* Follow the principle of least privilege to reduce the blast radius of compromises.

Quick checkpoint: Cody thinks she knows the answer.

What's the real reason security patches exist? Is it:
A) to clean up unused files,\
B) to fix known vulnerabilities, or\
C) to annoy users and ruin their mornings?

Correct answer: B — patches fix known vulnerabilities before attackers can exploit them.

<Frame>
  <img alt="A presenter wearing a KodeKloud shirt stands to the right of a slide asking, &#x22;What's the real reason security patches exist?&#x22; Two colorful multiple-choice options are visible, including &#x22;To fix known vulnerabilities&#x22; (B) and &#x22;To clean up unused files&#x22; (A)." />
</Frame>

Further reading and references

* NIST Cybersecurity Framework: [https://www.nist.gov/cyberframework](https://www.nist.gov/cyberframework)
* OWASP Top Ten (web application risks): [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
* Microsoft Security Update Guide: [https://msrc.microsoft.com/update-guide](https://msrc.microsoft.com/update-guide)

This lesson focused on OS-level controls — accounts, permissions, and patching. In the next part we’ll look at built-in defenses (firewalls, antivirus, and sandboxing) and practical system hardening steps you can take.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/98269c55-06d3-4512-b631-b104a6df02f9/lesson/1ea50860-bde8-4249-8e28-68dc21921e87" />
</CardGroup>
