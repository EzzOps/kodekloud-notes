# Create a sample file
echo "first line"  > file_sample.txt
echo "second line" >> file_sample.txt
echo "third line"  >> file_sample.txt

# Print only the second line twice
sed '2p' file_sample.txt
```

Output:

```text theme={null}
first line
second line
second line
third line
```

Explanation:

* Line 2 matches `2p`, so it's printed by the script and then automatically once more.

> **lightbulb** Use single quotes (`'`) around sed scripts to prevent the shell from interpreting special characters.

## Suppressing Automatic Printing

To output only the lines you explicitly match, use the `-n` option.

```bash theme={null}
sed -n '2p' file_sample.txt
```

Output:

```text theme={null}
second line
```

> **triangle-alert** Forgetting `-n` can lead to duplicate lines when using print scripts.

## Real-World Example: Filtering Command Output

Extract the third line from the `df -h` display:

```bash theme={null}
df -h
```

```text theme={null}
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       7.7G  2.9G  4.9G  38% /
devtmpfs        486M     0  486M   0% /dev
tmpfs           490M     0  490M   0% /dev/shm
...
```

Apply sed:

```bash theme={null}
df -h | sed -n '3p'
```

Result:

```text theme={null}
tmpfs           490M     0  490M   0% /dev/shm
```

## Working with a Data File

Consider an `employees.txt` file with pipe-delimited records:

![The image shows a text file named "employees.txt" containing a list of employees with details such as name, department, job title, email, and salary.](https://kodekloud.com/kk-media/image/upload/v1752868675/notes-assets/images/Advanced-Bash-Scripting-sed-print/employees-list-details-text-file.jpg)

| Field No. | Field Name    | Description           |
| --------- | ------------- | --------------------- |
| 1         | Record Number | Unique employee ID    |
| 2         | First Name    | Employee's first name |
| 3         | Last Name     | Employee's last name  |
| 4         | Department    | Department name       |
| 5         | Job Title     | Position held         |
| 6         | Email         | Company email address |
| 7         | Salary        | Annual salary in USD  |

To print the fifth record only:

```bash theme={null}
sed -n '5p' employees.txt
```

Output:

```text theme={null}
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
```

## Summary

* sed reads from **stdin** or listed files by default.
* Enclose scripts in single quotes to avoid shell expansion.
* Use addresses (e.g., `2p`) to target specific lines.
* The `-n` option disables automatic printing for precise control.
* Place input files after the script.

In upcoming lessons, we'll cover additional sed commands:

* `d` **delete** lines
* `s` **substitute** text
* `i` **insert** text

## References

* GNU sed Manual: [https://www.gnu.org/software/sed/manual/](https://www.gnu.org/software/sed/manual/)
* Bash Reference Manual: [https://www.gnu.org/software/bash/manual/](https://www.gnu.org/software/bash/manual/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/2d48deee-c9f8-4d65-b92f-f164c06b545c/lesson/e86caf90-4991-40d1-b2a9-a62549eb20ff)


# Creating an API server

Source: https://notes.kodekloud.com/docs/Advanced-Golang/API-Development-Project/Creating-an-API-server/page

This guide explains how to build a RESTful API server using Go, covering project setup, HTTP package exploration, handler registration, and server initialization.

In this guide, we will build a RESTful API server using Go. Follow along as we create a simple server, register endpoints, and serve HTTP requests using Go's built-in "net/http" package.

## Step 1: Setting Up the Project

Start by creating a file named `main.go`. Define your package and main function as shown below:

```go theme={null}
package main

func main() {
}
```

A quick terminal prompt may look like:

```plaintext theme={null}
Desktop/kodekloud/learn via 🐹 v1.19.3
```

## Step 2: Exploring the HTTP Package

To familiarize yourself with the HTTP package, you can use a command-line utility (in our case, "KodeKloud http") to locate relevant documentation:

```plaintext theme={null}
Desktop/codeccloud/learn via 🐱 v1.19.3
> go doc
```

The HTTP package provides both client and server implementations. For example, it includes helper functions:

```go theme={null}
resp, err := http.Get("http://example.com/")
...
resp, err := http.Post("http://example.com/upload", "image/jpeg", &buf)
```

The `ListenAndServe` method initializes an HTTP server. It listens on a specified TCP address and uses a handler to process incoming requests.

## Step 3: Registering Handlers

Below is a sample code snippet that demonstrates how to register handlers for different URL patterns:

```go theme={null}
package main

import (
    "fmt"
    "html"
    "net/http"
)

func main() {
    // Register a handler for the /foo endpoint
    http.Handle("/foo", fooHandler)

    // Register a handler inline for the /bar endpoint
    http.HandleFunc("/bar", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
    })
}
```

You can see detailed documentation for the `ListenAndServe` function by running:

```bash theme={null}
go doc http ListenAndServe
```

This shows that `ListenAndServe` listens on the specified TCP network address and invokes the given handler to serve incoming requests. In cases where the handler is `nil`, the `DefaultServeMux` is used:

```bash theme={null}
go doc http DefaultServeMux
```

> **lightbulb** The `DefaultServeMux` is an HTTP request multiplexer that matches incoming request URLs against registered patterns and invokes the appropriate handler.

## Step 4: Starting the HTTP Server

Initially, set up your HTTP server with a default address (using `localhost` on port `10000`) and a nil handler. Later, you will register your custom endpoints. The basic server code looks like this:

```go theme={null}
import "net/http"

func main() {
    http.ListenAndServe("localhost:10000", nil)
}
```

## Step 5: Creating the Homepage Endpoint

To serve a homepage, register a function via `HandleFunc` that handles requests to the root URL. According to the documentation, `HandleFunc` registers the handler function within the `DefaultServeMux`.

```go theme={null}
import "net/http"

func main() {
    http.HandleFunc("/", homepage)
    http.ListenAndServe("localhost:10000", nil)
}
```

Now, define the `homepage` function. This function accepts an `http.ResponseWriter` and an `*http.Request`. It uses `fmt.Fprintf` to write a formatted response back to the client:

```go theme={null}
func homepage(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Welcome to homepage")
    fmt.Println("Endpoint hit: homepage")
}

func main() {
    http.HandleFunc("/", homepage)
    http.ListenAndServe("localhost:10000", nil)
}
```

> **lightbulb** The `fmt.Fprintf` function writes formatted output to a given writer (`w` in this case). It returns the number of bytes written along with any error encountered.

When you run the program using:

```bash theme={null}
go run main.go
```

The HTTP server will start on `localhost:10000`. Accessing the homepage in a web browser will display "Welcome to homepage", and the server console logs:

```plaintext theme={null}
Endpoint hit: homepage
```

If you later change the endpoint registration from `/` to `/foo`, only the `/foo` endpoint will be active, demonstrating that only registered endpoints produce an output.

## Complete Example

Below is the full example of a simple API server with a registered homepage endpoint:

```go theme={null}
package main

import (
    "fmt"
    "net/http"
)

func homepage(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Welcome to homepage")
    fmt.Println("Endpoint hit: homepage")
}

func main() {
    // Register the homepage handler at the "/foo" endpoint
    http.HandleFunc("/foo", homepage)
    http.ListenAndServe("localhost:10000", nil)
}
```

Run the server with:

```bash theme={null}
go run main.go
```

Expected console output upon hitting the endpoint:

```plaintext theme={null}
Endpoint hit: homepage
```

## Conclusion

You have successfully set up a basic RESTful API server in Go. You now know how to register handlers, serve endpoints, and use Go's HTTP package effectively.

In future lessons, we will add more functionalities and expand our API by introducing additional endpoints and middleware.

![The image shows a web browser displaying a page with the text "Welcome to homepage" on a black background. The URL in the address bar is "localhost:10000/foo".](https://kodekloud.com/kk-media/image/upload/v1752868676/notes-assets/images/Advanced-Golang-Creating-an-API-server/welcome-homepage-black-background.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-golang/module/483ddd82-96d2-43d5-a9a8-e27e8cdb064d/lesson/9b33b9fd-f321-4bc2-bcfe-89921a91ee98)
