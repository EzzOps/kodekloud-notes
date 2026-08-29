# Demo 2 Get method

Source: https://notes.kodekloud.com/docs/Advanced-Golang/API-Development-Project/Demo-2-Get-method/page

Implementing a Go HTTP GET endpoint to fetch all products and a single product by ID using database/sql and gorilla/mux with proper error handling and parameterized queries

In this lesson we add a GET route that returns a single product by its ID as JSON. The following sections present the product model, helper functions to fetch all products and a single product from the database, the HTTP handler, and how to register the routes in your application. Code examples assume a standard Go web app using database/sql and gorilla/mux.

Key topics covered:

* product model and querying all products
* parameterized single-row query to fetch a product by ID
* HTTP handler for GET /product/
* route registration

Useful references:

* [database/sql package docs](https://pkg.go.dev/database/sql)
* [gorilla/mux](https://github.com/gorilla/mux)
* [strconv package docs](https://pkg.go.dev/strconv)

## Product model and getProducts (fetch all)

Define the `product` struct and a helper function to return all products from the database. This function uses a simple SELECT and scans the rows into a slice of products.

```go theme={null}
import (
    "database/sql"
)

type product struct {
    ID       int     `json:"id"`
    Name     string  `json:"name"`
    Quantity int     `json:"quantity"`
    Price    float64 `json:"price"`
}

func getProducts(db *sql.DB) ([]product, error) {
    query := "SELECT id, name, quantity, price FROM products"
    rows, err := db.Query(query)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    products := []product{}
    for rows.Next() {
        var p product
        err := rows.Scan(&p.ID, &p.Name, &p.Quantity, &p.Price)
        if err != nil {
            return nil, err
        }
        products = append(products, p)
    }

    if err = rows.Err(); err != nil {
        return nil, err
    }

    return products, nil
}
```

Example response returned by `/products` (for reference):

```json theme={null}
[
  {
    "id": 1,
    "name": "chair",
    "quantity": 100,
    "price": 200
  },
  {
    "id": 2,
    "name": "desk",
    "quantity": 800,
    "price": 600
  }
]
```

## Register routes

Register the routes for listing all products and fetching a single product by ID. This assumes your `App` struct includes `Router *mux.Router` and `DB *sql.DB`, and that the handler methods are defined on `App`.

```go theme={null}
func (app *App) handleRoutes() {
    app.Router.HandleFunc("/products", app.getProducts).Methods("GET")
    app.Router.HandleFunc("/product/{id}", app.getProduct).Methods("GET")
}
```

Table — Routes overview

| Route         | Description               | Response                            |
| ------------- | ------------------------- | ----------------------------------- |
| GET /products | Returns all products      | 200 OK, JSON array                  |
| GET /product/ | Returns one product by ID | 200 OK JSON or 400/404/500 on error |

## Fetch a single product (model method)

Create a method on `product` that populates the struct fields based on the product `ID`. Always use parameterized queries to avoid SQL injection. The placeholder token depends on your SQL driver (e.g., `?` for MySQL, `$1` for Postgres). The example below uses `?`—adjust for your driver accordingly.

```go theme={null}
import (
    "database/sql"
)

func (p *product) getProduct(db *sql.DB) error {
    // Use a parameterized query. Placeholder depends on the driver.
    query := "SELECT name, quantity, price FROM products WHERE id = ?"
    row := db.QueryRow(query, p.ID)
    err := row.Scan(&p.Name, &p.Quantity, &p.Price)
    if err != nil {
        return err
    }
    return nil
}
```

> **lightbulb** When using database/sql, prefer QueryRow with arguments rather than formatting values into the SQL string. This avoids SQL injection and is safer.

## Handler: GET /product/

The handler extracts the `{id}` path variable using `mux.Vars`, converts it to an integer with `strconv.Atoi`, constructs a `product{ID: key}`, calls the model method, and returns the appropriate HTTP response:

* 400 Bad Request when the path parameter is missing or not an integer.
* 404 Not Found when no matching row exists.
* 500 Internal Server Error for other DB errors.
* 200 OK with the product JSON on success.

```go theme={null}
import (
    "database/sql"
    "errors"
    "net/http"
    "strconv"

    "github.com/gorilla/mux"
)

func (app *App) getProduct(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    keyStr, ok := vars["id"]
    if !ok {
        sendError(w, http.StatusBadRequest, "invalid product ID")
        return
    }

    key, err := strconv.Atoi(keyStr)
    if err != nil {
        sendError(w, http.StatusBadRequest, "invalid product ID")
        return
    }

    p := product{ID: key}
    err = p.getProduct(app.DB)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            sendError(w, http.StatusNotFound, "Product not found")
        } else {
            sendError(w, http.StatusInternalServerError, err.Error())
        }
        return
    }

    sendResponse(w, http.StatusOK, p)
}
```

Notes:

* `sendError` and `sendResponse` are utility helpers that should write JSON responses and set the proper Content-Type and status code.
* The `getProduct` method uses a pointer receiver so the handler can return the populated `product` value directly.

Example implementations for utility functions (not required, but typically like):

```go theme={null}
// sendError writes {"error": "<message>"} with the given status code.
func sendError(w http.ResponseWriter, code int, message string) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(code)
    fmt.Fprintf(w, `{"error":"%s"}`, message)
}

// sendResponse writes the value as JSON with the given status code.
func sendResponse(w http.ResponseWriter, code int, v interface{}) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(code)
    json.NewEncoder(w).Encode(v)
}
```

## Example requests and responses

* GET a valid product:
  * Request: `GET http://localhost:10000/product/1`
  * Response 200:
    ```json theme={null}
    {
      "id": 1,
      "name": "chair",
      "quantity": 100,
      "price": 200
    }
    ```

* GET with an invalid integer ID:
  * Request: `GET http://localhost:10000/product/abc`
  * Response 400:
    ```json theme={null}
    {
      "error": "invalid product ID"
    }
    ```

* GET a non-existent product ID:
  * Request: `GET http://localhost:10000/product/10`
  * Response 404:
    ```json theme={null}
    {
      "error": "Product not found"
    }
    ```

Summary

With the model method, handler, and routes above wired into your application, you will have:

* /products — returns all products as JSON
* /product/ — retrieves a single product by ID with proper error handling and secure parameterized queries

For more best practices and production considerations, see:

* [database/sql best practices](https://pkg.go.dev/database/sql)
* [gorilla/mux route variables](https://github.com/gorilla/mux)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-golang/module/483ddd82-96d2-43d5-a9a8-e27e8cdb064d/lesson/07de5bcd-e155-4548-905b-425082094501)
