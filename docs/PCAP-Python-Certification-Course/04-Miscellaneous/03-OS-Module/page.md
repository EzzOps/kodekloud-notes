# Using the generator
for value in simple_generator():
    print(value)
```

Output:

```plaintext theme={null}
0
1
2
3
4
```

## List Comprehensions and Generator Expressions

List comprehensions provide an elegant and compact method to create lists. Take a look at this example that generates a list of powers of 10 using a traditional for loop:

```python theme={null}
first_list = []
for x in range(5):
    first_list.append(10 ** x)
print(first_list)
```

Output:

```plaintext theme={null}
[1, 10, 100, 1000, 10000]
```

The same result can be achieved more concisely with a list comprehension:

```python theme={null}
second_list = [10 ** x for x in range(10)]
print(second_list)
```

Output:

```plaintext theme={null}
[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
```

You can also incorporate conditional expressions within list comprehensions. For example, to create a list that contains 1 for even numbers and 0 for odd numbers:

```python theme={null}
even_odd_list = [1 if x % 2 == 0 else 0 for x in range(5)]
print(even_odd_list)
```

Output:

```plaintext theme={null}
[1, 0, 1, 0, 1]
```

Generator expressions, similar to list comprehensions, use parentheses instead of square brackets. They generate a generator that can be iterated over when needed, offering an even more memory-efficient approach.

## Lambda Functions

Lambda functions (or anonymous functions) allow you to write small functions in a concise way. They are often used alongside functions like map and filter. Here's a simple lambda function to compute the square of a number:

```python theme={null}
sqr = lambda x: x * x
print(sqr(2))
```

Output:

```plaintext theme={null}
4
```

Lambda functions can also be defined with no arguments or multiple arguments:

```python theme={null}
# Lambda that always returns 10
lambda: 10

# Lambda that adds two numbers
lambda a, b: a + b
```

## Using Lambda with Map and Filter

The map function applies a specified function to every item of an iterable, returning a new iterator with the results. For example, the following code doubles each number in the list using a lambda function:

```python theme={null}
nums = [1, 2, 3]
nums_multiplied = list(map(lambda x: x * 2, nums))
print(nums_multiplied)
```

Output:

```plaintext theme={null}
[2, 4, 6]
```

Similarly, the filter function constructs a new iterator comprising only the items that satisfy a specific condition. Consider this example that filters even and odd numbers from a list:

```python theme={null}
nums = [1, 2, 3, 4, 5, 6, 7]
nums_even = list(filter(lambda x: x % 2 == 0, nums))
nums_odd = list(filter(lambda x: x % 2 != 0, nums))
print(nums_even)
print(nums_odd)
```

Output:

```plaintext theme={null}
[2, 4, 6]
[1, 3, 5, 7]
```

## Closures

Closures in Python allow a function to capture and retain access to variables from its enclosing scope, even when the outer function has finished executing. The following example demonstrates a closure:

```python theme={null}
def outer_fun(x):
    def inner_fun(y):
        return x * y
    return inner_fun

# Create a closure with x bound to 4
var_one = outer_fun(4)
print(var_one(3))
```

Output:

```plaintext theme={null}
12
```

In this case, calling `outer_fun(4)` returns the `inner_fun` function, which retains the value of `x` (equal to 4) in its scope. When `var_one(3)` is invoked, it multiplies 4 by 3, resulting in 12, even though the execution context of `outer_fun` has ended.

> **lightbulb** Closures empower you to write more modular and dynamic code by allowing functions to remember and access data from their defining environment, which is particularly effective in functional programming.

## Summary

In this article, we covered:

* How the range function returns an iterator and its similarity to generators.
* The iterator protocol and its core methods: `__iter__()` and `__next__()`.
* Creating custom iterators and the advantages of using the yield keyword.
* The benefits and syntactic simplicity of list comprehensions and generator expressions.
* The use of lambda functions, and how to apply them with map and filter.
* The concept of closures and their practical applications in maintaining state.

Start practicing these concepts today to enhance your Python programming skills and develop more efficient, readable code.

- [Watch Video](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/f130fee7-a5f4-4c7f-bc8e-ffd6f1b8fdc1/lesson/53cd4396-5579-4c95-9078-e625b72200e2)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/f130fee7-a5f4-4c7f-bc8e-ffd6f1b8fdc1/lesson/b90c699d-2423-4adf-8506-c27e1389cb6c)


# OS Module

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/Miscellaneous/OS-Module/page

Learn to interact with the operating system using Python’s OS module, covering directory management and executing system commands.

In this article, you will learn how to interact with the operating system using Python’s OS module. This comprehensive guide covers obtaining operating system details, creating and listing directories, as well as deleting directories and executing system commands. The examples provided in this guide demonstrate how to use these methods effectively.

## Retrieving Operating System Information

To retrieve information about the current operating system, you can use the `uname` method from the OS module. This method returns an object containing details such as:

* The name of the operating system
* The machine name on the network
* The release and version of the operating system
* The hardware identifier

For instance, the `name` property of this object returns:

* `"POSIX"` for Linux-based systems,
* `"NT"` for Windows, and
* `"Java"` for platforms like Jython.

## Creating Directories

The `mkdir` function allows you to create a new directory by specifying a path. The location of the newly created directory depends on how you specify the path:

* Using just the directory name (or with a leading `./`) creates the directory in the current working directory.
* Prefixing the directory name with `../` creates it in the parent directory.
* Specifying an absolute path (for example, `/python/new_directory`) creates the directory in the designated folder at the root.

Below are some examples:

```bash theme={null}
mkdir new_directory
mkdir ./new_directory
```

*These commands create a directory named "new\_directory" in the current working directory.*

```bash theme={null}
mkdir ../new_directory
```

*This command creates a directory in the parent directory of the current working directory.*

```bash theme={null}
mkdir /python/new_directory
```

*This command creates a directory in the "python" directory located at the root.*

## Listing and Creating Directories with Python

To create a new directory in the current working directory and then list its contents, you can use the following example:

```python theme={null}
import os
os.mkdir("my_new_directory")
print(os.listdir())
```

This code produces output similar to:

```plaintext theme={null}
['_upm', 'main.py', 'my_new_directory']
```

This output shows individual files (which typically include extensions) as well as directories (which generally do not have an extension).

If you need to create a folder that contains subfolders, the `makedirs` method is ideal. It allows you to create nested directories with a single call. For example, the following code snippet creates a directory with a subdirectory, changes into the newly created folder, and lists its contents:

```python theme={null}
import os
os.makedirs("my_new_directory/another_new_directory")
os.chdir("my_new_directory")
print(os.listdir())
```

**Output:**

```plaintext theme={null}
['another_new_directory']
```

To get the absolute pathname of the current working directory, simply use the `getcwd` method.

## Deleting Directories

In addition to file operations, Python's OS module allows you to delete files and directories. To delete an empty directory, use the `rmdir` function. The example below demonstrates how to create an empty directory and then remove it:

```python theme={null}
import os

os.mkdir("my_new_directory")
print(os.listdir())
os.rmdir("my_new_directory")
print(os.listdir())
```

**Output:**

```plaintext theme={null}
['.upm', 'main.py', 'my_new_directory']
['.upm', 'main.py']
```

> **lightbulb** The `rmdir` function works only on directories that exist and are empty. Attempting to delete a directory that contains files or subdirectories will result in an error.

To remove a directory along with all its subdirectories, use the `removedirs` function. For example:

```python theme={null}
import os

os.makedirs("first_dir/second_dir")
print(os.listdir())
os.removedirs("first_dir/second_dir")
print(os.listdir())
```

**Output:**

```plaintext theme={null}
['.upm', 'main.py', 'first_dir']
['.upm', 'main.py']
```

## Executing System Commands

The OS module also provides the `system` method, which allows you to execute shell commands directly from Python. For example, you can create a new directory using a system command as follows:

```python theme={null}
import os
returned_value = os.system("mkdir my_new_directory")
```

The returned value is the exit status of the command: `0` indicates success, while a non-zero value (commonly `1`) indicates an error.

> **lightbulb** When executing system commands, always validate and sanitize any inputs to prevent security risks such as command injection.

## Summary

In this lesson, you learned how to:

* Retrieve operating system information using Python’s OS module.
* Create directories using both `mkdir` and `makedirs`.
* List directory contents using `os.listdir()`.
* Delete directories using `rmdir` and `removedirs`.
* Execute system commands with the `system` method.

Try applying these concepts through practice exercises to deepen your understanding and improve your proficiency with Python’s OS module.

- [Watch Video](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/f130fee7-a5f4-4c7f-bc8e-ffd6f1b8fdc1/lesson/cde38440-8fe4-4223-8235-07a9ebadfaca)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/f130fee7-a5f4-4c7f-bc8e-ffd6f1b8fdc1/lesson/b48c9ec3-5753-4a76-bb85-ecc523e24b3a)
