# Comments

Source: https://notes.kodekloud.com/docs/Python-Basics/Computer-Programming-and-Python-fundamentals/Comments/page

This article explains the importance of comments in code for readability, maintainability, and temporarily disabling code sections.

In many cases, code may not be immediately understandable to every team member. To improve code readability and maintainability, you can insert comments into your code by using a hash (#) followed by your description. During runtime, Python completely ignores these comments, meaning they serve solely as documentation for developers or your future self.

When you need to include a multi-line comment, be sure to begin every line with a hash. Omitting the hash on any line may cause Python to interpret the text as executable code, which can result in syntax errors.

Below is an example that demonstrates effective commenting:

```python theme={null}
>>> amount_of_apples = 2  # Amount in basket
