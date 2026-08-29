# helper_script.py
import os
import psycopg2

# Read DB connection info from environment variables, with optional fallbacks.
DB_HOST = os.environ.get('AWS_RDS_HOST', 'your-rds-host.example.rds.amazonaws.com')
DB_PORT = os.environ.get('AWS_RDS_PORT', '5432')
DB_USER = os.environ.get('AWS_RDS_USERNAME', 'postgres')
DB_PASSWORD = os.environ.get('AWS_RDS_PASSWORD', 'change_me')
DB_NAME = os.environ.get('AWS_RDS_DB_NAME', 'microservice')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

# Create the users table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
''')

# Dummy users to insert
dummy_users = [
    ('Alice_dummy', 'alice_dummy@example.com', 'password123_dummy'),
    ('Bob_dummy', 'bob_dummy@example.com', 'password456_dummy'),
    ('Charlie_dummy', 'charlie_dummy@example.com', 'password789_dummy')
]

# Insert dummy users, ignoring duplicates on email
for user in dummy_users:
    cur.execute('''
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING
    ''', user)

conn.commit()
cur.close()
conn.close()
```

Environment variables reference

| Environment variable | Purpose                           | Example                                   |
| -------------------- | --------------------------------- | ----------------------------------------- |
| `AWS_RDS_HOST`       | Database hostname or RDS endpoint | `your-rds-host.example.rds.amazonaws.com` |
| `AWS_RDS_PORT`       | Database port                     | `5432`                                    |
| `AWS_RDS_USERNAME`   | Database user                     | `postgres`                                |
| `AWS_RDS_PASSWORD`   | Database password                 | `change_me`                               |
| `AWS_RDS_DB_NAME`    | Database name                     | `microservice`                            |

Important: use environment variables or a secrets manager for credentials; avoid hardcoding secrets.

Clone and run from Cloud9 (or any terminal in the repo)

1. Clone the CodeCommit repository into your environment (HTTPS example):

```bash theme={null}
git clone https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/login-page-microservice
```

You should see output similar to:

```bash theme={null}
Cloning into 'login-page-microservice'...
remote: Counting objects: 10, done.
Unpacking objects: 100% (10/10), done.
```

2. If `psycopg2` is missing, install dependencies from `requirements.txt`:

```bash theme={null}
pip3 install -r requirements.txt
```

Common error before installing dependencies:

```bash theme={null}
Traceback (most recent call last):
  File "helper_script.py", line 1, in <module>
    import psycopg2
ModuleNotFoundError: No module named 'psycopg2'
```

3. Ensure environment variables are set (example Bash):

```bash theme={null}
export AWS_RDS_HOST='your-rds-host.example.rds.amazonaws.com'
export AWS_RDS_PORT='5432'
export AWS_RDS_USERNAME='postgres'
export AWS_RDS_PASSWORD='change_me'
export AWS_RDS_DB_NAME='microservice'
```

4. Run the helper script:

```bash theme={null}
python3 helper_script.py
```

If the script runs successfully it typically returns to the command prompt without additional output — this indicates the script executed and committed changes to the database.

<Callout icon="lightbulb">
  Always prefer using environment variables for credentials (or a secrets manager). Avoid hardcoding passwords or database hosts directly in scripts.
</Callout>

Verify the inserted rows with DBeaver
To confirm the table and data:

* Open DBeaver and create a new PostgreSQL connection.
* Provide host, port, username, password, and database name (for example `microservice`).
* Expand the connection: Databases → microservice → Schemas → public → Tables to find the `users` table.

<Frame>
  <img alt="The image shows the DBeaver interface with a PostgreSQL connection settings window open, where database connection details such as server, URL, authentication, and username are being configured." />
</Frame>

Open an SQL editor against the `microservice` database and run:

```sql theme={null}
select * from users;
```

<Frame>
  <img alt="The image shows a screenshot of DBeaver with a database named &#x22;microservice&#x22; open, displaying the database navigator and a context menu for SQL editor options." />
</Frame>

You should see the three dummy users in the result set. Use one of these accounts to log into the application for testing.

Troubleshooting: duplicate-key error
If you run a previous version of the script repeatedly without conflict handling, you may encounter a UniqueViolation on the `email` column. Example:

```text theme={null}
psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "users_email_key"
DETAIL:  Key (email)=(alice_dummy@example.com) already exists.
```

<Callout icon="warning">
  If you see a unique constraint error, either update the script to upsert or use `ON CONFLICT DO NOTHING` (as shown above), or clear the table before reinserting data if that is acceptable for your workflow.
</Callout>

Next steps

* Review how the login microservice queries the `users` table and integrates authentication.
* Promote the initialization script into a deployment automation step if you want repeatable environment setups (consider migrations tools such as Flyway or Alembic for production schema changes).

Links and references

* [AWS CodeCommit documentation](https://docs.aws.amazon.com/codecommit/)
* [AWS Cloud9](https://aws.amazon.com/cloud9/)
* [psycopg2 on PyPI](https://pypi.org/project/psycopg2/)
* [DBeaver](https://dbeaver.io/)
* [AWS RDS for PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/0d35c72c-1a52-4509-b1b0-9f16688f6265" />
</CardGroup>


# Setup CodePipeline for login application

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Setup-CodePipeline-for-login-application/page

Guide to set up an AWS CodePipeline and CodeBuild workflow that builds, tags, and pushes a Dockerized Flask login microservice to Amazon ECR for deployment.

Welcome — this guide walks through creating an AWS CodePipeline that builds and pushes a container image for a Flask-based login microservice. You'll learn how to:

* Verify the Flask application routes are present.
* Add a Dockerfile to containerize the app.
* Add a `buildspec.yml` so CodeBuild can build and push the image to ECR.
* Create the ECR repository and configure a CodePipeline that pulls from CodeCommit and invokes CodeBuild.

This workflow assumes your source is hosted in AWS CodeCommit and that you will use AWS CodeBuild to build and push the Docker image to Amazon ECR.

Prepare the Flask application routes (app.py)
Confirm these route handlers exist in your application (for example, in `app.py`). They are the minimal routes used by this microservice:

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_post', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return redirect(url_for('product'))

    return redirect(url_for('login'))

@app.route('/product')
def product():
    return redirect("http://35.156.49.246:5000/welcome_page")
    # return "Hello, this is the product page."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

<Callout icon="warning">
  This example checks passwords directly in the database and may use plaintext passwords. For production, always store passwords hashed (e.g., bcrypt) and use secure authentication flows. Also validate and sanitize inputs to prevent SQL injection — use parameterized queries and an ORM when possible.
</Callout>

Files to add to the repository

* `Dockerfile` — containerize the Flask app.
* `buildspec.yml` — instructs CodeBuild how to build the image, authenticate to ECR, push the image, and emit `imagedefinitions.json` used by deployment stages.
* Application code (`app.py`, templates, `requirements.txt`, etc.) — already present in your repo.

Create the Dockerfile
Add a `Dockerfile` at the repository root to build the container image. A minimal example:

```dockerfile theme={null}
FROM python:3.10-slim
