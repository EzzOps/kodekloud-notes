# Demo Creating Unit Tests for our Project

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Getting-Started-with-Claude-Code/Demo-Creating-Unit-Tests-for-our-Project/page

Creating deterministic pytest unit and integration tests for a METAR reader, mocking network calls and testing Flask endpoints for reliable continuous integration

In this lesson we add deterministic, fast unit and integration tests for the METAR reader application. We'll use pytest to validate METAR decoding logic, mock external network calls to avoid hitting APIs during tests, and exercise Flask endpoints using the Flask test client. The goal is to make tests reliable, easy to run, and useful for continuous integration.

<Frame>
  <img alt="A presentation slide with the title &#x22;Creating Unit Tests for our Project.&#x22; A large &#x22;Demo&#x22; label appears on a dark curved panel on the right." />
</Frame>

Using Claude Code For Beginners' CLI-like slash commands can speed up local development workflows and give helpful tips about the repository layout:

```bash theme={null}
* Welcome to Claude Code!

/help for help, /status for your current setup

cwd: /Users/jeremy/Repos/KodeKloud-METAR-Reader

Tips for getting started:

1. Run /init to create a CLAUDE.md file with instructions for Claude
2. Use Claude to help with file analysis, editing, bash commands and git
3. Be as specific as you would with another engineer for the best results
4. ✓ Run /terminal-setup to set up terminal integration

> Try "how do I log an error?"
? for shortcuts
```

## Test plan (concise)

* Use pytest for unit and integration testing.
* Mock network requests (requests.get) to simulate API responses and errors.
* Unit test METAR decoding functions: wind direction, visibility, clouds, weather phenomena, temperature conversion, edge cases.
* Integration tests to decode complete METAR strings and check structured output.
* Add Flask route tests to verify endpoint responses and error handling.
* Add test-only dependencies to requirements.txt and document test instructions in README.
* Run tests locally and produce coverage reports for CI.

| Test type         | Purpose                                             | Examples                            |
| ----------------- | --------------------------------------------------- | ----------------------------------- |
| Unit tests        | Validate individual decoder functions               | `test_decoder_unit.py`              |
| Integration tests | Verify decoding of full METAR strings               | `test_decoder_integration.py`       |
| Network tests     | Simulate network errors and HTTP failures           | `test_network.py`                   |
| Edge-case tests   | Exercise wrapping values, malformed inputs          | `test_edge_cases.py`                |
| Flask route tests | Ensure endpoints behave for success and error flows | Flask test client + pytest fixtures |

## Unit tests: METAR decoder

Below are cleaned-up unit tests for basic METAR components. These tests focus on pure functions so they remain fast and deterministic.

```python theme={null}
