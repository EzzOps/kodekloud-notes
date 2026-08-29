# main.py
print('hello world!'.capitalize())
print('12 bananas'.capitalize())
print('αβγδ'.capitalize())
print(' Hello!'.capitalize())

print('hello'.center(9))
print('hello'.center(9, '*'))
print('1234'.center(10, '0'))
print('1234'.center(10))
```

Console output:

```text theme={null}
Hello world!
12 bananas
Αβγδ
hello!
  hello  
**hello**
0001234000
   1234
```

## Endswith and Startswith

The `endswith` and `startswith` methods are used to verify whether a string ends or begins with a specified substring, respectively. Both methods return `True` or `False`.

Example usage:

```python theme={null}
print('hello world!'.endswith('!'))
print('hello world!'.endswith('world!'))
print('hello world!'.endswith('hello'))
print('hello world!'.endswith('world'))

print('hello world!'.startswith('hello'))
print('hello world!'.startswith('Hello'))
print('hello world!'.startswith('h'))
print('hello world!'.startswith('world'))
```

Expected output:

```text theme={null}
True
True
False
False
True
False
True
False
```

## Find and rfind

The `find` method returns the index of the first occurrence of a substring, and it returns `-1` if the substring is not found. You can also specify start and end indices for the search. Conversely, the `rfind` method searches from the right side of the string.

Example usage:

```python theme={null}
print('hello world!'.find('h'))
print('hello world!'.find('world'))
print('hello world!'.find('o'))
print('hello world!'.find('x'))
print('hello world!'.find('r', 4, 10))
print('hello world!'.find('r', 1, 4))
print('hello world!'.find('h', 3))
```

Searching from the right:

```python theme={null}
print('hello world!'.rfind('o'))
```

## Alphanumeric, Alphabetic, and Digit Checks

Python provides several methods to check the composition of strings:

* `isalnum()`: Returns `True` if all characters are alphanumeric.
* `isalpha()`: Returns `True` if all characters are letters.
* `isdigit()`: Returns `True` if all characters are digits.

Example usage:

```python theme={null}
print('python'.isalnum())
print('johndoe98@email.com'.isalnum())

print('Hello world!'.isalpha())
print('Hello'.isalpha())

print('1998'.isdigit())
print('1998/04/06'.isdigit())
```

Expected output:

```text theme={null}
True
False
False
True
True
False
```

## Case and Whitespace Checks

The following methods are used to verify the case of characters or the presence of whitespace:

* `islower()`: Returns `True` if all alphabetic characters are lowercase.
* `isupper()`: Returns `True` if all alphabetic characters are uppercase.
* `isspace()`: Returns `True` if the string consists solely of whitespace characters.

Example usage:

```python theme={null}
print('hello world'.islower())
print('Hello world'.islower())

print('hello world'.isupper())
print('HELLO WORLD'.isupper())

print('hello world'.isspace())
print(' '.isspace())
```

Expected output:

```text theme={null}
True
False
False
True
False
True
```

## Join and Split

### Join

The `join` method concatenates an iterable of strings using the string on which it is invoked as a separator. Ensure every element in the list is a string.

Example usage:

```python theme={null}
print(' '.join(['apple', 'kiwi', 'pear']))
print('!'.join(['apple', 'kiwi', 'pear']))
print(''.join(['apple', 'kiwi', 'pear']))
```

Expected output:

```text theme={null}
apple kiwi pear
apple!kiwi!pear
applekiwipear
```

### Split

The `split` method breaks a string into a list of substrings using a specified delimiter. If no delimiter is provided, it splits the string at whitespace.

Example usage:

```python theme={null}
print('apple kiwi pear'.split())
print('apple n kiwi n pear'.split())
print('apple kiwi pear'.split('kiwi'))
```

Expected output:

```text theme={null}
['apple', 'kiwi', 'pear']
['apple', 'kiwi', 'pear']
['apple ', ' pear']
```

## Lower and Upper

The `lower` method converts all uppercase letters in a string to lowercase, while the `upper` method converts all lowercase letters to uppercase.

Example usage for lowercase conversion:

```python theme={null}
print('Hello world!'.lower())
print('lowercase already'.lower())
print('User Input'.lower())
```

Expected output:

```text theme={null}
hello world!
lowercase already
user input
```

Example usage for uppercase conversion:

```python theme={null}
print('Hello world!'.upper())
print('UPPERCASE ALREADY'.upper())
print('User Input'.upper())
```

Expected output:

```text theme={null}
HELLO WORLD!
UPPERCASE ALREADY
USER INPUT
```

## Stripping Whitespace and Characters

Python provides three primary methods to remove characters from strings:

* `lstrip()`: Removes leading whitespace or specified characters.
* `rstrip()`: Removes trailing whitespace or specified characters.
* `strip()`: Removes both leading and trailing whitespace or specified characters.

### Using lstrip

Example usage:

```python theme={null}
print(' Hello world!'.lstrip())
print('www.kodekloud.com'.lstrip('w.'))
```

Expected output:

```text theme={null}
Hello world!
kodekloud.com
```

### Using rstrip

Example usage:

```python theme={null}
print('Hello world! '.rstrip())
print('www.kodekloud.com'.rstrip('.com'))
```

Expected output:

```text theme={null}
Hello world!
www.kodekloud
```

### Using strip

Example usage:

```python theme={null}
print(' Hello world! '.strip())
print('*123456789000'.strip('0'))
```

Expected output:

```text theme={null}
Hello world!
*123456789
```

## Replace, Swapcase, and Title

### Replace

The `replace` method generates a new string by replacing all occurrences of a specified substring with another substring. You can also limit the number of replacements by providing an optional third parameter.

Example usage:

```python theme={null}
print('That is great'.replace('great', 'bad'))
print('123456789'.replace('123', ''))
print('Replace all spaces'.replace(' ', '-'))
```

Expected output:

```text theme={null}
That is bad
456789
Replace-all-spaces
```

### Swapcase

The `swapcase` method swaps the case of each letter in the string, so uppercase becomes lowercase and vice versa.

Example usage:

```python theme={null}
print('I am SO happy!'.swapcase())
```

Expected output:

```text theme={null}
i AM so HAPPY!
```

### Title

The `title` method capitalizes the first character of every word and converts the rest to lowercase.

Example usage:

```python theme={null}
print('python has GREAT methods!'.title())
```

Expected output:

```text theme={null}
Python Has Great Methods!
```

That concludes our comprehensive guide on Python string methods. Start practicing these methods in your coding exercises and projects to improve your string manipulation skills. For more Python tutorials and examples, check out additional [Python documentation](https://www.python.org/doc/).

- [Watch Video](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/2c9c597a-cb2d-43ca-ba29-2dc1b630cae6/lesson/fb2e2b3f-9e59-4c15-aa80-d4dda7721f15)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/2c9c597a-cb2d-43ca-ba29-2dc1b630cae6/lesson/2e06ee69-6162-4f46-92fe-c70d879ed072)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Postman-Essentials/Introduction/Course-Introduction/page

This course provides an introduction to using Postman for API testing, covering basics to advanced techniques for efficient workflows.

Hello, and welcome to the course!

My name is Sanjeev Thiyagarajan, and I will be your instructor throughout this journey.

In this tutorial, we will dive deep into Postman—a robust tool used for testing APIs by generating custom HTTP requests. Think of Postman as an enhanced version of curl, augmented with a host of features that simplify the process of API testing.

We'll start by covering the basics:

* How to test a simple API using Postman
* How to perform various CRUD operations

After establishing a solid foundation, we’ll move on to more advanced topics such as:

* API authentication techniques
* Utilizing variables to streamline API testing workflows
* Leveraging scripts to automate testing tasks for better efficiency
* Setting up multiple environments to switch seamlessly between production and development settings

> **lightbulb** This course is designed to be both enjoyable and informative. Whether you're new to API testing or seeking to expand your technical skills, you'll find valuable insights throughout the lessons.

Let's get started on this exciting journey into API testing with Postman!

- [Watch Video](https://learn.kodekloud.com/user/courses/postman-essentials/module/20544a14-92cc-44ea-9aa0-4e2953ad6ca1/lesson/1929b7b8-69bf-4316-bf39-30060ee5ea7f)
