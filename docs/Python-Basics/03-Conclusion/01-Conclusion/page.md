# Output: 10
```

In this snippet, the numbers 2 and 5 lack explanation. Suppose 2 represents the number of apples you wish to buy, and 5 is the cost per apple. We can introduce variables to clarify these values.

Let's define two variables: `amount_of_apples` for the quantity of apples, and `cost_of_apple` for the price of one apple. Using these variables makes our code self-explanatory:

```python theme={null}
# Defining the variables with contextual names
amount_of_apples = 2
cost_of_apple = 5

# Calculating the total cost using the defined variables
print(amount_of_apples * cost_of_apple)
# Output: 10
```

In this example, each variable has a clear role. The variable names `amount_of_apples` and `cost_of_apple` store the values 2 and 5, respectively.

![The image shows two labeled boxes: "amount\_of\_apples" with value 2, and "cost\_of\_apple" with value 5.](https://kodekloud.com/kk-media/image/upload/v1752883524/notes-assets/images/Python-Basics-Variables/frame_60.jpg)

## Python Variable Naming Conventions

When naming variables in Python, there are specific rules to follow:

* A variable name can include uppercase and lowercase letters, digits, and an underscore.
* It must begin with a letter or an underscore.
* Python is case-sensitive; for instance, `costOfApple` and `CostOfApple` represent two different variables.

Below are examples of valid and invalid variable names.

> **lightbulb** **Valid Variable Names:**

  * amount\_of\_apples
  * cost\_of\_apple
  * \_total\_cost
  * COST\_OF\_APPLE

  **Invalid Variable Names:**

  * am\*unt\_0%\_ap|les
  * c\*st\_0%\_app|e
  * 5apples\_cost

Also, remember that variable names cannot be reserved keywords in Python. If you need a similar name, consider modifying its case.

![The image lists Python reserved keywords, including "False," "None," "True," "and," "elif," "else," "lambda," "return," and "yield," among others.](https://kodekloud.com/kk-media/image/upload/v1752883525/notes-assets/images/Python-Basics-Variables/frame_110.jpg)

![The image shows valid and invalid variable names in programming, highlighting case sensitivity with keywords like "Import" and "import."](https://kodekloud.com/kk-media/image/upload/v1752883527/notes-assets/images/Python-Basics-Variables/frame_120.jpg)

## Updating Variable Values

Variables are mutable, meaning their stored values can change over time. For example, if the price of an apple increases by \$2, you can update the `cost_of_apple` variable accordingly:

```python theme={null}
# Updating the variable to reflect a price increase
cost_of_apple = cost_of_apple + 2
print(amount_of_apples * cost_of_apple)
# With updated cost_of_apple = 7, the output is: 14
```

Python offers a shorthand operator to update variables more concisely. The "+=" operator adds a specified value to the current value of the variable:

```python theme={null}
# Using the '+=' operator for a more concise update
cost_of_apple += 2
print(amount_of_apples * cost_of_apple)
# Output: 14
```

## Shortcut Operators for Efficient Coding

Shortcut operators are available for most arithmetic operations. They help keep your code clean and reduce redundancy. For example, here is a comparison:

| Operation Type | Without Shortcut                         | With Shortcut           |
| -------------- | ---------------------------------------- | ----------------------- |
| Addition       | cost\_of\_apple = cost\_of\_apple + 2    | cost\_of\_apple += 2    |
| Subtraction    | cost\_of\_apple = cost\_of\_apple - 2    | cost\_of\_apple -= 2    |
| Multiplication | cost\_of\_apple = cost\_of\_apple \* 2   | cost\_of\_apple \*= 2   |
| Exponentiation | cost\_of\_apple = cost\_of\_apple \*\* 2 | cost\_of\_apple \*\*= 2 |
| Division       | cost\_of\_apple = cost\_of\_apple / 2    | cost\_of\_apple /= 2    |
| Floor Division | cost\_of\_apple = cost\_of\_apple // 2   | cost\_of\_apple //= 2   |
| Modulus        | cost\_of\_apple = cost\_of\_apple % 2    | cost\_of\_apple %= 2    |

## Summary of Key Points

* Variables store values under a specific name, making code more readable.
* Valid variable names must start with a letter or underscore and include only letters, digits, or underscores.
* Variable names should not overlap with Python's reserved keywords.
* Variables can be reassigned, and shortcut operators simplify the code.

> **lightbulb** That's it for this lesson on variables. Now, try the exercises to reinforce your understanding and elevate your Python programming skills.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-basics/module/4178f96e-8dcd-46a2-a9c9-f65a8c9c73b0/lesson/821807bf-9095-47f4-8ea1-5711778e7939)


# Conclusion

Source: https://notes.kodekloud.com/docs/Python-Basics/Conclusion/Conclusion/page

This article concludes a comprehensive Python course covering fundamentals, advanced topics, and encourages continuous practice for mastery.

Congratulations on reaching the end of this comprehensive Python course!

In this article, we explored the fundamentals of Python, starting with variables, data types, and basic syntax. We then advanced to more complex topics including loops and decision-making with logical operations. Along the way, we examined core Python constructs such as lists, functions, tuples, and dictionaries—each essential for effective programming and problem-solving.

This journey was not just about learning syntax; it was about cultivating a problem-solving mindset and harnessing creativity to address real-world challenges. Your progress through these topics is just the beginning of the expansive possibilities Python offers.

> **lightbulb** Remember, continuous practice and experimentation are the keys to mastery in Python. Engage with exciting projects and challenges to further enhance your skills.

If you're ready to elevate your Python expertise and earn formal recognition, consider enrolling in our [PCAP - Python Certification Course](https://learn.kodekloud.com/user/courses/pcap-python-certification-course). This course is designed to sharpen your skills and prepare you for advanced Python programming opportunities.

Thank you for joining this educational journey. Keep coding, keep exploring, and enjoy all that Python has to offer!

- [Watch Video](https://learn.kodekloud.com/user/courses/python-basics/module/076fa682-e40b-494c-beed-89db7a8102f1/lesson/1a3f288e-1fad-4e66-b05b-75f752648b20)
