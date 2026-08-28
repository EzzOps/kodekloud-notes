# Unix socket.
timeout 0
# TCP keepalive.
tcp-keepalive {{ tcp_keepalive | default('300') }}
daemonize no
supervised no
```

When rendered, this might produce:

```yaml theme={null}
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

### Generating Configurations with Jinja2 Loops

Jinja2 loops allow you to generate configuration file entries dynamically. For example, you can generate a list of nameserver entries for the `/etc/resolv.conf` file using a for loop.

#### Template for resolv.conf (resolv.conf.j2)

```jinja2 theme={null}


nameserver {{ name_server }}


```

Given the following variable definition:

```yaml theme={null}
name_servers:
  - 10.1.1.2
  - 10.1.1.3
  - 8.8.8.8
```

The generated `/etc/resolv.conf` file will be:

```ini theme={null}
nameserver 10.1.1.2
nameserver 10.1.1.3
nameserver 8.8.8.8
```

> **Note:** When using templates within roles, ensure they are stored in the role's dedicated `templates` directory.

## Templates in Roles Directory Structure

An effective directory structure for organizing your Ansible roles might look like the image below:

<Frame>
  ![The image shows a directory structure for "Templates in Roles," including folders for "mysql," "tasks," "handlers," and files like "README.md" and "templates."](https://kodekloud.com/kk-media/image/upload/v1752881078/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Jinja2-Templates-for-Dynamic-Configs-Demo/frame_460.jpg)
</Frame>

By leveraging Jinja2 templates and Ansible's extended filters, you can efficiently deploy dynamic configurations across your infrastructure while reducing redundancy and manual intervention. This approach not only simplifies management but also enhances the consistency and scalability of your deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/920849be-3dc5-4a4a-b398-67d89b67c710/lesson/c2585e90-5d41-41e1-b3df-2e0f872cf015" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/920849be-3dc5-4a4a-b398-67d89b67c710/lesson/a2362795-1391-4e14-9a02-6f936635c37c" />
</CardGroup>


# Ansible Facts

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Variables-and-Facts/Ansible-Facts/page

This article explores how Ansible collects system information, known as Facts, during playbook execution for efficient automation.

In this lesson, we explore how Ansible collects system information, known as Facts, during playbook execution. When a playbook runs, Ansible connects to each target machine and automatically gathers essential details such as:

* **Architecture** (e.g., 32-bit vs 64-bit)
* **Operating system version**
* **Processor and memory specifications**
* **Network interfaces, IP addresses, FQDN, and MAC addresses**
* **Disk details**

This comprehensive data collection is managed by the setup module, which is executed automatically at the beginning of every playbook unless explicitly disabled.

<Callout icon="lightbulb">
  The collected data is stored in the variable `ansible_facts`, which can be used in subsequent tasks to tailor configurations and decisions based on system characteristics.
</Callout>

## Simple Playbook Example

Consider the following playbook that prints a simple hello message. Even though only the debug task is specified in the playbook, Ansible first gathers facts from each host:

```yaml theme={null}
---
- name: Print hello message
  hosts: all
  tasks:
    - debug:
        msg: Hello from Ansible!
```

When you run this playbook, the output includes two key tasks: one that gathers facts and another that prints the debug message.

```plaintext theme={null}
PLAY [Print hello message] *******************************

TASK [Gathering Facts] ***********************************
ok: [web2]
ok: [web1]

TASK [debug] *********************************************
ok: [web1] => {
    "msg": "Hello from Ansible!"
}
ok: [web2] => {
    "msg": "Hello from Ansible!"
}
```

## Displaying Ansible Facts

To gain deeper insights, you can modify your playbook to print the `ansible_facts` variable instead of a simple message. This approach allows you to view extensive system details for each host:

```yaml theme={null}
---
- name: Print Ansible Facts
  hosts: all
  tasks:
    - debug:
        var: ansible_facts
```

Running this playbook produces output similar to the example below, featuring details such as IP configurations, system architecture, operating system information, DNS settings, and memory statistics:

```plaintext theme={null}
PLAY [Reset nodes to previous state] *********************************************************************** 

TASK [Gathering Facts] ***************************************************************************************
ok: [web2]
ok: [web1]

TASK [debug] ************************************************************************************************
ok: [web1] =>
  "ansible_facts": {
    "all_ipv4_addresses": [
      "172.20.1.100"
    ],
    "architecture": "x86_64",
    "date_time": {
      "date": "2019-09-07",
    },
    "distribution": "Ubuntu",
    "distribution_file_variety": "Debian",
    "distribution_major_version": "16",
    "distribution_release": "xenial",
    "distribution_version": "16.04",
    "dns": {
      "nameservers": [
        "127.0.0.11"
      ]
    },
    "fqdn": "web1",
    "hostname": "web1",
    "interfaces": [
      "lo",
      "eth0"
    ],
    "machine": "x86_64",
    "memfree_mb": 72,
    "memory_mb": {
      "real": {
        "free": 72,
        "total": 985,
        "used": 913
      }
    }
  },
```

The rich details provided by `ansible_facts` can be invaluable when configuring systems dynamically—whether you are setting up logical volumes, managing network settings, or optimizing system performance based on the hardware characteristics of your servers.

## Disabling Fact Gathering

If your playbook does not require this additional overhead of gathering facts, you can disable it by setting the `gather_facts` option to `no`:

```yaml theme={null}
---
- name: Print hello message without gathering facts
  hosts: all
  gather_facts: no
  tasks:
    - debug:
        var: ansible_facts
```

With `gather_facts: no`, Ansible skips the facts collection phase and executes only the specified tasks. Note that fact-gathering behavior can be further controlled by the setting in the Ansible configuration file (typically located at `/etc/ansible/ansible.cfg`):

```plaintext theme={null}
