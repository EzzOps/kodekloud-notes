# /etc/ansible/ansible.cfg
# By default, plays will gather facts automatically. The settings include:
# smart     - Gather by default, but do not regather if already gathered
# implicit  - Gather by default, turn off with gather_facts: False
# explicit  - Do not gather by default; must enable with gather_facts: True
gathering = implicit
```

If both the playbook and configuration file specify fact-gathering options, the playbook setting takes precedence.

## Targeted Fact Gathering

Remember that Ansible collects facts only for the hosts included in the playbook. For example, if your inventory has two hosts (web1 and web2) but you run the playbook only on web1, facts will be gathered solely for web1:

```yaml theme={null}
---
- name: Print Ansible Facts for web1 only
  hosts: web1
  tasks:
    - debug:
        var: ansible_facts
```

This behavior might result in missing facts for hosts not targeted by the playbook.

Later in this lesson, we will delve into how to parse and utilize these facts in conjunction with variables and Jinja2 templates to create dynamic and adaptable playbook configurations.

***

By understanding and leveraging Ansible Facts, you can create more efficient, responsive, and tailored automation scripts that adapt based on the actual state and configuration of your systems.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/c85e487f-ca75-448b-b7dd-f72e9519d9b9/lesson/f8cb5a3e-d4c8-4412-ba10-a332b7ea6b66" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/c85e487f-ca75-448b-b7dd-f72e9519d9b9/lesson/a34818eb-2eea-44c9-847a-86d1db6ca208" />
</CardGroup>


# Ansible Variables

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Variables-and-Facts/Ansible-Variables/page

This article explores how to define and use variables in Ansible playbooks and inventory files for flexibility and scalability.

In this lesson, we will explore how variables work in Ansible. Variables in Ansible serve the same purpose as in other scripting or programming languages: they store dynamic values that can differ between systems or tasks. For instance, when applying patches with a single playbook to hundreds of servers, variables provide unique information such as hostnames, usernames, or passwords for each server.

## Variables in Inventory Files

Previously, we encountered variables within the inventory file. In the example below, variables define settings such as the Ansible host, connection type, and SSH password:

```ini theme={null}
Web1 ansible_host=server1.company.com ansible_connection=ssh ansible_ssh_pass=P@ssW
db ansible_host=server2.company.com ansible_connection=winrm ansible_ssh_pass=P@s
Web2 ansible_host=server3.company.com ansible_connection=ssh ansible_ssh_pass=P@ssW
```

## Defining Variables in Playbooks

Variables can also be declared directly within a playbook. Consider the following playbook that adds a DNS entry to the `/etc/resolv.conf` file. Here, the variable `dns_server` is defined using the `vars` directive:

```yaml theme={null}
- name: Add DNS server to resolv.conf
  hosts: localhost
  vars:
    dns_server: 10.1.250.10
  tasks:
    - lineinfile:
        path: /etc/resolv.conf
        line: "nameserver 10.1.250.10"
```

However, the above playbook contains a hard-coded IP address. To improve its flexibility, replace the fixed IP with the variable `dns_server` using Jinja2 templating. Simply enclose the variable name in double curly braces:

```yaml theme={null}
- name: Add DNS server to resolv.conf
  hosts: localhost
  vars:
    dns_server: 10.1.250.10
  tasks:
    - lineinfile:
        path: /etc/resolv.conf
        line: "nameserver {{ dns_server }}"
```

## Using Variables for Firewall Configurations

Consider a playbook for configuring a firewall. The playbook below sets various firewall rules. However, many values are hard-coded, making it difficult to reuse the playbook in different scenarios:

```yaml theme={null}
- name: Set Firewall Configurations
  hosts: web
  tasks:
    - firewalld:
        service: https
        permanent: true
        state: enabled

    - firewalld:
        port: 8081/tcp
        permanent: true
        state: disabled

    - firewalld:
        port: 161-162/udp
        permanent: true
        state: disabled

    - firewalld:
        source: 192.0.2.0/24
        Zone: internal
        state: enabled
```

A more flexible approach is to move these values into the inventory or a dedicated variables file. When using the inventory file, the playbook refers to variables using Jinja2 templating. Modifying the inventory file alone updates the playbook's behavior without editing the playbook itself. An even more organized strategy is to store host-specific variables in a file such as `web.yml`, ensuring these values are automatically available when the playbook runs.

<Callout icon="lightbulb">
  When incorporating a variable into a string, enclose it within quotes if the variable appears at the beginning. However, if it appears in the middle of the string, quotes are not strictly necessary.
</Callout>

Below is an updated example of the firewall configuration playbook using variables:

```yaml theme={null}
- name: Set Firewall Configurations
  hosts: web
  tasks:
    - firewalld:
        service: https
        permanent: true
        state: enabled

    - firewalld:
        port: "{{ http_port }}/tcp"
        permanent: true
        state: disabled

    - firewalld:
        port: "{{ snmp_port }}/udp"
        permanent: true
        state: disabled

    - firewalld:
        source: "{{ inter_ip_range }}/24"
        zone: internal
        state: enabled
```

### Sample Variable Definitions

The following examples demonstrate how variables can be defined in both the inventory file and a dedicated variable file.

**Inventory File Example:**

```ini theme={null}
