# Defer Statement

Source: https://notes.kodekloud.com/docs/Golang/Using-Functions/Defer-Statement/page

This article explores the defer statement in Go, which postpones function execution until the surrounding function returns.

In this lesson, we'll explore the defer statement in Go, a powerful feature that postpones a function’s execution until the surrounding function returns. While the arguments for a deferred function call are evaluated immediately, the function itself executes later. This behavior ensures that certain operations, such as resource cleanup, occur right before a function exits.

![The image explains a "defer statement," which delays function execution until the surrounding function returns, with arguments evaluated immediately.](https://kodekloud.com/kk-media/image/upload/v1752877747/notes-assets/images/Golang-Defer-Statement/frame_20.jpg)

## How the Defer Statement Works

Consider the example below with three functions: `printName`, `printRollNo`, and `printAddress`.

* The `printName` function outputs a provided string.
* The `printRollNo` function prints an integer.
* The `printAddress` function prints a string representing an address.

Within the `main` function, the program flow is as follows:

1. The `printName` function is immediately called to print the name "Joe".
2. The `defer` keyword schedules the `printRollNo` function to execute after `main` finishes its other statements.
3. The `printAddress` function is called to print the address "street-32".
4. Once `main` is ready to return, the deferred `printRollNo(23)` call is executed.

> **lightbulb** Even though the argument for `printRollNo(23)` is evaluated immediately, the deferred function call itself is executed only after the `main` function completes.

## Example Code

Below is the complete Go code that demonstrates the usage of the defer statement:

```go theme={null}
package main

import "fmt"

// printName prints the provided name.
func printName(str string) {
    fmt.Println(str)
}

// printRollNo prints the student's roll number.
func printRollNo(rno int) {
    fmt.Println(rno)
}

// printAddress prints the provided address.
func printAddress(addr string) {
    fmt.Println(addr)
}

func main() {
    printName("Joe")
    defer printRollNo(23)
    printAddress("street-32")
}
```

## Running the Program

To execute the program, use the following command in your terminal:

```bash theme={null}
go run main.go
```

The output will be:

```bash theme={null}
Joe
street-32
23
```

### Output Breakdown

1. `printName("Joe")` is executed immediately, displaying `Joe`.
2. The `defer printRollNo(23)` statement schedules `printRollNo` to run after completion of the `main` function.
3. `printAddress("street-32")` executes next, printing `street-32`.
4. When `main` is about to return, the deferred call to `printRollNo(23)` is finally executed, printing `23`.

## Additional Resources

For further details on Go's control flow and function execution, consider visiting these resources:

* [Go Official Documentation](https://golang.org/doc/)
* [Understanding Defer in Go](https://blog.golang.org/defer-panic-and-recover)

That concludes our discussion of the defer statement. Happy coding and enjoy exploring Go's powerful features with your own hands-on exercises!

- [Watch Video](https://learn.kodekloud.com/user/courses/golang/module/71aef76c-bfcd-4e49-926e-fa7fbf73827c/lesson/0cdf9880-940a-4182-a5cb-c90ada749677)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/golang/module/71aef76c-bfcd-4e49-926e-fa7fbf73827c/lesson/4fb9703b-d425-4002-84f0-efb660227193)
