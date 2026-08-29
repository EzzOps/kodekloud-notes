# Structured Outputs

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Features/Structured-Outputs/page

Structured outputs enable OpenAI models to generate data in formats like JSON, CSV, or XML for easy integration and processing in applications and workflows.

Structured outputs let OpenAI models generate data in predefined schemas—such as JSON, CSV, or XML—making responses machine-readable, actionable, and easily integrated into applications, databases, or workflows. This article covers why structured outputs matter, their key benefits, common formats, and best practices for implementation.

## Why Structured Outputs Matter

Structured outputs transform AI-generated text into formats that downstream systems can parse and process automatically. By specifying a consistent schema, you ensure responses are:

* **Interpretable:** Downstream services understand each field.
* **Actionable:** Applications can trigger workflows based on parsed values.
* **Integrable:** Easily imported into databases, APIs, or third-party tools.

![The image lists three crucial aspects for ensuring generated responses: interpretable, actionable, and integrable.](https://kodekloud.com/kk-media/image/upload/v1752879017/notes-assets/images/Introduction-to-OpenAI-Structured-Outputs/crucial-aspects-generated-responses.jpg)

## Key Benefits of Structured Outputs

| Benefit              | Description                                                                      |
| -------------------- | -------------------------------------------------------------------------------- |
| Machine-readable     | Formats like JSON or CSV are parsed automatically without manual editing.        |
| Flexible integration | Feed structured data into forms, dashboards, or hardware control systems.        |
| Actionable data      | Populate CRM records, process orders, or trigger notifications programmatically. |

![The image lists three key factors: improving machine readability, flexibility for integration, and actionable data. It has a dark background with colored bars next to each factor.](https://kodekloud.com/kk-media/image/upload/v1752879019/notes-assets/images/Introduction-to-OpenAI-Structured-Outputs/key-factors-machine-readability-integration-data.jpg)

> **lightbulb** Defining your schema clearly in the prompt is the first step toward reliable, structured responses. Always include an example output to guide the model.

### Example: Extracting Calendar Events

The following Python snippet uses Pydantic models with the OpenAI Python client to parse a chat completion into a structured `CalendarEvent` object:

```python theme={null}
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event)
```

## What Are Structured Output Formats?

Structured outputs follow a schema—such as JSON, CSV, or XML—so they can be consumed directly by applications, APIs, or databases, eliminating the need for complex post-processing.

![The image is a slide titled "What Are Structured Outputs?" It lists examples like JSON, CSV, XML, mentions that outputs are machine-readable, and can directly integrate with applications, APIs, and databases.](https://kodekloud.com/kk-media/image/upload/v1752879020/notes-assets/images/Introduction-to-OpenAI-Structured-Outputs/structured-outputs-json-csv-xml.jpg)

### JSON for API Integration

JSON is a lightweight, human-readable data format widely used in web APIs. It’s ideal for real-time data exchange between clients and servers.

In a real estate chatbot, when a user requests property details, the backend can return structured JSON. The chatbot then displays fields like address, price, and specifications:

![The image is a slide titled "JSON – A common Output for API Integration," explaining JSON's use in API integration, with an example of a real estate chatbot providing property details and connecting to a backend database.](https://kodekloud.com/kk-media/image/upload/v1752879021/notes-assets/images/Introduction-to-OpenAI-Structured-Outputs/json-api-integration-chatbot-example.jpg)

Example JSON output for a property listing:

```json theme={null}
{
  "property_listings": {
    "address": "123 Main St Anytown, USA",
    "price": 350000,
    "number_of_bedrooms": 4,
    "number_of_bathrooms": 3
  }
}
```

### CSV for Data Reports

CSV is the go-to format for tabular data and reports that can be imported into spreadsheets or data warehouses. It’s commonly used in financial reporting, inventory management, and sales analysis.

Example CSV output for a sales report:

```csv theme={null}
product_name,units_sold,revenue
Smartphone,250,125000
Laptop,150,225000
Smartwatch,500,75000
```

## Best Practices for Structured Outputs

1. **Define the schema in your prompt.**\
   Clearly state “Output must be valid JSON” or “Return CSV rows only.”
2. **Validate generated data.**\
   Use a JSON schema validator or CSV linter to catch format errors.
3. **Fine-tune for consistency.**\
   For complex or domain-specific schemas, fine-tune the model on representative examples.

![The image outlines three best practices: clearly defining the output structure, validating generated outputs, and fine-tuning for consistency.](https://kodekloud.com/kk-media/image/upload/v1752879022/notes-assets/images/Introduction-to-OpenAI-Structured-Outputs/best-practices-output-structure-validation.jpg)

> **triangle-alert** Always validate outputs before integrating into production systems. Unverified data can lead to downstream errors or security risks.

## References

* [OpenAI Python Library](https://github.com/openai/openai-python)
* [Pydantic Documentation](https://docs.pydantic.dev/)
* [JSON Schema Validation](https://json-schema.org/)
* [CSV Linter Tools](https://csvlint.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/42afe984-cd3e-4b3c-b1e0-8e9093f57a63/lesson/7f3bb91d-e7bf-417e-8999-354386f397ec)
