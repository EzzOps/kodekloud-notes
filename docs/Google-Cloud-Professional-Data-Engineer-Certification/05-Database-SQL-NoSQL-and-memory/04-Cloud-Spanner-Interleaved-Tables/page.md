# Cloud Spanner Interleaved Tables

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Cloud-Spanner-Interleaved-Tables/page

Cloud Spanner interleaved tables co-locate parent and child rows to reduce disk seeks and speed parent-child queries, with primary key prefix requirement and cascade delete behavior.

Welcome back. This lesson explains Cloud Spanner interleaved tables — a powerful physical schema pattern that improves performance for tightly related parent-child data by co-locating rows on disk.

## What are interleaved tables?

* Interleaved tables physically co-locate parent and child rows in Cloud Spanner so related rows are stored next to each other on disk.
* This row locality reduces disk seeks and improves latency and throughput for queries that fetch a parent with its children together.
* In a typical relational layout (for example, `CUSTOMER` and `ORDERS` linked by `CustomerId`), rows might be stored far apart, requiring multiple seeks. With interleaving, each customer row is stored adjacent to its order rows, often enabling a single disk seek for parent + children retrieval.

## When to use interleaved tables

* Use interleaved tables when child rows are logically dependent on the parent and are rarely queried independently.
* Common scenarios include user profiles with recent activity, account pages with purchase history, audit logs grouped by entity, and other parent-centric read patterns.
* Avoid interleaving when child rows require frequent independent access, independent scaling/distribution, or when the child’s lifecycle is decoupled from the parent.

<Callout icon="warning">
  Be careful: interleaving enforces a primary key dependency and cascade deletes. If your application deletes parents frequently or requires independent child retention, interleaving may not be appropriate.
</Callout>

## Important technical notes

* A child table’s primary key must include the parent’s primary key as a prefix — this ordering drives physical colocation in Spanner.
* Deleting a parent automatically deletes its interleaved child rows (`ON DELETE CASCADE`).
* Interleaving changes only the physical storage layout, not the logical relational model.

<Frame>
  <img alt="An infographic titled &#x22;Parent-Child Data Co-location for Optimal Performance&#x22; that compares traditional separate CUSTOMER and ORDERS tables (left) with interleaved tables (right) where each customer row is stored together with its order rows to optimize disk seeks and query speed." />
</Frame>

## Example DDL

A common pattern is to create `Orders` interleaved under `Customers` so that orders are colocated with each customer:

```sql theme={null}
CREATE TABLE Customers (
  CustomerId   INT64 NOT NULL,
  Name         STRING(1024),
  Email        STRING(1024)
) PRIMARY KEY (CustomerId);

CREATE TABLE Orders (
  CustomerId   INT64 NOT NULL,
  OrderId      INT64 NOT NULL,
  OrderDate    TIMESTAMP NOT NULL,
  Amount       FLOAT64
) PRIMARY KEY (CustomerId, OrderId),
  INTERLEAVE IN PARENT Customers ON DELETE CASCADE;
```

* `Orders` uses `(CustomerId, OrderId)` as the primary key so Spanner colocates orders under the corresponding customer.
* `ON DELETE CASCADE` removes interleaved children automatically when the parent is deleted.

<Callout icon="lightbulb">
  Use interleaved tables when the child rows are tightly bound to the parent and you typically read or delete them together. Interleaving improves locality and read performance but implies cascade deletes and a primary key dependency.
</Callout>

## Real-world example

A retail mobile app that displays a user’s account page and recent purchases is a classic fit. When the account screen loads, the app typically queries the user (parent) and recent orders (children). Interleaving makes this read pattern more efficient because related rows are stored together.

## When to avoid interleaving — quick checklist

| Scenario                                                                    | Recommendation        |
| --------------------------------------------------------------------------- | --------------------- |
| Child rows frequently accessed independently of the parent                  | Avoid interleaving    |
| Child lifecycle differs from parent (e.g., retention independent of parent) | Avoid interleaving    |
| Parent and child require different scaling/sharding strategies              | Avoid interleaving    |
| Parent-centric read patterns where children are usually read with parent    | Consider interleaving |

## Summary

Cloud Spanner interleaved tables co-locate related parent and child rows to reduce disk I/O and speed up parent-child queries. They are most effective when children are dependent on the parent and usually accessed together. Keep in mind the primary-key prefix requirement and cascade-delete behavior when designing your schema.

## Links and references

* [Cloud Spanner: Schema design and interleaving](https://cloud.google.com/spanner/docs/schema-and-data-model#interleaved_tables)
* [Cloud Spanner Concepts](https://cloud.google.com/spanner/docs/concepts)

That’s it for this lesson — see you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/82f72dd7-a0bb-43f2-bf56-38343376b4b2" />
</CardGroup>
