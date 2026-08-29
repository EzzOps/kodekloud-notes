# What Are API Keys and How to Protect Them

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Pre-Requisites/What-Are-API-Keys-and-How-to-Protect-Them/page

This article explains API keys, their functionality, and best practices for generating and protecting them.

APIs rely on secure authentication to ensure only authorized clients can access your services. In this guide, you’ll learn what API keys are, how they work, and best practices for generating and safeguarding them.

## Understanding API Keys

An **API key** is a unique token that identifies and authorizes a client application when calling your API endpoints. By issuing API keys, you can:

| Benefit            | Description                                                       |
| ------------------ | ----------------------------------------------------------------- |
| Access Control     | Restrict who can invoke your API and tailor permissions per key.  |
| Usage Tracking     | Monitor request volume and set rate limits to prevent abuse.      |
| Scoped Permissions | Assign different access levels (read, write, admin) for each key. |

### How API Keys Work

1. A client includes the API key in the request header or query string.
2. Your server validates the key against its database.
3. If valid, the request is processed; otherwise, it’s rejected with an HTTP 401 or 403.

## Example: Calling the OpenAI API in Python

Here’s a simple Python snippet using the official OpenAI client library:

```python theme={null}
from openai import OpenAI
import os
