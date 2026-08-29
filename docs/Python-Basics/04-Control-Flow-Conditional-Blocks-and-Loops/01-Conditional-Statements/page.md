# Conditional Statements

Source: https://notes.kodekloud.com/docs/Python-Basics/Control-Flow-Conditional-Blocks-and-Loops/Conditional-Statements/page

This article explores executing code based on conditions using Python's built-in conditional statements for controlling program flow.

In this article, we explore how to execute code based on specific conditions using Python's built-in conditional statements. Conditional statements are essential for controlling the flow of your program by executing certain blocks of code only when certain criteria are met.

## The if Statement

The simplest conditional statement in Python uses the `if` keyword. When the condition provided after `if` evaluates to True, the following indented block of code is executed:

```python theme={null}
if condition:
    print("The condition is true!")
```

If the condition is False, Python skips the block and continues executing subsequent code.

<Callout icon="lightbulb">
  Always remember to end your `if` statement line with a colon (:). Proper indentation is critical for Python to correctly interpret which statements belong to the block.
</Callout>

## Practical Example with User Input

Consider a scenario where we prompt the user to enter their age. We then use an `if` statement to determine if the user is 18 or older, outputting an appropriate message accordingly. For example, if a user enters the age 22, the program will confirm that the user is an adult:

```python theme={null}
age = int(input("How old are you? "))
if age >= 18:
    print("You are an adult!")
```

When executed, the console interaction might look like this:

```text theme={null}
How old are you? 22
You are an adult!
```

## The if-else Statement

Sometimes, you need to execute one block of code when a condition is true and a different block when it is false. Use the `else` keyword to provide an alternative:

```python theme={null}
if condition:
    print("The condition is true!")
else:
    print("The condition is false!")
```

In this structure, if the initial condition is not met, the code under `else` will run.

## The if-elif-else Chain

For situations involving multiple conditions, Python's `elif` keyword lets you check additional expressions sequentially. This structure allows you to have several branching paths:

```python theme={null}
if False:
    print("The condition is true!")
elif True:
    print("Only the second condition is true!")
else:
    print("Both conditions are false!")
```

In this chain:

* Python first evaluates the `if` condition.
* If it evaluates to False, the program checks the `elif` condition.
* If the `elif` condition is also False, the `else` block is executed.

Note that if an earlier condition is met, the rest of the conditions (`elif` or `else`) are ignored:

```python theme={null}
if True:
    print("The condition is true!")
elif True:
    print("Only the second condition is true!")
else:
    print("Both conditions are false!")
```

## Nested Conditional Statements

You can nest conditional statements inside another to evaluate further conditions. For example, if you want to give a special message when a user's age is exactly 18, use a nested `if`:

```python theme={null}
if age >= 18:
    if age == 18:
        print("You are exactly 18 years old!")
    else:
        print("You are older than 18 years old!")
```

In this scenario:

* The outer `if` checks if the user is an adult (18 or older).
* If true, the inner `if` further checks whether the age is exactly 18.
* If the inner condition is False, it indicates that the user is older than 18.

<Callout icon="lightbulb">
  Using nested conditional statements helps create a more detailed decision-making process, allowing you to handle complex conditions efficiently.
</Callout>

## Summary of Conditional Statements

| Statement Type | Description                                            | Example Usage                                                         |
| -------------- | ------------------------------------------------------ | --------------------------------------------------------------------- |
| if             | Executes code when a condition is True                 | `if condition: print("True condition")`                               |
| if-else        | Provides an alternative when the condition is False    | `if condition: print("True") else: print("False")`                    |
| if-elif-else   | Evaluates multiple conditions sequentially             | `if a: ... elif b: ... else: ...`                                     |
| Nested if      | Allows deeper inspection by placing an if within an if | `if age>=18: if age==18: print("Exactly 18") else: print("Above 18")` |

## Conclusion

This guide covered the fundamentals of conditional statements in Python. We examined the basic `if` statement, introduced the alternative `else` clause, explored chaining multiple conditions with `elif`, and demonstrated how to nest conditionals for refined control. These techniques form the backbone of decision-making in Python programming.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-basics/module/87023015-df32-4bcb-a972-659f3e76b1d1/lesson/e7879232-5ea5-4756-8d45-a08390b9f684" />
</CardGroup>
