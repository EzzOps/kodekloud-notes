# Build your first agent

Source: https://notes.kodekloud.com/docs/Google-ADK/Introduction/Build-your-first-agent/page

Tutorial showing how to scaffold and run a minimal Google ADK Python agent with simple tools for time and weather, and how the LLM routes tool calls

In this lesson you'll scaffold and run a minimal Google ADK agent — a "hello world" style example that shows how to:

* scaffold an agent,
* register simple tools,
* and let the LLM decide which tool to call based on natural language.

This step-by-step walkthrough covers creating a Python virtual environment, installing the Google ADK package, scaffolding a starter application, implementing two deterministic tools (get\_current\_time and get\_current\_weather), and running the agent interactively.

<Frame>
  <img alt="A presentation slide that says &#x22;Build Your First Agent&#x22; on the left with a large &#x22;Demo&#x22; label on a dark, curved shape on the right. A small &#x22;© Copyright KodeKloud&#x22; appears in the lower-left corner." />
</Frame>

What we'll do

* Create and activate a Python virtual environment
* Install google-adk
* Scaffold an ADK app
* Add two simple tools
* Run the agent and interact with it

Create and activate a virtual environment (macOS / Linux shown):

```bash theme={null}
