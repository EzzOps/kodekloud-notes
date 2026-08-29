# test_decoder_unit.py
"""Test suite for the METARDecoder class."""
from metar_decoder import METARDecoder

class TestMETARDecoder:
    def setup_method(self):
        self.decoder = METARDecoder()

    def test_get_wind_direction_text(self):
        assert self.decoder.get_wind_direction_text(180) == 'south'
        assert self.decoder.get_wind_direction_text(270) == 'west'
        assert self.decoder.get_wind_direction_text(45) == 'northeast'
        assert self.decoder.get_wind_direction_text(225) == 'southwest'

    def test_decode_visibility(self):
        """Test visibility decoding from METAR format."""
        assert self.decoder.decode_visibility('10SM') == '10+ miles visibility'
        assert self.decoder.decode_visibility('5SM') == '5 miles visibility'
        assert self.decoder.decode_visibility('1SM') == '1 mile visibility'
```

## Integration-style test for a complete METAR

Integration tests exercise the decoder end-to-end for a full METAR line. These validate structured output keys and human-readable detail fields.

```python theme={null}
# test_decoder_integration.py
from metar_decoder import METARDecoder

class TestMETARDecodingIntegration:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.decoder = METARDecoder()

    def test_decode_complete_metar_clear_weather(self):
        """Test decoding a complete METAR with clear weather."""
        metar = "KHIO 061853Z 27008KT 10SM CLR 22/16 A3012"
        result = self.decoder.decode_metar(metar)

        assert result['details']['station'] == 'KHIO'
        assert 'Observed at 18:53Z on day 06' in result['details']['time']
        assert 'Wind from the west at 8 knots' in result['details']['wind']
        assert result['details']['visibility'] == '10+ miles visibility'
```

## Network-dependent tests: mocking requests

Network-dependent behavior is tested by mocking requests.get and forcing exceptions or specific response behavior. Use pytest monkeypatch or unittest.mock for predictable tests.

```python theme={null}
# test_network.py
from unittest import mock
from requests.exceptions import RequestException, HTTPError
from app.network import fetch_metar  # hypothetical function

def test_fetch_metar_network_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise RequestException("Network error")
    monkeypatch.setattr('requests.get', fake_get)
    result = fetch_metar('KHIO')
    assert result is None  # or assert expected fallback behavior

def test_fetch_metar_http_error(monkeypatch):
    mock_response = mock.Mock()
    mock_response.raise_for_status.side_effect = HTTPError("HTTP 404")
    monkeypatch.setattr('requests.get', lambda *a, **k: mock_response)
    result = fetch_metar('INVALID')
    assert result is None  # or assert expected fallback behavior
```

## Edge-case tests

Include tests for input wrapping and unusual formats. These ensure the decoder tolerates out-of-range values and uncommon METAR encodings.

```python theme={null}
# test_edge_cases.py
from metar_decoder import METARDecoder

def test_wind_direction_wrapping():
    decoder = METARDecoder()
    # Values outside 0-359 should wrap to a valid direction
    assert decoder.get_wind_direction_text(361) == 'north'
    assert decoder.get_wind_direction_text(-1) == 'north'

def test_unusual_visibility_values():
    decoder = METARDecoder()
    # Ensure parser handles unusual formats like "M1/4SM" (less than 1/4 SM)
    assert isinstance(decoder.decode_visibility('M1/4SM'), str)
```

## Test dependencies

Add the test runner and helper libraries to your requirements. Lock versions as needed for reproducibility.

```text theme={null}
requests==2.31.0
pytest==7.4.3
pytest-mock==3.11.0
```

Install dependencies and run tests:

```bash theme={null}
pip3 install -r requirements.txt
python3 -m pytest test_decoder_unit.py test_decoder_integration.py test_network.py -v
```

If tests fail, iterate on either the tests or the implementation. Example fixes typically discovered during test-driven debugging include:

* Use requests.exceptions.HTTPError and RequestException for mocked errors.
* Normalize negative and out-of-range wind-direction inputs.
* Return singular "mile" for 1SM visibility results.
* Enhance cloud parsing to support multiple cloud layers.
* Make weather-phenomena ordering idempotent and deterministic.

## Coverage

Use pytest-cov to report coverage and identify untested logic paths:

```bash theme={null}
python3 -m pytest test_app.py --cov=app --cov-report=term-missing
```

## Typical Git workflow for tests

Commit and push your test files and README changes as part of feature branches:

```bash theme={null}
git add test_app.py requirements.txt README.md
git commit -m "Add tests and README updates for testing"
git push
```

## README updates: add a Testing section

Include a concise Testing section in README.md that explains how developers run the suite locally and what mocks or fixtures to expect.

```markdown theme={null}
## Testing

- Install test dependencies:
  pip3 install -r requirements.txt

- Run tests:
  python3 -m pytest -v

- Run tests with coverage:
  python3 -m pytest --cov=app --cov-report=term-missing

Notes:
- Network calls are mocked in tests. No external API calls should be made during the test run.
- Flask endpoints are tested with the Flask test client and pytest fixtures.
```

> **lightbulb** Run tests in a virtual environment to keep dependencies isolated:
  python3 -m venv .venv && source .venv/bin/activate
  Then install the requirements and run pytest.

## Verification checklist

* Tests cover decoding of METAR components (wind, visibility, clouds, weather phenomena, temperature).
* Integration tests validate decoded outputs for realistic METAR examples.
* Network layer is tested with mocks for successful responses, HTTP errors, and network exceptions.
* Flask routes are tested for both normal and error flows using the Flask test client.
* Edge cases (malformed input, extreme values, missing data) are included.
* Tests are run with coverage to identify untested areas.

This testing strategy yields a maintainable, fast test suite that protects the METAR decoder from regressions and helps ensure correct aviation semantics. Review generated tests to ensure they assert correct behavior (not just the current implementation) and update the decoder as needed.

## Links and references

* [pytest documentation](https://docs.pytest.org/en/stable/)
* [requests documentation](https://docs.python-requests.org/en/latest/)
* [Flask documentation](https://flask.palletsprojects.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/e36fd287-dee2-4916-a919-953391788143/lesson/cdd241fb-994a-452a-87d4-f78d69704606)


# Demo Environment and Configuration Management

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Getting-Started-with-Claude-Code/Demo-Environment-and-Configuration-Management/page

Guide to Claude Code configuration and environment management, covering settings scopes and locations, secret protection, CLAUDE.md project memory, and the claude CLI for inspecting and editing settings.

This guide explains Claude Code's configuration and environment management: where settings live, how project and personal settings differ, how to protect secrets, how to use the CLAUDE.md memory file to give the assistant project context, and how to use the claude CLI for quick configuration checks and edits. Follow the examples to secure sensitive data and make team-wide settings consistent.

## Quick overview: settings types and typical uses

| Settings Type        | Scope                 | Typical Path(s)                                                                                                                                                                                 | Use Case                                                                                            |
| -------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| User-level           | Single user / machine | macOS/Linux: `~/.claude/settings.json`<br />Windows: `C:\Users\<YourUser>\AppData\Roaming\ClaudeCode\settings.json`                                                                             | Personal preferences (editor, telemetry opt-in, UI flags). Not usually checked into source control. |
| Project-level        | Repository-scoped     | `<repo>/.cloud/settings.json` or `<repo>/.claude/settings.json`                                                                                                                                 | Team-shared rules, tool permissions, environment overrides. Committed to repo.                      |
| Local (untracked)    | Developer override    | `<repo>/settings.local.json` (gitignored)                                                                                                                                                       | Personal experiments, local tokens, per-developer preferences.                                      |
| Managed / Enterprise | Organization-managed  | macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`<br />Linux/WSL: `/etc/claude-code/managed-settings.json`<br />Windows: `C:\ProgramData\ClaudeCode\managed-settings.json` | Centrally enforced policies for telemetry, tool access, denied paths.                               |

***

## User-level settings

User preferences are kept in a user settings file. Examples:

macOS / Linux:

```bash theme={null}
~/.claude/settings.json
```

Windows (roaming profile):

```text theme={null}
C:\Users\<YourUser>\AppData\Roaming\ClaudeCode\settings.json
```

A minimal example:

```json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "feedbackSurveyState": {
    "lastShownTime": 1754343213656
  }
}
```

Edit this file with your preferred editor. If `code` (VS Code CLI) isn't installed on macOS you may see:

```bash theme={null}
jeremy@MACSTUDIO KodeKloud-METAR-Reader % code ~/.claude/settings.json
zsh: command not found: code
