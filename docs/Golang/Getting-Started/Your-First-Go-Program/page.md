# Your First Go Program

Source: https://notes.kodekloud.com/docs/Golang/Getting-Started/Your-First-Go-Program/page

This tutorial explains the components of a basic "Hello, World" program in Go step by step.

In this tutorial, we’ll break down a basic "Hello, World" program in Go, explaining each component step by step.

## Package Declaration

The program begins with the package declaration:

package main

This line defines the package name. In Go, every program starts with a package declaration. Packages help organize and reuse code. When building standalone executable programs, the special package "main" is used to indicate the entry point.

## Import Statement

Next is the import statement:

The `import` keyword brings code from external packages into your program. Here, the `"fmt"` package is imported, which provides input and output formatting functions. Note that the package name is enclosed in double quotes, which is the correct syntax in Go.

## Comments

Comments are essential for documenting your code. They are ignored during compilation. In Go, comments can be written in two ways:

### Single-Line Comments

// This is a single line comment.

Single-line comments start with two forward slashes (`//`). They are ideal for brief explanations.

### Multi-Line Comments

/\*
This is a
multi-line comment.
\*/

Multi-line comments are enclosed within `/*` and `*/` and are useful for longer explanations.

## Function Declaration

The next part of the program is the function declaration:

func main()&#x20;

Here’s what happens:

1. **Entry Point**: The `main` function is the entry point of a Go program. When the program runs, the `main` function is executed automatically.
2. **Function Body**: The statements within the curly braces `{ }` define what happens when the program starts.

### Inside the Main Function

Within the `main` function, we have:

fmt.Println("Hello, World")

This statement has three main elements:

1. **Package Name**: `fmt` is the package that provides the necessary functionalities for formatted I/O.
2. **Function Name**: `Println` is a function within the `fmt` package. It prints its argument to the console and adds a newline at the end.
3. **Argument**: `"Hello, World"` is the string that is passed to the `Println` function for output.

When executed, this statement prints "Hello, World" to the console.

## Complete Code Example

Below is the complete code snippet with proper syntax highlighting:

```go theme={null}
package main

import "fmt"

// This is a single line comment.
// Comments are used to explain the code and are ignored by the compiler.

func main() {
    /*
    This is a multi-line comment.
    Multi-line comments span several lines.
    */
    fmt.Println("Hello, World")
}
```

<Callout icon="lightbulb">
  Understanding the structure of a basic Go program is crucial before diving into more complex topics like functions, variables, and data types.
</Callout>

In summary, this article covered the essential parts of a basic Go program: the package declaration, the import statement, single-line and multi-line comments, and the `main` function that serves as the starting point of the program.

Let's proceed to get some hands-on practice and explore more advanced features of Go!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/b8b98ba5-f252-4a84-91c1-c067ab96d656/lesson/c25fb15e-8fcf-49a0-aa58-2bb44c615e9e" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/golang/module/b8b98ba5-f252-4a84-91c1-c067ab96d656/lesson/0805570a-146d-47bc-9411-4071a5084567" />
</CardGroup>
