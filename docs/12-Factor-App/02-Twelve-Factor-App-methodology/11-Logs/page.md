# Logs

Source: https://notes.kodekloud.com/docs/12-Factor-App/Twelve-Factor-App-methodology/Logs/page

This article explores the logging mechanism of an application, detailing its importance for monitoring, troubleshooting, and various storage approaches.

In this article, we explore the logging mechanism used by our application and how it handles various output events like server startup, port listening, HTTP requests, and error reporting. Logs are crucial for monitoring system activities and troubleshooting issues.

When the application starts, it produces logs detailing the server startup sequence, including server addresses and port numbers. Every HTTP request served is recorded, as illustrated in the example below.

```Python theme={null}
* Serving Flask app 'main'
* Debug mode: on
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:8080
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: 547-019-069
127.0.0.1 - - [25/Feb/2023 16:19:24] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2023 16:19:24] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [25/Feb/2023 16:19:26] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2023 16:19:27] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2023 16:19:27] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2023 16:19:27] "GET / HTTP/1.1" 200 -
```

These logs not only capture standard operations of the server but also record errors and other significant events, making them indispensable for diagnosing issues when failures occur.

## Logging Storage Approaches

Traditionally, applications write logs to local files. However, in containerized environments, this method presents challenges:

* **Volatility:** A container may terminate at any time, causing the loss of local log files.
* **Inflexibility:** Tying your logging system to a specific file system location restricts scalability and portability.

An alternative is to send logs to a centralized logging server using systems such as Fluentd, the ELK Stack, or Splunk. While centralized logging enhances management and analysis, directly integrating your application with a specific logging provider is not recommended.

> **lightbulb** Always design your application so that it remains agnostic to any logging backend, which improves flexibility, scalability, and ease of maintenance.

## Example: Sending Logs via Fluentd

The following Python code demonstrates how logs can be sent to a Fluentd logging server. Note, however, that this pattern directly couples your application to Fluentd, which is discouraged:

```python theme={null}
from fluent import sender
