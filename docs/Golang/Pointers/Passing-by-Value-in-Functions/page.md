# Passing by Value in Functions

Source: https://notes.kodekloud.com/docs/Golang/Pointers/Passing-by-Value-in-Functions/page

This article explores passing arguments by value in functions, explaining how modifications to parameters do not affect the original variables.

In this lesson, we explore the concept of passing arguments by value in functions. There are two primary methods for passing arguments: passing by value and passing by reference. In this guide, our focus is on passing by value.

Passing by value means that when you pass a variable to a function, its value is copied to a new memory location. Any modifications made to the parameter within the function affect only the copy, leaving the original variable unchanged. Basic data types such as integers, floats, booleans, and strings are all passed by value.

<Callout icon="lightbulb">
  When a variable is passed by value, its original location in memory remains unchanged even if the function alters the copied parameter.
</Callout>

## Memory Layout Example

Consider a scenario where a variable `a` is declared inside the `main` function. The variable `a` is stored in memory at a particular address. When `a` is passed to the function `modify`, the value is copied to another memory location. As a result, any modification within `modify` does not impact the original value of `a`.

Imagine a memory layout as shown below:

```text theme={null}
memory address     memory
0x0301            10
0x0302
0x0303
0x0304
0x0305
0x0306
```

In this example, when the function adds 100 to the copy of the variable, the original value of `a` remains 10.

## Go Code Example: Integers

Below is a Go code snippet that demonstrates passing by value with integer data:

```go theme={null}
package main

import "fmt"

func modify(a int) {
    a += 100
}

func main() {
    a := 10
    fmt.Println(a) // Output: 10
    modify(a)
    fmt.Println(a) // Output: 10, since a is passed by value
}
```

As shown, the original value of `a` remains unchanged after the `modify` function is called.

## Go Code Example: Strings

Now consider an example with a string. In this case, a string variable is created with the value `"hello"`. The string is printed, passed to a function called `modify` that attempts to change its value to `"world"`, and then printed again. Despite the change within the function, the original string remains `"hello"` because it was passed by value.

```go theme={null}
package main

import "fmt"

func modify(s string) {
    s = "world"
}

func main() {
    a := "hello"
    fmt.Println(a) // Output: hello
    modify(a)
    fmt.Println(a) // Output: hello, since s is only a copy of a
}
```

Console output:

```console theme={null}
>>> go run main.go
hello
hello
```

In this case, the parameter `s` inside the `modify` function is simply a copy of the variable `a`. Thus, when `s` is updated to `"world"`, the original variable `a` remains unchanged.

<Callout icon="lightbulb">
  Passing by value means that a copy of the variable is provided to the function. Any changes to the parameter inside the function do not alter the original variable outside the function.
</Callout>

That concludes our lesson on passing by value in functions. In the next lesson, we will continue exploring more advanced programming concepts.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/ee351938-02d0-4200-ac8f-78b0da517e29/lesson/303f4170-f4b5-4d41-a8f8-01591c8fbb2f" />
</CardGroup>
