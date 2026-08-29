# The following line will raise an AttributeError because __stack_list is private.
print(len(stack_object.__stack_list))
```

Output:

```Python theme={null}
AttributeError: 'Stack' object has no attribute '__stack_list'
```

When a class attribute starts with two underscores, it becomes private and can only be used within the class. This encapsulation is crucial for maintaining the integrity of your data structure.

Next, we add the `push` and `pop` methods to the `Stack` class for manipulating the internal stack:

```python theme={null}
class Stack:
    def __init__(self):
        self.__stack_list = []

    def push(self, val):
        self.__stack_list.append(val)

    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val

stack_object = Stack()
stack_object2 = Stack()

stack_object.push(3)
stack_object.push(2)
stack_object.push(1)

stack_object2.push(10)
stack_object2.push(9)

print(stack_object2.pop())
print(stack_object.pop())
print(stack_object.pop())
print(stack_object.pop())
```

This object-oriented implementation clearly demonstrates that separate instances of the `Stack` class maintain independent data, providing a scalable solution for handling multiple stacks.

## Extending the Stack Class with Inheritance

Inheritance allows you to extend the functionality of a base class without modifying it. Consider a scenario where you need to track the cumulative sum of the elements in the stack. Instead of altering the original `Stack` class, you can create a subclass `AddingStack` that inherents from `Stack` and adds new behavior.

In the subclass:

* The constructor calls the base class constructor using `super().__init__()`.
* The `push` method is overridden to update the cumulative sum before invoking the base class method.
* The `pop` method is overridden to subtract the popped value from the cumulative sum.
* A new method `get_sum` is introduced to retrieve the current sum.

```python theme={null}
class AddingStack(Stack):
    def __init__(self):
        super().__init__()
        self.__sum = 0

    def get_sum(self):
        return self.__sum

    def push(self, val):
        self.__sum += val
        super().push(val)

    def pop(self):
        val = super().pop()
        self.__sum -= val
        return val

stack = AddingStack()
stack.push(10)
stack.push(5)
print(stack.get_sum())
```

Output:

```Python theme={null}
15
```

> **lightbulb** If a subclass does not define its own constructor, it automatically inherits the constructor from its superclass. In cases where no additional behavior is required, you can simply use the `pass` keyword to inherit all functionalities without modification.

This comprehensive guide on stack implementation in Python illustrates both procedural and object-oriented techniques, along with best practices such as encapsulation and inheritance.

That's it for now—it's time to gain some hands-on practice!

For more details on Python programming and data structures, check out [Python Official Documentation](https://docs.python.org/3/tutorial/) and [Data Structures in Python](https://realpython.com/python-data-structures/).

- [Watch Video](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/7e473cae-90c2-4d9a-8e81-6509481b52ce/lesson/98512165-dcf1-4158-b576-60496ac42de5)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/7e473cae-90c2-4d9a-8e81-6509481b52ce/lesson/720cfc1f-a716-4425-9f34-58d214cc6647)


# The objective nature of exceptions

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/Object-Oriented-Programming/The-objective-nature-of-exceptions/page

This article explores Python's exception handling mechanisms, including try-except, else, and finally blocks for effective error management.

In this article, we explore Python's exception handling mechanisms, a critical component of robust software development. You will learn about the basic try-except pattern designed to execute code that might produce an error and how to gracefully handle that error when it occurs.

## Using the Else Block

In addition to the conventional try and except blocks, Python allows you to include an **else** block. This block is placed after all except blocks and is executed only if no exception is raised in the try block. This feature is useful for running code that should only execute when the try block is successful.

Consider the following example:

```python theme={null}
def calc(num):
    try:
        result = 1 / num
        print(result)
    except ZeroDivisionError:
        print("You cannot divide by zero.")
    else:
        print("All good!")

calc(0)
calc(10)
```

**Console output:**

```text theme={null}
You cannot divide by zero.
0.1
All good!
```

> **lightbulb** The **else** block is executed only when no exceptions occur. This practice ensures that the normal flow executes separately from error handling.

## The Finally Block for Cleanup

Python also provides a **finally** block that will execute regardless of whether an exception has been raised or not. This is particularly useful for clean-up actions such as closing files or releasing external resources.

Below is an example demonstrating the use of a finally block:

```python theme={null}
def calc(num):
    try:
        result = 1 / num
        print(result)
    except ZeroDivisionError:
        print("You cannot divide by zero.")
    else:
        print("All good!")
    finally:
        print("Execution complete.")

calc(0)
calc(10)
```

**Console output:**

```text theme={null}
You cannot divide by zero.
Execution complete.
0.1
All good!
Execution complete.
```

> **lightbulb** The code in the **finally** block is executed after the try-except-else structure, regardless of the outcome. This makes it ideal for performing clean-up tasks.

## Summary

Understanding how Python handles exceptions is vital for writing robust code. By combining try, except, else, and finally blocks, programmers can manage errors effectively, ensuring that the program's normal flow is maintained while also handling unforeseen issues.

That's it for now—it's time to gain some hands-on practice!

- [Watch Video](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/7e473cae-90c2-4d9a-8e81-6509481b52ce/lesson/a072c713-2a19-4dad-a149-6e5865419ae7)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/7e473cae-90c2-4d9a-8e81-6509481b52ce/lesson/01a9211b-1610-459a-9dc3-05fd6d000737)
