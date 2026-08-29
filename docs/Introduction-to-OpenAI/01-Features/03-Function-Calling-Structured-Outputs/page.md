# Function Calling Structured Outputs

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Features/Function-Calling-Structured-Outputs/page

This article explains how to use structured outputs with the OpenAI API for consistent, machine-readable responses.

Structured outputs ensure your application receives well-defined, machine-readable responses every time. By enforcing formats such as JSON, CSV, or custom Pydantic models, you gain:

| Benefit           | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| Type Safety       | Guarantees fields are present and correctly typed             |
| Explicit Refusals | Model clearly indicates when it can’t comply                  |
| Simpler Prompting | Remove guesswork—just specify the format                      |
| Exact Formats     | Enforce JSON, CSV, or any structure your application requires |

***

## 1. Structured Outputs with Pydantic

Define a Pydantic model for your desired schema and instruct the API to parse directly into that model.

```python theme={null}
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user",   "content": "Alice and Bob are going to a science fair."}
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event)
