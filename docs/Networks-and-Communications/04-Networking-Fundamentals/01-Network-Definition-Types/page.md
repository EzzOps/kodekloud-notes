# Network Definition Types

Source: https://notes.kodekloud.com/docs/Networks-and-Communications/Networking-Fundamentals/Network-Definition-Types/page

Overview of network types, scales, wired vs wireless, peer-to-peer and client-server models, latency, and security trade-offs

No Wi‑Fi, no Bluetooth, no mobile data,\
no syncing, no cloud, no updates.

For some, that's bliss. For others, digital isolation.

This lesson explains how networks break that isolation — how your phone talks to your watch, how a laptop finds a printer, and how a movie travels from a server across the world to your screen. We'll define what a network is, compare the main network types (from personal to global), contrast wired and wireless links, and review two common data‑sharing models: peer‑to‑peer and client‑server.

<Frame>
  <img alt="A presenter wearing a KodeKloud shirt stands to the right of a purple slide listing numbered learning objectives about networks, with a small cartoon cat illustration on the left. The slide items include describing what a network is, identifying types and scaling, and explaining how size affects use cases." />
</Frame>

What is a network?

* A network is a group of connected devices that can share resources (files, printers, messages, or Internet access).
* Think of it like a group chat for devices: they send, receive, and coordinate information.

Common examples:

* Streaming music from your phone to a speaker at home.
* Hundreds of computers at a company accessing shared storage.
* Local networks that operate entirely without Internet access — devices can communicate directly.

> **lightbulb** Local networks (for example, PANs or LANs) can let devices communicate even when the Internet is unavailable. The Internet is one possible extension, not a requirement.

Wired vs wireless

* Wired (Ethernet): uses physical cables; common where speed, stability and low latency matter.
* Wireless (Wi‑Fi, Bluetooth): trades some reliability and range for mobility and convenience.
* The core idea remains connection and collaboration — without networks, devices are isolated.

Personal Area Network (PAN)

* Scope: very short range (typically \~10 meters / 30 feet).
* Use: device-to-device links for a single user — earbuds, smartwatch pairing, phone tethering.
* Typical tech: Bluetooth, USB‑based direct links.

Local Area Network (LAN) and Wireless LAN (WLAN)

* Scope: devices across a single location (home, office, classroom).
* LAN can be wired or wireless; WLAN specifically means a Wi‑Fi based LAN.
* Use: high‑speed sharing of files, printers, and local servers within a building.

Wide Area Network (WAN)

* Scope: connects LANs across cities, regions, or countries.
* Use: linking branch offices, data center interconnects, or distributed corporate networks.
* WAN infrastructure often involves ISPs, leased lines, or dedicated circuits and is more costly than local networks.

<Frame>
  <img alt="An isometric diagram of a Wide Area Network showing a company office connected through an Internet Service Provider to four labeled branch offices. A presenter wearing a KodeKloud shirt stands on the right explaining the diagram." />
</Frame>

Many organizations lease WAN links from ISPs — like hiring a private courier for your data. These links typically provide better throughput, security and reliability than general Internet connections, but at a higher cost.

Scale, trade-offs, and everyday experience

* PANs: perfect for personal device sync (earbuds, wearable). Short range and easily disrupted.
* LANs: ideal for high‑speed sharing inside a building. Limited geographic scope.
* WLANs: provide mobility within a LAN’s footprint, but can suffer reduced signal through walls and at distance.
* WANs: connect distant locations at scale, but introduce higher latency, cost, and operational complexity.

Network types at a glance:

| Network Type | Typical Range            | Typical Use Cases                                   | Trade-offs                                                     |
| ------------ | ------------------------ | --------------------------------------------------- | -------------------------------------------------------------- |
| PAN          | \~10 m (30 ft)           | Bluetooth earbuds, phone-watch sync                 | Very local, low power, limited throughput                      |
| LAN / WLAN   | Single building / campus | File sharing, printers, office networks, home Wi‑Fi | High speed locally; WLAN adds mobility but less predictability |
| WAN          | City / Country / Global  | Connecting branch offices, cloud data centers       | Higher latency and cost; requires routing and management       |

<Frame>
  <img alt="A presenter stands at the right wearing a black shirt with a &#x22;KodeKloud&#x22; logo. The background shows purple isometric illustrations of offices, devices (smartwatch, smartphone, printers) and network/Wi‑Fi icons on a black backdrop." />
</Frame>

Latency and the Internet

* Latency is the delay between sending and receiving data.
* As distance grows (WANs, the Internet), latency typically increases because packets traverse more routers and physical links.
* The Internet is the world’s largest WAN: it connects millions of LANs and WANs and carries services like web pages, email, streaming and gaming — each using the same underlying infrastructure in different ways.

<Frame>
  <img alt="A presenter stands on the right beside a purple-themed infographic showing a globe with WAN connections and multiple office/workstation blocks with Wi-Fi icons labeled &#x22;WLANs.&#x22; A &#x22;Latency&#x22; label and brief definition are shown near the globe." />
</Frame>

Security and scale
As networks grow, exposure to security and privacy risks increases. More devices and broader reach require structure: routing, addressing, access control, logging, and monitoring. How you organize sharing — whether peer‑to‑peer or client‑server — affects performance, manageability, and security posture.

> **warning** Larger, more connected networks require stronger security controls (segmentation, authentication, monitoring). An open or poorly managed WAN can expose many systems at once.

Peer-to-peer (P2P)

* In P2P, devices communicate directly without a central server.
* Useful for small-scale or ad‑hoc sharing: Bluetooth file transfer, LAN gaming, or local document sharing.
* Limitation: distributing the same data to many recipients can be inefficient unless specialized P2P protocols or multicast techniques are used.

<Frame>
  <img alt="An illustrated diagram titled &#x22;Peer-to-peer (P2P) Network&#x22; showing interconnected purple office-style nodes. A presenter stands to the right wearing a KodeKloud t-shirt." />
</Frame>

Client‑server

* A central server stores data and provides services; clients (desktops, phones, smart TVs) request those services.
* Efficient at scale: upload once, many clients download.
* Trade‑off: potential single point of failure — mitigated with redundancy, load balancing, and failover strategies.

Examples:

* Streaming platforms (Netflix, YouTube) store content on central servers and CDNs for millions of users.
* Video conferencing services (Zoom) often route or mix streams through servers rather than relying entirely on direct client connections.

Hybrid approaches
Most real systems blend both models: e.g., a video stream from central servers while devices on the same LAN share files P2P.

Quick check — select the true statements (select all that apply):
A. Networks must be connected to the Internet.\
B. WLANs are wireless versions of LANs.\
C. WANs are always faster than LANs.\
D. Peer‑to‑peer networks don't need a central server.

Answers:

| Option | Correct? | Explanation                                                                                        |
| ------ | -------- | -------------------------------------------------------------------------------------------------- |
| A      | False    | Networks can be local and function without Internet connectivity.                                  |
| B      | True     | A WLAN is simply a LAN that uses Wi‑Fi instead of cables.                                          |
| C      | False    | WANs typically have higher latency and can be slower than LANs due to distance and intermediaries. |
| D      | True     | P2P enables direct device-to-device communication without a central server.                        |

Recap

* A network connects devices so they can share data, services, and resources. Internet connectivity is optional — it’s an additional layer, not a requirement.
* Networks scale: PAN → LAN/WLAN → WAN → Internet, each adding reach and complexity.
* WLANs are wireless LANs, trading some reliability and range for mobility.
* Smaller networks are generally faster, simpler, and easier to secure; larger networks introduce latency, cost, and management overhead.
* Peer‑to‑peer suits small, informal setups; client‑server supports centralized control and scalability, but depends on server availability.

<Frame>
  <img alt="A presenter wearing a KodeKloud shirt stands on the right while a purple slide fills the left side, titled &#x22;Describe what a network is...&#x22; with a highlighted box that says &#x22;Connects devices to share.&#x22;" />
</Frame>

Next up: routing, path selection, and the protocols that move your data across networks. These topics explain how routers choose optimal paths, how packets travel between networks, and how reliability and ordering are maintained.

Further reading and references:

* [What is a LAN (Local Area Network)? — Cloudflare Learning](https://www.cloudflare.com/learning/ddos/glossary/local-area-network-lan/)
* [Wide Area Network (WAN) — Cisco](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-a-wan.html)
* [Peer-to-peer — Wikipedia](https://en.wikipedia.org/wiki/Peer-to-peer)
* [Client–server model — Wikipedia](https://en.wikipedia.org/wiki/Client–server_model)

- [Watch Video](https://learn.kodekloud.com/user/courses/networks-and-communications/module/f96c3ffe-8569-4a9d-99c2-2fe528af47cb/lesson/2c4351da-b634-49b2-9ee5-ad2baf84f54f)
