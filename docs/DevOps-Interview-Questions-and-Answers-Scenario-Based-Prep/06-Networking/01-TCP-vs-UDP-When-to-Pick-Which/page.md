# TCP vs UDP When to Pick Which

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Networking/TCP-vs-UDP-When-to-Pick-Which/page

Comparing TCP and UDP for different app needs, using WhatsApp examples to explain when reliability or low latency is preferred and how security and application protocols fit

This guide explains the practical differences between TCP and UDP using a WhatsApp-style backend as an example: text messages, voice/video calls, and how apps pick the appropriate transport for each use case.

## Text messaging: why TCP fits

When you send a text like "I'm running late, be there in ten", the receiver must get exactly what you typed — no missing words, no reordering. TCP provides:

* Reliable delivery (retransmits lost data),
* In-order delivery (reassembles packets using sequence numbers),
* Flow and congestion control (keeps the network stable).

These features make TCP ideal for messaging and other data that must arrive intact and in order.

<Frame>
  <img alt="The image explains how a text message should be delivered correctly by TCP, showing a message saying &#x22;I'm running late, be there in ten,&#x22; emphasizing delivery without errors like &#x22;Be ten in there.&#x22;" />
</Frame>

## Connection setup: TCP three-way handshake

Before application data flows, TCP performs a three-way handshake:

1. Client sends SYN (request to open connection).
2. Server replies with SYN-ACK (acknowledges request).
3. Client sends ACK (completes handshake).

Only after this exchange can the devices start reliable data transfer.

<Frame>
  <img alt="The image illustrates the TCP 3-way handshake process between a phone and a WhatsApp server, showing the exchange of SYN, SYN-ACK, and ACK packets." />
</Frame>

## Packetization, ordering, and retransmission

Once the connection is established, TCP breaks data into segments, assigns sequence numbers, and handles:

* Missing packets: the receiver detects gaps and triggers retransmission.
* Out-of-order arrivals: TCP reorders packets before handing data to the application.

This guarantees the application sees a continuous, ordered byte stream.

<Frame>
  <img alt="The image illustrates a network communication scenario where a packet labeled &#x22;#2&#x22; goes missing between a phone and a server." />
</Frame>

## Real-time audio/video: why UDP is usually preferred

Voice and video calls stream many small packets continuously. For real-time media, timeliness matters more than recovering every lost packet. Using TCP introduces two key problems for live streams:

* Head-of-line blocking: later packets wait for retransmissions of earlier lost packets, causing pauses.
* TCP congestion response: loss causes reduced send rates, increasing latency and making audio/video choppy.

Because a brief packet loss may be less harmful than a stalled stream, real-time applications commonly use UDP for media transport.

<Frame>
  <img alt="The image depicts a concept related to voice calls, indicating a continuous audio stream with packet representation, and notes that TCP is not used." />
</Frame>

## What UDP provides — and what the application layer adds

UDP itself is minimal: no handshake, no guaranteed delivery, no automatic retransmission, and no enforced ordering. Real-time apps build reliability and timing handling in the application layer, typically using protocols such as RTP/SRTP.

Application-layer techniques include:

* Sequence numbers and timestamps (detect lost/late packets and reorder),
* Jitter buffers (smooth variable arrival times),
* Selective retransmission or forward error correction (for non-real-time-critical parts),
* Dropping packets that arrive too late to be useful.

SRTP (Secure RTP) can add confidentiality and integrity for RTP streams carried over UDP.

<Frame>
  <img alt="The image describes UDP (User Datagram Protocol) as having no guarantees, no handshake, no retries, and no ordering, with SRTP (Secure Real-time Transport Protocol) adding sequence numbers and timestamps to audio packets." />
</Frame>

## Use both protocols where appropriate

Many apps keep both connection types simultaneously:

* Media (real-time voice/video): UDP + RTP/SRTP, optimized for low latency.
* Text, file transfer, or control messages: TCP or TLS over TCP (HTTP/2) for reliability and ordering.

Choose the transport based on whether timeliness or guaranteed delivery is the priority.

## Security is orthogonal to TCP vs UDP

Neither transport encrypts payloads by default. Security (encryption, authentication, integrity) must be added at a higher layer:

* Use TLS to secure TCP streams.
* Use SRTP to secure RTP over UDP.
* Use end-to-end application protocols (e.g., Signal Protocol) for message-level encryption.

> **lightbulb** Neither TCP nor UDP provides encryption by default. Use [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security), [SRTP](https://en.wikipedia.org/wiki/Secure_Real-time_Transport_Protocol), or an application-level protocol (e.g., [Signal Protocol](https://en.wikipedia.org/wiki/Signal_Protocol)) to secure transported data.

<Frame>
  <img alt="The image shows a comparison of different security protocols: Signal Protocol with end-to-end encryption, WhatsApp Encryption involving phone and server communications, and TCP/UDP with cleartext transport and no security." />
</Frame>

## Quick comparison

| Characteristic      |                                  TCP |                                           UDP |
| ------------------- | -----------------------------------: | --------------------------------------------: |
| Connection setup    |       Three-way handshake (stateful) |                    Connectionless (stateless) |
| Delivery guarantees |      Reliable, retransmits lost data |                Best-effort, no retransmission |
| Ordering            | In-order delivery (sequence numbers) |                          No enforced ordering |
| Latency behavior    |     Can suffer head-of-line blocking |           Low latency, suitable for real-time |
| Typical use cases   |   Messaging, file transfer, web APIs | VoIP, live video, gaming, real-time telemetry |
| Security            |             Use `TLS` for encryption |            Use `SRTP` or app-layer encryption |

## Summary

* Use TCP when you need reliable, ordered delivery (e.g., text, files, transactional data).
* Use UDP when low latency and timeliness trump perfect delivery (e.g., real-time voice/video), and rely on RTP/SRTP or application logic for sequencing, jitter management, and security.
* Encryption and authentication are implemented at higher layers — choose TLS, SRTP, or application-level end-to-end protocols as required.

## Links and references

* [VoIP — Wikipedia](https://en.wikipedia.org/wiki/VoIP)
* [RTP — Real-time Transport Protocol](https://en.wikipedia.org/wiki/Real-time_Transport_Protocol)
* [SRTP — Secure Real-time Transport Protocol](https://en.wikipedia.org/wiki/Secure_Real-time_Transport_Protocol)
* [TLS — Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security)
* [Signal Protocol](https://en.wikipedia.org/wiki/Signal_Protocol)

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/c1eb3967-23d3-4a34-b23d-14a892f95e1d/lesson/605680c0-3415-4777-955a-d37064b80774)
