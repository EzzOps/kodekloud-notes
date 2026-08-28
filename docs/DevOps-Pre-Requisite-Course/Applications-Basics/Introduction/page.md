# Update index.php with the correct database address, database name, and credentials
curl http://localhost
```

This configuration deploys the entire stack on a single node. In multi-node environments, the database and web server reside on separate machines, requiring additional connectivity configuration.

***

## Multi-Node Deployment Configuration

For multi-node deployments, host the database server and web server on different nodes. Ensure that the web server’s `index.php` is updated with the correct database server IP, and update database user permissions for remote access. The diagram below illustrates this multi-node setup:

<Frame>
  ![The image illustrates a multi-node deployment model with two servers, one running MariaDB and the other running Apache and PHP.](https://kodekloud.com/kk-media/image/upload/v1752873404/notes-assets/images/DevOps-Pre-Requisite-Course-KodeKloud-E-Commerce-Application/frame_260.jpg)
</Frame>

Update the database user to allow access from the web server's IP address:

```sql theme={null}
mysql
MariaDB > CREATE DATABASE ecomdb;
MariaDB > CREATE USER 'ecomuser'@'172.20.1.102' IDENTIFIED BY 'ecompassword';
MariaDB > GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'172.20.1.102';
MariaDB > FLUSH PRIVILEGES;
```

Modify the PHP connection settings accordingly:

```php theme={null}
$link = mysqli_connect('172.20.1.101', 'ecomuser', 'ecompassword');
if ($link) {
    $res = mysqli_query($link, "SELECT * FROM products;");
    while ($row = mysqli_fetch_assoc($res)) {
        // Process each product record
    }
}
```

<Callout icon="triangle-alert">
  Always ensure that user permissions and access control settings are securely configured when allowing remote connections.
</Callout>

***

## Code Explanation: HTML/PHP for Displaying Products

The `index.php` file is responsible for connecting to the MariaDB database and retrieving product data for display on the website. Below is a snippet demonstrating the database connection and data retrieval process:

```php theme={null}
$link = mysqli_connect('172.20.1.101', 'ecomuser', 'ecompassword', 'ecomdb');

if ($link) {
    $res = mysqli_query($link, "SELECT * FROM products;");
    while ($row = mysqli_fetch_assoc($res)) { 
?>
<div class="col-md-3 col-sm-6 business_content">
    <?php echo '<img src="img/' . $row['ImageUrl'] . '" alt="">'; ?>
    <div class="media">
        <div class="media-left">
        </div>
        <div class="media-body">
            <a href="#"><?php echo $row['Name']; ?></a>
            <p>Purchase <?php echo $row['Name']; ?> at the lowest price <span><?php echo $row['Price']; ?>$</span></p>
        </div>
    </div>
</div>
<?php 
    } 
}
```

This snippet establishes a secure connection to the database and retrieves product records to display on the front end. Modify the host, credentials, and database names as necessary to match your environment.

***

## Demonstration

The example below reiterates how the PHP code connects to the database and retrieves product records, reinforcing the concepts discussed:

```php theme={null}
$link = mysqli_connect('172.20.1.101', 'ecomuser', 'ecompassword', 'ecomdb');
if ($link) {
    $res = mysqli_query($link, "SELECT * FROM products;");
    while ($row = mysqli_fetch_assoc($res)) { 
        // Your code here to process and display each product
    }
}
```

After reviewing this demo, proceed to the project labs to set up your environment and apply your new skills.

***

This guide provided a complete walkthrough for deploying a LAMP stack application for the KodeKloud e-commerce website, covering both single-node and multi-node configurations. Enjoy setting up your lab environment and exploring the project!

***

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [MariaDB Official Site](https://mariadb.org/)
* [Apache HTTP Server](https://httpd.apache.org/)
* [PHP Official Site](https://www.php.net/)
* [GitHub](https://github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/2608518c-d8a5-4ee7-8089-e53c93b30abc/lesson/19df4649-073f-4bbe-9249-1ac10b2bb09f" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Applications-Basics/Introduction/page

This lesson explores application fundamentals from operations and software development perspectives, emphasizing development, deployment, and troubleshooting with hands-on labs.

In this lesson, we explore the fundamentals of applications from both an operations and software development perspective. As a DevOps engineer, you must be adept at performing operational tasks and understanding the principles behind application development. Rather than focusing on advanced coding techniques, this lesson emphasizes how applications are developed, built, deployed, and troubleshooted. Every lecture is paired with hands-on labs that allow you to practice with real-world application source code.

We will also examine the compilation process, discuss what constitutes source code, and explain how it is transformed into machine code. This high-level overview aims to demystify the various stages involved in modernizing and containerizing applications in DevOps and cloud environments.

There are countless programming languages available today. For this discussion, we focus on a few of the most popular languages based on insights from the Stack Overflow 2019 survey. Consider the following diagram which lists popular languages:

<Frame>
  ![The image shows a list of popular programming languages, with JavaScript, Python, and Java highlighted, alongside a bar chart from a Stack Overflow survey.](https://kodekloud.com/kk-media/image/upload/v1752873405/notes-assets/images/DevOps-Pre-Requisite-Course-Introduction/frame_130.jpg)
</Frame>

From the survey, after filtering out databases, scripting, and markup languages, JavaScript, Python, and Java emerge as the front runners. For JavaScript-based server-side applications, we will use the Node.js framework.

Applications can be built using either compiled or interpreted programming languages. Understanding these differences from a DevOps perspective is essential, as it impacts how you build, test, and deploy applications.

<Frame>
  ![The image categorizes programming languages into compiled (Java, C, C++) and interpreted (Python, Node.js, Ruby, Perl) types.](https://kodekloud.com/kk-media/image/upload/v1752873406/notes-assets/images/DevOps-Pre-Requisite-Course-Introduction/frame_170.jpg)
</Frame>

## Compiled Languages

Languages such as Java, C, and C++ follow a two-step process. First, you write the source code and then compile it into machine code. For example, consider the following simple Java program:

Save the code in a file named `MyClass.java`:

```java theme={null}
public class MyClass {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

Compile the source code with:

```bash theme={null}
javac MyClass.java
```

This command generates a compiled file named `MyClass.class`. Finally, run the program using:

```bash theme={null}
java MyClass
```

The output will be:

```plaintext theme={null}
Hello World
```

## Interpreted Languages

In contrast, interpreted languages like Python execute the source code directly using an interpreter, eliminating the explicit compilation step. Consider this sample Python application:

Save the code in a file named `main.py`:

```python theme={null}
def print_message():
    print("Hello World")

if __name__ == '__main__':
    print_message()
```

Execute the program using:

```bash theme={null}
python main.py
```

The output will be:

```plaintext theme={null}
Hello World
```

<Callout icon="lightbulb">
  Although languages like Python do not require manual compilation, the Python interpreter internally compiles the source code into an intermediate bytecode (stored as a `.pyc` file). This bytecode is then executed by the Python Virtual Machine (VM), which converts it into machine code that your computer can process.
</Callout>

Below is an illustration of how Python source code is transformed into bytecode and then executed as machine code:

```python theme={null}
