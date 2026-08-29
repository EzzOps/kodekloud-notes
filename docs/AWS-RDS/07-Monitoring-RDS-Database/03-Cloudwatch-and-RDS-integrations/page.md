# Cloudwatch and RDS integrations

Source: https://notes.kodekloud.com/docs/AWS-RDS/Monitoring-RDS-Database/Cloudwatch-and-RDS-integrations/page

Configuring CloudWatch alarms and SNS notifications to monitor Amazon Aurora RDS connections, inspect Performance Insights, and simulate load to trigger and test alerts.

Hello, and welcome back.

In this lesson we'll set up alerting and monitoring for an Amazon Aurora (RDS) database using Amazon CloudWatch alarms. If you want to follow along, I already have an Aurora cluster available — you can create one in your account and use that cluster's identifier throughout the steps below.

Key topics covered:

* Inspecting database behavior with Performance Insights and the RDS console
* Creating a CloudWatch alarm for DatabaseConnections
* Configuring SNS notifications for alarm actions
* Simulating load with a Python script to trigger the alarm

## Inspect the database with Performance Insights and RDS monitoring

Performance Insights provides detailed, database-level telemetry for Aurora and other RDS engines. You can also use the Monitoring tab in the RDS console for a quick overview of common metrics.

<Frame>
  <img alt="A screenshot of the AWS RDS console showing the &#x22;performance-insight-db-prod&#x22; Aurora PostgreSQL cluster with its instances, CPU/activity indicators, and endpoints. The Writer and Reader endpoints are listed as Available and there's a section for managing IAM roles." />
</Frame>

Use Performance Insights to understand query load, waits, and top-consuming SQL statements. When you need proactive notifications (for example, when active connections spike) use CloudWatch alarms.

## Create a CloudWatch alarm for DatabaseConnections (step-by-step)

1. Open the CloudWatch console and go to Alarms → Create alarm.
2. Select a metric source: choose RDS and filter by your DB identifier/role (WRITER/READER). For this guide we'll use the DatabaseConnections metric.
3. Preview the time series to confirm you're selecting the intended resource and timeframe.

<Frame>
  <img alt="A screenshot of an AWS CloudWatch/RDS metric selection screen showing a time-series graph of DatabaseConnections that rises to about 27. Below the graph is a selectable list of RDS metrics (DatabaseConnections, Deadlocks, FreeableMemory, CPUUtilization, etc.) for the performance-insight-db-prod cluster." />
</Frame>

4. Configure the metric evaluation:
   * Choose Statistic (e.g., Average) and Period (e.g., 1 minute) that match your desired sensitivity.
   * Set the evaluation period and datapoints to alarm according to how quickly you want alerts.

<Frame>
  <img alt="A screenshot of the AWS CloudWatch &#x22;Create alarm&#x22; screen configuring an RDS metric. It shows a rising DatabaseConnections graph on the left and form fields on the right for Namespace, Role, DBClusterIdentifier, Statistic, and Period." />
</Frame>

5. Define the threshold. For this demo, use a static threshold:
   * Trigger when DatabaseConnections > 30.
   * Adjust threshold and evaluation windows for your production needs.

<Frame>
  <img alt="A screenshot of the AWS CloudWatch alarm configuration page showing the &#x22;Conditions&#x22; section with a Static threshold and the &#x22;Greater&#x22; comparison selected, set to a threshold value of 30 for DatabaseConnections. The top of the screen shows metric settings (Role: WRITER, DBClusterIdentifier, and Statistic: Average)." />
</Frame>

6. Configure alarm actions:
   * Create or choose an existing SNS topic to send notifications (email, SMS, Lambda, HTTP endpoints).
   * Add subscribers (for example, an email address). You can create a new SNS topic as part of the alarm workflow.

<Frame>
  <img alt="Screenshot of the AWS CloudWatch alarm action setup showing options for alarm state triggers and creating an SNS topic. The form shows a topic name &#x22;Default_CloudWatch_Alarms_Topic&#x22; and an email endpoint field (user@example.com) for notifications." />
</Frame>

> **lightbulb** After creating an SNS topic and adding an email endpoint, you must confirm the subscription from the email inbox. Until the subscription is confirmed you will not receive alarm notifications.

7. Name the alarm (for example, "High DB connections") and create it. CloudWatch will evaluate the metric and change the alarm state to ALARM when conditions are met.

## Simulate load to trigger the alarm

To demonstrate the alarm firing, you can run a short Python script that opens many concurrent connections to the DB. Replace the connection parameters with your own host, database, username, and password.

```python theme={null}
import threading
import psycopg2

def run_query(thread_id):
    try:
        conn = psycopg2.connect(
            host="your-db-host",
            port=5432,
            database="your_db",
            user="your_user",
            password="your_password"
        )
        cur = conn.cursor()
        print(f"Thread-{thread_id} connected to the database.")

        # Simple query
        cur.execute("SELECT 1;")
        cur.fetchone()
        print(f"Thread-{thread_id} fetched 1 record from Simple Query.")

        # Example "complex" query
        cur.execute("SELECT COUNT(*) FROM information_schema.tables;")
        cur.fetchone()
        print(f"Thread-{thread_id} fetched 1 record from Complex Query.")

    except Exception as e:
        print(f"Thread-{thread_id} error: {e}")
    finally:
        try:
            cur.close()
            conn.close()
            print(f"Thread-{thread_id} closed the database connection.")
        except Exception:
            pass
