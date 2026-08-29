# go: creating new go.mod: module example.com/my-inventory
touch app.go
```

─────────────────────────────

## Step 4: Application Structure and Database Initialization

Open the **app.go** file in your preferred IDE. This file will hold application variables such as the HTTP router, database instance, and methods for setting up routes.

1. **Define the Package and App Struct**

   Start by declaring the package and defining an `App` struct that stores pointers to the HTTP router and the SQL database:

   ```go theme={null}
   package main

   import (
       "database/sql"
       "fmt"
       "log"
       "net/http"

       "github.com/gorilla/mux"
       _ "github.com/go-sql-driver/mysql"
   )

   type App struct {
       Router *mux.Router
       DB     *sql.DB
   }
   ```

2. **Create a Constants File for Database Configuration**

   For better organization, create a file named **constants.go** that will store your database configuration details:

   ```go theme={null}
   package main

   const DbName = "inventory"
   const DbUser = "root"
   const DbPassword = "Priyanka#123"
   ```

3. **Implement the Initialize Method**

   This method constructs the connection string, opens a MySQL connection, and initializes the HTTP router:

   ```go theme={null}
   func (app *App) Initialize() error {
       connectionString := fmt.Sprintf("%v:%v@tcp(127.0.0.1:3306)/%v", DbUser, DbPassword, DbName)

       var err error
       app.DB, err = sql.Open("mysql", connectionString)
       if err != nil {
           return err
       }

       app.Router = mux.NewRouter().StrictSlash(true)
       return nil
   }
   ```

4. **Create the Run Method**

   Define the `Run` method to start the HTTP server. This method listens on a specified address and uses `log.Fatal` to report any server startup errors:

   ```go theme={null}
   func (app *App) Run(address string) {
       log.Fatal(http.ListenAndServe(address, app.Router))
   }
   ```

─────────────────────────────

## Step 5: Main Function and Route Handling

Create a **main.go** file, which will serve as the application's entry point.

1. **Set Up the Main Function**

   Initialize the `App`, set up your HTTP routes, and run the server on a specified address (e.g., "localhost:10000"):

   ```go theme={null}
   package main

   func main() {
       app := App{}
       if err := app.Initialize(); err != nil {
           log.Fatal(err)
       }

       // Register HTTP routes.
       app.handleRoutes()

       // Start the server on localhost at port 10000.
       app.Run("localhost:10000")
   }
   ```

2. **Register HTTP Routes**

   Define the route registration method on the `App` struct. Here, a simple GET route for `/products` is registered, which is handled by the `getProducts` function:

   ```go theme={null}
   func (app *App) handleRoutes() {
       app.Router.HandleFunc("/products", getProducts).Methods("GET")
   }
   ```

> **lightbulb** Remember to implement the `getProducts` handler to process HTTP GET requests for the `/products` route based on your application needs.

─────────────────────────────

## Summary

In this lesson, we covered the following:

* Created a MySQL database and a **Products** table with sample data.
* Set up a new [Golang](https://learn.kodekloud.com/user/courses/golang) module and organized the project into multiple files.
* Built an `App` struct to encapsulate the database connection and HTTP router.
* Implemented the `Initialize` and `Run` methods to manage the MySQL connection and start the HTTP server.
* Registered a sample route for fetching products.

This structured approach lays the foundation for further developing your application with expanded routing and enhanced database operations.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-golang/module/483ddd82-96d2-43d5-a9a8-e27e8cdb064d/lesson/8e429055-beee-4d76-a736-4aaebdf643c9)


# Demo Put method

Source: https://notes.kodekloud.com/docs/Advanced-Golang/API-Development-Project/Demo-Put-method/page

This article explains how to implement a PUT endpoint for updating products in a web application.

In this lesson, we detail how to add a new route for the PUT endpoint to update a specific product. This endpoint follows a structure similar to our GET and POST endpoints, with the PUT HTTP method enabling data updates.

## Updating Route Definitions

Start by updating your application's routing function to include the new PUT route:

```go theme={null}
func (app *App) handleRoutes() {
    app.Router.HandleFunc("/products", app.getProducts).Methods("GET")
    app.Router.HandleFunc("/product/{id}", app.getProduct).Methods("GET")
    app.Router.HandleFunc("/product", app.createProduct).Methods("POST")
    app.Router.HandleFunc("/product/{id}", app.updateProduct).Methods("PUT")
}
```

## Creating the updateProduct Handler

Next, implement the `updateProduct` handler. The first step involves extracting the product ID from the URL, which is necessary to determine which product to update.

```go theme={null}
func (app *App) updateProduct(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    key, err := strconv.Atoi(vars["id"])
    if err != nil {
        sendError(w, http.StatusBadRequest, "invalid product ID")
        return
    }
}
```

Once you have successfully extracted the product ID, decode the user-provided JSON payload to update the product. The process is similar to the one used in the `createProduct` method. For reference, here is the original `createProduct` function:

```go theme={null}
func (app *App) createProduct(w http.ResponseWriter, r *http.Request) {
    var p product
    err := json.NewDecoder(r.Body).Decode(&p)
    if err != nil {
        sendError(w, http.StatusBadRequest, "Invalid request payload")
        return
    }
    err = p.createProduct(app.DB)
    if err != nil {
        sendError(w, http.StatusInternalServerError, err.Error())
        return
    }
    sendResponse(w, http.StatusOK, p)
}
```

For updating a product, the handler decodes the JSON payload and assigns the extracted product ID to the product before calling the `updateProduct` method:

```go theme={null}
func (app *App) updateProduct(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    key, err := strconv.Atoi(vars["id"])
    if err != nil {
        sendError(w, http.StatusBadRequest, "invalid product ID")
        return
    }

    var p product
    err = json.NewDecoder(r.Body).Decode(&p)
    if err != nil {
        sendError(w, http.StatusBadRequest, "Invalid request payload")
        return
    }
    p.ID = key

    err = p.updateProduct(app.DB)
    if err != nil {
        sendError(w, http.StatusInternalServerError, err.Error())
        return
    }
    sendResponse(w, http.StatusOK, p)
}
```

## Database Layer Integration

Update the database layer by adding a new method to handle the update query. Previously, we used the `createProduct` function to insert new products:

```go theme={null}
func (p *product) createProduct(db *sql.DB) error {
    query := fmt.Sprintf("insert into products(name, quantity, price) values('%v', %v, %v)", p.Name, p.Quantity, p.Price)
    result, err := db.Exec(query)
    if err != nil {
        return err
    }
    id, err := result.LastInsertId()
    if err != nil {
        return err
    }
    p.ID = int(id)
    return nil
}
```

Now, create the `updateProduct` method. This function updates the product's attributes based on its ID. Notice the check to ensure that at least one row was affected by the update:

```go theme={null}
func (p *product) updateProduct(db *sql.DB) error {
    query := fmt.Sprintf("update products set name='%v', quantity=%v, price=%v where id=%v", p.Name, p.Quantity, p.Price, p.ID)
    result, err := db.Exec(query)
    if err != nil {
        return err
    }
    rowsAffected, err := result.RowsAffected()
    if err != nil {
        return err
    }
    if rowsAffected == 0 {
        return errors.New("No such row exists")
    }
    return nil
}
```

> **lightbulb** Ensure that your database user has proper permissions for executing update queries and that the table schema matches the fields being updated.

## Testing the PUT Endpoint

After integrating the database update logic, it's time to test the implementation.

1. Build the module and run the executable.
2. Open Postman and create a new PUT request to modify a product.

### Example Scenario: Invalid Payload

If you send a PUT request without a valid JSON payload (e.g., for product with ID 10), you will receive an error response:

*Request:*

```HTTP theme={null}
PUT localhost:10000/product/10
```

*Request Body (empty or invalid):*

```json theme={null}
{
  "error": "Invalid request payload"
}
```

### Example Scenario: Valid Update

Send a valid JSON payload to update an existing product. For instance, updating product ID 2:

*Request:*

```text theme={null}
PUT localhost:10000/product/2
```

*Request Body:*

```json theme={null}
{
  "name": "desk",
  "quantity": 2000,
  "price": 600
}
```

*Response:*

```json theme={null}
{
  "id": 2,
  "name": "desk",
  "quantity": 2000,
  "price": 600
}
```

You can verify the update by fetching all products using the GET `/products` endpoint, which should return a list similar to:

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
        "quantity": 2000,
        "price": 600
    },
    {
        "id": 3,
        "name": "Pens",
        "quantity": 100,
        "price": 10
    }
]
```

> **lightbulb** When the update is successful, verify that the response returns the updated product data and that subsequent GET requests display the updated information.

Happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-golang/module/483ddd82-96d2-43d5-a9a8-e27e8cdb064d/lesson/59a5575f-7f37-4af9-aabb-b76da61db32a)
