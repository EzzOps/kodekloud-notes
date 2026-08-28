# Custom Skill Interfaces

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Create-a-Custom-Skill-for-Azure-AI-Search/Custom-Skill-Interfaces/page

Explains Azure AI Search custom skill input and output JSON schemas, required recordId and data structure, plus error and warning patterns for reliable enrichment

Custom skill interfaces for Azure AI Search define how external services communicate with the enrichment pipeline using a strict JSON schema. This article explains the input your custom skill receives, the output it must return, and the optional error/warning patterns that enable robust enrichment and correct mapping back to original records.

Why this matters: Azure AI enrichment relies on exact field names and structure to correlate results. Implementing these schemas correctly ensures your skill’s outputs are routed back to the right document and that partial failures can be handled gracefully.

## Input schema

The enrichment pipeline sends inputs as a JSON object with a top-level values array. Each element in values is a record object with:

* recordId: a unique identifier the pipeline uses to match responses to the originating input.
* data: a property bag (object) containing key/value pairs. Each key is an input field name and the value is the field content (string, number, array, or nested object).

Your skill must accept, parse, and process this exact structure. If any of these keys are missing or renamed, the pipeline cannot map responses back to the original records.

<Frame>
  <img alt="A presentation slide titled &#x22;Custom Skill Interfaces&#x22; showing an &#x22;Input Schema&#x22; panel. It explains that the input schema is an array of records, each with a unique identifier and a data object of key-value pairs." />
</Frame>

Example input JSON:

```json theme={null}
{
  "values": [
    {
      "recordId": "<unique_identifier>",
      "data": {
        "<input1_name>": "<input1_value>",
        "<input2_name>": "<input2_value>"
      }
    },
    {
      "recordId": "<unique_identifier>",
      "data": {
        "<input1_name>": "<input1_value>",
        "<input2_name>": "<input2_value>"
      }
    }
  ]
}
```

<Callout icon="lightbulb">
  Treat the top-level values key as mandatory. The data object is a flexible property bag: fields may be primitive values or nested structures depending on your use case (text extraction, language detection, OCR, etc.).
</Callout>

<Callout icon="warning">
  Your custom API must accept and parse this exact schema. If recordId or the values array are missing or misnamed, the enrichment pipeline will fail to correlate responses to inputs.
</Callout>

## Output schema

Responses from your custom skill must mirror the input format so the pipeline can correlate results to the same recordId values. The required structure:

* values: an array of result objects (one per processed input record).
* recordId: must match the recordId from the corresponding input record.
* data: a property bag containing output fields produced by your skill (for example, enriched text, tags, predictions, or metadata).
* Optional: errors and warnings arrays for per-record reporting.

Including errors/warnings enables the enrichment pipeline and downstream systems to handle partial failures, log issues, and avoid losing traceability.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Custom Skill Interfaces&#x22; with a highlighted &#x22;Output Schema&#x22; panel. The text explains that the output schema defines a custom skill's response structure, keeping the same recordId and including a data object plus optional errors and warnings." />
</Frame>

Example output JSON:

```json theme={null}
{
  "values": [
    {
      "recordId": "<unique_identifier_from_input>",
      "data": {
        "<output1_name>": "<output1_value>"
      },
      "errors": [],
      "warnings": []
    },
    {
      "recordId": "<unique_identifier_from_input>",
      "data": {
        "<output1_name>": "<output1_value>"
      },
      "errors": [],
      "warnings": []
    }
  ]
}
```

## Schema field reference

| Field                | Type   | Required | Purpose                                                                                                              |
| -------------------- | ------ | -------- | -------------------------------------------------------------------------------------------------------------------- |
| values               | array  | Yes      | Top-level container for records.                                                                                     |
| values\[\*].recordId | string | Yes      | Unique identifier passed through unchanged to correlate input and output.                                            |
| values\[\*].data     | object | Yes      | Property bag for inputs (on request) or outputs (on response). Flexible—may contain primitives or nested structures. |
| values\[\*].errors   | array  | No       | Per-record error objects for unrecoverable failures.                                                                 |
| values\[\*].warnings | array  | No       | Per-record warnings for recoverable or informational issues.                                                         |

## Notes and best practices

* Always return the same recordId you received for each record. Changing or omitting it breaks mapping.
* Keep the data property flexible but consistent: define expected output field names in your documentation so downstream skills or indexers know what to consume.
* Use errors for severe failures that prevent producing a valid output for a specific record. Use warnings for recoverable issues or informational messages.
* If your skill batches multiple inputs, ensure your response contains a corresponding entry for each recordId included in the request—even if the entry only contains an errors array.
* Validate incoming payloads early and return well-formed JSON with appropriate HTTP status codes (typically 200 OK with a values array; use errors within values for per-record failures).

## Troubleshooting tips

* If outputs are not appearing in the index or downstream skillset, check that recordId values match exactly (including case).
* Inspect the enrichment pipeline logs and the skill’s response for items in errors or warnings arrays.
* Test your custom skill locally with mock requests following the schema above before wiring it into the enrichment pipeline.

## Summary

* Azure AI Search custom skills use strict input and output JSON schemas exchanged via a top-level values array.
* Each record must include recordId and a data property bag for inputs and outputs.
* Optional errors and warnings enable robust error reporting and partial failure handling.
* Following these formats ensures reliable mapping of enrichment results back to original records and smooth operation within the enrichment pipeline.

References and further reading:

* [Azure Cognitive Search custom skills documentation](https://learn.microsoft.com/azure/search/cognitive-search-custom-skill-interface)
* [Azure Cognitive Search enrichment pipeline overview](https://learn.microsoft.com/azure/search/cognitive-search-enrich-content)

To use a custom skill, add it to an enrichment pipeline's skillset configuration so it can process records during indexing.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/1413da7e-948c-4865-8347-5710a35851a4/lesson/c78f3a35-3e60-408d-a449-c812f579f0e0" />
</CardGroup>
