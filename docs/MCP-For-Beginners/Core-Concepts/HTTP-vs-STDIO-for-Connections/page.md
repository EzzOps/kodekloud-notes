# Initialize project and venv (using uv as shown in this guide)
uv init .
uv venv
source .venv/bin/activate
```

You should see output similar to:

```text theme={null}
Initialized project `super-basic-mcp-server` at `/path/to/super-basic-mcp-server`
Using CPython 3.11.13 interpreter at: /opt/homebrew/opt/python@3.11/bin/python3.11
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

Quick command reference

| Purpose                                | Command                     |
| -------------------------------------- | --------------------------- |
| Initialize project & venv (using `uv`) | `uv init .` / `uv venv`     |
| Activate venv                          | `source .venv/bin/activate` |
| Add FastMCP (with CLI extras)          | `uv add mcp[cli]`           |
| Run development server                 | `mcp dev main.py`           |
| Run script directly                    | `python main.py`            |

## Minimal starter main.py

Start with a simple script to validate your environment:

```python theme={null}
# main.py
def main():
    print("Hello from super-basic-mcp-server!")


if __name__ == "__main__":
    main()
```

Run it:

```bash theme={null}
python main.py
```

Expected output:

```text theme={null}
Hello from super-basic-mcp-server!
```

## Adding FastMCP and a simple `add` tool

Install FastMCP (example uses `uv add`):

```bash theme={null}
uv add mcp[cli]
```

Replace `main.py` with a first MCP server that exposes a simple `add` tool:

```python theme={null}
# main.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("add_integers")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two integers and return the sum.

    Args:
        a: First integer
        b: Second integer

    Returns:
        The sum of a and b.
    """
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Run the development server (this opens the Inspector and prints a session token):

```bash theme={null}
mcp dev main.py
```

The server prints a session token and provides a local MCP Inspector UI (by default at `http://localhost:6274`). Open the Inspector and authenticate by appending the query parameter shown in the console, for example:

`http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>#resources`

(When copying, replace `<token>` with the value printed in your console.)

Using the Inspector you can list tools, view tool docstrings (used as descriptions), and call tools. For example:

* Calling `add(3, 5)` returns:

```json theme={null}
{
  "result": 8
}
```

## Adding structured error handling with `divide`

Introduce a small `MCPError` exception and add a `divide` tool that returns structured errors to callers:

```python theme={null}
# main.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("add_integers")

class MCPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """
    Divides two integers.

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        The result of the division.
    """
    if b == 0:
        raise MCPError(code=400, message="Division by zero is not allowed.")
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Run `mcp dev main.py` again. The Inspector now shows both `add` and `divide`. Example responses:

* Successful call `divide(24, 2)`:

```json theme={null}
{
  "result": 12
}
```

* Error case `divide(12, 0)` — the Inspector and client will show the structured error message similar to:

```text theme={null}
Error executing tool divide: [400] Division by zero is not allowed.
```

Validation errors (e.g., passing floats where integers are required) are surfaced by pydantic-style validation messages that indicate the type mismatch and provide guidance.

## Simulating long-running work

Some tools need to perform long-running tasks. Add `long_process` to simulate a multi-step job and show how STDIO behaves with longer processing times.

Warning: writing arbitrary text to stdout while using the STDIO transport can corrupt the MCP message stream. Use logging or the library's streaming/event APIs for progress updates.

<Callout icon="warning">
  Avoid printing arbitrary text to stdout when using the STDIO transport — it can interfere with the MCP protocol and break communication. Use logging or FastMCP's streaming features for progress reporting.
</Callout>

Example `long_process` that uses logging (preferred):

```python theme={null}
# main.py (append or modify as needed)
import time
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def long_process(steps: int) -> str:
    """
    Simulates a long-running process by iterating steps.
    """
    for i in range(steps):
        # Use logging instead of printing to stdout when using STDIO transport.
        logger.info("Processing step %s of %s", i + 1, steps)
        time.sleep(0.1)
    return "Process complete!"
```

Invoke `long_process(10)` from the Inspector to see how the server performs a short job. Increasing `steps` (e.g., `long_process(100)`) may trigger client or server timeouts depending on configured timeouts; timeouts are configurable on the server side.

## Transports and the Inspector

<Callout icon="lightbulb">
  STDIO is convenient for local development and tooling. FastMCP and the MCP Inspector also support other transports (for example, SSE or HTTP) when you need to expose your MCP server to other processes or to a network.
</Callout>

## Adding logging

Enable Python logging to capture server activity in a file and to emit progress or input/output info from tools.

Top-level logging setup:

```python theme={null}
# main.py (top-level additions)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log",
    filemode="a"  # append on each run ('w' to overwrite)
)
logger = logging.getLogger(__name__)
```

Log inputs and outputs within your tools, for example:

```python theme={null}
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    logger.info("Adding %s and %s", a, b)
    result = a + b
    logger.info("Result is %s", result)
    return result
```

After invoking tools via the Inspector, `mcp_server.log` will include entries similar to:

```text theme={null}
2025-07-09 00:25:04,183 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-07-09 00:25:12,229 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-07-09 00:25:12,229 - main - INFO - Adding 5 and 4
2025-07-09 00:25:12,229 - main - INFO - Result is 9
```

## Full consolidated example

A compact `main.py` that combines the pieces:

```python theme={null}
# main.py
from mcp.server.fastmcp import FastMCP
import time
import logging

mcp = FastMCP("add_integers")

class MCPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log",
    filemode="a"
)
logger = logging.getLogger(__name__)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    logger.info("Adding %s and %s", a, b)
    result = a + b
    logger.info("Result is %s", result)
    return result

@mcp.tool()
def divide(a: int, b: int) -> float:
    """
    Divides two integers.

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        The result of the division.
    """
    if b == 0:
        raise MCPError(code=400, message="Division by zero is not allowed.")
    return a / b

@mcp.tool()
def long_process(steps: int) -> str:
    """Simulates a long-running process."""
    for i in range(steps):
        logger.info("Processing step %s of %s", i + 1, steps)
        time.sleep(0.1)
    return "Process complete!"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Wrap-up

What you accomplished in this lesson:

* Exposed functions as MCP tools using `@mcp.tool()`
* Used docstrings for tool descriptions and argument schemas
* Implemented structured errors with `MCPError`
* Simulated long-running tasks and accounted for timeouts
* Added logging to persist server events to a logfile
* Ran and inspected the server locally via the MCP Inspector (STDIO transport)

You can now extend tools to access databases, call LLMs, perform async tasks, or expose your MCP server over other transports (HTTP/SSE) for remote clients.

Links and references

* FastMCP / MCP docs (check your installed package for local docs)
* [Python venv documentation](https://docs.python.org/3/library/venv.html)
* \[MCP Inspector — local UI] — (open `http://localhost:6274` when running `mcp dev`)

Example tool calls and expected outputs

| Tool call          | Expected response                                            |
| ------------------ | ------------------------------------------------------------ |
| `add(3, 5)`        | `{ "result": 8 }`                                            |
| `divide(24, 2)`    | `{ "result": 12 }`                                           |
| `divide(12, 0)`    | Error with message: `[400] Division by zero is not allowed.` |
| `long_process(10)` | `{ "result": "Process complete!" }`                          |

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/a27f1996-5412-4f48-a085-c87d68c51206/lesson/a14e7566-5dbb-42d5-8e11-d7399488cdd2" />
</CardGroup>


# HTTP vs STDIO for Connections

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Core-Concepts/HTTP-vs-STDIO-for-Connections/page

Comparison of STDIO, HTTP, and SSE transports for MCP services, explaining operation, data flow, trade offs, and recommended use cases like local IPC, remote APIs, and streaming

In this lesson we'll compare the three MCP service transports (service types): STDIO, HTTP, and SSE. You’ll learn how each transport works, the typical data flow, and which scenarios make each the best choice—local IPC, remote APIs, or streaming outputs.

<Callout icon="lightbulb">
  Choose a transport based on locality, latency, and streaming needs:

  * Use STDIO for simple local processes and developer workflows.
  * Use HTTP for remote, network-accessible APIs and short atomic requests.
  * Use SSE for server-to-client streaming, e.g., progressive model token delivery.
</Callout>

## STDIO (Standard Input / Standard Output)

STDIO is the simplest IPC mechanism for running an MCP service as a local subprocess or executable. Communication happens over standard input (stdin) and standard output (stdout), with no network layer between the application and the service. Typical uses include CLI tools, local servers, and single-machine batch jobs.

How STDIO works:

* The application launches or connects to a local MCP executable and writes a prompt or request to its stdin.
* The MCP service processes that input and writes the full response to stdout.
* No network transport is involved between the application and the service.

Notes:

* The STDIO process can still access networks or external resources (databases, documents, APIs) if the host machine permits, but other machines cannot directly reach the STDIO stream.
* STDIO is low-overhead and straightforward, making it ideal for development, testing, and single-machine workloads.

Example (conceptual):

```bash theme={null}
