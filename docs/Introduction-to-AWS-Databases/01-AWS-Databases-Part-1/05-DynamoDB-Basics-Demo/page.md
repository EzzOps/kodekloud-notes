# DynamoDB Basics Demo

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/DynamoDB-Basics-Demo/page

Hands-on demo for creating, populating, querying, monitoring, and deleting an Amazon DynamoDB orders table using the AWS Console and PartiQL, covering capacity, indexes, and backups.

This hands-on guide demonstrates how to create and use an Amazon DynamoDB table from the AWS Management Console using a simple e-commerce example: storing customer orders. You will create a table, insert items, run queries, inspect monitoring, and finally delete the table to avoid charges.

Key concepts covered:

* Table creation and primary key design
* Capacity modes and auto scaling
* Adding and querying items (Console + PartiQL)
* Monitoring, backups/replication, and cleanup

## Step 1 — Create the table and choose a primary key

Open the DynamoDB service in the AWS Console and create a new table named `orders`. The most important design decision is choosing the primary key. This controls how efficiently you can retrieve items.

For this demo:

* Partition key: `customerId` (String) — use this to fetch all orders for a specific customer.
* Sort key: `orderId` (String) — ensures each order for a given customer is unique and enables range queries.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB &#x22;Create table&#x22; console. The form shows a table named &#x22;orders&#x22; with partition key &#x22;customerId&#x22; and optional sort key &#x22;orderId,&#x22; both set as strings." />
</Frame>

> **lightbulb** Primary key tips:

  * Use a single partition key when every item is unique (e.g., profile records).
  * Use a composite key (partition + sort) when multiple related items share the same partition (e.g., orders for a customer).
  * Design keys based on access patterns — table design is driven by how you will query the data.

## Capacity mode, table class, and advanced options

You can accept defaults or click Customize to review:

* Table class: `Standard` or `Standard-Infrequent Access` (for less frequently accessed data).
* Capacity mode: `On-demand` (pay-per-request) or `Provisioned` (pre-allocated RCUs/WCUs).
* Encryption at rest and deletion protection.

If you choose Provisioned capacity, you can enable auto scaling for read and/or write capacity. Auto scaling requires a minimum, maximum, and a target utilization percentage (commonly \~70%).

<Frame>
  <img alt="A screenshot of the AWS DynamoDB &#x22;Read/write capacity settings&#x22; console with Capacity mode set to Provisioned. Read auto-scaling is On (min 1, max 10, target 70%) and write auto-scaling is Off with provisioned write capacity 5." />
</Frame>

You can review estimated monthly cost and encryption settings before creating the table.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing &#x22;Estimated read/write capacity cost&#x22; (Total read and write capacity units: 5 each, estimated $2.91/month). Below it are &#x22;Encryption at rest&#x22; options (selected: Owned by Amazon DynamoDB) and a panel about deletion protection." />
</Frame>

Create the table. It will take a few seconds to become `Active`. Once active, open the table to inspect configuration and metrics.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the &#x22;orders&#x22; table overview. It displays general information (partition key customerId, sort key orderId), table status (Active), and items/metrics panels." />
</Frame>

The overview displays:

* Primary key schema (`customerId`, `orderId`)
* Table status (`Active`)
* Item count, table size, average item size
* Capacity metrics and summary information

## Indexes, monitoring, and replication

To support additional access patterns, create Global Secondary Indexes (GSIs) or Local Secondary Indexes (LSIs) from the Indexes tab.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console displaying the &#x22;orders&#x22; table on the Indexes tab. The Global secondary indexes section shows no indexes and offers a &#x22;Create index&#x22; option." />
</Frame>

Monitoring integrates with CloudWatch and shows graphs for reads/writes, throttling, latency, and alarms. The Monitor tab provides the live metrics you need to tune capacity or investigate performance.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the monitoring dashboard for a table named &#x22;orders,&#x22; with multiple graphs for read/write usage, throttled requests/events, and latency. The left sidebar shows DynamoDB menu options like Tables, Backups, and Exports to S3." />
</Frame>

Global table replicas appear under Global tables, and Exports & Streams offers backups, export-to-S3, and DynamoDB Streams / Kinesis integration.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console focused on an &#x22;orders&#x22; table with the Global tables tab open, showing &#x22;No replicas&#x22; and buttons to create or delete replicas. The left sidebar shows navigation items like Dashboard, Tables, Backups and DAX." />
</Frame>

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console open to the &#x22;orders&#x22; table on the Exports and streams tab, showing no exports and buttons for &#x22;Export to S3&#x22; and to turn on Kinesis/DynamoDB streams. The left sidebar shows DynamoDB navigation items like Tables, Backups, Exports/Imports, and the selected table &#x22;orders.&#x22;" />
</Frame>

## Step 2 — Insert sample items via the Console

Open Explore table items to run Scans or Queries and to inspect item data. For production use prefer the AWS SDK or AWS CLI, but the Console is useful for quick tests.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the &#x22;orders&#x22; table in the Explore items view with a Scan selected and no items returned. A green banner notes the scan completed and consumed 0.5 read capacity units." />
</Frame>

Click Create item and provide values for the partition and sort keys. Make sure numeric attributes are typed as Number and booleans as Boolean in the Console.

Example items for this demo (JSON representation):

```json theme={null}
[
  {
    "customerId": "CUST-1",
    "orderId": "ORDER-10",
    "price": 100,
    "delivered": true
  },
  {
    "customerId": "CUST-1",
    "orderId": "ORDER-20",
    "price": 50,
    "delivered": true
  },
  {
    "customerId": "CUST-2",
    "orderId": "ORDER-3",
    "price": 35,
    "delivered": false
  }
]
```

<Frame>
  <img alt="The image shows the AWS DynamoDB &#x22;Create item&#x22; form for an orders table with fields like customerId &#x22;CUST-1&#x22;, orderId &#x22;ORDER-10&#x22;, price &#x22;100&#x22;, and a delivered boolean set to True. Buttons to add/remove attributes and a &#x22;Create item&#x22; button are also visible." />
</Frame>

After creating items, use Query operations to fetch items efficiently. Queries require the partition key value. For example, to retrieve all orders for `CUST-1` use:

* `customerId = "CUST-1"`

Queries can also use a `KeyConditionExpression` on the sort key (e.g., range queries on `orderId`) or a `FilterExpression` for non-key attributes (e.g., `price > 60`). Important: filter expressions are applied after the read and do not reduce the read capacity units consumed by the underlying query.

Example (Console):

* Query partition key `customerId = "CUST-1"`
* Add FilterExpression: `price > 60`
  Result: both items for `CUST-1` are read, but only the item with `price = 100` is returned.

You can edit items (Edit item → Save) or delete items (select → Delete item) directly from the Console.

## PartiQL: a SQL-like option

DynamoDB supports PartiQL — a SQL-compatible language that maps to DynamoDB operations. PartiQL is useful for users familiar with SQL, but the same DynamoDB access patterns and limits still apply.

<Frame>
  <img alt="The screenshot shows the AWS DynamoDB console open to the PartiQL editor, with a left navigation pane and a blank query editor. The Tables panel lists a table named &#x22;orders&#x22; and the query area shows no results." />
</Frame>

Useful PartiQL examples:

* Select all orders for a customer:
  * `SELECT * FROM "orders" WHERE "customerId" = 'CUST-1'`
* Filter by price (note: this still maps to DynamoDB reads/filters):
  * `SELECT * FROM "orders" WHERE "customerId" = 'CUST-1' AND "price" > 60`

## Step 3 — Monitor, then delete the table

After running reads/writes, check the Monitor tab to view actual read/write metrics, throttles, and latency trends.

When you finish the demo, delete the table to avoid ongoing charges:

* Select the table → Delete → confirm.

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the &#x22;orders&#x22; table in the table list with status &#x22;Deleting&#x22; and a green banner confirming the delete request was submitted successfully." />
</Frame>

> **warning** Deleting a table is irreversible and removes all data. Consider enabling deletion protection or creating a backup if you need to retain data before deletion.

## Quick reference table

| Topic                  |                                                                                       Recommendation | Example                                                               |
| ---------------------- | ---------------------------------------------------------------------------------------------------: | --------------------------------------------------------------------- |
| Primary key            |                                                                              Match to access pattern | `customerId` (PK), `orderId` (SK)                                     |
| Read vs Write capacity | Use On-demand for unpredictable traffic; Provisioned + auto scaling for stable predictable workloads | `On-demand` or `Provisioned` with scaling (min 1, max 10, target 70%) |
| Query vs Scan          |                        Prefer `Query` for specific partition key reads; avoid `Scan` on large tables | `Query WHERE customerId = 'CUST-1'`                                   |
| Indexes                |                                                  Use GSIs/LSIs to support additional access patterns | Create a GSI for queries by `orderDate`                               |
| Backup & restore       |                                       Use on-demand backups or point-in-time recovery for protection | Export to S3 or enable PITR                                           |
| SQL-like queries       |                                                                      Use PartiQL for familiar syntax | `SELECT * FROM "orders"`                                              |

## Additional resources

* DynamoDB Developer Guide: [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)
* PartiQL reference: [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html)
* AWS CLI: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)
* AWS SDKs & Tools: [https://aws.amazon.com/tools/](https://aws.amazon.com/tools/)
* CloudWatch: [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)
* S3 (export target): [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Kinesis: [https://aws.amazon.com/kinesis/](https://aws.amazon.com/kinesis/)

> **lightbulb** Key takeaways:

  * Choose a primary key that matches your read/write access patterns (partition key for customer queries; add a sort key for multiple items per customer).
  * Prefer Query over Scan to reduce costs and improve performance.
  * Choose capacity mode based on traffic predictability; use Provisioned mode with auto scaling for predictable workloads.
  * PartiQL offers SQL-like convenience but maps to the same DynamoDB operations and limits.

That concludes this step-by-step DynamoDB Console demo.

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/577d791f-026e-4eed-8a1e-26fb1d66a35b)
