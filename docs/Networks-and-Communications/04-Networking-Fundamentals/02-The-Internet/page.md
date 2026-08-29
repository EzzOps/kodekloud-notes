# The Internet

Source: https://notes.kodekloud.com/docs/Networks-and-Communications/Networking-Fundamentals/The-Internet/page

Explains how data is split into packets, addressed with IP and MAC, routed across networks, and switched within LANs to deliver web requests.

Have you ever wondered how a webpage hosted halfway around the world appears on your screen in seconds?

You type an address, press Enter, and a few moments later the page loads. Behind the scenes, that request and the response travel across cities, countries, and under oceans — all as a sequence of smaller, labeled data chunks. In this lesson we’ll trace that round trip from Kody in India to a server in California and back, covering four core ideas:

* how devices split and reassemble data into packets,
* how addressing (IP and MAC) helps packets find their destination,
* how routers forward packets between networks, and
* how switches deliver frames inside local networks.

When Kody hits Enter, her device prepares an HTTP request for [www.calicatnip.com](http://www.calicatnip.com). The request itself is just data, but sending it as one large blob would be fragile and inefficient: if a small part gets corrupted, the entire message would need re-sending. Instead, data is split into packets.

Each packet is a labeled, self-contained chunk that’s easier to transmit, verify, and recover. A typical packet contains:

* a header with delivery information (source/destination IPs, source/destination ports, protocol, sequence or identification fields),
* a payload carrying part of the message,
* and usually a checksum or CRC to detect transmission errors.

<Frame>
  <img alt="A man in a black KodeKloud shirt stands beside a laptop screen showing a colorful diagram of a GET webpage request split into packets and a payload/header message chunk. A small cartoon cat is standing on the laptop keyboard." />
</Frame>

Packet anatomy (quick reference)

|      Component | Purpose                                   | Example fields                                                |
| -------------: | ----------------------------------------- | ------------------------------------------------------------- |
|         Header | Delivery metadata used by network devices | `src IP`, `dst IP`, `src port`, `dst port`, `protocol`, `seq` |
|        Payload | The actual chunk of the application data  | part of an HTTP GET or HTML text                              |
| Checksum / CRC | Error detection for the packet            | TCP checksum, CRC32 (link-layer)                              |

Splitting data into packets makes networks robust and efficient: only the damaged packets need retransmitting rather than the whole file.

DNS and addressing

Human-friendly names like [www.calicatnip.com](http://www.calicatnip.com) must be translated into numeric IP addresses that routers and hosts can use. The Domain Name System (DNS) performs this translation — acting like the Internet’s phone book.

* DNS returns the destination IP address that identifies the server on the network.
* Kody’s laptop uses a private IP inside her home LAN; her home router holds a public IP visible to the wider Internet.
* The packet header therefore carries a source IP (where it originated) and a destination IP (where it should arrive).

<Callout icon="lightbulb">
  DNS: try `dig +short www.calicatnip.com` or `nslookup www.calicatnip.com` to see how names map to addresses. Note that `private` IPs (RFC 1918) are only meaningful inside a local network; NAT translates private-to-public at the router.
</Callout>

Devices also need a way to identify which physical interface should receive a frame on a local link. That role is filled by MAC addresses — hardware identifiers burned into network interfaces. In short:

| Addressing type | Scope                                 | Used by                       |
| --------------- | ------------------------------------- | ----------------------------- |
| IP address      | Global/logical across networks        | Routers (layer 3 routing)     |
| MAC address     | Local/link-layer within a LAN segment | Switches (layer 2 forwarding) |

<Frame>
  <img alt="A laptop screen displays an IP address (203.0.113.42) and a fingerprint icon labeled &#x22;MAC Address.&#x22; A presenter wearing a KodeKloud t-shirt stands to the right against a dark background." />
</Frame>

Routing: how packets find their way across the Internet

Once a packet leaves Kody’s laptop it typically goes to her home router, then to her ISP, and onward through a chain of routers until it reaches the server’s network. Routers operate like distributed sorting offices:

* Each router reads the destination IP in the packet header and consults its routing table to decide the next hop.
* Routers forward packets hop-by-hop rather than computing a full end-to-end path for each packet.
* Routing tables are built and updated using routing protocols (for example, BGP between ASes, OSPF or IS‑IS within an AS).
* When links fail or become congested, routing protocols help routers converge on new paths.

This hop-by-hop model means return packets may take the same path back, or a completely different one, depending on real-time routing decisions.

<Frame>
  <img alt="A stylized network diagram labeled &#x22;Home Router,&#x22; &#x22;ISP,&#x22; and &#x22;Host Server&#x22; shows arrows indicating path references between devices. A presenter wearing a KodeKloud shirt stands to the right of the diagram." />
</Frame>

Switching: local delivery inside a LAN

While routers handle inter-network forwarding using IP addresses, switches move frames within each local network using MAC addresses.

* Switches learn which MAC addresses are reachable on which physical ports and build a MAC address table.
* When a frame arrives, the switch looks up the destination MAC and forwards the frame only to the port where that MAC was last seen.
* This design is efficient and supports many simultaneous conversations over the same physical media (multiplexing), unlike circuit switching which reserved a dedicated path.

Circuit switching (telephone-style) reserved an exclusive path for a session; modern Ethernet uses packet switching, allowing many devices to share links dynamically.

<Frame>
  <img alt="A presentation slide illustrating packet switching, showing two users (a laptop and a smartphone) connecting through a network switch with arrows labeled MAC 1 and MAC 2. A presenter wearing a &#x22;KodeKloud&#x22; t‑shirt stands at the right." />
</Frame>

Pop quiz — which of the following is true about how Kody's data is delivered?

A. Data is divided into smaller packets that are labeled and reassembled on arrival.\
B. MAC addresses are used to route packets across the Internet.\
C. The entire route is chosen before the packet leaves Kody's device.\
D. Switches reserve a dedicated path between devices to avoid collisions.

Pause now to lock in your answer.

Correct answer: A. Data is divided into smaller packets that are labeled and reassembled on arrival.

Why the other options are incorrect:

* B: MAC addresses are used only for local delivery inside a LAN; routers use IP addresses to forward packets between networks.
* C: Routers make hop-by-hop forwarding decisions; they do not precompute a fixed end-to-end path for each packet.
* D: Circuit switching reserved dedicated paths; modern Ethernet switching is packet-based and multiplexes many flows over the same media.

Quick summary — the essentials

* Data is split into packets to reduce retransmission cost; packets include a header, payload, and checksum.
* Packets travel independently and are reassembled at the receiver using sequence identifiers.
* IP addresses provide logical, globally routable addressing across networks.
* MAC addresses provide link-layer addressing for local delivery inside a LAN.
* Routers use destination IPs and routing tables to choose the next hop; routes can change dynamically.
* Switches use MAC addresses to forward frames inside local networks without reserving a path.

<Frame>
  <img alt="A presenter stands on the right wearing a KodeKloud t-shirt against a black background. On the left is a purple slide about networking titled &#x22;Explain how switches move data within a local network,&#x22; mentioning MAC addresses and switching." />
</Frame>

Hardware and next steps

The routers, switches, cables, and servers are the physical and virtual infrastructure that makes these processes possible. In the next lesson we’ll examine the common hardware found in home and datacenter networks and how they’re configured.

Further reading and references

* DNS: [https://en.wikipedia.org/wiki/Domain\_Name\_System](https://en.wikipedia.org/wiki/Domain_Name_System)
* IP addressing: [https://tools.ietf.org/html/rfc791](https://tools.ietf.org/html/rfc791)
* MAC addresses and Ethernet: [https://en.wikipedia.org/wiki/MAC\_address](https://en.wikipedia.org/wiki/MAC_address)
* BGP overview: [https://en.wikipedia.org/wiki/Border\_Gateway\_Protocol](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)
* OSPF overview: [https://en.wikipedia.org/wiki/Open\_Shortest\_Path\_First](https://en.wikipedia.org/wiki/Open_Shortest_Path_First)

Additional commands to try locally

```bash theme={null}
