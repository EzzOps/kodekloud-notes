# BigQuery Data Structures Datasets Tables Views

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Data-Structures-Datasets-Tables-Views/page

Explains BigQuery data structures and best practices for organizing datasets, tables, views and materialized views, including access control, partitioning, clustering, and DDL examples.

Hello and welcome back.

In this lesson we explain how BigQuery organizes data so you can design secure, performant datasets and queries. We previously reviewed BigQuery's internal architecture; now we’ll focus on the data structures you interact with daily: datasets, tables, views, and materialized views. To make the concepts concrete, we’ll use a global petroleum company example.

## BigQuery hierarchy (at-a-glance)

* Project (top-level; not shown in this lesson)
* Dataset — logical container for related tables and views
* Table — the object that physically stores rows and columns of data
* Views and materialized views — saved queries that present or cache derived results

Example: the petroleum company operates in regions (USA, Middle East, Africa, Asia). Use datasets like `us_operations`, `asia_supply_chain`, or `retail_sales` to group related tables such as `oil_production`, `well_maintenance`, or `equipment_inventory`. Use consistent naming (underscores rather than special characters) to simplify management and automation.

## What is a dataset?

A dataset is a logical container that groups related tables and views. Key dataset features:

* Logical grouping of related tables and views (for example, all refinery or retail data).
* IAM-based access control to grant teams selective access (e.g., give Finance access to pricing tables but not to drilling telemetry).
* Location-aware: a dataset is created in a specific region — choose the region that meets your compliance and performance needs.
* Labeling and tagging to support governance and cataloging (e.g., integration with Data Catalog).

<Frame>
  <img alt="An infographic titled &#x22;Dataset Features&#x22; with four numbered panels: Logical Container, Access Control, Location-Aware, and Organization & Labeling. Each panel has an icon and a short description about organizing tables, IAM permissions, regional creation, and logical grouping of data." />
</Frame>

## What is a table?

Tables are the primary storage objects in BigQuery. Think of a table as a spreadsheet: rows of data with named columns. Important table capabilities:

* Partitioning (e.g., by date) and clustering (e.g., by `site_id`) to reduce scanned data and speed up queries.
* Schema: defines field names and types; can be declared or auto-detected on load.
* Storage types:
  * Native tables — stored in BigQuery storage.
  * External tables — reference data in Cloud Storage, Google Drive, Bigtable, or external systems.
  * Materialized views — cached query results stored for faster repeated reads.
* Lifecycle management: table-level expiration for temporary data; when both dataset and table expirations exist, the table expiration takes precedence.

<Frame>
  <img alt="The image is a slide titled &#x22;Table Features&#x22; showing four numbered blue info cards that summarize features: Primary Storage, Schema Definition, Storage Types, and Lifecycle Management. Each card has an icon and a short description about how tables store data, define schemas, support different storage types, and handle expiration/versioning." />
</Frame>

## Quick reference table

| BigQuery object   | Purpose                                         | Typical examples / notes                             |
| ----------------- | ----------------------------------------------- | ---------------------------------------------------- |
| Dataset           | Logical container + IAM boundary                | `us_operations`, `asia_supply_chain`                 |
| Table             | Stores the actual data (rows/columns)           | `oil_production`, `equipment_inventory`              |
| View              | Virtual table that stores SQL only              | `daily_production_summary` (evaluates at query time) |
| Materialized View | Cached/precomputed results for repeated queries | `mv_daily_production` (refreshes automatically)      |

## DDL examples

Create a dataset (bq CLI):

```bash theme={null}
