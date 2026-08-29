# Jinja2 Basics

Source: https://notes.kodekloud.com/docs/Jinja2-Basics-Mini-Course/Jinja2/Jinja2-Basics/page

Introduction to Jinja2 templating covering variables, filters, loops, conditionals, and use in web development and automation such as Ansible

In this lesson we cover the essentials of Jinja2: what templating is, how templates are used in IT automation and web development, and the core syntax for substitutions, filters, loops, and conditionals.

What is templating? Think of an invitation letter: the body (event details, venue, signature) stays the same for all recipients, while the addressee and family member names change. The invitation format is the template and the names are variables. A templating engine takes a template plus variables and renders the final personalized output — one email or hundreds.

<Frame>
  <img alt="The image displays four invitation templates with differing text colors for different recipients, titled &#x22;Templating Engine.&#x22; Each template invites the recipient and their family to a company celebration." />
</Frame>

Templates are widely used in web pages (HTML templates -> rendered HTML) and in automation tools like Ansible (templates -> configuration or files on remote hosts). Jinja2 is the templating engine commonly used in Python projects and many automation frameworks.

<Callout icon="lightbulb">
  Templating helps you reuse structure and separate content/data from presentation. You can render the same template with different data to produce many customized outputs.
</Callout>

## Basic HTML example (Jinja2 template)

Template:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
  <title>&#123;&#123; title &#125;&#125;</title>
</head>
<body>
  &#123;&#123; msg &#125;&#125;
</body>
</html>
```

Variables (YAML):

```yaml theme={null}
title: Our Site
msg: Welcome!
```

Rendered HTML:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
  <title>Our Site</title>
</head>
<body>
  Welcome!
</body>
</html>
```

## Templating in Ansible

Ansible uses Jinja2 extensively for templates and variable interpolation. Example task that touches a file whose path is provided as a variable:

```yaml theme={null}
- hosts: web1
  tasks:
    - file:
        path: "&#123;&#123; file &#125;&#125;"
        state: touch
```

If you supply `file: /tmp/1.txt`, the task will operate on `/tmp/1.txt`.

Templates are also used to generate configuration files. Example Jinja2 template for a MySQL configuration:

```ini theme={null}
[mysqld]
innodb_buffer_pool_size=&#123;&#123; pool_size &#125;&#125;
datadir=&#123;&#123; datadir &#125;&#125;
user=&#123;&#123; mysql &#125;&#125;
```

When `pool_size`, `datadir`, and `mysql` are provided, the template renders into a ready-to-use configuration file for the target host.

For more on Ansible templating, see the Ansible documentation and tutorials such as the KodeKloud course linked below.

* [Ansible Templating Guide (Docs)](https://docs.ansible.com/)
* [Learn Ansible Basics (KodeKloud)](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)

## What is Jinja2?

Jinja2 is a full-featured templating engine for Python. It supports:

* Variable substitution
* Filters to transform values
* Control structures: loops and conditionals
* Blocks and template inheritance
* Macros for reusable snippets

Example using a block and a loop:

```text theme={null}
<title>&#123;% block title &#37;&#125;&#123;% endblock &#37;&#125;</title>
<ul>
&#123;% for user in users &#37;&#125;
  <li><a href="&#123;&#123; user.url &#125;&#125;">&#123;&#123; user.username &#125;&#125;</a></li>
&#123;% endfor &#37;&#125;
</ul>
```

## Variables and Filters

A simple substitution uses `&#123;&#123; variable &#125;&#125;`. Filters modify values using the pipe `|` syntax.

Examples:

```text theme={null}
The name is &#123;&#123; my_name &#125;&#125;             => The name is Bond
The name is &#123;&#123; my_name | upper &#125;&#125;    => The name is BOND
The name is &#123;&#123; my_name | lower &#125;&#125;    => The name is bond
The name is &#123;&#123; my_name | title &#125;&#125;    => The name is Bond
The name is &#123;&#123; my_name | replace("Bond", "Bourne") &#125;&#125; => The name is Bourne
The name is &#123;&#123; first_name | default("James") &#125;&#125; &#123;&#123; my_name &#125;&#125; => The name is James Bond
```

<Callout icon="warning">
  Undefined variables can cause unexpected output. Use `default(...)` or enable strict undefined checks during rendering to catch missing values early.
</Callout>

## Common filters (overview)

| Filter                    | Purpose                               | Example            |                                |          |
| ------------------------- | ------------------------------------- | ------------------ | ------------------------------ | -------- |
| `upper`, `lower`, `title` | Change string case                    | \`\{\{ my\_name    | upper }}\`                     |          |
| `replace(old, new)`       | Replace substrings                    | \`\{\{ my\_name    | replace("Bond", "Bourne") }}\` |          |
| `default(value)`          | Provide fallback for undefined values | \`\{\{ first\_name | default("James") }}\`          |          |
| `join(sep)`               | Join list items into a string         | \`\{\{ my\_list    | join(", ") }}\`                |          |
| `random`                  | Select a random element               | \`\{\{ my\_list    | random }}\`                    |          |
| `unique`                  | Remove duplicates from a list         | \`\{\{ \[1,2,2,3]  | unique }}\`                    |          |
| `min`, `max`              | Minimum/maximum of a list             | \`\{\{ \[1,2,3]    | min }}`/`\{\{ \[1,2,3]         | max }}\` |
| `union(list2)`            | Merge lists and remove duplicates     | \`\{\{ \[1,2]      | union(\[2,3]) }}\`             |          |

## List and set-based filters (examples)

```text theme={null}
&#123;&#123; [1, 2, 3] | min &#125;&#125;         => 1
&#123;&#123; [1, 2, 3] | max &#125;&#125;         => 3
&#123;&#123; [1, 2, 3, 2] | unique &#125;&#125;   => [1, 2, 3]
&#123;&#123; [1, 2, 3, 4] | union([4, 5]) &#125;&#125;    => [1, 2, 3, 4, 5]
```

## Control structures: loops and conditionals

Jinja2 control structures use `&#123;% ... %&#125;` tags. Common constructs:

* For loop:

```text theme={null}
&#123;% for number in [0, 1, 2, 3, 4] %&#125;
&#123;&#123; number &#125;&#125;
&#123;% endfor %&#125;
```

Rendered:

```text theme={null}
0
1
2
3
4
```

* Loop with conditional (print only number equal to 2):

```text theme={null}
&#123;% for number in [0, 1, 2, 3, 4] %&#125;
  &#123;% if number == 2 %&#125;
&#123;&#123; number &#125;&#125;
  &#123;% endif %&#125;
&#123;% endfor %&#125;
```

Rendered:

```text theme={null}
2
```

* If/elif/else example:

```text theme={null}
&#123;% if users | length == 0 %&#125;
  No users found.
&#123;% elif users | length == 1 %&#125;
  One user found.
&#123;% else %&#125;
  Multiple users found.
&#123;% endif %&#125;
```

## Summary

* Jinja2 templates mix static text with placeholders, filters, loops, and conditionals to produce dynamic outputs.
* Use filters to transform values and control structures to repeat or conditionally render content.
* Templating is invaluable in automation (Ansible), configuration management, and web development for reusing structure while rendering variable data.

Further reading and references:

* [Jinja2 Documentation](https://jinja.palletsprojects.com/)
* [Ansible Documentation](https://docs.ansible.com/)
* [Learn Ansible Basics (KodeKloud)](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jinja2-basics-mini-course/module/401d97bc-edbb-4181-bfcf-fb5ed517c34e/lesson/2a3e5aec-cdd6-4325-8b40-f5518b9814d2" />
</CardGroup>
