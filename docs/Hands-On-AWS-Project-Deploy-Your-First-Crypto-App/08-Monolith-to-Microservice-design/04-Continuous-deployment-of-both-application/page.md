# Configure the product service endpoint via env var:
# e.g. export PRODUCT_URL="http://crypto-app-882103207.eu-central-1.elb.amazonaws.com:5000/welcome"
PRODUCT_URL = os.environ.get('PRODUCT_URL', 'http://crypto-app-882103207.eu-central-1.elb.amazonaws.com:5000/welcome')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    user = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

    if user:
        # Redirect to the product microservice endpoint configured via PRODUCT_URL
        return redirect(PRODUCT_URL)

    # Authentication failed — redirect back to login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
```

<Callout icon="warning">
  Do not hard-code external service URLs or secrets in production code. Use environment variables, a configuration system, or service discovery (e.g., AWS Cloud Map or Route 53). Never store plaintext passwords — use a secure password hashing mechanism such as `bcrypt` and validate credentials by comparing hashes.
</Callout>

Step 3 — Commit and push your change (trigger CI/CD)
Commit the change and push to the repository branch monitored by your pipeline (for example `master` or `main`). This will trigger your CI/CD pipeline (e.g., AWS CodePipeline) to build a new Docker image and deploy the updated login service.

```bash theme={null}
git add app.py
git commit -m "Update login: redirect to product microservice after successful login"
git push origin master
```

Watch the pipeline build/deploy in the AWS Console to confirm the new image is built and a new task is started.

<Frame>
  <img alt="The image shows an AWS CodePipeline console for a project named &#x22;login-page-microservice&#x22; with the source stage succeeded and the build stage in progress. It includes navigation options on the left for CodePipeline features." />
</Frame>

Step 4 — Test the integration
Follow these steps to validate the login → product redirect:

| Task                     | How to perform                                                                                                         |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Open the login page      | Use the login microservice load balancer URL in your browser                                                           |
| Invalid credentials test | Try an incorrect email/password — you should remain on the login page                                                  |
| Retrieve valid user      | Query the DB to get a valid user record: <br />`sql<br>select * from users;`                                           |
| Successful login         | Login with valid credentials — you should be redirected to the product microservice (the `PRODUCT_URL` you configured) |

Expected result: after a successful login, the browser should redirect to the product microservice endpoint (e.g. `http://.../welcome`), demonstrating that the two services are connected but still independently deployable.

Step 5 — Confirm services are running in ECS
Verify both microservices are running in your cluster (for example, an Amazon ECS cluster). You should see the product service (crypto-app) and the login service (login-app-microservice) as separate services with running tasks.

<Frame>
  <img alt="The image shows an AWS Elastic Container Service (ECS) dashboard displaying details of a cluster named &#x22;ProductionCluster,&#x22; with active services including &#x22;crypto-app&#x22; and &#x22;login-app-microservice.&#x22; The status for both services is marked as active with tasks running." />
</Frame>

Links and references

* [AWS Cloud9](https://aws.amazon.com/cloud9/) — in-browser IDE for editing your microservice code.
* [AWS CodePipeline (CI/CD)](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline) — example pipeline for build and deploy.
* [Amazon ECS](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs) — container orchestration to run microservice tasks.
* [Route 53](https://aws.amazon.com/route53/) — for managing DNS names instead of hard-coded ELB URLs.
* [bcrypt documentation](https://bcrypt.readthedocs.io/en/latest/) — use for secure password hashing.

<Callout icon="lightbulb">
  By redirecting authenticated users to the product microservice load balancer, the login service remains decoupled from the product implementation. This enables independent development, testing, and deployment. For production, prefer configuration via environment variables, DNS-based routing (Route 53), or a service discovery mechanism rather than embedding ELB URLs in source code.
</Callout>

This completes the connection between the login and product microservices. Teams can now iterate independently while users are routed between services after authentication.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/e5b58a73-87f8-48f6-8275-bf679a28476a" />
</CardGroup>


# Continuous deployment of both application

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Continuous-deployment-of-both-application/page

Implementing continuous deployment for two microservices using AWS CodeCommit, CodePipeline, CodeBuild, and ECS to automatically build, deploy, and verify UI updates.

Welcome back. In this lesson we implement continuous deployment for both microservices and verify that commits pushed to each repository are automatically built and deployed to ECS via CodePipeline — without manual intervention.

## Overview

The original monolithic application has been split into independent microservices. Each microservice lives in its own repository and is built, tested, and deployed independently. This architecture enables faster releases, isolation of failures, and autonomy for different teams.

Below is a diagram that illustrates the migration from a monolith to microservices and how AWS CodePipeline and Amazon ECS work together in the CI/CD flow.

<Frame>
  <img alt="The image illustrates the process of moving from a monolithic architecture to microservices using AWS Cloud services. It shows how applications are built and deployed via AWS CodePipeline and Amazon Elastic Container Service, with an Application Load Balancer distributing traffic." />
</Frame>

What we'll do in this lesson:

* Make small UI changes to the product page and the login page.
* Commit and push those changes to each microservice repository.
* Watch CodePipeline detect the changes, build Docker images, and update the ECS services.
* Verify the new versions are served by the Application Load Balancer.

## Changes made

I used the Cloud9 IDE to edit both microservice repositories. Below are the final files I saved for each service.

### Product microservice — templates/product.html

This is the polished, production-ready product page that was committed to the product microservice repository:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>product.page</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/project_styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>NodeCloud Crypto Version 01</h1>
        <p>This is not actual crypto. This is just for learning purposes.</p>
    </div>

    <!-- Repeat this block for each product, just change the id and image source -->
    <div class="product" id="product1">
        <img src="{{ url_for('static', filename='images/product1.png') }}" alt="Product 1">
        <button onclick="window.location.href='/place_order?product=1';">ORDER NOW</button>
    </div>

    <div class="product" id="product2">
        <img src="{{ url_for('static', filename='images/product2.png') }}" alt="Product 2">
        <button onclick="window.location.href='/place_order?product=2';">ORDER NOW</button>
    </div>

    <div class="product" id="product3">
        <img src="{{ url_for('static', filename='images/product3.png') }}" alt="Product 3">
        <button onclick="window.location.href='/place_order?product=3';">ORDER NOW</button>
    </div>

    <div class="product" id="product4">
        <img src="{{ url_for('static', filename='images/product4.png') }}" alt="Product 4">
        <button onclick="window.location.href='/place_order?product=4';">ORDER NOW</button>
    </div>

    <div class="product" id="product5">
        <img src="{{ url_for('static', filename='images/product5.png') }}" alt="Product 5">
        <button onclick="window.location.href='/place_order?product=5';">ORDER NOW</button>
    </div>
</body>
</html>
```

### Login microservice — templates/login.html

I updated the login button text and improved inline styles for clarity. The final saved `login.html`:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Login</title>
    <style>
        body {
            width: 100%;
            padding: 10px;
            border: 4px solid #007f7f;
            background-color: #007f7f;
            color: white;
            box-sizing: border-box;
        }
        input {
            display: block;
            margin: 8px 0;
            padding: 8px;
        }
        button[type="submit"] {
            background-color: #00563c;
            color: white;
            padding: 8px 12px;
            border: none;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <form action="/login" method="post">
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Application login</button>
    </form>
</body>
</html>
```

## Commit and push (triggering pipelines)

After editing the files, I staged, committed, and pushed changes in each repository from Cloud9. The push to AWS CodeCommit triggered the associated CodePipelines.

Product microservice — example terminal steps:

```bash theme={null}
