# String Methods

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/String-and-List-Methods/String-Methods/page

This article reviews useful Python string methods for creating new strings without modifying the original, aiding effective string manipulation in projects.

In this article, we review several useful Python string methods that create new strings from a source string without modifying the original. These methods are essential for effective string manipulation in your Python projects and can help you build cleaner and more readable code.

> **lightbulb** All string methods demonstrated here return new string objects. The original strings remain unchanged throughout the transformations.

## Capitalize

The `capitalize` method converts the first character of the string to uppercase (if it's alphabetical) and converts all remaining characters to lowercase.

Example usage:

```python theme={null}
print('hello world!'.capitalize())
print('12 bananas'.capitalize())
print('αβγδ'.capitalize())
print(' Hello!'.capitalize())
```

Expected output:

```text theme={null}
Hello world!
12 bananas
Αβγδ
hello!
```

## Center

The `center` method returns a new string padded with spaces or an optional specified character. The first parameter represents the total width of the resulting string.

Example usage:

```python theme={null}
print('hello'.center(9))
print('hello'.center(9, '*'))
print('1234'.center(10, '0'))
print('1234'.center(10))
```

Expected output:

```text theme={null}
  hello  
**hello**
0001234000
   1234
```

> **lightbulb** When providing a second argument to the `center` method, it uses that character for padding instead of the default space.

## Combined Example for Capitalize and Center

The following example demonstrates using both the `capitalize` and `center` methods in a single script:

```python theme={null}
