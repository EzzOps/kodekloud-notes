# How a Request Actually Travels

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Foundations-One-Server/How-a-Request-Actually-Travels/page

How a user request travels from device to server covering DNS resolution, IP addressing, HTTPS and TLS, caching, CDNs, and latency effects on performance.

Let's pause the scaling story for a moment and answer a foundational question we've been skipping:

A user opens their phone, types your app's address — `photoapp.com` — and taps Enter. What actually happens between that moment and the feed appearing on their screen?

Quick reminder: a server is just a computer in a data center whose job is answering user requests. Like every machine on the internet, your server

<Frame>
  <img alt="The image illustrates a client-server interaction, showing a smartphone sending a request to a server with &#x22;photoapp.com&#x22; and the server responding. The text emphasizes that a server has an address." />
</Frame>

has an address — an IP address. Think of the IP address as the machine's phone number: a string of numbers that tells the network exactly where to deliver packets.

<Frame>
  <img alt="The image illustrates the concept that a server has an address, showing a phone with a website URL &#x22;photoapp.com&#x22; and an IP address &#x22;203.0.113.5&#x22; labeled as the machine's phone number." />
</Frame>

But users type names, not numbers. When the user typed `photoapp.com`, the phone first asks a DNS resolver: what IP address is behind that name? This lookup is performed by the Domain Name System (DNS).

<Frame>
  <img alt="The image illustrates the Domain Name System (DNS) as the internet's &#x22;phone book,&#x22; showing how domain names like &#x22;photoapp.com&#x22; are mapped to IP addresses. A mobile device queries a domain name, which is resolved to an IP address for accessing the server." />
</Frame>

Think of DNS as the internet's phone book: the device asks DNS, “Where is `photoapp.com`?” DNS replies with an IP address so the device knows which machine to contact.

Once the phone has the IP address, the client and the server need a common protocol to exchange messages. In practice that protocol is HTTP (more often today HTTP/2 or HTTP/3). The phone sends a request like “Get me the home feed,” and the server does the work and returns a response containing the feed data.

These days this communication almost always runs over HTTPS rather than plain HTTP. The “S” stands for secure: HTTPS encrypts the conversation between client and server. Without encryption, anyone on the same network (for example, someone on a coffee‑shop Wi‑Fi) could read the traffic — including sensitive data like passwords.

<Frame>
  <img alt="The image illustrates how HTTP transmits plain text data, such as passwords, which anyone on the WiFi can read, and highlights the importance of HTTPS for security." />
</Frame>

With HTTPS the request and response payloads are encrypted, so intermediaries cannot read the contents. Some metadata (for example, IP addresses or the TLS Server Name Indication) can still be visible. How the secure connection is established (the TLS handshake and certificate management) is an additional topic we won't dive into here.

A couple of optimizations play an outsized role in real-world performance:

* A cache can avoid trips to your database for frequently requested data.
* A CDN (Content Delivery Network) serves static assets like thumbnails from locations geographically close to users.

> **lightbulb** Latency measures how long a single round trip takes between the client and the server. Bandwidth measures how much data can transfer at once — the width of the pipe.

This distinction matters for a photo app. A feed showing thirty thumbnails can be slow not because the images are large, but because of round trips. If each thumbnail requires a separate request that travels halfway around the world, thirty round trips add up — even on fast Wi‑Fi. Both caching and CDNs are designed primarily to reduce round‑trip latency.

<Frame>
  <img alt="The image illustrates a conceptual diagram of slow image loading due to round trips, showing a smartphone app displaying images and a global server. It highlights the impact of round trips on speed and suggests using cache and CDN to improve performance." />
</Frame>

Putting the pieces together: the phone asks DNS for the IP address of the site, the phone sends an HTTPS request to that address, and the server performs the work and returns a response.

<Frame>
  <img alt="The image illustrates a visual representation of a digital request journey, showing the flow from a mobile app interface to a server through steps like DNS, HTTPS request, and server response." />
</Frame>

One important wrinkle remains: the DNS answer in the simple picture above looked like it pointed to a single server, but real deployments typically run multiple servers — for example, ten. Which of those ten should the phone talk to?

Key concepts mentioned

| Concept     | What it does                                                     | Learn more                                                              |
| ----------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| DNS         | Maps a domain name (e.g., `photoapp.com`) to an IP address       | [DNS basics](https://en.wikipedia.org/wiki/Domain_Name_System)          |
| IP address  | The numeric “address” of a machine on the network                | [IP addressing explanation](https://en.wikipedia.org/wiki/IP_address)   |
| HTTPS / TLS | Encrypts client–server communication                             | [TLS overview](https://datatracker.ietf.org/doc/html/rfc5246)           |
| CDN         | Serves static assets from locations near users to reduce latency | [CDN concepts](https://en.wikipedia.org/wiki/Content_delivery_network)  |
| Cache       | Stores frequently used data to avoid expensive backend work      | [Caching strategies](https://en.wikipedia.org/wiki/Cache_\(computing\)) |

Further reading and references

* [How the Domain Name System (DNS) Works](https://developers.google.com/speed/public-dns/docs/overview)
* [Introduction to TLS / HTTPS](https://letsencrypt.org/docs/)
* [Content Delivery Networks (CDNs) explained](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/df166cca-6100-4b0c-af69-1c80618a63c1/lesson/319a26f6-6b9b-4f1d-9ea2-b69817662bdf)
