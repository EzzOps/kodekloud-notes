# Maps

Source: https://notes.kodekloud.com/docs/Golang/Arrays-Slices-and-Maps/Maps/page

This article explores maps in Go, covering their declaration, initialization, value access, updating, deletion, and iteration.

In this article, we'll explore maps in Go. A map is a robust data structure that stores an unordered collection of key-value pairs. Depending on the language, similar structures might be known as associative arrays in PHP, hash tables in Java, or dictionaries in Python. Maps are ideal for quickly retrieving data based on a key, thanks to their efficient implementation using hash tables.

Consider a map that associates language codes with their respective languages. For example, the key "en" might store the value "English", and "hi" could map to "Hindi".

## Declaring a Map

To declare a map in Go, use the `var` keyword along with the map type specification. For instance, to declare a map with string keys and integer values, write:

```go theme={null}
var my_map map[string]int
```

<Callout icon="lightbulb">
  This syntax initializes a nil map. The zero value of a map in Go is nil, meaning it doesn't contain any keys. Trying to add a key-value pair to a nil map will result in a runtime error.
</Callout>

## Adding Values to a Map

Let's observe what happens when we try to add a key-value pair to an uninitialized (nil) map. Consider this example:

```go theme={null}
package main

import "fmt"

func main() {
    var codes map[string]string
    codes["en"] = "English"
    fmt.Println(codes)
}
```

This code will trigger a runtime error:

```Go theme={null}
panic: assignment to entry in nil map
```

Since the map is nil, it cannot accept new key-value pairs until it is properly initialized.

## Initializing a Map with Values

To initialize a map with initial key-value pairs, you can use the shorthand literal syntax:

```go theme={null}
codes := map[string]string{"en": "English", "fr": "French"}
```

In this snippet:

* We declare a map named `codes` using the shorthand declaration operator.
* The map is populated with string keys and values inside curly braces.

You can print the map using:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French"}
    fmt.Println(codes)
}
```

When executed, the output will resemble:

```Go theme={null}
map[en:English fr:French]
```

## Using the make Function

An alternative to direct initialization is to use the built-in `make` function. This function allows you to define the map type and, optionally, an initial capacity:

```go theme={null}
codes := make(map[string]int)
fmt.Println(codes)
```

This code produces the following output:

```Go theme={null}
map[]
```

## Determining the Length of a Map

To obtain the number of key-value pairs in a map, utilize the built-in `len` function:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}
    fmt.Println(len(codes))
}
```

Running this code will display:

```Go theme={null}
3
```

This indicates that the map contains three key-value pairs.

## Accessing Map Values

To access a map value, refer to its key enclosed in square brackets. For instance, to display the values for the keys "en", "fr", and "hi":

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}
    fmt.Println(codes["en"])
    fmt.Println(codes["fr"])
    fmt.Println(codes["hi"])
}
```

When executed, the program prints the corresponding values.

It's important to note that indexing a map in Go returns two values: the value itself and a boolean indicating whether the key exists. The syntax is:

```go theme={null}
value, found := map_name[key]
```

If the key does not exist, `value` will be the zero value for the map’s value type. Consider the following example:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]int{"en": 1, "fr": 2, "hi": 3}
    value, found := codes["en"]
    fmt.Println(found, value)
    value, found = codes["hh"]
    fmt.Println(found, value)
}
```

The output of this code will be:

```Go theme={null}
true 1
false 0
```

For the key "en", the key exists (true) and its value is 1. For the non-existent key "hh", the boolean is false, and the value is 0—the zero value for an integer.

## Adding and Updating Map Entries

Adding a new key-value pair to a map is straightforward; simply assign a value to a new key:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}
    codes["it"] = "Italian"
    fmt.Println(codes)
}
```

This adds the key "it" with the value "Italian". If you assign a new value to an existing key, the map updates that key's value:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}
    codes["en"] = "English Language"
    fmt.Println(codes)
}
```

After running this code, the value for the key "en" will be updated to "English Language".

## Deleting Map Entries

To remove a key-value pair from a map, use the built-in `delete` function. This function takes the map and the key to delete as its arguments:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}
    fmt.Println(codes)
    delete(codes, "en")
    fmt.Println(codes)
}
```

The output will display the map before and after the deletion:

```Go theme={null}
map[en:English fr:French hi:Hindi]
map[fr:French hi:Hindi]
```

As shown, the key-value pair for "en" is removed after calling `delete`.

## Iterating Over a Map

You can iterate over a map using the `range` expression, which retrieves both the key and its associated value. In the example below, each key-value pair is printed on a new line:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{
        "en": "English",
        "fr": "French",
        "hi": "Hindi",
    }
    
    for key, value := range codes {
        fmt.Println(key, "=>", value)
    }
}
```

Running this loop will print all the elements in the map.

## Truncating a Map

Truncating a map involves clearing all its elements. There are two common methods to achieve this:

### Method 1: Deleting Each Key Iteratively

Loop through the map and delete each key:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}

    for key := range codes {
        delete(codes, key)
    }
    fmt.Println(codes)
}
```

This prints:

```Go theme={null}
map[]
```

### Method 2: Re-initializing the Map

Alternatively, reinitialize the map using the `make` function:

```go theme={null}
package main

import "fmt"

func main() {
    codes := map[string]string{"en": "English", "fr": "French", "hi": "Hindi"}
    codes = make(map[string]string)
    fmt.Println(codes)
}
```

The output is again an empty map:

```Go theme={null}
map[]
```

## Conclusion

Maps in Go are versatile and efficient structures for managing key-value pairs. By understanding how to declare, initialize, access, update, and truncate maps, you can effectively manage data in your Go applications. Continue practicing these concepts to master the use of maps.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/d42c8657-2eaa-4e17-8605-277e81ac1176/lesson/1ba283a9-8a13-4f92-b777-91b066419bf9" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/golang/module/d42c8657-2eaa-4e17-8605-277e81ac1176/lesson/e31232d0-aa6c-458a-b45b-4d0c0be7b8ed" />
</CardGroup>
