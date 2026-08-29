# Hierarchy of Exceptions

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/Exceptions/Hierarchy-of-Exceptions/page

This article explains the hierarchy of exceptions in Python, including handling, raising, and re-raising exceptions, along with using the assert keyword for validation.

Python 3 provides 63 built-in exceptions that are organized in a hierarchical tree. For example, a ZeroDivisionError is a specialized exception under ArithmeticError, which in turn is a subtype of Exception. Ultimately, all these derive from BaseException.

Because ZeroDivisionError inherits from ArithmeticError, you can design your exception handling logic to catch any ArithmeticError, not just a ZeroDivisionError. However, ensure that your error messages are generic enough because the caught error might not strictly be about division by zero. Additionally, if you specify multiple exception handlers (for instance, both ZeroDivisionError and ArithmeticError), only the first matching branch will execute. This makes the order of exception handlers critical for accurate error handling.

Below is a sample code snippet illustrating these concepts:

```python theme={null}
try:
    x = int(input("Enter a number: "))
    y = 1 / x
    print(y)
except ZeroDivisionError:
    print("You cannot divide by zero.")
except ArithmeticError:
    print("Calculation failed.")
except:
    print("Something else went wrong")
    
print("All done!")
```

Example output when the input is 0:

```text theme={null}
Enter a number:
0
You cannot divide by zero.
All done!
```

If you want to handle two or more exceptions in the same way, you can combine them into a tuple. Consider the following example:

```python theme={null}
try:
    x = int(input("Enter a number: "))
    y = 1 / x
    print(y)
except (ZeroDivisionError, ValueError):
    print("Invalid input value")
except ArithmeticError:
    print("Calculation failed.")
except:
    print("Something else went wrong")
    
print("All done!")
```

Example output when 0 is entered:

```text theme={null}
Enter a number:
0
Invalid input value
All done!
```

<Callout icon="lightbulb">
  When combining exceptions in a tuple, all specified exceptions are handled by the same code block. This method simplifies your code when similar error handling is required.
</Callout>

## Raising Exceptions Inside Functions

Exceptions can be raised within functions, and you can choose to handle them either inside the function or externally by wrapping the function call in a try block.

### Handling the Exception Inside the Function

```python theme={null}
def calculate_user_input():
    try:
        x = int(input("Enter a number: "))
        y = 1 / x
        print(y)
    except ZeroDivisionError:
        print("You cannot divide by zero.")
    except:
        print("Something else went wrong")
    return None

calculate_user_input()
```

### Handling the Exception Outside the Function

```python theme={null}
def calculate_user_input():
    x = int(input("Enter a number: "))
    y = 1 / x
    print(y)
    return None

try:
    calculate_user_input()
except ZeroDivisionError:
    print("You cannot divide by zero.")
except:
    print("Something else went wrong")
```

For example, if you enter 0, the output will be:

```text theme={null}
Enter a number:
0
You cannot divide by zero.
```

## Manually Raising Exceptions

You can manually raise exceptions using the `raise` keyword. This is useful for testing your error-handling strategy or delegating error processing elsewhere in your application. For instance, the following code manually raises a ZeroDivisionError:

```python theme={null}
raise ZeroDivisionError
```

The output will be similar to:

```text theme={null}
ZeroDivisionError
```

Consider this scenario where a function always raises a ZeroDivisionError. This code snippet tests the exception handling:

```python theme={null}
def calculate_user_input():
    raise ZeroDivisionError

try:
    calculate_user_input()
except ZeroDivisionError:
    print("You cannot divide by zero.")
except:
    print("Something else went wrong")
```

For input that leads to an exception, the output will be:

```text theme={null}
You cannot divide by zero.
```

## Re-raising Exceptions

Sometimes you may need to perform additional actions (like logging) and then allow the exception to propagate upward. In such cases, you can re-raise the exception within an `except` block:

```python theme={null}
def calculate_user_input():
    try:
        x = int(input("Enter a number: "))
        y = 1 / x
        print(y)
    except:
        print("Something else went wrong")
        raise  # Re-raise the caught exception
    return None

calculate_user_input()
```

<Callout icon="triangle-alert">
  When re-raising exceptions, ensure that you have already performed any necessary cleanup or logging. This practice maintains robust error handling in larger applications.
</Callout>

## Using the assert Keyword

The `assert` keyword in Python allows you to test if a condition is true. If the condition evaluates to False (or a value considered false, such as 0, an empty string, or None), an AssertionError is raised immediately. This is particularly useful for validating data and ensuring that functions operate on valid inputs.

Consider the following example:

```python theme={null}
import math
x = int(input("Enter a number: "))
assert x >= 0
result = math.sqrt(x)
print("Result:", result)
```

Example outputs:

```text theme={null}
Enter a number:
0
Result: 0.0
```

```text theme={null}
Enter a number:
-1
Traceback (most recent call last):
  ...
AssertionError
```

Raising an AssertionError in this manner helps ensure that your code does not proceed with invalid data, minimizing the risk of producing erroneous results.

For more detailed information, refer to the [Python documentation on built-in exceptions](https://docs.python.org/3/library/exceptions.html).

That concludes this lesson. Continue practicing and applying these concepts to develop robust error handling in your Python applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/8db6ee04-f51f-41fc-9539-029474f44a1b/lesson/59f80173-0a33-4128-bcec-6d243f0c34d2" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/8db6ee04-f51f-41fc-9539-029474f44a1b/lesson/02d42994-18b4-4e1d-8555-bd4e4ef7d6fa" />
</CardGroup>
