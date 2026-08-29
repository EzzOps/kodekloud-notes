# Arguments

Source: https://notes.kodekloud.com/docs/Python-Basics/Functions/Arguments/page

This article explains how to pass arguments to Python functions, including single and multiple parameters, named parameters, and default values.

In this lesson, we'll explore how to pass values—known as arguments—to a Python function. Arguments allow you to customize a function's behavior by providing it with specific data during invocation.

## Single Parameter Example

Consider a function that multiplies the user's input by a given value. In the example below, the function `input_number` has a single parameter named `num`. When calling this function, you supply an argument (in this case, 10), which is assigned to `num`. The function then multiplies the user's input by this value.

```python theme={null}
def input_number(num):
    return int(input("Enter a number: ")) * num

input1 = input_number(10)
```

If the user enters `12`, the function calculates 12 × 10, resulting in 120.

## Multiple Parameters in Functions

A function can accept multiple parameters that are separated by commas. The order in which you pass the arguments is important because the first argument is assigned to the first parameter, the second to the second, and so on. For example:

```python theme={null}
def input_number(num1, num2):
    return int(input("Enter a number: ")) * num1 - num2

input1 = input_number(10, 20)
```

In this case, `num1` receives the value 10, and `num2` receives 20. So if the user inputs 12, the function computes 12 × 10 and then subtracts 20, resulting in 100.

## Utilizing Named Parameters

To reduce dependency on the order of arguments, you can use named parameters when calling a function. This approach enables you to explicitly assign values to specific parameters, even if they are provided in a different order. For example, to swap the values assigned to `num1` and `num2`, you can call the function like this:

```python theme={null}
def input_number(num1, num2):
    return int(input("Enter a number: ")) * num1 - num2
