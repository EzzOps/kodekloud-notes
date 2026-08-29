# LLM Response

Source: https://notes.kodekloud.com/docs/LangChain/Building-Blocks-of-LLM-Apps/LLM-Response/page

Guidance on requesting, parsing, validating, and normalizing LLM outputs with examples for date handling, schema enforcement, and security to ensure reliable and safe consumption

LLMs return text that your application must often parse and validate before use. The model can provide plain strings, semi-structured text, or strictly structured formats (JSON, CSV, XML). Because LLM outputs can vary in formatting and content, you should design a robust parsing and validation layer that coerces or rejects unexpected formats and normalizes values (dates, numbers, enums) before further processing.

For example, when an LLM supplies a date string, you must parse and validate that string so it can be converted into a proper date object for arithmetic. The more explicit you are about the expected output schema in the prompt, the easier and safer parsing becomes.

<Frame>
  <img alt="The image shows a calendar icon in the center with symbols representing user, date, response options, and a large language model (LLM) surrounding it." />
</Frame>

After receiving the LLM response, apply these steps in order:

* Detect the format (plain text vs. requested JSON/CSV/XML).
* Validate the structure (required keys, value types, allowed enums).
* Normalize values (parse ISO-8601 dates, trim whitespace, coerce numbers).
* Apply domain-specific checks (ranges, cross-field consistency).
* Fail fast or fallback to safe defaults when validation fails.

> **lightbulb** Always ask the LLM for a clear output format (for example, `JSON` with explicit keys). Validate and sanitize the returned data before using it in production. Consider schema validation libraries (e.g., `pydantic`, `jsonschema`) for reliable enforcement.

Example: parsing an ISO-8601 date string returned by the LLM and computing the difference in days (Python)

```python theme={null}
from datetime import date
