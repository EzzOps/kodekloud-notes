# RDS database configuration
db_host = 'database-1.caywlfxrbtml.eu-central-1.rds.amazonaws.com'
db_port = '5432'
db_user = 'postgres'
db_password = '02kq1ON6PFt8Lj3rf08h'
db_name = 'postgres'
table_name = 'postgres_user'

# Connect to the database
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except psycopg2.Error as e:
        print("Connection to the database failed:", e)
        return None

# Create the table if it doesn't exist (uses psycopg2.sql for safe identifier formatting)
def create_table():
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to the database")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "CREATE TABLE IF NOT EXISTS {} ("
                    "id SERIAL PRIMARY KEY, "
                    "name VARCHAR(255) NOT NULL, "
                    "email VARCHAR(255) NOT NULL, "
                    "country VARCHAR(255) NOT NULL"
                    ")"
                ).format(sql.Identifier(table_name))
            )
        connection.commit()
        print("Table created successfully!")
    except psycopg2.Error as e:
        print("Error while creating table:", e)
    finally:
        connection.close()

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)
```

<Callout icon="lightbulb">
  Do not hardcode production credentials in source code. Use environment variables, [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), or [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) to manage secrets securely. Also ensure security groups and VPC/subnet routing restrict access to only necessary IPs and services.
</Callout>

Example: verifying the project layout and editing app.py on the EC2 instance

```bash theme={null}
[ec2-user@ip-172-31-19-201 ~]$ sudo su
[root@ip-172-31-19-201 ec2-user]# cd
[root@ip-172-31-19-201 ~]# ls -lrt
total 0
drwxr-xr-x. 4 root root 49 Aug 31 22:08 aws-rds
[root@ip-172-31-19-201 ~]# cd aws-rds/
[root@ip-172-31-19-201 aws-rds]# ls -lrt
total 4
-rw-r--r--. 1 root root 129 Aug 31 22:08 README.md
drwxr-xr-x. 3 root root 37 Aug 31 22:09 db-app
[root@ip-172-31-19-201 aws-rds]# cd db-app/
[root@ip-172-31-19-201 db-app]# ls -lrt
total 4
-rw-r--r--. 1 root root 3085 Aug 31 22:08 app.py
drwxr-xr-x. 2 root root 65 Aug 31 22:09 templates
[root@ip-172-31-19-201 db-app]# vim app.py
[root@ip-172-31-19-201 db-app]#
```

Step 5 — Start the Flask app and test

* Start the Flask application (for example: python3 app.py or using your process manager).
* Open the application URL in your browser and submit user details.
* The app will insert rows into the RDS PostgreSQL table.

Verify stored records

* The sample application provides a /getdata endpoint that queries the table and renders results.
* Visit http\://\<ec2\_ip>:5000/getdata to confirm entries are stored.

<Frame>
  <img alt="A screenshot of a simple web page titled &#x22;Data&#x22; showing a small table of user records (ID, Name, Email, Country) with entries like &#x22;raghu&#x22; and &#x22;tom&#x22; and a &#x22;Go Back&#x22; button. The browser tab bar and the URL (52.59.212.235:5000/getdata) are visible at the top." />
</Frame>

Summary

* Created a PostgreSQL instance in Amazon RDS and captured the endpoint, port, username, and password.
* Used the optional RDS "Set up EC2 connection" helper to simplify networking when applicable.
* Updated the Flask application to connect to the RDS endpoint, ensuring the required table is created at startup.
* Verified data insertion and retrieval via the application UI and the /getdata endpoint.

Further reading and references

* [Amazon RDS Documentation](https://docs.aws.amazon.com/rds/)
* [Amazon RDS for PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
* [psycopg2 — PostgreSQL adapter for Python](https://www.psycopg.org/docs/)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
* [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

That concludes this hands-on lesson on connecting a Flask application on EC2 to a PostgreSQL database hosted in Amazon RDS. Thank you for following along.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/218df4b1-3f04-401b-98c4-a9ada7471e88" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/02cb4468-ae89-457e-863c-eac32be6fd07" />
</CardGroup>


# Deploying the sample application on EC2 instance

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/Deploying-the-sample-application-on-EC2-instance/page

Guide to deploy, run, and verify a Flask sample application on an Amazon EC2 instance, including setup, dependencies, security group configuration, and noting missing RDS database connectivity.

Hello and welcome to this lesson.

In this guide you'll deploy a small Flask-based sample application to an Amazon EC2 instance, run it, and verify the app is reachable from a browser. This lesson demonstrates the application lifecycle on EC2 (installation, running, and basic verification). Database connectivity (RDS configuration) is intentionally excluded here — the app will start, but form submissions will fail until an RDS endpoint and credentials are configured.

What you'll do

* Launch an EC2 instance to host a Flask app.
* Connect to the instance and install packages.
* Clone and run the sample app.
* Verify the web app is reachable externally.
* Attempt a data submission (expected to fail due to missing DB configuration).

Why this matters (SEO keywords): EC2 deploy Flask app, run Flask on EC2, EC2 security group open port 5000, connect EC2 via EC2 Instance Connect, install git and pip on Amazon Linux.

***

## Step 1 — Launch an EC2 instance

1. Open the EC2 console (use the AWS console search bar).
2. Click **Launch Instance** and give the instance a name, for example: `User Information App`.
3. Choose the Amazon Linux AMI.
4. Create or select a security group. For this demo we allow SSH from anywhere, but in production restrict SSH to your IP address only.

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch an instance&#x22; console showing the Name and tags field, Application and OS Images (AMIs) selection, and quick-start OS tiles. The right-hand Summary panel lists details like 1 instance, Amazon Linux AMI, t2.micro instance type, and a &#x22;Launch instance&#x22; button." />
</Frame>

<Callout icon="warning">
  For security, do not open SSH (port 22) to 0.0.0.0/0 in production. Restrict SSH inbound access to specific IP addresses or your administrator network.
</Callout>

If you encounter a key-pair prompt and haven't created one, for this demo you can select "Proceed without key pair" (not recommended for production). Click **Launch Instance** and wait for the instance state to become **running**. Then select the instance to view its details.

<Frame>
  <img alt="Screenshot of the AWS EC2 Instances page. It shows one running t2.micro instance named &#x22;user-information-app&#x22; with its instance ID and public IPv4 address displayed." />
</Frame>

***

## Step 2 — Connect to the EC2 instance

1. Select the instance in the console and click **Connect**.
2. Use **EC2 Instance Connect** to open a browser-based terminal. For Amazon Linux the username is typically `ec2-user`.

<Frame>
  <img alt="A screenshot of the AWS EC2 console &#x22;Connect to instance&#x22; page showing EC2 Instance Connect options, the instance ID, public IPv4 address, and a default username (ec2-user). The dialog includes tabs for Session Manager, SSH client and an orange &#x22;Connect&#x22; button." />
</Frame>

In the browser terminal, become root and switch to the home directory:

```bash theme={null}
sudo su
cd ~
```

***

## Step 3 — Get the application code from GitHub

On the repository page click **Code** and copy the HTTPS URL for cloning.

<Frame>
  <img alt="A screenshot of a GitHub repository page for &#x22;aws-rds&#x22; showing the Clone dialog with the HTTPS URL copied. The README for &#x22;user-information-app-rds&#x22; is visible and the repo language breakdown (Python and HTML) appears on the right." />
</Frame>

Try cloning the repo. If `git` is not installed you will see an error like:

```bash theme={null}
[root@ip-172-31-19-201 ~]# git clone https://github.com/kodekloudhub/aws-rds.git
bash: git: command not found
```

Install Git and pip (python3-pip on Amazon Linux), then install a PostgreSQL client driver (psycopg2-binary) which the app will use later when you configure an RDS backend:

```bash theme={null}
sudo yum install -y git
sudo yum install -y python3-pip
pip3 install psycopg2-binary
```

***

## Step 4 — Clone the repo and inspect the app

Clone the repository and change into the app folder:

```bash theme={null}
git clone https://github.com/kodekloudhub/aws-rds.git
cd aws-rds/db-app
ls -lrt
```

You should see the main application file and the templates folder:

```bash theme={null}
total 4
-rw-r--r--. 1 root root 3085 Aug 31 22:08 app.py
drwxr-xr-x. 2 root root   65 Aug 31 22:09 templates
```

***

## Step 5 — Install Python dependencies and attempt to start the app

Try running the Flask app:

```bash theme={null}
python3 app.py
```

If Flask is not installed you'll see an import error:

```text theme={null}
Traceback (most recent call last):
  File "/root/aws-rds/db-app/app.py", line 1, in <module>
    from flask import Flask, render_template, request
ModuleNotFoundError: No module named 'flask'
```

The repository includes a requirements.txt file (in this repository it’s inside the `templates` folder). Install the required Python packages:

```bash theme={null}
cd templates
pip3 install -r requirements.txt
```

Typical packages to be installed include Flask, PyMySQL/Psycopg2, Jinja2, and Werkzeug. You may see a warning about running pip as root.

<Callout icon="lightbulb">
  Tip: For cleaner dependency management, create and activate a Python virtual environment (venv) instead of installing packages globally. This prevents permission conflicts and keeps dependencies isolated.
</Callout>

***

## Step 6 — Start the Flask application

Return to the app folder and start the app:

```bash theme={null}
cd ..
python3 app.py
```

You should see the Flask development server start and bind to port 5000:

```text theme={null}
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.31.19.201:5000
Press CTRL+C to quit
```

<Callout icon="warning">
  The built-in Flask server is for development and testing only. For production, use a WSGI server such as Gunicorn or uWSGI and place it behind a reverse proxy (Nginx, Apache).
</Callout>

***

## Step 7 — Open port 5000 in the instance security group

By default the security group created during instance launch may only allow SSH (22), HTTP (80), and HTTPS (443). Port 5000 is not open, so the Flask app won't be accessible externally until you add an inbound rule.

<Frame>
  <img alt="A screenshot of the AWS EC2 console showing the security group &#x22;launch-wizard-5&#x22; (sg-0fef0dcd096356b03) details. The inbound rules list shows SSH (port 22), HTTPS (443) and HTTP (80) open to 0.0.0.0/0." />
</Frame>

Edit the security group's inbound rules and add a rule allowing TCP port 5000 from your IP (or 0.0.0.0/0 for a quick demo). Save the changes.

Recommended inbound rules (example):

| Type       | Protocol | Port range | Source                         | Use case                            |
| ---------- | -------- | ---------- | ------------------------------ | ----------------------------------- |
| SSH        | TCP      | 22         | Your IP (e.g., 203.0.113.4/32) | Secure shell access (restrict this) |
| HTTP       | TCP      | 80         | 0.0.0.0/0                      | Web traffic (optional)              |
| HTTPS      | TCP      | 443        | 0.0.0.0/0                      | Encrypted web traffic (optional)    |
| Custom TCP | TCP      | 5000       | Your IP or 0.0.0.0/0 (demo)    | Flask dev server port for testing   |

***

## Step 8 — Access the application in a browser

Copy the instance's public IPv4 address from the EC2 console and open the Flask app in a browser:

http\://\<PUBLIC\_IP>:5000

You should see the "User Details" form served by the Flask app:

<Frame>
  <img alt="A web browser shows a centered &#x22;User Details&#x22; form with fields for Name, Email, Country and a green &#x22;Submit&#x22; button. The page is loaded from an IP address (3.64.252.128:5000) with several tabs open." />
</Frame>

***

## Step 9 — Submit data (expected failure)

The app displays a form to collect user details. If you submit the form now, the app will likely fail to connect to a database and return an error like "Failed to connect to the database." This is expected — you have not yet configured RDS connection details (endpoint, port, username, password, database name) or the necessary network access (VPC, security group, routing).

<Frame>
  <img alt="A browser window showing a mostly blank page with the message &#x22;Failed to connect to the database&#x22; in the top-left. The address bar shows 3.64.252.128:5000/submit and several AWS/EC2-related tabs are open." />
</Frame>

***

## Next steps — Connect the app to RDS (not covered in this lesson)

To complete the deployment and persist form submissions you will need to:

* Create an RDS instance (MySQL/Postgres) or use an existing database.
* Provide the application with the database endpoint, port, username, password, and database name (edit config or environment variables in the app).
* Ensure network connectivity: place EC2 and RDS in the same VPC/subnet or allow routing, and update security group inbound/outbound rules to permit traffic between EC2 and RDS.
* Re-test the form submission and verify data is inserted into the database.

Additional resources and references

* [Amazon EC2 documentation](https://docs.aws.amazon.com/ec2/)
* [EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html)
* [Flask documentation](https://flask.palletsprojects.com/)
* [AWS RDS documentation](https://docs.aws.amazon.com/rds/)
* [Python virtual environments (venv)](https://docs.python.org/3/library/venv.html)

That’s it for this lesson — in the next lesson we will configure the RDS database and connect the app so form submissions persist successfully.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/64436ab4-aa3b-4f53-8092-70d4d3dbe4a6" />
</CardGroup>
