# Message Queues

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Media-APIs-and-Async-Work/Message-Queues/page

Explains message queues and how they decouple producers and consumers to handle background tasks, buffer spikes, ensure reliability, and require idempotency for at-least-once delivery.

In this lesson we cover message queues: what they are, why they matter, and how they enable resilient, decoupled systems for handling background work and traffic spikes.

A concrete motivating example is a photo-upload flow in a typical photo app. We don't want to serve full-size images to users, so we generate smaller thumbnails. Thumbnail generation can be slow, so doing it synchronously would make users wait. Instead, we offload this work to a background system.

When a user uploads a photo, the client calls an API such as `POST /photos`. The server-side handler (for example, `savePhoto`) validates the image, stores the original file in object storage (e.g., [S3](https://aws.amazon.com/s3/)), writes metadata to the database, and triggers thumbnail creation.

<Frame>
  <img alt="The image is a flowchart illustrating how an app server processes a photo upload request from a mobile app. It depicts steps such as API call, validation, saving the photo, and storage in object storage and metadata." />
</Frame>

A naive (and inefficient) approach is to call the thumbnail generator (`resizePhoto`) synchronously from `savePhoto`. In this design, the upload handler performs the resize before returning success to the client. If the resize is slow or gets stuck, the user experiences long waits or timeouts.

<Frame>
  <img alt="The image depicts a flowchart illustrating a process for handling photo uploads, showing interactions between a mobile device, an app server, and storage solutions, with the message &#x22;Don't make the user wait.&#x22;" />
</Frame>

A better design is to make the resize task asynchronous. After saving the original photo and metadata, the server returns success to the user immediately and hands the slow work to a background system. The question becomes: how do we hand off the job safely so it won't be lost if the server crashes?

The safe solution is a message queue. Instead of calling `resizePhoto` directly, `savePhoto` writes a small message to a queue (for example, a `resize-photo` queue) describing the job. Then `savePhoto` returns success to the client.

<Frame>
  <img alt="The image is a flowchart depicting a photo upload process using an app server and message queue system. It shows steps from making an API call to saving, resizing the photo, and storing metadata and the object." />
</Frame>

The message persists in the queue until a worker (consumer) picks it up. Thumbnail generation no longer runs inside the main app server; instead, independent worker processes or services poll the queue, process messages, and acknowledge completion.

<Frame>
  <img alt="The image illustrates a workflow diagram for photo processing, showing an app server handling a POST request to save a photo, storing it, and then using a message queue to resize the photo on separate machines." />
</Frame>

Key terms

| Term     | Meaning                                                                                |
| -------- | -------------------------------------------------------------------------------------- |
| Producer | The function or service that puts messages on the queue (e.g., `savePhoto`).           |
| Consumer | The worker that pulls messages and performs the work (e.g., `resizePhoto` worker).     |
| Queue    | The intermediary that decouples producers and consumers; typically durable/persistent. |

Why this decoupling helps

* Producers and consumers are independent: they do not need to know each other's implementation or location.
* Producers return quickly and do not block on slow work.
* The queue acts as a buffer: it absorbs traffic spikes and stores work until consumers are ready.
* Workers can be scaled independently to increase processing throughput.
* If a worker crashes, the message remains in the queue until processed—improving fault tolerance.

<Frame>
  <img alt="The image is a flowchart illustrating a photo processing system where an app server saves photos through an API call, stores them in object storage and metadata, sends them to a message queue, and then a consumer resizes the photos." />
</Frame>

Important nuance: delivery semantics and idempotency

Many queues provide at-least-once delivery. That means a message can sometimes be delivered more than once. Example: a worker receives a message, completes the resize, but crashes before acknowledging the queue; the queue will eventually redeliver the message. Resizing twice is usually harmless, but duplicate effects (such as charging a customer) can be catastrophic.

Design consumers to tolerate duplicate deliveries:

* Make operations idempotent (safe to repeat).
* Or check whether work is already done before acting (e.g., a `processed` flag in the database or checking object existence).

<Frame>
  <img alt="The image is a flowchart illustrating a photo processing system, showing steps from uploading photos via an app to resizing through a message queue system. It includes components like an app server, object storage, metadata, and a consumer for resizing photos." />
</Frame>

> **lightbulb** Message queues typically expose visibility timeouts and acknowledgement semantics. Consumers should acknowledge/delete messages only after successfully finishing their work. Implement idempotency checks or persistent flags so re-delivered messages do not cause duplicate side effects.

Minimal examples (illustrative pseudocode)

Producer — save the photo then enqueue a job:

```python theme={null}
