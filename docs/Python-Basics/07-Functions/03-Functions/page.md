# Explicitly assign values to parameters regardless of their order
input1 = input_number(num2=10, num1=20)
```

<Callout icon="triangle-alert">
  Avoid assigning a value to the same parameter more than once. For example, providing `num1` both positionally and by name will result in an error:
</Callout>

```python theme={null}
def input_number(num1, num2):
    return int(input("Enter a number: ")) * num1 - num2

# This will raise an error because num1 is provided twice:
input1 = input_number(10, num1=20)
```

## Default Parameter Values

Python also allows you to define default values for parameters. When calling the function, if the caller does not supply an argument for a parameter with a default value, Python automatically uses that default. For instance, if we set the default value of `num` to 10, the function will multiply the user’s input by 10 if no argument is provided:

```python theme={null}
def input_number(num=10):
    return int(input("Enter a number: ")) * num

# Using the default value of 10
print(input_number())
```

If the user enters 12, the output is 120 because 12 × 10 = 120.

Alternatively, if you specify a value (for example, 5), Python overrides the default value:

```python theme={null}
def input_number(num=10):
    return int(input("Enter a number: ")) * num

# Overriding the default value by passing 5
print(input_number(5))
```

In this case, if the input is 12, the function computes 12 × 5, yielding 60.

***

That's the end of our discussion on passing arguments to Python functions. It's time to get hands-on and practice these concepts. For further reading on Python functions, consider visiting the [Python Documentation](https://docs.python.org/3/tutorial/controlflow.html#defining-functions).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-basics/module/e169dc83-5d71-40ac-8437-4f500246efe6/lesson/7e6d0bc3-0286-4025-aec1-a5d5b131f77e" />
</CardGroup>


# Functions

Source: https://notes.kodekloud.com/docs/Python-Basics/Functions/Functions/page

Learn to create and use custom functions in Python to enhance code readability and reduce redundancy.

In this lesson, you'll learn how to create and use custom functions in Python. So far, we've worked with built-in functions like `print`, `len`, and `input`, and we've distinguished between functions and methods. In Python, functions can come from the core language, external modules, or be defined by you.

<Callout icon="lightbulb">
  Encapsulating repeated code into functions enhances readability and minimizes potential bugs.
</Callout>

## Why Use Functions?

Repeating blocks of code can make your programs harder to maintain and increase the risk of errors. By defining a function, you bundle the code into a reusable unit, reducing redundancy and improving clarity.

Consider the following example where the same input logic is repeated multiple times:

```python theme={null}
input1 = int(input("Enter a number: "))
input2 = int(input("Enter a number: "))
input3 = int(input("Enter a number: "))
input4 = int(input("Enter a number: "))
input5 = int(input("Enter a number: "))
```

To streamline this, we can define a function named `input_number`:

## Defining the Function

We create a function using Python's `def` keyword. The function starts with the function name and parentheses, followed by a colon to indicate the beginning of the function body. In this case, the function prompts the user for a number, converts the input to an integer using `int()`, and returns the value.

Here's how to rewrite the repetitious code using our new `input_number` function:

```python theme={null}
def input_number():
    return int(input("Enter a number: "))

input1 = input_number()
input2 = input_number()
input3 = input_number()
input4 = input_number()
input5 = input_number()
```

Each time you call `input_number()`, the function executes its internal code, prompting the user, converting the input to an integer, and returning the resulting value. For example, the variable `input1` holds the number provided by the user.

## Important Consideration

It is crucial to define a function before calling it. If you attempt to use a function before its definition, Python will throw an error:

```python theme={null}
>>> input1 = input_number()
def input_number():
    return int(input("Enter a number: "))
NameError: name 'input_number' is not defined
```

This error occurs because Python processes the code sequentially and has not encountered the definition of `input_number` when it is called.

<Callout icon="triangle-alert">
  Always define your functions before invoking them to avoid `NameError` issues.
</Callout>

That’s all for this lesson. Keep practicing your function definitions and usage. [Learn more about Python functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) for additional insights.

See you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-basics/module/e169dc83-5d71-40ac-8437-4f500246efe6/lesson/07eeb9c0-46aa-45f3-92b4-b1cb2c06e30d" />
</CardGroup>
