# AWS DynamoDB

Source: https://notes.kodekloud.com/docs/AWS-For-Beginners-with-Hands-On-Labs/AWS-Essentials-Part-2/AWS-DynamoDB/page

Hands-on tutorial for creating and managing an AWS DynamoDB orders table covering keys, capacity, items, queries, monitoring, and cleanup.

In this lesson we'll walk through a hands-on demo of creating and using a DynamoDB table to store orders for an e‑commerce website. The walkthrough covers table creation, key selection, capacity settings, adding and editing items via the console, efficient queries, and monitoring.

What you'll do:

* Create a table named `orders`.
* Choose partition and sort keys to support query patterns.
* Configure capacity and encryption.
* Add, query, filter, edit, and delete items.
* Review monitoring, indexes and other table options.

## 1. Create the table and choose keys

Open the AWS Console and search for the DynamoDB service. Create a new table named `orders`. The partition key and optional sort key determine how you access and organize items. Choosing the right keys is critical because Query operations require an equality on the partition key and are far more efficient than Scan.

Recommended keys for this demo:

* Partition key: `customerId` (String) — so you can efficiently fetch all orders for a customer.
* Sort key: `orderId` (String) — to uniquely identify each order for a given customer and enable range queries on order attributes.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB &#x22;Create table&#x22; console showing form fields to create a table named &#x22;orders&#x22;. The partition key is set to customerId (String) and the optional sort key is orderId (String), with default table settings selected." />
</Frame>

> **lightbulb** Table design in DynamoDB is an advanced topic—consider access patterns, single-table design, and secondary indexes for real applications. For exams and practical tasks, focus on understanding partition keys, sort keys, and when to use Query vs Scan.

## 2. Table class and capacity mode

Choose a table class and capacity mode that match your workload:

* Table class: Standard (general purpose) or Standard‑IA (infrequent access).
* Capacity mode: On‑Demand (pay-per-request) or Provisioned (set read/write capacity units).

Example Provisioned configuration used in this demo: read auto-scaling enabled (min 1, max 10, target 70%), write auto-scaling off with 5 provisioned write capacity units.

<Frame>
  <img alt="Screenshot of the AWS DynamoDB &#x22;Read/write capacity settings&#x22; page. It shows Provisioned capacity selected, read auto-scaling enabled (min 1, max 10, target 70%) and write auto-scaling off with 5 provisioned write capacity units." />
</Frame>

Quick reference — capacity terms:

|                     Setting | Purpose                                  | When to use                           |
| --------------------------: | ---------------------------------------- | ------------------------------------- |
|                   On‑Demand | Pay-per-request pricing                  | Unpredictable or spiky traffic        |
| Provisioned w/ Auto Scaling | Set min/max, target utilization          | Predictable traffic with cost control |
|                 Standard‑IA | Lower-cost storage for infrequent access | Archival or rarely read data          |

A few important notes:

* Auto Scaling adjusts provisioned throughput between the minimum and maximum you set.
* Target utilization (commonly \~70%) is the utilization level Auto Scaling tries to maintain.
* GSIs and LSIs may introduce additional capacity considerations.

You can also configure encryption (AWS-owned CMK by default, AWS managed CMK, or a customer-managed KMS key), enable deletion protection, and review estimated monthly costs before creating the table.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console's Create Table settings showing estimated read/write capacity cost, encryption-at-rest key management options, and deletion protection information. The page shows region us-east-1 and an estimated cost of $2.91/month." />
</Frame>

## 3. Table overview and status

After creating the table, wait for its status to become Active. The table overview displays keys, capacity mode, item count, and size.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console for an &#x22;orders&#x22; table. It shows general table information (partition/sort keys, capacity mode, status), an items summary, and table capacity metrics with the left navigation menu visible." />
</Frame>

Indexes, monitoring, backups, replication, streams, and exports are available in the table tabs. The Indexes tab lists any GSIs/LSIs you create.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console on the &#x22;orders&#x22; table Indexes tab, showing no global secondary indexes and a &#x22;Create index&#x22; button. The left sidebar displays DynamoDB navigation items like Dashboard, Tables, Backups and settings." />
</Frame>

The Monitor tab exposes CloudWatch metrics (read/write usage, throttling, latency) and provides configuration for alarms, backups (point-in-time recovery), global tables/replicas, streams, and exports.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the monitoring dashboard for a table named &#x22;orders,&#x22; with charts for read/write usage, throttled requests/events, and latency. The left sidebar shows DynamoDB navigation options (Dashboard, Tables, Update settings) and DAX sections." />
</Frame>

## 4. Add items (console)

Open Explore items in the console to view or add items. A freshly created table starts empty.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the &#x22;orders&#x22; table in the Explore items view with a Scan selected. The scan completed (0.5 read units) and returned no items." />
</Frame>

Example items added in this demo:

| customerId | orderId  | price (Number) | delivered (Boolean) |
| ---------: | -------- | -------------: | ------------------: |
|     CUST-1 | ORDER-10 |            100 |               False |
|     CUST-1 | ORDER-20 |             50 |                True |
|     CUST-2 | ORDER-30 |             35 |               False |

Create an item by supplying partition and sort keys and any additional attributes.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB &#x22;Create item&#x22; console showing a form for an order. The attributes shown are customerId: CUST-2, orderId: ORDER-30, price: 35 and delivered set to False." />
</Frame>

After inserting these records, a Scan returns all items in the table:

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing a scan of the &#x22;orders&#x22; table, with three returned items listing customerId, orderId, delivered status, and price. The results panel shows entries like CUST-2/ORDER-30 and CUST-1/ORDER-20 with prices and delivery flags." />
</Frame>

## 5. Prefer Query over Scan

Use Query whenever possible—it's much more efficient because it retrieves items by partition key rather than scanning the whole table. Query requires an equality condition on the partition key; you can combine it with sort key conditions (range queries) and FilterExpressions for further narrowing.

> **lightbulb** Query operations require an equality on the partition key. Filter expressions are applied after the query and do not reduce the read capacity units consumed by the initial query—they only narrow the results returned to you.

Example: Query all orders for `CUST-1` returns both orders for that customer. To return only orders with `price > 60`, add a FilterExpression—note the filter runs after DynamoDB reads the partition's items, so read units are still consumed for the items that matched the partition key.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the &#x22;Explore items&#x22; view for the &#x22;orders&#x22; table with customerId set to CUST-1 and a filter for price > 60. The query returned one item (orderId ORDER-10) marked delivered with price 100." />
</Frame>

## 6. Edit and delete items

You can edit attributes for an item from the console (for example update `price` or `delivered` status). Use Edit item to change values and Save to apply changes.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB &#x22;Edit item&#x22; form showing an order record with attributes: customerId = CUST-1, orderId = ORDER-10, delivered = False, and price = 100. UI controls like Cancel, Save, and Save and close are visible." />
</Frame>

To remove an item, select it and choose Delete item(s), then confirm the deletion.

## 7. PartiQL and programmatic access

DynamoDB supports PartiQL, a SQL-compatible language that lets you run familiar INSERT/SELECT/UPDATE/DELETE statements against DynamoDB tables. PartiQL statements are translated into native DynamoDB operations. For automation and production use, prefer the AWS CLI or SDKs.

* PartiQL reference: [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html)

## 8. Summary and cleanup

This demo covered:

* Creating an `orders` table with partition key `customerId` and sort key `orderId`.
* Choosing table class and capacity (On‑Demand vs Provisioned with Auto Scaling).
* Configuring encryption and deletion protection.
* Adding items, using Query vs Scan, applying FilterExpressions.
* Editing and deleting items and viewing monitoring metrics.

When you finish the demo, delete the table from the console to avoid ongoing costs. If you want to prevent accidental removal, enable deletion protection while the table exists.

## Links and references

* [DynamoDB Developer Guide — PartiQL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html)
* [AWS CloudWatch documentation](https://learn.kodekloud.com/user/courses/aws-cloudwatch)
* [Amazon DynamoDB documentation](https://docs.aws.amazon.com/dynamodb/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/68a80d2a-9ede-43f1-a18e-84e7efe89dc6/lesson/8828129b-e9f5-4144-a41d-a68583f4eba8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/68a80d2a-9ede-43f1-a18e-84e7efe89dc6/lesson/93b75e86-63f1-498f-a025-f5ce814a2234)
