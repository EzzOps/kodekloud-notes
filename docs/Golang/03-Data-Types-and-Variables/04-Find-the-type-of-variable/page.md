# Find the type of variable

Source: https://notes.kodekloud.com/docs/Golang/Data-Types-and-Variables/Find-the-type-of-variable/page

Learn to determine the data type of a variable in Go using `%T` and the reflect package’s TypeOf function.

In this article, you'll learn how to determine the data type of a variable in Go. We cover two primary techniques: using the `%T` format specifier with fmt.Printf and using the reflect package’s TypeOf function, which can also handle literal values.

***

## Using the `%T` Format Specifier

The simplest way to discover a variable's data type in Go is by using the `%T` format specifier with fmt.Printf. In the example below, four variables of different types (integer, string, boolean, and float) are declared. Their values and corresponding data types are then printed.

```go theme={null}
package main
import "fmt"

func main() {
    var grades int = 42
    var message string = "hello world"
    var isCheck bool = true
    var amount float32 = 5466.54

    fmt.Printf("variable grades = %v is of type %T \n", grades, grades)
    fmt.Printf("variable message = '%v' is of type %T \n", message, message)
    fmt.Printf("variable isCheck = %v is of type %T \n", isCheck, isCheck)
    fmt.Printf("variable amount = %v is of type %T \n", amount, amount)
}
```

To run the above program, use the following command:

```bash theme={null}
go run main.go
```

The expected output will be:

```text theme={null}
variable grades = 42 is of type int
variable message = 'hello world' is of type string
variable isCheck = true is of type bool
variable amount = 5466.54 is of type float32
```

***

## Using the reflect.TypeOf Function with Literals

The reflect package's `TypeOf` function is a powerful alternative that works with both variables and literals. In this example, the code shows how to determine the data types of various literals.

```go theme={null}
package main

import (
    "fmt"
    "reflect"
)

func main() {
    fmt.Printf("Type: %v \n", reflect.TypeOf(1000))
    fmt.Printf("Type: %v \n", reflect.TypeOf("priyanka"))
    fmt.Printf("Type: %v \n", reflect.TypeOf(46.0))
    fmt.Printf("Type: %v \n", reflect.TypeOf(true))
}
```

Run the program with:

```bash theme={null}
go run main.go
```

The output is as follows:

```text theme={null}
Type: int
Type: string
Type: float64
Type: bool
```

***

## Using the reflect.TypeOf Function with Variables

You can also pass variables into the `reflect.TypeOf` function to determine their data types. The following example declares two variables and prints both their values and their types.

```go theme={null}
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var grades int = 42
    var message string = "hello world"

    fmt.Printf("variable grades = %v is of type %v \n", grades, reflect.TypeOf(grades))
    fmt.Printf("variable message = '%v' is of type %v \n", message, reflect.TypeOf(message))
}
```

Execute the program with:

```bash theme={null}
go run main.go
```

The expected output is:

```text theme={null}
variable grades = 42 is of type int
variable message = 'hello world' is of type string
```

***

<Callout icon="lightbulb">
  Understanding the data type of variables and literals is essential when debugging or optimizing your Go programs.
</Callout>

That’s it for this tutorial. In this lesson, you explored two methods to determine the data type of a variable or a literal in Go using both the `%T` format specifier and the `reflect.TypeOf` function.

Keep practicing and see you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/eeafa284-50db-4de2-a58a-759d3926fced/lesson/3e793374-fc8a-48ab-bf3c-7673b3939555" />
</CardGroup>
