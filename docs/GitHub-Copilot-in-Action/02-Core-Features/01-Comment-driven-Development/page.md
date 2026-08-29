# Comment driven Development

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Core-Features/Comment-driven-Development/page

Explains comment-driven development using descriptive comments to generate scaffolding, validation, data pipelines, and tests, then review and refine generated code for correctness.

In this lesson, we explore comment-driven development: writing concise, descriptive comments to generate scaffolding — classes, validation, data-processing pipelines, and unit tests — then refining and validating the generated outputs. This workflow accelerates development for repetitive boilerplate while keeping you focused on high-value algorithmic and edge-case logic.

<Frame>
  <img alt="A presentation slide with the title &#x22;Comment-driven development&#x22; on the left and the word &#x22;Demo&#x22; highlighted on a dark curved shape on the right. A small copyright notice &#x22;© Copyright KodeKloud&#x22; appears in the bottom left." />
</Frame>

Use comment-driven generation to create initial scaffolding quickly, then review and harden the produced code.

<Callout icon="lightbulb">
  Use comment-driven generation to create initial scaffolding quickly, but manually verify validation, edge cases, and algorithmic details afterwards.
</Callout>

## What this example includes (quick overview)

| Component                     | Purpose                                               | Key features                                                                                               |
| ----------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `Employee` class              | Demonstrates typed attributes with runtime validation | `name`, `age`, `salary` properties with setters that validate types and ranges                             |
| `process_stock_data`          | Process market data for simple analytics and signals  | Handles missing data, clips outliers, computes `SMA_50`, `SMA_200`, `daily_return`, `volatility`, `signal` |
| `validate_trading_parameters` | Lightweight pre-trade validation utility              | Ensures `price`, `volume`, and `symbol` have correct types and positive values                             |
| Tests (`pytest`)              | Example unit tests generated from the code context    | Checks structure and basic behavior of the processing function and validators                              |

## Full example: implementation (main.py)

The following consolidated example demonstrates a realistic scaffold that you might generate from well-formed comments. It keeps type hints, validation logic, and a stock-data processing method suitable for prototyping.

```python theme={null}
