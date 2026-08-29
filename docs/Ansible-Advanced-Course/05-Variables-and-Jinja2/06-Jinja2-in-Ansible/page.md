# variables.yml
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

## Using Jinja2 in Ansible

Ansible uses Jinja2 templating everywhere: playbooks, task parameters, templates, and inventory. Example: using a variable for a file path in a task.

Template playbook:

```yaml theme={null}
# playbook.yml (template)
- hosts: web1
  tasks:
    - name: Create a file at a path from a variable
      file:
        path: "{{ file }}"
        state: touch
```

Variables:

```yaml theme={null}
# vars.yml
file: /tmp/1.txt
```

Rendered task after substitution:

```yaml theme={null}
- hosts: web1
  tasks:
    - name: Create a file at a path from a variable
      file:
        path: /tmp/1.txt
        state: touch
```

You can template configuration files too. Example MySQL configuration template and result.

Template:

```ini theme={null}
# my.cnf.j2 (template)
[mysqld]
innodb-buffer-pool-size={{ pool_size }}
datadir={{ datadir }}
user={{ mysql_user }}
```

Variables:

```yaml theme={null}
# vars.yml
pool_size: 128M
datadir: /var/lib/mysql
mysql_user: mysql
```

Rendered configuration:

```ini theme={null}
[mysqld]
innodb-buffer-pool-size=128M
datadir=/var/lib/mysql
user=mysql
```

## What is Jinja2?

Jinja2 is a full-featured, powerful templating engine for Python. It provides a compact syntax for:

* Expressions that output values
* Control structures (loops, conditionals)
* Template inheritance (blocks)
* Filters to transform values
* Tests to check values (defined, none, etc.)

Use Jinja2 to create reusable templates for web pages, configuration files, cloud templates, and automation playbooks.

## Common Jinja2 constructs

* Expressions: `{{ ... }}` — evaluate and output a value.
* Statements: `{% ... %}` — control structures like for/if or block definitions.
* Comments: `{# ... #}` — template comments not rendered in output.

### Blocks and template inheritance

Blocks let a base template define placeholders that child templates can override.

Example:

```html theme={null}
<title>{% block title %}{% endblock %}</title>
<ul>
  {% for user in users %}
  <li><a href="{{ user.url }}">{{ user.username }}</a></li>
  {% endfor %}
</ul>
```

### Filters: transform values inline

Filters use the pipe (|) syntax and let you transform a variable before rendering.

* Strings: upper, lower, title, replace, default
* Sequences: min, max, unique, union, intersect, random, join

Examples:

```jinja theme={null}
The name is {{ my_name }}                      => The name is Bond
The name is {{ my_name | upper }}              => The name is BOND
The name is {{ my_name | lower }}              => The name is bond
The name is {{ my_name | title }}              => The name is Bond
The name is {{ my_name | replace("Bond","Bourne") }} => The name is Bourne
{{ first_name | default("James") }} {{ my_name }}     => James Bond   # if first_name undefined
```

> **lightbulb** Use filters to transform values inline. The default filter prevents
  undefined-variable errors by providing a fallback.

Table: selected filters, use cases, and examples

\| Filter              | Use case                          | Example          |
\| ------------------- | --------------------------------- | ---------------- | ----------------------------------- |
\| upper, lower, title | Normalize string case             | `{{ name         | upper }}` -> "BOND"                 |
\| replace             | Replace substrings                | `{{ text         | replace("a","b") }}`                |
\| default             | Fallback when undefined           | `{{ value        | default("N/A") }}`                  |
\| join                | Join list elements into a string  | `{{ words        | join(" ") }}` -> "The name is Bond" |
\| unique              | Remove duplicates from a sequence | `{{ [1,2,2]      | unique }}` -> \[1,2]                 |
\| union, intersect    | Combine or intersect sequences    | `{{ [1,2]        | union([2,3]) }}` -> \[1,2,3]         |
\| random              | Pick a random element             | `{{ range(1,201) | random }}` -> random 1–200          |

Selected examples (sequence filters):

```jinja theme={null}
{{ [1, 2, 3] | min }}                => 1
{{ [1, 2, 3] | max }}                => 3
{{ [1, 2, 3, 2] | unique }}          => [1, 2, 3]
{{ [1, 2, 3, 4] | union([4, 5]) }}   => [1, 2, 3, 4, 5]
{{ [1, 2, 3, 4] | intersect([4, 5]) }} => [4]
{{ range(1, 201) | random }}         => Random number between 1 and 200
{{ ["The", "name", "is", "Bond"] | join(" ") }} => The name is Bond
```

### Blocks vs expressions

* Use `{{ ... }}` when you want to output a value or the result of an expression.
* Use `{% ... %}` for control flow, including loops, conditionals, and block definitions.

### Loops and conditionals

Example template that prints a message for numbers 0–4 and highlights when the number equals 2:

```jinja theme={null}
{% for number in [0, 1, 2, 3, 4] %}
  {% if number == 2 %}
    Number is two
  {% else %}
    Number is not two
  {% endif %}
{% endfor %}
```

Rendered output:

```text theme={null}
Number is not two
Number is not two
Number is two
Number is not two
Number is not two
```

## When to use Jinja2 templates

| Resource Type                                     | Use Case                                         |
| ------------------------------------------------- | ------------------------------------------------ |
| HTML pages                                        | Render dynamic web pages with consistent layouts |
| Configuration files                               | Generate valid configs for services and daemons  |
| Automation scripts (Ansible, Terraform templates) | Inject variables into tasks and manifests        |
| Email or document generation                      | Produce personalized documents at scale          |

## Next steps and references

Jinja2 provides many more filters, tests, and extension points. Combine filters, tests, template inheritance, and macros to build clean, maintainable templates for web apps, automation, and infrastructure.

Links and references:

* Jinja2 documentation: [https://jinja.palletsprojects.com/](https://jinja.palletsprojects.com/)
* Ansible templating: [https://docs.ansible.com/ansible/latest/user\_guide/playbooks\_templating.html](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)
* Ansible Advanced Course: [https://learn.kodekloud.com/user/courses/ansible-advanced-course](https://learn.kodekloud.com/user/courses/ansible-advanced-course)

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/15e6b588-6cfc-48cd-a773-e365ac3a32ef/lesson/3a267fe3-05a8-463b-9457-0242a8107200)


# Jinja2 in Ansible

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Variables-and-Jinja2/Jinja2-in-Ansible/page

This article focuses on how Ansible enhances Jinja2 with custom filters for managing infrastructure tasks.

In our previous guide, we explored the basic features of Jinja2. In this document, we focus on how Ansible enhances Jinja2 with custom filters specifically designed for managing infrastructure. For more details on Jinja2 filters, refer to the [Jinja2 documentation](https://jinja.palletsprojects.com/).

Ansible extends the built-in Jinja2 filters with additional options to handle practical tasks such as converting YAML and JSON, managing file names and directory paths across Linux and Windows, and processing passwords and regular expressions. Here, we emphasize file-related filters.

## File-Related Filters

To extract the file name from a complete path on a Linux system, you use the `basename` filter. For example, given the path `/etc/hosts`, applying the `basename` filter returns `hosts`. However, note that this method does not work with Windows paths—which use backslashes. Instead, use the `win_basename` filter for Windows paths.

To separate the drive letter from the rest of a Windows path, use the `win_splitdrive` filter. This filter returns an array where the first element is the drive letter and the second element is the remaining path. If you need only the drive letter, simply chain the `first` filter to the result.

### Examples of File-Related Filters

Below are examples demonstrating how to use these filters:

```jinja theme={null}
{{ "/etc/hosts" | basename }}
{{ "c:\windows\hosts" | win_basename }}
{{ "c:\windows\hosts" | win_splitdrive }}
```

To extract only the drive letter from a Windows path, chain the filters as follows:

```jinja theme={null}
{{ "c:\windows\hosts" | win_splitdrive | first }}
```

Similarly, if you need just the path without the drive letter, chain the `last` filter:

```jinja theme={null}
{{ "c:\windows\hosts" | win_splitdrive | last }}
```

## Integrating Jinja2 with Ansible Playbooks

Before executing an Ansible playbook, Ansible processes the file through the Jinja2 templating engine. This step replaces variables with actual values from the inventory, ensuring the final playbook is ready for execution.

Consider the example below, which includes a simple inventory file and a playbook that updates the DNS server settings:

```yaml theme={null}
