# Errors and Exceptions

Source: https://notes.kodekloud.com/docs/Python-Basics/Exceptions/Errors-and-Exceptions/page

This article explains how to handle errors and exceptions in Python using try-except blocks for better program stability.

When Python runs your code, it might encounter an issue and raise an exception—a special type of object that signals an error occurred. If the exception isn’t handled, Python stops the program and displays an error message.

Consider this example:

```python theme={null}
name = 'Lydia'

print('My name is' + naem)
print('All done!')
```

```Python theme={null}
NameError: name 'naem' is not defined
```

In this case, Python raises a NameError because the variable "naem" does not exist. Instead of crashing immediately, you can catch and handle exceptions so that the program continues executing.

<Callout icon="lightbulb">
  Use a try-except block to monitor code for errors. The code under the try block executes normally, but if an error occurs, the code in the corresponding except block takes over.
</Callout>

## Try-Except: A Basic Example

You can handle exceptions using the `try` and `except` keywords. In the example below, if an error arises in the try block, the program jumps to the except block:

```python theme={null}
try:
    name = 'Lydia'
    print('My name is' + naem)
except:
    print('Something went wrong')

print('All done!')
```

The output of this code is:

```Python theme={null}
Something went wrong
All done!
```

Since the exception was caught, Python exits the try-except block and continues with the rest of the program.

## Handling Specific Exceptions

Python allows you to handle specific types of errors individually. Among the common error types are:

* ZeroDivisionError
* ValueError
* TypeError
* SystemError
* AssertionError
* AttributeError
* IndexError
* KeyError
* IndentationError

<Frame>
  ![The image lists various Python error types, including ZeroDivisionError, ValueError, TypeError, SystemError, AssertionError, AttributeError, IndexError, KeyError, IndentationError, and others.](https://kodekloud.com/kk-media/image/upload/v1752883528/notes-assets/images/Python-Basics-Errors-and-Exceptions/frame_80.jpg)
</Frame>

Suppose you ask a user to input a number and try to compute its reciprocal. Two issues may occur:

| Scenario                         | Expected Exception |
| -------------------------------- | ------------------ |
| User enters a non-numeric string | ValueError         |
| User enters zero                 | ZeroDivisionError  |

Here’s how you can manage these specific exceptions using multiple except blocks:

```python theme={null}
try:
    x = int(input("Enter a number: "))
    y = 1 / x
    print(y)
except ZeroDivisionError:
    print("You cannot divide by zero.")
except ValueError:
    print("Please enter an integer.")
except:
    print("Something else went wrong")
    
print("All done!")
```

When a ValueError occurs (for example, if the user inputs a non-integer), the corresponding except block is executed. Likewise, entering zero triggers the ZeroDivisionError block. Note that any generic `except` block without a specified exception type should always come last to catch any other unforeseen errors.

<Callout icon="lightbulb">
  Always handle specific exceptions before using a generic exception block. This practice improves code readability and error handling precision.
</Callout>

That concludes our article on Python errors and exceptions. Now, it's time to put this knowledge into practice and enhance your Python programming skills!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-basics/module/b7dfa718-4f50-4b8b-bc7c-51915b87a2a7/lesson/eb3cef1e-6cb3-4adf-a763-992614247cde" />
</CardGroup>
