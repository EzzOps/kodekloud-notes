# Performance Insights

Source: https://notes.kodekloud.com/docs/AWS-RDS/Monitoring-RDS-Database/Performance-Insights/page

Guide to using AWS RDS Performance Insights with Aurora PostgreSQL to populate a demo database, generate load, inspect top SQL and diagnose query performance

Welcome back.

In this lesson we'll explore how to use AWS RDS Performance Insights to diagnose database activity and improve query performance for Aurora PostgreSQL. We'll cover how to populate a demo database, where to find the key metrics in the console, and how to generate load so you can observe query-level activity in Performance Insights.

## Prepare the demo database

I created an Aurora PostgreSQL cluster with one writer instance and made it accessible from my network. I copied the username, password, and endpoint to a secure note so I can connect using the Query Editor or a client.

Open a new SQL script in the Query Editor (or use psql) and run the following statements in sequence: first run the CREATE TABLE statements, then run the INSERT statements. This will give you a simple Customers/Orders dataset to exercise queries.

```sql theme={null}
-- Create Customers table
CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    CustomerName VARCHAR(255),
    ContactName VARCHAR(255),
    Country VARCHAR(255),
    Email VARCHAR(255)
);

-- Create Orders table
CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    ProductName VARCHAR(255),
    Quantity INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Insert data into Customers
INSERT INTO Customers (CustomerName, ContactName, Country, Email) VALUES
('John Doe', 'John', 'USA', 'john.doe@example.com'),
('Jane Doe', 'Jane', 'UK', 'jane.doe@example.com'),
('Emily Smith', 'Emily', 'Canada', 'emily.smith@example.com');

-- Insert data into Orders
INSERT INTO Orders (CustomerID, OrderDate, ProductName, Quantity) VALUES
(1, '2023-08-01', 'Laptop', 2),
(1, '2023-08-10', 'Smartphone', 1),
(2, '2023-07-22', 'TV', 1),
(3, '2023-08-15', 'Camera', 2);
```

Run the statements in the order shown (CREATE TABLEs first, then INSERTs). After the script completes you'll have basic data to generate test queries and observe Performance Insights.

## Performance Insights overview

Performance Insights gives a dimensional view of database load at the SQL level. It surfaces top SQL by load, execution time, and average active sessions (AAS), and it shows which users, hosts, or applications are issuing those queries. Performance Insights must be enabled for your DB instance (either at creation or enabled later). Note that enabling Performance Insights can affect costs depending on retention and usage.

> **warning** Before continuing: ensure Performance Insights is enabled for your instance and review pricing/retention options. See the AWS docs for details on enabling Performance Insights and storage costs.

When you open your DB instance in the AWS Management Console and select Monitoring, you'll see standard RDS/CloudWatch metrics like CPUUtilization and DatabaseConnections. When Performance Insights is enabled, additional dimensional metrics (for example DBLoad, top SQL, and breakdowns by user/host) become available and provide deeper visibility into query-level activity.

<Frame>
  <img alt="A monitoring dashboard (AWS-style) showing multiple performance graphs for a database, including BufferCacheHitRatio, CommitLatency, CommitThroughput, CPUUtilization, DatabaseConnections and DBLoad. The charts display time-series lines and a tooltip showing connection counts for two instances." />
</Frame>

In the console you can inspect connection counts and CPU utilization at the instance level. To get detailed, dimensional information (top SQL, execution time, sessions, top users, application names, etc.) open Performance Insights for the selected database instance.

Performance Insights displays:

* Top SQL statements by load (AAS).
* SQL text and execution samples.
* Which database user, host, or application issued the query.
* A timeline of DBLoad so you can correlate spikes with specific queries or clients.

<Frame>
  <img alt="A screenshot of AWS RDS Performance Insights for an Aurora PostgreSQL instance, showing a database load graph with bar markers and a tooltip detailing SELECT queries. The lower panel shows &#x22;Top users&#x22; with the postgres user listed and a small AAS load." />
</Frame>

### Quick reference — what to look for in Performance Insights

| Metric / View                       | Purpose                               | How it helps                                   |
| ----------------------------------- | ------------------------------------- | ---------------------------------------------- |
| DBLoad (AAS)                        | Active sessions over time             | Identify periods of contention and heavy load  |
| Top SQL                             | Statements contributing most load     | Finds expensive queries to optimize            |
| Top users / hosts / apps            | Source of load                        | Pinpoint clients or services causing issues    |
| SQL text & samples                  | Full query text and execution details | Use for rewriting queries or adding indexes    |
| Standard metrics (CPU, connections) | Instance-level health                 | Correlate resource utilization with query load |

## Generate load to observe query activity

To demonstrate Performance Insights capturing query activity, generate concurrent load that mixes simple point selects and heavier aggregation queries. The Python script below creates multiple threads; each thread opens a persistent connection and repeatedly runs a simple SELECT and a JOIN+aggregation.

> **lightbulb** Replace the db\_params values (dbname, user, password, host, port) with the connection details for your own Aurora instance before running the script.

```python theme={null}
import threading
import psycopg2
import time
import random
