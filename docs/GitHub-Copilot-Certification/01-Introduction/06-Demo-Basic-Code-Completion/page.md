# Create an Employee class with name, age, and salary attributes
# Include type hints and validation for each field
```

<Callout icon="lightbulb">
  GitHub Copilot will trigger on typing patterns like `def` or `class`. Press `Tab` (or your configured shortcut) to accept the suggestion.
</Callout>

After accepting Copilot’s suggestion, your file should look like this:

```python theme={null}
import pandas as pd
import numpy as np

class Employee:
    def __init__(self, name: str, age: int, salary: float):
        self.name = name
        self.age = age
        self.salary = salary

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        self._age = value

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        self._salary = value
```

### Instantiate and Verify

```python theme={null}
# main.py
employee = Employee("Alice", 30, 50000.0)
print(employee.name)    # Alice
print(employee.age)     # 30
print(employee.salary)  # 50000.0
```

```bash theme={null}
(venv) $ python main.py
Alice
30
50000.0
```

***

## Extend with Domain-Specific Methods

You can drive Copilot to add data-processing methods by writing comments in the class. For example, to analyze stock data:

```python theme={null}
# create a method that processes stock market data
# calculate moving averages, volatility, and trading signals
# handle missing data and outliers
def process_stock_data(self, data: pd.DataFrame) -> pd.DataFrame:
    # calculate moving averages
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # calculate volatility
    data['daily_return'] = data['Close'].pct_change()
    data['volatility'] = data['daily_return'].rolling(window=50).std()

    # generate signals
    data['signal'] = 0
    data.loc[data['SMA_50'] > data['SMA_200'], 'signal'] = 1
    data.loc[data['SMA_50'] < data['SMA_200'], 'signal'] = -1

    # handle missing values
    data.fillna(method='ffill', inplace=True)
    return data
```

Add this directly under the `Employee` class. Running `main.py` again confirms existing behavior is preserved:

```bash theme={null}
(venv) $ python main.py
Alice
30
50000.0
```

***

## Comment-Driven Function Generation

Standalone functions are just as easy. In `main.py`, add:

```python theme={null}
# Validate trading parameters before order execution
```

Copilot generates:

```python theme={null}
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
```

***

## Auto-Generate Unit Tests

Create `test_main.py` and write test-descriptive comments:

```python theme={null}
# test process_stock_data function
```

Copilot suggests:

```python theme={null}
import pytest
import pandas as pd
import main

def test_process_stock_data():
    data = pd.DataFrame({'Close': list(range(1, 201))})
    emp = main.Employee("Alice", 30, 50000.0)
    processed = emp.process_stock_data(data.copy())

    assert 'SMA_50' in processed
    assert 'SMA_200' in processed
    assert 'volatility' in processed
    assert 'signal' in processed
    assert processed['signal'].iloc[-1] == 1

def test_validate_trading_parameters_success():
    assert main.validate_trading_parameters(100.5, 1000, 'AAPL') is True

@pytest.mark.parametrize("price,volume,symbol,exception", [
    (-1,   100, 'AAPL', ValueError),
    (100.5,   0, 'AAPL', ValueError),
    (100.5, 1000,    123, TypeError),
])
def test_validate_trading_parameters_errors(price, volume, symbol, exception):
    with pytest.raises(exception):
        main.validate_trading_parameters(price, volume, symbol)
```

Run tests:

```bash theme={null}
(venv) $ pytest -q
```

***

<Callout icon="triangle-alert">
  Always review generated code for edge cases and security considerations—AI suggestions may not cover every scenario.
</Callout>

***

## Resources & References

* [GitHub Copilot](https://github.com/features/copilot)
* [pandas Documentation](https://pandas.pydata.org/docs/)
* [pytest Documentation](https://docs.pytest.org/)
* [Python Type Hints](https://docs.python.org/3/library/typing.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-certification/module/b02a5227-ee17-43dc-b006-51fef8272f13/lesson/159f6e4d-16da-4bf2-9047-12d0bba43a28" />
</CardGroup>


# Demo Basic Code Completion

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Introduction/Demo-Basic-Code-Completion/page

This tutorial explores how GitHub Copilot accelerates common Python workflows with examples of generating boilerplate, implementing algorithms, and handling data structures.

In this tutorial, we’ll explore how GitHub Copilot accelerates common Python workflows. You’ll see examples of generating boilerplate, implementing algorithms, handling data structures, managing errors, and making HTTP requests—all with minimal typing.

## Table of Contents

* [1. Setup: Creating the Python File](#1-setup-creating-the-python-file)
* [2. Hello, World!](#2-hello-world)
* [3. Factorial Function](#3-factorial-function)
* [4. List Comprehension Example](#4-list-comprehension-example)
* [5. File I/O with Exception Handling](#5-file-io-with-exception-handling)
* [6. HTTP Requests with the `requests` Library](#6-http-requests-with-the-requests-library)
* [Conclusion & Key Takeaways](#conclusion--key-takeaways)
* [Links and References](#links-and-references)

***

## 1. Setup: Creating the Python File

First, open your terminal and create a new script named `main.py`:

```bash theme={null}
touch main.py
```

Then open **main.py** in your preferred editor and trigger Copilot suggestions by starting to type.

***

## 2. Hello, World!

Start by asking Copilot to scaffold the classic “Hello, World!” program:

```python theme={null}
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

Save and run:

```bash theme={null}
python3 main.py
