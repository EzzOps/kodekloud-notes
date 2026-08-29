# using console producer with key parsing
kafka-console-producer.sh --topic checkout-orders --bootstrap-server kafka:9092 \
  --property "parse.key=true" --property "key.separator=:"

# Example message line you would type/publish:
cust-123:{"orderId":101,"items":[{"sku":"X","qty":1}],"total":79.99}
```

* Inspect consumer group offsets:

```bash theme={null}
kafka-consumer-groups.sh --bootstrap-server kafka:9092 --group email-service --describe
```

## Consumer groups and parallel consumption

Consumer groups let multiple consumer instances cooperate to consume a topic without duplicating work. Kafka assigns each partition to exactly one consumer within a consumer group. Examples:

* Topic `checkout-orders` has 3 partitions.
* Analytics service runs 3 instances in the same consumer group → each instance gets one partition and processes in parallel.
* Email service runs 1 instance in its own group → that instance consumes all partitions (and keeps a separate offset).

Each consumer group tracks offsets per partition. If a consumer restarts, it resumes from the last committed offset. If a consumer fails, Kafka reassigns its partitions to remaining consumers (a rebalance).

Different services should use different consumer groups when they need to process the same events independently.

## Replication and broker failure handling

Kafka runs as a cluster of brokers. Partitions are typically replicated across brokers for fault tolerance. Each partition has multiple replicas:

* One replica is the leader for reads/writes.
* Other replicas are followers that replicate the leader’s data.

If the broker hosting the leader fails, Kafka elects an in-sync replica as the new leader, allowing producers and consumers to continue with minimal disruption (assuming replicas are up to date and producer acks are configured appropriately).

<Frame>
  <img alt="The image illustrates a Kafka cluster replication and failover process, showing a transition of leadership from Broker 1 to Broker 2 after Broker 1 goes down, with stick figures labeled as &#x22;interviewer&#x22; and &#x22;candidate.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Replication is controlled by the replication factor (how many copies of each partition exist) and by which replicas are considered in-sync. Kafka promotes a new leader only from replicas that are up to date to avoid data loss.
</Callout>

## Delivery semantics and idempotency

By default, Kafka provides at-least-once delivery semantics: events are not lost, but in some failure scenarios they may be processed more than once.

Example of duplicate processing:

* Consumer reads order 101 and performs side effects (charge customer, send email).
* Before committing the offset, the consumer crashes.
* On restart, since the offset was not committed, the consumer reads order 101 again and executes the side effects again.

Because of this, consumers and downstream systems must be idempotent: processing the same event multiple times should not produce incorrect results (e.g., double charging). Idempotency strategies include:

* Use unique transaction or event IDs and deduplicate based on that ID.
* Implement idempotent APIs or business logic (e.g., mark an order as processed).
* Use Kafka’s idempotent producers and transactions to achieve stronger semantics (but these require additional configuration and careful design).

<Frame>
  <img alt="The image is a diagram illustrating an idempotent process involving two attempts at reading and processing orders, with labels such as &#x22;charge,&#x22; &#x22;send email,&#x22; and &#x22;commit.&#x22; It includes elements like &#x22;partition,&#x22; &#x22;consumer,&#x22; and highlights concepts of &#x22;at-least-once&#x22; processing and idempotency, with a consumer performing the same work again without additional damage." />
</Frame>

<Callout icon="warning">
  If your business cannot tolerate duplicates, design idempotent consumers or use Kafka’s stronger features (idempotent producers and transactions) to approach exactly-once semantics end-to-end. These features require additional configuration and careful design.
</Callout>

## Quick reference table

|            Concept | Purpose                                                        | Example / Command                                                 |
| -----------------: | -------------------------------------------------------------- | ----------------------------------------------------------------- |
|              Topic | Named stream of events                                         | `checkout-orders`                                                 |
|          Partition | Ordered subset of a topic for scale & parallelism              | `--partitions 3`                                                  |
|             Offset | Sequential position in a partition                             | Visible via `kafka-consumer-groups.sh --describe`                 |
|     Consumer group | Coordinates consumers so each partition is read once per group | `--group email-service`                                           |
|        Replication | Redundancy for availability & failover                         | `--replication-factor 2`                                          |
| Delivery semantics | Guarantees for message delivery                                | at-least-once (default); use transactions for stronger guarantees |

## Summary

* Kafka decouples producers from consumers and retains events for replay.
* Topics are split into partitions for scale and parallelism; ordering is guaranteed only within a partition.
* Consumer groups distribute partition consumption so each partition is read by one consumer instance in the group.
* Replication and leader election provide fault tolerance.
* Kafka defaults to at-least-once delivery; handle duplicates using idempotent consumers or adopt Kafka’s transactional features for stronger semantics.

## Links and references

* Apache Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Kafka consumer groups and offsets: [https://kafka.apache.org/documentation/#consumerconfigs](https://kafka.apache.org/documentation/#consumerconfigs)
* Confluent blog—Kafka design and guarantees: [https://www.confluent.io/blog/](https://www.confluent.io/blog/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/b171f2a5-552f-44a7-a82e-e1770f1f9b53/lesson/ac1e213a-2e49-4137-b33e-ddf50f9a1c7d" />
</CardGroup>


# How Does Terraform Actually Work

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Interview-Setup/How-Does-Terraform-Actually-Work/page

Explains how Terraform translates declarative HCL into infrastructure changes, using state, planning, providers, dependency graph, and remote state for collaboration and drift management.

This lesson explains what happens under the hood when you run Terraform and how it translates your declarative HCL configuration into real infrastructure changes.

Terraform is declarative: you describe the desired end state of your infrastructure using [HCL (the HashiCorp Configuration Language)](https://developer.hashicorp.com/hcl). Terraform figures out what to create, change, or delete to reach that target state.

For example, to request three Amazon EC2 instances and an Application Load Balancer, your configuration might look like this:

```hcl theme={null}
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
}

resource "aws_lb" "app_lb" {
  name               = "app-lb"
  internal           = false
  load_balancer_type = "application"
  subnets            = ["subnet-0123", "subnet-0456"]
}
```

When you run `terraform apply`, Terraform turns that desired state into the necessary cloud API calls to create or modify real resources so the live environment matches your configuration.

What about duplicate or repeated resources? In the example above, `count = 3` ensures Terraform will create three instances and manage them as a single logical resource block.

## How Terraform Knows What Currently Exists

Terraform tracks resources it manages using a state file (by default `terraform.tfstate`). This JSON file maps resource blocks from your configuration to actual cloud resource IDs and metadata. Example snippet from a state file:

```json theme={null}
{
  "resources": [
    {
      "type": "aws_instance",
      "name": "web",
      "instances": [
        {
          "attributes": {
            "id": "i-0abc123def456"
          }
        }
      ]
    }
  ]
}
```

When planning changes, Terraform compares three sources of truth:

| Source              | What it is            | Purpose                                 |
| ------------------- | --------------------- | --------------------------------------- |
| Configuration (HCL) | Your `.tf` files      | Desired end state                       |
| Saved state         | `terraform.tfstate`   | Last known mapping of managed resources |
| Live resources      | Queried via providers | Current reality in the cloud            |

## What `terraform plan` Does

`terraform plan` previews changes by comparing the configuration, the saved state, and the live resources. It reports what will be created, changed, or destroyed without making any modifications.

```bash theme={null}
