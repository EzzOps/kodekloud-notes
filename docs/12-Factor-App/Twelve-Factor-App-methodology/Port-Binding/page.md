# Configure logger for remote logging via Fluentd
logger = sender.FluentSender('app', host='host', port=24224)

# Emit a log event with details
logger.emit('follow', {'from': 'userA', 'to': 'userB'})
```

According to the 11th principle of the [12 Factor App](https://learn.kodekloud.com/user/courses/12-factor-app) methodology, applications should not be responsible for log storage or routing. Instead, all logs should be directed to standard output or written as structured JSON to a local file. This practice allows an external agent to collect and forward logs to a centralized repository, where they can be queried and analyzed efficiently.

Centralized logging solutions like the ELK Stack and Splunk are designed to ingest and process structured log data, making log analysis faster and more effective.

By decoupling the logging mechanism from your application, you ensure that your system remains agile and well-suited for cloud-native and containerized environments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/12-factor-app/module/086a3d2d-be7f-4b05-92ae-1b2e4ab90f6a/lesson/635cc3fc-da70-4d2b-822e-0d63f0e17323" />
</CardGroup>


# Port Binding

Source: https://notes.kodekloud.com/docs/12-Factor-App/Twelve-Factor-App-methodology/Port-Binding/page

This article explains port-binding in Flask applications, highlighting how to access them and the importance of unique ports in multi-service environments.

Accessing our Flask web application is as straightforward as entering the URL along with the port number into your web browser. In our example, the application runs on port 5000. When accessed successfully, a welcome message along with a visitor count is displayed.

<Frame>
  ![A browser window displays a message: "Welcome to KODEKLOUD! Visitor Count: 10" on a localhost server.](https://kodekloud.com/kk-media/image/upload/v1752856837/notes-assets/images/12-Factor-App-Port-Binding/frame_10.jpg)
</Frame>

By default, the Python Flask framework listens on port 5000. However, when running multiple instances of the application on the same server, each instance can bind to a unique port (such as 5001, 5002, etc.). In multi-service environments, different services are assigned distinct ports—for instance, Redis typically operates on port 6379.

<Frame>
  ![The image shows a network diagram with four nodes labeled 5001, 5000, 5002, and 6379, featuring globe and database icons.](https://kodekloud.com/kk-media/image/upload/v1752856838/notes-assets/images/12-Factor-App-Port-Binding/frame_30.jpg)
</Frame>

Binding an application to a specific port allows it to export HTTP as a service and listen directly for incoming requests. In contrast to traditional web applications that depend on an external web server, the 12-Factor App methodology encourages creating self-contained applications with built-in web servers. This design approach not only simplifies deployment but also enhances scalability.

<Callout icon="lightbulb">
  For environments that host multiple services simultaneously, ensuring each service is bound to a unique port is crucial for preventing conflicts and maintaining smooth communication between services.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/12-factor-app/module/086a3d2d-be7f-4b05-92ae-1b2e4ab90f6a/lesson/c1850baa-bddf-4f55-977c-cb3c9234ee15" />
</CardGroup>
