# main.py
from typing import Any
import pandas as pd
import numpy as np


class Employee:
    def __init__(self, name: str, age: int, salary: float) -> None:
        self.name = name
        self.age = age
        self.salary = salary

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value:
            raise ValueError("Name must not be empty")
        self._name = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0:
            raise ValueError("Age must be non-negative")
        self._age = value

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary must be non-negative")
        self._salary = float(value)

    def process_stock_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate moving averages, volatility, and trading signals.
        Handle missing data and outliers in a conservative, example manner.
        - Expects a DataFrame with a 'Close' column.
        - Adds columns: 'SMA_50', 'SMA_200', 'daily_return', 'volatility', 'signal'
        """
        if "Close" not in data.columns:
            raise KeyError("DataFrame must contain a 'Close' column")

        df = data.copy()

        # Handle missing data: forward-fill then drop remaining NaNs
        df["Close"] = df["Close"].ffill()
        df = df.dropna(subset=["Close"])

        # Calculate returns
        df["daily_return"] = df["Close"].pct_change()

        # Handle outliers in returns by clipping to mean +/- 3*std
        ret_mean = df["daily_return"].mean(skipna=True)
        ret_std = df["daily_return"].std(skipna=True)
        if pd.notna(ret_std) and ret_std != 0:
            lower = ret_mean - 3 * ret_std
            upper = ret_mean + 3 * ret_std
            df["daily_return"] = df["daily_return"].clip(lower, upper)

        # Calculate volatility and moving averages (examples: windows 50 and 200)
        df["volatility"] = df["daily_return"].rolling(window=50, min_periods=1).std()
        df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
        df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

        # Trading signal: 1 when short MA > long MA, -1 when short MA < long MA, else 0
        df["signal"] = np.where(df["SMA_50"] > df["SMA_200"], 1, np.where(df["SMA_50"] < df["SMA_200"], -1, 0))

        return df


def validate_trading_parameters(price: float, volume: int, symbol: str) -> bool:
    """Validate trading parameters before order execution"""
    if not isinstance(price, (int, float)):
        raise TypeError("Price must be a number")
    if not isinstance(volume, int):
        raise TypeError("Volume must be an integer")
    if not isinstance(symbol, str):
        raise TypeError("Symbol must be a string")

    if price <= 0:
        raise ValueError("Price must be positive")
    if volume <= 0:
        raise ValueError("Volume must be positive")

    return True


if __name__ == "__main__":
    employee = Employee("Alice", 30, 50000)
    print(employee.name)
    print(employee.age)
    print(employee.salary)
```

Example console output:

```bash theme={null}
$ python main.py
Alice
30
50000.0
```

## Example unit tests (test\_main.py)

Below is a compact pytest-based test module that checks structure and some basic expectations of the stock-processing pipeline and the trading parameter validator. Generated tests often focus on structure and obvious edge cases; review and extend them for numerical correctness and domain-specific behavior.

```python theme={null}
# test_main.py
import pandas as pd
import numpy as np
import pytest
import main


def test_process_stock_data_structure():
    # Short sample of closing prices (10 datapoints)
    data = pd.DataFrame({
        "Close": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    })
    emp = main.Employee("Alice", 30, 50000)
    processed = emp.process_stock_data(data)

    # Check expected columns exist
    for col in ["SMA_50", "SMA_200", "daily_return", "volatility", "signal"]:
        assert col in processed.columns

    # With only 10 rows, SMA_50 and SMA_200 will be present but many values will be computed using min_periods=1.
    # Ensure signal column contains only -1, 0, or 1
    assert set(processed["signal"].dropna().unique()).issubset({-1, 0, 1})


def test_validate_trading_parameters_valid():
    assert main.validate_trading_parameters(100.0, 10, "AAPL") is True


def test_validate_trading_parameters_invalid():
    with pytest.raises(TypeError):
        main.validate_trading_parameters("100", 10, "AAPL")
    with pytest.raises(ValueError):
        main.validate_trading_parameters(0, 10, "AAPL")
```

<Callout icon="warning">
  Generated code and tests are a starting point. Always inspect generated logic for correctness, numeric stability, and security issues before using in production.
</Callout>

## Best practices for comment-driven generation

* Write clear, concise comments describing the intended behavior and edge cases you care about (input shapes, allowed ranges, failure modes).
* Use generated code to scaffold structure and tests, but prioritize manual reviews for:
  * Validation logic (types and ranges)
  * Numerical stability (rolling windows, NaN handling, outlier treatment)
  * Performance-critical loops or IO
* Create targeted unit tests that assert domain-specific numerical expectations in addition to structural checks.
* Document assumptions directly in code docstrings so generated tests can pick up on them.

## Links and references

* pandas documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
* numpy documentation: [https://numpy.org/doc/](https://numpy.org/doc/)
* pytest documentation: [https://docs.pytest.org/](https://docs.pytest.org/)

In the next lesson we'll apply comment-driven generation to build a fake data generator project for testing and prototyping.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/192b5dd0-981d-43ef-80e9-b4189b3877af/lesson/159f6e4d-16da-4bf2-9047-12d0bba43a28" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Core-Features/Introduction/page

A lesson explaining GitHub Copilot core features, productivity tips, comment-driven prompts, usage patterns, and best practices for safe, effective AI-assisted coding.

In this lesson we explore the core features of GitHub Copilot: what it is, how it works, and practical ways to use it effectively in day-to-day development.

<Frame>
  <img alt="A KodeKloud presentation slide with the logo and the title &#x22;Mastering GitHub Copilot&#x22; and subtitle &#x22;Core Features&#x22; on a dark blue background." />
</Frame>

You’ll learn quick wins that accelerate coding, techniques to improve code quality, and simple usage patterns you can apply immediately to make Copilot a reliable coding partner.

<Frame>
  <img alt="A presentation slide with a dark left panel labeled &#x22;Agenda.&#x22; On the pale right side is an item marked &#x22;01 Quick wins.&#x22;" />
</Frame>

We’ll finish with practical guidance on using inline comments and prompts to steer Copilot’s suggestions so they match project conventions, documentation style, and desired levels of detail.

<Callout icon="lightbulb">
  Tip: Treat GitHub Copilot as an AI pair programmer — accept, modify, or reject suggestions. Use concise comments and consistent naming to get more relevant, context-aware completions.
</Callout>

## What you will learn

* Core capabilities of GitHub Copilot: code completion, whole-line and multi-line suggestions, and test generation.
* Quick wins to boost productivity: snippets, refactor suggestions, and boilerplate generation.
* How to craft comments and prompts that guide Copilot toward correct, idiomatic code.
* Safety and review practices to maintain code quality and security.

## Lesson outline

| Topic                             | Benefit                              | Example                                                |
| --------------------------------- | ------------------------------------ | ------------------------------------------------------ |
| Quick wins                        | Faster development for common tasks  | Generating CRUD endpoints or unit test scaffolding     |
| Usage patterns                    | Better, more predictable suggestions | Use descriptive variable names and function signatures |
| Guiding suggestions with comments | Tailored, project-specific outputs   | `// Calculate monthly revenue in USD`                  |
| Best practices                    | Maintain code quality and security   | Review AI-generated code before merging                |

## How this lesson is structured

1. Quick wins — immediate productivity gains and typical workflows.
2. Usage patterns — how to get consistent Copilot behavior across files and teams.
3. Comments & prompts — examples of comment-driven completions and prompt templates.
4. Best practices — verification, testing, and security checks for AI-assisted code.

## Links and references

* [GitHub Copilot documentation](https://docs.github.com/en/copilot)
* [AI coding best practices](https://github.com/features/copilot)
* [Secure coding guidelines](https://owasp.org)

Keep these references handy as you follow along — they reinforce verification steps and configuration options for Copilot across editors and IDEs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/192b5dd0-981d-43ef-80e9-b4189b3877af/lesson/e3299056-a2b6-4876-ac55-07c44145eaf8" />
</CardGroup>
