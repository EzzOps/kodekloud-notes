# Demo Building Simple MCP Server

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Core-Concepts/Demo-Building-Simple-MCP-Server/page

Guide to build and run a minimal FastMCP MCP server over STDIO, exposing example tools, structured errors, logging, and using the MCP Inspector for local testing.

In this lesson you'll build a minimal MCP (Model Communication Protocol) server using the FastMCP Python library and run it locally with the STDIO transport. The guide shows how to:

* Create a Python virtual environment
* Expose simple tools: `add`, `divide`, and `long_process`
* Return structured errors via a custom `MCPError` exception
* Run and test the server locally with the MCP Inspector
* Add logging to capture server activity

Prerequisite: Python 3.11+ (examples tested with Python 3.11).

Table of contents

* Setting up the project
* Minimal starter `main.py`
* Adding FastMCP and an `add` tool
* Run the dev server and use the Inspector
* Add error handling with `divide`
* Simulate long-running work (`long_process`)
* Transports and stdout warning
* Add logging
* Full consolidated example
* Wrap-up and references

## Setting up the project

Create a project and a virtual environment. This example uses the `uv` helper shown in this guide, but you can substitute with `python -m venv .venv` if preferred.

```bash theme={null}
