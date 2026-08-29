# Real Time Polling vs WebSockets

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Media-APIs-and-Async-Work/Real-Time-Polling-vs-WebSockets/page

Comparison of real-time notification methods like polling, long polling, SSE, WebSockets, and push services, explaining trade-offs, scaling, and mobile background considerations.

Imagine someone just liked your photo and — without refreshing the screen or manually asking the server — a small red dot appears on the notification bell in your mobile app within a second.

<Frame>
  <img alt="The image illustrates a notification system for an app, showing how a red dot appears on a notification bell after server communication, without refreshing, when someone likes a post." />
</Frame>

That instant update feels “real-time,” but HTTP APIs follow a request–response model: the client asks and the server answers. The server cannot proactively send a response until the client has made a request.

<Frame>
  <img alt="The image illustrates a &#x22;Request and Response&#x22; process between a client application and a server, connected by an API. It shows the client sending a request and the server responding." />
</Frame>

When someone likes your photo, the server needs an additional mechanism to deliver that update to your phone. Below are the common approaches, their trade-offs, and when to use each.

## Polling

Polling is the simplest strategy: the client periodically asks the server, “Anything new for me?” (for example, every few seconds). The server replies immediately with the current state (often “no changes”).

* Pros: Extremely simple; works in almost every environment (HTTP/1.1, proxies, corporate firewalls).
* Cons: Wastes CPU, memory, and bandwidth when many clients poll frequently and most responses are empty.

Example cost estimate: if 1,000,000 users poll every 5 seconds, that’s approximately 200,000 requests/second — and most responses will be “no change,” leading to heavy wasted load.

<Frame>
  <img alt="The image illustrates the concept of polling in app-server communication, where the app repeatedly asks the server for updates, and the server responds with &#x22;no&#x22; if there's nothing new." />
</Frame>

<Frame>
  <img alt="The image illustrates a polling system where 1,000,000 users are sending frequent requests to a server, generating approximately 200,000 requests per second, even though most responses indicate &#x22;nothing changed.&#x22;" />
</Frame>

When is polling acceptable?

* Use polling when a small delay (seconds) is tolerable and simplicity is valuable — e.g., a like-count that updates a few seconds late is usually fine.
* It’s straightforward to implement and may be adequate for many non-critical features.

<Frame>
  <img alt="The image discusses when polling is worth it, highlighting that it is suitable for situations where slight lag is acceptable, as it's a trade-off for simplicity. It shows a visual with a mobile app interface and a server, noting that a few seconds' delay often goes unnoticed." />
</Frame>

## Long Polling (HTTP Long Polling)

Long polling is a pragmatic improvement over short-interval polling:

* The client sends a request asking “Anything new?”
* The server holds that request open until it has new data or a timeout occurs.
* When new data arrives, the server responds immediately; the client then typically issues another long-poll request to continue listening.

Advantages over regular polling:

* Fewer requests overall.
* Much lower wasted work when updates are infrequent.

In practice, servers implement reasonable timeouts and reconnection logic so connections don’t hang forever, making long polling a robust compromise when bi-directional streaming is not required.

<Frame>
  <img alt="The image illustrates a long polling process for notifications in a mobile app. It compares polling and long polling, showing the app waiting for server responses for updates such as likes." />
</Frame>

## WebSockets

WebSockets open a single long-lived TCP connection between client and server. After the handshake, both ends can push messages anytime without repeated HTTP handshakes.

* Pros: Low latency, true bi-directional communication; ideal for chat, multiplayer games, collaborative editing, and live feeds.
* Cons: Stateful connections on the server; each connection consumes memory and file descriptors.

<Frame>
  <img alt="The image is an illustration explaining WebSockets, showing a continuous open connection between a user app and a server enabling real-time interactions, like live comments during events. It depicts a phone interface and a simplified server representation connected by a line to convey seamless data exchange." />
</Frame>

Scaling WebSockets typically requires:

* Sticky sessions or connection affinity at the load balancer.
* Connection sharding across multiple socket servers.
* A distributed pub/sub layer (for example, `Redis` or `Kafka`) or managed socket services to route messages to the correct connection.
* Operational care for deploys, restarts, and connection migration.

## Trade-offs Summary

| Approach                 | Best For                              |               Latency | Server State                   | Complexity to Scale |
| ------------------------ | ------------------------------------- | --------------------: | ------------------------------ | ------------------- |
| Polling                  | Simple features with tolerant latency |               Seconds | Stateless                      | Low                 |
| Long Polling             | Occasional pushes, fewer requests     | Sub-second to seconds | Semi-stateless (requests held) | Medium              |
| WebSockets               | Bi-directional, low-latency apps      |          Milliseconds | Stateful (per-connection)      | High                |
| Server-Sent Events (SSE) | One-way server-to-client streaming    |                   Low | Stateful (connections)         | Medium              |
| Platform Push (APNs/FCM) | Background mobile notifications       | Variable (OS-managed) | Offloaded to platform          | Low (for apps)      |

## Server-Sent Events (SSE)

* SSE is a lightweight, one-way streaming solution where the server pushes events and the client listens.
* It uses regular HTTP (Content-Type: `text/event-stream`) and supports automatic reconnection.
* SSE is simpler than WebSockets when only server-to-client updates are required (e.g., live score feeds, stock tickers).

## Mobile and Background Considerations

All the above methods assume the app is running and can maintain a connection. Mobile OSes restrict background network activity because maintaining many open connections drains battery.

When your app is closed or backgrounded, platform push services are the reliable mechanism:

* iOS: Apple Push Notification service (APNs) — [https://developer.apple.com/notifications/](https://developer.apple.com/notifications/)
* Android: Firebase Cloud Messaging (FCM) — [https://firebase.google.com/docs/cloud-messaging](https://firebase.google.com/docs/cloud-messaging)

<Frame>
  <img alt="The image illustrates a process flow when an app is closed, involving the phone's OS, a server, and cloud services like Apple Push Notification Service (APNs) and Firebase Cloud Messaging (FCM). It highlights the impact on battery drain and the role of the OS in managing notifications." />
</Frame>

> **warning** Mobile platforms intentionally limit background network activity to conserve battery. Rely on APNs/FCM for closed-app notifications rather than trying to keep persistent connections for each app.

## Decision Guide — Which to pick?

* Start with the simplest solution that meets feature and latency requirements.
  * Polling: choose when slight delays are acceptable and simplicity matters.
  * Long polling or SSE: choose when the server mainly pushes occasional updates and you want to reduce wasted requests.
  * WebSockets: choose when you need frequent, low-latency, bi-directional communication (chat, multiplayer, collaborative editing).
  * APNs/FCM: use for delivering notifications to backgrounded/closed mobile apps.

> **lightbulb** Choose the simplest, reliable option that satisfies latency and scale requirements. If you adopt stateful connections (WebSockets), plan for scaling using pub/sub layers, connection sharding, or managed socket services.

## Links and References

* [Redis](https://redis.io/) — common pub/sub and message-broker option
* [Kafka](https://kafka.apache.org/) — durable, scalable streaming platform
* [Apple Push Notification service (APNs)](https://developer.apple.com/notifications/)
* [Firebase Cloud Messaging (FCM)](https://firebase.google.com/docs/cloud-messaging)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/02240fc4-695f-4112-9594-bb05cfc5ca73/lesson/85034e7b-8245-4008-8ff9-e1e12f2ec5d4)
