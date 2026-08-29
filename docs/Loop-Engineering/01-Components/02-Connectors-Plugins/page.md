# Connectors Plugins

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Components/Connectors-Plugins/page

Describes connectors and plugins that link the Loop to external tools, MCP standard, and security best practices for permissions and secret management

On its own, a loop can only touch the files in front of it. Real work usually lives in external tools — for example, GitHub, Slack, or project trackers. Connectors and plugins are how the loop reaches those tools and participates in real work.

> **lightbulb** Connectors give the Loop a single, focused link to an external tool. Plugins are installable bundles that can contain multiple connectors plus skills and tools. Use connectors for targeted access; use plugins to install a package of capabilities in one step.

Connectors

A connector links the Loop to one external tool. Picture a cable running from the Loop to GitHub, Slack, or a project tracker. Once that link exists, the Loop can read and act in that tool — for example, it can read an open issue, post a message, or check task status.

<Frame>
  <img alt="The image depicts a diagram showing &#x22;The Loop&#x22; connected to GitHub, Slack, and Project Tracker, symbolizing interactions such as reading an issue, posting a message, and checking a task." />
</Frame>

The connector is the bridge that enables those actions.

Plugins

A plugin is an installable bundle. Inside a plugin there can be multiple skills, tools, and connectors packaged together. The distinction is one of scope: a connector is a single link to one tool (one cable), while a plugin is a kit that can include many pieces and be installed in a single step.

<Frame>
  <img alt="The image compares a &#x22;Connector,&#x22; represented by a plug and a link indicating &#x22;One link – One tool,&#x22; with a &#x22;Plug-in,&#x22; which includes skills, tools, and connectors, all installable in one step." />
</Frame>

MCP — Model Context Protocol

Some connectors follow an open (or emerging) standard called MCP — the Model Context Protocol. MCP defines a shared set of rules and message formats for how an AI agent connects to an external tool. In short, it’s a common language for communication between agents and tools.

<Frame>
  <img alt="The image illustrates the concept of a protocol as a set of agreed rules enabling communication between an AI agent and an outside tool through a shared language. It shows an AI agent and an outside tool connected via &#x22;MCP,&#x22; highlighted with &#x22;Agreed rules&#x22; and &#x22;One shared language.&#x22;" />
</Frame>

A helpful analogy is a standard plug, like USB: before a common plug, every device required a unique cable. With a shared shape, any device fits any port. MCP does the same for AI tools: a toolmaker implements one MCP connector, and any agent that speaks MCP can use it. Because of this shared standard, connectors built for one tool can often be adapted to others with little extra effort.

Why connectors and plugins matter

Connectors and plugins give the Loop hands. Without them, the Loop is limited to local files. With connectors and plugins, the Loop can:

* Pull an issue from a tracker.
* Open a pull request on GitHub.
* Send updates to a team chat.

This reach is what lets the Loop participate in real work rather than only edit files locally. More reach, however, increases responsibility.

Security and trust considerations

Only add the connectors you actually need. Each extra link increases the potential surface for errors or misuse. Be deliberate about permissions and secret management.

Bad practice example — storing secrets in source code:

```python theme={null}
