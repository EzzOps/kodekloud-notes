# Database connection parameters (replace with your values)
db_params = {
    'dbname': 'testdb',
    'user': 'postgres',
    'password': 'Nqb17STYtto4v9IstLez',
    'host': 'performance-insight-db-prod.cluster-caywlfxrbtml.eu-central-1.rds.amazonaws.com',
    'port': '5432'
}

def run_query(thread_id):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        print(f"Thread-{thread_id} connected to the database.")

        while True:
            # Simple Query
            cur.execute("SELECT * FROM Customers WHERE Country = 'USA';")
            simple_records = cur.fetchall()
            print(f"Thread-{thread_id} fetched {len(simple_records)} records from Simple Query.")

            # Complex Query: join + aggregation
            cur.execute("""
                SELECT C.CustomerName, COUNT(O.OrderID) AS NumberOfOrders
                FROM Customers C
                LEFT JOIN Orders O ON C.CustomerID = O.CustomerID
                WHERE C.Country = 'USA'
                GROUP BY C.CustomerName;
            """)
            complex_records = cur.fetchall()
            print(f"Thread-{thread_id} fetched {len(complex_records)} records from Complex Query.")

            # Sleep randomly between 1 and 3 seconds to spread queries
            time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"Thread-{thread_id} encountered an error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print(f"Thread-{thread_id} connection closed.")

def main(thread_count=10):
    threads = []
    for i in range(1, thread_count + 1):
        t = threading.Thread(target=run_query, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    try:
        # Keep the main thread alive while worker threads run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping load generation...")

if __name__ == "__main__":
    main(thread_count=10)
```

Key points about the script:

* Default is 10 concurrent threads (adjust with main(thread\_count=N)).
* Each thread opens one persistent connection and alternates between a simple point-select and a JOIN+GROUP BY aggregation.
* Random short sleeps create staggered query timing so load is spread out.
* Threads are daemonized in this example; for graceful shutdown in production use non-daemon threads with a stop flag and join.

Sample terminal output (threads interleave):

```text theme={null}
Thread-1 connected to the database.
Thread-2 connected to the database.
Thread-1 fetched 1 records from Simple Query.
Thread-2 fetched 1 records from Simple Query.
Thread-1 fetched 1 records from Complex Query.
Thread-2 fetched 1 records from Complex Query.
Thread-3 connected to the database.
Thread-3 fetched 1 records from Simple Query.
...
```

After the script is running, open Performance Insights in the AWS Console. Within a few minutes you should see the SQL statements show up in Top SQL and DBLoad will reflect the generated activity. Use the dashboard to:

* Identify the queries contributing most AAS.
* See which user/host is causing load spikes.
* Inspect SQL text and execution samples to plan optimizations (rewrite, indexing, or parameterization).
* Correlate DBLoad spikes with instance-level metrics like CPUUtilization or DatabaseConnections.

## Further reading and references

* [AWS Performance Insights documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html)
* [Amazon Aurora (PostgreSQL) documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
* [RDS Monitoring and metrics](https://docs.aws.amazon.[SECRET_REDACTED].html)

I hope this lesson clarified how to use AWS RDS Performance Insights to monitor query-level performance on Aurora PostgreSQL. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/91b2b41b-ba10-4ab3-b483-1ee050a4556c/lesson/02f8439b-6f68-499c-9d44-000ca43a5748" />
</CardGroup>


# Query Editor console

Source: https://notes.kodekloud.com/docs/AWS-RDS/Monitoring-RDS-Database/Query-Editor-console/page

Guide to create and configure an Aurora PostgreSQL cluster, enable the Data API for Query Editor, and connect from the AWS console to run ad hoc SQL queries.

In this guide you'll learn how to create an Aurora PostgreSQL cluster that supports the in-console RDS Query Editor and how to connect to it from the AWS Management Console. The Query Editor is ideal for quick ad-hoc SQL against supported RDS/Aurora engines without installing a local client, but it requires specific engine versions and configuration (not all engines or versions are supported).

What you'll do:

* Create an Aurora (PostgreSQL-compatible) cluster in the AWS RDS console
* Enable the Data API (required for Serverless + Query Editor)
* Connect using the RDS Query Editor and run a sample SQL query

Prerequisites

* AWS account with permissions to create RDS/Aurora clusters
* Console access to Amazon RDS
* A username/password pair you will remember for DB authentication

Step 1 — Start creating the database

1. In the RDS console, go to Databases (or DB instances).
2. Click Create.
3. Choose Standard create.
4. Select Aurora (PostgreSQL-compatible).
5. Scroll to choose an engine version that supports the Query Editor (for this demo we used PostgreSQL 13.9).

Set your credentials (use something you will remember). In the demo below I used postgres for both username and password.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the RDS/Aurora DB creation form with Credentials Settings (master username set to &#x22;postgres&#x22; and masked password fields) and cluster storage configuration options. The right pane lists supported DB engine versions and provisioning details." />
</Frame>

Step 2 — Configure cluster, capacity and connectivity

* Keep default cluster settings unless you need custom networking, VPC, or subnet groups.
* For capacity, choose Serverless if you want Aurora Serverless. In the demo min and max capacity were both set to two capacity units.
* Leave connectivity defaults unless a specific VPC/subnet/security group is required.

In Additional configuration make sure to enable the Data API when using Aurora Serverless. The Data API lets the Query Editor (and other tools) communicate with Serverless clusters without a persistent database network connection.

<Callout icon="lightbulb">
  Enable the Data API if you plan to use the RDS console Query Editor with Aurora Serverless. Without the Data API enabled, the Query Editor will be unable to connect to the cluster.
</Callout>

<Frame>
  <img alt="A screenshot of the AWS RDS/Aurora console showing network and additional configuration options, including DB subnet group, VPC security group selection, and a checked Data API option. The page also shows Babelfish settings and other database authentication sections." />
</Frame>

Step 3 — Create and wait for availability

* Review all settings and click Create database.
* Wait for the cluster to show as available in the Databases list before attempting to connect.

<Frame>
  <img alt="Screenshot of the Amazon RDS console with a green success banner saying &#x22;Successfully created database database-1.&#x22; The Databases list shows one available Aurora PostgreSQL Serverless instance (database-1) in eu-central-1." />
</Frame>

Step 4 — Open and connect with the Query Editor

1. In the RDS console, open Query Editor.
2. From the database dropdown select the newly created database.
3. If prompted, provide the database credentials (username and password you configured) and click Connect database.

<Callout icon="lightbulb">
  Note: The Query Editor requires valid database credentials (or an appropriate authentication method) and the necessary IAM permissions to use the editor in the console. For Aurora Serverless clusters, the Data API must be enabled so the editor can connect.
</Callout>

Running SQL in the Query Editor
Once connected you can run SQL directly in the editor. Example — list tables in the current database:

```sql theme={null}
select * from information_schema.tables;
-- Press Run to see the current database tables below
```

After executing the query, results appear in the pane below the editor. By default a newly created Aurora PostgreSQL cluster typically contains a default database named postgres; that is the DB you are querying here.

<Frame>
  <img alt="Screenshot of the Amazon RDS Query Editor showing a result set (183 rows) listing PostgreSQL catalog tables. The table displays columns like table_catalog, table_schema, table_name and table_type with entries such as pg_type, pg_roles and pg_settings." />
</Frame>

Saving, switching and managing queries

* Save queries: Click Save, give the query a name (e.g., "RDS query") — saved queries appear in the Saved queries section.
* Recent queries: The Recent tab lists queries you have executed.
* Switch databases: Use Change database in the Query Editor, select a different DB, and provide the correct credentials.

Quick compatibility and checklist

| Item                      | Requirement / Notes                                  | Links & References                                                   |
| ------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------- |
| Engine                    | Aurora PostgreSQL (supported versions only)          | See AWS docs below                                                   |
| Serverless + Query Editor | Data API must be enabled                             | [https://docs.aws.amazon.com/rds/](https://docs.aws.amazon.com/rds/) |
| Authentication            | Valid DB credentials and console IAM permissions     | Console access and DB user/password                                  |
| Use case                  | Ad-hoc queries and light administration from browser | Good for quick checks; use full clients for heavy operations         |

Troubleshooting tips

* If the Query Editor cannot connect, confirm Data API is enabled (for Serverless) and that you used the correct DB username/password.
* Ensure your AWS IAM role/user has permissions to use RDS console Query Editor and related APIs.
* If you need persistent client access, configure network/security groups and connect with a local psql client or use AWS Systems Manager Session Manager for secure access.

Further reading

* Amazon RDS documentation: [https://docs.aws.amazon.com/rds/](https://docs.aws.amazon.com/rds/)
* Aurora Serverless & Data API overview: [https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-serverless.html](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-serverless.html)
* Query Editor in the AWS Console: [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)

That covers the essentials of using the RDS Query Editor with an Aurora PostgreSQL cluster configured for the Data API. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/91b2b41b-ba10-4ab3-b483-1ee050a4556c/lesson/3a13af8e-07ca-4130-b9aa-13ec6c4648c8" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-rds/module/91b2b41b-ba10-4ab3-b483-1ee050a4556c/lesson/e37fd3b7-759d-490a-95eb-6ca212f2e628" />
</CardGroup>
