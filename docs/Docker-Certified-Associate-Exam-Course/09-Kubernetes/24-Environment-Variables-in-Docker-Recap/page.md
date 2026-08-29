# Environment Variables in Docker Recap

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Environment-Variables-in-Docker-Recap/page

This article explains how to manage environment variables in Docker for Flask applications to enhance configuration flexibility and security.

Modern application development favors separating configuration from code. By using environment variables—especially within Docker containers—you can adhere to [The Twelve-Factor App](https://12factor.net/) methodology and deploy more flexibly.

## Table of Contents

1. [Why Use Environment Variables?](#why-use-environment-variables)
2. [Step 1: Read Environment Variables Locally](#step-1-read-environment-variables-locally)
3. [Step 2: Pass Variables into Docker](#step-2-pass-variables-into-docker)
4. [Docker Commands Reference](#docker-commands-reference)
5. [Further Reading](#further-reading)

***

## Why Use Environment Variables?

Hardcoding configuration values (such as colors, database URLs, or API keys) leads to brittle deployments and requires code changes for every tweak. Environment variables allow you to:

* Decouple code from deployment details
* Support multiple environments (dev, staging, prod) without modifying source
* Secure sensitive data outside of version control

> **lightbulb** Using environment variables is a best practice for twelve-factor compliant apps.

***

## Step 1: Read Environment Variables Locally

Below is a simple Flask application (`app.py`) that reads `APP_COLOR` from the environment, defaulting to `"red"` if unset.

```python theme={null}
import os
from flask import Flask, render_template

app = Flask(__name__)
