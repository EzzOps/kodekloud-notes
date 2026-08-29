# Build stage: contains source, dev deps, and compilers
FROM node:18 AS build
WORKDIR /app

# Install all dependencies (including devDependencies for build)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Final stage: a minimal runtime image
FROM node:18-alpine
WORKDIR /app

# Copy only what's needed from the build stage
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./

# Install only production dependencies in the final image
RUN npm ci --production

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

The build tools (TypeScript compiler, testing tools, etc.) remain only in the build stage and are not present in the runtime image.

<Frame>
  <img alt="The image outlines &#x22;3 Things&#x22; related to multi-stage builds, depicting a process from a &#x22;Build Stage&#x22; with node modules and a TypeScript compiler to a &#x22;Final Stage&#x22; with only the compiled output." />
</Frame>

2. Start from a small base image

* Prefer `-slim` or Alpine-based images when appropriate. Alpine-based images are often much smaller than Debian/Ubuntu equivalents.
* For the smallest runtime and reduced attack surface, consider distroless images such as `gcr.io/distroless/nodejs:18`. Distroless images remove package managers and shells.
* Test compatibility: Alpine uses musl instead of glibc, so some native Node modules may fail.

<Callout icon="warning">
  Alpine uses musl instead of glibc; some native Node modules built against glibc may fail on Alpine. If your app depends on native binaries, either build those binaries for musl or use a `-slim`/glibc-based image. Always test before switching base images.
</Callout>

3. Add a good .dockerignore

* Many Docker builds accidentally include `node_modules`, `.git`, local configs, test folders, and large artifacts in the build context. That bloats the build context and can leak into the image.
* A `.dockerignore` keeps unnecessary files out of the build context (like `.gitignore` for Docker).

Example `.dockerignore`:

```text theme={null}
node_modules
.git
npm-debug.log
Dockerfile*
.dockerignore
.env
*.md
tests
coverage
.vscode
```

Practical tips and tools

* Inspect layers to find the biggest contributors:
  * `docker images` and `docker history <image:tag>` show layer sizes.
  * Use dive to visualize layers and contents: [https://github.com/wagoodman/dive](https://github.com/wagoodman/dive)
* Combine RUN steps to reduce intermediate layers and clean up package caches in the same RUN to avoid leftover files.
  * Example: `RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*`
* Use `--no-install-recommends` on Debian/Ubuntu when installing packages to avoid extra packages.
* Avoid committing secrets or large artifacts into the image or build context.
* Consider build-time dependency separation: compile native modules in the build stage, then copy compiled artifacts into the runtime stage.

Links and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — deploy time and autoscaling context
* dive — layer inspection: [https://github.com/wagoodman/dive](https://github.com/wagoodman/dive)
* Distroless images: [https://github.com/GoogleContainerTools/distroless](https://github.com/GoogleContainerTools/distroless)

<Callout icon="lightbulb">
  A small, minimal image improves bootstrap time, reduces network/IO costs, and reduces your production attack surface. Multi-stage builds + a minimal base image + a proper `.dockerignore` usually solve most "fat image" problems.
</Callout>

Keep these three practices in mind and you'll turn that 2 GB image into something fast, secure, cost-efficient, and friendly for autoscaling and rapid deploys.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/1d3d5877-dbf7-4105-8bc2-2c619ac62421/lesson/cfa03d1f-517e-411d-ba65-7beee9934f18" />
</CardGroup>


# How Does Kafka Work

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Interview-Setup/How-Does-Kafka-Work/page

Explains how Kafka works, covering producers, topics, partitions, consumer groups, replication, and delivery semantics using an e-commerce checkout example

In this lesson we'll cover the problem Kafka solves, how it organizes event data, and the guarantees it provides. We'll use a simple e-commerce checkout example to explain producers, topics, partitions, consumer groups, replication, and delivery semantics.

Imagine a shopping site where a customer places an order. The checkout service handles the order, but multiple other services must react to that same event: send a confirmation email, update inventory, and push analytics.

A straightforward but fragile design is for the checkout service to call each of those downstream services synchronously. That design introduces two issues:

<Frame>
  <img alt="The image depicts a flowchart illustrating a checkout process without Kafka, showing services like email, inventory, and analytics coupled directly to a checkout service. An &#x22;interviewer&#x22; and &#x22;candidate&#x22; are shown on opposite sides, with the phrase &#x22;decouples producers & consumers&#x22; at the top." />
</Frame>

* Tight coupling: the checkout service must know about every downstream service. Adding a loyalty program or another integration requires changes to checkout.
* Blocking and reliability: the checkout flow waits on each downstream call. If one service is slow or unavailable, checkout is impacted.

Kafka resolves both problems by decoupling producers (writers) from consumers (readers). Instead of calling each service, the checkout service writes an order event into Kafka. Other services read those events independently, at their own pace, and can even replay history.

## Producers, topics, partitions, and offsets

* Producers write events into Kafka topics.
* Consumers read events from topics.
* The producer does not need to know who will read the events.
* Kafka retains events for a configurable period (or indefinitely), so new consumers can read past events from the beginning.

What does Kafka store internally?

* Topic: a named stream of events, e.g. `checkout-orders`.
* Event (message): one produced message is stored as one event — Kafka doesn't split a single produced message across multiple events.
* Partition: each topic is split into partitions. A partition is an ordered, immutable sequence of events.
* Offset: within a partition, each event gets a sequential offset (0, 1, 2, ...).

If `checkout-orders` has three partitions, Kafka will place each order into one partition (based on a partition key or a partitioner). For example, order 101 → partition 0 offset 0, order 102 → partition 1 offset 0, etc.

Why partition a topic? Two reasons: scale and parallelism.

<Frame>
  <img alt="The image depicts a diagram illustrating a data processing flow, labeled &#x22;Scale + parallel reads,&#x22; with partitions for checkout orders handled by a checkout service. Two figures labeled &#x22;Interviewer&#x22; and &#x22;Candidate&#x22; sit opposite each other." />
</Frame>

* With one partition, only a single broker and a single reader handle the topic's load.
* With multiple partitions, Kafka can spread partitions across brokers to increase throughput, and multiple consumers can read in parallel.

Important: ordering is only guaranteed within a single partition—not across partitions. If ordering for a logical entity matters (for example, all events for one customer), assign a key (commonly the customer ID). Kafka’s default partitioner hashes that key so all events with the same key map to the same partition and retain their relative order.

Note: changing the number of partitions can change how keys map to partitions for future messages, which may affect ordering guarantees for subsequent events.

Example commands and message format

* Create a topic with 3 partitions and replication factor 2:

```bash theme={null}
kafka-topics.sh --create \
  --topic checkout-orders \
  --partitions 3 \
  --replication-factor 2 \
  --bootstrap-server kafka:9092
```

* Produce a message with a key (so it hashes to a partition consistently):

```bash theme={null}
