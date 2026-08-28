# /etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102

[web_servers]
web1
web2
web3

[web_servers:vars]
dns_server=10.5.5.3
```

## Host Versus Group Variables

When the same variable is defined both on the host level and in the group, the host-specific variable takes precedence. Consider modifying the inventory for "web2" as follows:

```bash theme={null}
# /etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101  dns_server=10.5.5.4
web3 ansible_host=172.20.1.102

[web_servers]
web1
web2
web3

[web_servers:vars]
dns_server=10.5.5.3
```

In this scenario, Ansible first associates the group variable (dns\_server=10.5.5.3) with all hosts. However, since "web2" is explicitly defined with its own variable (dns\_server=10.5.5.4), that value is used during playbook execution.

## Variables Defined in Playbooks

Variables can also be declared directly within a playbook. Defining variables at the play level overrides both host and group inventory variables. For example, consider the following playbook that configures the DNS server using a play-level variable:

```yaml theme={null}
---
- name: Configure DNS Server
  hosts: all
  vars:
    dns_server: 10.5.5.5
  tasks:
    - name: Update DNS settings
      nsupdate:
        server: '{{ dns_server }}'
```

Here, the playbook variable (dns\_server: 10.5.5.5) overrides the inventory-defined values during playbook runtime.

## Extra Variables from the Command Line

Extra variables passed via the command line have the highest precedence in Ansible. For instance, running the following command:

```bash theme={null}
$ ansible-playbook playbook.yml --extra-vars "dns_server=10.5.5.6"
```

ensures that the value provided (dns\_server=10.5.5.6) supersedes any values defined in the inventory or playbook. The command below demonstrates a similar override with a different value:

```bash theme={null}
$ ansible-playbook playbook.yml --extra-vars "dns_server=10.5.6"
```

In both cases, the extra variable takes precedence over all others.

## Overview of Precedence

Ansible applies variables following a defined hierarchical order. The order starts from the lowest precedence (role default variables), then proceeds through inventory and playbook variables, and finally applies extra vars provided directly on the command line (the highest precedence). This structure guarantees that more specific variables override more general ones.

<Frame>
  ![The image shows a list of Ansible variable precedence, detailing the order in which variables are applied, from role defaults to extra vars.](https://kodekloud.com/kk-media/image/upload/v1752869409/notes-assets/images/Ansible-Advanced-Course-Variable-Precedence/frame_190.jpg)
</Frame>

That concludes our discussion on variable precedence in Ansible. In the next article, we will explore additional methods to manage and override variables effectively in your Ansible deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/15e6b588-6cfc-48cd-a773-e365ac3a32ef/lesson/dd9f5da1-334f-4a98-b268-7fc6d22cad8b" />
</CardGroup>


# Variable Scope

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Variables-and-Jinja2/Variable-Scope/page

This article explores variable scope in Ansible, detailing how variable definitions affect their accessibility across hosts and plays.

In this article, we explore the concept of variable scope in Ansible and explain how the location where variables are defined determines their accessibility.

## Host-Level Variables

Consider an inventory file where the DNS server is specified only for the host `web2`:

```ini theme={null}
/etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101 dns_server=10.5.5.4
web3 ansible_host=172.20.1.102
```

In this example, running a playbook that prints the `dns_server` variable for all hosts results in the variable being defined only for `web2`:

```yaml theme={null}
---
- name: Print DNS Server
  hosts: all
  tasks:
    - debug:
        msg: "{{ dns_server }}"
```

The output will be:

```Ansible theme={null}
PLAY [Check /etc/hosts file] *********************************************************
TASK [debug] *********************************************************************
ok: [web1] => {
    "dns_server": "VARIABLE IS NOT DEFINED!"
}
ok: [web2] => {
    "dns_server": "10.5.5.4"
}
ok: [web3] => {
    "dns_server": "VARIABLE IS NOT DEFINED!"
}
```

This demonstrates the host scope: each host only accesses the variables defined specifically for it.

<Frame>
  ![The image illustrates a network diagram showing variable scopes for hosts, including web servers (web1, web2, web3) and a DNS server with IP 10.5.5.4.](https://kodekloud.com/kk-media/image/upload/v1752869410/notes-assets/images/Ansible-Advanced-Course-Variable-Scope/frame_60.jpg)
</Frame>

When a playbook runs, Ansible associates variables with each host based on inventory and group variable files. By default, the primary scope during playbook execution is the host scope.

## Play-Level Variables

Next, consider a scenario where a variable is defined within a play. In the following playbook, the variable `ntp_server` is defined only in the first play, making it accessible there but not in the second play:

```yaml theme={null}
---
- name: Play1
  hosts: web1
  vars:
    ntp_server: 10.1.1.1
  tasks:
    - debug:
        var: ntp_server

- name: Play2
  hosts: web1
  tasks:
    - debug:
        var: ntp_server
```

The output will be:

```Ansible theme={null}
PLAY [Play1] *********************************************************************
TASK [debug] *********************************************************************
ok: [web1] => {
    "ntp_server": "10.1.1.1"
}

PLAY [Play2] *********************************************************************
TASK [debug] *********************************************************************
ok: [web1] => {
    "ntp_server": "VARIABLE IS NOT DEFINED!"
}
```

This example illustrates the play scope: variables defined in one play do not automatically carry over to subsequent plays.

## Global Variables

Global (or extra) variables are available throughout the entire execution of a playbook. For instance, if you run the playbook with an extra variable like so:

```bash theme={null}
$ ansible-playbook playbook.yml --extra-vars "ntp_server=10.1.1.1"
```

And use this playbook:

```yaml theme={null}
---
- name: Play1
  hosts: web1
  vars:
    ntp_server: 10.1.1.1
  tasks:
    - debug:
        var: ntp_server

- name: Play2
  hosts: web1
  tasks:
    - debug:
        var: ntp_server
```

Both plays will have access to the `ntp_server` variable, producing the following output:

```Ansible theme={null}
PLAY [Play1] *****************************************************************
TASK [debug] ******************************************************************
ok: [web1] => {
  "ntp_server": "10.1.1.1"
}

PLAY [Play2] *****************************************************************
TASK [debug] ******************************************************************
ok: [web1] => {
  "ntp_server": "10.1.1.1"
}
```

## Conclusion

Understanding variable scopes—host, play, and global—is essential for managing configurations and troubleshooting within Ansible playbooks. Each scope offers a level of variable visibility that can be strategically utilized to create efficient and modular playbooks.

<Callout icon="lightbulb">
  For further details on variable precedence and advanced usage, consult the [Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html).
</Callout>

Thank you for reading, and happy automating!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/15e6b588-6cfc-48cd-a773-e365ac3a32ef/lesson/31b7636d-5056-48e5-aedf-b9c554e01e58" />
</CardGroup>
