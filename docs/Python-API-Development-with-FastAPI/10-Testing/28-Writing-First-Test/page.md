# Writing First Test

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Writing-First-Test/page

This guide walks you through creating your first test using the pytest framework, covering installation, writing tests, and understanding assertions.

In this guide, we’ll walk you through creating your very first test using the pytest framework. If you’re new to pytest, consider searching for its documentation online to familiarize yourself with its setup and capabilities. We will cover installing pytest, writing an intentionally failing test to learn from its output, and building a simple test suite for a basic calculation module.

***

## Installing Pytest

Begin by installing pytest as you would any other Python package:

```bash theme={null}
pip install pytest
```

After installation, confirm that the pytest command is available by running:

```bash theme={null}
pytest
```

A successful run displays output similar to:

```plaintext theme={null}
================================ test session starts =============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-1.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_IMPDIR
collected 1 item

test_sample.py [100%]

============================= FAILURES ============================================
___________________________ test_answer ___________________________________________

def test_answer():
>       assert inc(3) == 5
E       assert 4 == 5
E        +   where 4 = inc(3)

test_sample.py:6: AssertionError
============================== short test summary info ============================
FAILED test_sample.py::test_answer - AssertionError: assert 4 == 5
```

This output indicates that a test failure occurred as expected. The failure stems from an error in the test setup, which we will address in the next section.

***

## Writing a Sample Test

Create a file named `test_sample.py` where we define a simple function alongside its failing test:

```python theme={null}
