# Creating and connecting the RDS instance to the application

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/Creating-and-connecting-the-RDS-instance-to-the-application/page

Guide to creating an Amazon RDS PostgreSQL instance, configuring network access, updating a Flask app on EC2 to connect and verify database persistence.

Welcome back. In the previous lesson we deployed the application to an EC2 instance. Submitting data from the web UI previously failed to persist because there was no database attached. In this guide we'll:

* Create an Amazon RDS PostgreSQL instance.
* Configure network access so the EC2 application can connect.
* Update the Flask app to use the RDS endpoint and verify data persistence.

This walkthrough assumes you have an EC2 instance running the application and appropriate AWS console access to create RDS instances and modify security groups.

Step 1 — Create an RDS PostgreSQL instance

1. Open the RDS console and click **Create database**.
2. For a simple demo, choose the Easy create option and select **PostgreSQL** (Free tier if eligible).
3. Provide a DB instance identifier (example: `database-one`) and the master username (example: `postgres`). Let RDS auto-generate the master password or set your own.

<Frame>
  <img alt="A screenshot of the AWS RDS &#x22;Create database&#x22; console showing DB instance size options (Production, Dev/Test, Free tier) and form fields for DB instance identifier and master username (set to &#x22;postgres&#x22;). The page also includes master password fields and an optional &#x22;Set up EC2 connection&#x22; section." />
</Frame>

Optional — Use the "Set up EC2 connection" helper

* On the Create database page, there is an optional "Set up EC2 connection" section. Enabling it and selecting your EC2 instance gives RDS permission to adjust network settings (security group/VPC) so the selected EC2 instance can reach the DB instance directly.
* This simplifies networking when your DB and EC2 instance are in different subnets or VPCs.

<Frame>
  <img alt="A screenshot of the AWS RDS &#x22;Create database&#x22; console showing the master username set to &#x22;postgres&#x22; and the optional &#x22;Set up EC2 connection&#x22; section selected. It also displays an EC2 instance dropdown and an informational box about VPC settings and compute resources." />
</Frame>

<Callout icon="lightbulb">
  When RDS shows the auto-generated master password, copy it immediately and store it securely. The password is only visible once on the creation success page — refreshing will hide it and require a reset via the RDS console.
</Callout>

Step 2 — Wait for the instance and capture connection details

* After creation, wait until the DB instance status becomes **Available**.
* Open the DB details and copy the endpoint and port (PostgreSQL default port: 5432). Note the master username and password you used/received.

Quick reference — typical PostgreSQL connection values

|       Parameter | Example value / notes                                    |
| --------------: | :------------------------------------------------------- |
| Host (endpoint) | `database-1.caywlfxrbtml.eu-central-1.rds.amazonaws.com` |
|            Port | `5432`                                                   |
|        Username | `postgres` (or your master user)                         |
|        Password | Auto-generated or chosen at creation — store it securely |
|   Database name | `postgres` (default)                                     |
|      Table name | `postgres_user` (example used in code)                   |

Step 3 — Connect to your EC2 instance

* SSH into the EC2 instance running the application (or use the EC2 console Connect option).
* Become root if necessary and navigate to the application directory to edit the code.

Step 4 — Update the Flask application to use RDS
Edit your application configuration to point to the RDS endpoint and credentials you copied. The example below shows an app.py that:

* Uses psycopg2 to connect to PostgreSQL.
* Creates the `postgres_user` table if it does not exist.
* Starts the Flask app listening on 0.0.0.0:5000.

```python theme={null}
from flask import Flask, render_template, request
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
