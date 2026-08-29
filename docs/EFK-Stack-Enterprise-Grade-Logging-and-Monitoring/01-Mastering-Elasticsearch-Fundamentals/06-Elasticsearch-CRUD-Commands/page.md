# Elasticsearch CRUD Commands

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Mastering-Elasticsearch-Fundamentals/Elasticsearch-CRUD-Commands/page

This article provides a guide on Elasticsearch CRUD commands for creating, updating, retrieving, and deleting indices and documents using Kibana’s DevTools interface.

Welcome to this comprehensive lesson on Elasticsearch CRUD commands. In this guide, we demonstrate how to create, update, retrieve, and delete indices and documents through Kibana’s DevTools interface. Follow the sections below to learn how to interact with Elasticsearch using various commands.

The Kibana UI provides an intuitive editor where you can send requests to Elasticsearch. The left pane is for entering commands, while the right pane displays the corresponding output. Let’s dive in.

***

## Searching All Documents

To retrieve all documents from Elasticsearch, run the following command:

```http theme={null}
GET _search
{
  "query": {
    "match_all": {}
  }
}
```

***

## Checking Cluster Health

Before executing any modifications, it is advisable to verify the health of your Elasticsearch cluster. Run this GET request to check the cluster's status:

```http theme={null}
GET /_cluster/health
```

A successful response (HTTP status 200) returns details similar to the example below:

```json theme={null}
{
  "cluster_name": "elasticsearch",
  "status": "yellow",
  "timed_out": false,
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "active_primary_shards": 10,
  "active_shards": 10,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 2,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 83.33333333333334
}
```

<Callout icon="lightbulb">
  The response status will typically be yellow or green. A red status indicates critical issues that require immediate attention.
</Callout>

***

## Creating an Index

To create a new index named "products", execute the following PUT command:

```http theme={null}
PUT /products
```

On successful execution, you will receive an acknowledgement confirming the creation of the "products" index.

***

## Adding a Document

Insert a new document into the "products" index using the POST command. The example below adds a product document with multiple properties:

```http theme={null}
POST /products/_doc/1
{
  "product_id": 67890,
  "name": "Cozy Winter Sweater",
  "description": "Soft and stylish sweater for cold days",
  "price": 59.99,
  "category": "Apparel",
  "brand": "Trendy Threads"
}
```

<Callout icon="lightbulb">
  Before running any command, make sure to highlight the relevant section in the editor and then click on "Run" in Kibana.
</Callout>

***

## Retrieving the Document

To confirm that the document has been added, retrieve it with the following GET command:

```http theme={null}
GET /products/_doc/1
```

You can also search for the document by matching specific fields. For example, to find a product with "sweater" in its name, use:

```http theme={null}
GET /products/_search
{
  "query": {
    "match": {
      "name": "sweater"
    }
  }
}
```

In the response, note that the document data is stored under the "\_source" key, while other keys hold metadata.

***

## Updating a Document

### Incorrect Approach Using PUT

Attempting to update a document using the PUT command may result in issues, as it replaces the entire document rather than updating specific fields. For example:

```http theme={null}
PUT /products/_doc/1
{
  "price": 129.99
}
```

This approach can trigger a parsing exception (HTTP status 400) if not formatted correctly.

### Correct Approach Using POST with \_update

To modify only specific fields without replacing the entire document, use the POST command with the \_update endpoint. First, ensure your document exists:

```http theme={null}
POST /products/_doc/1
{
  "product_id": 67890,
  "name": "Cozy Winter Sweater",
  "description": "Soft and stylish sweater for cold days",
  "price": 59.99,
  "category": "Apparel",
  "brand": "Trendy Threads"
}
```

Now, update specific fields using:

```http theme={null}
POST /products/_doc/1/_update
{
  "doc": {
    "description": "Soft and stylish sweater for cold days. Available in multiple colors.",
    "category": "Apparel - Seasonal"
  }
}
```

After executing this update command, verify the changes by retrieving the document again:

```http theme={null}
GET /products/_doc/1
```

<Callout icon="lightbulb">
  Using PUT replaces the whole document, whereas using POST with \_update only modifies the designated fields.
</Callout>

***

## Deleting Documents and Indices

To delete a single document from the index:

```http theme={null}
DELETE /products/_doc/1
```

If you prefer to delete the entire index, execute:

```http theme={null}
DELETE /products/
```

***

## Summary of Commands

Below is a consolidated list of essential Elasticsearch CRUD commands covered in this lesson:

```http theme={null}
GET _search
{
  "query": {
    "match_all": {}
  }
}

GET /_cluster/health

PUT /products

POST /products/_doc/1
{
  "product_id": 67890,
  "name": "Cozy Winter Sweater",
  "description": "Soft and stylish sweater for cold days",
  "price": 59.99,
  "category": "Apparel",
  "brand": "Trendy Threads"
}

GET /products/_doc/1

GET /products/_search
{
  "query": {
    "match": {
      "name": "sweater"
    }
  }
}

POST /products/_doc/1/_update
{
  "doc": {
    "description": "Soft and stylish sweater for cold days. Available in multiple colors.",
    "category": "Apparel - Seasonal"
  }
}

DELETE /products/_doc/1

DELETE /products/
```

***

## Final Thoughts

Mastering these Elasticsearch CRUD commands is essential for effective data management and troubleshooting in your Elasticsearch environment. Experiment with these commands in Kibana’s DevTools to enhance your understanding and ensure smooth operations.

Happy querying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/a70164d0-faba-407d-a6e8-4e227044c3aa/lesson/be59507e-6707-4b30-8adc-07558904d84a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/a70164d0-faba-407d-a6e8-4e227044c3aa/lesson/3f944181-6327-497f-bc2b-03293f96f94e" />
</CardGroup>
