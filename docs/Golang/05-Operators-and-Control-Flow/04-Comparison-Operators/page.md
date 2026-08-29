# Output:
# 424
```

Right shift (>>)
Right shifting moves bits to the right, discarding bits shifted out on the right. For unsigned or non-negative signed integers, right shifting by n is equivalent to integer division by 2^n, rounding down.

Example: 212 >> 2

Binary demonstration:

```text theme={null}
212 = 11010100
212 >> 2 = 00110101 = 53
```

Go example:

```go theme={null}
package main

import "fmt"

func main() {
	var x int = 212
	z := x >> 2
	fmt.Println(z) // 53
}
```

<Callout icon="warning">
  Be careful with signed integers and right shifts: the fill behavior for the leftmost bits (sign extension vs. zero fill) depends on the type and implementation. For predictable behavior, use unsigned integers (`uint`, `uint32`, `uint64`) when performing bit-level shifts.
</Callout>

Further reading and references

* [The Go Programming Language Specification — Operators](https://golang.org/ref/spec#Operators)
* [Kubernetes Documentation](https://kubernetes.io/docs/) (for system-level use cases)
* [Binary and Bitwise Operations — Wikipedia](https://en.wikipedia.org/wiki/Bitwise_operation)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/036484d6-1e16-46e2-908d-77e545bde2bf/lesson/fd041fad-e23c-418a-9251-a78316437f74" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/golang/module/036484d6-1e16-46e2-908d-77e545bde2bf/lesson/5d8ca114-b153-4000-9a57-c35e5d27cb07" />
</CardGroup>


# Comparison Operators

Source: https://notes.kodekloud.com/docs/Golang/Operators-and-Control-Flow/Comparison-Operators/page

Explains Go comparison operators, their meanings, type comparability rules, and examples for equality and ordering operations.

Comparison operators compare two operands and return a Boolean value: true or false. Equality operators (==, !=) require operands to be of comparable types (typically the same type or types that the language allows to be compared). Ordering operators (\<, \<=, >, >=) require ordered types such as numeric types and strings. Common comparisons include checking whether two strings match, if two numbers are equal, or if one number is greater than another.

<Frame>
  <img alt="A presentation slide titled &#x22;Comparison Operators&#x22; with bullet points explaining that they compare two operands to yield a Boolean, require same data types, and giving examples (string match, number equality, greater‑than). The slide has a dark background and a small KodeKloud logo in the top-right." />
</Frame>

<Callout icon="warning">
  Not all types are comparable using == and !=. Types such as slices, maps, and functions cannot be compared with equality operators — attempting to do so results in a compile-time error. Structs and arrays are comparable only if all their fields/elements are comparable.
</Callout>

We have the following comparison operators: equal (==), not equal (!=), less than (\<), less than or equal to (\<=), greater than (>), and greater than or equal to (>=).

<Frame>
  <img alt="A dark-themed slide titled &#x22;Comparison Operators&#x22; showing six boxed symbols: ==, !=, <, <=, >, >=. Each symbol is labeled beneath as equal, not equal, less than, less than or equal to, greater than, and greater than or equal to." />
</Frame>

<Callout icon="lightbulb">
  When comparing values in Go, make sure both operands are of comparable types. Use explicit conversions when necessary (for example, converting between int types) and prefer clear, readable comparisons to avoid subtle bugs.
</Callout>

Operator reference

| Operator | Meaning                  | Typical Use Case                     |
| -------- | ------------------------ | ------------------------------------ |
| ==       | equal                    | Compare identical values or strings  |
| !=       | not equal                | Check inequality                     |
| \<       | less than                | Order comparisons (numbers, strings) |
| \<=      | less than or equal to    | Order or boundary checks             |
| >        | greater than             | Order comparisons                    |
| >=       | greater than or equal to | Order or boundary checks             |

Examples

Equal (==)
The equal operator returns true when the two values are equal.

```go theme={null}
package main

import "fmt"

func main() {
	var city string = "Kolkata"
	var city2 string = "Calcutta"
	fmt.Println(city == city2)
}
```

```bash theme={null}
$ go run main.go
false
```

Not equal (!=)
The not-equal operator returns true when the two values are not equal.

```go theme={null}
package main

import "fmt"

func main() {
	var city string = "Kolkata"
	var city2 string = "Calcutta"
	fmt.Println(city != city2)
}
```

```bash theme={null}
$ go run main.go
true
```

Less than (\<)
The less-than operator returns true when the left operand is strictly less than the right operand.

```go theme={null}
package main

import "fmt"

func main() {
	var a, b int = 5, 10
	fmt.Println(a < b)
}
```

```bash theme={null}
$ go run main.go
true
```

Less than or equal to (\<=)
This operator returns true when the left operand is less than or equal to the right operand.

```go theme={null}
package main

import "fmt"

func main() {
	var a, b int = 10, 10
	fmt.Println(a <= b)
}
```

```bash theme={null}
$ go run main.go
true
```

Greater than (>)
The greater-than operator returns true when the left operand is strictly greater than the right operand.

```go theme={null}
package main

import "fmt"

func main() {
	var a, b int = 20, 10
	fmt.Println(a > b)
}
```

```bash theme={null}
$ go run main.go
true
```

Greater than or equal to (>=)
This operator returns true when the left operand is greater than or equal to the right operand.

```go theme={null}
package main

import "fmt"

func main() {
	var a, b int = 20, 20
	fmt.Println(a >= b)
}
```

```bash theme={null}
$ go run main.go
true
```

Links and References

* Go Language Specification — Expressions: [https://golang.org/ref/spec#Comparison\_operators](https://golang.org/ref/spec#Comparison_operators)
* Go Documentation: [https://golang.org/doc/](https://golang.org/doc/)
* Effective Go: [https://golang.org/doc/effective\_go.html](https://golang.org/doc/effective_go.html)

That's it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/036484d6-1e16-46e2-908d-77e545bde2bf/lesson/ea9cf2b6-be7e-4a39-a712-cba0525c0553" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/golang/module/036484d6-1e16-46e2-908d-77e545bde2bf/lesson/501bf696-1e86-4055-993b-bcf4654f1805" />
</CardGroup>
