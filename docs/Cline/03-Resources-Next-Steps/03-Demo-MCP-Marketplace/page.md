# Get all castings
castings = get_castings("http://localhost:8000")

# Search for 350 engines
results = search_castings("http://localhost:8000", cid=350)
```

## Typical workflow example

A typical local workflow to run the migration and web interface:

1. Start the API server (example):
   \$ python run.py
2. Start the web interface:
   \$ python flask\_web\_interface/run\_flask.py
3. Check the API docs on the homepage or visit `http://localhost:8000/docs`.

## Conclusion

Automated documentation generation with tools like Cline can:

* Improve code discoverability by inserting standardized docstrings
* Produce user-facing guides (Markdown) that are easy to publish
* Generate or augment API documentation (Swagger/OpenAPI)
* Speed up onboarding and reduce maintenance overhead

In this demo, documentation generation was fast and low-cost (the run cost was about \$0.15), showing this approach is practical for many projects.

Happy documenting!

## Links and references

* [Cline](https://learn.kodekloud.com/user/courses/cline)
* [FastAPI Documentation](https://fastapi.tiangolo.com)
* [OpenAPI / Swagger Overview](https://swagger.io/docs/specification/about/)
* [KodeKloud Learn](https://learn.kodekloud.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cline/module/994745b4-8b52-4c0c-ae6c-1afb232520d7/lesson/0cade788-b9a0-41a0-adad-43ad4587e56b" />
</CardGroup>


# Demo MCP Marketplace

Source: https://notes.kodekloud.com/docs/Cline/Resources-Next-Steps/Demo-MCP-Marketplace/page

Guide to discover, install, and configure MCP servers from the Cline Marketplace, exemplified with Ollama, automating setup, updating settings, and testing tools for seamless integration.

This guide demonstrates how to discover, install, and configure an MCP server from the Cline Marketplace, using the Ollama MCP server as a concrete example. You'll see how Cline integrates external tools as plugins (MCP servers), automates most installation steps, and updates client-side MCP settings so tools become available inside Cline.

Plugins in Cline are MCP servers you can browse and one‑click install from the marketplace.

<Frame>
  <img alt="A dark-themed webpage screenshot titled &#x22;Plugins for Cline&#x22; showing steps to browse and one-click install MCP servers on the left and a plugin marketplace panel on the right listing integrations like Airtable, Google Calendar, and Supabase with &#x22;Install&#x22; buttons." />
</Frame>

Why install MCP servers? A developer can request a new capability (for example, add user authentication), and Cline can orchestrate the end-to-end workflow: research docs, present a plan, implement the feature, manage branching, and update project tracking. The marketplace simplifies adding the MCP servers that expose those capabilities as tools.

<Frame>
  <img alt="A screenshot of a web page titled &#x22;How Cline Can Use MCP Servers&#x22; showing a vertical, numbered workflow (developer request, accessing Notion, researching docs, presenting plan) with icons and short descriptions. The page appears to be part of a product/site that explains a seamless request-to-completion flow." />
</Frame>

Cline’s marketplace includes many types of MCP servers: filesystem tools, browser automation, context helpers, sequential reasoning tools, Git tools, Puppeteer wrappers, fetch wrappers, and more. Browse the tool grid and install the cards you need.

<Frame>
  <img alt="Screenshot of a web marketplace page (Cline MCP Marketplace) showing a grid of tool cards like File System, Browser Tools, Context7, Sequential Thinking, and Git Tools. Each card displays a short description, tags, and star counts." />
</Frame>

## What happens during installation

Below is a concise, step-by-step summary of what Cline automates when installing an MCP server (Ollama shown as an example):

1. Detect an existing Cline MCP settings file to avoid overwriting current servers.
2. Create a local MCP directory if one doesn't already exist.
3. Clone the MCP server repository into that directory.
4. Install dependencies using the repository’s preferred package manager (pnpm), falling back to npm if pnpm is unavailable.
5. Build the server (run the repo’s build script).
6. Add the server entry to Cline’s client MCP settings (JSON).
7. Start or test the server from Cline and verify tools respond.

<Callout icon="lightbulb">
  Cline checks for an existing MCP settings file and will prompt before making changes. Review prompts carefully to avoid accidental overwrites. Approve steps interactively when asked.
</Callout>

### Common shell commands (local example paths)

Run these from a terminal when you need to perform or inspect the same steps manually:

```bash theme={null}
