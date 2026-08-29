# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Use parameterized query to avoid SQL injection
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for('product'))

    return redirect(url_for('login'))

@app.route('/product')
def product():
    # This redirect points to the product application running on another service.
    return redirect("http://35.156.49.246:5000/welcomepage")
    # Alternative for local testing:
    # return "Hello, this is the product page."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

Key points about this implementation

* The app uses `get_db_connection()` to obtain a DB connection and performs a parameterized query to look up the user by `email` and `password`.
* On success, the route redirects to `/product`, which in turn forwards to the product application at the configured external URL.
* The Flask app listens on `0.0.0.0:5000` with `debug=True` for local development.

Routes summary

| Method | Path       | Purpose                                                                                                         |
| ------ | ---------- | --------------------------------------------------------------------------------------------------------------- |
| GET    | `/`        | Render `login.html` — the login form.                                                                           |
| POST   | `/login`   | Validate submitted `email` and `password`. If valid, redirect to `/product`.                                    |
| GET    | `/product` | Redirects to the product application (`http://35.156.49.246:5000/welcomepage`) or serves a local test response. |

Security note

> **warning** This example checks passwords as stored plaintext in the database. Storing or comparing plaintext passwords is insecure. In production, always store hashed passwords (e.g., using bcrypt) and verify using a secure hashing check. Also run the app over HTTPS in production.

Best practices and quick improvements

* Password storage: Replace plaintext storage with a strong hashing scheme (bcrypt, Argon2). Verify using the hashing library rather than direct comparison.
* Sessions: After authentication, set a secure session or issue a JWT so subsequent requests can be authorized without re-checking credentials.
* Input validation: Validate and sanitize form inputs before using them in queries or application logic.
* HTTPS: Deploy behind TLS in production and disable `debug=True` for safety.
* Connection handling: Use connection pooling for production workloads (e.g., SQLAlchemy pool, a connection pooler).

Links and references

* Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Password hashing (bcrypt): [https://pypi.org/project/bcrypt/](https://pypi.org/project/bcrypt/)
* Docker training (reference): [https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner)
* AWS CodeBuild: [https://aws.amazon.com/codebuild/](https://aws.amazon.com/codebuild/)
* AWS CodePipeline (CI/CD): [https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)

Next steps

* Containerize this service with a Dockerfile and build images for your CI pipeline.
* Add automated tests and a CI job (e.g., AWS CodeBuild).
* Deploy via a CD pipeline (e.g., AWS CodePipeline) and secure traffic with HTTPS.

That's it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/f5375085-5a50-4d15-a21f-b288e68a7c77)


# Run DB initialization script

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Run-DB-initialization-script/page

Guide to initialize a PostgreSQL users table with dummy accounts for a login microservice, including cloning the repo, running a helper script, and verifying via DBeaver.

Hello and welcome back.

In this lesson we will run an initialization script to create a few dummy users in our PostgreSQL database. This helps the login microservice have test accounts available during development and QA.

Overview

* Locate the CodeCommit repository in the AWS Console.
* Clone the repo into your Cloud9 environment (or another terminal).
* Save and run the helper script that creates the `users` table and inserts dummy accounts.
* Verify the inserted rows using a SQL client such as DBeaver.

Open the AWS CodeCommit repository (in my account it's called `login-page-microservice`). You should see the same repository in your exercise account.

<Frame>
  <img alt="The image shows a screenshot of the AWS CodeCommit console with a list of repositories, including their names, last modified dates, and options for cloning via HTTPS or SSH." />
</Frame>

Prerequisites

* AWS Cloud9 (or any machine with terminal access to your repo).
* Python 3 and `pip3`.
* `psycopg2` installed (or `psycopg2-binary`).
* Network access to your PostgreSQL instance (RDS endpoint or other host).
* A SQL client like DBeaver for verification.

Helper script (save as `helper_script.py`)
Below is a clean, robust helper script that:

* reads DB connection settings from environment variables,
* creates the `users` table if it doesn't exist,
* inserts dummy users using `ON CONFLICT DO NOTHING` to avoid duplicate-key errors.

```python theme={null}
