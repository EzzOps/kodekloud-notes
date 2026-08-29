# OpenAI Compatibility for Ollama

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/OpenAI-Compatibility-for-Ollama/page

This guide explains how to use Ollamas compatibility with the OpenAI API for seamless local development and production deployment.

In this guide, we’ll show how Ollama’s seamless compatibility with the OpenAI API lets you build and test LLM-powered applications locally—and then switch to the OpenAI cloud for production with zero code changes. You’ll learn how to configure your environment variables, compare development versus production setups, and follow a real-world workflow.

## Why Use OpenAI Compatibility?

By leveraging the OpenAI client libraries against a local Ollama endpoint, you get:

* Consistent API interface across development and production
* Zero code rewriting when moving to the cloud
* Full control for local testing without incurring API costs

Let’s follow Jane’s journey from local development to production-ready deployment.

![The image illustrates "Jane's Story," showing a progression from "Jane" to "Development" with Ollama, and then to "Production" with OpenAI Library.](https://kodekloud.com/kk-media/image/upload/v1752883670/notes-assets/images/Running-Local-LLMs-With-Ollama-OpenAI-Compatibility-for-Ollama/janes-story-development-production-illustration.jpg)

## 1. Development Environment Setup

In development, point your OpenAI client at Ollama’s REST API. Add these lines to your `.env` file:

```bash theme={null}
