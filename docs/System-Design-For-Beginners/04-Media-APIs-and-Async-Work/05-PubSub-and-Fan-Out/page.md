# Producer: save photo and enqueue resize job
import json

def save_photo(file):
    s3_key = upload_to_s3(file)            # upload original to object storage
    db.save({'s3_key': s3_key})            # save metadata
    message = json.dumps({'s3_key': s3_key})
    queue.send_message(QueueUrl=QUEUE_URL, MessageBody=message)
    return {'status': 'ok'}                 # return immediately to the client
```

Consumer — poll the queue and process jobs idempotently:

```python theme={null}
# Consumer: poll queue, process messages idempotently
import json

def process_messages():
    messages = queue.receive_messages(QueueUrl=QUEUE_URL, MaxNumberOfMessages=10)
    for msg in messages:
        body = json.loads(msg.body)
        s3_key = body['s3_key']

        if already_processed(s3_key):      # idempotency check
            queue.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg.receipt_handle)
            continue

        resize_image_from_s3(s3_key)
        mark_processed(s3_key)              # record that the job is done
        queue.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg.receipt_handle)
```

When to use message queues (quick guide)

| Scenario                                           | Use queue?                                                   |
| -------------------------------------------------- | ------------------------------------------------------------ |
| Short request/response tasks                       | No                                                           |
| Long-running or CPU-intensive background work      | Yes                                                          |
| Rate-limited downstream services                   | Yes (buffer requests)                                        |
| Need to decouple systems and absorb traffic spikes | Yes                                                          |
| Strict exactly-once side effects (e.g., billing)   | Use caution — design idempotency or transactional safeguards |

Summary

Message queues let you safely hand off long-running or unreliable tasks, decouple producers from consumers, buffer traffic spikes, and simplify scaling and recovery. Common real-world options include [RabbitMQ](https://www.rabbitmq.com/) and [Amazon SQS](https://aws.amazon.com/sqs/). For operations with critical side effects, combine queues with idempotency checks, deduplication, or transactional outbox patterns.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/02240fc4-695f-4112-9594-bb05cfc5ca73/lesson/f88dd042-654a-4b46-9640-6d69abbe1774)


# PubSub and Fan Out

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Media-APIs-and-Async-Work/PubSub-and-Fan-Out/page

Explains pub/sub and fan-out for decoupling photo upload events so multiple independent services like thumbnails, feeds, indexing, and scanners process their own copies.

When a user uploads a photo, the application saves the file and emits a message to a messaging system. In a simple queue-based design, a single worker picks up that message and resizes the image. That works well when exactly one thing must happen for every event.

However, as the product grows, a single upload typically triggers many independent actions at once. For example, beyond creating thumbnails, an upload might need to:

* Update the home feeds of everyone who follows the uploader.
* Add the photo to the search index.
* Run a banned-content scanner.
* And more as features are added.

Each of these is a separate reaction to the same upload event.

<Frame>
  <img alt="The image illustrates a workflow of uploading a photo, which triggers multiple processes like creating thumbnails, updating home feeds, and indexing for search. The text emphasizes that every new feature requires an additional process." />
</Frame>

For situations where one event must trigger many independent reactions, the publish–subscribe (pub/sub) pattern is a better fit.

Instead of the `SavePhoto` function calling each downstream service directly, `SavePhoto` publishes a single event (for example, `photo:99:posted`) to a topic and moves on. The publisher does not need to know who subscribes — it only announces what happened.

Subscribers register interest in that topic and process their own copy of the event:

* The Thumbnail Service subscribes to create thumbnails.
* The Feed Service subscribes to update followers’ home feeds.
* The Search Indexer subscribes to add the photo to the search index.
* The Banned Content Scanner subscribes to check for illicit content.

When the event is published, each subscriber receives its own copy and processes it independently. If a service runs multiple instances that should share the work for the same subscription, those instances typically use a shared subscription or consumer group so messages are partitioned among them. Different services that should each receive the event use separate subscriptions so each gets its own copy. Inside a subscriber, a pool of workers can further parallelize processing (for example, multiple thumbnail workers handling a batch).

This pattern — one event fanning out to many listeners — is called fan-out.

Compare queue and pub/sub:

<Frame>
  <img alt="The image compares &#x22;Queue&#x22; and &#x22;Pub-Sub&#x22; messaging systems. It illustrates how a queue sends one message to one worker, while pub-sub sends one event to multiple subscribers." />
</Frame>

A quick comparison:

| System  | Behavior                                                       | When to use                                                                                                 |
| ------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Queue   | `one message → one worker` — work is partitioned among workers | Single responsibility tasks where exactly one consumer should process each job (e.g., background job queue) |
| Pub/Sub | `one event → many subscribers` — each subscriber gets a copy   | Events that should trigger many independent reactions (e.g., analytics, indexing, notifications)            |

The main advantages of pub/sub are loose coupling and fault isolation. Services don’t need to know about one another: to add a new feature (such as a banned-content scanner), you don’t modify `SavePhoto`; you simply subscribe the scanner to the `photo:posted` topic and it starts receiving events.

Fault isolation: each subscriber can be slow or fail without blocking others. With a durable pub/sub system, events are retained so a subscriber that was down can resume and catch up. For example, if the Search Indexer is down when an upload happens, the Thumbnail and Feed updates still run; when the indexer restarts it consumes the backlog and updates the index.

<Frame>
  <img alt="The image is a flowchart illustrating a photo-sharing process, where a saved photo is published and distributed to various features like thumbnails, home feeds, search index, and a banned-content scanner. The title reads &#x22;Add a Feature — Touch Nothing.&#x22;" />
</Frame>

Durable event streaming platforms (for example, Kafka) implement pub/sub semantics that make replay and catch-up straightforward. Kafka persists events in a commit log for a configurable retention period so services can replay messages or catch up after downtime. Independent services read the same events at their own pace by using separate consumer groups (each service typically uses its own consumer group to receive its own copy). Kafka provides ordering guarantees per-partition and usually offers at-least-once delivery semantics, so consumers should handle duplicates or implement idempotent processing when exactly-once behavior is required.

<Frame>
  <img alt="The image is a flowchart showing how a photo is published and processed through a system using Kafka, resulting in reactions like thumbnails, home feeds, search index updates, and content scanning. It's titled &#x22;One Event, Many Reactions.&#x22;" />
</Frame>

When to choose pub/sub

* Use pub/sub when one occurrence must trigger many independent reactions and those reactions should evolve independently.
* Use a queue when exactly one worker must process each job and the work is a single responsibility.

Shift your mental model from “after I upload, I call A, B, and C” to “I announce that an upload happened, and interested systems subscribe and handle it independently.”

> **lightbulb** Pub/Sub is ideal for decoupling and scaling many independent reactions to the same event. For simple one-off work items where exactly one worker must process the job, a queue is still the simpler and more appropriate choice.

## Links and references

* Kafka (event streaming): [https://learn.kodekloud.com/user/courses/event-streaming-with-kafka](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka)
* Pub/Sub pattern overview: [https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe\_pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/02240fc4-695f-4112-9594-bb05cfc5ca73/lesson/14bc3bc8-5893-408f-a952-f348d262e51e)
