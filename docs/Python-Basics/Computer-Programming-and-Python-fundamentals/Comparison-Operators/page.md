# The cost of an apple in USD
# This value should always be an integer
>>> cost_of_apple = 5
```

<Callout icon="lightbulb">
  While detailed comments improve understanding, it's best to maintain self-documenting code. Use meaningful variable names and clear code structure to reduce the need for excessive comments.
</Callout>

Comments are also useful for temporarily disabling parts of your code. For example, if you comment out the assignment to the `cost_of_apple` variable, Python will skip creating it. Any subsequent operation that references `cost_of_apple` will trigger an error. Consider the snippet below:

```python theme={null}
>>> amount_of_apples = 2
>>> # cost_of_apple = 5
>>> print(amount_of_apples * cost_of_apple)
NameError: name 'cost_of_apple' is not defined
```

In summary, comments are a vital tool for enhancing code clarity and providing additional context for code functionality. However, always strive for simplicity by writing self-explanatory code that minimizes the need for excessive inline comments.

That's it for now. It's time to gain some hands-on practice.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-basics/module/4178f96e-8dcd-46a2-a9c9-f65a8c9c73b0/lesson/b257316f-9014-4f65-b602-38ff01d4ef1c" />
</CardGroup>


# Comparison Operators

Source: https://notes.kodekloud.com/docs/Python-Basics/Computer-Programming-and-Python-fundamentals/Comparison-Operators/page

Overview of Python comparison operators and how they produce boolean results for controlling program flow in conditionals and expressions

Previously we explored logical operators. This article introduces comparison operators — a separate category of operators used to compare values in Python. Comparison operators are fundamental for branching and looping (for example, in if and while statements) and return boolean results (True or False).

There are six comparison operators in Python:

| Operator | Meaning                  | Example  |
| -------: | ------------------------ | -------- |
|     `==` | equal to                 | `2 == 2` |
|     `!=` | not equal to             | `2 != 4` |
|      `>` | greater than             | `4 > 2`  |
|     `>=` | greater than or equal to | `4 >= 4` |
|      `<` | less than                | `2 < 4`  |
|     `<=` | less than or equal to    | `2 <= 2` |

These operators compare values and yield boolean results that are commonly used in control flow and expressions.

## Equal (==)

Checks whether two values are equal.

```python theme={null}
print(2 == 2)               # True
print(2 == 4)               # False
print("Hello!" == "Hello!") # True
print("Hello!" == "Goodbye!") # False
print(4 == (2 * 2))         # True
```

## Not equal (!=)

Returns True when the two values are different.

```python theme={null}
print(2 != 2)               # False
print(2 != 4)               # True
print("Hello!" != "Hello!") # False
print("Hello!" != "Goodbye!") # True
print(4 != (2 * 2))         # False
```

## Greater than (>)

True if the left-hand operand is greater than the right-hand operand.

```python theme={null}
print(4 > 2)  # True
print(2 > 4)  # False
print(2 > 2)  # False

cost_of_apple = 2
cost_of_banana = 3
print(cost_of_apple > cost_of_banana)  # False
```

## Greater than or equal to (>=)

True if the left-hand operand is greater than or equal to the right-hand operand.

```python theme={null}
print(4 >= 2)  # True
print(2 >= 4)  # False
print(2 >= 2)  # True
```

## Less than (\<)

True if the left-hand operand is less than the right-hand operand.

```python theme={null}
print(4 < 2)  # False
print(2 < 4)  # True
print(2 < 2)  # False

cost_of_apple = 2
cost_of_banana = 3
print(cost_of_apple < cost_of_banana)  # True
```

## Less than or equal to (\<=)

True if the left-hand operand is less than or equal to the right-hand operand.

```python theme={null}
print(4 <= 2)  # False
print(2 <= 4)  # True
print(2 <= 2)  # True
```

<Callout icon="lightbulb">
  Comparison operators are most often used in conditional statements (for example, `if` and `while`) to control program flow. They return `True` or `False`, which you can use directly in conditions. When comparing values, be mindful of types — comparing incompatible types may return `False` or raise a `TypeError` depending on the operation.
</Callout>

<Callout icon="warning">
  Be careful when comparing different types (e.g., strings vs integers). For example, `"10" == 10` is `False`. Use explicit conversion (like `int()` or `str()`) when necessary to avoid unexpected results or runtime errors.
</Callout>

## Quick reference and common patterns

* Use equality (`==`) to check for exact matches.
* Use inequality (`!=`) to exclude specific values.
* Use chained comparisons for concise expressions: `0 < x < 10` is valid and equivalent to `(0 < x) and (x < 10)`.
* Combine comparisons with logical operators (`and`, `or`, `not`) to build complex conditions.

Example of chaining:

```python theme={null}
x = 5
print(0 < x < 10)  # True
```

## References

* [Python Documentation — Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)
* [Python Tutorial — More on Expressions](https://docs.python.org/3/tutorial/introduction.html#numbers)

This concludes the article on comparison operators.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-basics/module/4178f96e-8dcd-46a2-a9c9-f65a8c9c73b0/lesson/67201484-5cee-4377-a872-0e85fd7cd6ee" />
</CardGroup>
