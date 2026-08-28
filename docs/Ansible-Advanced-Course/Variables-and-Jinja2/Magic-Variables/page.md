# /etc/ansible/hosts
web1 ansible_host=172.20.1.100 dns_server=10.5.5.4
web2 ansible_host=172.20.1.101 dns_server=10.5.5.4
web3 ansible_host=172.20.1.102 dns_server=10.5.5.4

---

- name: Update DNS server
  hosts: all
  tasks:
    - nsupdate:
        server: '{{ dns_server }}'
```

<Callout icon="lightbulb">
  For more examples and detailed explanations on using filters with Ansible, please visit the [Ansible documentation on filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html).
</Callout>

<Frame>
  ![The image lists links to Jinja2 and Ansible documentation for additional filters, with URLs provided for each.](https://kodekloud.com/kk-media/image/upload/v1752869408/notes-assets/images/Ansible-Advanced-Course-Jinja2-in-Ansible/frame_160.jpg)
</Frame>

## Hands-On Exercises

The first exercise introduces you to an emulated environment where you can practice working with Jinja2 independently. After gaining some experience, you will transition into an Ansible lab exercise designed to cement your understanding of integrating Jinja2 filters with Ansible playbooks.

Good luck with the exercises and enjoy exploring the powerful combination of Jinja2 and Ansible!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/15e6b588-6cfc-48cd-a773-e365ac3a32ef/lesson/50db62dc-0edc-4b1a-b8d7-f4aeb7076f81" />
</CardGroup>


# Magic Variables

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Variables-and-Jinja2/Magic-Variables/page

This article explores how magic variables in Ansible simplify accessing variables across hosts and enhance playbook functionality.

In this article, we explore how magic variables in Ansible simplify accessing variables across hosts. Previously, we delved into variable scopes and saw that host variables are defined for each individual host. Now, we will build on that foundation using magic variables.

## Inventory File Example

Consider the following inventory file, where a DNS server is specified for host "web2":

```text theme={null}
/etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101 dns_server=10.5.5.4
web3 ansible_host=172.20.1.102
```

When an Ansible playbook starts, it creates separate subprocesses for each host. Before executing tasks on these hosts, Ansible performs variable interpolation by gathering variables from multiple sources and associating them with their respective hosts. As a result, the DNS server IP defined for "web2" is available solely on that host.

> **Tip:**
> If you need to access the DNS server information from another host, magic variables offer a clean solution.

## Using the "hostvars" Magic Variable

The magic variable `hostvars` enables you to retrieve variables set on one host from another host. For example, to retrieve the DNS server defined on "web2", use the following playbook:

```yaml theme={null}
---
- name: Print DNS server IP
  hosts: all
  tasks:
    - debug:
        msg: "{{ hostvars['web2'].dns_server }}"
```

```Ansible theme={null}
PLAY [Check /etc/hosts file] **********************************************************************************

TASK [debug] **************************************************************************************************
ok: [web1] => {
    "dns_server": "10.5.5.4"
}
ok: [web2] => {
    "dns_server": "10.5.5.4"
}
ok: [web3] => {
    "dns_server": "10.5.5.4"
}
```

Because each host is defined with an `ansible_host` parameter, gathering facts permits access to detailed information about other hosts. This includes architecture, devices, mounts, processors, and more. Everything available from a host’s facts can be accessed with `hostvars`. For instance:

```yaml theme={null}
---
- name: Print details from web2
  hosts: all
  tasks:
    - debug:
        msg: "{{ hostvars['web2'].dns_server }}"
    - debug:
        msg: "{{ hostvars['web2'].ansible_host }}"
    - debug:
        msg: "{{ hostvars['web2'].ansible_facts.architecture }}"
    - debug:
        msg: "{{ hostvars['web2'].ansible_facts.devices }}"
    - debug:
        msg: "{{ hostvars['web2'].ansible_facts.mounts }}"
    - debug:
        msg: "{{ hostvars['web2'].ansible_facts.processor }}"
```

Both expression formats yield the same results. You may notice that the official Ansible documentation sometimes presents these expressions with slight variations.

## Exploring Other Magic Variables: "groups" and "group\_names"

Another essential magic variable is `groups`. It returns a list of all hosts within a specified group. In contrast, `group_names` returns all the groups that the current host belongs to.

### Inventory Example with Groups

```Ansible theme={null}
/etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102

[web_servers]
web1
web2
web3

[americas]
web1
web2

[asia]
web3
```

To retrieve the list of hosts in the "americas" group, you can use:

```yaml theme={null}
- debug:
    msg: "{{ groups['americas'] }}"
```

When running a playbook on host "web1", the `group_names` variable returns the groups that host is a member of (for instance, "web\_servers" and "americas"):

```yaml theme={null}
msg: "{{ group_names }}"
```

## Understanding "inventory\_hostname"

A related magic variable, `inventory_hostname`, returns the hostname as specified in the inventory file rather than its fully qualified domain name (FQDN). For example:

```Ansible theme={null}
/etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102

[web_servers]
web1
web2
web3

[americas]
web1
web2

[asia]
web3
```

```yaml theme={null}
msg: "{{ inventory_hostname }}"
```

> **Further Reading:**
> For more details on magic variables, consult the official Ansible documentation, especially the sections on variable usage in playbooks.

## Magic Variables in Jinja2 Templates

Magic variables can also be extremely useful in Jinja2 templates. Below are a couple of examples:

```text theme={null}
{{ hostvars['test.example.com']['ansible_facts']['distribution'] }}
```

```jinja2 theme={null}
