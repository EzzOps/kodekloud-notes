# How to Generate API Key Securely

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/How-to-Generate-API-Key-Securely/page

This guide explains how to securely generate and use your OpenAI API key in Python using environment variables.

Managing sensitive credentials like your OpenAI API key with environment variables helps you avoid hard-coding secrets in your source code. In this guide, you’ll learn how to:

* Create an isolated Python environment
* Install required packages
* Store your API key safely
* Write and run a simple Python script using the OpenAI client

## 1. (Optional) Create and Activate a Virtual Environment

Isolating dependencies prevents conflicts across projects.

```bash theme={null}
