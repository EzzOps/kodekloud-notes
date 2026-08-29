# Categories of Controls

Source: https://notes.kodekloud.com/docs/CompTIA-Security-Certification/Controls-and-Security-Concepts/Categories-of-Controls/page

Summarizes four security control categories and deception techniques, describing implementation, differences, examples, and role in layered security programs

This article explains the four primary categories of security controls, how they differ, and where they fit in a layered security program. Two categories are implemented by people, and two are implemented by systems or devices.

* Managerial controls (implemented by people)
* Operational controls (implemented by people)
* Technical controls (implemented by things)
* Physical controls (implemented by things)

Use the following quick reference table to compare these control categories at a glance.

| Control Category | Implemented By                       | Purpose / Use Case                                                | Examples                                                        |
| ---------------- | ------------------------------------ | ----------------------------------------------------------------- | --------------------------------------------------------------- |
| Managerial       | People (leadership/management)       | Define policies, governance, risk tolerance, and responsibilities | Security policy, risk assessments, governance frameworks        |
| Operational      | People (staff/operations)            | Day-to-day execution of security tasks and procedures             | Incident response, backups, change control, data classification |
| Technical        | Systems (hardware/software/firmware) | Enforce security automatically at a technical level               | Firewalls, IDS/IPS, authentication, encryption                  |
| Physical         | Things (physical devices/structures) | Prevent or deter unauthorized physical access and tampering       | Locks, fences, badge readers, CCTV, lighting                    |

Managerial controls establish the rules and acceptable risk levels. Operational controls are the human actions that enforce and follow those rules. Technical and physical controls are the automated or tangible mechanisms that enforce security, either electronically or physically.

## Managerial Controls (implemented by people)

Managerial controls are set by organizational leadership to define what must be done and who is accountable. They build the foundation for a security program and typically include:

* Policies, standards, and procedures
* Security governance and oversight
* Risk assessments, business impact analysis, and acceptance criteria
* Security planning and resource allocation
* Vendor/third-party risk management

These controls guide both operational staff and technical teams. Examples of standards and frameworks that influence managerial controls include NIST SP 800-series and organizational security policies.

## Operational Controls (implemented by people)

Operational controls are the everyday security-related activities performed by staff to implement managerial direction. They typically focus on processes and human behavior:

* Incident response and forensics
* Change management and configuration control
* Asset management and inventory
* Data labeling, classification, and handling
* Physical security patrols and identity verification

Operational controls often intersect with technical controls—for example, an operator who triages alerts from an intrusion detection system or a backup administrator who verifies restore procedures.

## Technical Controls (implemented by things)

Technical controls are implemented via hardware, software, or firmware. They are designed to automatically enforce security policies and reduce human error:

* Network defenses: firewalls, IDS/IPS, network segmentation
* Endpoint protections: antivirus/anti-malware, EDR
* Access controls: authentication, authorization, access control lists (ACLs)
* Data protection: encryption (at-rest and in-transit), tokenization
* Monitoring and logging systems

Technical controls are critical for scalability and consistent enforcement, and they should be aligned with managerial policies and operational procedures.

## Physical Controls (implemented by things)

Physical controls protect facilities, systems, and personnel from physical threats. They are implemented as tangible barriers and detection systems:

* Structural: fences, gated perimeters, walls
* Entry controls: locks, badge readers, turnstiles, vestibules
* Environmental: lighting, secure enclosures, tamper-evident seals
* Detection: cameras (CCTV), motion sensors, alarms
* Human: security guards, reception screening

Examples of physical controls include fences, locked doors, badge readers, lighting, and video surveillance.

<Frame>
  <img alt="A presentation slide titled &#x22;Security Controls – Categories&#x22; showing two colored panels: &#x22;Technical Controls&#x22; (firewall icon and bullets) and &#x22;Physical Controls&#x22; (barrier icon and bullets). A banner above reads &#x22;Implemented by Things.&#x22;" />
</Frame>

Physical security is most effective when layered. Multiple scales of intrusion should be anticipated—from perimeter breaching to insider threats—so defenses are combined to delay and detect attackers before they reach critical assets.

For example, controlled entry points such as vestibules create staged authentication zones that slow or prevent unauthorized entry and reduce the risk of simple techniques such as

<Frame>
  <img alt="The slide titled &#x22;Fundamental Security Concepts&#x22; shows an &#x22;Intruder&#x22; icon on the left, an &#x22;Access Control Vestibules&#x22; icon in the center, and a building inside a dotted perimeter labeled &#x22;Physical Security&#x22; on the right. It visually links an intruder to physical security controls (access control/vestibules) protecting the building." />
</Frame>

tailgating, piggybacking, or walking into facilities unnoticed. All authorized personnel should use badges or other approved credentials for access, and environmental measures like lighting and video surveillance should be part of a comprehensive program.

## Deception-based Controls (honeypots and honeynets)

Deception-based controls are designed to lure, observe, and analyze attackers. A honeypot is a deliberately vulnerable or enticing system deployed to attract adversaries so defenders can study attacker behavior and tactics without risking production assets.

Key considerations for honeypots:

* Isolate them from production networks to prevent lateral movement.
* Instrument honeypots with detailed logging and monitoring.
* Treat honeypots as research and detection tools, not replacements for hardening real systems.
* Consider legal and privacy implications before recording or interacting with attackers.

> **warning** Honeypots require careful design and legal consideration: they must be isolated to prevent attackers from pivoting into production, and monitoring/collection must comply with privacy and legal requirements.

You can deploy a single honeypot or scale to honeynets (interconnected decoys). Choose low-, medium-, or high-interaction honeypots based on the intelligence you want to gather and the risk you’re willing to accept.

## Further reading and references

| Resource                                                                   | Why it helps                                                          |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)        | Guidance on risk-based cybersecurity governance and control selection |
| [CompTIA Security Resources](https://www.comptia.org/content/white-papers) | Practitioner-focused security topics and certification materials      |
| [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)                  | Best practices for technical controls and application security        |

These references provide deeper guidance for designing, implementing, and assessing managerial, operational, technical, and physical controls.

- [Watch Video](https://learn.kodekloud.com/user/courses/comptia-security-certification/module/1846e159-7ab4-46d3-be5d-95c1a0eb51b9/lesson/78941d41-7fd5-4e24-ae4f-f1ce84808147)
