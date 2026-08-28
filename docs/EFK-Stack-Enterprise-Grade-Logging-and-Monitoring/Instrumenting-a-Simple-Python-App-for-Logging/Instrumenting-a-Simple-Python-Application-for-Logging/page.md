# Default credentials
USERNAME = 'admin'
PASSWORD = 'password'

def is_weak_password(password):
    if len(password) < 8:
        return True
    if not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
        return True
    return False

@app.before_request
def log_request_info():
    logger.info(f"Request method: {request.method}")
    logger.info(f"User Agent: {request.user_agent}")
    logger.info(f"Client IP: {request.remote_addr}")

@app.after_request
def log_response_info(response):
    logger.info(f"Response status: {response.status}")
    return response

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == USERNAME and password == PASSWORD:
        flash('Login successful!', 'success')
        logger.info('Login successful for user: %s', username)
        if is_weak_password(password):
            logger.warning('Weak password used by user: %s', username)
        return redirect(url_for('welcome'))
    else:
        # Handle login failure
        ...
```

This configuration ensures every request, response, and significant action (like login success or failure) is logged thoroughly, enhancing monitoring and debugging capabilities.

***

## Next Steps

The next phase of this lesson will cover configuring Fluent Bit to forward these logs to Elasticsearch, establishing a centralized logging and monitoring system. This topic will be explored in the subsequent lesson.

Thank you for following along. For more detailed Kubernetes documentation and best practices, check out the [Kubernetes Documentation](https://kubernetes.io/docs/) and related resources.

Happy Deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/2c0792c4-1a21-404f-83e2-75698bc62fe0/lesson/6054679d-c66a-46b4-a0e2-ec01dc9dbb48" />
</CardGroup>


# Instrumenting a Simple Python Application for Logging

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Instrumenting-a-Simple-Python-App-for-Logging/Instrumenting-a-Simple-Python-Application-for-Logging/page

This article covers deploying a Python application with logging, using Fluent Bit and Elasticsearch, and creating dashboards in Kibana for performance monitoring.

In this article, we dive into deploying a front-end Python application with robust logging capabilities. We will demonstrate how user interactions within the application generate logs, how Fluent Bit collects these logs and sends them to Elasticsearch, and how to create insightful dashboards in Kibana. This guide is ideal for developers and engineers who want to monitor application performance and gain valuable insights into user behavior.

## High-Level Architecture Overview

The Login App in this scenario serves two primary audiences:

* **Users** – They interact with the app.
* **Developers** – They maintain and troubleshoot the application using logs and dashboards.

This application is deployed in a Kubernetes environment where Elasticsearch and Kibana are pre-configured. The workflow is as follows:

1. **User Interaction:** When a user interacts with the Login App, it generates logs.
2. **Log Collection:** Fluent Bit collects these logs and forwards them to Elasticsearch.
3. **Data Visualization:** Kibana is used to build dashboards that display the log data, providing insights into app behavior and performance.

<Frame>
  ![The image illustrates the deployment of a login app and Kibana on Kubernetes, showing interactions between a user, an app, Elasticsearch, Kibana, FluentBit, and an engineer.](https://kodekloud.com/kk-media/image/upload/v1752874238/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Instrumenting-a-Simple-Python-Application-for-Logging/kubernetes-login-app-kibana-deployment.jpg)
</Frame>

<Callout icon="lightbulb">
  Each component in this architecture plays a crucial role in ensuring that every user action is logged and analyzed effectively.
</Callout>

## Application Workflow and Logging Process

The following steps detail the end-to-end process:

* **User Interaction:** Each action in the Login App generates a corresponding log entry.
* **Fluent Bit Integration:** Fluent Bit monitors the application logs and collects them.
* **Log Forwarding:** The collected logs are sent to the Elasticsearch cluster where they are stored and indexed.
* **Dashboard Creation:** Developers utilize Kibana to build dashboards and analyze the logs for performance monitoring and troubleshooting.

<Callout icon="triangle-alert">
  Ensure that Fluent Bit is properly configured to parse the logs according to your application's log format to avoid data loss or misinterpretation.
</Callout>

## Demo Walkthrough

In the next section, we will walk through the detailed demo which includes:

* Building and deploying the Login App.
* Integrating Fluent Bit for centralized logging.
* Creating Kibana dashboards for real-time monitoring.

This comprehensive demonstration will provide practical insights into how structured logging can enhance the performance and user experience of your application.

That concludes this article. Thank you for reading, and we look forward to exploring more innovative topics with you soon.

## Additional Resources

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Elasticsearch Reference](https://www.elastic.co/[AWS_SECRET_ACCESS_KEY]/index.html)
* [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/2c0792c4-1a21-404f-83e2-75698bc62fe0/lesson/8fc5c067-55ef-4cb6-a6fc-1dbaac0cab2c" />
</CardGroup>
