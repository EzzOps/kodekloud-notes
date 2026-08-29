# Minimal fake directory and service status for local testing
_FAKE_USER_DIRECTORY: Dict[str, Dict[str, Any]] = {}

_FAKE_SERVICE_STATUS: Dict[str, str] = {
    "email": "operational",
    "vpn": "degraded",
    "gitlab": "outage",
    "wifi": "operational",
}
```

High-level test flows to capture

* Locked account flow:
  * Agent should call `lookup_user` and detect a locked account.
  * Agent should inform the user the account is locked and offer to open a ticket.
* VPN outage flow:
  * Agent should call `check_service_status`.
  * If the service is degraded or in outage for multiple users, create a high-impact ticket.

Capture these two flows as golden sessions in the ADK web UI, then evaluate them against two built-in metrics: `tool_trajectory_avg_score` and `response_match_score`.

Metrics summary

| Metric                       | What it measures                                          | Example threshold |
| ---------------------------- | --------------------------------------------------------- | ----------------- |
| tool\_trajectory\_avg\_score | Correct tools called in the correct order and arguments   | 1.0               |
| response\_match\_score       | Similarity of the final response to the expected response | 0.8               |

Example UI session (condensed)

* User: "My email says my account is locked. My email is [carol@example.com](mailto:carol@example.com)"

* Desired agent: "I see that your account [carol@example.com](mailto:carol@example.com) is indeed locked. To unlock your account, you'll need to contact IT directly. Would you like me to open a ticket for this issue?"

* User (VPN case): "My whole team can't use the VPN this morning. We're all blocked. My email is [alice@example.com](mailto:alice@example.com)"

* Desired agent: "I've checked the VPN service status and it appears degraded. Since this is affecting your team, I can open a ticket. Would you like me to do that?"

Create an eval set in the UI (example id/name: `helpdesk_core_flows`) and add these captured sessions.

Configuring thresholds via JSON
Create folder `helpdesk_agent/evals` and add `test_config.json` to tweak pass/fail thresholds:

```json theme={null}
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

The JSON controls what counts as PASS for each metric.

Install evaluation dependencies

<Callout icon="lightbulb">
  If you get errors like "ModuleNotFoundError: No module named 'rouge\_score'", install the ADK eval extras which include text-similarity dependencies:

  pip install "google-adk\[eval]"

  This pulls in packages used by the evaluator for response similarity metrics.
</Callout>

Running evaluations from the ADK web UI

* Create an eval set (e.g., `helpdesk_core_flows`).
* Add the captured sessions to that eval set.
* Configure thresholds inline or reference your `test_config.json`.
* Click "Run evaluation" to see detailed results: expected vs. actual tool calls and response similarity scores.

Common CLI evaluation workflow

1. Ensure eval dependencies are installed:

```bash theme={null}
(.venv) $ pip install "google-adk[eval]"
```

2. Run the ADK web server if you want the UI:

```bash theme={null}
(.venv) $ adk web
```

3. Run evaluations programmatically with `adk eval`. Provide your agent module path, the evalset file, and the config file:

```bash theme={null}
(.venv) $ adk eval \
  helpdesk_agent \
  helpdesk_agent/helpdesk_core_flows.evalset.json \
  --config_file_path=helpdesk_agent/evals/test_config.json \
  --print_detailed_results
```

Make sure `helpdesk_agent` is the importable agent module/directory.

Sample CLI output (condensed)

```text theme={null}
Eval Set Id: helpdesk_core_flows
Eval Id: casef6b2f7
Overall Eval Status: FAILED
---------------------------------------------------------------
Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0
---------------------------------------------------------------
Metric: response_match_score, Status: FAILED, Score: 0.6391, Threshold: 0.8
---------------------------------------------------------------
Invocation Details:
- Prompt: My email says my account is locked. My email is carol@example.com
- Expected response: I see that your account carol@example.com is indeed locked. To unlock your account, you will need to contact IT directly. Would you like me to open a ticket for this issue?
- Actual response: It looks like your account, carol@example.com, is indeed locked. You'll need IT to unlock it for you. Would you like me to open a ticket for this issue?
- Expected tool calls: lookup_user(email=carol@example.com)
- Actual tool calls: lookup_user(email=carol@example.com)
```

Interpreting results

* Trajectory passed: the expected tool was called in the correct order.
* Response similarity failed: the similarity score (\~0.639) did not meet the 0.8 threshold.

<Callout icon="warning">
  LLMs are non-deterministic: a case that passes once may fail later. If you see flakiness, try multiple runs, relax thresholds temporarily, or increase robustness by improving prompts and tool grounding.
</Callout>

Using the CLI in automated workflows

* `adk eval` supports flags for config files, eval storage URIs, and detailed printing:
  * `--config_file_path` — JSON criteria file.
  * `--eval_storage_uri` — where to store eval results (e.g., `gs://bucket/...`).
  * `--print_detailed_results` — prints the full invocation result to the console.
* Use CI jobs or nightly runs to detect regressions over time.

Handling common issues and tuning guidance

* If an eval fails, start with the prompt and tool instructions — improving the initial prompt often yields the best gains.
* Lower thresholds to get passing CI quickly, but prioritize improving the underlying prompts and tool grounding to achieve reliable results.
* Add more golden-path and edge cases to your eval sets to cover real-world variations.

Automating collection and storage of results

* Evaluator invocation objects include:
  * Expected and actual tool calls and their arguments,
  * Expected and actual final responses,
  * Per-invocation metric scores.
* Ingest these objects into a database or CI artifact store for nightly regressions or pre-release checks.

Agent orchestration & schema snippets
Root agent configuration (instruction and model selection):

```python theme={null}
root_agent = Agent(
    model='gemini-2.5-flash',
    name="helpdesk_root_agent",
    description=(
        "Smart IT Helpdesk assistant that troubleshoots common IT issues "
        "using clarifying questions and internal tools."
    ),
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n"
        "\n"
        "You are running inside a multi-turn session. ADK will give you the full "
        "conversation history each time, so you should remember what has already "
        "been asked and answered.\n"
        "\n"
        "=== OVERALL GOAL ===\n"
        "- Help the user troubleshoot issues with email, VPN, GitLab, Wi-Fi and similar services.\n"
        "- When appropriate, look up their account and check the status of backend services.\n"
        "- Explain what steps the user should take and offer to open a support ticket when needed.\n"
    ),
)
```

Minimal tool implementation pattern:

```python theme={null}
def lookup_user_impl(email: str) -> Dict[str, Any]:
    """Look up a user in the internal directory.

    Args:
        email: The user's work email address.

    Returns:
        dict: A result object with:
            - status: 'success' or 'error'
            - user: user details if found
            - error_message: explanation when status='error'
    """
    user = _FAKE_USER_DIRECTORY.get(email.lower())
    if not user:
        return {"status": "error", "error_message": "User not found", "user": None}
    return {"status": "success", "user": user}
```

What we built in this lesson

* A smart IT helpdesk assistant that:
  * Troubleshoots email, VPN, GitLab, and Wi‑Fi issues,
  * Looks up users and service status with tools,
  * Creates structured tickets using a `Ticket` schema,
  * Uses evaluation sets to guard against regressions.

Example eval set fragment

```json theme={null}
{
  "eval_set_id": "helpdesk_core_flows",
  "name": "helpdesk_core_flows",
  "eval_cases": [
    {
      "eval_id": "casee4c486",
      "conversation": [
        {
          "invocation_id": "e-c5ca4cfa-9f76-48bb-8f9b-28ea39475115",
          "user_content": {
            "parts": [
              {
                "text": "My email says my account is locked. My email is carol@example.com"
              }
            ],
            "role": "user"
          },
          "final_response": {
            "parts": [
              {
                "text": "I see that your account carol@example.com is indeed locked..."
              }
            ]
          }
        }
      ]
    }
  ]
}
```

Next steps and recommendations

* Iterate on your instruction prompt to be explicit about which tools to call and when.
* Add more golden-path and edge cases to your eval set.
* Store evaluation results in cloud storage or a database to track trends over time.
* If your helpdesk grows, split responsibilities across smaller agents (triage, ticketing, knowledge) for clearer eval boundaries.

References and further reading

* Python basics course: [Python Basics](https://learn.kodekloud.com/user/courses/python-basics)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-adk/module/672589ad-758d-4e70-8408-bd4bd4409388/lesson/3b622c33-58bf-4e6d-8434-54011a3d934f" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/google-adk/module/672589ad-758d-4e70-8408-bd4bd4409388/lesson/905ed00f-f56b-4de6-82a5-fd03fd176ffd" />
</CardGroup>


# Implementing Ticket Schemas

Source: https://notes.kodekloud.com/docs/Google-ADK/Deploying-and-Operating-ADK-Agents/Implementing-Ticket-Schemas/page

Refactoring an agent demo to use Pydantic ticket schemas and typed tools so the agent orchestrates while tools handle validation, lookups, and ticket creation.

In this lesson we'll refactor the single-file demo into a small, well-structured project and implement a typed, validated ticket workflow using Pydantic. The goal is to keep the agent focused on orchestration while tools implement domain logic and validation.

<Frame>
  <img alt="A presentation slide titled &#x22;Implementing Ticket Schemas&#x22; with a dark curved shape on the right containing the word &#x22;Demo.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

Goals for this lesson:

* Create a `schemas` package with a Pydantic `Ticket` model.
* Move domain logic into a `tools` package.
* Add a typed `create_ticket` tool that returns a validated, structured ticket.
* Keep the agent orchestrator thin—use tools for lookup, checks, and ticket creation.

File layout

| Path                      | Purpose                                                                       |
| ------------------------- | ----------------------------------------------------------------------------- |
| `schemas/ticket.py`       | Pydantic Ticket model defining the canonical ticket shape                     |
| `tools/helpdesk_tools.py` | Implementations: user lookup, service status check, and ticket creation tools |
| `agent.py`                | Agent setup and FunctionTool wrappers that call the tools                     |

## 1) Ticket schema (Pydantic)

Use a Pydantic model to enforce a consistent ticket shape on the Python side. The LLM does not need to produce the exact JSON; instead, the agent will call a tool which builds and validates the Pydantic model, returning a reliable dict.

Example `schemas/ticket.py`:

```python theme={null}
