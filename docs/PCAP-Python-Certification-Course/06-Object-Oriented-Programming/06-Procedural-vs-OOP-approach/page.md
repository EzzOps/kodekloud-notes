# Procedural vs OOP approach

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/Object-Oriented-Programming/Procedural-vs-OOP-approach/page

This article compares procedural and object-oriented stack implementations in Python, highlighting techniques, best practices, and encapsulation.

A stack is a fundamental data structure that follows the last-in-first-out (LIFO) principle, meaning that the last element added is the first to be removed. In this guide, we demonstrate how to implement a stack in Python using both procedural and object-oriented programming (OOP) approaches.

## Procedural Approach

In the procedural approach, the stack's data and the associated logic (functions for pushing and popping) are separate. Below is an example where the stack is represented as a simple list, and helper functions manipulate it.

```python theme={null}
stack = []

def push(val):
    stack.append(val)

def pop():
    val = stack[-1]
    del stack[-1]
    return val

push(3)
push(2)
push(1)
print(pop())
print(pop())
print(pop())
```

> **lightbulb** In this implementation, the global `stack` variable can be accessed and modified from anywhere in your code, which can lead to unintended side effects. For multiple stacks, additional functions must be created, reducing reusability.

## Object-Oriented Approach

The object-oriented method encapsulates both data and behavior within a class, promoting modularity and data protection. We begin by defining a `Stack` class with an initializer that confirms the creation of a new stack instance.

```python theme={null}
class Stack:
    def __init__(self):
        print("I am in the constructor function!")

stack_object = Stack()
```

Output:

```text theme={null}
I am in the constructor function!
```

Next, we introduce a property for the stack's data. Initially, this property (`stack_list`) is public, offering direct access:

```python theme={null}
class Stack:
    def __init__(self):
        self.stack_list = []

stack_object = Stack()
print(len(stack_object.stack_list))
```

Output:

```text theme={null}
0
```

> **lightbulb** Although a public attribute is simple to implement, it compromises encapsulation. To protect the internal data structure, converting it to a private attribute is recommended.

To enforce encapsulation, we modify `stack_list` to a private attribute by prefixing it with two underscores. Attempting to access this attribute externally will raise an error:

```python theme={null}
class Stack:
    def __init__(self):
        self.__stack_list = []

stack_object = Stack()
