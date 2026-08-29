# Connecting login microservice with product microservice

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Connecting-login-microservice-with-product-microservice/page

Connecting a login microservice to a product microservice by redirecting authenticated users to the product load balancer using environment variables and CI/CD deployment verification

Goal: after users successfully authenticate with the login microservice, redirect them to the product microservice running behind its own load balancer. This preserves service boundaries so each microservice can be developed, built, and deployed independently.

Overview

* Copy the product microservice load balancer DNS name from the AWS console.
* Update the login microservice code to redirect authenticated users to the product service endpoint.
* Push the change to trigger your CI/CD pipeline (build → image → deploy).
* Verify the integration by logging in and confirming the redirect.

Step 1 — Get the product load balancer DNS
Copy the product service's load balancer DNS (ELB/ALB) from the AWS Console and append the appropriate path (for example `/welcome` or `/welcome-page`) to use as the redirect target.

<Frame>
  <img alt="The image shows an AWS EC2 console with a focus on a &#x22;Load Balancers&#x22; section for an application named &#x22;crypto-app,&#x22; displaying navigation and instance management options." />
</Frame>

Step 2 — Update the login microservice code (Flask example)
In your login microservice repository (for example, in [Cloud9](https://aws.amazon.com/cloud9/)), open `app.py` and update the login POST handler so that on successful authentication it redirects to the product microservice load balancer URL.

Below is an improved example that:

* uses an environment variable for the product URL (so you avoid hard-coding in source),
* shows the login route and redirect handler,
* keeps the login flow simple for clarity.

```python theme={null}
import os
from flask import Flask, request, redirect, url_for
app = Flask(__name__)
