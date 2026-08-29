# Unix socket.
timeout 0
# TCP keepalive.
tcp-keepalive {{ tcp_keepalive | default('300') }}
daemonize no
supervised no
```

When rendered, if no explicit value is provided for redis\_port or tcp\_keepalive, the configuration defaults to 6379 and 300 respectively:

```plaintext theme={null}
bind 192.168.1.100
protected-mode yes
port 6379
tcp-backlog 511
# Unix socket.
timeout 0
# TCP keepalive.
tcp-keepalive 300
daemonize no
supervised no
```

You can also incorporate Jinja2 control structures. For example, to generate multiple nameserver entries in an `/etc/resolv.conf` file using a loop:

```jinja2 theme={null}


nameserver {{ name_server }}


```

Given the following array of nameservers:

```yaml theme={null}
name_servers:
  - 10.1.1.2
  - 10.1.1.3
  - 8.8.8.8
```

The rendered file would be:

```plaintext theme={null}
nameserver 10.1.1.2
nameserver 10.1.1.3
nameserver 8.8.8.8
```

!!! note "Best Practice"
When using templates within roles, it is recommended to place them under the role's templates directory for better organization and maintenance.

To further enhance your understanding, try applying these techniques in a hands-on exercise with Ansible templates. This practical experience will help solidify your grasp on dynamically generating configuration files with Jinja2 and Ansible.

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/15e6b588-6cfc-48cd-a773-e365ac3a32ef/lesson/644fe328-43be-420a-a519-0566eee0ea99)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/15e6b588-6cfc-48cd-a773-e365ac3a32ef/lesson/addfa587-40d2-45ce-bb84-ac1f3084f67a)


# Jinja2 Basics

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Variables-and-Jinja2/Jinja2-Basics/page

Introduction to Jinja2 templating basics, syntax, filters, and practical examples for generating HTML, configuration files, and Ansible templates

Templating lets you separate fixed structure (the template) from changing content (the variables). For example, a company's CEO may want to send a personalized invitation to every employee: the letter layout remains the same (the template) while names and family members vary (the variables). A templating engine takes a template plus a set of variables and renders one or many final outputs (one email or hundreds).

<Frame>
  <img
    alt="A dark presentation slide titled &#x22;Templating Engine&#x22; showing four colored
text boxes, each containing a sample invitation letter addressed to different
people. The letters have different colored monospaced text (yellow, orange,
blue, green) on black
panels."
  />
</Frame>

In IT, templating is widely used to generate HTML pages, configuration files, or inputs for automation tools such as Ansible. Keep a template file and feed variables to produce valid output automatically.

## Simple HTML templating example

Template:

```html theme={null}
<!-- template.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
    {{ msg }}
  </body>
</html>
```

Variables:

```yaml theme={null}
