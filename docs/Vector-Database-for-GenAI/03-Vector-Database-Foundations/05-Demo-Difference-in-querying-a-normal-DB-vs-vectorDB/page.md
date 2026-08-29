# Demo Difference in querying a normal DB vs vectorDB

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Foundations/Demo-Difference-in-querying-a-normal-DB-vs-vectorDB/page

Demo comparing PostgreSQL relational queries and LanceDB vector semantic search using a Node.js app to illustrate differences and hybrid architecture

Welcome back.

In this lesson we compare querying the same dataset using a traditional relational database (PostgreSQL) and a vector database (LanceDB). The repository for this demo contains:

* a small Node.js application,
* a Docker Compose setup that launches PostgreSQL and the app, and
* code that loads a CSV of support-ticket data into both backends so you can compare queries side-by-side.

Prerequisites

* Docker and Docker Compose installed
* A machine with internet access (the build will pull container images)

Start the application
First, stop and remove any previous Docker artifacts for this lab, rebuild without cache, and bring the stack up:

```bash theme={null}
docker compose down -v --rmi local --remove-orphans
docker compose build --no-cache
docker compose up
```

Note: the build/pull step can take a couple minutes depending on network speed.

When startup completes you should see PostgreSQL initialize and the application log indicating the server is running, for example:

```plaintext theme={null}
PostgreSQL init process complete; ready for start up.
2026-03-21 08:49:46.715 UTC [1] LOG:  starting PostgreSQL 16.13...
2026-03-21 08:49:46.726 UTC [1] LOG:  database system is ready to accept connections
server running on http://localhost:3000
```

Open the app at `http://localhost:3000` in your browser.

Project overview
This demo is a simple Node.js application that accepts a CSV of support tickets and loads the rows into:

* PostgreSQL (tabular storage)
* LanceDB (vector storage; stores embeddings/vectors representing text content)

Relevant dependencies from `package.json`:

```json theme={null}
{
  "name": "sql-vs-vector-demo",
  "version": "1.0.0",
  "description": "Classroom demo for SQL query vs vector search",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "@lancedb/lancedb": "^0.18.2",
    "csv-parse": "^5.5.6",
    "express": "^4.21.2",
    "multer": "^1.4.5-lts.2",
    "pg": "^8.13.1"
  }
}
```

Load the CSV

1. Click "Choose CSV File" in the web UI and select the provided support-tickets CSV.
2. Preview the CSV to inspect fields such as `title`, `body`, `category`, `priority`, `status`, `resolution`, `language`, `created_on`, and `tags`.
3. Click the button to load the file into Postgres and LanceDB. The app will:
   * Insert rows into a Postgres `documents` table.
   * Create embeddings (vectors) from the text and store them in LanceDB along with metadata (`id`, `title`, `category`, etc.).

How the data is stored

* PostgreSQL: rows are stored in a table with columns like `id`, `title`, `body`, `category`, `priority`, `status`, `created_at`, `resolution`, etc. This is a traditional tabular representation suitable for structured queries and analytics.
* LanceDB (vector DB): for each document the application stores:
  * an embedding vector (a numeric array representing semantic features of the text), and
  * accompanying metadata such as `id`, `title`, and `category`.
    The vector DB indexes those vectors to support fast similarity search. The "vector preview" shown in the UI is the embedding representation, not a relational row.

Querying examples — SQL vs neural search

1. Exact / keyword search with SQL\
   To find tickets mentioning a forgotten password or related issues, a typical SQL pattern-matching query:

```sql theme={null}
SELECT id, title, priority, status, resolution
FROM documents
WHERE title ILIKE '%password%'
   OR body ILIKE '%password%'
ORDER BY id;
```

This returns rows containing the literal substring "password" in the `title` or `body`.

2. Natural-language / semantic search with a vector DB\
   With a vector DB you issue a natural-language query and retrieve documents ranked by similarity to that query. For example:

```text theme={null}
I am locked out and my sign-in code never arrives
```

The vector search returns documents semantically similar to the query, even if they do not contain literal words like "password" or "sign-in code". Results are ordered by a similarity score (distance or similarity metric), so you may see relevant tickets with different phrasing — and occasionally some noise (irrelevant matches that share semantic features).

3. Aggregation and analytics — SQL\
   For counts, groupings, and analytics, SQL provides powerful aggregation functions. Example: tickets per category:

```sql theme={null}
SELECT category, COUNT(*) AS total
FROM documents
GROUP BY category
ORDER BY total DESC;
```

This is ideal for dashboards, reporting, and any structured analytics work.

Comparison: when to use each

|                         Capability |               PostgreSQL (relational)               |                          LanceDB (vector DB)                         |
| ---------------------------------: | :-------------------------------------------------: | :------------------------------------------------------------------: |
|               Exact keyword search |        Excellent (SQL WHERE / ILIKE / regex)        |         Possible only via metadata or additional text fields         |
| Semantic / natural-language search |   Limited — requires synonyms, additional tooling   |           Excellent — built for embedding similarity search          |
|         Aggregations and analytics |           Native (GROUP BY, COUNT, JOINs)           |                 Not designed for complex aggregations                |
|            Transactional integrity |                    Strong (ACID)                    |              Not a replacement for transactional storage             |
|                           Best for | Reporting, structured retrieval, transactional data | Retrieval for conversational agents, semantic search, fuzzy matching |

Example: why results differ

* SQL returns exact or pattern-based matches as defined by your WHERE clause — deterministic and precise.
* Vector DB returns semantically similar results based on embedding similarity — fuzzy, ranked, and great for conversational or ambiguous queries.

Why vector DBs are not a substitute for analytics
Vector databases excel at semantic search and powering conversational/generative workflows (e.g., retrieval-augmented generation, chat with data). They are not optimized for traditional relational aggregations such as `GROUP BY`, counts, joins, or strict transactional consistency. For analytics, reporting, and structured queries, a relational database like PostgreSQL remains the appropriate tool.

> **lightbulb** Use PostgreSQL (or another relational DB) for structured storage, deterministic filters, aggregations, and transactional integrity. Use a vector DB (LanceDB in this demo) for semantic search, similarity matching, and conversational retrieval. Many real-world systems combine both: vectors for retrieval and relational DB for storage, metadata, and analytics.

Practical architecture patterns

* Hybrid approach (recommended): store full records and metadata in PostgreSQL for durability, aggregation, and joins; store embeddings in LanceDB and use the vector DB to retrieve candidate documents by semantic relevance. Then enrich or filter those candidates using SQL queries on metadata.
* Common pipeline:
  1. Ingest raw document into PostgreSQL (store source text & metadata).
  2. Compute embedding for text and insert into LanceDB with the same `id` and metadata.
  3. For queries, run a semantic search on LanceDB → get top-N candidate ids → fetch full records from PostgreSQL for display or further filtering.

Summary

* Both systems can store and surface the same underlying documents, but they index and retrieve them differently.
* SQL queries are explicit, precise, and ideal for analytics and structured retrieval.
* Vector search accepts natural-language queries and returns semantically similar content ranked by score — excellent for search and conversational retrieval, but not for structured aggregations.
* A hybrid approach (use both) is common in production: vector DB for retrieval, relational DB for analytics and persistence.

Links and references

* LanceDB: [https://github.com/lancedb/lancedb](https://github.com/lancedb/lancedb)
* PostgreSQL Documentation: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
* Retrieval-Augmented Generation (RAG) overview: [https://learn.kodekloud.com/user/courses/fundamentals-of-rag](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)

That concludes this lesson. Thanks for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/82014ec3-9709-44d1-bd41-577af87083ed/lesson/008d1058-2dbc-4983-aed6-82efbb2320fa)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/82014ec3-9709-44d1-bd41-577af87083ed/lesson/e98154fa-93b2-4ace-ac1d-c6f518e03bac)
