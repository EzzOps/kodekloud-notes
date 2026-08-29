# Testing Exceptions

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Testing-Exceptions/page

This article discusses enhancing the BankAccount class with exception handling for withdrawals to prevent overdrafts and improve error management.

In this article, we enhance our BankAccount class by introducing exception handling for withdrawal operations. This update ensures that users cannot withdraw more money than is available in their account. The guide covers the original implementation, the issue with insufficient balance checks, testing adjustments, and the introduction of a custom exception for better error handling.

## Original BankAccount Implementation

Initially, our BankAccount class was implemented as follows:

```python theme={null}
class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
```

When running tests, all tests passed:

```plaintext theme={null}
PASSED
tests/test_calculations.py::test_bank_transaction[50-10-40] creating empty bank account
PASSED
tests/test_calculations.py::test_bank_transaction[1200-200-1000] creating empty bank account
================================== 14 passed in 0.09s ==================================
```

## Problem: Insufficient Funds Check

Upon inspection, the `withdraw` method does not verify if the account has sufficient funds. For example, if the account has $100 and a withdrawal of $500 is attempted, the operation should be blocked. To address this, we add a check in the `withdraw` method that raises an exception when necessary.

### Updated BankAccount Implementation with Basic Exception

The revised BankAccount class adds a condition to the `withdraw` method to raise an exception if the withdrawal amount exceeds the account balance:

```python theme={null}
class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
```

Re-running the tests produces the following output:

```plaintext theme={null}
PASSED
tests/test_calculations.py::test_bank_transaction[50-10-40] creating empty bank account
PASSED
tests/test_calculations.py::test_bank_transaction[1200-200-1000] creating empty bank account
PASSED
================= 14 passed in 0.09s =================
```

## Adjusting Tests for Exception Handling

The original parameterized test included a case where more money was withdrawn than deposited:

```python theme={null}
import pytest

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
    (10, 200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected
```

The test output indicated a failure for the case where 10 is deposited and 200 is withdrawn:

```plaintext theme={null}
self = <app.calculations.BankAccount object at 0x0000018C971BC940>, amount = 50

def withdraw(self, amount):
    if amount > self.balance:
        raise Exception("Insufficient funds in account")
E       Exception: Insufficient funds in account

app/calculations.py:27: Exception
================================= short test summary info =================================
FAILED tests/test_calculations.py::test_bank_transaction[10-50-40] - Exception: Insufficient funds in account
```

Since an exception is expected for insufficient funds, it's better to remove this failing test case from the parameterized group and create a dedicated test.

### Creating a Dedicated Test for Insufficient Funds

We use Pytest’s `raises` context manager for this purpose. For an account with an initial balance of zero (using the `zero_bank_account` fixture), attempting to withdraw money should trigger an exception:

```python theme={null}
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)
```

Here, the `bank_account` fixture initializes an account with a balance (for instance, 50) to ensure that withdrawing \$200 raises the expected exception. Running the tests now produces:

```plaintext theme={null}
tests/test_calculations.py::test_bank_transaction[50-10-40] creating empty bank account
tests/test_calculations.py::test_bank_transaction[1200-200-1000] creating empty bank account
tests/test_calculations.py::test_insufficient_funds PASSED
15 passed in 0.09s
```

## Introducing a Custom Exception: InsufficientFunds

For better clarity and maintainability in production code, we define a custom exception called `InsufficientFunds` that inherits from Python’s built-in `Exception` class. This approach allows our tests to verify that the correct exception is raised.

### Defining the Custom Exception

```python theme={null}
class InsufficientFunds(Exception):
    pass
```

### Updated BankAccount Class with Custom Exception

The BankAccount class is updated to raise `InsufficientFunds` when an over-withdrawal is attempted:

```python theme={null}
class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
```

### Updating the Test for Insufficient Funds

We also update the insufficient funds test to assert that an `InsufficientFunds` exception is raised:

```python theme={null}
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
```

Running the tests now confirms that the proper exception is raised:

```plaintext theme={null}
tests/test_calculations.py::test_bank_transaction[200-100-100] creating empty bank account PASSED
tests/test_calculations.py::test_bank_transaction[50-10-40] creating empty bank account PASSED
tests/test_calculations.py::test_bank_transaction[1200-200-1000] creating empty bank account PASSED
tests/test_calculations.py::test_insufficient_funds PASSED

15 passed in 0.08s
```

> **lightbulb** Specifying the exact exception type ensures that our code not only raises an error but also raises the correct, expected type. This improves test precision and code reliability.

## Demonstrating the Importance of the Correct Exception Type

To highlight the importance of using a custom exception, consider a scenario where `ZeroDivisionError` is raised instead of `InsufficientFunds`. For example, changing the `withdraw` method as shown below would trigger a test failure:

```python theme={null}
def withdraw(self, amount):
    if amount > self.balance:
        # raise InsufficientFunds("Insufficient funds in account")
        raise ZeroDivisionError()
    self.balance -= amount
```

Test output in this case would be:

```plaintext theme={null}
app/calculations.py:32: ZeroDivisionError
FAILED tests/test_calculations.py::test_insufficient_funds - ZeroDivisionError
```

This failure confirms that our tests correctly check for a specific exception, and any deviation from the expected behavior will be flagged immediately.

## Conclusion

By defining and raising a custom exception for insufficient funds, our BankAccount class now operates in a robust and predictable manner. The updated tests validate this behavior precisely, ensuring that the internal logic of our application remains stable and error-free.

Happy testing!

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/6fd9eb3e-c45a-4121-a4ee-803a30b59ad2)
