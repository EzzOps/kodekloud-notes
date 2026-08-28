# Python Question 1

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Preparation-Course/Programming/Python-Question-1/page

This article explores simple API testing using Python and the requests module to verify API endpoint functionality through HTTP status codes.

In this article, we will explore how to perform simple API testing using Python. We'll focus on using the popular requests module to verify if an API endpoint is operational by checking its HTTP status code.

## Using the Requests Module for API Testing

The recommended module for this task is the [requests](https://docs.python-requests.org/) module. It allows you to send an HTTP GET request to an API endpoint and retrieve its status code. If the returned status code is 200, it indicates that the API endpoint is functioning properly. Any other status code suggests that there might be an issue with the endpoint.

Below is an example demonstrating the basic usage:

```python theme={null}
import requests

website = "http://example.com/api"  # Replace with your API endpoint
status_code = requests.get(website).status_code
print(f"Status Code: {status_code}")
